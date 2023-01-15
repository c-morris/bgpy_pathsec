from bgp_simulator_pkg import Relationships

from ..policies import BGPsecTransitiveDownOnlyAS


class BGPsecTransitiveDownOnlyEncrUpAS(BGPsecTransitiveDownOnlyAS):

    name = "BGPsec Transitive Down Only Encrypted UP"

    __slots__ = tuple()
    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        BGPsecTransitiveAS.count += len(ann.bgpsec_path)
        return (super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship) and  # noqa E501
                self.passes_down_only_checks(ann, recv_relationship) and
                len(ann.removed_signatures) == 0 and
                (recv_relationship != Relationships.CUSTOMERS or
                 ann.up_pre))

    def down_only_modifications(self, as_obj, ann_to_send, propagate_to, *args, **kwargs): # noqa E501
        # UP preimage modifications
        if propagate_to in (Relationships.CUSTOMERS, Relationships.PEERS):
            ann_to_send.up_pre = False
        super(BGPsecTransitiveDownOnlyEncrUpAS, self).down_only_modifications(
              as_obj,
              ann_to_send,
              propagate_to,
              *args,
              **kwargs)

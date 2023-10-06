from typing import Optional
from copy import deepcopy

from bgp_simulator_pkg import BGPAS, Relationships
from bgp_simulator_pkg import Announcement as Ann


opt_bool = Optional[bool]


class BGPsecAS(BGPAS):

    name = "BGPsec"

    # Total number of signatures verified
    count = 0
    # Total number of signatures verified (BPO)
    bpo_count = 0

    __slots__ = tuple()

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        if len(ann.bgpsec_path) == len(ann.as_path):
            BGPsecAS.count += len(ann.bgpsec_path)
            # print(f"Added {len(ann.bgpsec_path)} at {self.asn} for total")
            # print(f"BGPsecAS {BGPsecAS.count}")
        return super(BGPsecAS, self)._valid_ann(ann, recv_relationship)

    def _process_outgoing_ann(self, as_obj, ann, *args):

        # Set next_as for bgpsec
        next_as = as_obj.asn if ann.next_as == self.asn else ann.next_as

        super(BGPsecAS, self)._process_outgoing_ann(as_obj,
                                                    ann.copy(overwrite_default_kwargs={'next_as':next_as}), # noqa E501
                                                    *args)

    # As of July 2022 the preferred behavior is security third
    # The function below does not run, but is saved as an example
    # Rename function and comment out the other one for security second
    def _security_second_new_ann_better(self,
                                        current_ann,
                                        current_processed,
                                        default_current_recv_rel,
                                        new_ann,
                                        new_processed,
                                        default_new_recv_rel):
        """Assigns the priority to an announcement according to Gao Rexford
        """

        new_rel_better: opt_bool = self._new_rel_better(current_ann, # noqa F821
                                                        current_processed,
                                                        default_current_recv_rel, # noqa E501
                                                        new_ann,
                                                        new_processed,
                                                        default_new_recv_rel)
        if new_rel_better is not None:
            return new_rel_better
        else:
            # bgpsec_better = self._new_ann_better_bgpsec(current_ann,
            #                                             current_processed,
            #                                             new_ann,
            #                                             new_processed)
            # if (bgpsec_better is not None):
            #     return bgpsec_better
            # else:
                return self._new_as_path_ties_better(current_ann,
                                                     current_processed,
                                                     new_ann,
                                                     new_processed)

    def _new_as_path_ties_better(self,
                                 current_ann: Optional[Ann],
                                 current_processed: bool,
                                 new_ann: Ann,
                                 new_processed: bool) -> opt_bool:

        new_as_path_shorter: opt_bool = self._new_as_path_shorter(
            current_ann, current_processed, new_ann, new_processed)

        if new_as_path_shorter is not None:
            return new_as_path_shorter
        else:
            # Security Third
            # bgpsec_better = self._new_ann_better_bgpsec(current_ann,
            #                                             current_processed,
            #                                             new_ann,
            #                                             new_processed)
            # if (bgpsec_better is not None):
            #     return bgpsec_better
            # else:
                return self._new_wins_ties(current_ann,
                                           current_processed,
                                           new_ann,
                                           new_processed)

    def _new_ann_better_bgpsec(self,
                               current_ann,
                               current_processed,
                               new_ann,
                               new_processed):
        # This is BGPsec Security Third, where announcements with security
        # attributes are preferred over those without, but only after
        # considering path length.
        if current_processed:
            current_path = current_ann.as_path[1:]
            current_bgpsec_path = current_ann.bgpsec_path[1:]
        else:
            current_path = current_ann.as_path
            current_bgpsec_path = current_ann.bgpsec_path
        if new_processed:
            new_path = new_ann.as_path[1:]
            new_bgpsec_path = new_ann.bgpsec_path[1:]
        else:
            new_path = new_ann.as_path
            new_bgpsec_path = new_ann.bgpsec_path

        current_ann_valid = current_bgpsec_path == current_path and current_ann.next_as == self.asn # noqa E501
        new_ann_valid = new_bgpsec_path == new_path and new_ann.next_as == self.asn # noqa E501

        if new_ann_valid and not current_ann_valid:
            return True
        elif current_ann_valid and not new_ann_valid:
            return False
        else:
            return None

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          overwrite_default_kwargs=None):
        """Policy modifications to ann"""

        if overwrite_default_kwargs is None:
            overwrite_default_kwargs = dict()
        # Update the BGPsec path
        if ann.bgpsec_path == ann.as_path:
            # If paths are equal, there is an unbroken chain of adopters,
            # otherwise, the attributes are lost
            overwrite_default_kwargs.update({"bgpsec_path": (self.asn, *ann.bgpsec_path)}) # noqa E501
        else:
            overwrite_default_kwargs.update({"bgpsec_path": tuple(), "next_as": 0}) # noqa E501

        # NOTE that after this point ann has been deep copied and processed
        # This means the AS path has 1 extra ASN that you don't need to check
        return super(BGPsecAS, self)._copy_and_process(ann, recv_relationship, overwrite_default_kwargs) # noqa E501

    def process_incoming_anns(self,
                              *,
                              from_rel: Relationships,
                              propagation_round: int,
                              scenario,
                              reset_q: bool = True):
        """Increment BPO counter when the local rib changes"""
        previous_local_rib = deepcopy(self._local_rib)
        super(BGPsecAS, self).process_incoming_anns(from_rel=from_rel,
                                                    propagation_round=propagation_round, # noqa E501
                                                    scenario=scenario,
                                                    reset_q=reset_q)
        for prefix, ann in self._local_rib.prefix_anns():
            if previous_local_rib.get_ann(prefix) != ann:
                BGPsecAS.bpo_count += len(ann.bgpsec_path)

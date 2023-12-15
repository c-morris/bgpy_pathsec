from dataclasses import replace
import random

from bgpy import Relationships

from . import BGPsecTransitiveDownOnlyEncrUpAS, BGPsecTransitiveAS


class KAPKFalseAS(BGPsecTransitiveDownOnlyEncrUpAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalseAS"
    count = 0
    bpo_count = 0
    unknown_adopting_percent = 1.0
    # Specific random generator for KAPKFalseAS and its subclasses
    # for reproduceable experiments
    rand_gen = random.Random("KAPKFalseAS")

    def __init__(self, *args, **kwargs):
        # Set the property of being an unknown adopter for *this* AS only
        self.unknown_adopting = self.rand_gen.random() < (
            self.unknown_adopting_percent / 100.0
        )

        super(KAPKFalseAS, self).__init__(*args, **kwargs)

    def _process_outgoing_ann(
        self, as_obj, ann, propagate_to, send_rels, *args, **kwargs
    ):
        """If this is a unknown adopting AS, add self to list of unkown adopters and removed signatures"""
        ann_to_send = ann
        if self.unknown_adopting:
            # If unknown adopter, add ASN to list of removed signatures and unknown adopting
            ann_to_send = replace(
                ann_to_send,
                unknown_adopters=ann_to_send.unknown_adopters + (self.asn,),
            )

        super(KAPKFalseAS, self)._process_outgoing_ann(
            as_obj, ann_to_send, propagate_to, send_rels, *args, **kwargs
        )

    def _valid_ann(self, ann, recv_relationship: Relationships):
        """Determine if an announcement is valid or should be dropped"""
        # check is AS is in both removed signatures and unknown adopters list
        # if AS is on removed signatures but not unknown adopters, this is a detection
        for signature in ann.removed_signatures:
            if signature not in ann.unknown_adopters:
                return False

        BGPsecTransitiveAS.count += len(ann.bgpsec_path)
        return (
            super(BGPsecTransitiveAS, self)._valid_ann(ann, recv_relationship)
            and self.passes_down_only_checks(ann, recv_relationship)
            and (
                recv_relationship != Relationships.CUSTOMERS
                or (recv_relationship == Relationships.CUSTOMERS and ann.up_pre)
            )
        )


class KAPKFalse01AS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalse01AS"
    unknown_adopting_percent = 20


class KAPKFalse05AS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalse05AS"
    unknown_adopting_percent = 30


class KAPKFalse5AS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalse5AS"
    unknown_adopting_percent = 10


class KAPKFalseAlwaysAS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalseAlwaysAS"
    unknown_adopting_percent = 100.0

    def __init__(self, *args, unknown_adopting_percent=1.0, **kwargs):
        # Set the property of being an unknown adopter for *this* AS only
        # For this test class, this is always true
        self.unknown_adopting = True

        super(KAPKFalseAS, self).__init__(*args, **kwargs)


class KAPKFalseNeverAS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""

    name = "KAPKFalseNeverAS"
    unknown_adopting_percent = 0.0

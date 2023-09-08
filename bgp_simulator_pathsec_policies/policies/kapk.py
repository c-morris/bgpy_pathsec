import random

from . import BGPsecTransitiveDownOnlyEncrUpAS

# TODO:
# 1. Replace transitive_dropping with a more descriptive variable name
# 2. Replace the override of _process_outgoing_ann below with an override for _valid_ann (similar to bgpsec_transitive_do_encr_up.py)
# 3. Run the engine_test to confirm the KAPKFalseAlwaysAS behaves as expected
# 4. Confirm the simulation runs with run/kapk.py
# 5. Generate a sample set of data with 100 trials using run/kapk.py

class KAPKFalseAS(BGPsecTransitiveDownOnlyEncrUpAS):
    """Has unknown adopting status with some probability"""
    name = "KAPKFalseAS"
    count = 0
    bpo_count = 0
    transitive_dropping_percent = 1.0
    # Specific random generator for KAPKFalseAS and its subclasses
    # for reproduceable experiments
    rand_gen = random.Random('KAPKFalseAS')

    def __init__(self,
                 *args,
                 **kwargs):
        # Set the probability of dropping transitive attrs for *this* AS only
        self.transitive_dropping = (
           self.rand_gen.random() < (self.transitive_dropping_percent / 100.0))

        super(KAPKFalseAS, self).__init__(*args,**kwargs)

    def _process_outgoing_ann(self, as_obj, ann, propagate_to, send_rels,
        *args, **kwargs):
        """If this is a transitive dropping AS, drop transitive attributes"""
        ann_to_send = ann.copy()
        if self.transitive_dropping:
            ann_to_send.next_as = 0
            ann_to_send.do_communities = tuple()
            # The signatures removed, if any, will be detected by adopting ASes
            if len(ann_to_send.removed_signatures) == 0:
                ann_to_send.removed_signatures = ann_to_send.bgpsec_path
            ann_to_send.bgpsec_path = tuple()
        super(KAPKFalseAS, self)._process_outgoing_ann(as_obj, ann_to_send,
            propagate_to, send_rels, *args, **kwargs)


class KAPKFalse2AS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""
    name = "KAPKFalse2AS"
    transitive_dropping_percent = 2.0


class KAPKFalse4AS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""
    name = "KAPKFalse4AS"
    transitive_dropping_percent = 4.0


class KAPKFalseAlwaysAS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""
    name = "KAPKFalse8AS"
    transitive_dropping_percent = 100.0
    def __init__(self,
                 *args,
                 transitive_dropping_percent=1.0,
                 **kwargs):
        # Set the probability of dropping transitive attrs for *this* AS only
        # For this test class, this is always true
        self.transitive_dropping = True

        super(KAPKFalseAS, self).__init__(*args, **kwargs)


class KAPKFalseNeverAS(KAPKFalseAS):
    """Has unknown adopting status with some probability"""
    name = "KAPKFalseNeverAS"
    transitive_dropping_percent = 0.0

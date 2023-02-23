#from .shortest_path_export_all_no_hash_up import ShortestPathExportAllNoHashUp
#from .. import TransitiveDroppingNeverAS
#
#
#class ShortestPathExportAllNoHashUpTransitiveDropping(ShortestPathExportAllNoHashUp):
#    """Shortest path Export all strategy, from other works.
#
#    Only leaks a single path (the shortest one) to providers.  This version of
#    the attack accounts for UP attributes and ensures customers of transitive
#    dropping no adopt customer ASes are correctly reverted back to adopting
#    ASes for the next run.
#    """
#
#    def _get_non_default_as_cls_dict(
#            self,
#            engine,
#            percent_adoption,
#            prev_scenario,
#            ):
#        """Returns as class dict
#        """
#        if prev_scenario:
#            non_default_as_cls_dict = dict()
#            for asn, OldASCls in prev_scenario.non_default_as_cls_dict.items():
#                # If the ASN was of the adopting class of the last scenario,
#                if OldASCls == TransitiveDroppingNeverAS:
#                    non_default_as_cls_dict[asn] = self.AdoptASCls
#                # Otherwise keep the AS class as it was
#        super()._get_non_default_as_cls_dict(engine, percent_adoption, prev_scenario)

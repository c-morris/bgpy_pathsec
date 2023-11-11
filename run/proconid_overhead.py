import os
import random
import functools
import logging
from copy import deepcopy
from caida_collector_pkg import CaidaCollector
from bgpy import BGPSimpleAS, SimulationEngine

class ProviderConeNode:
    """
    Class for creating simple trees that can be pruned without modifying the
    AS graph. These are used for computing ProConID Overhead.
    """
    
    def __init__(self, asn):
        self.asn = asn
        self.providers = set()
        self.do_not_prune = False
    
    def __eq__(self, other):
        return self.asn == other.asn

    def __lt__(self, other):
        return self.asn < other.asn

    def __hash__(self):
        return self.asn

class ProviderConeComputation:
    """Compute provider cones for every AS in the CAIDA topology."""

    def __init__(self):
        self.engine = CaidaCollector(BaseASCls=BGPSimpleAS,
                                GraphCls=SimulationEngine,
                                ).run(tsv_path=None)
        # Initialize
        # set of adopting ASes
        self.adopters = set()
        # map of ASNs to the set of ASNs that make up their provider cones
        self.provider_cones = dict()
        # map of ASNs to the set of ASNs verified as part of their provider
        # cone during initial adoption by that AS
        self.initial_overheads = dict()
        # map of ASNs to the set of additional ASNs verified as other ASes 
        # adopt
        self.maintenance_overheads = dict()
        # temporary list of ProviderConeNodes that need to be reset after 
        # pruning to determine overhead
        self.modified_nodes = []
        # list of ASNs that we are tracking the maintenance overhead of
        self.maint_ovh_tracking_list = []
        # dict mapping ASNs to ProviderConeNodes that we are tracking the maintenance
        # overhead of
        self.maint_ovh_tracking = dict()
        # dictionary mapping ASNs to a list of ProviderConeNodes they are in 
        # the provider cone of
        self.proconid_reversemap = dict()
        # cache of nodes checked for not pruning
        self.checked_nodes = set()
        # cache of already validated providers
        self.already_validated_providers = set()
        for as_obj in self.engine.ases:
            self.provider_cones[as_obj.asn] = set()
            self.initial_overheads[as_obj.asn] = set()
            self.maintenance_overheads[as_obj.asn] = set()


    def get_cone(self, as_obj):
        """Compute a provider cone for a single AS"""
        if as_obj.input_clique or len(self.provider_cones[as_obj.asn]) > 0:
            return
        asns_in_cone = set()
        for provider_obj in as_obj.providers:
            if len(self.provider_cones[provider_obj.asn]) == 0:
                self.get_cone(provider_obj)
            asns_in_cone = asns_in_cone.union(self.provider_cones[provider_obj.asn])
            asns_in_cone.add(provider_obj.asn)
        self.provider_cones[as_obj.asn] = asns_in_cone

    def get_all_cones(self):
        """Populate self.provider_cones for every AS"""
        for as_obj in self.engine.ases:
            self.get_cone(as_obj)


    def pruning_overhead_calc(self, asn):
        """Compute initial provider cone verification overhead for an ASN"""
        # add this ASN to the adopters list
        self.adopters.add(asn)

        # update the proconid_reversemap for maintenance ovh tracking
        for pr_asn in self.provider_cones[asn]:
            if pr_asn not in self.proconid_reversemap.keys():
                self.proconid_reversemap[pr_asn] = []
            self.proconid_reversemap[pr_asn].append(asn)

        # traverse and prune tree
        as_obj = self.engine.as_dict[asn]
        cone_list = self.provider_cones[asn] 
        cone = ProviderConeNode(as_obj.asn)

        # add to ovh tracking dict and list
        self.maint_ovh_tracking[asn] = cone
        self.maint_ovh_tracking_list.append(asn)

        self.build_tree(cone, as_obj)
        self.prune_tree(cone)
        # clear pruning cache for next adopter
        #self.check_node_for_not_pruning.cache_clear()
        self.checked_nodes.clear()
        self.already_validated_providers.clear()
        self.prune_tree.cache_clear()
        self.get_non_pruned_ovh(cone, self.initial_overheads[asn])
        for n in self.modified_nodes:
            # reset nodes after pruning (graph is cached)
            n.do_not_prune = False
        self.modified_nodes.clear()
        logging.debug('OVH' + str(self.initial_overheads[asn]))

    def build_tree(self, cone, as_obj):
        """Build provider tree to be pruned to compute initial adopting and
           maintenance overhead.
        """
        logging.debug(f'called build tree on {cone.asn}')
        for pr_obj in as_obj.providers:
            cone.providers.add(self.build_new_node(pr_obj))

    @functools.cache
    def build_new_node(self, as_obj):
        new_node = ProviderConeNode(as_obj.asn)
        for pr_obj in as_obj.providers:
            new_node.providers.add(self.build_new_node(pr_obj))
        return new_node


    @functools.cache
    def prune_tree(self, node):
        """Prune a tree for computing initial adopting overhead."""
        self.already_validated_providers.clear()
        node.do_not_prune = self.check_node_for_not_pruning(node)
        self.modified_nodes.append(node)
        return node.do_not_prune

    def check_node_for_not_pruning(self, node):
        """Recursively check if the current node and its providers should be
           left un-pruned.
        """ 
        logging.debug(f'checking {node.asn}')
        logging.debug(f'already validated providers {self.already_validated_providers}')
        if node in self.checked_nodes:
            return node.do_not_prune
        self.checked_nodes.add(node)
        do_not_prune = False
        for pr in node.providers:
            if pr.asn in self.adopters and pr.asn not in self.already_validated_providers:
                logging.debug(f'Not pruning {node.asn} due to adopting provider')
                self.already_validated_providers.add(pr.asn)
                do_not_prune = True
        for pr in node.providers:
            if pr.asn not in self.adopters:
                pr.do_not_prune = self.check_node_for_not_pruning(pr)
                self.modified_nodes.append(pr)
        for pr in node.providers:
            if pr.do_not_prune:
                logging.debug(f'Not pruning {node.asn} due to non-pruned provider')
                do_not_prune = True
        if do_not_prune == False:
            logging.debug(f'Pruning {node.asn}')
            pass
        else:
            self.modified_nodes.append(node)
        return do_not_prune
            
    
    def get_non_pruned_ovh(self, node, overhead_set):
        """Recursively count overhead based on an already pruned graph"""
        logging.debug(f'getting ovh for as {node.asn} with providers {[x.asn for x in node.providers]}')
        logging.debug(f'adopting providers are: {[x.asn for x in node.providers if x.asn in self.adopters]}')
        for pr in node.providers:
            self.get_non_pruned_ovh_aux(pr, overhead_set)

    def get_non_pruned_ovh_aux(self, node, overhead_set):
        if node.do_not_prune:
            overhead_set.add(node.asn)
        for pr in node.providers:
            self.get_non_pruned_ovh_aux(pr, overhead_set)

    def update_maintenance_overhead(self, asn):
        """Update maintenance overhead for a given ASN that is now adopting"""
        a.adopters.add(asn)
        if asn in self.proconid_reversemap.keys():
            for tracked_asn in self.proconid_reversemap[asn]:
                cone = self.maint_ovh_tracking[tracked_asn]
                self.prune_tree(cone)
                # clear pruning cache for next adopter
                #self.check_node_for_not_pruning.cache_clear()
                self.checked_nodes.clear()
                self.already_validated_providers.clear()
                self.prune_tree.cache_clear()
                tmp_ovh = set()
                self.get_non_pruned_ovh(cone, tmp_ovh)
                self.maintenance_overheads[tracked_asn] = self.maintenance_overheads[tracked_asn].union(tmp_ovh)
                for n in self.modified_nodes:
                    # reset nodes after pruning (graph is cached)
                    n.do_not_prune = False
                self.modified_nodes.clear()
                logging.debug(f'Addl OVH {self.maintenance_overheads[tracked_asn] - self.initial_overheads[tracked_asn]}')
        

def test_provider_cones():
    """Test functionality to generate provider cones"""
    a = ProviderConeComputation()
    a.engine.ases[0].providers = (a.engine.ases[1], a.engine.ases[2])
    a.engine.ases[1].providers = tuple()
    a.engine.ases[2].providers = tuple()
    a.get_cone(a.engine.ases[0])
    if len(a.provider_cones[a.engine.ases[0].asn]) != 2:
        print("Error 1")
        exit()
    a = ProviderConeComputation()
    a.engine.ases[0].providers = (a.engine.ases[1], a.engine.ases[2])
    a.engine.ases[1].providers = tuple()
    a.engine.ases[2].providers = (a.engine.ases[3],)
    a.engine.ases[3].providers = tuple()
    a.get_cone(a.engine.ases[0])
    if len(a.provider_cones[a.engine.ases[0].asn]) != 3:
        print("Error 2")
        exit()

def test_overheads1():
    a = ProviderConeComputation()
    for i in range(1, 8):
        # print ASNs for ease of debugging
        print(i, a.engine.ases[i].asn)
    a.engine.ases[1].providers = (a.engine.ases[2], a.engine.ases[3])
    a.engine.ases[2].providers = (a.engine.ases[4], a.engine.ases[5])
    a.engine.ases[3].providers = tuple() #(a.engine.ases[5],)
    a.engine.ases[4].providers = (a.engine.ases[6],)
    a.engine.ases[5].providers = tuple()
    a.engine.ases[6].providers = tuple()
    a.engine.ases[7].providers = tuple()
    a.get_all_cones()
    a.adopters.add(a.engine.ases[6].asn)
    a.adopters.add(a.engine.ases[7].asn)
    a.pruning_overhead_calc(a.engine.ases[1].asn)

def test_overheads2():
    a = ProviderConeComputation()
    for i in range(1, 16):
        # print ASNs for ease of debugging
        print(i, a.engine.ases[i].asn)
    a.engine.ases[1].providers = tuple()
    a.engine.ases[2].providers = (a.engine.ases[1],)
    a.engine.ases[3].providers = (a.engine.ases[2],)
    a.adopters.add(a.engine.ases[3].asn)
    a.engine.ases[3].providers = tuple() #(a.engine.ases[5],)
    a.engine.ases[4].providers = (a.engine.ases[3],)
    a.engine.ases[5].providers = tuple()
    a.adopters.add(a.engine.ases[5].asn)
    a.engine.ases[6].providers = (a.engine.ases[5],)
    a.engine.ases[7].providers = (a.engine.ases[6], a.engine.ases[8])
    a.engine.ases[8].providers = tuple()
    a.adopters.add(a.engine.ases[8].asn)
    a.engine.ases[9].providers = tuple()
    a.adopters.add(a.engine.ases[9].asn)
    a.engine.ases[10].providers = (a.engine.ases[9], a.engine.ases[14])
    a.engine.ases[11].providers = tuple()
    a.engine.ases[12].providers = (a.engine.ases[11],)
    a.engine.ases[13].providers = (a.engine.ases[12],)
    a.engine.ases[14].providers = (a.engine.ases[13],)
    a.engine.ases[15].providers = (a.engine.ases[4], a.engine.ases[7], a.engine.ases[10])
    a.get_all_cones()
    a.pruning_overhead_calc(a.engine.ases[15].asn)

def test_overheads3():
    a = ProviderConeComputation()
    for i in range(1, 16):
        # print ASNs for ease of debugging
        print(i, a.engine.ases[i].asn)
    a.engine.ases[1].providers = tuple()
    a.adopters.add(a.engine.ases[1].asn)
    a.engine.ases[2].providers = (a.engine.ases[1],)
    a.engine.ases[3].providers = (a.engine.ases[2],)
    a.adopters.add(a.engine.ases[3].asn)
    a.engine.ases[3].providers = tuple() #(a.engine.ases[5],)
    a.engine.ases[4].providers = (a.engine.ases[3],)
    a.engine.ases[5].providers = tuple()
    a.adopters.add(a.engine.ases[5].asn)
    a.engine.ases[6].providers = (a.engine.ases[5],a.engine.ases[2])
    a.engine.ases[7].providers = (a.engine.ases[6], a.engine.ases[8])
    a.engine.ases[8].providers = tuple()
    a.adopters.add(a.engine.ases[8].asn)
    a.engine.ases[9].providers = tuple()
    a.adopters.add(a.engine.ases[9].asn)
    a.engine.ases[10].providers = (a.engine.ases[9], a.engine.ases[14])
    a.engine.ases[11].providers = tuple()
    a.adopters.add(a.engine.ases[11].asn)
    a.engine.ases[12].providers = (a.engine.ases[11],)
    a.engine.ases[13].providers = (a.engine.ases[12],)
    a.engine.ases[14].providers = (a.engine.ases[13],)
    a.engine.ases[15].providers = (a.engine.ases[4], a.engine.ases[7], a.engine.ases[10], a.engine.ases[3])
    a.get_all_cones()
    a.pruning_overhead_calc(a.engine.ases[15].asn)

def test_overheads4():
    a = ProviderConeComputation()
    for i in range(1, 16):
        # print ASNs for ease of debugging
        print(i, a.engine.ases[i].asn)
    a.engine.ases[1].providers = tuple()
    a.adopters.add(a.engine.ases[1].asn)
    a.engine.ases[2].providers = (a.engine.ases[1],)
    a.engine.ases[3].providers = (a.engine.ases[2],)
    a.adopters.add(a.engine.ases[3].asn)
    a.engine.ases[3].providers = tuple() #(a.engine.ases[5],)
    a.engine.ases[4].providers = (a.engine.ases[3],)
    a.engine.ases[5].providers = tuple()
    a.adopters.add(a.engine.ases[5].asn)
    a.engine.ases[6].providers = (a.engine.ases[5],a.engine.ases[2])
    a.engine.ases[7].providers = (a.engine.ases[6], a.engine.ases[8])
    a.engine.ases[8].providers = tuple()
    a.adopters.add(a.engine.ases[8].asn)
    a.engine.ases[9].providers = tuple()
    a.adopters.add(a.engine.ases[9].asn)
    a.engine.ases[10].providers = (a.engine.ases[9], a.engine.ases[14])
    a.engine.ases[11].providers = tuple()
    a.adopters.add(a.engine.ases[11].asn)
    a.engine.ases[12].providers = (a.engine.ases[11],)
    a.engine.ases[13].providers = (a.engine.ases[12],)
    a.engine.ases[14].providers = (a.engine.ases[13],)
    a.engine.ases[15].providers = (a.engine.ases[4], a.engine.ases[7], a.engine.ases[10], a.engine.ases[3])
    a.get_all_cones()
    a.pruning_overhead_calc(a.engine.ases[15].asn)
    a.pruning_overhead_calc(a.engine.ases[15].asn)





if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    #test_overheads4()
    a = ProviderConeComputation()
    a.get_all_cones()
    all_asns = []
    for asn, cone in a.provider_cones.items():
        all_asns.append(asn)
    random.seed(os.environ['SLURM_ARRAY_TASK_ID'])
    random.shuffle(all_asns)
    # skip to 1%
    i = 0
    adopters_per_percent = 50
    percents = [1.0, 10.0, 20.0, 30.0, 50.0, 80.0, 99.0]
    #percents = [1.0, 10.0, 20]
    for percent in percents:
        avg = 0.0
        while i < (percent*(len(all_asns) / 100)):
            a.update_maintenance_overhead(all_asns[i])
            #a.adopters.add(all_asns[i])
            i += 1
        for _ in range(adopters_per_percent):
            i += 1
            a.pruning_overhead_calc(all_asns[i])
            avg += len(a.initial_overheads[all_asns[i]])
        print('AVG', avg / float(adopters_per_percent))
    j = 0
    for percent in percents:
        maintenance_avg = 0.0
        old_j = j
        while j < old_j + adopters_per_percent:
            asn = a.maint_ovh_tracking_list[j]
            maintenance_avg += len(a.maintenance_overheads[asn] - a.initial_overheads[asn])
            j += 1
        print('M AVG', maintenance_avg / float(adopters_per_percent))

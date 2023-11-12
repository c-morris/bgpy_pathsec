import math
import random
from typing import Optional, Union

from frozendict import frozendict

from bgpy.caida_collector import AS
from bgpy.enums import ASGroups
from bgpy.simulation_engine import SimulationEngine
from bgpy.simulation_framework import Scenario

from .valid_signature import ValidSignature
from bgpy_pathsec.policies import TransitiveDroppingAlwaysAS


class TransitiveDroppingNoAdoptCustomers(ValidSignature):
    """TODO"""

    def _get_non_default_asn_cls_dict(
        self,
        override_non_default_asn_cls_dict: Union[
            Optional[frozendict[int, type[AS]]],
            # Must include due to mypy weirdness
            # about empty frozendicts
            frozendict[str, None],
        ],
        engine: Optional[SimulationEngine],
        prev_scenario: Optional["Scenario"],
    ) -> dict[int, type[AS]]:

        # For testing purposes only
        if override_non_default_asn_cls_dict:
            return override_non_default_asn_cls_dict


        # DO NOT call super's _get_non_default_asn_cls_dict, instead just
        # get the randomized dictionary. since that relies on the prev_scenario's
        # adopting AS classes, which change based on the dropping ASes
        # so every time we need a completely new random set
        # NOTE: This also means this can NOT!!! be run in the same sim
        # as other scenario_configs since this will make all scenario_configs
        # independent
        non_default_asn_cls_dict = self._get_randomized_non_default_asn_cls_dict(
            engine
        )

        ##################################
        # add dropping ASes to this dict #
        ##################################

        percent_drop_trans = self.scenario_config.transitive_dropping_percent

        asns = set([x.asn for x in engine.ases])
        possible_droppers = asns.difference(self._preset_asns)
        possible_droppers = possible_droppers.difference(
            set(list(non_default_asn_cls_dict))
        )

        k = math.ceil(len(possible_droppers) * (percent_drop_trans / 100))

        # https://stackoverflow.com/a/15837796/8903959
        possible_droppers_tup = tuple(possible_droppers)
        try:
            droppers = set(random.sample(possible_droppers_tup, k))
            for asn in droppers:
                non_default_asn_cls_dict[asn] = TransitiveDroppingAlwaysAS
        except ValueError:
            raise ValueError(
                f"{k} can't be sampled from {len(possible_droppers)}"
            )

        ################################################################
        # Remove adopters that only have transitive dropping providers #
        ################################################################

        visited_asns = set()
        # For each dropper, check the customers
        for asn in droppers:
            as_obj = engine.as_dict[asn]
            # For each customer, get the provider_asns
            for customer in as_obj.customers:

                # If customer is adopting and all providers are dropping
                # the AS no longer adopts
                if ((customer.asn not in visited_asns)
                    and isinstance(customer, self.scenario_config.AdoptASCls)
                    and all(isinstance(x, TransitiveDroppingAlwaysAS) for x
                            in customer.providers)):
                    non_default_asn_cls_dict.pop(customer.asn)
                visited_asns.add(customer.asn)

        return non_default_asn_cls_dict

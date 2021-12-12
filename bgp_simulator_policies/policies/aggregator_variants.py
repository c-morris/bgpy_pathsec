from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS

class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsec Aggressive"

class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "BGPsec Transitive Aggressive"

class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "PaBGPsec Aggressive"

class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGPsec Transitive Timid"

class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeak"""
    name = "PaBGPsec Timid"

class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakNoHash"""
    name = "PaBGPsec No Hash Timid"

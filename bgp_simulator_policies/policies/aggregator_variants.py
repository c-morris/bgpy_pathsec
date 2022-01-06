from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS


class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsec 1-hop"


class BGPsecTimidAS(BGPsecAS):
    """For use with IntentionalLeak"""
    name = "BGPsec Timid"


class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "BGPsec Transitive 1-hop"


class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "PaBGPsec 1-hop"


class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGPsec Transitive Timid"


class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeak"""
    name = "PaBGPsec Timid"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakNoHash"""
    name = "PaBGPsec No Hash Timid"


class BGPsecTransitiveDownOnlyNoHashAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "PaBGPsec No Hash 1-hop"

from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS


class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsec, Aggressive"


class BGPsecTimidAS(BGPsecAS):
    """For use with IntentionalLeak"""
    name = "BGPsec, Timid"


class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "PaBGPsec, No Leak Prevention Aggressive"


class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "PaBGPsec, Aggressive"


class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "PaBGPsec, No Leak Prevention or Path Shortening Timid"


class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeak"""
    name = "PaBGPsec, Timid"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakNoHash"""
    name = "PaBGPsec, No Path Shortening Defense Timid"


class BGPsecTransitiveDownOnlyNoHashAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "PaBGPsec, No Path Shortening Defense Aggressive"


class BGPsecTransitiveDownOnlyTimidLeakAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakTimid"""
    name = "PaBGPsec, Timid Leak"

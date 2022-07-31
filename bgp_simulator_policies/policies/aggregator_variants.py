from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS


class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsec Aggressive"


class BGPsecTimidAS(BGPsecAS):
    """For use with IntentionalLeak"""
    name = "BGPsec Timid"


class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "BGP-Isec No Leak Prevention Aggressive"


class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "BGP-Isec Aggressive"


class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGP-Isec No Leak Prevention or Path Shortening Timid"


class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeak"""
    name = "BGP-Isec Timid"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakNoHash"""
    name = "BGP-Isec No Path Shortening Defense Timid"


class BGPsecTransitiveDownOnlyNoHashAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "BGP-Isec No Path Shortening Defense Aggressive"

class BGPsecTransitiveDownOnlyTimidLeakAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakTimid"""
    name = "BGP-Isec Timid Leak"



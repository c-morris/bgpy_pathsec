from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS


class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsecAggressiveAS"


class BGPsecTimidAS(BGPsecAS):
    """For use with IntentionalLeak"""
    name = "BGPsecTimidAS"


class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "BGPsecTransitiveAggressiveAS"


class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "BGPsecTransitiveDownOnlyAggressiveAS"


class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with IntentionalLeak"""
    name = "BGPsecTransitiveTimidAS"


class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeak"""
    name = "BGPsecTransitiveDownOnlyTimidAS"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakNoHash"""
    name = "BGPsecTransitiveDownOnlyNoHashTimidAS"


class BGPsecTransitiveDownOnlyNoHashAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "BGPsecTransitiveDownOnlyNoHashAggressiveAS"


class BGPsecTransitiveDownOnlyTimidLeakAS(BGPsecTransitiveDownOnlyAS):
    """For use with IntentionalLeakTimid"""
    name = "BGPsecTransitiveDownOnlyTimidLeakAS"

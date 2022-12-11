from bgp_simulator_pkg import BGPAS
from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS
from .path_end import PathEndAS


class BGPsecAggressiveAS(BGPsecAS):
    """For use with OriginHijack"""
    name = "BGPsecAggressiveAS"


class BGPsecTimidAS(BGPsecAS):
    """For use with ShortestPathExportAll"""
    name = "BGPsecTimidAS"


class BGPsecTransitiveAggressiveAS(BGPsecTransitiveAS):
    """For use with OriginHijack"""
    name = "BGPsecTransitiveAggressiveAS"


class BGPsecTransitiveTimidAS(BGPsecTransitiveAS):
    """For use with ShortestPathExportAll"""
    name = "BGPsecTransitiveTimidAS"


class BGPsecTransitiveDownOnlyAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with OriginHijack"""
    name = "BGPsecTransitiveDownOnlyAggressiveAS"


class BGPsecTransitiveDownOnlyTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAll"""
    name = "BGPsecTransitiveDownOnlyTimidAS"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllNoHash"""
    name = "BGPsecTransitiveDownOnlyNoHashTimidAS"


class BGPsecTransitiveDownOnlyNoHashUpTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllNoHash"""
    name = "BGPsecTransitiveDownOnlyNoHashUpTimidAS"


class BGPsecTransitiveDownOnlyNoHashAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "BGPsecTransitiveDownOnlyNoHashAggressiveAS"


class BGPsecTransitiveDownOnlyNoHashUpAggressiveAS(BGPsecTransitiveDownOnlyAS):
    """For use with Origin Hijack"""
    name = "BGPsecTransitiveDownOnlyNoHashUpAggressiveAS"


class BGPsecTransitiveDownOnlyTimidLeakAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllTimid"""
    name = "BGPsecTransitiveDownOnlyTimidLeakAS"


class PathEndAggressiveAS(PathEndAS):
    """For use with Origin Hijack"""
    name = "PathEndAggressiveAS"


class PathEndTimidAS(PathEndAS):
    """For use with TwoHopAttack"""
    name = "PathEndTimidAS"


class PathEndTimidUpAS(PathEndAS):
    """For use with TwoHopAttackUp"""
    name = "PathEndTimidUpAS"


class BaselineBGPAS(BGPAS):
    """For use with Origin Hijack"""
    name = "BaselineBGPAS"

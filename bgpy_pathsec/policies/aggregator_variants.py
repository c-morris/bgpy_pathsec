from bgpy import BGPAS
from . import BGPsecAS, BGPsecTransitiveAS, BGPsecTransitiveDownOnlyAS
from . import BGPsecTransitiveDownOnlyEncrUpAS
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


class BGPsecTransitiveDownOnlyUpTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllUp"""

    name = "BGPsecTransitiveDownOnlyUpTimidAS"


class BGPsecTransitiveDownOnlyNoHashTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllNoHash"""

    name = "BGPsecTransitiveDownOnlyNoHashTimidAS"


class BGPsecTransitiveDownOnlyNoHashUpTimidAS(BGPsecTransitiveDownOnlyAS):
    """For use with ShortestPathExportAllNoHashUp"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidAS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 1% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping1AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 2% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping2AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 4% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping4AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping8AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 8% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping8AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping16AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 16% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping16AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping32AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 32% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping32AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping64AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 64% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping64AS"


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping99AS(
    BGPsecTransitiveDownOnlyAS
):
    """For use with ShortestPathExportAllNoHashUp, 99% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDropping99AS"


# TODO these class names are getting out of hand...


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS(
    BGPsecTransitiveDownOnlyAS
):  # noqa E501
    """For use with ShortestPathExportAllNoHashUp, 1% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers1AS"  # noqa E501


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS(
    BGPsecTransitiveDownOnlyAS
):  # noqa E501
    """For use with ShortestPathExportAllNoHashUp, 2% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers2AS"  # noqa E501


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS(
    BGPsecTransitiveDownOnlyAS
):  # noqa E501
    """For use with ShortestPathExportAllNoHashUp, 4% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers4AS"  # noqa E501


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers8AS(
    BGPsecTransitiveDownOnlyAS
):  # noqa E501
    """For use with ShortestPathExportAllNoHashUp, 8% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers8AS"  # noqa E501


class BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers16AS(
    BGPsecTransitiveDownOnlyAS
):  # noqa E501
    """For use with ShortestPathExportAllNoHashUp, 16% transitive dropping"""

    name = "BGPsecTransitiveDownOnlyNoHashUpTimidTransitiveDroppingNoAdoptCustomers16AS"  # noqa E501


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


class OverheadBGPsecAS(BGPsecAS):
    """For use with ValidPrefix"""

    name = "OverheadBGPsecAS"


class OverheadBGPsecTransitiveDownOnlyAS(BGPsecTransitiveDownOnlyAS):
    """For use with ValidPrefix"""

    name = "OverheadBGPsecTransitiveDownOnlyAS"


class BGPsecTransitiveDownOnlyGlobalEavesdropperAS(BGPsecTransitiveDownOnlyAS):
    """For use with GlobalEavesdropper"""

    name = "BGPsecTransitiveDownOnlyGlobalEavesdropperAS"


class BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS(
    BGPsecTransitiveDownOnlyEncrUpAS
):
    """For use with GlobalEavesdropperUp"""

    name = "BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperAS"


class BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperUnknownAdoptersAS(
    BGPsecTransitiveDownOnlyEncrUpAS
):
    """For use with GlobalEavesdropperUpUnknownAdopters"""

    name = "BGPsecTransitiveDownOnlyEncrUpGlobalEavesdropperUnknownAdoptersAS"


class BaselineBGPAS(BGPAS):
    """For use with Origin Hijack"""

    name = "BaselineBGPAS"
    count = 0
    bpo_count = 0

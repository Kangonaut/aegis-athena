from typing import Self

from spacecraft.parts.ars import ArsController
from spacecraft.parts.base import BaseController
from spacecraft.parts.hts import HtsController
from spacecraft.parts.oscpcs import OscpcsController
from spacecraft.parts.wcs import WcsController


class EcsController(BaseController):
    def __init__(self, name: str,
                 wcs_controller: WcsController,
                 oscpcs_controller: OscpcsController,
                 ars_controller: ArsController,
                 hts_controller: HtsController) -> None:
        super().__init__(name)
        self.wcs_controller = wcs_controller
        self.oscpcs_controller = oscpcs_controller
        self.ars_controller = ars_controller
        self.hts_controller = hts_controller

    @property
    def dependencies(self) -> set[Self]:
        return {self.wcs_controller, self.oscpcs_controller, self.ars_controller, self.hts_controller}

    def display_details(self) -> str:
        return (
                super().display_details() +
                f"WCS: {self.wcs_controller.part_id}\n"
                f"OSCPCS: {self.oscpcs_controller.part_id}\n"
                f"ARS: {self.ars_controller.part_id}\n"
                f"HTS: {self.hts_controller.part_id}\n"
        )

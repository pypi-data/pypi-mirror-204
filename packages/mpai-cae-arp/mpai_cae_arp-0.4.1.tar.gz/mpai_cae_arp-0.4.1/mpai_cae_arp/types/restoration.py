# pylint: disable=too-few-public-methods
import uuid
from typing import TypeVar
from pydantic import BaseModel, Field
from mpai_cae_arp.audio.standards import SpeedStandard, EqualizationStandard
from mpai_cae_arp.files import File, FileType


class Restoration(BaseModel):
    """
    .. versionadded:: 0.4.0
    """

    class Config:
        allow_population_by_field_name = True

    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="RestorationID")
    preservation_audio_file_start: str = Field(alias="PreservationAudioFileStart")
    preservation_audio_file_end: str = Field(alias="PreservationAudioFileEnd")
    restored_audio_file_URI: str = Field(alias="RestoredAudioFileURI")
    reading_backwards: bool = Field(alias="ReadingBackwards")
    applied_speed_standard: SpeedStandard = Field(alias="AppliedSpeedStandard")
    applied_sample_frequency: int = Field(alias="AppliedSampleFrequency")
    applied_equalization_standard: EqualizationStandard = Field(
        alias="AppliedEqualisationStandard")


Self = TypeVar("Self", bound="EditingList")


class EditingList(BaseModel):
    """
    .. versionadded:: 0.4.0
    """

    class Config:
        allow_population_by_field_name = True

    original_speed_standard: SpeedStandard = Field(alias="OriginalSpeedStandard")
    original_equalization_standard: EqualizationStandard = Field(
        alias="OriginalEqualisationStandard")
    original_sample_frequency: int = Field(alias="OriginalSampleFrequency")
    restorations: list[Restoration] = Field(alias="Restorations")

    def add(self, restoration: Restoration) -> Self:
        self.restorations.append(restoration)
        return self

    def remove(self, restoration: Restoration) -> Self:
        self.restorations.remove(restoration)
        return self

    def remove_by_id(self, restoration_id: uuid.UUID) -> Self:
        filtered = list(filter(lambda r: r.id != restoration_id, self.restorations))

        if len(filtered) == len(self.restorations):
            raise ValueError(f"Restoration with ID {restoration_id} not found.")

        self.restorations = filtered
        return self

    def save_as_json_file(self, path: str) -> None:
        File(path=path,
             filetype=FileType.JSON).write_content(self.json(by_alias=True, indent=4))

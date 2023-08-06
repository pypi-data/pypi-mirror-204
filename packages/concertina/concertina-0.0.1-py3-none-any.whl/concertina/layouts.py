from collections.abc import Iterator, Mapping
from types import MappingProxyType
from typing import NewType

import pydantic

from concertina.base_models import BaseModel
from concertina.pitches import parse_note, Pitch, PitchClass, InvalidInputError


ButtonId = NewType("ButtonId", str)


class Button(BaseModel):
    push: Pitch
    pull: Pitch

    @pydantic.validator("push", "pull", pre=True)
    def coerce_to_pitch(cls, v) -> Pitch:
        if isinstance(v, str):
            v = Pitch(v)
        if isinstance(v, Mapping):
            v = Pitch(**v)
        return v


class FoundButtons(BaseModel):
    push: tuple[ButtonId, ...]
    pull: tuple[ButtonId, ...]


class ButtonLayout(BaseModel):
    name: str
    buttons: Mapping[ButtonId, Button]

    def find_pitch(self, pitch: str | Pitch) -> FoundButtons:
        pitch = Pitch(pitch)
        found_push = []
        found_pull = []
        for button_id, button in self.buttons.items():
            if button.push == pitch:
                found_push.append(button_id)
            if button.pull == pitch:
                found_pull.append(button_id)
        return FoundButtons(
            push=found_push,
            pull=found_pull,
        )

    def find_pitch_class(self, pitch_class: str | PitchClass) -> FoundButtons:
        pitch_class = PitchClass(pitch_class)

        found_push = []
        found_pull = []
        for button_id, button in self.buttons.items():
            if button.push.pitch_class == pitch_class:
                found_push.append(button_id)
            if button.pull.pitch_class == pitch_class:
                found_pull.append(button_id)
        return FoundButtons(
            push=found_push,
            pull=found_pull,
        )

    def find(self, target: str | PitchClass | Pitch) -> FoundButtons:
        parsed = parse_note(target)

        match parsed:
            case Pitch():
                return self.find_pitch(parsed)
            case PitchClass():
                return self.find_pitch_class(parsed)

    def _iter_pitches(self) -> Iterator[Pitch]:
        return (
            getattr(button, bellows_attr)
            for button in self.buttons.values()
            for bellows_attr in ("push", "pull")
        )

    @property
    def lowest_pitch(self) -> Pitch:
        return min(self._iter_pitches())

    @property
    def highest_pitch(self) -> Pitch:
        return max(self._iter_pitches())

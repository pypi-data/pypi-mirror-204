"""Modeling and parsing pitches.

Resources:
- https://viva.pressbooks.pub/openmusictheory/chapter/aspn/
"""

from dataclasses import dataclass
from typing import Literal, NewType, Type, TypeVar

import pydantic

from concertina.base_models import BaseModel


class InvalidInputError(Exception):
    ...


class ParseError(InvalidInputError):
    ...


HALFSTEPS_IN_OCTAVE = 12


PITCH_CLASS_MAPPING = {
    0: "C",
    1: "C#",
    2: "D",
    3: "D#",
    4: "E",
    5: "F",
    6: "F#",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}


class _ParsedScientificNote(BaseModel):
    letter: str
    accidental: Literal["#", "b", ""]
    octave: int | None


def _parse_scientific_note(note: str) -> _ParsedScientificNote:
    """Quick and dirty parse of scientific notation."""

    def _take_note_letter(string: str) -> tuple[str, str]:
        _valid_note_letters = "CDEFGAB"
        letter = string[0]
        remaining = string[1:]
        if letter not in _valid_note_letters:
            # TODO: better error
            raise ParseError(f"{letter!r} is not a valid note letter.")
        return letter, remaining

    def _take_accidental(string: str) -> tuple[str, str]:
        if string == "":
            return "", ""
        accidental = ""
        remaining = string
        if string[0] in {"#", "b"}:
            accidental = string[0]
            remaining = string[1:]
        return accidental, remaining

    letter, remaining = _take_note_letter(note)
    accidental, remaining = _take_accidental(remaining)

    octave = int(remaining) if remaining else None
    return _ParsedScientificNote(letter=letter, accidental=accidental, octave=octave)


def _apply_accidental(semitones: int, accidental: str) -> int:
    # EARLY RETURN
    if accidental == "":
        return semitones

    if accidental == "#":
        semitones += 1
    elif accidental == "b":
        semitones -= 1
    else:
        raise NotImplementedError("Can only handle accidental as '#' or 'b' right now.")
    return semitones


_PitchClassT = TypeVar("_PitchClassT", bound="PitchClass")


class PitchClass(BaseModel, frozen=True):
    note: str
    midi: int

    def __init__(
        self: _PitchClassT,
        pitch_class: (str | _PitchClassT | None) = None,
        **data,
    ) -> None:
        if pitch_class and data:
            raise InvalidInputError("Cannot mix positional and keyword arguments.")

        if pitch_class is not None:
            if isinstance(pitch_class, str):
                pitch_class = type(self).from_scientific(pitch_class)
            elif not isinstance(pitch_class, type(self)):
                bad_class_name = type(pitch_class).__name__
                self_class_name = type(self).__name__
                raise InvalidInputError(
                    f"Cannot initialize {self_class_name} with a {bad_class_name}"
                )
            data = vars(pitch_class)

        super().__init__(**data)

    @classmethod
    def from_midi(cls: Type[_PitchClassT], note: int) -> _PitchClassT:
        assert note >= 0, "TODO: How should we handle negative notes?"
        note = note % HALFSTEPS_IN_OCTAVE
        return cls(
            note=PITCH_CLASS_MAPPING[note],
            midi=note,
        )

    @classmethod
    def from_scientific(cls: Type[_PitchClassT], note: str) -> _PitchClassT:
        inverse_mapping = dict(
            zip(PITCH_CLASS_MAPPING.values(), PITCH_CLASS_MAPPING.keys())
        )

        if note not in inverse_mapping:
            # Try to parse the note
            parsed = _parse_scientific_note(note)
            midi = inverse_mapping[parsed.letter]
            midi = _apply_accidental(midi, parsed.accidental)
            # Add an octave, in case we flattened to a negative number
            midi += HALFSTEPS_IN_OCTAVE
            return cls.from_midi(midi)

        return cls(
            note=note,
            midi=inverse_mapping[note],
        )

    def __str__(self):
        return self.note


_PitchT = TypeVar("_PitchT", bound="Pitch")


class Pitch(BaseModel, frozen=True):
    pitch_class: PitchClass
    octave: int
    midi: int
    scientific: str

    def __init__(self: _PitchT, pitch: (str | _PitchT | None) = None, **data) -> None:
        if pitch and data:
            raise InvalidInputError("Cannot mix positional and keyword arguments.")
        if pitch is not None:
            if isinstance(pitch, str):
                pitch = type(self).from_scientific(pitch)
            elif not isinstance(pitch, type(self)):
                bad_class_name = type(pitch).__name__
                self_class_name = type(self).__name__
                raise InvalidInputError(
                    f"Cannot initialize {self_class_name} with a {bad_class_name}"
                )
            data = vars(pitch)
        super().__init__(**data)

    @classmethod
    def from_midi(cls: Type[_PitchT], midi: int) -> _PitchT:
        octave, midi_pitch_class = divmod(midi, HALFSTEPS_IN_OCTAVE)
        # C4 is 60, so we need to subtract 1 from the octave.
        octave -= 1
        pitch_class = PitchClass.from_midi(midi_pitch_class)
        return cls(
            pitch_class=pitch_class,
            octave=octave,
            midi=midi,
            scientific=f"{pitch_class}{octave}",
        )

    @classmethod
    def from_scientific(cls: Type[_PitchT], scientific: str) -> _PitchT:
        parsed = _parse_scientific_note(scientific)
        # Resolve the letter and the octave together before applying the
        # accidental.
        # https://infogalactic.com/info/Scientific_pitch_notation#C-flat_and_B-sharp_issues
        pitch_class = PitchClass.from_scientific(parsed.letter)
        if not isinstance(parsed.octave, int):
            raise ParseError("Pitches must end with an octave number.")
        # C4 is 60, so we need to add 1 to the octave.
        midi = (parsed.octave + 1) * HALFSTEPS_IN_OCTAVE + pitch_class.midi
        # Now that we have the correct octave, we can apply the accidental.
        midi = _apply_accidental(midi, parsed.accidental)
        # Use `from_midi` as the constructor to ensure consistent rendering of
        # the note.
        return cls.from_midi(midi)

    @pydantic.validator("pitch_class", pre=True)
    def coerce_pitch_class(cls, v: str | PitchClass) -> PitchClass:
        return PitchClass(v)

    def __str__(self):
        return self.scientific

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.scientific!r})"

    #
    # Comparison operators
    #

    def __lt__(self: _PitchT, other: _PitchT) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.midi.__lt__(other.midi)

    def __le__(self: _PitchT, other: _PitchT) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.midi.__le__(other.midi)

    def __gt__(self: _PitchT, other: _PitchT) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.midi.__gt__(other.midi)

    def __ge__(self: _PitchT, other: _PitchT) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.midi.__ge__(other.midi)


def parse_note(note: str | Pitch | PitchClass) -> Pitch | PitchClass:
    match note:
        case Pitch() | PitchClass():
            # It's already parsed! Return it as is.
            return note

    parsed_note = _parse_scientific_note(note)
    match parsed_note:
        case _ParsedScientificNote(octave=int()):
            # If it has an integer octave, it's a Pitch!
            return Pitch(note)
        case _:
            return PitchClass(note)

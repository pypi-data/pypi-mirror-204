from typing import Sequence

import musthe  # type: ignore

from concertina.pitches import PitchClass


def parse_chord_into_pitch_classes(chord_string: str) -> Sequence[PitchClass]:
    chord = musthe.Chord(chord_string)
    return tuple(PitchClass(str(note)) for note in chord.notes)

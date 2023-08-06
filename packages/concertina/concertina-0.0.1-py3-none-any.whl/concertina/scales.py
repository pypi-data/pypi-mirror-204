from typing import Sequence

import musthe  # type: ignore

from concertina.pitches import Pitch, PitchClass


SUPPORTED_SCALES = tuple(musthe.Scale.scales)

# We'll support the greek scales, but we don't want to display it by default in
# the helptext.
DISPLAY_SCALES = tuple(
    scale for scale in SUPPORTED_SCALES if scale not in musthe.Scale.greek_modes_set
)


def get_scale_pitch_class_sequence(
    root: str | PitchClass,
    scale_name: str,
) -> Sequence[PitchClass]:
    # Validate the root by parsing it as a PitchClass
    root = PitchClass(root)
    scale = musthe.Scale(str(root), scale_name)
    return tuple(PitchClass(str(note)) for note in scale.notes)


def get_scale_as_pitch_range(
    root: str | PitchClass,
    scale_name: str,
    *,
    low: str | Pitch,
    high: str | Pitch,
) -> Sequence[Pitch]:
    root = PitchClass(root)
    low = Pitch(low)
    high = Pitch(high)
    scale = musthe.Scale(str(root), scale_name)

    def _find_start():
        found_start = low
        # This is hacky and goofy, but in theory, it'll never do more than 12
        # iterations!
        while found_start.pitch_class != root:
            assert found_start.midi >= 0, "TODO: properly handle this case"
            found_start = Pitch.from_midi(found_start.midi - 1)
        return found_start

    def _find_end():
        # Assume the last one is the end of the scale
        end_pitch_class = PitchClass(str(scale.notes[-1]))
        found_end = high
        while found_end.pitch_class != end_pitch_class:
            # NOTE: 127 is the top of the MIDI tuning range
            assert found_end.midi <= 127, "TODO: properly handle this case"
            found_end = Pitch.from_midi(found_end.midi + 1)
        return found_end

    start = _find_start()
    end = _find_end()
    # Oh god, this is terrible, but I'm sleepy and I don't want to think about
    # this right now. The size of the data is well-bounded, so even if I'm
    # being horribly inefficient, it's not the end of the world here. (I'd
    # promise to fix it later, but that would effectively guarantee that this
    # comment is still here decades later.)
    pitch_classes = frozenset(get_scale_pitch_class_sequence(root, scale_name))
    return tuple(
        pitch
        for midi in range(start.midi, end.midi + 1)
        if (pitch := Pitch.from_midi(midi)).pitch_class in pitch_classes
    )

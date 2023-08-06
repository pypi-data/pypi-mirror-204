import argparse

from rich.tree import Tree
from rich import print
from rich import console

from concertina import chords
from concertina import pitches
from concertina import scales
from concertina.layouts import ButtonLayout, Button, FoundButtons


DEFAULT_LAYOUT = ButtonLayout(
    name="Wheatstone 30-button C/G",
    buttons={
        "left 1a": Button(push="E3", pull="F3"),
        "left 2a": Button(push="A3", pull="A#3"),
        "left 3a": Button(push="C#4", pull="D#4"),
        "left 4a": Button(push="A4", pull="G4"),
        "left 5a": Button(push="G#4", pull="A#4"),
        "left 1": Button(push="C3", pull="G3"),
        "left 2": Button(push="G3", pull="B3"),
        "left 3": Button(push="C4", pull="D4"),
        "left 4": Button(push="E4", pull="F4"),
        "left 5": Button(push="G4", pull="A4"),
        "left 6": Button(push="B3", pull="A3"),
        "left 7": Button(push="D4", pull="F#4"),
        "left 8": Button(push="G4", pull="A4"),
        "left 9": Button(push="B4", pull="C5"),
        "left 10": Button(push="D5", pull="E5"),
        "right 1a": Button(push="C#5", pull="D#5"),
        "right 2a": Button(push="A5", pull="G5"),
        "right 3a": Button(push="G#5", pull="A#5"),
        "right 4a": Button(push="C#6", pull="D#6"),
        "right 5a": Button(push="A6", pull="F6"),
        "right 1": Button(push="C5", pull="B4"),
        "right 2": Button(push="E5", pull="D5"),
        "right 3": Button(push="G5", pull="F5"),
        "right 4": Button(push="C6", pull="A5"),
        "right 5": Button(push="E6", pull="B5"),
        "right 6": Button(push="G5", pull="F#5"),
        "right 7": Button(push="B5", pull="A5"),
        "right 8": Button(push="D6", pull="C6"),
        "right 9": Button(push="G6", pull="E6"),
        "right 10": Button(push="B6", pull="F#6"),
    },
)


def render_found_buttons(found: FoundButtons, note: pitches.Pitch | pitches.PitchClass):
    push = Tree("Push" if found.push else "Push (none)")
    pull = Tree("Pull" if found.pull else "Pull (none)")

    longest_key = max(found.push + found.pull, key=len)
    just_count = len(longest_key)
    for found_push in found.push:
        if isinstance(note, pitches.PitchClass):
            actual_pitch = DEFAULT_LAYOUT.buttons[found_push].push
            push.add(f"{found_push.ljust(just_count)} [{actual_pitch}]")
        else:
            push.add(found_push)
    for found_pull in found.pull:
        if isinstance(note, pitches.PitchClass):
            actual_pitch = DEFAULT_LAYOUT.buttons[found_pull].pull
            pull.add(f"{found_pull.ljust(just_count)} [{actual_pitch}]")
        else:
            pull.add(found_pull)
    print(push)
    print(pull)


def handle_chord(chord_string: str):
    chord_notes = chords.parse_chord_into_pitch_classes(chord_string)
    found_buttons_for_each_pitch_class = {
        pitch_class: DEFAULT_LAYOUT.find_pitch_class(pitch_class)
        for pitch_class in chord_notes
    }
    push_tree = Tree("Push")
    pull_tree = Tree("Pull")

    max_length = max(
        len(button_id)
        for found_buttons in found_buttons_for_each_pitch_class.values()
        for bellows_attr in ["push", "pull"]
        for button_id in getattr(found_buttons, bellows_attr)
    )

    for bellows_attr, tree in [("push", push_tree), ("pull", pull_tree)]:
        for pitch_class, found_buttons in found_buttons_for_each_pitch_class.items():
            pc_tree = tree.add(str(pitch_class))
            for button_id in getattr(found_buttons, bellows_attr):
                pitch = getattr(DEFAULT_LAYOUT.buttons[button_id], bellows_attr)
                pc_tree.add(f"{button_id.ljust(max_length)} [{pitch}]")
    print(push_tree)
    print(pull_tree)


def handle_scale(root: str, scale: str):
    root_pitch_class = pitches.PitchClass(root)
    scale_pitches = scales.get_scale_as_pitch_range(
        root, scale, low=DEFAULT_LAYOUT.lowest_pitch, high=DEFAULT_LAYOUT.highest_pitch
    )
    found_buttons_for_each_pitch = {
        pitch: DEFAULT_LAYOUT.find_pitch(pitch) for pitch in scale_pitches
    }
    for pitch, found_buttons in found_buttons_for_each_pitch.items():
        pitch_label = str(pitch)
        if pitch.pitch_class == root_pitch_class:
            pitch_label = f"[bold green]{pitch_label} (root)[/bold green]"
        tree = Tree(pitch_label)
        for bellows_attr in ["push", "pull"]:
            button_ids = getattr(found_buttons, bellows_attr)
            if button_ids:
                bellows_tree = tree.add(bellows_attr.title())
                for button_id in button_ids:
                    bellows_tree.add(button_id)
        print(tree)


def console_main(args: list[str] | None = None):
    parser = argparse.ArgumentParser(prog="concertina")

    subparsers = parser.add_subparsers(dest="subcommand")

    note_command = subparsers.add_parser("note")
    note_command.add_argument("note", type=str)

    chord_command = subparsers.add_parser("chord")
    chord_command.add_argument("chord", type=str, metavar="<chord>")

    scale_command = subparsers.add_parser("scale")
    scale_command.add_argument(
        "root",
        type=str,
        metavar="<root>",
    )
    _advertised_scales = [
        scale
        for scale in scales.SUPPORTED_SCALES
        # lol, none of that weird 'phrygian' shit in the helptext. These can
        # still be used, but they won't show up in the helptext. If I can find
        # a clean way to show the full list of supported scales in the
        # helptext, I'll do that.
        if not scale.endswith("ian")
    ]
    scale_command.add_argument(
        "scale",
        type=str,
        default="major",
        choices=scales.SUPPORTED_SCALES,
        metavar=f"[{'|'.join(_advertised_scales)}]",
    )

    parsed = parser.parse_args(args)

    if parsed.subcommand == "note":
        parsed_note = pitches.parse_note(parsed.note)
        found = DEFAULT_LAYOUT.find(parsed_note)
        render_found_buttons(found, parsed_note)
    elif parsed.subcommand == "chord":
        handle_chord(parsed.chord)
    elif parsed.subcommand == "scale":
        handle_scale(parsed.root, parsed.scale)

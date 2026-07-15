from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageSequence


CANVAS_SIZE = 220
MAX_SPRITE_SIZE = 204
FRAME_DURATION_MS = 83
# RunState/WalkFast travel 1.6x faster than walk (see src/panel/states.ts).
# Play the same frames 1.6x quicker so leg cadence matches travel and the
# sprite stops "skating".
RUN_DURATION_MS = round(FRAME_DURATION_MS / 1.6)
SHEET_BACKGROUNDS = {(138, 90, 157), (195, 134, 255)}


def remove_background(image: Image.Image, remove_magenta: bool = False) -> Image.Image:
    image = image.convert('RGBA')
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            is_sheet_background = (red, green, blue) in SHEET_BACKGROUNDS
            is_magenta = remove_magenta and red > 240 and green < 20 and blue > 240
            if is_sheet_background or is_magenta:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (red, green, blue, alpha)
    return image


def normalize_frame(image: Image.Image) -> Image.Image:
    bounds = image.getchannel('A').getbbox()
    if bounds is None:
        raise ValueError('Sprite frame has no visible pixels')
    sprite = image.crop(bounds)
    scale = min(MAX_SPRITE_SIZE / sprite.width, MAX_SPRITE_SIZE / sprite.height)
    sprite = sprite.resize(
        (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))),
        Image.Resampling.NEAREST,
    )
    canvas = Image.new('RGBA', (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
    left = (CANVAS_SIZE - sprite.width) // 2
    top = CANVAS_SIZE - sprite.height - 10
    canvas.alpha_composite(sprite, (left, top))
    return canvas


def load_gif(path: Path, remove_magenta: bool = False) -> list[Image.Image]:
    with Image.open(path) as source:
        return [
            normalize_frame(remove_background(frame.copy(), remove_magenta))
            for frame in ImageSequence.Iterator(source)
        ]


def load_sheet_frames(path: Path, regions: list[tuple[int, int, int, int]]) -> list[Image.Image]:
    with Image.open(path) as source:
        source = source.convert('RGBA')
        return [normalize_frame(remove_background(source.crop(region))) for region in regions]


def add_ball(frame: Image.Image) -> Image.Image:
    result = frame.copy()
    draw = ImageDraw.Draw(result)
    draw.ellipse((162, 91, 194, 123), fill=(21, 92, 22, 255))
    draw.ellipse((165, 94, 191, 120), fill=(79, 178, 51, 255))
    draw.rectangle((172, 98, 181, 104), fill=(173, 238, 105, 255))
    draw.rectangle((174, 96, 179, 98), fill=(226, 255, 177, 255))
    return result


def ping_pong(frames: list[Image.Image]) -> list[Image.Image]:
    if len(frames) < 3:
        return frames
    return frames + list(reversed(frames[1:-1]))


def save_gif(
    frames: list[Image.Image],
    path: Path,
    duration: int = FRAME_DURATION_MS,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    first, *rest = frames
    first.save(
        path,
        format='GIF',
        save_all=True,
        append_images=rest,
        duration=duration,
        loop=0,
        transparency=0,
        disposal=2,
        optimize=False,
    )


def save_character(
    output_dir: Path,
    name: str,
    idle: list[Image.Image],
    walk: list[Image.Image],
    run: list[Image.Image] | None = None,
    swipe: list[Image.Image] | None = None,
    with_ball: list[Image.Image] | None = None,
) -> None:
    character_dir = output_dir / name
    # walk_fast is the 1.6x run state: same frames, faster cadence.
    # run (ball chase) travels at walk speed, so it keeps the walk cadence.
    states = {
        'idle': (idle, FRAME_DURATION_MS),
        'walk': (walk, FRAME_DURATION_MS),
        'walk_fast': (run or walk, RUN_DURATION_MS),
        'run': (run or walk, FRAME_DURATION_MS),
        'swipe': (swipe or walk, FRAME_DURATION_MS),
        'with_ball': (
            with_ball or [add_ball(frame) for frame in idle],
            FRAME_DURATION_MS,
        ),
    }
    for state, (frames, duration) in states.items():
        save_gif(frames, character_dir / f'darkworld_{state}_8fps.gif', duration)

    icon = idle[0].copy()
    icon.thumbnail((128, 128), Image.Resampling.NEAREST)
    icon.save(character_dir / 'icon.png')
    icon.save(character_dir / 'icon_darkworld.png')


def build_kris(source_dir: Path, output_dir: Path) -> None:
    kris_idle = load_gif(source_dir / 'kris-idle.gif')
    kris_walk = ping_pong(load_gif(source_dir / 'kris-walk-right-darkworld.gif'))
    kris_dance = load_gif(source_dir / 'kris-dance.gif')
    save_character(output_dir, 'kris', kris_idle, kris_walk, kris_walk, kris_dance)


def build_spamton(source_dir: Path, output_dir: Path) -> None:
    # Spamton is a battle NPC with no overworld walk cycle on his sheet, so we
    # reuse animated previews: a 4-frame march for walking and a laugh emote.
    walk = ping_pong(load_gif(source_dir / 'spamton-walk.gif'))
    laugh = load_gif(source_dir / 'spamton-laugh.gif')
    idle = load_gif(source_dir / 'spamton-glitch.gif')  # 2-frame standing talk
    save_character(output_dir, 'spamton', idle, walk, walk, laugh)


def build_jevil(source_dir: Path, output_dir: Path) -> None:
    # Jevil only has a floating bounce; use the full loop everywhere so nothing
    # is a frozen single frame.
    bounce = load_gif(source_dir / 'jevil-dance.gif')
    save_character(output_dir, 'jevil', bounce, bounce, bounce, bounce)


def build(source_dir: Path, output_dir: Path) -> None:
    build_kris(source_dir, output_dir)

    lancer_idle = load_sheet_frames(
        source_dir / 'lancer.png',
        [(5, 44, 41, 79), (46, 44, 82, 79), (87, 44, 123, 79)],
    )
    lancer_walk = ping_pong(load_sheet_frames(
        source_dir / 'lancer.png',
        [(5, 84, 41, 119), (46, 84, 82, 119), (126, 84, 162, 119),
         (172, 84, 208, 119), (213, 84, 249, 119), (259, 84, 295, 119),
         (300, 84, 336, 119)],
    ))
    lancer_swipe = load_sheet_frames(
        source_dir / 'lancer.png',
        [(5, 124, 41, 159), (46, 124, 82, 159), (126, 124, 162, 159),
         (172, 124, 208, 159), (213, 124, 249, 159)],
    )
    save_character(output_dir, 'lancer', lancer_idle, lancer_walk, lancer_walk, lancer_swipe)

    ralsei_idle = load_sheet_frames(
        source_dir / 'ralsei.png',
        [(170, 54, 198, 98), (203, 54, 231, 98), (236, 54, 264, 98)],
    )
    ralsei_walk = ping_pong(load_sheet_frames(
        source_dir / 'ralsei.png',
        [(5, 152, 28, 196), (33, 152, 56, 196), (61, 152, 84, 196),
         (89, 152, 112, 196), (122, 152, 145, 196), (150, 152, 173, 196),
         (178, 152, 201, 196), (206, 152, 229, 196)],
    ))
    ralsei_dance = load_gif(source_dir / 'ralsei-dance.gif')
    save_character(output_dir, 'ralsei', ralsei_idle, ralsei_walk, ralsei_walk, ralsei_dance)

    noelle_idle = load_sheet_frames(
        source_dir / 'noelle.png',
        [(0, 262, 28, 311), (33, 262, 56, 311),
         (61, 262, 84, 311), (89, 262, 112, 311)],
    )
    noelle_walk = ping_pong(load_sheet_frames(
        source_dir / 'noelle.png',
        [(0, 370, 28, 416), (33, 370, 56, 416),
         (61, 370, 84, 416), (89, 370, 112, 416)],
    ))
    noelle_swipe = load_sheet_frames(
        source_dir / 'noelle.png',
        [(0, 421, 28, 467), (33, 421, 56, 467),
         (61, 421, 84, 467), (89, 421, 112, 467)],
    )
    save_character(output_dir, 'noelle', noelle_idle, noelle_walk, noelle_walk, noelle_swipe)

    susie_idle = load_sheet_frames(source_dir / 'susie.png', [(505, 5, 531, 51)])
    susie_walk = ping_pong(load_sheet_frames(
        source_dir / 'susie.png',
        [(505, 56, 530, 102), (535, 56, 560, 102),
         (565, 56, 590, 102), (595, 56, 620, 102)],
    ))
    susie_dance = load_gif(source_dir / 'susie-dance.gif')
    susie_eat = load_gif(source_dir / 'susie-eat.gif')
    save_character(output_dir, 'susie', susie_idle, susie_walk, susie_walk, susie_dance, susie_eat)

    build_spamton(source_dir, output_dir)
    build_jevil(source_dir, output_dir)

    tenna_bow = load_gif(source_dir / 'tenna-bow.gif')
    tenna_dance = load_gif(source_dir / 'tenna-dance.gif')
    tenna_dance_cane = load_gif(source_dir / 'tenna-dance-cane.gif')
    tenna_kick = load_gif(source_dir / 'tenna-kick.gif', remove_magenta=True)
    save_character(output_dir, 'tenna', tenna_bow, tenna_dance_cane, tenna_dance, tenna_kick)


def load_existing_frames(path: Path) -> list[Image.Image]:
    """Coalesce an already-built GIF back to full RGBA frames."""
    with Image.open(path) as source:
        return [frame.convert('RGBA') for frame in ImageSequence.Iterator(source)]


def retime(media_dir: Path) -> None:
    """Re-derive walk_fast/run from each character's shipped walk cycle so the
    run state animates 1.6x faster than walk (fixes the "skating" mismatch).

    Used when the hand-cut source sheets are unavailable but the walk frames
    already live in media/. A full `build` supersedes this."""
    for walk in sorted(media_dir.glob('*/darkworld_walk_8fps.gif')):
        char_dir = walk.parent
        frames = load_existing_frames(walk)
        save_gif(frames, char_dir / 'darkworld_walk_8fps.gif', FRAME_DURATION_MS)
        save_gif(frames, char_dir / 'darkworld_walk_fast_8fps.gif', RUN_DURATION_MS)
        save_gif(frames, char_dir / 'darkworld_run_8fps.gif', FRAME_DURATION_MS)
        print(f'retimed {char_dir.name}: {len(frames)} frames')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build VS Code Deltarune character GIFs')
    parser.add_argument('--source-dir', type=Path, default=Path('tmp/deltarune-sources'))
    parser.add_argument('--output-dir', type=Path, default=Path('media'))
    builders = {'kris': build_kris, 'spamton': build_spamton, 'jevil': build_jevil}
    parser.add_argument('--character', choices=('all', *builders), default='all')
    parser.add_argument(
        '--retime',
        action='store_true',
        help='Re-derive walk_fast/run from shipped walk GIFs (no source sheets needed)',
    )
    args = parser.parse_args()
    if args.retime:
        retime(args.output_dir)
    elif args.character in builders:
        builders[args.character](args.source_dir, args.output_dir)
    else:
        build(args.source_dir, args.output_dir)


if __name__ == '__main__':
    main()

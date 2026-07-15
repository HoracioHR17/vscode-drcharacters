# Deltarune sprite credits

The Deltarune character GIFs in `media/` were adapted for the VS Code Pets
animation contract from sprite sheets and animated previews hosted by
[The Spriters Resource](https://www.spriters-resource.com/pc_computer/deltarune/).

The original artwork and Deltarune characters belong to Toby Fox and the
Deltarune team. The following community members uploaded or prepared the
source sheets used by this project:

- [Kris (Chapter 1 + 2)](https://www.spriters-resource.com/pc_computer/deltarune/asset/110448/):
  uploaded by Kendotlibero; additional credits to asym, Eli101gamer,
  MrDoubleA, Sissel, Yuti and Bubbled.
- [Lancer](https://www.spriters-resource.com/pc_computer/deltarune/asset/110484/):
  uploaded by p0kin; additional credits to asym, MrDoubleA and Sissel.
- [Ralsei](https://www.spriters-resource.com/pc_computer/deltarune/asset/110469/):
  uploaded by Kendotlibero; additional credits to asym, Luxandre,
  Sissel and TattleameliaMLG.
- [Noelle](https://www.spriters-resource.com/pc_computer/deltarune/asset/110612/):
  uploaded by Dragon11136; additional credits to asym, Sissel and
  wrongsave.
- [Susie](https://www.spriters-resource.com/pc_computer/deltarune/asset/110471/):
  uploaded by Kendotlibero; additional credits to asym, Sissel and
  TattleameliaMLG.
- [Spamton](https://www.spriters-resource.com/pc_computer/deltarune/asset/162176/):
  uploaded by Askywalker; additional credits to asym and smgboneys75.
- [Jevil](https://www.spriters-resource.com/pc_computer/deltarune/asset/110456/):
  uploaded by Modern.
- [Tenna](https://www.spriters-resource.com/pc_computer/deltarune/asset/273063/):
  uploaded by Zavemann.

## Rebuilding from source

The sheets are not committed (they belong to Toby Fox / the Deltarune team).
Fetch them into a local, gitignored folder and rebuild:

```
python3 scripts/fetch_deltarune_sheets.py   # -> tmp/deltarune-sources/
python3 scripts/build_deltarune_sprites.py  # -> media/
```

If you only need to refresh the run cadence from the walk GIFs already in
`media/` (no source sheets required):

```
python3 scripts/build_deltarune_sprites.py --retime
```

The generated GIFs normalize the source frames to a transparent 220x220 canvas.
Walking sheets use reversible (ping-pong) cycles to avoid a hard jump between
the last and first frame. The overworld sprites only have a walk cycle, so the
`walk_fast`/run state reuses the walk frames played ~1.6x faster (50ms vs 80ms
per frame) to match the 1.6x run travel speed in `src/panel/states.ts` — this
keeps the legs in step with the movement instead of "skating".

Some characters have no walk cycle on their static sheet and instead use the
animated GIF previews hosted on the same asset pages (`fetch_deltarune_sheets.py`
downloads these as well):

- **Jevil** has only a floating bounce, so every state uses that 8-frame loop
  (previously idle was a single frozen frame).
- **Spamton** uses a 4-frame march for walking and a laugh emote for swiping.
- **Tenna**'s long dance/kick previews are intentional: they already loop
  cleanly (the last→first seam is smaller than the average frame step), so they
  are kept as-is rather than trimmed.

The extension displays characters at `medium` size by default. Tenna receives a
2x runtime scale so his proportions remain visibly larger than the rest of the
cast. A green ball is added only when an original interaction animation is not
available and the catching mechanic requires one.

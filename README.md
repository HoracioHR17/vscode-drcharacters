# Deltarune Characters for VS Code

A Deltarune-focused fork of VS Code Pets. It places animated Deltarune
characters in the Explorer or panel while you work.

## Characters

- Kris
- Lancer
- Ralsei
- Noelle
- Susie
- Spamton
- Jevil
- Tenna

All characters use their Dark World presentation. The default display size is
`medium`; Tenna intentionally renders at twice the scale of the rest of the
cast to preserve his larger proportions.

## Run locally

1. Open this repository as the workspace in VS Code.
2. Run `npm install`.
3. Press `F5` and choose **Run Extension**.
4. In the Extension Development Host, run
   **Deltarune Characters: Start Deltarune character session** from the command
   palette.

Use the `vscode-pets.petType` setting or the spawn-character command to choose
another member of the cast.

## Development

```powershell
npm run compile
npm test
```

The animation build pipeline is in `scripts/build_deltarune_sprites.py`. Source
credits and links are documented in `docs/deltarune-assets.md`.

## Credits

Deltarune and its characters belong to Toby Fox and the Deltarune team. Sprite
sheets and animation previews are adapted from community rips hosted by
[The Spriters Resource](https://www.spriters-resource.com/pc_computer/deltarune/).

This project retains the generic movement and interaction engine from the
open-source VS Code Pets extension.

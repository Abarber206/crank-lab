# Building tests

Run with Node and Playwright (Chromium), from a folder that has `three` and `peerjs` in `node_modules` (see `h.js`).

- `tedit.js` — the 38 checks from Part 16 of `../EDIT_SPEC.txt`: every edit configuration, collision, reset, structure, ownership.
- `mp_edit.js` — two real players over a local PeerJS server: edits sync, a guest's edit that cuts support collapses on both screens, forged shapes are refused. Needs the `peer` and `express` packages.
- `thouse2.js` — every town house piece is held up under the support rules.
- `tsky.js` — skydiving: a drop from 620 m dives, opens the glider by itself about 85 m up, lands with no fall damage; Jump opens it early; no building or shooting in the air.
- `mp_sky.js` — a friend sees you in freefall (belly-down), gliding (glider out) and landed. Needs the `peer` and `express` packages.

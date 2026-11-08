# Building tests

Run with Node and Playwright (Chromium), from a folder that has `three` and `peerjs` in `node_modules` (see `h.js`).

- `tedit.js` — the 38 checks from Part 16 of `../EDIT_SPEC.txt`: every edit configuration, collision, reset, structure, ownership.
- `mp_edit.js` — two real players over a local PeerJS server: edits sync, a guest's edit that cuts support collapses on both screens, forged shapes are refused. Needs the `peer` and `express` packages.
- `thouse2.js` — every town house piece is held up under the support rules.
- `tsky.js` — skydiving: a drop from 620 m dives, opens the glider by itself about 85 m up, lands with no fall damage; Jump opens it early; no building or shooting in the air.
- `mp_sky.js` — a friend sees you in freefall (belly-down), gliding (glider out) and landed. Needs the `peer` and `express` packages.
- `tkart.js` — dune buggies: they're parked in garages; Drive / Get out prompts; it accelerates to its top speed, steers the right way, brakes and reverses, stops at the garage's back wall, and you get out beside it.
- `mp_kart.js` — a buggy in a party: the host drives and a friend sees it move with the driver seated, the friend rides as passenger, and the parked buggy ends up in the same place for both. Needs the `peer` and `express` packages.
- `tswap.js` — with full slots, Interact swaps the weapon in your hands for one on the ground; map houses can't be edited under any edit setting; the mouse wheel steps a scope's zoom in and out.
- `tslope.js` — mountainsides: you can't walk up a 45°+ face, you slide down it with no fall damage, and gentle hills are still walkable.

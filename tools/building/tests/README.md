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
- `tquick.js` — the drop from the sky happens with the bot on; the Kettle Creek–Copper Ridge and Hollow Hill–Brambleford roads exist; a buggy on a cliff slides back; walking past the old circular edge is no longer stopped.
- `thsky.js` — a zombie horde game starts with a drop from the sky.
- `trsky.js` — pressing Respawn drops you back in from the sky.
- `tstair.js` — house stairs: walking at the handrail from a middle step, you stay on the stairs.
- `mp_drop.js` — a party match drops both players high up a few metres apart, each with just a pickaxe.
- `twalk.js` — no yard tree stands on a front path, driveway or sidewalk.
- `tglide.js` — Jump opens the glider, Jump again lets go into freefall, Jump again redeploys; you land unhurt.
- `tzdie.js` — a killed monster is obliterated (gone within a moment).
- `tmapz.js` — the full map zooms in toward the cursor and shows the real houses and garages.
- `tkdmg.js` — crashing a buggy again and again wrecks it and throws the driver clear.
- `ttracer.js` — tracers and bullet streaks leave from the muzzle (standing, running, every gun), stepped at 60 fps.
- `tcrawl.js` — knocked down on flat ground, up, down and across a slope, lying still and crawling: nothing sinks in, the chest rests on the ground, the body follows the slope.
- `tskyview.js` — pictures from high in the sky (FOV=6 zooms on a town: roofs must not flicker); GLIDE=1 with the glider out.
- `tupview.js` — pictures from the top of the stairs in two-storey houses: the hallway and the doors off it.
- `tswim.js` — dropped into deep water from 30 m: no damage, you swim with your head out, can't shoot or aim, swim slower than you run, and climb out onto the beach.
- `tswimai.js` — a monster wades and swims out to you; Buddy swims after you and holds fire.
- `tboat.js` — boats are moored in water deep enough; drive one (top speed, turning), it never goes up onto land, and getting out in deep water leaves you swimming.
- `twbuild.js` — building from the water starts on the seabed (walls and stairs below level 0, floors no lower than the bed); on land nothing changes.
- `tperf.js` — draw calls and triangles of each pass (main, reflection) at a riverside view, plus a picture.
- `tlocker.js` — Locker preview pictures: a pickaxe just picked and a second later, and emotes (EMOTES=salute,groove).
- `tlobby3d.js` — pictures of the 3D lobby (desktop and phone landscape), the Friends, Profile and Locker tabs, and the Mode pop-up.
- `mp_friends.js` — friends: B adds A by account number, A accepts, both see each other online with names; A invites B to the lobby and B joins A's party and stands on A's pads. Needs the `peer` and `express` packages.
- `temowheel.js` — the emote wheel: in the lobby (tap one, the hero does it on its pad), in a match (hold the key, move the mouse, let go; a quick tap plays the Locker emote); the other lobby tabs are solid.

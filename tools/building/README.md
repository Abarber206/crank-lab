patch183.py — uplifted island: the map ends at a sheer cliff over an open ocean, far mountains across the water, the lagoon spills over the edge as a waterfall (mist, foam)
patch184.py — swimmers near the lagoon's mouth are pulled by the current, carried over the falls and eliminated when they hit the sea
patch185.py — 30-player battle royale; beaten bots flee and heal, brave (skilled) ones keep pushing
patch186.py — longer draw distances (trees, terrain detail, people, loot, props, towns)
patch187.py + bus.js — battle bus remodelled: a city bus under a striped hot-air balloon
patch188.py + gunkit.js — guns differ by rarity in shape: grips, sights, scope, brake/compensator, laser, longer mags
patch189.py — sound: per-rarity gun sounds, speed-of-sound delay, bullet whiz, waterfall and cliff surf, ambience ducking
patch190.py + indoor.js — dim interiors and shade under tree canopies
patch191.py — river banks: wet earth, sand patches, grass thinning out, damp tint
patch192.py — BR bots: two guns and swapping, materials, building (walls, ramps, rushes, boxes), aim settle/spray, shoot through walls
(patch188 + gunkit.js retired: rarity changes damage only)
patch193.py — rarity changes damage only (not reload)
patch194.py + housedecor.js — paintings, lamps, rugs and curtains in houses; panelled lighter doors; indoor light tuned
patch195.py — bots land on loot, loot further, edit windows in their walls, hear you through walls, remember fights
patch196.py — BR kill feed with weapon/distance, end-of-life summary, spectating, Victory Royale summary, storm murk + lightning
patch197.py — shots/line of sight only test pieces in grid cells along the ray (8x faster)
patch198.py + weather.js — rain in some matches
patch199.py — phones: one WebGL context (icons/portraits drawn offscreen by the game's renderer), locker portraits on demand, no island photo in the lobby, shorter draw distances and smaller light map, reload on context loss
patch200.py — Fortnite-style hotbar: big diagonal guns on rarity-coloured slots, ammo count with its mark
patch201.py — 100 players; far bots drawn as one merged figure and updated less often; spectator camera behind the shoulder (never in the ground or walls) with the player's health and gun; more floor loot
patch202.py — small far objects skipped when drawing (never pieces, never for shots); house decor drawn only near its town
weather.js — rain only inside the storm, dark and purple
patch203.py — the storm forms ~90 s after the bus (land anywhere); HUD counts down to it
patch204.py + harvest.js — Fortnite-style weak point on whatever you pickaxe (moves after each hit, crits for double), health bar for the thing you're breaking
trees.js — new pine shape (solid drooping tiers), rounder oak crowns with fewer cards poking out
poi_*.js / decor.js — open sheds and bays stand on posts; detailed lorries (poiRig) at Gearworks, Timber Yard, Crater Labs; trebuchet + supplies in Fort Granite; drying shed, chipper, loader at Timber Yard; Gearworks gatehouse and boiler house detail; clipping fixed (ruin rubble, cabin porch/chimney, office barrier, log piles one object)
tests/tpoiclip.js — lists every solid/visible overlap at the points of interest; tpoieye/tpoitop/tpoishot — pictures of them

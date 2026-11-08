# Crank Lab

A browser build-fight practice range: Chapter 1-style movement, turbo build, wall / floor / ramp / cone edits, and fully custom keybinds (mouse side buttons and scroll wheel included).

**Play:** https://abarber206.github.io/crank-lab/

## Menu
The menu has four tabs: **Play** (mode, party and match buttons), **Locker**, **Settings** and **Controls**. Your points show in the top corner.

## Locker and shop
Seven outfits are free: Rook, Nova, Ember, Sprig, Volt, Glacier and Whisk. So are six pickaxes: Steel Pick, Bonk Mallet, Neon Cleaver, Geode Pick, Frostreap and Gilded Pick. Each outfit has its own hair or headwear, top and back bling.

Another 12 outfits and 6 pickaxes are in the shop. You pay for them with points earned in zombie horde:
- 10 points per Walker, 15 per Runner and 60 per Brute
- a bonus for every wave you clear: 20 + 10 × the wave number

Points pop up where the kill happened. Locked items show their price. Click one you can afford, confirm, and it's yours and equipped.

| Rarity | Outfits | Outfit price | Pickaxes | Pickaxe price |
| --- | --- | --- | --- | --- |
| Common | Scout, Mason | 150 | Crowbar | 100 |
| Uncommon | Drift, Moss | 300 | Trench Shovel | 200 |
| Rare | Dusk Ranger, Blaze, Frostbyte | 600 | Summit Axe, Sledge | 400 |
| Epic | Jinx, Thorne, Marina | 1,000 | Bone Breaker | 700 |
| Legendary | Nightfall, Regalia | 1,600 | Sweet Swing | 1,100 |

Your points and what you own are saved in this browser. Everyone in a party sees your outfit and pickaxe, and the bot wears a free outfit.

## Characters and animation
Characters have realistic proportions: an oval head with ears, nose, brows and natural eyes; a shaped torso; slim arms, hands and legs; and sneakers. Hair and headwear sit on the head properly. A pickaxe is carried angled up past the shoulder, and a swing throws the whole body: the hips turn with the chest, the knees dip on impact and the free arm pulls back.

## The map and materials
The island is about 1.6 km across, closed in by a ring of big snow-capped mountains you can't climb past. The middle (about 40 m around spawn) is flat for build fights. Rolling hills spread out from it, four rocky mountain ranges (95–170 m high) rise inside the island, and the outer range climbs to about 450 m. Ten towns are joined by asphalt roads with white edge lines and a dashed yellow centre line, and one road runs from the build field to the nearest town. Hillsides turn to bare rock where they get steep, snow sits above the snowline, and the road shoulders are dirt. Overhead is a deck of volumetric clouds (real 3D cloud, ray-marched) that swirl and curl as they drift, with shaded undersides, bright silver linings when you look toward the sun, and a pink glow at dusk. Settings > Clouds switches between Volumetric, Simple (the old puffs, lighter on older devices) and Off. The map is generated from integer maths only, so every player in a party builds exactly the same mountains, towns, roads, trees and chests.

You can walk and build anywhere: builds that touch the hillside count as supported, and on a slope a piece drops a level to meet the ground. About 520 trees, 520 pines (higher up), 220 rocks (on rocky ground) and 40 cars (25 parked along the roads) are scattered around. The cars come in four body styles (sedan, hatchback, pickup with an open bed, SUV with roof rails) and eight paints, with glass cabins, hubcaps, bumpers, lights, mirrors and door handles; the junkers are rusting. They keep off roads, towns and snow. Pickaxe trees for wood, rocks for brick and cars for metal; they grow back 35–80 seconds after they're gone. Materials are infinite by default. Turn off **Infinite materials** in Settings and every piece costs 10 of the selected material: you start with 30 wood, your counts show on the right, and clearing a horde wave gives a bonus.

- **Minimap.** Shows the roads, streets, sidewalks, houses, builds, trees, chests and players around you, and town names when a town is in view.
- **Full map.** Press **M** (bindable) or tap the minimap for the whole island: hillshaded terrain, roads, towns, players and your arrow. Press M again, click or tap to close it.
- **Terrain detail** is drawn in 128 m chunks at three levels of detail that follow the camera, so the whole island stays in view without slowing down.

## Look and performance
- **Build materials** are painted with real relief: grain, knots and nail heads in wood; chipped, bevelled stone blocks in recessed mortar; and corrugated steel with rivets, scratches and rust streaks. A normal map makes each one catch the light, and metal has a soft sheen.
- **Models** are smoothly shaded, with no cartoon bands or black outlines.
- **Guns** are built from one parts kit, so every gun is in proportion and its parts join up. Grips rake back with finger grooves, trigger guards sit under the receiver, and magazines seat in a magazine well. Stocks are shaped, and barrels carry real muzzle devices: brakes, flash hiders, compensators and suppressors.
- **The world** has wind-blown grass and little flowers around you that stay out from under builds. Bushes are scattered across the island. Trees have lumpy leaf clusters and branches, pines have ragged tiers, and boulders are chipped with moss on top. Shadows no longer crawl as you move.
- **Performance:**
  - Characters and zombies are batched: each joint is one mesh instead of dozens. A player went from about 200 draw calls to about 30.
  - Dust and smoke puffs are pooled.
  - **Auto resolution** (on by default) lowers sharpness a little when the frame rate drops and raises it again when there's headroom.
  - **Grass detail** (Off, Low, Medium, High or Ultra) sets how far and how thick the grass grows. It defaults to High on computers and Medium on phones. Turn it down, or turn off **Shadows**, on slower devices.

## Zombie horde
Pick **Zombie horde** next to Play. You get 20 seconds to build a fort, then waves of zombies walk in from every side. The horde is Austin's purple creatures: no eyes, a head that rises into a flickering crown of flame, and ragged holes torn right through them that burn from inside (hot pink, orange on Brutes, acid green on Hurlers), so they glow in the dusk of a horde round. They hunch forward on bent legs with their heads jutting out, long blade arms hanging low with hooked claws, mottled, veined skin that gets darker toward the hands and feet, and a bony ridge down the back. Every creature gets its own random holes and veins. There are four kinds:

- **Walkers** lurch forward in surges, dragging their right leg.
- **Runners** (from wave 2) are skinny and crouch almost on all fours, galloping with their arms like front legs.
- **Hurlers** (from wave 3) have glowing growths on the right shoulder. They hang back 7–20 m, tear off a chunk and lob it at you: 20 damage on a direct hit, a bit less from the splash, and 60 to any build it hits, so walls protect you but get worn down.
- **Brutes** (from wave 4) are huge, with a humped back, spiked shoulders and a small head.

The first time one gets close it rears up and screeches. Before a swipe it rears back with its arms up, then lunges forward and rakes down, so you can see it coming. Hits are measured from the real models: the head and flames count as headshots, and the legs, body and arms are body shots. Hits splash purple. Their groans fade out quickly with distance. They have to be right next to you to hit you and can't claw through walls. Zombies claw through anything built in their way, and if you're up on a tower they go for the piece holding it up. A wave bar under the compass shows the wave and how many creatures are left, draining as you kill them, or the countdown to the next wave. It appears when something changes and fades out after a few seconds, then stays up and pulses orange in the last 5 seconds of a break. Clearing a wave gives you a 15-second break, 50 shield, 30 health, 3 bandages and 2 small shields. In a party the leader picks the mode and runs the zombies for everyone, and each player gets the points for their own kills; zombies get tougher and waves bigger with more players, and anyone who goes down is back in 3 seconds.

## Towns, houses and chests
Ten towns sit on the flattest lowland spots around the island (Rustwood, Pebble Point, Kettle Creek, Lantern Row, Mossy Mill, Hollow Hill, Cinder Flats, Brambleford, Copper Ridge and Willow Bend). Each is laid out on a grid: a main street and a cross street meet in the middle and split the town into four blocks. Six to eleven houses stand in rows along both streets on levelled ground, each facing its street with a front yard and a gap to its neighbours. The roads from other towns run in to the ends of the streets. A town's name pops up when you walk in.
- **Houses look like houses.** Outside they're painted lap siding, stucco with a stone plinth, or modern board-and-batten panels, in a range of colours, with trim round the windows and doors, shutters, a porch lamp and closed gable ends. Roofs are asphalt shingles or clay tiles. Inside there are painted walls with baseboards, hardwood floors and white ceilings.
- **Sidewalks.** Concrete sidewalks run down both sides of every street, and a path runs from each front door out to the sidewalk.
- **Stairs.** Two-storey houses have a real staircase: 20 steps along an inside wall up to a landing, under a stairwell with a railing round it. You walk up it step by step.
- **Farming.** Underneath, every house is still wood, brick or metal (siding is wood, stucco is brick, panels are metal). Pickaxe a house to farm that material, 4–8 a hit, and aim at a piece to see its health.
- **Houses** are made of real build pieces, so you can shoot, pickaxe, crack and collapse them. **Clear builds**, or the start of a new round, puts them back.
- **Chests.** Gold-banded chests sit in houses (some upstairs) and out in the wild. They hum and glow when you're close and show as gold squares on the minimap. Stand next to one for half a second and it bursts open, throwing out:
  - a gun (any rarity, with rarer ones less likely)
  - ammo for that gun
  - often a bonus: heals, grenades or extra ammo

  Opened chests refill after a couple of minutes.
- **Floor loot.** Guns and ammo lie on the floors of houses from the start.
- **In a party**, the host opens every chest, so two players can never loot the same one. Damage to houses and opened chests stay in sync, including for players who join later.

## Trees, rocks and cars
Trees, pine trees, rocks and old cars are scattered around the map. They're solid, so you, the bot and zombies have to go around them. Materials are infinite by default. Turn off **Infinite materials** in Settings and every build costs 10 of its material: pickaxe trees for wood, rocks for brick and cars for metal (your stock shows on the right). You start each life with 30 wood. Anything you harvest grows back in its spot after 35–80 seconds. In a party everyone sees the same map, and the host decides when things grow back.

## Inventory, weapons and loot
Every weapon's icon on the hotbar and in the inventory is a picture of the gun you actually hold, with its stock, magazine, sights, muzzle device and rarity trim. Bandages and shield potions have their own models too, on the ground and in your slots.
You carry a pickaxe plus 5 slots (keys 2–6) that hold any weapon or item. Press **Tab** (bindable) to open the inventory. Everything is drag and drop:
- Drag a slot onto another slot to move it there, or swap the two.
- Drag a slot onto the drop area, or anywhere outside the panel, to drop it on the ground. Ammo works the same way.
- Drag loot from the *On the ground nearby* list straight onto a slot. Whatever was in that slot is dropped in its place.
- Click a slot to select it; click it again to equip it.

On phones, the bag button opens the inventory. You can also hold a weapon in the hotbar for a moment and drag it onto another slot (empty ones show up while you drag).

### Weapons
There are 22 guns plus grenades, and most come in several rarities: Common (grey), Uncommon (green), Rare (blue), Epic (purple) and Legendary (gold). That makes 67 guns in all. The rarer the gun, the more damage it does and the faster it reloads. Guns do a quarter less damage than they used to (builds take the same damage as before). Each gun's trim shows its rarity colour, and the inventory names the rarity.

| Type | Guns |
| --- | --- |
| Rifles | Assault Rifle, Burst Rifle (3 rounds per pull), Heavy Rifle, Infantry Rifle |
| Scoped rifles | Scoped Rifle, Bolt-Action Sniper (scope view, bolt cycles after each shot), Hunting Rifle |
| Shotguns | Pump Shotgun, Tactical Shotgun, Heavy Shotgun, Double Barrel |
| SMGs | Submachine Gun, Compact SMG, Suppressed SMG (quiet) |
| Pistols | Pistol, Revolver, Hand Cannon |
| Heavy guns | Machine Gun, Light Machine Gun, Minigun (spins up before it fires) |
| Explosives | Rocket Launcher, Grenade Launcher (bouncing grenades that burst on anyone they hit), Grenades |

Guns use light, medium, heavy, shell or rocket ammo, and reloads come out of your reserves.

### Aiming
- **The crosshair shows exactly where your shots can land.** Every bullet or pellet lands inside it, spread evenly, with no stray outliers. It grows as you move, jump or keep firing. When your first-shot accuracy is ready, it tightens.
- **Each kind of gun has its own crosshair.** Rifles, SMGs and pistols have four ticks. Shotguns show the pellet ring with a centre dot. Scoped guns have short ticks and a dot. Launchers and grenades show a dashed ring.
- **Aiming down sights** tightens the crosshair and adds a centre dot.
- **The scope view** has a fine crosshair with thick outer posts, range marks and a red centre dot.

### Gun animation
Each shot kicks the gun back. Pistol slides blow back, the revolver's cylinder turns one chamber per shot, and the pump fore-end racks. Bolt-action rifles lift, pull and push the bolt after every shot, and the double barrel breaks open to reload.

In zombie horde, demons sometimes drop loot when they die: about half drop nothing, others drop a random kind of ammo (not necessarily what you use), now and then a gun, heals or grenades, and Behemoths usually drop a gun. Loot falls and lands on the ground or on builds, and you pick it up by walking over it. In build fights ammo reserves are endless.

## Fall damage
Like Fortnite: drops up to 10 m are free. Past that you take 7 damage for every extra metre, straight to health (shields don't soak it), so a fall of about 24 m or more eliminates you.

## Heals
Slot 4 is bandages (15 health each, up to 75, 3.5 s) and slot 5 is small shield potions (25 shield each, up to 50, 2 s). Click to use one, hold fire to keep using them. You start with 5 bandages and 3 small shields.

## Teams
On the Play tab, pick a team. Teammates can't damage each other, and have a marker over their heads and a coloured dot on the minimap. In zombie horde everyone is on the same side.

## Opponent
A bot that strafes, shoots, walls up when hit, ramp rushes when you take height, and boxes up to peek through window edits. On **Adaptive** it measures your accuracy, build speed, edits and damage over the last 40 seconds and matches it, nudging harder when you win rounds and easier when you lose. Fixed Easy to Expert levels are in the menu. In a multiplayer party the host's game runs the bot for everyone: it goes after the nearest player, its builds and edits show up for everyone, anyone can eliminate it, and it comes back 3 seconds later. The host picks its level in the menu (Off removes it).

You can't build through walls: a spot behind a wall (or a window) is blocked, but you can build through a door.

## Parties and multiplayer
On the Play tab, type a name and press **Create party**. Share the 5-letter code (**Copy code** copies it), and friends type it and press **Join**. Up to 8 players.
- **The party list** shows everyone, who leads and who's ready.
- **Members** press **Ready**.
- **The leader** picks Build fight or Zombie horde, then presses **Start match**. That clears the builds and drops everyone in.
- **Back to lobby** ends the match for everyone.
- **Joining mid-match** puts you straight into it.
- **When the leader leaves**, the party closes for everyone.

Multiplayer is peer-to-peer (WebRTC via [PeerJS](https://peerjs.com)), no server to run. The host is the source of truth for builds: it checks every placement and edit, decides what collapses when a support breaks (so everyone sees exactly the same result) and corrects conflicts, including two players editing the same piece at once. Players can shoot each other; each player applies the damage they take, eliminations show in the feed, and you respawn after 3 seconds. Build damage, health, materials, edits and half stairs stay in sync, and late joiners get the whole map. The party leader is the host.

## Default PC binds
| Action | Bind |
|---|---|
| Move | W A S D |
| Jump | Space |
| Crouch | Left Shift |
| Wall / Floor / Ramp / Cone | Q / F / E / C |
| Place (hold for turbo) | Left mouse |
| Edit / confirm | G |
| Reset edit | Right mouse |
| Rotate ramp | R |
| Pickaxe | 1 |
| Assault rifle | 2 |
| Pump shotgun | 3 |
| Reload | T |
| Switch material | X |
| Full map | M |

Every bind can be changed in the menu.

## Building rules
- **Preview.** Green outline: it will build. Red outline plus the reason underneath: *Already built*, *Nothing to attach to*, *Out of reach*, *Wall in the way*, *Player in the way*, *Build height limit* or *Edge of the map*. A grey outline means the spot is taken. Every placement (yours, the bot's, a joining player's) goes through the same validator, and in a party the host checks it again.
- **Materials.** Wood 150/140, brick 300/280, metal 500/460 max health (wall / other pieces). Builds start weaker and gain health while they finish. Start health, build-up times, damage resistance, crack thresholds and debris are all in `MATERIALS` and `BUILD_CFG` near the top of the script.
- **Construction.** A piece appears as a blue blueprint with a material-coloured frame, then fills in section by section: wood plank by plank, brick course by course, metal in a few big panels. Walls rise from the bottom, floors grow out from the side they're attached to, stairs build from the low end up and roofs from the base.
- **Three separate systems.** Every piece has a *shape* (what it looks like: which tiles are left, which way a stair runs), *collision* built from that same shape (what you walk into, stand on, bump your head on, shoot through and see through) and *structural support* (what holds it up). Each edit updates all three in that order, and none stands in for another: a piece can look like it floats and still be held up, and an opening can look solid but have nothing to bump into.
- **Support.** Pieces hold each other up only through a shared edge or face; floors that only touch at a corner don't count. Anything resting on the ground is *anchored*; anything with a chain of connections down to the ground is *supported*. Attachments come from what's left of a piece: an edit that removes the tiles along a shared edge removes that connection too. Aim at a build with the pickaxe or in build mode to see its health, whether it's anchored, and how many pieces it's holding up. When a piece is destroyed or edited, only the pieces it touched are re-checked: a group that still has another way down stays up (a platform on two walls survives losing one), and a group with none left collapses.
- **Damage and collapse.** Builds crack in three stages as they take damage (splits and splinters in wood, cracked and chipped brick, dents and scratches in metal) and shudder when hit. A destroyed piece bursts into its own material: planks, bricks, or metal panels and sparks. A piece that loses its support does something different: it darkens, shudders, tips away from the break, falls and crumbles into dust and debris, with pieces farther from the break going a moment later. It stops blocking you the instant it loses support.
- **Wall edits.** 3×3 tiles, and only the edits Fortnite really has (from the reference sheets), each with its mirror image: center, side and left+right windows; center and side doors; center and side arches; window door; half wall, low wall and half wall door; columns; partial low and half walls; 45° cuts and triangles. That's 27 shapes, named live as you pick tiles; any other selection turns red. 45° cuts are cut on the diagonal and collide along the diagonal.
- **Floor and roof edits.** 2×2 tiles: 3/4, half, the diagonal bridge and 1/4 floors (at least one tile stays). Roofs raise corners: corner roof, ridge, ramp roof, pocket (at least one corner stays down).
- **Stair edits.** Four big squares plus Fortnite's thin center strip. Drag across two side-by-side squares for a half stair, three in an L for an L stair, or all four in a U for a spiral stair; each rises the way you drag. Drag straight across the center strip to turn the whole stair to rise that way. L and spiral stairs climb to half height, cross a landing at each turn and climb to the top.
- **Editing.** Edits are named live as you pick tiles, and a pattern that isn't a real edit turns red until you fix it. Reset puts a wall, floor or roof back to its full shape, and turns a stair back into a full stair facing the way it faces now (not the way it was placed). It keeps the piece's health, owner and material, it never brings back pieces that already fell. Cancelling leaves it untouched. An edit that takes away the last support of something else is still allowed; that piece falls (the edited piece too, if it no longer touches anything). In Settings, **Who can edit builds** lets you choose between only the builder, the builder and teammates, or anyone. In a party the host's choice counts, and the host re-checks every edit's permission and shape. When a player leaves, their builds become editable by everyone.
- **Your collision.** You're an upright capsule (a round footprint 0.68 m across, 1.8 m tall, 1.25 m crouched), so you fit through doors and arches, can't fit through a window even jumping, can jump over a low wall, fall through removed floor tiles, and bump your head on what's above you.
- **Build limit.** Up to 1,500 of your own builds; past that your oldest build goes. The towns' houses don't count toward it.

### Where this approximates Fortnite
Exact Fortnite numbers and rules aren't public, so these are decisions, all adjustable in `BUILD_CFG` or the shape rules:
- **Wall edit list.** The 27 accepted wall edits are the ones on the Fortnite reference sheets (cheat sheets and guides) plus their mirror images. Fortnite has no official published list, so a rare edit that exists in Fortnite but isn't on those sheets may be missing; it's one line to add in `WALL_SHAPES`.
- **Edits and support.** Here an edit that removes the tiles along a shared edge removes that connection. That matches the Fortnite tip that cutting the half of a floor touching its only support breaks it, but exactly which edits break which connections in Fortnite isn't documented.
- **L and spiral stairs** use a landing at each turn. Fortnite's exact step layout for these may differ.
- There's no limit on how far a structure can reach from the ground, as long as there's an unbroken chain to it (`maxSupportDepth: 0`). Set a number to cap overhangs.
- Start health, construction time and crack thresholds are estimates.

### Tests
The building system is checked against the editing rulebook (`tools/building/EDIT_SPEC.txt`) by 38 scripted checks run in a real browser:
- **Every configuration:** all 511 wall selections (27 valid, 484 refused; each valid one checked for no collision where tiles were removed, collision on every tile left and one attachment per tile), all floor and roof shapes, and every half, L, spiral and turned stair.
- **Collision:** walking into a wall, through a door, jumping over a low wall, failing to fit through a window, standing on and falling through floor quarters, climbing half and L stairs, standing on an edited roof, bumping your head under a stair (and not once that half is removed), and shots and sight through and around a doorway.
- **Reset:** edit, reset and edit again many times; a reset stair keeps the way it faces; after moving; after a neighbour was destroyed.
- **Structure:** the 12 cases in the rulebook (ground, wall, platform, tower, bridge with two supports and with one, an edit that drops a wall standing on a floor, an edit that drops a platform, a destroyed stair and a turned stair, resetting after a change) plus a platform that survives losing one of two supports.
- **Ownership:** your builds, other players' builds, map buildings, destroyed pieces, cancelling, and the host refusing impossible shapes.
- **Two real players:** a guest's arch and L stair look and collide the same on the host, a guest's edit that cuts support makes the platform fall on both screens, and a forged impossible shape is refused.
- Controller supported (standard gamepad mapping); see the in-game menu for the layout.

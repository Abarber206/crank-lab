# Crank Lab

A browser build-fight practice range: Chapter 1-style movement, turbo build, wall / floor / ramp / cone edits, and fully custom keybinds (mouse side buttons and scroll wheel included).

**Play:** https://abarber206.github.io/crank-lab/

## Locker
Pick an outfit in the menu: Rook, Nova, Ember, Sprig, Volt, Glacier or Whisk. Each has its own hair or headwear, top and back bling. Below the outfits are six pickaxes: Steel Pick, Bonk Mallet, Neon Cleaver, Geode Pick, Frostreap and Gilded Pick. Everyone in a room sees your outfit and pickaxe, and the bot wears a different outfit.

## The map and materials
The island is about 800 m across, ringed by mountains you can't climb past. The middle (about 40 m around spawn) is flat for build fights, and rolling hills rise all around it, getting taller toward the edge. You can walk and build anywhere: builds that touch the hillside count as supported, and on a slope a piece drops a level to meet the ground. Trees, pines, rocks and junk cars are scattered around the range, the same for everyone in a room. Pickaxe trees for wood, rocks for brick and cars for metal; they grow back 35–80 seconds after they're gone. Materials are infinite by default. Turn off **Infinite materials** in Settings and every piece costs 10 of the selected material: you start with 30 wood, your counts show on the right, and clearing a horde wave gives a bonus.

## Look and performance
- **Build materials** are painted with real relief: grain, knots and nail heads in wood; chipped, bevelled stone blocks in recessed mortar; and corrugated steel with rivets, scratches and rust streaks. A normal map makes each one catch the light, and metal has a soft sheen.
- **Models** are smoothly shaded, with no cartoon bands or black outlines.
- **The world** has wind-blown grass and little flowers around you that stay out from under builds. Bushes are scattered across the island. Trees have lumpy leaf clusters and branches, pines have ragged tiers, and boulders are chipped with moss on top. Shadows no longer crawl as you move.
- **Performance:**
  - Characters and zombies are batched: each joint is one mesh instead of dozens. A player went from about 200 draw calls to about 30.
  - Dust and smoke puffs are pooled.
  - **Auto resolution** (on by default) lowers sharpness a little when the frame rate drops and raises it again when there's headroom.
  - **Grass detail** (Off, Low, Medium, High or Ultra) sets how far and how thick the grass grows. It defaults to High on computers and Medium on phones. Turn it down, or turn off **Shadows**, on slower devices.

## Zombie horde
Pick **Zombie horde** next to Play. You get 20 seconds to build a fort, then waves of zombies walk in from every side. The horde is pale, rotting, bloodied zombies: Walkers, fast Runners (from wave 2) and big bloated Brutes (from wave 4). Their groans fade out quickly with distance. They have to be right next to you to hit you and can't claw through walls. Zombies claw through anything built in their way, and if you're up on a tower they go for the piece holding it up. Clearing a wave gives you a 15-second break, 50 shield, 30 health, 3 bandages and 2 small shields. In a room the host picks the mode and runs the zombies for everyone; zombies get tougher and waves bigger with more players, and anyone who goes down is back in 3 seconds.

## Trees, rocks and cars
Trees, pine trees, rocks and old cars are scattered around the map. They're solid, so you, the bot and zombies have to go around them. Materials are infinite by default. Turn off **Infinite materials** in Settings and every build costs 10 of its material: pickaxe trees for wood, rocks for brick and cars for metal (your stock shows on the right). You start each life with 30 wood. Anything you harvest grows back in its spot after 35–80 seconds. In a room everyone sees the same map, and the host decides when things grow back.

## Inventory, weapons and loot
You carry a pickaxe plus 5 slots (keys 2–6) that hold any weapon or item. Press **Tab** (bindable) to open the inventory. Everything is drag and drop:
- Drag a slot onto another slot to move it there, or swap the two.
- Drag a slot onto the drop area, or anywhere outside the panel, to drop it on the ground. Ammo works the same way.
- Drag loot from the *On the ground nearby* list straight onto a slot. Whatever was in that slot is dropped in its place.
- Click a slot to select it; click it again to equip it.

On phones, the bag button opens the inventory. You can also hold a weapon in the hotbar for a moment and drag it onto another slot (empty ones show up while you drag).

Weapons: Assault Rifle, Pump Shotgun, Submachine Gun, Machine Gun, Minigun (spins up before it fires), Rocket Launcher (explosive, wrecks builds) and Grenades (bounce, then explode after 2 s). Guns use light, medium, shells or rocket ammo; reloads come out of your reserves.

In zombie horde, demons sometimes drop loot when they die: about half drop nothing, others drop a random kind of ammo (not necessarily what you use), now and then a gun, heals or grenades, and Behemoths usually drop a gun. Loot falls and lands on the ground or on builds, and you pick it up by walking over it. In build fights ammo reserves are endless.

## Heals
Slot 4 is bandages (15 health each, up to 75, 3.5 s) and slot 5 is small shield potions (25 shield each, up to 50, 2 s). Click to use one, hold fire to keep using them. You start with 5 bandages and 3 small shields.

## Teams
In the multiplayer menu, pick a team. Teammates can't damage each other, and have a marker over their heads and a coloured dot on the minimap. In zombie horde everyone is on the same side.

## Opponent
A bot that strafes, shoots, walls up when hit, ramp rushes when you take height, and boxes up to peek through window edits. On **Adaptive** it measures your accuracy, build speed, edits and damage over the last 40 seconds and matches it, nudging harder when you win rounds and easier when you lose. Fixed Easy to Expert levels are in the menu. In a multiplayer room the host's game runs the bot for everyone: it goes after the nearest player, its builds and edits show up for everyone, anyone can eliminate it, and it comes back 3 seconds later. The host picks its level in the menu (Off removes it).

You can't build through walls: a spot behind a wall (or a window) is blocked, but you can build through a door.

## Multiplayer
Open the menu, type a name, and press **Host a room**. Share the 5-letter code; friends press **Join** with it. Up to 8 players.

Multiplayer is peer-to-peer (WebRTC via [PeerJS](https://peerjs.com)), no server to run. The host is the source of truth for builds: it checks every placement and edit, decides what collapses when a support breaks (so everyone sees exactly the same result) and corrects conflicts, including two players editing the same piece at once. Players can shoot each other; each player applies the damage they take, eliminations show in the feed, and you respawn after 3 seconds. Build damage, health, materials, edits and half stairs stay in sync, and late joiners get the whole map. The room closes when the host leaves.

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

Every bind can be changed in the menu.

## Building rules
- **Preview.** Green outline: it will build. Red outline plus the reason underneath: *Already built*, *Nothing to attach to*, *Out of reach*, *Wall in the way*, *Player in the way*, *Build height limit* or *Edge of the map*. A grey outline means the spot is taken. Every placement (yours, the bot's, a joining player's) goes through the same validator, and in a room the host checks it again.
- **Materials.** Wood 150/140, brick 300/280, metal 500/460 max health (wall / other pieces). Builds start weaker and gain health while they finish. Start health, build-up times, damage resistance, crack thresholds and debris are all in `MATERIALS` and `BUILD_CFG` near the top of the script.
- **Construction.** A piece appears as a blue blueprint with a material-coloured frame, then fills in section by section: wood plank by plank, brick course by course, metal in a few big panels. Walls rise from the bottom, floors grow out from the side they're attached to, stairs build from the low end up and roofs from the base.
- **Support.** Pieces hold each other up only through a shared edge or face; floors that only touch at a corner don't count. Anything resting on the ground is *anchored*; anything with a chain of connections down to the ground is *supported*. Aim at a build with the pickaxe or in build mode to see its health, whether it's anchored, and how many pieces it's holding up. When a piece is destroyed, only the pieces it touched are re-checked: a group that still has another way down stays up, and a group with none left collapses.
- **Damage and collapse.** Builds crack in three stages as they take damage (splits and splinters in wood, cracked and chipped brick, dents and scratches in metal) and shudder when hit. A destroyed piece bursts into its own material: planks, bricks, or metal panels and sparks. A piece that loses its support does something different: it darkens, shudders, tips away from the break, falls and crumbles into dust and debris, with pieces farther from the break going a moment later. It stops blocking you the instant it loses support.
- **Edits.** Edits are named live (Window, Door, Wide window, Arch, Half wall, Ridge, Ramp roof…). Editing never changes what a piece holds up. Reset puts it back exactly as placed, rotated stairs included. In Settings, **Who can edit builds** lets you choose between only the builder, the builder and teammates, or anyone. In a room the host's choice counts and the host re-checks every edit. When a player leaves, their builds become editable by everyone.

### Where this approximates Fortnite
Exact Fortnite numbers aren't public, so these are best guesses, all adjustable in `BUILD_CFG`:
- There's no limit on how far a structure can reach from the ground, as long as there's an unbroken chain to it (`maxSupportDepth: 0`). Set a number to cap overhangs.
- A rotated stair keeps the attachment it was placed with, so an edit can never drop anything.
- Start health, construction time and crack thresholds are estimates.

### Tests
The building system is covered by 35 scripted checks: placement, support, editing, damage, multiplayer and performance. Each one was run in a real browser, with two real clients for the multiplayer cases. They include a 540-piece, 5-level structure brought down wall by wall with the connection graph checked after every step, and a check that nothing is left behind afterwards.
- Controller supported (standard gamepad mapping); see the in-game menu for the layout.

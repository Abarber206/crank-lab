# Crank Lab

A browser build-fight practice range: Chapter 1-style movement, turbo build, wall / floor / ramp / cone edits, and fully custom keybinds (mouse side buttons and scroll wheel included).

**Play:** https://abarber206.github.io/crank-lab/

## Locker
Pick an outfit in the menu: Rook, Nova, Ember, Sprig, Volt, Glacier or Whisk. Each has its own hair or headwear, top and back bling. Everyone in a room sees your outfit, and the bot wears a different one.

## Zombie horde
Pick **Zombie horde** next to Play. You get 20 seconds to build a fort, then waves of zombies walk in from every side. Husks shamble, runners sprint (from wave 2), and brutes (from wave 4) are huge, tanky and smash builds fast. Zombies claw through anything built in their way, and if you're up on a tower they go for the piece holding it up. Clearing a wave gives you a 15-second break, 50 shield, 30 health, 3 bandages and 2 small shields. In a room the host picks the mode and runs the zombies for everyone; zombies get tougher and waves bigger with more players, and anyone who goes down is back in 3 seconds.

## Heals
Slot 4 is bandages (15 health each, up to 75, 3.5 s) and slot 5 is small shield potions (25 shield each, up to 50, 2 s). Click to use one, hold fire to keep using them. You start with 5 bandages and 3 small shields.

## Opponent
A bot that strafes, shoots, walls up when hit, ramp rushes when you take height, and boxes up to peek through window edits. On **Adaptive** it measures your accuracy, build speed, edits and damage over the last 40 seconds and matches it, nudging harder when you win rounds and easier when you lose. Fixed Easy to Expert levels are in the menu. In a multiplayer room the host's game runs the bot for everyone: it goes after the nearest player, its builds and edits show up for everyone, anyone can eliminate it, and it comes back 3 seconds later. The host picks its level in the menu (Off removes it).

You can't build through walls: a spot behind a wall (or a window) is blocked, but you can build through a door.

## Multiplayer
Open the menu, type a name, and press **Host a room**. Share the 5-letter code; friends press **Join** with it. Up to 8 players.

Multiplayer is peer-to-peer (WebRTC via [PeerJS](https://peerjs.com)), no server to run. The host is the source of truth for builds: it checks every placement and edit and corrects conflicts. Players can shoot each other; each player applies the damage they take, eliminations show in the feed, and you respawn after 3 seconds. Build damage, health, materials, edits and half stairs stay in sync, and late joiners get the whole map. The room closes when the host leaves.

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
- Every placement goes through one validator, and the red preview shows the reason it fails: *Already built*, *Nothing to attach to*, *Out of reach*, *Player in the way*, *Build height limit* or *Edge of the map*.
- Materials: wood 150/140, brick 300/280, metal 500/460 max health (wall / other pieces). Builds start weaker and gain health while they finish. Start health and build-up times are estimates and can be tuned in `MATERIALS`.
- Edits are named live (Window, Door, Wide window, Arch, Half wall, Ridge, Ramp roof…). You can only edit your own builds.
- Controller supported (standard gamepad mapping); see the in-game menu for the layout.

# Crank Lab

A browser build-fight practice range: Chapter 1-style movement, turbo build, wall / floor / ramp / cone edits, and fully custom keybinds (mouse side buttons and scroll wheel included).

**Play:** https://abarber206.github.io/crank-lab/

## Opponent
A bot that strafes, shoots, walls up when hit, ramp rushes when you take height, and boxes up to peek through window edits. On **Adaptive** it measures your accuracy, build speed, edits and damage over the last 40 seconds and matches it, nudging harder when you win rounds and easier when you lose. Fixed Easy to Expert levels are in the menu. The bot is off while you're in a multiplayer room.

## Multiplayer
Open the menu, type a name, and press **Host a room**. Share the 5-letter code; friends press **Join** with it. Up to 8 players.

Multiplayer is peer-to-peer (WebRTC via [PeerJS](https://peerjs.com)). The host's game relays movement and every build, edit and break, so the room closes when the host leaves. No server to run.

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

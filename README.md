# Crank Lab

A browser build-fight practice range: Chapter 1-style movement, turbo build, wall / floor / ramp / cone edits, and fully custom keybinds (mouse side buttons and scroll wheel included).

**Play:** https://abarber206.github.io/crank-lab/

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

Every bind can be changed in the menu.

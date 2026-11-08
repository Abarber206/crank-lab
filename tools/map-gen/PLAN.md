# Big map update: plan (full version)

Goal: an island about 1.6 km across (MAP_R 800, up from 392), more realistic mountains, 10 towns joined by roads.

## Already done (this folder)
- `gen.js`: deterministic generator. It uses only integer hashing (Math.imul), + - * /, Math.sqrt and Math.floor, so every browser builds the identical map and multiplayer stays in sync. **Never add Math.sin, Math.cos, Math.pow, Math.hypot or Math.exp to it.**
  - `makeWorldGen({FLAT_R,MAP_R,massifs:4,rng:seeded})` returns `genH(u,v)`, the height at u,v metres from SPAWN, and `MASSIFS`.
  - The landscape: rolling hills; 4 ridged mountain ranges inside the map (95–170 m); an outer ridged range up to about 450 m.
  - `bakeWorld({gen,HS:2,HALF:832,FLAT_R:42,MAP_R:800,rng:seeded,towns:10,townGap:210,LVL:4,townR:31,loops:3,loopMax:520,maxGrade:0.1,roadW:6,blendMax:34,snap})` makes:
    - a 2 m heightfield `H` (833×833), plus `H0` without the roads
    - road distance `RD`
    - ground cover arrays `ROCK`, `SNOW` and `GRASS` (Uint8)
    - `towns` with u, v, h and R
    - `roads`, each with pts `[u,v,y]` every 2 m and skip flags where it overlaps an earlier road
  - How the bake works:
    - Towns are the flattest lowland spots, levelled to a build level.
    - Roads come from an A* search on an 8 m grid along a minimum spanning tree plus 3 loops, plus one road from the build field to the nearest town.
    - They are smoothed (Chaikin) and given a profile limited to a 10% grade, pinned flat in towns and where they cross earlier roads.
    - They are cut and filled into the ground, with blends that get longer where the drop is bigger.
  - `snap` should round the town centres to the CELL grid: `(u,v)=>[Math.round((SPAWN[0]+u)/CELL)*CELL-SPAWN[0], …]`.
  - Bake time is about 0.8 s in V8.
- `preview.js` and `preview2.js` render top-down hillshade PNGs (node).

## To do in index.html
1. **Terrain:**
   - Paste in the generator.
   - Replace `terrainRaw`, `planTowns` and `terrainH`. `terrainH` becomes a bilinear read of H inside ±HALF, and `genH` outside.
   - Add `roadDistAt(x,z)` from RD.
   - Set `MAP_R=800` and replace the uses of `MTN_R` (grass edge, chests, the old ground and the ring decor).
2. **TOWNS** come from `WORLD.towns`. Add 4 names to `TOWN_NAMES`. Use seeds from `seeded(9000+k)`. In `planHouses`, mark cells with `roadDistAt < 7.5` as used.
3. **Terrain rendering:**
   - 128 m chunks (13×13) with 3 levels of detail: 2, 4 and 8 m steps, chosen by camera distance (<170, <480, beyond). Build them lazily and dispose LOD0 when far.
   - Skirts along the chunk edges hide the cracks.
   - Normals from H.
   - The material is MeshLambert with the grass texture plus a rock texture (canvas), mixed through a vertex attribute (rock, snow, dirt) in `onBeforeCompile`. Snow is near-white. Dirt goes on the road shoulders (RD 3.6–6.5 m).
   - Keep the polygonOffset.
   - Outer mountains: 16 tiles out to ±2400 m at 16 m steps, using `genH` directly.
4. **Roads:**
   - One mesh per road with half-width 3.6 m, at y+0.07.
   - Asphalt canvas texture with white edge lines and a dashed yellow centre (repeat every 12 m along v).
   - polygonOffset of −(4+k) per road. Skip overlapped segments.
   - A plain asphalt disc as a plaza at each town centre (uv u fixed at 0.3).
5. **Fog and camera:**
   - Day fog near 250, far 2600; update the dusk code at `scene.fog.near=…`.
   - `camera.far` 3200.
   - Props cull at 400 m.
   - Clouds at 380–520 m high, spread to 1500 m, wrapping at 1600.
6. **Props:**
   - About 520 trees, 520 pines (higher up), 220 rocks (on rocky ground) and 40 cars (25 parked along the roads). They stay off roads (<8 m), rock and snow, and towns.
   - Share the merged geometry by variant (`p.id % 8`) and scale with `g.scale=s`. The grow, dying and revive animations then scale by `p.s*k`. This keeps memory down.
   - Bushes: about 1000, in 16 regional InstancedMeshes with their own bounding spheres.
   - Wild chests: about 35, kept off roads.
7. **Grass** skips where `GRASS[cell]` is low, which means roads, rock and snow.
8. **Maps:**
   - Draw roads on the minimap.
   - A full map overlay (M key, bindable, or tap the minimap) from a pre-rendered hillshade canvas with roads, towns, players and the player arrow.
9. **Tests, README and ship:**
   - t43, t46, t30, t36, t44, t63, t66 and the mp_* tests, run one at a time. Swiftshader is slow, so use waitForFunction.
   - Check the load time.
   - Update the README map and towns sections.
   - Commit and push main, run `mkart.py` (artifact transform), then publish.

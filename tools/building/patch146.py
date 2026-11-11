# patch146: smooth skydiving. From high up the trees and terrain under you were still drawn at full detail (detail was
# chosen by distance across the ground only, so the forest 500 m below counted as "near": ~3M triangles a frame), and
# the far shadow map was redrawn several times a second while you fell. Now detail goes by the real distance from the
# camera (height included), and in the air the far shadows follow the ground under you, redrawn at most about once
# a second.
rep("""const TLOD=[170,480];
function stepTerrain(cx,cz,force){""","""const TLOD=[170,480]; var CAMH=0; // how high the camera is above the ground under it
function stepTerrain(cx,cz,force){ CAMH=Math.max(0,camera.position.y-Math.max(terrainH(cx,cz),waterAt(cx,cz))-3); const h2=CAMH*CAMH;""")
rep("""    const dx=Math.max(c.x0-cx,0,cx-c.x1), dz=Math.max(c.z0-cz,0,cz-c.z1), d=Math.sqrt(dx*dx+dz*dz);
    let want=d<TLOD[0]?0:d<TLOD[1]?1:2;""","""    const dx=Math.max(c.x0-cx,0,cx-c.x1), dz=Math.max(c.z0-cz,0,cz-c.z1), d=Math.sqrt(dx*dx+dz*dz+h2);
    let want=d<TLOD[0]?0:d<TLOD[1]?1:2;""")
rep("""function stepForest(dt){ if(!FOREST.near) return; FOREST.t-=dt; const cx=camera.position.x, cz=camera.position.z;
  const moved=Math.hypot(cx-FOREST.lastX,cz-FOREST.lastZ);""","""function stepForest(dt){ if(!FOREST.near) return; FOREST.t-=dt; const cx=camera.position.x, cz=camera.position.z, ch=CAMH*CAMH;
  const moved=Math.max(Math.hypot(cx-FOREST.lastX,cz-FOREST.lastZ),Math.abs(CAMH-(FOREST.lastH||0))); if(moved>6&&FOREST.t<=0) FOREST.lastH=CAMH;""")
rep("""for(const p of FOREST.trees){ if(p.gone||!p.alive||p.g.parent) continue; const dx=p.x-cx, dz=p.z-cz, d2=dx*dx+dz*dz; if(d2>F2) continue;""",
    """for(const p of FOREST.trees){ if(p.gone||!p.alive||p.g.parent) continue; const dx=p.x-cx, dz=p.z-cz, d2=dx*dx+dz*dz+ch; if(d2>F2) continue;""")
# the far shadows in the air: centred on the ground under you, and not redrawn every few metres you fall
rep("""function placeFarShadow(pos){ if(!sunFar.castShadow) return; const now=performance.now(), st=8, a=Math.round(pos.dot(_lX)/st)*st, b=Math.round(pos.dot(_lY)/st)*st; // it follows you in 8 m steps (40 of its texels)
  if(a===FARS.a&&b===FARS.b&&now-FARS.t<(FARS.dir.equals(SUN_DIR)?420:300)) return;""","""const _fsG=new THREE.Vector3();
function placeFarShadow(pos){ if(!sunFar.castShadow) return; const air=P.sky&&pos===P.pos; if(air) pos=_fsG.set(P.pos.x,terrainH(P.pos.x,P.pos.z),P.pos.z);
  const now=performance.now(), st=air?24:8, a=Math.round(pos.dot(_lX)/st)*st, b=Math.round(pos.dot(_lY)/st)*st; // it follows you in 8 m steps (40 of its texels)
  if(air&&now-FARS.t<1100) return;
  if(a===FARS.a&&b===FARS.b&&now-FARS.t<(FARS.dir.equals(SUN_DIR)?420:300)) return;""")
# the cloud bank you fall out of: sixteen screen-sized puffs, each blurred by a filter as it animated (costly on a
# phone); their own soft gradient is enough
rep("rgba(240,246,252,0) 100%);filter:blur(6px);will-change:transform,opacity}","rgba(240,246,252,0) 100%);will-change:transform,opacity}")

# ---------- 125. a reason to go to each town's landmark: a strongbox stands at its foot under a shaft of gold light you can
# see from far off. It always holds a rare-or-better gun with twice the ammunition, a second gun, and shield potions ----------
rep("  // a few in the wild, under trees and on hilltops\n  const r=seeded(99173), RC=MAP_R-30; let made=0;",
    """  // one strongbox at the foot of each town's landmark, on the side facing the town
  buildLandmarks();
  for(const t of TOWNS){ const L=t.poi; if(!L) continue; const a0=Math.atan2(t.x-L.x,t.z-L.z); let x=0, z=0, dx=0, dz=0, ok=false;
    const clear=(x,z,y)=>{ for(const s of STATICS){ if(!s.solid||Math.abs(s.x-x)>14||Math.abs(s.z-z)>14) continue; for(const b of s.solid.boxes){ if(b[4]<y+0.2||b[1]>y+1.5) continue; if(Math.hypot(Math.max(b[0]-x,0,x-b[3]),Math.max(b[2]-z,0,z-b[5]))<1.3) return false; } } return !propsNear(x,z,[],1).some(q=>!q.gone&&Math.hypot(q.x-x,q.z-z)<1.8); };
    for(const R of [6.6,7.3,5.8,8.2]){ for(const da of [0,0.6,-0.6,1.2,-1.2,1.9,-1.9,3.14]){ dx=Math.sin(a0+da); dz=Math.cos(a0+da); x=L.x+dx*R; z=L.z+dz*R; if(clear(x,z,terrainH(x,z))){ ok=true; break; } } if(ok) break; }
    const c=addChest(x,terrainH(x,z),z,Math.atan2(-dx,-dz)+Math.PI);
    c.big=true; c.g.scale.setScalar(1.3); const bm=new THREE.Mesh(new THREE.CylinderGeometry(0.3,1.1,26,14,1,true),new THREE.MeshBasicMaterial({color:0xffd060,transparent:true,opacity:0.3,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,fog:false})); bm.position.set(x,c.y+13.4,z); bm.renderOrder=3; scene.add(bm); c.beam=bm; }
  // a few in the wild, under trees and on hilltops
  const r=seeded(99173), RC=MAP_R-30; let made=0;""")
rep("function rollChestLoot(){","""function lootWeaponMin(luck,minIdx){ for(let q=0;q<40;q++){ const id=lootWeapon(luck); if(RARITIES.indexOf(WEAPONS[id].rarity)>=minIdx) return id; } return lootWeapon(luck); }
function rollBigLoot(){ const a=lootWeaponMin(2.4,2), b=lootWeapon(1.5), am=ammoFor(a); return [[a,WEAPONS[a].mag],[am[0],am[1]*2],[b,WEAPONS[b].mag],ammoFor(b),['mini',3]]; }
function stepBigChests(){ const t=performance.now()/1000; for(const c of chests){ if(!c.beam) continue; const on=!c.open&&c.g.visible; c.beam.visible=on; if(on){ c.beam.material.opacity=0.27+0.08*Math.sin(t*2.1); c.beam.rotation.y=t*0.3; } } }
function rollChestLoot(){""")
rep("  rollChestLoot().forEach(([item,n],q)=>{ const sp=(q-1)*0.9;","  (c.big?rollBigLoot():rollChestLoot()).forEach(([item,n],q)=>{ const sp=(q-(c.big?2:1))*0.8;")
rep("function closeChest(c){ c.open=false; c.prog=0; c.respawnT=0; c.goneT=0; c.poofed=false; c.g.scale.setScalar(1); c.lidA=0; }","function closeChest(c){ c.open=false; c.prog=0; c.respawnT=0; c.goneT=0; c.poofed=false; c.g.scale.setScalar(c.big?1.3:1); c.lidA=0; }")
rep("c.g.scale.setScalar(1-0.85*f);","c.g.scale.setScalar((c.big?1.3:1)*(1-0.85*f));")
rep("stepPlayers(dt); stepTracers(dt); stepBullets(dt);","stepPlayers(dt); stepTracers(dt); stepBullets(dt); stepBigChests();")

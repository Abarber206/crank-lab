# patch157: zombies that end up far from everyone come back. A zombie more than 110 m from the nearest player for
# three seconds (lost behind a hill, stuck across a river, left behind by a car) is moved to a fresh spot 42-62 m from
# that player, somewhere dry and out of their sight where it can, and walks in again. New zombies also spawn around a
# player (not around the middle of a spread-out squad, which could be far from all of them).
rep("""function hordeSpawnPoint(){
  const tg=hordeTargets(); const c=new THREE.Vector3(); if(tg.length){ tg.forEach(t=>c.add(t.pos)); c.multiplyScalar(1/tg.length); } else c.set(SPAWN[0],0,SPAWN[2]);
  const a=Math.random()*Math.PI*2, r=46+Math.random()*16; let x=c.x+Math.cos(a)*r, z=c.z+Math.sin(a)*r; const d=Math.hypot(x-SPAWN[0],z-SPAWN[2]); if(d>MAP_R-8){ x=SPAWN[0]+(x-SPAWN[0])*(MAP_R-8)/d; z=SPAWN[2]+(z-SPAWN[2])*(MAP_R-8)/d; } return [x,z];
}""","""const _hsF=new THREE.Vector3();
function hordeSpawnPoint(near){
  const tg=hordeTargets(), t=near||(tg.length?tg[Math.floor(Math.random()*tg.length)]:null), cx=t?t.pos.x:SPAWN[0], cz=t?t.pos.z:SPAWN[2];
  camera.getWorldDirection(_hsF); let best=null, bs=-1e9;
  for(let k=0;k<14;k++){ const a=Math.random()*Math.PI*2, r=42+Math.random()*20; let x=cx+Math.cos(a)*r, z=cz+Math.sin(a)*r; const d=Math.hypot(x-SPAWN[0],z-SPAWN[2]); if(d>MAP_R-8){ x=SPAWN[0]+(x-SPAWN[0])*(MAP_R-8)/d; z=SPAWN[2]+(z-SPAWN[2])*(MAP_R-8)/d; }
    let s=Math.random(); if(waterAt(x,z)>-999) s-=10;                                                   // not in the water
    const vx=x-camera.position.x, vz=z-camera.position.z, vl=Math.hypot(vx,vz)||1; if((vx*_hsF.x+vz*_hsF.z)/vl>0.35) s-=2; // not where you're looking
    for(const o of tg) if(Math.hypot(o.pos.x-x,o.pos.z-z)<35) s-=5;                                     // not on top of anyone else
    if(s>bs){ bs=s; best=[x,z]; } }
  return best;
}""")
rep("""    zombieThink(z,dt,tg);""","""    zombieThink(z,dt,tg);
    { let nd=Infinity, nt=null; for(const o of tg){ const d=Math.hypot(o.pos.x-z.pos.x,o.pos.z-z.pos.z); if(d<nd){ nd=d; nt=o; } } // left far behind: come back from nearer
      z.farT=nt&&nd>110?(z.farT||0)+dt:0;
      if(z.farT>3){ const [x,zz]=hordeSpawnPoint(nt); z.pos.set(x,terrainUnder(x,zz),zz); z.vel.set(0,0,0); z.farT=0; z.stuckT=0; z.goal=null; z.target=null; z.tT=0; } }""")

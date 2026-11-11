# patch138: water reflections that work, for less.
#  - the mirror is set at the level of the water you're looking at (a short march along the view), not of whatever water
#    is nearest on a coarse 32 m grid, so a river shows its reflection even where the sea or another stretch of river
#    is closer; water a little off that level still mirrors
#  - the mirror image is redrawn every other frame (the water keeps showing the last one, which still lines up), and the
#    far trees (hundreds of metres off, deep in the haze) are left out of it: well under half the cost
#  - turned off to keep the game smooth, reflections come back once there's room again
rep("""  const cp=camera.position, LN=WATER.LN, i=Math.max(0,Math.min(LN-1,Math.floor((cp.x-SPAWN[0]+WHALF)/WATER.LC))), j=Math.max(0,Math.min(LN-1,Math.floor((cp.z-SPAWN[2]+WHALF)/WATER.LC))), lvl=WATER.lv[j*LN+i], off=WATER.ld[j*LN+i], hgt=cp.y-lvl;""",
"""  const cp=camera.position, LN=WATER.LN, i=Math.max(0,Math.min(LN-1,Math.floor((cp.x-SPAWN[0]+WHALF)/WATER.LC))), j=Math.max(0,Math.min(LN-1,Math.floor((cp.z-SPAWN[2]+WHALF)/WATER.LC)));
  let lvl=WATER.lv[j*LN+i], off=WATER.ld[j*LN+i];
  { camera.getWorldDirection(_rfD); const hl=Math.hypot(_rfD.x,_rfD.z); if(hl>0.05){ const dx=_rfD.x/hl, dz=_rfD.z/hl; // the water ahead of you, if there is some
      for(let s=1;s<=140;s+=s<20?1.5:4){ const x=cp.x+dx*s, z=cp.z+dz*s, w=waterAt(x,z); if(w>-999&&w<cp.y-0.1){ lvl=w; off=Math.min(off,s*0.5); break; } } } }
  const hgt=cp.y-lvl;
  if(Math.abs(lvl-REFL.lvl)>0.02) REFL.skip=0; REFL.lvl=lvl; if(REFL.skip>0&&REFL.ok){ REFL.skip--; u.reflM.value.copy(REFL.m); u.reflK.value=REFL.K; u.reflY.value=lvl; return; } // the last mirror image still serves
  REFL.ok=false;""")
rep("""  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh]) if(o&&o.visible){ o.visible=false; hid.push(o); }""",
"""  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh]) if(o&&o.visible){ o.visible=false; hid.push(o); }
  if(FOREST.far) for(const kind in FOREST.far) for(const o of FOREST.far[kind]) if(o.visible){ o.visible=false; hid.push(o); } // the far trees: too far off to matter in a rippled mirror""")
rep("""  u.reflM.value.copy(REFL.m); u.reflK.value=K; u.reflY.value=lvl;
}""","""  u.reflM.value.copy(REFL.m); u.reflK.value=K; u.reflY.value=lvl; REFL.K=K; REFL.ok=true; REFL.skip=1;
}
const _rfD=new THREE.Vector3();""")
rep("""const REFL={rt:null,""","""const REFL={lvl:-1e4,skip:0,ok:false,K:0,rt:null,""")
rep("""mir=mix(mir,texture2D(reflT,clamp(ruv,0.003,0.997)).rgb,reflK*(1.0-smoothstep(0.35,1.4,abs(vW.y-reflY)))); }""",
    """mir=mix(mir,texture2D(reflT,clamp(ruv,0.003,0.997)).rgb,reflK*(1.0-smoothstep(0.6,2.2,abs(vW.y-reflY)))); }""")
# reflections shed to keep it smooth come back when there's headroom (at most three times a game)
rep("""  if(PERF.reflect&&settings.reflect!==false){ PERF.reflect=false; say('Water reflections off to keep the game smooth'); return true; } PERF.reflect=false;""",
    """  if(PERF.reflect&&settings.reflect!==false){ PERF.reflect=false; PERF.shedAt=performance.now(); say('Water reflections off to keep the game smooth'); return true; } PERF.reflect=false;""")
rep("""  if(settings.autoRes&&avg>30&&dynRes.cur<=dynRes.min+1e-3){""",
    """  if(!PERF.reflect&&settings.reflect!==false&&PERF.shedAt&&(PERF.back||0)<3&&now-PERF.shedAt>30000&&avg<14&&dynRes.cur>=Math.min(dynRes.max,dynRes.ceil)-1e-3){ PERF.reflect=true; PERF.back=(PERF.back||0)+1; PERF.shedAt=0; }
  if(settings.autoRes&&avg>30&&dynRes.cur<=dynRes.min+1e-3){""")

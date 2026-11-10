# ---------- 123. a frame-rate guard: when the resolution is already as low as it goes and frames are still slow, the costly
# extras are shed one at a time for the rest of the session (water reflections, then ambient occlusion, then far shadows);
# your saved settings are left alone ----------
rep("function stepDynRes(raw,now){","""const PERF={reflect:true,ao:true,far:true,slow:0};
function perfShed(){ const say=m=>{ try{ toast(m); }catch(e){} };
  if(PERF.reflect&&settings.reflect!==false){ PERF.reflect=false; say('Water reflections off to keep the game smooth'); return true; } PERF.reflect=false;
  if(PERF.ao&&settings.ao!==false&&AO.ok){ PERF.ao=false; say('Soft shading off to keep the game smooth'); return true; } PERF.ao=false;
  if(PERF.far&&sunFar.castShadow){ PERF.far=false; sunFar.castShadow=false; say('Far shadows off to keep the game smooth'); return true; } PERF.far=false; return false; }
function stepDynRes(raw,now){""")
rep("  let next=dynRes.cur;\n  if(!settings.autoRes){ next=dynRes.max; }","  if(settings.autoRes&&avg>30&&dynRes.cur<=dynRes.min+1e-3){ if(++PERF.slow>=2){ PERF.slow=0; perfShed(); } } else if(avg<26) PERF.slow=0; // still slow at the lowest resolution for four seconds: drop an extra\n  let next=dynRes.cur;\n  if(!settings.autoRes){ next=dynRes.max; }")
rep("function renderMain(){ if(!AO.ok||settings.ao===false||!scene.visible){","function renderMain(){ if(!AO.ok||settings.ao===false||!PERF.ao||!scene.visible){")
rep("  if(settings.reflect===false||!WATER.lv||!scene.visible) return;","  if(settings.reflect===false||!PERF.reflect||!WATER.lv||!scene.visible) return;")

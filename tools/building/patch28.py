# ---------- 28. sound pass: footsteps that match the ground, a rolling hill echo on gunfire, wind, birds and crickets ----------
rep("    case 'step': case 'step_grass': noise(650*r(),0.07,0.06,0.6,0,'lowpass'); break;",
"""    case 'step': case 'step_grass': noise(2600*r(),0.05,0.035,0.8,0,'highpass'); noise(520*r(),0.06,0.05,0.7,0,'lowpass'); break; // a soft swish
    case 'step_dirt': noise(900*r(),0.07,0.07,0.7,0,'lowpass'); noise(2400*r(),0.03,0.025,1,0.01); break;
    case 'step_road': knock(260*r(),0.04,0.06,4); noise(2200*r(),0.035,0.05,1.2); break;
    case 'step_concrete': knock(330*r(),0.035,0.07,5); noise(3000*r(),0.025,0.04,1.5,0,'highpass'); break;
    case 'step_rock': knock(430*r(),0.05,0.06,6); noise(1800*r(),0.03,0.05,2); break;
    case 'step_snow': for(let q=0;q<4;q++) noise(1300+Math.random()*900,0.03,0.035,1,q*0.018); break; // crunch""")
rep("""function stepSound(E){
  if(E.pos.y<0.05) return 'step_grass';
  if(E.groundSlab) return 'step_'+(E.groundSlab.mat||'wood');
  const i=Math.floor(E.pos.x/CELL), j=Math.floor(E.pos.z/CELL), l=Math.round(E.pos.y/LVL), f=pieces.get(`f${i}_${j}_${l}`);
  return 'step_'+(f?f.mat:'wood');
}""","""function stepSound(E){
  if(E.groundSlab) return 'step_'+(E.groundSlab.mat||'wood');
  const x=E.pos.x, z=E.pos.z, y=E.pos.y;
  if(y-terrainH(x,z)>0.12){ // on a build or in a house
    const i=Math.floor(x/CELL), j=Math.floor(z/CELL), l=Math.round(y/LVL), f=pieces.get(`f${i}_${j}_${l}`);
    return f&&!f.skin?'step_'+f.mat:'step_wood'; }
  // on the ground: sidewalk, road, snow, rock, bare dirt or grass
  if(townAt(x,z,0)) for(const [a,b] of SIDEWALKS){ const dx=b[0]-a[0], dz=b[1]-a[1], L2=dx*dx+dz*dz||1, t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/L2)); if(Math.hypot(a[0]+dx*t-x,a[1]+dz*t-z)<WALK_W/2+0.1) return 'step_concrete'; }
  if(roadDistAt(x,z)<ROAD_HW-0.2) return 'step_road';
  const c=worldCell(x,z); if(c>=0){ if(WORLD.SNOW[c]>110) return 'step_snow'; if(WORLD.ROCK[c]>140) return 'step_rock'; if(WORLD.GRASS[c]<60) return 'step_dirt'; }
  return 'step_grass';
}""")
# gunfire and blasts roll back off the hills a moment later
rep("    case 'shield': tone('sine',660,990,0.25,0.08); tone('sine',990,1320,0.3,0.06,0.12); noise(5000,0.2,0.04,1,0.05,'highpass'); break;\n  }\n}",
"""    case 'shield': tone('sine',660,990,0.25,0.08); tone('sine',990,1320,0.3,0.06,0.12); noise(5000,0.2,0.04,1,0.05,'highpass'); break;
  }
  if(HILL_ECHO[k]){ const e=HILL_ECHO[k]; noise(650,0.55,0.05*e,0.7,0.32+Math.random()*0.08,'lowpass',260); noise(480,0.8,0.03*e,0.7,0.78+Math.random()*0.15,'lowpass',200); }
}
const HILL_ECHO={shot:1,pump:1.2,shot_mg:1,shot_smg:0.6,shot_mini:0.7,shot_pistol:0.6,shot_rev:1.1,shot_heavy:1.3,shot_sniper:1.6,shot_heavyar:1.1,shot_tac:1.1,shot_dbl:1.3,boom:2,rocket:1,gl:0.8};
/* ambience: a quiet wind that grows the higher you are, birds now and then in the day, crickets at dusk (horde) */
let amb=null, ambBirdT=3, ambCricketT=1;
function stepAmbience(dt){ if(!AC) return;
  if(!amb){ const s=AC.createBufferSource(); s.buffer=noiseBuf; s.loop=true; const f=AC.createBiquadFilter(); f.type='lowpass'; f.frequency.value=400; f.Q.value=0.6; const g=AC.createGain(); g.gain.value=0; s.connect(f).connect(g).connect(master); s.start(); amb={s,f,g,t:0}; }
  amb.t+=dt; const on=playing&&!document.hidden, hi=Math.max(0,Math.min(1,(P.pos.y-terrainH(P.pos.x,P.pos.z)+P.pos.y*0.15)/60));
  const gust=0.5+0.5*Math.sin(amb.t*0.37)*Math.sin(amb.t*0.11+1.3);
  amb.g.gain.setTargetAtTime(on?0.012+0.03*hi+0.012*gust:0,AC.currentTime,0.4); amb.f.frequency.setTargetAtTime(300+500*gust+600*hi,AC.currentTime,0.6);
  if(!on) return;
  if(!horde.on){ ambBirdT-=dt; if(ambBirdT<=0){ ambBirdT=5+Math.random()*10; const a=Math.random()*6.28, p=P.pos.clone().add(new THREE.Vector3(Math.cos(a)*25,6,Math.sin(a)*25)); if(!townAt(P.pos.x,P.pos.z,0)||Math.random()<0.5) sfxAt('bird',p); } }
  else { ambCricketT-=dt; if(ambCricketT<=0){ ambCricketT=1.4+Math.random()*1.8; const a=Math.random()*6.28; sfxAt('cricket',P.pos.clone().add(new THREE.Vector3(Math.cos(a)*14,0,Math.sin(a)*14))); } } }""")
rep("    case 'groan': zombieGroan(0.34); break;","""    case 'groan': zombieGroan(0.34); break;
    case 'bird': { const n=2+Math.floor(Math.random()*3), b=2300+Math.random()*900; for(let q=0;q<n;q++) tone('sine',b*r(),b*1.25*r(),0.07,0.02,q*0.11); break; }
    case 'cricket': for(let q=0;q<6;q++) tone('sine',4500,4400,0.02,0.008,q*0.045); break;""")
rep("  stepClouds(dt); stepDoors(dt); stepPick(dt);","  stepClouds(dt); stepDoors(dt); stepAmbience(dt); stepPick(dt);")

# patch189: sound upgrades
#  - each rarity of a gun sounds different: a common one is thinner and rattlier, an epic one (muzzle brake) louder and
#    harsher with more slap off the surroundings, a legendary one (compensator) deeper with a longer, heavier tail
#  - far gunfire and explosions arrive late, at the speed of sound (you see the flash, then hear it)
#  - bullets that pass close to you crack and whiz past your head
#  - the lagoon waterfall roars (positioned at the falls), and the sea booms against the cliffs when you're near the edge
#  - the ambience ducks under your own gunfire and nearby explosions, so the fight sits on top of the mix
rep("""const gunTakes={};""","""const gunTakes={};
const GUN_RAR={common:{boom:0.85,sub:0.75,f1:1.18,mech:1.4,rate:1.04},uncommon:{},rare:{boom:1.05,sub:1.1,rate:0.99},
  epic:{blast:1.12,crack:1.12,boom:1.1,sub:1.15,blastT:1.1,slap:1.2,drive:0.2,rate:0.97},legendary:{boom:1.22,sub:1.35,subF:0.9,f1:0.85,boomT:1.18,blastT:1.15,slap:1.28,len:1.15,drive:0.3,rate:0.94}};
function gunSndKey(W){ const base=(W&&W.snd)||'shot'; if(!W||!GUN_SND[base]||!GUN_RAR[W.rarity]) return base; const vk=base+'|'+W.rarity;
  if(!GUN_SND[vk]){ const o=Object.assign({},GUN_SND[base]), m=GUN_RAR[W.rarity]; for(const f of ['boom','sub','f1','blast','crack','blastT','boomT','slap','len','subF']) if(m[f]) o[f]*=m[f];
    if(m.drive) o.drive+=m.drive; if(m.mech) o.mech=o.mech.map(([t,v,b])=>[t,v*m.mech,b]).concat(o.mech.length?[[o.mech[0][0]+0.012,0.12]]:[]); o.rate=m.rate||1; GUN_SND[vk]=o; }
  return vk; }""")
rep("""s.playbackRate.value=0.96+Math.random()*0.08; g.gain.value=o.vol;""","""s.playbackRate.value=(o.rate||1)*(0.96+Math.random()*0.08); g.gain.value=o.vol;""")
rep("""})[k]||0""","""})[k.split('|')[0]]||0""")
rep("""  sfx(W.snd||'shot'); animEvent(localHero,'fi""","""  sfx(gunSndKey(W)); animEvent(localHero,'fi""")
rep("""muzzleFlash(b.h); sfxAt(W.snd||'shot',b.pos);""","""muzzleFlash(b.h); sfxAt(gunSndKey(W),b.pos);""")
rep("""muzzleFlash(pl.h); sfxAt((WEAPONS[m.w]&&WEAPONS[m.w].snd)||'shot',pl.pos);""","""muzzleFlash(pl.h); sfxAt(WEAPONS[m.w]?gunSndKey(WEAPONS[m.w]):'shot',pl.pos);""")
# the speed of sound
rep("""function sfxAt(k,pos){ const L=typeof camera!=='undefined'?camera.position:P.pos, d=pos.distanceTo(L), far=SFX_FAR.test(k), R=far?320:110; if(d>R) return;""",
"""function sfxAt(k,pos){ const L=typeof camera!=='undefined'?camera.position:P.pos, d=pos.distanceTo(L), far=SFX_FAR.test(k), R=far?320:110; if(d>R) return;
  if(far&&d>45&&!sfxAt.late){ const p=pos.clone(); setTimeout(()=>{ sfxAt.late=true; try{ sfxAt(k,p); }finally{ sfxAt.late=false; } },d/343*1000); return; } // sound is slow: far shots arrive after their flash""")
# ducking: the ambience goes through its own bus
rep("""function sfx(k){
  if(!AC) return;""","""function sfx(k){
  if(!AC) return;
  if(AUDIO.amb&&(GUN_SND[k]||k==='boom'||k==='rocket')&&sfxGain>0.45){ const t=AC.currentTime, g=AUDIO.amb.gain, dd=k==='boom'?0.75:0.45; g.cancelScheduledValues(t); g.setValueAtTime(Math.min(1,g.value),t); g.linearRampToValueAtTime(1-dd,t+0.02); g.setTargetAtTime(1,t+0.12,k==='boom'?0.6:0.3); }""")
rep("""function stepAmbience(dt){ if(!AC) return;""","""function stepAmbience(dt){ if(!AC) return; if(!AUDIO.amb){ AUDIO.amb=AC.createGain(); AUDIO.amb.connect(master); }
  const m0=master; master=AUDIO.amb; try{ stepAmbience0(dt); stepAmbience2(dt); } finally{ master=m0; } }
// the waterfall's roar and the sea at the foot of the cliffs
function stepAmbience2(dt){ const on=playing&&!document.hidden, c=camera.position;
  if(!amb.fall&&typeof OCEAN!=='undefined'&&OCEAN.mists){ amb.fall=loopSound(out=>{ const mk=(type,f,q,v,rate)=>{ const s=AC.createBufferSource(); s.buffer=noiseBuf; s.loop=true; s.playbackRate.value=rate; const fl=AC.createBiquadFilter(); fl.type=type; fl.frequency.value=f; fl.Q.value=q; const g=AC.createGain(); g.gain.value=v; s.connect(fl).connect(g).connect(out); s.start(0,Math.random()*0.4); return s; };
      return [mk('lowpass',260,0.6,1.0,0.6),mk('bandpass',900,0.5,0.45,0.8),mk('highpass',3500,0.4,0.12,1.1)]; }); amb.fallT=0; amb.fallP=new THREE.Vector3(); amb.fallD=1e9; }
  if(amb.fall){ amb.fallT-=dt; if(amb.fallT<=0){ amb.fallT=0.25; let bd=1e9; for(const s of OCEAN.mists){ const d=s.position.distanceTo(c); if(d<bd){ bd=d; amb.fallP.copy(s.position); } } amb.fallD=bd; }
    const k=on?Math.pow(Math.max(0,1-amb.fallD/420),2):0; amb.fall.set(0.55*k,amb.fallP); }
  if(!amb.cliff){ amb.cliff=loopSound(out=>{ const s=AC.createBufferSource(); s.buffer=noiseBuf; s.loop=true; s.playbackRate.value=0.5; const f=AC.createBiquadFilter(); f.type='lowpass'; f.frequency.value=180; const g=AC.createGain(); g.gain.value=1; s.connect(f).connect(g).connect(out); s.start(); amb.cliffG=g; return [s]; }); amb.cliffP=new THREE.Vector3(); }
  { const u=c.x-SPAWN[0], v=c.z-SPAWN[2], d=Math.hypot(u,v)||1, er=WGEN.edgeR(u,v), de=Math.max(0,er-d), k=on&&!P.sky?Math.pow(Math.max(0,1-de/70),2):0, sw=0.5+0.5*Math.sin(amb.t*0.55)*Math.sin(amb.t*0.21+0.7);
    amb.cliffP.set(SPAWN[0]+u/d*(er+20),WGEN.OCEAN_Y,SPAWN[2]+v/d*(er+20)); amb.cliff.set(k*(0.12+0.3*sw*sw),amb.cliffP); } }
function stepAmbience0(dt){""")
# bullets past your head
rep("""    if(k<3) tracer(muzzleV.clone(),r.point,0xffb070,b.h); }""","""    if(k<3) tracer(muzzleV.clone(),r.point,0xffb070,b.h); if(k===0&&!(r.kind==='body'&&T===P)) whizBy(eye,d,r.t); }""")
rep("""function brFire(b,T){""","""// a bullet that passes within a couple of metres of you cracks and whizzes by (heard from where it passed)
function whizBy(o,d,t){ if(!AC||isDead()) return; const c=camera.position, s=Math.max(0,Math.min(t,(c.x-o.x)*d.x+(c.y-o.y)*d.y+(c.z-o.z)*d.z)); if(s<6) return;
  const q=o.clone().addScaledVector(d,s); if(q.distanceTo(c)>2.6) return; sfxPos=q; sfxGain=1; sfx('whiz'); sfxPos=null; }
function brFire(b,T){""")
rep("""    case 'honk':""","""    case 'whiz': noise(5200,0.006,0.32,0.8,0,'highpass'); noise(4200,0.14,0.16,2.2,0.004,'bandpass',1500); tone('sine',2200*r(),900,0.12,0.02,0.005); break; // the crack, then the whine falling away
    case 'honk':""")

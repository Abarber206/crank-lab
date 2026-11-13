# patch201: frame rate with lots of bots, 100 players, a proper spectator camera
#  - a bot more than ~30 m away is drawn as one merged figure (one draw instead of fifty-odd for its rig) and isn't
#    animated; bots far from you think and move a few times a second instead of every frame
#  - battle royale: 100 players (99 bots, names don't repeat)
#  - spectating: the camera sits just behind the player's shoulder, smoothly, never under the ground or water and
#    never through a wall (it used to be dragged from where you died and could end up inside the terrain)
rep("const BR_N=29,","const BR_N=99,")
rep("name:BR_NAMES[i%BR_NAMES.length]","name:BR_NAMES[i%BR_NAMES.length]+(i>=BR_NAMES.length?String(Math.floor(i/BR_NAMES.length)+1):'')")
rep("""function brAnim(b,dt,now){ const d=b.pos.distanceTo(camera.position); b.h.group.visible=d<420||b.sky;""","""// the far figure: an outfit merged into a single mesh in a standing pose (made once per outfit)
const BOT_FAR=new Map();
function botFarGeo(id){ let g=BOT_FAR.get(id); if(g) return g; const o=OUTFITS.find(x=>x.id===id)||OUTFITS[0], h=heroFor(o), z=new THREE.Vector3();
  for(let k=0;k<12;k++) animateRig(h,{bare:true,pos:z,vel:z,yaw:0,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0},1/30);
  if(h.rig.pick) h.rig.pick.visible=false; if(h.lod) heroLod(h,500); g=flattenModel(h.group); BOT_FAR.set(id,g); return g; }
function brFar(b,on){ if(!on){ if(b.far) b.far.visible=false; return; } if(!b.far){ b.far=new THREE.Mesh(botFarGeo(b.h.outfit),bakedMat(false)); b.far.castShadow=false; b.far.receiveShadow=false; scene.add(b.far); }
  const f=b.far; f.visible=true; f.position.copy(b.pos); f.rotation.set(b.sky&&b.sky.phase==='fall'?-1.2:0,b.yaw,0,'YXZ'); }
function brAnim(b,dt,now){ const d=b.pos.distanceTo(camera.position), near=(d<32||b===BR.spec)&&b.alive; brFar(b,!near&&(d<900||!!b.sky)); b.h.group.visible=near;""")
rep("""const h=b.h; setTimeout(()=>{ if(!b.alive) h.group.visible=false; },2600); }""","""const h=b.h; setTimeout(()=>{ if(!b.alive){ h.group.visible=false; if(b.far) b.far.visible=false; } },2600); if(b.far&&b.pos.distanceTo(camera.position)>=32){ b.far.visible=false; } }""")
rep("""for(const b of BR.bots){ b.h.group.visible=false; b.alive=false; }""","""for(const b of BR.bots){ b.h.group.visible=false; b.alive=false; if(b.far) b.far.visible=false; }""")
rep("""  for(const b of BR.bots) if(b.alive) brStepBot(b,dt,now);""","""  { const cp=camera.position; let k=0; for(const b of BR.bots){ k++; if(!b.alive) continue; b.acc=(b.acc||0)+dt; // far from you (and not falling in): a few times a second is plenty
      const far=!b.sky&&!b.bus&&b!==BR.spec&&Math.abs(b.pos.x-cp.x)+Math.abs(b.pos.z-cp.z)>260; if(far&&(BR.frame+k)%3) continue; const st=Math.min(0.12,b.acc); b.acc=0; brStepBot(b,st,now); } }""")
rep("""  if(BR.on) for(const b of BR.bots){ const d=D(b.pos.x,b.pos.z); heroLod(b.h,d); if(d>40) mir.push(b.h.group); }""","""  if(BR.on) for(const b of BR.bots){ const d=D(b.pos.x,b.pos.z); heroLod(b.h,d); if(d>40) mir.push(b.h.group); if(b.far) mir.push(b.far); }""")
# furniture: back to its old distance
rep("far=p.kind==='furn'?d2>60*60:d2>520*520;","far=p.kind==='furn'?d2>45*45:d2>520*520;")
# the spectator camera
rep("""  if(BR.out&&BR.spec&&!$('specTag').hidden){ if(!BR.spec.alive){ brSpecPick(1); if(!BR.spec){ $('specTag').hidden=true; return; } } const b=BR.spec, fx=-Math.sin(b.yaw), fz=-Math.cos(b.yaw);
    _spV.set(b.pos.x-fx*4.2+fz*0.9,b.pos.y+2.4,b.pos.z-fz*4.2-fx*0.9); camera.position.lerp(_spV,Math.min(1,dt*6)); camera.lookAt(b.pos.x+fx*6,b.pos.y+1.4,b.pos.z+fz*6); }""","""  if(BR.out&&BR.spec&&!$('specTag').hidden){ if(!BR.spec.alive){ brSpecPick(1); if(!BR.spec){ $('specTag').hidden=true; return; } } const b=BR.spec;
    if(BR.specFor!==b){ BR.specFor=b; BR.specYaw=b.yaw; BR.specCam=null; } let dy=((b.yaw-BR.specYaw+Math.PI*3)%(Math.PI*2))-Math.PI; BR.specYaw+=dy*Math.min(1,dt*5); // follow their turning, smoothly
    const fx=-Math.sin(BR.specYaw), fz=-Math.cos(BR.specYaw), head=_spH.set(b.pos.x,b.pos.y+1.6,b.pos.z);
    _spV.set(b.pos.x-fx*3.4+fz*0.75,b.pos.y+2.1,b.pos.z-fz*3.4-fx*0.75); const dv=_spD.copy(_spV).sub(head), L=dv.length(); dv.normalize();
    { const r=castShot(head,dv,L+0.4,0.05,null); if(r.kind==='piece'&&r.t<L+0.3) _spV.copy(head).addScaledVector(dv,Math.max(0.6,r.t-0.35)); } // not through a wall
    for(let q=1;q<=3;q++){ const p=_spE.copy(head).lerp(_spV,q/3); const g=Math.max(terrainH(p.x,p.z),waterAt(p.x,p.z))+0.45; if(p.y<g){ _spV.y+=g-p.y; } } // nor into the ground
    if(!BR.specCam) BR.specCam=_spV.clone(); else BR.specCam.lerp(_spV,1-Math.exp(-dt*12));
    camera.position.copy(BR.specCam); camera.lookAt(b.pos.x+fx*5,b.pos.y+1.5,b.pos.z+fz*5); }""")
rep("""const _spV=new THREE.Vector3();""","""const _spV=new THREE.Vector3(), _spH=new THREE.Vector3(), _spD=new THREE.Vector3(), _spE=new THREE.Vector3();""")
# more guns on the ground for a hundred players: lying in yards and streets and out in the wild, as well as in houses
rep("""      else { const k=['light','medium','shells','heavy'][Math.floor(Math.random()*4)]; netDrop(k,AMMO_PACK[k],pos,new THREE.Vector3(),true); } }); }""","""      else { const k=['light','medium','shells','heavy'][Math.floor(Math.random()*4)]; netDrop(k,AMMO_PACK[k],pos,new THREE.Vector3(),true); } }); }
  { const R=Math.random; let n=0; for(let k=0;k<900&&n<150;k++){ const T0=TOWNS[Math.floor(R()*TOWNS.length)], wild=R()<0.45, a=R()*6.283, r=wild?Math.sqrt(R())*MAP_R*0.85:T0.R*(0.3+0.8*R()), x=(wild?SPAWN[0]:T0.x)+Math.cos(a)*r, z=(wild?SPAWN[2]:T0.z)+Math.sin(a)*r, dc=Math.hypot(x-SPAWN[0],z-SPAWN[2]);
      if(worldCell(x,z)<0||waterAt(x,z)>-999||brHouseAt(x,z)||dc<FLAT_R+12||dc>MAP_R-30||terrainH(x,z)>70||slopeAt(x,z)[0]>0.45) continue;
      const pos=new THREE.Vector3(x,terrainH(x,z)+0.5,z), id=lootWeapon(0.85); netDrop(id,WEAPONS[id].mag,pos,new THREE.Vector3(),true); const am=ammoFor(id); netDrop(am[0],am[1],pos.clone().add(new THREE.Vector3(-0.9,0,0.3)),new THREE.Vector3(),true); n++; } }""")
# while spectating: the tag shows who, their health and shield, and their gun
rep("""camera.position.copy(BR.specCam); camera.lookAt(b.pos.x+fx*5,b.pos.y+1.5,b.pos.z+fz*5); }""","""camera.position.copy(BR.specCam); camera.lookAt(b.pos.x+fx*5,b.pos.y+1.5,b.pos.z+fz*5);
    BR.specT=(BR.specT||0)-dt; if(BR.specT<=0){ BR.specT=0.25; $('specName').innerHTML='Spectating <b>'+esc(b.name)+'</b> <span style="opacity:.8;font-size:12px">'+Math.round(b.hp)+' HP'+(b.sh>0?' · '+Math.round(b.sh)+' shield':'')+(b.wpn&&WEAPONS[b.wpn]?' · '+esc(WEAPONS[b.wpn].name):'')+'</span>'; } }""")

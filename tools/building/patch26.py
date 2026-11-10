# ---------- 26. interact key (chests, pick-ups, doors), real doors, inventory, monster elbows and waddle, build reach, shot cracks ----------
# ===== the Interact key =====
rep("emote:'KeyB',map:'KeyM'};","emote:'KeyB',map:'KeyM',interact:'KeyV'};")
rep("emote:'Emote',map:'Full map'};","emote:'Emote',map:'Full map',interact:'Interact (open, pick up, doors)'};")
rep('<div class="hud" id="chestBar" hidden><span>Opening chest</span><span class="pb"><i id="chestB"></i></span></div>',
    '<div class="hud" id="chestBar" hidden><span><b id="useK" class="usek"></b> <span id="useT"></span></span><span class="pb" id="usePB"><i id="chestB"></i></span></div>')
rep("#chestBar .pb{","#chestBar .usek{display:inline-block;min-width:22px;padding:2px 6px;border-radius:4px;background:rgba(255,255,255,.92);color:#10151c;font-style:normal;text-align:center}\nbody.touch #chestBar .usek{display:none}\n#chestBar .pb{")
rep('  <button class="tb" id="tEdit" data-act="edit">Edit</button>','  <button class="tb" id="tEdit" data-act="edit">Edit</button>\n  <button class="tb" id="tUse" data-act="use" hidden>Use</button>')
rep("    else if(act==='emote') startEmote(settings.emote);\n  });","    else if(act==='emote') startEmote(settings.emote);\n    else if(act==='use') useDown();\n  });")
rep("    if(act==='jump') touchJump=false;\n    else if(act==='fire') fireUp('touch'); };","    if(act==='jump') touchJump=false;\n    else if(act==='use') useUp();\n    else if(act==='fire') fireUp('touch'); };")
rep("  else if(a==='map') toggleMap();\n}","  else if(a==='map') toggleMap();\n  else if(a==='interact') useDown();\n}")
rep("function releaseAction(a){\n  if(a==='aim') adsHeld=false;","function releaseAction(a){\n  if(a==='interact') useUp();\n  if(a==='aim') adsHeld=false;")
rep("      if(down(2)) startReload(); if(down(3)) toggleEdit(); if(down(1)) toggleBuild();",
    "      if(down(2)){ if(useTgt) useDown(); else startReload(); } if(up(2)) useUp(); if(down(3)) toggleEdit(); if(down(1)) toggleBuild();")
# what you can interact with: the nearest thing in front of you (an unopened chest, something to pick up, a door)
rep("let chestHumT=0, chestNear=null;","""let chestHumT=0, chestNear=null, useHeld=false, useTgt=null;
function useDown(){ useHeld=true; const t=useTgt; if(!t||isDead()) return;
  if(t.kind==='drop'){ const d=t.d; if(!canTake(d)){ if(performance.now()-fullToastT>1500){ fullToastT=performance.now(); toast('Inventory full – press '+codeName(settings.binds.inventory||'Tab')+' to swap'); } return; } takeDrop(d,null); }
  else if(t.kind==='door') toggleDoor(t.p,t.c,false); }
function useUp(){ useHeld=false; }
function findUseTarget(){
  if(!playing||isDead()||edit||invOpen) return null;
  const fx=-Math.sin(P.yaw), fz=-Math.cos(P.yaw); let best=null, bs=1e9;
  const consider=(x,y,z,r,o)=>{ const dx=x-P.pos.x, dz=z-P.pos.z, d=Math.hypot(dx,dz); if(d>r||Math.abs(y-P.pos.y)>1.8) return; const face=d>0.05?(dx*fx+dz*fz)/d:1, s=d-face*0.9; if(s<bs){ bs=s; best=o; } };
  for(const c of chests) if(!c.open&&c.g.visible) consider(c.x,c.y,c.z,2.4,{kind:'chest',c,label:'Open chest'});
  drops.forEach(d=>{ if(AMMO_T[d.item]||d.pending||(!d.landed&&d.t<0.4)) return; consider(d.pos.x,d.pos.y,d.pos.z,1.9,{kind:'drop',d,label:'Pick up '+itemInfo(d.item).name+(isWeapon(d.item)&&d.item!=='nade'?'':' ×'+d.n)}); });
  near(P.pos.x,P.pos.z,1).forEach(p=>{ if(!p.doors) return; p.doors.forEach((dr,c)=>{ if(!dr) return; const q=doorCenter(p,c); consider(q.x,q.y-1.2,q.z,2.4,{kind:'door',p,c,label:dr.open?'Close door':'Open door'}); }); });
  return best; }""")
# chests: open by holding Interact (not by walking up), a soft magical hum instead of a ding, heard only close by
rep("  chestHumT-=dt; let best=null, bd=16;","  chestHumT-=dt; let best=null, bd=9; useTgt=findUseTarget();")
rep("    if(!c.open&&playing&&!isDead()&&d<2.1&&Math.abs(c.y-P.pos.y)<1.7){ c.prog+=dt/CHEST_OPEN_T; showing=true; $('chestB').style.width=Math.min(100,c.prog*100).toFixed(0)+'%'; if(c.prog>=1) requestChest(c); }",
    "    if(!c.open&&useTgt&&useTgt.c===c&&useHeld){ c.prog+=dt/CHEST_OPEN_T; if(c.prog>=1) requestChest(c); }")
rep("  if(bar.hidden===showing) bar.hidden=!showing;\n  if(best&&chestHumT<=0){ chestHumT=1.5; sfxAt('chest_hum',new THREE.Vector3(best.x,best.y+0.5,best.z)); }",
    """  // the prompt: what Interact would do here (and how far along opening a chest is)
  showing=!!useTgt; if(showing){ const lt=useTgt.kind==='chest'&&useTgt.c.prog>0?'Opening chest':useTgt.label; if($('useT').textContent!==lt) $('useT').textContent=lt; const kl=codeName(settings.binds.interact||'KeyV'); if($('useK').textContent!==kl) $('useK').textContent=kl;
    const pr=useTgt.kind==='chest'; $('usePB').hidden=!pr; if(pr) $('chestB').style.width=Math.min(100,useTgt.c.prog*100).toFixed(0)+'%'; }
  if(bar.hidden===showing) bar.hidden=!showing; const tu=$('tUse'); if(tu&&tu.hidden===showing) tu.hidden=!showing;
  if(best&&chestHumT<=0){ chestHumT=2.1; sfxAt('chest_hum',new THREE.Vector3(best.x,best.y+0.5,best.z)); }""")
rep("    case 'chest_hum': [880,1109,1319,1760].forEach((f,q)=>tone('sine',f,f*1.003,1.1,0.018,q*0.07)); break;",
    """    case 'chest_hum': { const t=AC.currentTime, g=AC.createGain(); g.gain.setValueAtTime(0.0001,t); g.gain.linearRampToValueAtTime(0.016,t+0.9); g.gain.linearRampToValueAtTime(0.0001,t+2.5); g.connect(cur); // a soft, swelling shimmer: no attack, so it never dings
      [392,494,587,784].forEach((f,q)=>{ const o=AC.createOscillator(), l=AC.createOscillator(), lg=AC.createGain(); o.type='sine'; o.frequency.value=f*(1+q*0.0015); l.frequency.value=4.5+q*0.7; lg.gain.value=f*0.005; l.connect(lg).connect(o.frequency); o.connect(g); o.start(t); o.stop(t+2.6); l.start(t); l.stop(t+2.6); }); break; }""")
# an open lid is solid from inside too (it was see-through from below)
rep("put(lid,rbox(.16,.18,.05,.02),Au,0,-.02,-.63);","put(lid,rbox(.16,.18,.05,.02),Au,0,-.02,-.63); put(lid,rbox(.98,.025,.6,.008),Dk,0,.012,-.31);")
rep("const l=new THREE.Mesh(M.lidGeo,M.body);","if(!M.lidMat){ M.lidMat=M.body.clone(); M.lidMat.side=THREE.DoubleSide; } const l=new THREE.Mesh(M.lidGeo,M.lidMat);")
# weapons and items are picked up with Interact; only ammo is collected by walking over it
rep("    const dx=d.pos.x-P.pos.x, dz=d.pos.z-P.pos.z; if(dx*dx+dz*dz>1.5*1.5||Math.abs(d.pos.y-P.pos.y)>1.8) return;",
    "    if(!AMMO_T[d.item]) return; // guns, heals and grenades wait for Interact\n    const dx=d.pos.x-P.pos.x, dz=d.pos.z-P.pos.z; if(dx*dx+dz*dz>1.5*1.5||Math.abs(d.pos.y-P.pos.y)>1.8) return;")

# ===== inventory: keep moving, slot numbers match the hotbar, no ammo text on guns =====
rep("  if(invOpen||!playing) return; invOpen=true; releaseAll(); fireHeld=false; adsHeld=false; P.vel.x*=0.3; P.vel.z*=0.3;",
    "  if(invOpen||!playing) return; invOpen=true; if(fireHeld) fireUp('desk'); fireHeld=false; adsHeld=false; heldPiece=null; // movement keys stay held: you keep moving")
rep("    const sub=id?(isItem(id)||id==='nade'?'×'+countOf(id):RNAME[I.rarity]+' · '+(P.ammo[id]|0)+' / '+WEAPONS[id].mag+(WEAPONS[id].ammo?' · '+AMMO_T[WEAPONS[id].ammo].name:'')):'Empty';\n    b.innerHTML=`<span class=\"key\">${i+2}</span>`+(id?`<svg viewBox=\"0 0 48 48\">${iconOf(id)}</svg>`:'<span class=\"plus\">+</span>')+`<b>${id?I.name:'Slot '+(i+2)}</b><small>${sub}</small>`;",
    "    const sub=id?(isItem(id)||id==='nade'?'×'+countOf(id):''):'Empty', kl=slotKeyLabel(i);\n    b.innerHTML=`<span class=\"key\">${kl}</span>`+(id?`<svg viewBox=\"0 0 48 48\">${iconOf(id)}</svg>`:'<span class=\"plus\">+</span>')+`<b>${id?I.name:'Slot '+kl}</b>`+(sub?`<small>${sub}</small>`:'');")
s=s.replace("'Swap into slot '+(invSel+2)","'Swap into slot '+slotKeyLabel(invSel)")
rep("function renderInv(){","function slotKeyLabel(i){ return codeName(settings.binds[SLOT_BINDS[i]]||'').replace(' mouse','').replace(/ \\((back|fwd)\\)/,''); } // the same key label the hotbar shows\nfunction renderInv(){")

# ===== no turning once you're eliminated =====
rep("  P.yaw-=e.movementX*s; P.pitch=Math.max(-1.45,Math.min(1.45,P.pitch-e.movementY*s));","  if(isDead()) return; P.yaw-=e.movementX*s; P.pitch=Math.max(-1.45,Math.min(1.45,P.pitch-e.movementY*s));")
rep("const s=0.0058*settings.sens*(1-0.4*adsK)*(scopeOn?0.45:1)*(edit?settings.editSens:1); P.yaw-=","const s=isDead()?0:0.0058*settings.sens*(1-0.4*adsK)*(scopeOn?0.45:1)*(edit?settings.editSens:1); P.yaw-=")
rep("    const am=(1-0.45*adsK)*(edit?settings.editSens:1); P.yaw-=","    const am=isDead()?0:(1-0.45*adsK)*(edit?settings.editSens:1); P.yaw-=")

# ===== builds land close: walls on the edge of the tile you're on, other pieces on the next tile =====
rep("    if(Math.abs(ux)>=Math.abs(uz)){ axis='x'; i=Math.round(lx/CELL); if((i*CELL-x)*Math.sign(ux)<0.4) i+=Math.sign(ux); j=cellOf(z+uz*Math.abs((i*CELL-x)/ux)); t=Math.abs((i*CELL-x)/ux); }\n    else { axis='z'; j=Math.round(lz/CELL); if((j*CELL-z)*Math.sign(uz)<0.4) j+=Math.sign(uz); i=cellOf(x+ux*Math.abs((j*CELL-z)/uz)); t=Math.abs((j*CELL-z)/uz); }",
    "    if(Math.abs(ux)>=Math.abs(uz)){ axis='x'; i=ux>0?ci+1:ci; t=Math.abs((i*CELL-x)/ux); j=cellOf(z+uz*t); }\n    else { axis='z'; j=uz>0?cj+1:cj; t=Math.abs((j*CELL-z)/uz); i=cellOf(x+ux*t); }")
rep("const hl2=Math.hypot(_ld.x,_ld.z)||1, far={x:x+_ld.x/hl2*REACH,z:z+_ld.z/hl2*REACH};","const hl2=Math.hypot(_ld.x,_ld.z)||1, far={x:x+_ld.x/hl2*2.6,z:z+_ld.z/hl2*2.6};")

# ===== shots stop at a build's solid shape (no slipping through the hairline gaps between pieces) =====
rep("function castShot(o,d,range,nearT,target){","""function rayBox(o,d,b){ let t0=-1e9, t1=1e9; const O=[o.x,o.y,o.z], D=[d.x,d.y,d.z];
  for(let a=0;a<3;a++){ const lo=b[a], hi=b[a+3]; if(Math.abs(D[a])<1e-9){ if(O[a]<lo||O[a]>hi) return -1; continue; } let ta=(lo-O[a])/D[a], tb=(hi-O[a])/D[a]; if(ta>tb){ const s_=ta; ta=tb; tb=s_; } if(ta>t0) t0=ta; if(tb<t1) t1=tb; if(t0>t1) return -1; }
  return t0; }
function boxShot(o,d,range,nearT){ let best=null;
  for(const p of order){ if(!p.boxes||!p.boxes.length) continue; _c.subVectors(p.group.position,o); const t=_c.dot(d); if(t<-4||t>range+4||_c.addScaledVector(d,-t).lengthSq()>36) continue;
    for(const b of p.boxes){ const tb=rayBox(o,d,b); if(tb>=nearT&&tb<=range&&(!best||tb<best.t)) best={t:tb,p}; } }
  return best; }
function castShot(o,d,range,nearT,target){""")
rep("""  if(bh&&bh.t<=range&&(!ph||bh.t<ph.distance)) return {kind:'body',t:bh.t,head:bh.head,who,point:o.clone().addScaledVector(d,bh.t)};
  if(ph) return {kind:'piece',t:ph.distance,piece:ph.object.userData.piece,point:ph.point.clone()};""",
"""  const bx=boxShot(o,d,range,nearT); let pt=ph?ph.distance:Infinity, pp=ph?ph.object.userData.piece:null;
  if(bx&&bx.t<pt-0.02){ pt=bx.t; pp=bx.p; }
  if(bh&&bh.t<=range&&bh.t<pt) return {kind:'body',t:bh.t,head:bh.head,who,point:o.clone().addScaledVector(d,bh.t)};
  if(pp) return {kind:'piece',t:pt,piece:pp,point:o.clone().addScaledVector(d,pt)};""")

# ===== real doors: every door opening in a wall (a door edit, a window door, the houses' front doors) gets a door =====
rep("function buildPiece(p){","""/* Doors. A wall whose edit leaves a door opening (two tiles high in one column, wall above it and beside it)
   gets a door panel hinged at one side. Interact opens it (swinging away from you) or closes it. A closed door
   blocks players, bots, creatures and shots like the wall; an open one doesn't. Doors are their own small meshes
   (so they keep moving even when a town's houses are merged into one mesh) and are only drawn within 120 m. */
const DOOR_ANG=1.5, doorMats={};
function doorSlots(mask){ const out=[]; if(mask==null||mask===511) return out; const k=i=>!!(mask>>i&1);
  for(let c=0;c<3;c++) if(!k(c)&&!k(c+3)&&k(c+6)&&[c-1,c+1].every(n=>n<0||n>2||(k(n)&&k(n+3)))) out.push(c); return out; }
function doorCenter(p,c){ const tw=CELL/3, th=LVL/3, y=p.l*LVL+th; return p.axis==='x'?new THREE.Vector3(p.i*CELL,y,p.j*CELL+(c+.5)*tw):new THREE.Vector3(p.i*CELL+(c+.5)*tw,y,p.j*CELL); }
function doorGeo(X){ const key=X?'x':'z'; if(doorGeo[key]) return doorGeo[key]; const tw=CELL/3-0.08, h=2*LVL/3-0.06, th=0.09;
  const panel=X?new THREE.BoxGeometry(th,h,tw):new THREE.BoxGeometry(tw,h,th); X?panel.translate(0,h/2+0.02,tw/2+0.04):panel.translate(tw/2+0.04,h/2+0.02,0);
  const parts=[{geo:panel,M:new THREE.Matrix4(),col:new THREE.Color(1,1,1)}];
  for(const s of [-1,1]){ const kb=new THREE.SphereGeometry(0.055,10,8); const off=X?new THREE.Vector3(s*0.07,1.0,tw-0.12):new THREE.Vector3(tw-0.12,1.0,s*0.07); parts.push({geo:kb,M:new THREE.Matrix4().makeTranslation(off.x,off.y,off.z),col:new THREE.Color(0xd8c27a)}); }
  return doorGeo[key]=bakeGeo(parts,true); }
function doorMat(p){ const col=p.skin?[0x7a2e2a,0x3b4a5a,0x5a3d26,0x2f5a46][(p.i*7+p.j*3)&3]:{wood:0x8a5a32,brick:0x6e4a36,metal:0x7d8794}[p.mat]||0x8a5a32;
  return doorMats[col]||(doorMats[col]=new THREE.MeshPhongMaterial({color:col,vertexColors:true,shininess:20,specular:0x222222})); }
const doorPieces=new Set();
function makeDoors(p){ dropDoors(p); if(p.type!=='wall') return; const slots=doorSlots(p.mask); if(!slots.length) return;
  p.doors=[]; p.doorMeshes=[]; const g=new THREE.Group(); g.position.copy(pieceCenter(p)); scene.add(g); p.doorG=g; const X=p.axis==='x', tw=CELL/3;
  for(const c of slots){ const pv=new THREE.Group(); X?pv.position.set(0,-LVL/2,-CELL/2+c*tw):pv.position.set(-CELL/2+c*tw,-LVL/2,0);
    const m=new THREE.Mesh(doorGeo(X),doorMat(p)); m.castShadow=m.receiveShadow=true; m.userData.piece=p; pv.add(m); g.add(pv); p.doorMeshes.push(m);
    p.doors[c]={open:false,ang:0,to:0,pv}; }
  doorPieces.add(p); }
function dropDoors(p){ if(p.doorG){ if(p.doorG.parent) p.doorG.parent.remove(p.doorG); } p.doorG=null; p.doors=null; p.doorMeshes=null; doorPieces.delete(p); }
function toggleDoor(p,c,fromNet,open,side){ const d=p.doors&&p.doors[c]; if(!d||!pieces.has(p.key)) return;
  if(!fromNet){ open=!d.open; const q=doorCenter(p,c); side=p.axis==='x'?Math.sign(P.pos.x-q.x)||1:Math.sign(P.pos.z-q.z)||1; }
  d.open=open; d.to=open?(p.axis==='x'?(side<0?DOOR_ANG:-DOOR_ANG):(side<0?-DOOR_ANG:DOOR_ANG)):0;
  p.boxes=makeBoxes(p); if(!open) popPlayerOut();
  const q=doorCenter(p,c); if(q.distanceTo(P.pos)<40) sfxAt(open?'door_open':'door_close',q);
  if(!fromNet) netOp({op:'door',key:p.key,c,open,side}); }
function stepDoors(dt){ doorPieces.forEach(p=>{ if(!pieces.has(p.key)){ dropDoors(p); return; } const vis=p.doorG.position.distanceTo(camera.position)<120; p.doorG.visible=vis;
  p.doors.forEach(d=>{ if(!d||Math.abs(d.to-d.ang)<1e-3) return; d.ang+=(d.to-d.ang)*Math.min(1,dt*10); d.pv.rotation.y=d.ang; }); }); }
function buildPiece(p){""")
rep("  p.boxes=makeBoxes(p); p.slab=(p.type==='ramp'||p.type==='cone'); p.bb=null; p.bb=pbox(p);",
    "  if(p.type==='wall'){ const keep=p.doors&&String(doorSlots(p.mask))===String(p.doors.map((d,c)=>d?c:null).filter(c=>c!=null))?p.doors.map(d=>d&&{open:d.open,to:d.to}):null; makeDoors(p); if(keep&&p.doors) keep.forEach((k,c)=>{ if(k&&p.doors[c]){ p.doors[c].open=k.open; p.doors[c].to=p.doors[c].ang=k.to; p.doors[c].pv.rotation.y=k.to; } }); }\n  p.boxes=makeBoxes(p); p.slab=(p.type==='ramp'||p.type==='cone'); p.bb=null; p.bb=pbox(p);")
rep("  if(p.fix) out.push(...p.fix.boxes); // a house's staircase or stairwell railing\n  return out;",
    "  if(p.fix) out.push(...p.fix.boxes); // a house's staircase or stairwell railing\n  if(p.doors) p.doors.forEach((d,c)=>{ if(!d||d.open) return; const tw=CELL/3, th=LVL/3; if(p.axis==='x'){ const X=p.i*CELL, z0=p.j*CELL+c*tw; out.push([X-WT/2,y0,z0,X+WT/2,y0+2*th,z0+tw]); } else { const Z=p.j*CELL, x0=p.i*CELL+c*tw; out.push([x0,y0,Z-WT/2,x0+tw,y0+2*th,Z+WT/2]); } }); // a closed door\n  return out;")
rep("  if(!keepMesh){ dropScaffold(p); scene.remove(p.group); }","  if(!keepMesh){ dropScaffold(p); scene.remove(p.group); dropDoors(p); }\n  else if(p.doorG){ p.doorG.position.set(0,0,0); p.group.add(p.doorG); doorPieces.delete(p); } // the door falls with its wall")
rep("    if(_c.addScaledVector(d,-t).lengthSq()<36) for(const m of p.group.children) out.push(m); }","    if(_c.addScaledVector(d,-t).lengthSq()<36){ for(const m of p.group.children) out.push(m); if(p.doorMeshes) out.push(...p.doorMeshes); } }")
rep("function nearMeshes(x,z,rad){ const out=[]; near(x,z,rad).forEach(p=>{ for(const m of p.group.children) out.push(m); }); return out; }",
    "function nearMeshes(x,z,rad){ const out=[]; near(x,z,rad).forEach(p=>{ for(const m of p.group.children) out.push(m); if(p.doorMeshes) out.push(...p.doorMeshes); }); return out; }")
rep("  else if(o.op==='shape'){","  else if(o.op==='door'){ const p=pieces.get(o.key); if(p) toggleDoor(p,o.c,true,!!o.open,o.side||1); }\n  else if(o.op==='shape'){")
rep("  stepClouds(dt); stepPick(dt);","  stepClouds(dt); stepDoors(dt); stepPick(dt);")
rep("    case 'groan': zombieGroan(0.34); break;","""    case 'groan': zombieGroan(0.34); break;
    case 'door_open': knock(180*r(),0.06,0.3,4); noise(500,0.35,0.12,2,0.04,'bandpass',300); tone('sawtooth',90*r(),70,0.3,0.012,0.05); break; // latch, then a creak
    case 'door_close': knock(140*r(),0.1,0.45,4,0.05); knock(900,0.03,0.15,8); break;""")

# ===== creatures do less damage to builds and houses =====
for a,b in [("hp:110,spd:0.56,dmg:12,bld:16,","hp:110,spd:0.56,dmg:12,bld:10,"),("hp:70, spd:0.98,dmg:8, bld:10,","hp:70, spd:0.98,dmg:8, bld:6, "),("hp:520,spd:0.42,dmg:30,bld:55,","hp:520,spd:0.42,dmg:30,bld:32,"),("hp:95, spd:0.5, dmg:10,bld:14,","hp:95, spd:0.5, dmg:10,bld:8, "),("throwDmg:20,throwBld:60}","throwDmg:20,throwBld:35}")]: rep(a,b)
# ===== the waddle comes from the hips over the planted leg, not the whole body rocking =====
rep("  if(ty==='husk'){ R.legL.rotation.x=s*0.55*mv; R.legR.rotation.x=-0.22*mv-s*0.16*mv; R.hips.position.y=R.hipY-0.07*Math.max(0,-s)*mv; R.hips.rotation.z=s*0.15*mv; }\n  else if(run){ R.legL.rotation.x=s*0.8*mv; R.legR.rotation.x=-s*0.8*mv; R.hips.position.y=R.hipY+Math.abs(c)*0.07*mv; R.hips.rotation.z=s*0.05*mv; }\n  else { const a=ty==='brute'?0.42:0.5; R.legL.rotation.x=s*a*mv; R.legR.rotation.x=-s*a*mv; R.hips.position.y=R.hipY+Math.abs(c)*(ty==='brute'?0.06:0.04)*mv; R.hips.rotation.z=s*0.1*mv; }",
    """  if(ty==='husk'){ R.legL.rotation.x=s*0.55*mv; R.legR.rotation.x=-0.22*mv-s*0.16*mv; R.hips.position.y=R.hipY-0.07*Math.max(0,-s)*mv; }
  else if(run){ R.legL.rotation.x=s*0.8*mv; R.legR.rotation.x=-s*0.8*mv; R.hips.position.y=R.hipY+Math.abs(c)*0.07*mv; }
  else { const a=ty==='brute'?0.42:0.5; R.legL.rotation.x=s*a*mv; R.legR.rotation.x=-s*a*mv; R.hips.position.y=R.hipY+Math.abs(c)*(ty==='brute'?0.06:0.04)*mv; }
  // weight shift: the hips slide over the leg that's down and tip a little; the legs stay planted (they counter the tip)
  // and the spine leans back the other way, so the body stays over the feet instead of rocking side to side
  const roll=(ty==='husk'?0.07:ty==='brute'?0.06:run?0.025:0.05)*s*mv; R.hips.rotation.z=roll; R.legL.rotation.z=-roll; R.legR.rotation.z=-roll; R.hips.position.x=-s*(ty==='brute'?0.06:0.04)*mv;""")
rep("  R.spine.rotation.y=(ty==='brute'?s*0.12*mv:0)-thW*0.45+thF*0.35; R.spine.rotation.z=Math.sin(z.walk*0.5)*0.08;",
    "  R.spine.rotation.y=(ty==='brute'?s*0.12*mv:0)-thW*0.45+thF*0.35; R.spine.rotation.z=-roll*0.85;")
# elbows: the forearms bend (hang relaxed, swing behind the upper arm, cock back on the wind-up, snap straight on the strike)
rep("  R.armL.rotation.z=-0.12-raise*0.25-scr*0.9; R.armR.rotation.z=0.12+raise*0.25+scr*0.9+thW*0.3;",
    """  R.armL.rotation.z=-0.12-raise*0.25-scr*0.9; R.armR.rotation.z=0.12+raise*0.25+scr*0.9+thW*0.3;
  if(R.foreL){ const lag=run?0.5*Math.max(0,s)*mv:0.18*Math.max(0,Math.sin(z.walk*0.9-0.8))+0.12*mv, lagR=run?0.5*Math.max(0,-s)*mv:0.18*Math.max(0,-Math.sin(z.walk*0.9+0.6-0.8))+0.12*mv;
    R.foreL.rotation.x=R.elbow0+lag+raise*0.9-strike*0.55+scr*0.3; R.foreR.rotation.x=R.elbow0+lagR+raise*0.9-strike*0.55+scr*0.3+thW*1.3-thF*0.8; }""")
# ===== no hitch the first time you build, edit or switch material: compile those shaders up front, on the menu =====
rep("setTimeout(()=>queueIcons([...Object.keys(WEAPONS),...Object.keys(ITEMS),...Object.keys(AMMO_T)]),400); // icon pictures, a few a frame",
"""setTimeout(()=>queueIcons([...Object.keys(WEAPONS),...Object.keys(ITEMS),...Object.keys(AMMO_T)]),400); // icon pictures, a few a frame
// Every material building and editing can show (the preview, edit tiles, all three materials, cracks, scaffold
// lines, sparks, doors) is compiled once while you're on the menu, so the first wall or edit doesn't pause the game.
function warmBuildShaders(){ try{ const g=new THREE.Group(), geo=new THREE.BoxGeometry(0.01,0.01,0.01), lg=new THREE.EdgesGeometry(geo), mats=[ghostMat,ghostBad,ghostDim,editPieceMat,tileMat,tileBadMat,tileHoverMat,tileSelMat,blueprintMat,buildGlowMat,sparkMat,hotSparkMat];
  MAT_ORDER.forEach(m=>{ const M=matFor[m]; mats.push(M.wall,M.floor,M.tread,M.beam,M.cone,M.chip,...(crackMats[m]||[])); });
  mats.forEach(m=>{ if(!m) return; const x=new THREE.Mesh(geo,m); x.castShadow=x.receiveShadow=true; g.add(x); });
  [ghostLine.ok,ghostLine.bad,ghostLine.occ,...Object.values(scaffoldMat)].forEach(m=>g.add(new THREE.LineSegments(lg,m)));
  const dm=new THREE.Mesh(doorGeo(true),doorMat({mat:'wood'})); g.add(dm);
  g.position.copy(camera.position); scene.add(g); renderer.compile(scene,camera); scene.remove(g); }catch(e){ console.warn('shader warm-up skipped',e); } }
setTimeout(warmBuildShaders,1500);""")

# ---------- 84. map you can use with the mouse (cursor freed while it's open; wheel zooms, drag pans), sharper and with the
# forest drawn on it; solid mailboxes; the hole beside the stairs on the upper floor is floored over with the railing against the stairs ----------
# (a) the map
rep("  $('bigmap').hidden=!mapOpen;\n  if(mapOpen){","  $('bigmap').hidden=!mapOpen;\n  if(!isTouch){ if(mapOpen&&document.pointerLockElement){ invUnlocking=true; document.exitPointerLock(); } else if(!mapOpen&&playing&&!lockFailed&&!invOpen){ try{ const r=canvas.requestPointerLock(); if(r&&r.catch) r.catch(()=>{}); }catch(e){} } }\n  if(mapOpen){")
rep("else if(invUnlocking||invOpen){ invUnlocking=false; }","else if(invUnlocking||invOpen||mapOpen){ invUnlocking=false; }")
rep("'Scroll to zoom · drag to move · '+codeName(settings.binds.map||'KeyM')+' or click to close'","'Scroll to zoom · drag to move · '+codeName(settings.binds.map||'KeyM')+' or Close to exit'")
rep("if(mapView.ptrs.size===0&&mapView.moved<6) toggleMap(false); };","if(isTouch&&mapView.ptrs.size===0&&mapView.moved<6) toggleMap(false); };")
rep("  const S=1024, c=document.createElement('canvas'); c.width=c.height=S; const g=c.getContext('2d'), img=g.createImageData(S,S)","  const S=2048, c=document.createElement('canvas'); c.width=c.height=S; const g=c.getContext('2d'), img=g.createImageData(S,S)")
rep("  g.lineCap='round'; g.lineJoin='round';\n  for(const [w,col] of [[7,'#26282c'],[3.6,'#9a9ea4']]){",
r"""  // the forest: every tree as a small crown with a lit side (pines darker and pointier)
  for(const p of props){ if(p.gone||!(p.kind==='tree'||p.kind==='pine')) continue; const x=X(p.x-SPAWN[0]), y=X(p.z-SPAWN[2]), r=(p.kind==='pine'?1.9:2.6)*(p.s||1)/mpp;
    g.fillStyle='rgba(20,40,22,.35)'; g.beginPath(); g.arc(x+r*0.35,y+r*0.35,r,0,7); g.fill();
    g.fillStyle=p.kind==='pine'?'#2c5a3c':'#3f7a34'; g.beginPath(); g.arc(x,y,r,0,7); g.fill();
    g.fillStyle=p.kind==='pine'?'#3f7450':'#5c9a48'; g.beginPath(); g.arc(x-r*0.25,y-r*0.25,r*0.55,0,7); g.fill(); }
  g.lineCap='round'; g.lineJoin='round';
  for(const [w,col] of [[14,'#26282c'],[7.2,'#9a9ea4']]){""")
rep("g.setLineDash([]); g.strokeStyle='rgba(255,236,190,.8)'; g.lineWidth=2; g.beginPath(); g.arc(X(0),X(0),FLAT_R/mpp,0,7); g.stroke(); // the build field","g.setLineDash([]); g.strokeStyle='rgba(255,236,190,.8)'; g.lineWidth=3; g.beginPath(); g.arc(X(0),X(0),FLAT_R/mpp,0,7); g.stroke(); // the build field")
rep("function mapClamp(){ mapView.zoom=Math.max(1,Math.min(10,mapView.zoom));","function mapClamp(){ mapView.zoom=Math.max(1,Math.min(16,mapView.zoom));")
# (b) small solid things in the world (mailboxes): bumped into by people and buggies
rep("const solidNear=(E)=>{","var STATICS=[];\nconst solidNear=(E)=>{")
rep("if(VANS) for(const v of VANS) if(Math.abs(v.x-E.pos.x)<7&&Math.abs(v.z-E.pos.z)<7) ps.add(v.solid); if(typeof chests","for(const q of STATICS) if(Math.abs(q.x-E.pos.x)<3&&Math.abs(q.z-E.pos.z)<3) ps.add(q.solid); if(VANS) for(const v of VANS) if(Math.abs(v.x-E.pos.x)<7&&Math.abs(v.z-E.pos.z)<7) ps.add(v.solid); if(typeof chests")
rep("propsNear(x,z,ps); if(VANS) for(const v of VANS) if(Math.abs(v.x-x)<8&&Math.abs(v.z-z)<8) ps.add(v.solid);","propsNear(x,z,ps); for(const q of STATICS) if(Math.abs(q.x-x)<4&&Math.abs(q.z-z)<4) ps.add(q.solid); if(VANS) for(const v of VANS) if(Math.abs(v.x-x)<8&&Math.abs(v.z-z)<8) ps.add(v.solid);")
rep("        put(new THREE.BoxGeometry(0.09,1.05,0.09),0x5a4030,x,y0+0.52,z,ry);","        STATICS.push({x,z,solid:{boxes:[[x-0.16,y0,z-0.16,x+0.16,y0+1.26,z+0.16]],key:'mail'+STATICS.length}});\n        put(new THREE.BoxGeometry(0.09,1.05,0.09),0x5a4030,x,y0+0.52,z,ry);")
# (c) upstairs: floor over the open strip beside the staircase, and put the railing right against the stairs
rep("const stairs={boxes:[],parts:{tread:[],inner:[],beam:[]}}, rail={boxes:[],parts:{beam:[]}};","const stairs={boxes:[],parts:{tread:[],inner:[],beam:[]}}, rail={boxes:[],parts:{beam:[],tread:[]}}, RT=SW+0.14;")
rep("  rail.boxes.push(box(LAND,S1,TW-0.05,TW+0.05,LVL,LVL+1.0), box(S1-0.05,S1+0.05,0,TW,LVL,LVL+1.0));\n  const posts=[[LAND,TW],[LAND+(S1-LAND)/3,TW],[LAND+2*(S1-LAND)/3,TW],[S1,TW],[S1,TW/2],[S1,0.06]];",
    "  { const slab=box(LAND,S1,SW+0.08,TW,LVL-0.26,LVL); rail.boxes.push(slab); rail.parts.tread.push(geo(slab)); }\n  rail.boxes.push(box(LAND,S1,RT-0.05,RT+0.05,LVL,LVL+1.0), box(S1-0.05,S1+0.05,0,RT,LVL,LVL+1.0));\n  const posts=[[LAND,RT],[LAND+(S1-LAND)/3,RT],[LAND+2*(S1-LAND)/3,RT],[S1,RT],[S1,RT/2],[S1,0.06]];")
rep("rail.parts.beam.push(beamGeo(V3(LAND,TW,LVL+y),V3(S1,TW,LVL+y),y>0.9?0.07:0.04), beamGeo(V3(S1,TW,LVL+y),V3(S1,0.06,LVL+y),y>0.9?0.07:0.04)); }","rail.parts.beam.push(beamGeo(V3(LAND,RT,LVL+y),V3(S1,RT,LVL+y),y>0.9?0.07:0.04), beamGeo(V3(S1,RT,LVL+y),V3(S1,0.06,LVL+y),y>0.9?0.07:0.04)); }")
rep("  for(let s=LAND+0.3;s<S1-0.1;s+=0.32) rail.parts.beam.push(beamGeo(V3(s,TW,LVL),V3(s,TW,LVL+0.97),0.03));\n  for(let t=0.36;t<TW-0.1;t+=0.32) rail.parts.beam.push(beamGeo(V3(S1,t,LVL),V3(S1,t,LVL+0.97),0.03));",
    "  for(let s=LAND+0.3;s<S1-0.1;s+=0.32) rail.parts.beam.push(beamGeo(V3(s,RT,LVL),V3(s,RT,LVL+0.97),0.03));\n  for(let t=0.36;t<RT-0.1;t+=0.32) rail.parts.beam.push(beamGeo(V3(S1,t,LVL),V3(S1,t,LVL+0.97),0.03));")
# (d) skydiving / gliding: every gun model is put away (only two of them were being hidden)
rep("  r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;\n  // the glider unfolds","  r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false; for(const k of GUN_MODELS) if(r[k]) r[k].visible=false;\n  // the glider unfolds")

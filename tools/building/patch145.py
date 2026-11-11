# patch145: the Reboot Van, rebuilt. A real step van: one body (side profile with a sloped windscreen, a hood, a
# rounded roof and real wheel arches, extruded and bevelled) in white over a blue skirt and an orange stripe; glass all
# round, grille, bumpers, headlights and tail lights, mirrors, a sliding side door and rear doors, a ladder and roof
# rack, a dish and a light bar; tyres with hubs in lined arches. Its terminal screen shows READY / CHARGING with the
# time left, and fills a bar while you reboot. While you carry a reboot card a marker on screen points to the nearest
# van that's ready, with its distance.
a=s.index("function makeVan(x,y,z,yaw){"); b=s.index("// ---- interact: grab a card (hold), reboot at a van (hold) ----")
s=s[:a]+r"""function vanBodyGeo(){ const V=(x,y,z)=>new THREE.Vector3(x,y,z), W=2.06;
  // the side profile, u along the van (front at -2.25), v up; wheel arches cut in at the front and back wheels
  const P=new THREE.Shape(); P.moveTo(2.1,0.48); P.lineTo(2.1,2.62); P.quadraticCurveTo(2.1,2.86,1.86,2.86); P.lineTo(-0.72,2.86); P.quadraticCurveTo(-0.95,2.86,-1.02,2.62);
  P.lineTo(-1.82,1.5); P.quadraticCurveTo(-1.9,1.38,-2.05,1.36); P.lineTo(-2.18,1.32); P.quadraticCurveTo(-2.27,1.29,-2.27,1.15); P.lineTo(-2.27,0.58); P.quadraticCurveTo(-2.27,0.48,-2.17,0.48);
  P.lineTo(-2.0,0.48); P.absarc(-1.45,0.48,0.55,Math.PI,0,true); P.lineTo(0.8,0.48); P.absarc(1.35,0.48,0.55,Math.PI,0,true); P.lineTo(2.1,0.48);
  const body=new THREE.ExtrudeGeometry(P,{depth:W,bevelEnabled:true,bevelThickness:0.05,bevelSize:0.05,bevelSegments:2,curveSegments:10}); body.rotateY(-Math.PI/2); body.translate(W/2,0,0);
  // the blue skirt and orange stripe: the lower body again, a hair wider, cut off flat on top
  const band=(v0,v1,grow)=>{ const S=new THREE.Shape(); S.moveTo(2.15+grow,v0); S.lineTo(2.15+grow,v1); S.lineTo(-2.32-grow,v1); S.lineTo(-2.32-grow,v0);
    if(v0<0.6){ S.lineTo(-2.0-grow,v0); S.absarc(-1.45,0.48,0.55-0.015,Math.PI,0,true); S.lineTo(0.8,v0); S.absarc(1.35,0.48,0.55-0.015,Math.PI,0,true); } S.lineTo(2.15+grow,v0);
    const g=new THREE.ExtrudeGeometry(S,{depth:W+0.12+grow*2,bevelEnabled:false,curveSegments:10}); g.rotateY(-Math.PI/2); g.translate((W+0.12+grow*2)/2,0,0); return g; };
  return {body,skirt:band(0.43,1.22,0.008),stripe:band(1.22,1.31,0.012)}; }
function makeVan(x,y,z,yaw){ if(!_vanMats) _vanMats={white:new THREE.MeshPhongMaterial({color:0xf3f5f8,shininess:70,specular:0x555555}),blue:new THREE.MeshPhongMaterial({color:0x1f5fd8,shininess:80,specular:0x666666}),orange:new THREE.MeshPhongMaterial({color:0xff7a1a,shininess:50}),
    dark:new THREE.MeshPhongMaterial({color:0x22262d,shininess:30}),glass:new THREE.MeshPhongMaterial({color:0x1d3048,shininess:140,specular:0xbfd8ff}),glass2:new THREE.MeshPhongMaterial({color:0x1d3048,shininess:140,specular:0xbfd8ff,side:THREE.DoubleSide}),rub:new THREE.MeshLambertMaterial({color:0x18191c}),metal:new THREE.MeshPhongMaterial({color:0xb8bec6,shininess:90,specular:0x888888}),
    lamp:new THREE.MeshBasicMaterial({color:0x9fe0ff}),head:new THREE.MeshBasicMaterial({color:0xfff6d8}),tail:new THREE.MeshBasicMaterial({color:0xd01818}),amber:new THREE.MeshBasicMaterial({color:0xffa31a}),liner:new THREE.MeshLambertMaterial({color:0x111214,side:THREE.BackSide})};
  if(!_vanMats.geo) _vanMats.geo=vanBodyGeo();
  const M=_vanMats, G=M.geo, g=new THREE.Group(), add=(geo,mat,px,py,pz,rx=0,ry=0,rz=0)=>{ const m=new THREE.Mesh(geo,mat); m.position.set(px,py,pz); m.rotation.set(rx,ry,rz); m.castShadow=m.receiveShadow=true; g.add(m); return m; };
  const B=(w,h,d)=>new THREE.BoxGeometry(w,h,d), X=1.09; // X: just outside the body's sides
  add(G.body,M.white,0,0,0); add(G.skirt,M.blue,0,0,0); add(G.stripe,M.orange,0,0,0);
  add(B(1.9,0.28,4.0),M.dark,0,0.5,0);                                                   // underside
  // glass: the windscreen along the slope, cab side windows, a small rear window in each back door
  { const ws=add(B(1.9,1.3,0.04),M.glass,0,2.07,-1.47,0.95,0,0); ws.castShadow=false; }
  for(const s of [-1,1]){ const sw=new THREE.Shape(); sw.moveTo(-1.08,1.6); sw.lineTo(-1.08,2.42); sw.lineTo(-1.2,2.42); sw.lineTo(-1.74,1.6); const gg=new THREE.ShapeGeometry(sw); gg.rotateY(-Math.PI/2); const m=add(gg,M.glass2,s*X,0,0); m.castShadow=false;
    add(B(0.02,0.82,0.03),M.dark,s*X,2.0,-1.02); }                                         // the door pillar
  for(const s of [-1,1]) add(B(0.62,0.44,0.03),M.glass,s*0.42,2.25,2.16);
  // doors: seams of the sliding side door (both sides) and the twin rear doors, with handles
  for(const s of [-1,1]){ for(const zz of [-0.7,0.55]) add(B(0.012,1.9,0.025),M.dark,s*(X+0.002),1.48,zz); add(B(0.012,0.03,1.25),M.dark,s*(X+0.002),2.42,-0.08); add(B(0.03,0.05,0.2),M.metal,s*(X+0.02),1.45,0.38); }
  add(B(0.025,2.2,0.012),M.dark,0,1.6,2.165); for(const s of [-1,1]) add(B(0.04,0.22,0.05),M.metal,s*0.14,1.45,2.18);
  // front: grille, bumper, headlights, indicators; back: bumper, tail lights; mirrors on stalks
  add(B(1.3,0.42,0.05),M.dark,0,0.95,-2.3); for(let k=0;k<4;k++) add(B(1.2,0.03,0.06),M.metal,0,0.8+k*0.1,-2.31);
  add(B(2.16,0.24,0.2),M.dark,0,0.58,-2.3); add(B(2.16,0.2,0.18),M.dark,0,0.56,2.2);
  for(const s of [-1,1]){ add(B(0.36,0.2,0.05),M.head,s*0.82,1.06,-2.31); add(B(0.12,0.12,0.05),M.amber,s*0.98,0.82,-2.31); add(B(0.12,0.4,0.05),M.tail,s*0.94,1.0,2.18);
    add(B(0.3,0.04,0.04),M.dark,s*1.22,2.0,-1.12); add(B(0.05,0.32,0.18),M.dark,s*1.38,2.02,-1.14); }
  // roof: a rack, the ladder up the back, the light bar, the dish on its mast
  for(const zz of [-0.3,0.6,1.5]) add(B(1.9,0.05,0.06),M.metal,0,2.94,zz); for(const s of [-1,1]) add(B(0.05,0.05,2.0),M.metal,s*0.92,2.98,0.6);
  for(const s of [-1,1]) add(B(0.04,2.3,0.04),M.metal,0.62+s*0.2,1.6,2.24); for(let k=0;k<7;k++) add(B(0.42,0.03,0.03),M.metal,0.62,0.7+k*0.32,2.24);
  add(new THREE.CylinderGeometry(0.05,0.05,0.7,8),M.metal,0.4,3.2,0.9);
  // the dish: a bowl turned up to the sky (open side up), with the feed arm reaching out of its middle
  const dish=new THREE.Group(); dish.position.set(0.4,3.58,0.9); g.add(dish); { const tilt=new THREE.Group(); tilt.rotation.x=-0.75; dish.add(tilt);
    const bowl=new THREE.Mesh(new THREE.SphereGeometry(0.62,22,10,0,Math.PI*2,Math.PI*0.62,Math.PI*0.38),_vanMats.dishM||(_vanMats.dishM=new THREE.MeshPhongMaterial({color:0xf3f5f8,shininess:60,specular:0x555555,side:THREE.DoubleSide}))); bowl.position.y=0.55; bowl.castShadow=true; tilt.add(bowl);
    const arm=new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.025,0.55,6),M.metal); arm.position.y=0.27; tilt.add(arm); const feed=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.04,0.12,8),M.dark); feed.position.y=0.56; tilt.add(feed); }
  add(B(1.25,0.1,0.3),M.dark,0,2.93,-0.62); const beacon=add(B(1.1,0.14,0.24),M.lamp,0,3.03,-0.62); beacon.castShadow=false;
  // wheels: tyre, rim and hub, in dark arch liners
  for(const [wz] of [[-1.45],[1.35]]){ const lin=add(new THREE.CylinderGeometry(0.56,0.56,2.0,20,1,true,-Math.PI/2,Math.PI).rotateZ(Math.PI/2),M.liner,0,0.48,wz); lin.castShadow=false;
    for(const s of [-1,1]){ add(new THREE.CylinderGeometry(0.47,0.47,0.3,22).rotateZ(Math.PI/2),M.rub,s*0.9,0.47,wz); add(new THREE.CylinderGeometry(0.28,0.28,0.32,16).rotateZ(Math.PI/2),M.metal,s*0.9,0.47,wz); add(new THREE.CylinderGeometry(0.09,0.09,0.34,10).rotateZ(Math.PI/2),M.dark,s*0.9,0.47,wz); } }
  // the terminal on the kerb side: a recessed panel, a live screen, a handle each side
  const term=new THREE.Group(); term.position.set(X,1.62,0.55); g.add(term);
  const panel=new THREE.Mesh(B(0.08,1.0,1.56),M.dark); term.add(panel); for(const s of [-1,1]){ const h=new THREE.Mesh(B(0.08,0.5,0.05),M.metal); h.position.set(0.06,-0.05,s*0.86); term.add(h); }
  const cv=document.createElement('canvas'); cv.width=256; cv.height=128; const tex=new THREE.CanvasTexture(cv); const scr=new THREE.Mesh(new THREE.PlaneGeometry(1.36,0.68),new THREE.MeshBasicMaterial({map:tex})); scr.rotation.y=Math.PI/2; scr.position.x=0.045; scr.position.y=0.06; term.add(scr);
  { const cv2=document.createElement('canvas'); cv2.width=512; cv2.height=128; const q=cv2.getContext('2d'); q.clearRect(0,0,512,128);
    q.save(); q.translate(64,60); q.lineWidth=11; q.strokeStyle='#fff'; q.beginPath(); q.arc(0,0,34,0.5,5.6); q.stroke(); q.fillStyle='#fff'; q.beginPath(); q.moveTo(34*Math.cos(5.6)+16,34*Math.sin(5.6)-2); q.lineTo(34*Math.cos(5.6)-12,34*Math.sin(5.6)-18); q.lineTo(34*Math.cos(5.6)-8,34*Math.sin(5.6)+16); q.fill(); q.restore();
    q.fillStyle='#fff'; q.font='900 italic 74px "Arial Black",Arial,sans-serif'; q.textBaseline='middle'; q.fillText('REBOOT',128,62);
    const sign=new THREE.Mesh(new THREE.PlaneGeometry(2.3,0.58),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(cv2),transparent:true})); sign.rotation.y=-Math.PI/2; sign.position.set(-X-0.005,0.86,0.45); g.add(sign); }
  const pad=new THREE.Mesh(new THREE.RingGeometry(0.55,0.72,40).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:0x7fc8ff,transparent:true,opacity:0.35,blending:THREE.AdditiveBlending,depthWrite:false,fog:false})); pad.position.set(1.75,0.09,0.55); g.add(pad);
  const holo=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.7,0.03),new THREE.MeshBasicMaterial({color:0x9fd8ff,transparent:true,opacity:0.75,blending:THREE.AdditiveBlending,depthWrite:false,fog:false})); holo.position.set(0,3.75,-0.62); holo.visible=false; g.add(holo);
  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);
  const flare=new THREE.Mesh(new THREE.CylinderGeometry(0.55,0.55,46,20,1,true).translate(0,23,0),new THREE.MeshBasicMaterial({color:0x7fc8ff,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide,fog:false})); flare.position.y=2.9; flare.visible=false; g.add(flare);
  const c=Math.round(Math.cos(yaw)), s_=Math.round(Math.sin(yaw)), hx=Math.abs(c)*1.1+Math.abs(s_)*2.3, hz=Math.abs(s_)*1.1+Math.abs(c)*2.3;
  const tx=x+c*1.75, tz=z-s_*1.75;
  const v={x,y,z,yaw,g,scr,scrCv:cv,scrTex:tex,scrKey:'',beacon,flare,dish,pad,holo,cd:0,prog:0,req:0,flash:0,tx,tz,solid:{boxes:[[x-hx,y,z-hz,x+hx,y+2.9,z+hz]],key:'van'+Math.round(x)+'_'+Math.round(z),isVan:true}};
  vanDrawScreen(v,0); return v; }
// the terminal: READY with a pulsing ring, CHARGING with the seconds left, or a bar filling while you reboot
function vanDrawScreen(v,now){ const ready=now>=v.cd, left=Math.ceil(Math.max(0,v.cd-now)/1000), pr=v.prog>0?Math.round(v.prog*40):0, key=(ready?'r':'c'+left)+'/'+pr; if(key===v.scrKey) return; v.scrKey=key;
  const g=v.scrCv.getContext('2d'), gr=g.createLinearGradient(0,0,0,128); gr.addColorStop(0,ready?'#1c5cff':'#3a3f4a'); gr.addColorStop(1,ready?'#0a1f6a':'#1a1d24'); g.fillStyle=gr; g.fillRect(0,0,256,128);
  g.strokeStyle=ready?'#9fe0ff':'#8a8f99'; g.lineWidth=4; g.strokeRect(6,6,244,116);
  g.save(); g.translate(50,58); g.lineWidth=7; g.strokeStyle='#fff'; g.beginPath(); g.arc(0,0,24,0.5,5.6); g.stroke(); g.fillStyle='#fff'; g.beginPath(); g.moveTo(24*Math.cos(5.6)+11,24*Math.sin(5.6)-2); g.lineTo(24*Math.cos(5.6)-8,24*Math.sin(5.6)-13); g.lineTo(24*Math.cos(5.6)-6,24*Math.sin(5.6)+11); g.fill(); g.restore();
  g.fillStyle='#fff'; g.textAlign='left'; g.textBaseline='middle'; g.font='900 italic 30px "Arial Black",Arial,sans-serif';
  if(pr){ g.fillText('REBOOTING',88,46); g.fillStyle='rgba(255,255,255,.2)'; g.fillRect(88,74,146,18); g.fillStyle='#9fe0ff'; g.fillRect(88,74,146*pr/40,18); }
  else if(ready){ g.fillText('READY',88,50); g.font='700 16px Arial,sans-serif'; g.fillStyle='#cfe6ff'; g.fillText('Hold to reboot',90,86); }
  else { g.fillText('CHARGING',88,50); g.font='700 18px Arial,sans-serif'; g.fillStyle='#d6d9e0'; g.fillText(left+'s',90,86); }
  v.scrTex.needsUpdate=true; }
"""+s[b:]
# the screen now draws itself; no more swapping two fixed materials
rep("""    const ready=now>=v.cd; if(v.scr.material!==(ready?_vanMats.ready:_vanMats.wait)) v.scr.material=ready?_vanMats.ready:_vanMats.wait;""",
    """    const ready=now>=v.cd; if(Math.hypot(v.x-P.pos.x,v.z-P.pos.z)<70) vanDrawScreen(v,now);""")
# the marker to the nearest ready van while you carry a card
s=s.replace("</style>","""
#vanMark{position:fixed;left:0;top:0;z-index:6;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:2px;transform:translate(-50%,-100%);color:#fff;font:900 italic 14px/1 var(--font-hud);text-shadow:0 1px 3px #000;letter-spacing:.04em}
#vanMark i{display:block;width:30px;height:30px;border-radius:50%;background:#1f5fd8 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 12a6 6 0 1 1-1.8-4.3' fill='none' stroke='%23fff' stroke-width='2.6' stroke-linecap='round'/%3E%3Cpath d='M17.5 3.5v4.5H13' fill='none' stroke='%23fff' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/62% no-repeat;border:2px solid #fff;box-shadow:0 0 12px rgba(80,170,255,.8)}
#vanMark.edge i{opacity:.85}
</style>""",1)
rep("""<div id="invitePop" hidden>""","""<div id="vanMark" hidden><i></i><span id="vanMarkD"></span></div>
<div id="invitePop" hidden>""")
rep("""  // you, carrying
  const ce=$('rbCarry');""","""  vanMarker(now);
  // you, carrying
  const ce=$('rbCarry');""")
rep("""// waiting for a reboot: watch a teammate""","""const _vmV=new THREE.Vector3();
function vanMarker(now){ const el=$('vanMark'); if(!RB.carry.size||isDead()||!VANS||!VANS.length||!playing){ if(!el.hidden) el.hidden=true; return; }
  let v=null, bd=1e9; for(const q of VANS){ const d=Math.hypot(q.x-P.pos.x,q.z-P.pos.z)+(now>=q.cd?0:400); if(d<bd){ bd=d; v=q; } } if(!v){ el.hidden=true; return; }
  const d=Math.hypot(v.x-P.pos.x,v.z-P.pos.z); if(d<6){ el.hidden=true; return; }
  _vmV.set(v.x,v.y+4.4,v.z).project(camera); const W=innerWidth, H=innerHeight; let x=(_vmV.x+1)/2*W, y=(1-_vmV.y)/2*H; const behind=_vmV.z>1;
  if(behind){ x=W-x; y=H-40; } const m=40, edge=behind||x<m||x>W-m||y<m+30||y>H-m; x=Math.max(m,Math.min(W-m,x)); y=Math.max(m+30,Math.min(H-m,y));
  el.hidden=false; el.classList.toggle('edge',edge); el.style.left=x.toFixed(0)+'px'; el.style.top=y.toFixed(0)+'px'; const t=Math.round(d)+' m'+(now>=v.cd?'':' · charging'); if($('vanMarkD').textContent!==t) $('vanMarkD').textContent=t; }
// waiting for a reboot: watch a teammate""")

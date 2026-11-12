# patch178: the full map zooms and pans smoothly (it eases toward where you scroll or pinch, every frame, and draws from
# a picture sized to the zoom, so it never jumps or crawls), and you can mark a spot: click (or tap) the map to drop a
# pin; click it again (or right-click) to take it away. The pin shows on the full map, the minimap, the compass and in
# the world as a tall beam with its distance, and in a party everyone sees everyone's pins in their own colours.
rep("""const mapView={zoom:1,cx:0,cz:0,ptrs:new Map(),moved:0,pinch:0};""","""const mapView={zoom:1,cx:0,cz:0,tz:1,tcx:0,tcz:0,ptrs:new Map(),moved:0,pinch:0};
// the picture at a few sizes (each half the last), so zoomed out it's drawn from a small one: quick and not grainy
function mapLevels(){ if(!bigMapImg) return []; if(bigMapImg.lv) return bigMapImg.lv; const lv=[bigMapImg]; let src=bigMapImg;
  while(src.width>1024){ const c=document.createElement('canvas'); c.width=c.height=src.width/2; const g=c.getContext('2d'); g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high'; g.drawImage(src,0,0,c.width,c.height); lv.push(c); src=c; }
  return bigMapImg.lv=lv; }
function mapClampT(){ mapView.tz=Math.max(1,Math.min(bigMapImg&&bigMapImg.width>=4096?8:5,mapView.tz)); const lim=WHALF*(1-1/mapView.tz); mapView.tcx=Math.max(-lim,Math.min(lim,mapView.tcx)); mapView.tcz=Math.max(-lim,Math.min(lim,mapView.tcz)); }
// ease the view toward where it's headed (zoom in log space, so in and out feel the same)
function stepMapView(dt){ const k=1-Math.exp(-Math.min(0.1,dt||0.016)*14), z0=Math.log(mapView.zoom), z1=Math.log(mapView.tz);
  mapView.zoom=Math.exp(z0+(z1-z0)*k); mapView.cx+=(mapView.tcx-mapView.cx)*k; mapView.cz+=(mapView.tcz-mapView.cz)*k;
  if(Math.abs(z1-z0)<0.0005){ mapView.zoom=mapView.tz; } if(Math.abs(mapView.tcx-mapView.cx)<0.05) mapView.cx=mapView.tcx; if(Math.abs(mapView.tcz-mapView.cz)<0.05) mapView.cz=mapView.tcz; mapClamp(); }""")
rep("""function mapZoomAt(f,clientX,clientY){ const cv=$('bigmapC'), r=cv.getBoundingClientRect(), u=(clientX-r.left)/r.width-0.5, v=(clientY-r.top)/r.height-0.5, half=WHALF/mapView.zoom;
  const wx=mapView.cx+u*2*half, wz=mapView.cz+v*2*half; mapView.zoom*=f; mapClamp(); const h2=WHALF/mapView.zoom; mapView.cx=wx-u*2*h2; mapView.cz=wz-v*2*h2; mapClamp(); drawBigMap(); }""",
    """function mapZoomAt(f,clientX,clientY){ const cv=$('bigmapC'), r=cv.getBoundingClientRect(), u=(clientX-r.left)/r.width-0.5, v=(clientY-r.top)/r.height-0.5, half=WHALF/mapView.tz;
  const wx=mapView.tcx+u*2*half, wz=mapView.tcz+v*2*half; mapView.tz*=f; mapClampT(); const h2=WHALF/mapView.tz; mapView.tcx=wx-u*2*h2; mapView.tcz=wz-v*2*h2; mapClampT(); } // (where you point stays put; the view eases there)""")
rep("""  const m=2*WHALF/mapView.zoom; mapView.cx-=dx/r.width*m; mapView.cz-=dy/r.height*m; mapClamp(); drawBigMap(); });""",
    """  const m=2*WHALF/mapView.zoom; mapView.cx-=dx/r.width*m; mapView.cz-=dy/r.height*m; mapClamp(); mapView.tcx=mapView.cx; mapView.tcz=mapView.cz; mapClampT(); drawBigMap(); });""")
rep("""  if(mapOpen) drawBigMap();
}""","""  if(mapOpen){ stepMapView(lastDt); drawBigMap(); }
  stepMarks();
}""")
rep("""  const g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true; const Z0=mapView.zoom, half=WHALF/Z0, ppm=bigMapImg.width/(2*WHALF);
  g.drawImage(bigMapImg,(mapView.cx-half+WHALF)*ppm,(mapView.cz-half+WHALF)*ppm,2*half*ppm,2*half*ppm,0,0,S,S);""",
    """  const g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high'; const Z0=mapView.zoom, half=WHALF/Z0;
  { const LV=mapLevels(); let L=0; while(L<LV.length-1&&2*half*LV[L+1].width/(2*WHALF)>=S*0.95) L++; const img=LV[L], ppm=img.width/(2*WHALF);
    g.fillStyle='#22405a'; g.fillRect(0,0,S,S); g.drawImage(img,(mapView.cx-half+WHALF)*ppm,(mapView.cz-half+WHALF)*ppm,2*half*ppm,2*half*ppm,0,0,S,S); }""")
# opening the map starts the view where it was left (targets and all)
rep("""  if(mapOpen&&!bigMapImg) bigMapImg=renderBigMapImage();""","""  if(mapOpen&&!bigMapImg) bigMapImg=renderBigMapImage(); if(mapOpen){ mapView.tz=mapView.zoom; mapView.tcx=mapView.cx; mapView.tcz=mapView.cz; }""")
# ---- pins
rep("""const mapUp=e=>{ if(!mapView.ptrs.has(e.pointerId)) return; mapView.ptrs.delete(e.pointerId); mapView.pinch=0; if(isTouch&&mapView.ptrs.size===0&&mapView.moved<6) toggleMap(false); }; // a tap (no drag) closes it""",
    """const mapUp=e=>{ if(!mapView.ptrs.has(e.pointerId)) return; const was=mapView.ptrs.size; mapView.ptrs.delete(e.pointerId); mapView.pinch=0;
  if(was===1&&mapView.moved<6){ const r=$('bigmapC').getBoundingClientRect(), half=WHALF/mapView.zoom, u=(e.clientX-r.left)/r.width-0.5, v=(e.clientY-r.top)/r.height-0.5, x=SPAWN[0]+mapView.cx+u*2*half, z=SPAWN[2]+mapView.cz+v*2*half;
    const me=MARKS.get(markId()), near=me&&Math.hypot(me.x-x,me.z-z)<14/(r.width/(2*half));
    if(e.button===2||near) setMark(null); else setMark(x,z); drawBigMap(); } }; // a click (no drag) drops your pin; on it, or a right-click, takes it away
$('bigmapC').addEventListener('contextmenu',e=>e.preventDefault());""")
rep("""function drawBigMap(){""","""/* ---------- pins on the map ----------
   One pin each: yours, and in a party everyone else's in their colour. Drawn on the full map, the minimap and the
   compass, and stood up in the world as a tall beam you can see from afar with how far it is. */
const MARKS=new Map(), markGeo=new THREE.CylinderGeometry(0.35,0.35,90,10,1,true);
function markId(){ return net.role?net.id:'me'; }
function markCol(id){ return '#'+(id==='me'||id===net.id?0xffd23f:colorFor(id)).toString(16).padStart(6,'0'); }
function setMark(x,z,id,quiet){ id=id||markId(); const old=MARKS.get(id); if(old){ scene.remove(old.beam); old.tag.remove(); MARKS.delete(id); }
  if(x!=null){ const col=markCol(id), m=new THREE.Mesh(markGeo,new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:0.42,blending:THREE.AdditiveBlending,depthWrite:false,fog:false}));
    m.position.set(x,terrainH(x,z)+45,z); m.renderOrder=5; scene.add(m);
    const tag=document.createElement('div'); tag.className='mtag'; tag.innerHTML='<i></i><b></b>'; tag.style.setProperty('--mc',col); document.body.appendChild(tag);
    MARKS.set(id,{x,z,col,beam:m,tag}); if(!quiet) sfx('equip'); }
  if(!quiet&&id===markId()&&net.role) netSend({type:'mk',x:x==null?null:+x.toFixed(1),z:z==null?null:+z.toFixed(1)}); }
const _mv=new THREE.Vector3();
function stepMarks(){ if(!MARKS.size) return; const W=innerWidth, H=innerHeight, show=playing&&!mapOpen;
  MARKS.forEach(M=>{ M.beam.visible=playing; if(!show){ M.tag.hidden=true; return; } _mv.set(M.x,terrainH(M.x,M.z)+2.2,M.z).project(camera);
    let sx=(_mv.x*0.5+0.5)*W, sy=(-_mv.y*0.5+0.5)*H; const behind=_mv.z>1; if(behind){ sx=W-sx; sy=H-24; } sx=Math.max(24,Math.min(W-24,sx)); sy=Math.max(60,Math.min(H-24,sy));
    M.tag.hidden=false; M.tag.style.transform=`translate(${sx}px,${sy}px)`; const d=Math.hypot(M.x-P.pos.x,M.z-P.pos.z); M.tag.lastChild.textContent=Math.round(d)+' m'; M.tag.style.opacity=d<6?0.4:1; }); }
function drawBigMap(){""")
rep("""  const dot=(x,z,col)=>{ g.fillStyle=col; g.strokeStyle='#fff'; g.lineWidth=1.6*u; g.beginPath(); g.arc(X(x),Z(z),5*u,0,7); g.fill(); g.stroke(); };""",
    """  MARKS.forEach(M=>{ const px=X(M.x), pz=Z(M.z), q=u, t=(performance.now()/1000)%1.2/1.2; if(px<-30||px>S+30||pz<-30||pz>S+30) return;
    g.strokeStyle=M.col; g.globalAlpha=1-t; g.lineWidth=2*q; g.beginPath(); g.ellipse(px,pz,(6+14*t)*q,(3+7*t)*q,0,0,7); g.stroke(); g.globalAlpha=1;
    g.fillStyle=M.col; g.strokeStyle='#14181f'; g.lineWidth=1.8*q; g.beginPath(); g.moveTo(px,pz); g.bezierCurveTo(px-9*q,pz-12*q,px-9*q,pz-24*q,px,pz-24*q); g.bezierCurveTo(px+9*q,pz-24*q,px+9*q,pz-12*q,px,pz); g.fill(); g.stroke();
    g.fillStyle='#14181f'; g.beginPath(); g.arc(px,pz-17*q,3.2*q,0,7); g.fill(); });
  const dot=(x,z,col)=>{ g.fillStyle=col; g.strokeStyle='#fff'; g.lineWidth=1.6*u; g.beginPath(); g.arc(X(x),Z(z),5*u,0,7); g.fill(); g.stroke(); };""")
rep("""  rbMiniMap(g,tx,tz,c,dpr); brMiniMap(g,tx,tz,sc,dpr);""","""  MARKS.forEach(M=>{ let px=tx(M.x), pz=tz(M.z); const dx=px-c, dz=pz-c, m=Math.hypot(dx,dz), lim=c-8*dpr; if(m>lim){ px=c+dx/m*lim; pz=c+dz/m*lim; }
    g.fillStyle=M.col; g.strokeStyle='#14181f'; g.lineWidth=1.3*dpr; const q=dpr*0.75; g.beginPath(); g.moveTo(px,pz+6*q); g.bezierCurveTo(px-7*q,pz-3*q,px-7*q,pz-12*q,px,pz-12*q); g.bezierCurveTo(px+7*q,pz-12*q,px+7*q,pz-3*q,px,pz+6*q); g.fill(); g.stroke(); });
  rbMiniMap(g,tx,tz,c,dpr); brMiniMap(g,tx,tz,sc,dpr);""")
rep("""function drawCompass(){ if(Math.abs(P.yaw-(drawCompass.y??1e9))<0.0015&&!(BR.on&&drawCompass.n++%10===0)) return;""","""function drawCompass(){ if(Math.abs(P.yaw-(drawCompass.y??1e9))<0.0015&&!(BR.on&&drawCompass.n++%10===0)&&!(MARKS.size&&drawCompass.n++%6===0)) return;""")
rep("""  g.fillStyle='#fff'; g.beginPath(); g.moveTo(W/2,24); g.lineTo(W/2-5,32); g.lineTo(W/2+5,32); g.fill();
  g.font='700 10px "Chakra Petch",sans-serif';""","""  MARKS.forEach(M=>{ const a=((Math.atan2(M.x-P.pos.x,-(M.z-P.pos.z))*180/Math.PI)%360+360)%360; let rel=((a-bear+540)%360)-180; rel=Math.max(-72,Math.min(72,rel)); const x=W/2+rel*pxPerDeg;
    g.fillStyle=M.col; g.strokeStyle='#14181f'; g.lineWidth=1.2; g.beginPath(); g.moveTo(x,21); g.bezierCurveTo(x-5,15,x-5,9,x,9); g.bezierCurveTo(x+5,9,x+5,15,x,21); g.fill(); g.stroke(); });
  g.fillStyle='#fff'; g.beginPath(); g.moveTo(W/2,24); g.lineTo(W/2-5,32); g.lineTo(W/2+5,32); g.fill();
  g.font='700 10px "Chakra Petch",sans-serif';""")
# the pin's tag in the world, and the hint
rep("""#bigmapC{width:100%;height:100%;display:block}""","""#bigmapC{width:100%;height:100%;display:block;cursor:crosshair}
.mtag{position:fixed;left:0;top:0;z-index:12;pointer-events:none;display:flex;flex-direction:column;align-items:center;margin:-34px 0 0 -12px;width:24px;filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}
.mtag i{width:18px;height:18px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--mc);border:2px solid #14181f}
.mtag b{font:800 12px "Chakra Petch",sans-serif;color:#fff;white-space:nowrap;margin-top:3px;text-shadow:0 1px 2px #000}""")
rep("""$('bigmapHint').textContent=isTouch?'Pinch to zoom · drag to move · tap to close':'Scroll to zoom · drag to move · '+codeName(settings.binds.map||'KeyM')+' or Close to exit';""",
    """$('bigmapHint').textContent=isTouch?'Pinch to zoom · drag to move · tap to drop a pin · Close to exit':'Scroll to zoom · drag to move · click to drop a pin (right-click removes it) · '+codeName(settings.binds.map||'KeyM')+' or Close to exit';""")
# party: share pins (the host passes them on)
rep("""function hostData(from,m){
  if(!m||typeof m!=='object') return; net.seen.set(from,performance.now());""","""function hostData(from,m){
  if(!m||typeof m!=='object') return; net.seen.set(from,performance.now());
  if(m.type==='mk'){ setMark(m.x,m.z,from,true); netSend({type:'mk',id:from,x:m.x,z:m.z},from); return; }""")
rep("""function clientData(m){
  if(!m||typeof m!=='object') return; net.hostSeen=performance.now();""","""function clientData(m){
  if(!m||typeof m!=='object') return; net.hostSeen=performance.now();
  if(m.type==='mk'){ setMark(m.x,m.z,m.id||'h',true); return; }""")

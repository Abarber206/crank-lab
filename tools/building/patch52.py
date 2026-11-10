# ---------- 52. the full map zooms (wheel or pinch) and pans (drag); zoomed in, it shows every house and garage as it really is ----------
rep("$('bigmap').addEventListener('pointerdown',e=>{ e.preventDefault(); e.stopPropagation(); toggleMap(false); });",r"""const mapView={zoom:1,cx:0,cz:0,ptrs:new Map(),moved:0,pinch:0};
function mapClamp(){ mapView.zoom=Math.max(1,Math.min(10,mapView.zoom)); const lim=WHALF*(1-1/mapView.zoom); mapView.cx=Math.max(-lim,Math.min(lim,mapView.cx)); mapView.cz=Math.max(-lim,Math.min(lim,mapView.cz)); }
function mapZoomAt(f,clientX,clientY){ const cv=$('bigmapC'), r=cv.getBoundingClientRect(), u=(clientX-r.left)/r.width-0.5, v=(clientY-r.top)/r.height-0.5, half=WHALF/mapView.zoom;
  const wx=mapView.cx+u*2*half, wz=mapView.cz+v*2*half; mapView.zoom*=f; mapClamp(); const h2=WHALF/mapView.zoom; mapView.cx=wx-u*2*h2; mapView.cz=wz-v*2*h2; mapClamp(); drawBigMap(); }
$('bigmapC').addEventListener('wheel',e=>{ e.preventDefault(); e.stopPropagation(); mapZoomAt(Math.exp(-e.deltaY*0.0015),e.clientX,e.clientY); },{passive:false});
$('bigmapC').addEventListener('pointerdown',e=>{ e.preventDefault(); e.stopPropagation(); mapView.ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY}); mapView.moved=0; if(mapView.ptrs.size===2){ const [a,b]=[...mapView.ptrs.values()]; mapView.pinch=Math.hypot(a.x-b.x,a.y-b.y); } try{ e.target.setPointerCapture(e.pointerId); }catch(_){} });
$('bigmapC').addEventListener('pointermove',e=>{ const p=mapView.ptrs.get(e.pointerId); if(!p) return; const r=$('bigmapC').getBoundingClientRect(), dx=e.clientX-p.x, dy=e.clientY-p.y; p.x=e.clientX; p.y=e.clientY; mapView.moved+=Math.abs(dx)+Math.abs(dy);
  if(mapView.ptrs.size===2){ const [a,b]=[...mapView.ptrs.values()], d=Math.hypot(a.x-b.x,a.y-b.y); if(mapView.pinch>0) mapZoomAt(d/mapView.pinch,(a.x+b.x)/2,(a.y+b.y)/2); mapView.pinch=d; return; }
  const m=2*WHALF/mapView.zoom; mapView.cx-=dx/r.width*m; mapView.cz-=dy/r.height*m; mapClamp(); drawBigMap(); });
const mapUp=e=>{ if(!mapView.ptrs.has(e.pointerId)) return; mapView.ptrs.delete(e.pointerId); mapView.pinch=0; if(mapView.ptrs.size===0&&mapView.moved<6) toggleMap(false); }; // a tap (no drag) closes it
$('bigmapC').addEventListener('pointerup',mapUp); $('bigmapC').addEventListener('pointercancel',mapUp);
$('bigmap').addEventListener('pointerdown',e=>{ if(e.target===$('bigmapC')||e.target===$('bigmapX')) return; e.preventDefault(); e.stopPropagation(); toggleMap(false); });""")
rep("  const g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true; g.drawImage(bigMapImg,0,0,S,S);\n  const k=S/(2*WHALF), X=x=>(x-SPAWN[0]+WHALF)*k, Z=z=>(z-SPAWN[2]+WHALF)*k, u=dpr*Math.max(0.8,Math.min(1.4,S/dpr/700));",
"""  const g=cv.getContext('2d'); g.setTransform(1,0,0,1,0,0); g.imageSmoothingEnabled=true; const Z0=mapView.zoom, half=WHALF/Z0, ppm=bigMapImg.width/(2*WHALF);
  g.drawImage(bigMapImg,(mapView.cx-half+WHALF)*ppm,(mapView.cz-half+WHALF)*ppm,2*half*ppm,2*half*ppm,0,0,S,S);
  const k=S/(2*half), X=x=>(x-SPAWN[0]-mapView.cx+half)*k, Z=z=>(z-SPAWN[2]-mapView.cz+half)*k, u=dpr*Math.max(0.8,Math.min(1.4,S/dpr/700));
  // zoomed in: the real houses and garages (roofs in their own colours), the sidewalks and paths
  if(Z0>=1.8){ const a=Math.min(1,(Z0-1.8)/1.2); g.globalAlpha=a;
    for(const t of TOWNS){ if(X(t.x)<-200||X(t.x)>S+200||Z(t.z)<-200||Z(t.z)>S+200) continue;
      g.strokeStyle='#c9c4b8'; g.lineWidth=WALK_W*k; g.lineCap='butt'; for(const [p,q] of SIDEWALKS){ if(Math.hypot(p[0]-t.x,p[1]-t.z)>t.R+20) continue; g.beginPath(); g.moveTo(X(p[0]),Z(p[1])); g.lineTo(X(q[0]),Z(q[1])); g.stroke(); }
      for(const h of t.houses){ const C=CELL, roof=h.roof==='brick'?['#b5583f','#a14b38','#c4694a','#8f4636'][h.skin.roof]:['#5f5a55','#6e655c','#4f4c49','#7a6f63'][h.skin.roof];
        g.fillStyle=roof; g.strokeStyle='rgba(20,14,8,.85)'; g.lineWidth=Math.max(1,0.25*k); g.fillRect(X(h.i0*C),Z(h.j0*C),h.w*C*k,h.d*C*k); g.strokeRect(X(h.i0*C),Z(h.j0*C),h.w*C*k,h.d*C*k);
        g.strokeStyle='rgba(255,255,255,.25)'; g.beginPath(); if(h.w>=h.d){ g.moveTo(X(h.i0*C),Z((h.j0+h.d/2)*C)); g.lineTo(X((h.i0+h.w)*C),Z((h.j0+h.d/2)*C)); } else { g.moveTo(X((h.i0+h.w/2)*C),Z(h.j0*C)); g.lineTo(X((h.i0+h.w/2)*C),Z((h.j0+h.d)*C)); } g.stroke(); // the ridge
        const G=h.garage; if(G){ g.fillStyle='#6b6f75'; g.fillRect(X(G.i*C),Z(G.j*C),C*k,C*k); g.strokeStyle='rgba(20,14,8,.85)'; g.strokeRect(X(G.i*C),Z(G.j*C),C*k,C*k); } } }
    g.globalAlpha=1; }""")
rep("  TOWNS.forEach(t=>{ const px=X(t.x), pz=Z(t.z), q=u;\n","  TOWNS.forEach(t=>{ const px=X(t.x), pz=Z(t.z), q=u; if(px<-60||px>S+60||pz<-60||pz>S+60) return; if(mapView.zoom>=2.4){ g.lineWidth=3.5*q; g.strokeStyle='rgba(0,0,0,.75)'; g.fillStyle='#fff'; g.strokeText(t.name,px,pz-4*q); g.fillText(t.name,px,pz-4*q); return; } // zoomed in, just the name over the real town\n")
rep("$('bigmapHint')","$('bigmapHint')") if "$('bigmapHint')" in s else None
s=s.replace('<p class="bmhint" id="bigmapHint">M or tap to close</p>','<p class="bmhint" id="bigmapHint">Scroll or pinch to zoom · drag to move · M or tap to close</p>')
rep("$('bigmapHint').textContent=isTouch?'Tap the map to close':codeName(settings.binds.map||'KeyM')+' or click to close';","$('bigmapHint').textContent=isTouch?'Pinch to zoom · drag to move · tap to close':'Scroll to zoom · drag to move · '+codeName(settings.binds.map||'KeyM')+' or click to close';")

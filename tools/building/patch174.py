# patch174: the map is a real picture of the island. The first time it's needed the world is photographed straight
# down (in four tiles, at midday, no fog, clouds or shadows, every tree and house showing), and the full map and the
# minimap both show that picture; names, players, the storm and your own builds still go on top. If the photograph
# can't be taken (no WebGL render target), the old painted map is used.
rep("""function renderBigMapImage(){
  const S=2048,""","""function renderIslandPhoto(){
  const big=!isTouch&&renderer.capabilities.maxTextureSize>=4096, S=big?4096:2048, TS=S/2, c=document.createElement('canvas'); c.width=c.height=S; const g=c.getContext('2d'), cx=SPAWN[0], cz=SPAWN[2];
  const hid=[], shown=[], hide=o=>{ if(o&&o.visible){ o.visible=false; hid.push(o); } }, show=o=>{ if(o&&!o.visible){ o.visible=true; shown.push(o); } };
  // nothing in the sky, nobody standing about: just the land
  hide(VCLOUD.sky); if(typeof clouds!=='undefined') clouds.forEach(cl=>hide(cl.m)); scene.children.forEach(o=>{ if(o.userData&&o.userData.noPhoto) hide(o); if(o.isSprite||o.isPoints) hide(o); });
  if(typeof localHero!=='undefined'&&localHero&&localHero.group) hide(localHero.group); net.players.forEach(pl=>{ if(pl.h&&pl.h.group) hide(pl.h.group); }); if(typeof STAGE_OBJS!=='undefined') STAGE_OBJS.forEach(hide);
  // the ground everywhere at middle detail, every house, every tree
  const made=[], lods=TERR.chunks.map(ch=>ch.m.map(m=>m&&m.visible)), blk=TERR.blocks.map(b=>b.m&&b.m.visible);
  for(const ch of TERR.chunks){ if(!ch.m[1]){ ch.m[1]=chunkMesh(ch,1); made.push(ch); } ch.m.forEach((m,l)=>{ if(m) m.visible=l===1; }); }
  TERR.blocks.forEach(b=>{ if(b.m) b.m.visible=false; });
  if(typeof townBatch!=='undefined') townBatch.forEach(bb=>bb.meshes.forEach(show));
  const camWas=camera.position.clone(), camhWas=CAMH;
  if(FOREST.near){ const cnt=new Map(), col=new THREE.Color(); // every standing tree, as its picture (crown from above)
    for(const p of FOREST.trees){ if(p.gone||!p.alive||p.g.parent) continue; const m=FOREST.mid[p.kind][p.id%8], i=cnt.get(m)||0; p.g.updateMatrix(); m.setMatrixAt(i,p.g.matrix); const t=p.tint||1; m.setColorAt(i,col.setRGB(t,t,t)); cnt.set(m,i+1); }
    for(const set of [FOREST.near,FOREST.mid,FOREST.far]) for(const kind in set) for(const m of set[kind]){ m.count=cnt.get(m)||0; m.instanceMatrix.needsUpdate=true; if(m.instanceColor) m.instanceColor.needsUpdate=true; show(m); } }
  const wu=WATER.mat&&WATER.mat.uniforms, reflWas=wu?[wu.reflK.value,wu.reflK2.value]:null; if(wu){ wu.photo.value=1; wu.reflK.value=0; wu.reflK2.value=0; }
  // midday, no fog, no shadows
  const todWas=TOD.fix, fogN=scene.fog&&scene.fog.near, fogF=scene.fog&&scene.fog.far; TOD.fix=0.3; stepSky(0); if(scene.fog){ scene.fog.near=0; } // (the fog's near is its density)
  const auto=renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate=false; renderer.shadowMap.needsUpdate=false;
  const prevRT=renderer.getRenderTarget(), prevC=renderer.getClearColor(new THREE.Color()), prevA=renderer.getClearAlpha();
  for(const L of [sun,sunFar]) if(L&&L.shadow&&L.shadow.map){ renderer.setRenderTarget(L.shadow.map); renderer.setClearColor(0xffffff,1); renderer.clear(); }
  const rt=new THREE.WebGLRenderTarget(TS,TS,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat}), buf=new Uint8Array(TS*TS*4), im=g.createImageData(TS,TS);
  const cam=new THREE.OrthographicCamera(-WHALF/2,WHALF/2,WHALF/2,-WHALF/2,1,3000); cam.up.set(0,0,-1);
  renderer.setClearColor(0x6fa7c8,1);
  try{ for(let ty=0;ty<2;ty++) for(let tx=0;tx<2;tx++){ const x=cx-WHALF/2+tx*WHALF, z=cz-WHALF/2+ty*WHALF; cam.position.set(x,1500,z); cam.lookAt(x,0,z); cam.updateMatrixWorld();
      renderer.setRenderTarget(rt); renderer.clear(); renderer.render(scene,cam); renderer.readRenderTargetPixels(rt,0,0,TS,TS,buf);
      for(let y=0;y<TS;y++) im.data.set(buf.subarray((TS-1-y)*TS*4,(TS-y)*TS*4),y*TS*4); for(let q=3;q<im.data.length;q+=4) im.data[q]=255; g.putImageData(im,tx*TS,ty*TS); } }
  finally{
    rt.dispose(); renderer.setRenderTarget(prevRT); renderer.setClearColor(prevC,prevA); renderer.shadowMap.autoUpdate=auto; renderer.shadowMap.needsUpdate=true;
    TOD.fix=todWas; stepSky(0); if(scene.fog){ scene.fog.near=fogN; scene.fog.far=fogF; }
    camera.position.copy(camWas); CAMH=camhWas; forestDirty=true; FOREST.t=0; stepForest(0); if(wu){ wu.photo.value=0; wu.reflK.value=reflWas[0]; wu.reflK2.value=reflWas[1]; }
    for(const ch of made){ scene.remove(ch.m[1]); ch.m[1].geometry.dispose(); ch.m[1]=null; }
    TERR.chunks.forEach((ch,i)=>ch.m.forEach((m,l)=>{ if(m) m.visible=!!lods[i][l]; })); TERR.blocks.forEach((b,i)=>{ if(b.m) b.m.visible=!!blk[i]; });
    hid.forEach(o=>o.visible=true); shown.forEach(o=>o.visible=false); }
  // the playable island bright, the ground beyond the edge a little dimmer
  const k=S/(2*WHALF); g.save(); g.beginPath(); g.rect(0,0,S,S); g.arc(S/2,S/2,MAP_R*k,0,Math.PI*2,true); g.fillStyle='rgba(10,20,30,.22)'; g.fill('evenodd'); g.restore();
  return c; }
function renderBigMapImage(){ try{ return renderIslandPhoto(); }catch(e){ console.warn('map photo unavailable, painting it instead',e); return renderBigMapPainted(); } }
function renderBigMapPainted(){
  const S=2048,""")
# the full map: no drawn houses or paths over the picture; it can zoom in as far as the picture holds up
i=s.index("  // zoomed in: the real houses and garages (roofs in their own colours), the sidewalks and paths\n  if(Z0>=1.8){"); j=s.index("    g.globalAlpha=1; }\n",i)+len("    g.globalAlpha=1; }\n")
s=s[:i]+s[j:]
rep("""function mapClamp(){ mapView.zoom=Math.max(1,Math.min(16,mapView.zoom));""","""function mapClamp(){ mapView.zoom=Math.max(1,Math.min(bigMapImg&&bigMapImg.width>=4096?8:5,mapView.zoom));""")
# the minimap: a window onto the same picture (your builds, chests, players and names still drawn on top)
i=s.index("  g.fillStyle='#3d6b3a'; g.fillRect(0,0,S,S);\n  const ox=P.pos.x, oz=P.pos.z, tx=x=>c+(x-ox)*sc, tz=z=>c+(z-oz)*sc;"); j=s.index("  near(ox,oz,Math.ceil(R/CELL)+1).forEach(p=>{ if(p.owner==='world') return;",i)
s=s[:i]+"""  g.fillStyle='#3d6b3a'; g.fillRect(0,0,S,S);
  const ox=P.pos.x, oz=P.pos.z, tx=x=>c+(x-ox)*sc, tz=z=>c+(z-oz)*sc;
  if(!bigMapImg) try{ bigMapImg=renderBigMapImage(); }catch(e){}
  if(bigMapImg){ const k=bigMapImg.width/(2*WHALF), x0=SPAWN[0]-WHALF, z0=SPAWN[2]-WHALF; g.imageSmoothingEnabled=true; g.imageSmoothingQuality='high'; g.drawImage(bigMapImg,(ox-R-x0)*k,(oz-R-z0)*k,2*R*k,2*R*k,0,0,S,S); }
"""+s[j:]
rep("""  propsNear(ox,oz,[],Math.ceil(R/PCELL)+1).forEach(p=>{ if(p.kind==='furn') return;""","""  if(!bigMapImg) propsNear(ox,oz,[],Math.ceil(R/PCELL)+1).forEach(p=>{ if(p.kind==='furn') return;""")
# the water's own distance haze can be switched off (for the photograph from high above)
rep("""        float fg=min(1.0-exp(-dist*0.0011),0.92);""","""        float fg=min(1.0-exp(-dist*0.0011),0.92)*(1.0-photo);""")
rep("""uniform float time, lum, reflK, reflY, reflK2, reflY2;""","""uniform float time, lum, reflK, reflY, reflK2, reflY2, photo;""")
rep("""    uniforms:{ nT:{value:nT},""","""    uniforms:{ photo:{value:0}, nT:{value:nT},""")
# no house icons for the towns on either map: the picture shows the town itself, and its name sits on it
for a in ["""g.fillStyle='#f6e7c6'; g.strokeStyle='#3a2a14'; g.lineWidth=1.2*dpr; g.beginPath(); g.moveTo(qx,qz-5*dpr); g.lineTo(qx+4*dpr,qz-1*dpr); g.lineTo(qx+3*dpr,qz-1*dpr); g.lineTo(qx+3*dpr,qz+3.5*dpr); g.lineTo(qx-3*dpr,qz+3.5*dpr); g.lineTo(qx-3*dpr,qz-1*dpr); g.lineTo(qx-4*dpr,qz-1*dpr); g.closePath(); g.fill(); g.stroke();""",
          """g.fillStyle='#f6e7c6'; g.strokeStyle='#3a2a14'; g.lineWidth=1.4*q; g.beginPath(); g.moveTo(px,pz-7*q); g.lineTo(px+6*q,pz-1.5*q); g.lineTo(px+4.5*q,pz-1.5*q); g.lineTo(px+4.5*q,pz+5*q); g.lineTo(px-4.5*q,pz+5*q); g.lineTo(px-4.5*q,pz-1.5*q); g.lineTo(px-6*q,pz-1.5*q); g.closePath(); g.fill(); g.stroke();"""]:
    assert s.count(a)==1,a[:60]; s=s.replace(a,'')
rep("""g.strokeText(t.name,qx,qz-7*dpr); g.fillText(t.name,qx,qz-7*dpr);""","""g.strokeText(t.name,qx,qz+4*dpr); g.fillText(t.name,qx,qz+4*dpr);""")
rep("""g.strokeText(t.name,px,pz-9*q); g.fillText(t.name,px,pz-9*q); });""","""g.strokeText(t.name,px,pz+6*q); g.fillText(t.name,px,pz+6*q); });""")

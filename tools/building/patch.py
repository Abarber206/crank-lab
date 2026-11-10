import re
F='/home/claude/crank-lab/index.html'
s=open(F).read()
def rep(a,b,c=1):
    global s
    assert s.count(a)==c,(s.count(a),a[:120]); s=s.replace(a,b)

# ---------- 1. world, towns, terrain, roads ----------
a=s.index('/* ---------- world: a big island of rolling hills around a flat build-fight field ---------- */')
b=s.index('/* ---------- grass, flowers and bushes ----------')
blk=open('/home/claude/mg/world_block.js').read().replace('@@GEN@@',open('/home/claude/mg/gen_embed.js').read().rstrip())
s=s[:a]+blk+'\n'+s[b:]

# ---------- 2. grass skips roads, rock and snow ----------
rep("    const dd=Math.hypot(x-SPAWN[0],z-SPAWN[2]); if(dd>MTN_R-4) continue;\n",
    "    const gc=worldCell(x,z); if(gc<0||WORLD.GRASS[gc]<110) continue; // no grass on roads, bare rock or snow\n")

# ---------- 3. bushes: ~1000 in 16 regional batches ----------
rep("// bushes: round, leafy, scattered in clumps across the island (decoration only: no collision)\nconst bushMesh=(()=>{",
    "// bushes: round, leafy, scattered in clumps across the island (decoration only: no collision)\nconst bushMeshes=(()=>{")
a=s.index("  const r=seeded(4242), spots=[];")
b=s.index("// instances span the island: never culled as one box\n")+len("// instances span the island: never culled as one box\n")
s=s[:a]+"""  const r=seeded(4242), spots=[], RB=MAP_R-15;
  for(let k=0;k<3000&&spots.length<1000;k++){ const u=(r()*2-1)*RB, v=(r()*2-1)*RB, n=1+Math.floor(r()*3); if(u*u+v*v>RB*RB||u*u+v*v<22*22) continue;
    for(let q=0;q<n;q++){ const x=SPAWN[0]+u+(r()-0.5)*4, z=SPAWN[2]+v+(r()-0.5)*4, s_=[x,z,0.7+r()*0.7,r()*6.28], c=worldCell(x,z);
      if(c<0||townAt(x,z,4)||roadDistAt(x,z)<6||WORLD.ROCK[c]>120||WORLD.SNOW[c]>40) continue; spots.push(s_); } }
  // 16 regional batches, each with its own bounding sphere, so the ones out of view aren't drawn
  const RG=4, cw=2*MAP_R/RG, groups=new Map(), mat=swayMaterial({vertexColors:true},0.05), out=[];
  spots.forEach((s_,i)=>{ const gi=Math.min(RG-1,Math.max(0,Math.floor((s_[0]-SPAWN[0]+MAP_R)/cw))), gj=Math.min(RG-1,Math.max(0,Math.floor((s_[1]-SPAWN[2]+MAP_R)/cw))), k=gj*RG+gi;
    let l=groups.get(k); if(!l){ l=[]; groups.set(k,l); } l.push([s_,i]); });
  groups.forEach(list=>{ const g2=new THREE.BufferGeometry(); for(const k in geo.attributes) g2.setAttribute(k,geo.attributes[k]); if(geo.index) g2.setIndex(geo.index); // shares the GPU buffers
    const m=new THREE.InstancedMesh(g2,mat,list.length), c=new THREE.Vector3(), lo=new THREE.Vector3(1e9,1e9,1e9), hi=new THREE.Vector3(-1e9,-1e9,-1e9);
    list.forEach(([s_,i],n)=>{ _gq.setFromAxisAngle(_gy,s_[3]); _gs.set(s_[2],s_[2]*(0.8+((i*37)%10)/40),s_[2]); _gp.set(s_[0],terrainH(s_[0],s_[1])-0.1,s_[1]); m.setMatrixAt(n,_gm.compose(_gp,_gq,_gs)); lo.min(_gp); hi.max(_gp); });
    c.addVectors(lo,hi).multiplyScalar(0.5); g2.boundingSphere=new THREE.Sphere(c,lo.distanceTo(hi)/2+2);
    m.receiveShadow=true; scene.add(m); out.push(m); });
  return out; })();
"""+s[b:]

# ---------- 4. clouds: higher, bigger, spread over the whole sky ----------
rep("  for(let k=0;k<22;k++){\n    // pile puffs","  for(let k=0;k<38;k++){\n    // pile puffs")
rep("const m=new THREE.Mesh(g,cloudMat), a=Math.random()*Math.PI*2, d=120+Math.random()*560;\n    m.position.set(SPAWN[0]+Math.cos(a)*d,170+Math.random()*90,SPAWN[2]+Math.sin(a)*d); m.rotation.y=Math.random()*Math.PI; m.scale.setScalar(1.3+Math.random()*1.0);",
    "const m=new THREE.Mesh(g,cloudMat), a=Math.random()*Math.PI*2, d=100+Math.sqrt(Math.random())*1400;\n    m.position.set(SPAWN[0]+Math.cos(a)*d,380+Math.random()*140,SPAWN[2]+Math.sin(a)*d); m.rotation.y=Math.random()*Math.PI; m.scale.setScalar(2.0+Math.random()*1.4);")
rep("float d=length(vW-cameraPosition); col=mix(col,haze,clamp((d-350.0)/900.0,0.0,0.45));","float d=length(vW-cameraPosition); col=mix(col,haze,clamp((d-600.0)/1800.0,0.0,0.5));")
rep("if(Math.hypot(dx,dz)>720) c.m.position.x=SPAWN[0]-Math.sign(dx)*Math.min(700,Math.sqrt(Math.max(0,720*720-dz*dz))-5); } }",
    "if(Math.hypot(dx,dz)>1600) c.m.position.x=SPAWN[0]-Math.sign(dx)*Math.min(1580,Math.sqrt(Math.max(0,1600*1600-dz*dz))-5); } }")

# ---------- 5. fog and camera ----------
rep("scene.fog=new THREE.Fog(HAZE,150,620); // distance fades into a pale horizon haze, like real air",
    "scene.fog=new THREE.Fog(HAZE,250,2600); // distance fades into a pale horizon haze, like real air")
rep("scene.fog.near=150-90*duskK; scene.fog.far=620-380*duskK;","scene.fog.near=250-190*duskK; scene.fog.far=2600-2360*duskK;")
rep("innerWidth/innerHeight, 0.08, 1100);","innerWidth/innerHeight, 0.08, 3200);")

# ---------- 6. props: shared geometry per variant ----------
a=s.index("function buildPropMesh(p,r){\n  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const s=p.s;\n  const q=seeded(p.id*7919+101); // shape details get their own stream, so the map layout doesn't shift\n")
b=s.index("  mergeProp(g,p.kind==='rock'); scene.add(g); return g;\n}\n")
body=s[a:b]
body=body.replace("function buildPropMesh(p,r){\n  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const s=p.s;\n  const q=seeded(p.id*7919+101); // shape details get their own stream, so the map layout doesn't shift\n",
"""// Props share their merged geometry: 8 shapes of each kind, every copy placed and sized by its own group. Keeps memory down.
const propGeos=new Map();
function propVariant(kind,variant){ const key=kind+variant; let v=propGeos.get(key); if(v) return v;
  const g=new THREE.Group(), s=1, p={kind}, q=seeded(variant*7919+101+['tree','pine','rock','car'].indexOf(kind)*104729);
""")
assert "{ const o5=(r(),r(),r(),r(),r()); if(o5<.5){ r(); r(); } } // keep the shared layout stream exactly as before\n" in body
body=body.replace("    { const o5=(r(),r(),r(),r(),r()); if(o5<.5){ r(); r(); } } // keep the shared layout stream exactly as before\n","")
assert "const body=[0xb5532f,0x4a7fae,0xc9a227,0x6d8f5a][Math.floor(r()*4)];" in body
body=body.replace("const body=[0xb5532f,0x4a7fae,0xc9a227,0x6d8f5a][Math.floor(r()*4)];","const body=[0xb5532f,0x4a7fae,0xc9a227,0x6d8f5a][variant%4];")
assert 'r()' not in body, 'layout stream still used in shapes'
s=s[:a]+body+"""  mergeProp(g,kind==='rock'); const m=g.children[0]; v={geo:m.geometry,mat:m.material}; propGeos.set(key,v); return v;
}
function buildPropMesh(p,r){
  const g=new THREE.Group(); g.position.set(p.x,0,p.z); g.rotation.y=r()*Math.PI*2; const v=propVariant(p.kind,p.id%8);
  const m=new THREE.Mesh(v.geo,v.mat); m.castShadow=m.receiveShadow=true; g.add(m); g.scale.setScalar(p.s); scene.add(g); return g;
}
"""+s[b+len("  mergeProp(g,p.kind==='rock'); scene.add(g); return g;\n}\n"):]
rep("function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true; p.g.scale.setScalar(0.01); propCullT=0; }",
    "function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true; p.g.scale.setScalar(p.s*0.01); propCullT=0; }")
rep("const k=Math.max(0.01,p.dying/0.35); p.g.scale.setScalar(k);","const k=Math.max(0.01,p.dying/0.35); p.g.scale.setScalar(p.s*k);")
rep("Math.sin(p.grow*Math.PI)*0.08:1; p.g.scale.setScalar(e); }","Math.sin(p.grow*Math.PI)*0.08:1; p.g.scale.setScalar(p.s*e); }")
rep("const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>200*200;","const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400;")
a=s.index("function initProps(){\n  const r=seeded(20261106);")
b=s.index("function propsNear(x,z,out,rad=1){")
s=s[:a]+"""function initProps(){
  /* About 520 trees, 520 pines (higher up), 220 rocks (on rocky ground) and 40 cars, 25 of them parked along the roads.
     They keep off the roads, the towns, bare rock (except the rocks) and snow. Seeded from integer maths, so every
     player in a party gets the same ones. */
  const r=seeded(20261108), RR=MAP_R-20, byKind={tree:[],pine:[],rock:[],car:[]}; let id=0, tries=0;
  const add=(kind,x,z,sc,yaw)=>{
    const p={id:id++,kind,x,z,s:sc,isProp:true,type:'prop',slab:false,alive:true,respawnT:0,wob:0,grow:1};
    p.key='prop'+p.id; p.mat=PROP_T[kind].mat; p.maxHp=Math.round(PROP_T[kind].hp*(kind==='rock'?p.s:1)); p.hp=p.maxHp;
    const e=kind==='car'?2:1; p.base=Math.min(terrainH(x,z),terrainH(x+e,z),terrainH(x-e,z),terrainH(x,z+e),terrainH(x,z-e));
    p.g=buildPropMesh(p,r); if(yaw!=null) p.g.rotation.y=yaw; p.g.position.y=p.base; p.g.traverse(m=>{ if(m.isMesh&&m.material!==inkMat) m.userData.piece=p; }); p.boxes=propBoxes(p);
    props.push(p); byKind[kind].push(p); const k=pkey(x,z); let set=propCells.get(k); if(!set){ set=new Set(); propCells.set(k,set); } set.add(p); return p; };
  const roomy=(x,z,kind)=>!propsNear(x,z,[],1).some(q=>Math.hypot(q.x-x,q.z-z)<(kind==='car'||q.kind==='car'?9:kind==='rock'||q.kind==='rock'?6:8));
  for(const [kind,n] of [['tree',520],['pine',520],['rock',220],['car',15]]){ let made=0;
    while(made<n&&tries<90000){ tries++;
      let x=SPAWN[0]+(r()*2-1)*RR, z=SPAWN[2]+(r()*2-1)*RR;
      // trees grow in clumps: most new trees start near an existing one, which makes little woods
      const own=byKind[kind]; if((kind==='tree'||kind==='pine')&&made>8&&r()<0.6){ const q=own[Math.floor(r()*own.length)]; x=q.x+(r()*2-1)*16; z=q.z+(r()*2-1)*16; }
      const u=x-SPAWN[0], v=z-SPAWN[2], d2=u*u+v*v; if(d2>RR*RR||d2<18*18) continue;
      const c=worldCell(x,z); if(c<0||WORLD.SNOW[c]>50||roadDistAt(x,z)<8||townAt(x,z,8)) continue;
      const rock=WORLD.ROCK[c], h=terrainH(x,z);
      if(kind==='rock'){ if(rock<90&&r()<0.8) continue; } else if(rock>120) continue;
      if(kind==='pine'&&h<24&&r()<0.8) continue;  // pines like it higher up
      if(kind==='tree'&&h>70&&r()<0.8) continue;  // broadleaf trees stay lower
      if(!roomy(x,z,kind)) continue;
      add(kind,x,z,kind==='rock'?.8+r()*.7:kind==='car'?1:kind==='pine'?1.45+r()*.7:1.35+r()*.6); made++; } } // big, tall trees
  // parked cars: on a road's shoulder, lined up with it
  const roads=WORLD.roads; let parked=0;
  for(let t=0;t<800&&parked<25&&roads.length;t++){ const rd=roads[Math.floor(r()*roads.length)], n=rd.pts.length; if(n<9) continue;
    const q=4+Math.floor(r()*(n-8)), a=rd.pts[q-3], b=rd.pts[q+3], side=r()<0.5?-1:1; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl;
    const x=SPAWN[0]+rd.pts[q][0]-tz*5.4*side, z=SPAWN[2]+rd.pts[q][1]+tx*5.4*side;
    if(rd.skip[q]||townAt(x,z,3)||roadDistAt(x,z)<4.8||Math.abs(terrainH(x,z)-rd.pts[q][2])>0.6||!roomy(x,z,'car')) continue;
    add('car',x,z,1,Math.atan2(-tz,tx)+(r()<0.5?Math.PI:0)); parked++; }
}
"""+s[b:]

# ---------- 7. wild chests ----------
rep("""  const r=seeded(99173); let made=0;
  for(let k=0;k<200&&made<14;k++){ const a=r()*Math.PI*2, d=60+r()*280, x=SPAWN[0]+Math.cos(a)*d, z=SPAWN[2]+Math.sin(a)*d;
    if(townAt(x,z,8)||Math.hypot(x-SPAWN[0],z-SPAWN[2])>MTN_R-25) continue; addChest(x,terrainH(x,z),z,r()*6.28); made++; }""",
"""  const r=seeded(99173), RC=MAP_R-30; let made=0;
  for(let k=0;k<3000&&made<35;k++){ const u=(r()*2-1)*RC, v=(r()*2-1)*RC, d2=u*u+v*v; if(d2<60*60||d2>RC*RC) continue;
    const x=SPAWN[0]+u, z=SPAWN[2]+v, c=worldCell(x,z);
    if(c<0||townAt(x,z,8)||roadDistAt(x,z)<7||WORLD.SNOW[c]>30||WORLD.ROCK[c]>150||chests.some(q=>Math.hypot(q.x-x,q.z-z)<70)) continue;
    addChest(x,terrainH(x,z),z,r()*6.28); made++; }""")

# ---------- 8. houses keep off the roads and the town square ----------
rep("""  const r=seeded(t.seed), L=Math.round(t.h/LVL), ci=Math.round(t.x/CELL), cj=Math.round(t.z/CELL), used=new Set(), out=[];
""","""  const r=seeded(t.seed), L=Math.round(t.h/LVL), ci=Math.round(t.x/CELL), cj=Math.round(t.z/CELL), used=new Set(), out=[];
  for(let a=-9;a<=9;a++) for(let b=-9;b<=9;b++){ const x=(ci+a+0.5)*CELL, z=(cj+b+0.5)*CELL; if(roadDistAt(x,z)<7.5||Math.hypot(x-t.x,z-t.z)<PLAZA_R+3) used.add((ci+a)+','+(cj+b)); }
""")

# ---------- 9. terrain detail follows the camera ----------
rep("  fitView(); updateCamera(); animateHero(dt); updateGhost(); updateHUD();\n  renderer.render(scene,camera);",
    "  fitView(); updateCamera(); stepTerrain(camera.position.x,camera.position.z); animateHero(dt); updateGhost(); updateHUD();\n  renderer.render(scene,camera);")

# ---------- 10. maps: roads on the minimap, full map overlay ----------
rep("""  for(let gz=Math.ceil((oz-R)/CELL)*CELL; gz<=oz+R; gz+=CELL){ g.beginPath(); g.moveTo(0,tz(gz)); g.lineTo(S,tz(gz)); g.stroke(); }
""","""  for(let gz=Math.ceil((oz-R)/CELL)*CELL; gz<=oz+R; gz+=CELL){ g.beginPath(); g.moveTo(0,tz(gz)); g.lineTo(S,tz(gz)); g.stroke(); }
  // roads and town squares
  g.lineCap='round'; g.lineJoin='round';
  for(const [w,col] of [[ROAD_HW*2+1,'#2f3236'],[ROAD_HW*2,'#575b61']]){ g.strokeStyle=col; g.lineWidth=w*sc;
    for(const rd of WORLD.roads){ const bx=rd.box; if(bx[2]<ox-R||bx[0]>ox+R||bx[3]<oz-R||bx[1]>oz+R) continue; g.beginPath(); let on=false;
      for(const p of rd.pts){ const x=SPAWN[0]+p[0], z=SPAWN[2]+p[1]; if(Math.abs(x-ox)<R+10&&Math.abs(z-oz)<R+10){ if(on) g.lineTo(tx(x),tz(z)); else { g.moveTo(tx(x),tz(z)); on=true; } } else on=false; }
      g.stroke(); }
    g.fillStyle=col; TOWNS.forEach(t=>{ if(Math.abs(t.x-ox)<R+10&&Math.abs(t.z-oz)<R+10){ g.beginPath(); g.arc(tx(t.x),tz(t.z),(PLAZA_R+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); } }); }
  g.lineCap='butt';
""")
a=s.index("(function(){\n  const root=document.documentElement, apply=()=>{ root.style.setProperty('--tbs',settings.btnSize);")
s=s[:a]+open('/home/claude/mg/bigmap.js').read()+s[a:]
rep("  miniT-=lastDt; if(miniT<=0){ miniT=1/15; drawMini(); }\n}","  miniT-=lastDt; if(miniT<=0){ miniT=1/15; drawMini(); }\n  if(mapOpen) drawBigMap();\n}")
rep("aim:'Mouse2',emote:'KeyB'};","aim:'Mouse2',emote:'KeyB',map:'KeyM'};")
rep("aim:'Aim down sights',emote:'Emote'};","aim:'Aim down sights',emote:'Emote',map:'Full map'};")
rep("  else if(a==='emote') startEmote(settings.emote);\n}","  else if(a==='emote') startEmote(settings.emote);\n  else if(a==='map') toggleMap();\n}")
rep("function openMenu(){ menu.hidden=false;","function openMenu(){ if(mapOpen) toggleMap(false); menu.hidden=false;")
rep('  <div class="mapwrap"><canvas id="mini"></canvas><span class="n">N</span></div>',
    '  <div class="mapwrap" id="miniWrap" title="Full map (M)"><canvas id="mini"></canvas><span class="n">N</span></div>')
rep('#mini{width:100%;height:100%;display:block}','''#mini{width:100%;height:100%;display:block}
#miniWrap{pointer-events:auto;cursor:pointer}
#bigmap{position:fixed;inset:0;z-index:30;display:grid;place-items:center;background:rgba(6,11,18,.78);padding:max(10px,env(safe-area-inset-top,0px)) max(10px,env(safe-area-inset-right,0px)) max(10px,env(safe-area-inset-bottom,0px)) max(10px,env(safe-area-inset-left,0px))}
#bigmap[hidden]{display:none}
#bigmapBox{position:relative;width:min(92vw,92vh);height:min(92vw,92vh);border-radius:14px;overflow:hidden;border:2px solid rgba(255,255,255,.85);box-shadow:0 10px 40px rgba(0,0,0,.55)}
#bigmapC{width:100%;height:100%;display:block}
#bigmapX{position:absolute;top:10px;right:10px;font:800 13px var(--font-hud,sans-serif);color:#fff;background:rgba(10,16,26,.72);border:1px solid rgba(255,255,255,.5);border-radius:999px;padding:6px 12px;cursor:pointer}
#bigmap .bmhint{position:absolute;left:12px;bottom:10px;margin:0;font:700 12px var(--font-hud,sans-serif);color:rgba(255,255,255,.85);text-shadow:0 1px 2px #000;pointer-events:none}''')
rep('<div class="hud" id="topR">','''<div id="bigmap" hidden><div id="bigmapBox"><canvas id="bigmapC"></canvas><button id="bigmapX" type="button">Close</button><p class="bmhint" id="bigmapHint">M or tap to close</p></div></div>
<div class="hud" id="topR">''')

# ---------- 11. houses dressed as houses, and farmable ----------
rep("    for(let tries=0;tries<14&&!ok;tries++){ const a=(k+r()*0.8)/n*Math.PI*2+tries*0.9, rad=9+r()*12; // around a little square in the middle",
    "    for(let tries=0;tries<40&&!ok;tries++){ const a=(k+r()*0.8)/n*Math.PI*2+tries*0.9, rad=12+r()*17; // around the town square")
rep("/* ---------- houses ----------\n", open('/home/claude/mg/house_skins.js').read()+"\n/* ---------- houses ----------\n")
rep("    out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length});",
    "    const rs=seeded(t.seed+977*(k+1)), style=HOUSE_STYLE[mat]; // looks come from their own stream, so the layout doesn't shift\n    out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length,skin:{style,paint:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});")
rep("      P_.push({type:'wall',axis,i,j,l,mask,mat}); };","      P_.push({type:'wall',axis,i,j,l,mask,mat,out:face==='w'||face==='n'?-1:1}); };")
rep("  return P_.map(q=>Object.assign(q,{key:q.type==='wall'?","  return P_.map(q=>Object.assign(q,{skin:h.skin,key:q.type==='wall'?")
rep("  const M=matFor[p.mat||'wood'], base=mat||(p.type==='wall'?M.wall:M.floor);","  const M=p.skin?houseSkin(p):matFor[p.mat||'wood'], base=mat||(p.type==='wall'?M.wall:M.floor);")
rep("    if(!mat) add(coneFrame(p.mask||0),0,0,0,0,0,M.beam); }",
    "    if(!mat&&!p.skin) add(coneFrame(p.mask||0),0,0,0,0,0,M.beam); // house roofs go without the build-piece frame\n    if(p.skin&&p.gable) p.gable.forEach(([side,out])=>{ const gg=gableGeo(p.mask||0,side,out); if(gg) add(gg,0,0,0,0,0,mat||housePlainMat(p.skin)); }); }")
rep("    P_.push({type:'cone',i:i0+a,j:j0+b,l:top,mask,mat:h.roof}); }",
    "    const gable=[]; if(a===0) gable.push(['w',-1]); if(a===w-1) gable.push(['e',1]); if(b===0) gable.push(['n',-1]); if(b===d-1) gable.push(['s',1]);\n    P_.push({type:'cone',i:i0+a,j:j0+b,l:top,mask,mat:h.roof,gable}); }")
rep("  if(p.type==='wall') add(wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);","  if(p.type==='wall') add(p.skin?houseWallGeo(p.axis,p.mask==null?511:p.mask,p.out||1):wallGeo(p.axis,p.mask==null?511:p.mask),0,0,0);")
rep("const parts=ms.map(m=>{ const g=m.geometry.index?m.geometry.toNonIndexed():m.geometry; n+=g.attributes.position.count; return [g,m.matrixWorld]; });",
    "const parts=ms.map(m=>{ const g=m.geometry.index?m.geometry.toNonIndexed():m.geometry; n+=g.attributes.position.count; return [g,m.matrixWorld]; }), hasIn=!!parts[0][0].attributes.inside, IN=hasIn?new Float32Array(n):null;")
rep("if(ua) U.set([ua.getX(i),ua.getY(i)],(o+i)*2); }","if(ua) U.set([ua.getX(i),ua.getY(i)],(o+i)*2); if(hasIn&&g.attributes.inside) IN[o+i]=g.attributes.inside.getX(i); }")
rep("out.setAttribute('uv',new THREE.BufferAttribute(U,2)); out.computeBoundingSphere(); return out; }","out.setAttribute('uv',new THREE.BufferAttribute(U,2)); if(hasIn) out.setAttribute('inside',new THREE.BufferAttribute(IN,1)); out.computeBoundingSphere(); return out; }")
rep("  if(hit){ const hp_=hit.object.userData.piece; dmgNum(hit.point,PICK_DMG,'build'); sfx('pick_hit'); damagePiece(hp_,PICK_DMG,hit.point); }",
    "  if(hit){ const hp_=hit.object.userData.piece; dmgNum(hit.point,PICK_DMG,'build'); sfx('pick_hit'); damagePiece(hp_,PICK_DMG,hit.point);\n    if(hp_&&hp_.owner==='world') giveMats(hp_.mat,Math.round(HOUSE_FARM[hp_.mat][0]+Math.random()*(HOUSE_FARM[hp_.mat][1]-HOUSE_FARM[hp_.mat][0])),hit.point); } // houses farm like the map does")
rep("const PROP_T={","const HOUSE_FARM={wood:[5,8],brick:[5,8],metal:[4,7]}; // materials per pickaxe hit on a house\nconst PROP_T={")

rep("  $('pieceHpT').textContent=MATERIALS[p.mat].name+' '+Math.ceil(p.hp)+' / '+p.maxHp;",
    "  $('pieceHpT').textContent=(p.skin?'House · farms '+MATERIALS[p.mat].name.toLowerCase():MATERIALS[p.mat].name)+' '+Math.ceil(p.hp)+' / '+p.maxHp;")
# ---------- 12. real staircases and sidewalks ----------
rep("/* ---------- houses ----------\n", open('/home/claude/mg/house_stairs.js').read()+"\n/* ---------- houses ----------\n")
rep("""  if(stair){ const dir=stair.i===i0?0:2; // rises toward the middle of the house, onto the upper floor
    P_.push({type:'ramp',i:stair.i,j:stair.j,l:L,dir,mat:'wood'});
    for(let a=0;a<w;a++) for(let b=0;b<d;b++) if(!(i0+a===stair.i&&j0+b===stair.j)) P_.push({type:'floor',i:i0+a,j:j0+b,l:L+1,mat:'wood'}); }""",
"""  if(stair){ // a real staircase up to the upper floor, under a stairwell cut into it
    const S=houseStair(h);
    for(let a=0;a<w;a++) for(let b=0;b<d;b++){ const i=i0+a, j=j0+b, m=S.masks[i+','+j], top=i===S.top[0]&&j===S.top[1];
      P_.push(Object.assign({type:'floor',i,j,l:L+1,mat:'wood'},m!=null?{mask:m}:{},top?{fix:S.rail}:{})); }
    const g=P_.find(q=>q.type==='floor'&&q.l===L&&q.i===S.top[0]&&q.j===S.top[1]); g.fix=S.stairs; }""")
rep("""  const stairI=h.floors>1?(h.side==='w'?i0+w-1:i0):-99, stairJ=h.floors>1?(h.side==='n'?j0+d-1:j0):-99;
  const cells=[]; for(let a=0;a<w;a++) for(let b=0;b<d;b++) if(!(i0+a===stairI&&j0+b===stairJ)) cells.push([i0+a,j0+b]);""",
"""  const sc=h.floors>1?houseStair(h).cells:[], onStair=(i,j)=>sc.some(c=>c[0]===i&&c[1]===j);
  const cells=[]; for(let a=0;a<w;a++) for(let b=0;b<d;b++) if(!onStair(i0+a,j0+b)) cells.push([i0+a,j0+b]);""")
rep("""  }
  return out;
}
const buildGlowMat""","""  }
  if(p.fix) out.push(...p.fix.boxes); // a house's staircase or stairwell railing
  return out;
}
const buildGlowMat""")
rep("    if(p.skin&&p.gable) p.gable.forEach(","    if(p.skin&&p.gable) p.gable.forEach(")
rep("""  if(p.type==='wall') add(p.skin?houseWallGeo""","""  if(p.fix&&p.skin&&!mat) p.fix.parts.forEach(([geo,k])=>add(geo,0,0,0,0,0,k==='inner'?housePlainMat(p.skin):M[k]));
  if(p.type==='wall') add(p.skin?houseWallGeo""")
rep("""      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } } batchTown(t); }
}""","""      const p=addPiece(Object.assign({},q,{owner:'world',instant:true})); p.town=t; if(q.mask!=null&&q.mask!==p.mask){ p.mask=q.mask; buildPiece(p); } } batchTown(t); }
  buildSidewalks();
}""")
rep("""    g.fillStyle=col; TOWNS.forEach(t=>{ if(Math.abs(t.x-ox)<R+10""","""    g.fillStyle=col; TOWNS.forEach(t=>{ if(Math.abs(t.x-ox)<R+10""")
rep("""  g.lineCap='butt';
""","""  g.strokeStyle='#c9c6be'; g.lineWidth=WALK_W*sc; // sidewalks
  for(const w of SIDEWALKS){ if(Math.abs(w[0][0]-ox)>R+30||Math.abs(w[0][1]-oz)>R+30) continue; g.beginPath(); w.forEach((p,k)=>k?g.lineTo(tx(p[0]),tz(p[1])):g.moveTo(tx(p[0]),tz(p[1]))); g.stroke(); }
  g.lineCap='butt';
""")
# ---------- 13. a frame never runs backwards in time (the first rAF timestamp can be earlier than the clock's start) ----------
rep("  const raw=now-last, dt=Math.min(0.05,raw/1000); last=now; lastDt=dt;","  const raw=Math.max(0,now-last), dt=Math.min(0.05,raw/1000); last=now; lastDt=dt;")
rep("  miniT-=lastDt; if(miniT<=0){ miniT=1/15; drawMini(); }","  miniT=Math.min(miniT,1/15)-lastDt; if(miniT<=0){ miniT=1/15; drawMini(); }")
# ---------- 14. draw-call trims: far towns and chests ----------
rep("const dx=c.x-P.pos.x, dz=c.z-P.pos.z, d=Math.hypot(dx,dz); if(d>90){ c.g.visible=d<200; continue; } c.g.visible=true;",
    "const dx=c.x-P.pos.x, dz=c.z-P.pos.z, d=Math.hypot(dx,dz); if(d>90){ c.g.visible=d<130; continue; } c.g.visible=true;")
rep("    for(const p of props){ const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400; p.g.visible=!far&&(p.alive||p.dying>0); } }",
    "    for(const p of props){ const far=(p.x-cx)*(p.x-cx)+(p.z-cz)*(p.z-cz)>400*400; p.g.visible=!far&&(p.alive||p.dying>0); }\n    townBatch.forEach((b,t)=>{ const on=Math.hypot(t.x-cx,t.z-cz)<700; b.meshes.forEach(m=>{ m.visible=on; }); }); } // far towns are a few pixels in the haze")
rep("n+=g.attributes.position.count; return [g,m.matrixWorld]; }),","n+=g.attributes.position.count; return [g,m.matrixWorld,m.material.color]; }),")
rep("  for(const [g,M] of parts){ const pa=g.attributes.position,","  for(const [g,M,PC] of parts){ const pa=g.attributes.position,")
# ---------- 15. town batches: one material per house style; each house's colour rides along per vertex ----------
rep("for(const m of p.group.children){ if(!m.isMesh) continue; let a=byMat.get(m.material); if(!a){ a=[]; byMat.set(m.material,a); } a.push(m); } }",
    "for(const m of p.group.children){ if(!m.isMesh) continue; const k=m.material.userData.batch||m.material; let a=byMat.get(k); if(!a){ a=[]; byMat.set(k,a); } a.push(m); } }")
rep("hasIn=!!parts[0][0].attributes.inside, IN=hasIn?new Float32Array(n):null;","hasIn=!!parts[0][0].attributes.inside, IN=hasIn?new Float32Array(n):null, hasPaint=!!ms[0].material.userData.batch, PA=hasPaint?new Float32Array(n*3):null;")
rep("if(hasIn&&g.attributes.inside) IN[o+i]=g.attributes.inside.getX(i); }","if(hasIn&&g.attributes.inside) IN[o+i]=g.attributes.inside.getX(i); if(hasPaint){ const c=PC; PA[(o+i)*3]=c.r; PA[(o+i)*3+1]=c.g; PA[(o+i)*3+2]=c.b; } }")
rep("if(hasIn) out.setAttribute('inside',new THREE.BufferAttribute(IN,1));","if(hasIn) out.setAttribute('inside',new THREE.BufferAttribute(IN,1)); if(hasPaint) out.setAttribute('paint',new THREE.BufferAttribute(PA,3));")
# ---------- 16. Austin's purple creature replaces the zombies ----------
a=s.index("function makeZombie(type){"); b=s.index("function newZombie(type,x,z,id){")
s=s[:a]+open('/home/claude/mg/creature.js').read()+s[b:]
rep("""const ZT={ // walkers, runners and brutes: pale, rotting, bloodied
  husk:  {name:'Walker',hp:110,spd:0.56,dmg:12,bld:16,sc:1,   skin:0x9ba1aa,shirt:0x6b5d4c,pants:0x3d4250,hair:0x2a221c,pts:1},
  runner:{name:'Runner',hp:70, spd:0.98,dmg:8, bld:10,sc:0.95,skin:0xb3a7ad,shirt:0x7a2f2f,pants:0x2e3340,hair:0x3a2a20,pts:1},
  brute: {name:'Brute', hp:520,spd:0.42,dmg:30,bld:55,sc:1.45,skin:0x857b88,shirt:0x000000,pants:0x3a3328,hair:0x1c1816,pts:3}
};""","""const ZT={ // the purple creatures: walkers, slim pale runners and huge deep-violet brutes
  husk:  {name:'Walker',hp:110,spd:0.56,dmg:12,bld:16,sc:1,   body:0x7b52a6,light:0xa47bd4,dark:0x24102f,wound:0x4a1a5c,core:0xc77dff,eye:0xe9b8ff,pts:1},
  runner:{name:'Runner',hp:70, spd:0.98,dmg:8, bld:10,sc:0.95,body:0x9673c2,light:0xbd9ae6,dark:0x2b1638,wound:0x53206a,core:0xd99bff,eye:0xf3d4ff,pts:1},
  brute: {name:'Brute', hp:520,spd:0.42,dmg:30,bld:55,sc:1.45,body:0x55327f,light:0x7a52a8,dark:0x1a0a24,wound:0x3d1250,core:0xb35cff,eye:0xffa0f0,pts:3}
};""")
rep("goreMat=new THREE.MeshLambertMaterial({color:0x5a1215})","goreMat=new THREE.MeshLambertMaterial({color:0x6a2c8c})") # purple ichor
# the hitbox follows the new body: taller, head higher and less far forward
rep("const hx=E.isZombie?-Math.sin(E.yaw)*0.22*k:0, hz=E.isZombie?-Math.cos(E.yaw)*0.22*k:0, hy=E.isZombie?1.5:(cr?1.2:1.66);",
    "const hx=E.isZombie?-Math.sin(E.yaw)*0.17*k:0, hz=E.isZombie?-Math.cos(E.yaw)*0.17*k:0, hy=E.isZombie?1.95:(cr?1.2:1.66);")
rep("const top=cr?1.0:E.isZombie?1.3:1.42;","const top=cr?1.0:E.isZombie?1.72:1.42;")
rep("dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.05:1.6)*who.sc)","dmgNum(who.pos.clone().setY(who.pos.y+(e.head?2.3:1.7)*who.sc)")
rep("  if(z.hitFlash>0){ z.hitFlash-=dt; g.position.x+=(Math.random()-.5)*0.06; }\n}",
    "  if(z.hitFlash>0){ z.hitFlash-=dt; g.position.x+=(Math.random()-.5)*0.06; }\n  if(R.crown){ const t=performance.now()*0.001+z.id*1.7; // the flame crown flickers\n    R.crown.scale.set(1+0.05*Math.sin(t*8.3),1+0.1*Math.sin(t*6.1)+0.05*Math.sin(t*13.7),1+0.05*Math.cos(t*7.7)); R.crown.rotation.z=0.06*Math.sin(t*3.1);\n    if(R.crownGlow) R.crownGlow.material.opacity=0.16+0.1*(0.5+0.5*Math.sin(t*11)); }\n}")
# ---------- 17. icons rendered from the real models ----------
rep("const iconOf=id=>ICONS[id]||(WEAPONS[id]?ICONS[WEAPONS[id].base]:'')||'';",
    open('/home/claude/mg/icons.js').read()+"""const iconOf=id=>{ if(!id) return ''; const u=ICON_IMG.get(iconKey(id));
  if(u) return `<image href="${u}" x="0" y="0" width="48" height="48"/>`;
  if(u===undefined&&(WEAPONS[id]||ITEMS[id]||AMMO_T[id])) queueIcons([id]);
  return ICONS[id]||(WEAPONS[id]?ICONS[WEAPONS[id].base]:'')||''; };""")
rep("""  else if(item==='bandage'){ const m=new THREE.Mesh(rbox(.34,.12,.24,.04),toon(0xf3e3c3)); m.position.y=.06; g.add(m); const x=new THREE.Mesh(rbox(.06,.125,.16,.01),toon(0xd9483b)); x.position.y=.07; g.add(x); }
  else if(item==='mini'){ const m=new THREE.Mesh(new THREE.CylinderGeometry(.07,.09,.22,12),toon(0x3fa9ff)); m.position.y=.11; g.add(m); }""",
"""  else if(item==='bandage'){ // a roll of bandage with a strip unwound, taped with a red cross
    const roll=new THREE.Mesh(new THREE.CylinderGeometry(.11,.11,.2,18),toon(0xf4ead6)); roll.rotation.z=Math.PI/2; roll.position.y=.11; g.add(roll);
    const core=new THREE.Mesh(new THREE.CylinderGeometry(.045,.045,.206,12),toon(0xcfc1a6)); core.rotation.z=Math.PI/2; core.position.y=.11; g.add(core);
    const strip=new THREE.Mesh(rbox(.19,.014,.3,.004),toon(0xefe3cc)); strip.position.set(0,.007,.2); g.add(strip);
    const x1=new THREE.Mesh(rbox(.05,.016,.15,.004),toon(0xd9483b)); x1.position.set(0,.016,.24); g.add(x1); const x2=x1.clone(); x2.rotation.y=Math.PI/2; g.add(x2); }
  else if(item==='mini'){ // a round flask of glowing blue shield, corked
    const body=new THREE.Mesh(new THREE.SphereGeometry(.11,18,14),toon(0x3fb0ff)); body.position.y=.12; g.add(body);
    const top=new THREE.Mesh(new THREE.SphereGeometry(.112,18,6,0,Math.PI*2,0,Math.PI*.3),toon(0xcdeeff)); top.position.y=.12; g.add(top);
    const shine=new THREE.Mesh(new THREE.SphereGeometry(.03,10,8),toon(0xffffff)); shine.position.set(-.05,.17,.07); g.add(shine);
    const neck=new THREE.Mesh(new THREE.CylinderGeometry(.035,.045,.08,12),toon(0xcdeeff)); neck.position.y=.25; g.add(neck);
    const cork=new THREE.Mesh(new THREE.CylinderGeometry(.042,.036,.055,10),toon(0x9a6a3a)); cork.position.y=.31; g.add(cork); }""")
rep("initProps(); props.forEach(p=>{","setTimeout(()=>queueIcons([...Object.keys(WEAPONS),...Object.keys(ITEMS),...Object.keys(AMMO_T)]),400); // icon pictures, a few a frame\ninitProps(); props.forEach(p=>{")
# ---------- 18. each creature gets its own wound layout; fall damage ----------
rep("sc:T.sc,alive:true,atkT:0.5+Math.random(),atk:0,walk:Math.random()*6,target:null,tT:0,chewT:0,stuckT:0,sideT:0,side:0,deadT:0,groanT:2+Math.random()*6,m:makeZombie(type)};",
    "sc:T.sc,alive:true,atkT:0.5+Math.random(),atk:0,walk:Math.random()*6,target:null,tT:0,chewT:0,stuckT:0,sideT:0,side:0,deadT:0,groanT:2+Math.random()*6,m:null};\n  z0.m=makeZombie(type,z0.id); // the id picks its wounds, the same on every screen")
rep("const zReach=z=>0.75*z.sc+0.45;",r"""/* Fall damage, like Fortnite: short drops are free; past FALL_SAFE metres you take damage that grows with the
   height, straight to health (shields don't soak it). A big enough drop eliminates you. */
const FALL_SAFE=10, FALL_PER=7;
function stepFall(){
  if(P.onGround||isDead()){ if(P.fallTop!=null&&P.onGround&&!isDead()){ const drop=P.fallTop-P.pos.y; if(drop>FALL_SAFE) fallHurt(drop); } P.fallTop=null; return; }
  P.fallTop=Math.max(P.fallTop??P.pos.y,P.pos.y); }
function fallHurt(drop){
  if(!playing) return; const dmg=Math.round((drop-FALL_SAFE)*FALL_PER); if(dmg<=0) return;
  dmgNum(P.pos.clone().setY(P.pos.y+1.9),dmg,'hp'); const f=$('hurtfx'); f.classList.add('on'); void f.offsetWidth; f.classList.remove('on'); sfx('hurt'); animEvent(localHero,'hurt');
  P.hp=Math.max(0,P.hp-dmg); if(P.hp>0) return;
  animEvent(localHero,'die');
  if(net.role){ net.dead=true; net.deaths++; const e={type:'elim',id:net.id,by:net.id,w:'fall'}; onElim(e); netSend(e);
    setTimeout(()=>{ net.dead=false; const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); banner('Back in','',1); },3000); }
  else if(horde.on){ horde.phase='over'; horde.t=6; horde.best=Math.max(horde.best,horde.wave-1); banner('Fell!','You survived '+(horde.wave-1)+(horde.wave-1===1?' wave':' waves')+' · '+horde.kills+' zombies',5); sfx('lose'); }
  else if(B&&B.active&&round.state==='fight') endRound(false);
  else { net.dead=true; feed('<b>You</b> fell too far',true); banner('Eliminated','by the fall',2); sfx('lose'); setTimeout(()=>{ net.dead=false; respawn(); },2500); }
}
const zReach=z=>0.75*z.sc+0.45;""")
rep("  const nm=id=>id===net.id?'You':id==='bot'?'Bot':id==='zombie'?'A zombie':(net.players.get(id)||{}).name||'Player', w=(WEAPONS[m.w]||{name:m.w==='zombie'?'Claws':'Pickaxe'}).name;",
    "  const nm=id=>id===net.id?'You':id==='bot'?'Bot':id==='zombie'?'A zombie':(net.players.get(id)||{}).name||'Player', w=(WEAPONS[m.w]||{name:m.w==='zombie'?'Claws':'Pickaxe'}).name;\n  if(m.w==='fall'){ feed(`<b>${nm(m.id)}</b> fell too far`,m.id===net.id); if(m.id===net.id){ banner('Eliminated','by the fall',2.6); sfx('lose'); }\n    const pl=net.players.get(m.id); if(pl){ pl.alive=false; animEvent(pl.h,'die'); setTimeout(()=>{ if(!pl.alive) pl.h.group.visible=false; },900); } return; }")
rep("    const n=Math.max(1,Math.ceil(dt/0.008)); for(let k=0;k<n;k++){ physStep(dt/n,P);","    const n=Math.max(1,Math.ceil(dt/0.008)); stepFall(); for(let k=0;k<n;k++){ physStep(dt/n,P);")
rep("function respawn(){ animEvent(localHero,'revive'); P.pos.set(...SPAWN); P.vel.set(0,0,0); P.onGround=true;","function respawn(){ animEvent(localHero,'revive'); P.pos.set(...SPAWN); P.vel.set(0,0,0); P.onGround=true; P.fallTop=null;")
rep("  TOWNS.forEach(t=>{ const px=tx(t.x), pz=tz(t.z), dx=px-c, dz=pz-c, m=Math.hypot(dx,dz), lim=c-9*dpr, qx=m>lim?c+dx/m*lim:px, qz=m>lim?c+dz/m*lim:pz;",
    "  TOWNS.forEach(t=>{ const px=tx(t.x), pz=tz(t.z), dx=px-c, dz=pz-c, m=Math.hypot(dx,dz), lim=c-9*dpr, qx=m>lim?c+dx/m*lim:px, qz=m>lim?c+dz/m*lim:pz; if(m>lim) return; // only towns actually on the minimap (the full map shows them all)")
# ---------- 19. creature hitboxes follow the model per type ----------
rep("""  const hx=E.isZombie?-Math.sin(E.yaw)*0.17*k:0, hz=E.isZombie?-Math.cos(E.yaw)*0.17*k:0, hy=E.isZombie?1.95:(cr?1.2:1.66);
  const ht=raySphere(o,d,_d.set(E.pos.x+hx,f+hy*k,E.pos.z+hz),0.19*k);
  if(ht>0) best={t:ht,head:true};
  const top=cr?1.0:E.isZombie?1.72:1.42;
  for(let y=0.25;y<=top+0.001;y+=0.19){ const t=raySphere(o,d,_d.set(E.pos.x,f+y*k,E.pos.z),0.31*k); if(t>0&&(!best||t<best.t)) best={t,head:false}; }""",
"""  const Zt=E.isZombie?ZT[E.type]:null, fx=-Math.sin(E.yaw), fz=-Math.cos(E.yaw);
  if(Zt){ // the creature's skull, then the base of its flame crown: both count as the head
    for(const [up,fw,r] of [[2.06,Zt.hf,0.16],[2.34,Zt.hf+0.07,0.11]]){ const ht=raySphere(o,d,_d.set(E.pos.x+fx*fw*k,f+up*k,E.pos.z+fz*fw*k),r*k); if(ht>0&&(!best||ht<best.t)) best={t:ht,head:true}; } }
  else { const ht=raySphere(o,d,_d.set(E.pos.x,f+(cr?1.2:1.66)*k,E.pos.z),0.19*k); if(ht>0) best={t:ht,head:true}; }
  const top=cr?1.0:Zt?1.9:1.42, lean=Zt?Math.sin(Zt.lean):0;
  for(let y=0.25;y<=top+0.001;y+=0.19){ const fw=Math.max(0,y-1.1)*lean; const t=raySphere(o,d,_d.set(E.pos.x+fx*fw*k,f+y*k,E.pos.z+fz*fw*k),0.31*k); if(t>0&&(!best||t<best.t)) best={t,head:false}; }""")
rep("husk:  {name:'Walker',hp:110,","husk:  {name:'Walker',hf:.2,lean:.16,hp:110,")
rep("runner:{name:'Runner',hp:70, ","runner:{name:'Runner',hf:.4,lean:.34,hp:70, ")
rep("brute: {name:'Brute', hp:520,","brute: {name:'Brute', hf:.24,lean:.2,hp:520,")
# ---------- 20. towns on a grid: houses in rows down both sides of a main street ----------
a=s.index("function planHouses(t){"); b=s.index("// the piece list for one house: [{type,i,j,l,axis,dir,mask,mat}]")
s=s[:a]+open('/home/claude/mg/planhouses.js').read()+s[b:]
exec(open('/home/claude/mg/patch21.py').read())
exec(open('/home/claude/mg/patch22.py').read())
exec(open('/home/claude/mg/patch23.py').read())
exec(open('/home/claude/mg/patch24.py').read())
exec(open('/home/claude/mg/patch25.py').read())
exec(open('/home/claude/mg/patch26.py').read())
exec(open('/home/claude/mg/patch27.py').read())
exec(open('/home/claude/mg/patch28.py').read())
exec(open('/home/claude/mg/patch29.py').read())
exec(open('/home/claude/mg/patch30.py').read())
exec(open('/home/claude/mg/patch31.py').read())
exec(open('/home/claude/mg/patch32.py').read())
exec(open('/home/claude/mg/patch33.py').read())
exec(open('/home/claude/mg/patch34.py').read())
exec(open('/home/claude/mg/patch35.py').read())
exec(open('/home/claude/mg/patch36.py').read())
exec(open('/home/claude/mg/patch37.py').read())
exec(open('/home/claude/mg/patch38.py').read())
exec(open('/home/claude/mg/patch39.py').read())
exec(open('/home/claude/mg/patch40.py').read())
exec(open('/home/claude/mg/patch41.py').read())
exec(open('/home/claude/mg/patch42.py').read())
exec(open('/home/claude/mg/patch43.py').read())
exec(open('/home/claude/mg/patch44.py').read())
exec(open('/home/claude/mg/patch45.py').read())
exec(open('/home/claude/mg/patch46.py').read())
exec(open('/home/claude/mg/patch47.py').read())
exec(open('/home/claude/mg/patch48.py').read())
exec(open('/home/claude/mg/patch49.py').read())
exec(open('/home/claude/mg/patch50.py').read())
exec(open('/home/claude/mg/patch51.py').read())
exec(open('/home/claude/mg/patch52.py').read())
exec(open('/home/claude/mg/patch53.py').read())
exec(open('/home/claude/mg/patch54.py').read())
exec(open("/home/claude/mg/patch55.py").read())
exec(open("/home/claude/mg/patch56.py").read())
exec(open("/home/claude/mg/patch57.py").read())
exec(open("/home/claude/mg/patch58.py").read())
exec(open("/home/claude/mg/patch59.py").read())
exec(open("/home/claude/mg/patch60.py").read())
exec(open("/home/claude/mg/patch61.py").read())
exec(open("/home/claude/mg/patch62.py").read())
exec(open("/home/claude/mg/patch63.py").read())
exec(open("/home/claude/mg/patch64.py").read())
exec(open("/home/claude/mg/patch65.py").read())
exec(open("/home/claude/mg/patch66.py").read())
exec(open("/home/claude/mg/patch67.py").read())
exec(open("/home/claude/mg/patch68.py").read())
exec(open("/home/claude/mg/patch69.py").read())
exec(open("/home/claude/mg/patch70.py").read())
exec(open("/home/claude/mg/patch71.py").read())
exec(open("/home/claude/mg/patch72.py").read())
exec(open("/home/claude/mg/patch73.py").read())
exec(open("/home/claude/mg/patch74.py").read())
exec(open("/home/claude/mg/patch75.py").read())
exec(open("/home/claude/mg/patch76.py").read())
exec(open("/home/claude/mg/patch77.py").read())
exec(open("/home/claude/mg/patch78.py").read())
exec(open("/home/claude/mg/patch79.py").read())
exec(open("/home/claude/mg/patch80.py").read())
exec(open("/home/claude/mg/patch81.py").read())
exec(open("/home/claude/mg/patch82.py").read())
exec(open("/home/claude/mg/patch83.py").read())
exec(open("/home/claude/mg/patch84.py").read())
exec(open("/home/claude/mg/patch85.py").read())
exec(open("/home/claude/mg/patch86.py").read())
exec(open("/home/claude/mg/patch87.py").read())
exec(open("/home/claude/mg/patch88.py").read())
exec(open("/home/claude/mg/patch89.py").read())
exec(open("/home/claude/mg/patch90.py").read())
exec(open("/home/claude/mg/patch91.py").read())
exec(open("/home/claude/mg/patch92.py").read())
exec(open("/home/claude/mg/patch93.py").read())
exec(open("/home/claude/mg/patch94.py").read())
exec(open("/home/claude/mg/patch95.py").read())
exec(open("/home/claude/mg/patch96.py").read())
exec(open("/home/claude/mg/patch97.py").read())
exec(open("/home/claude/mg/patch98.py").read())
exec(open("/home/claude/mg/patch99.py").read())
exec(open("/home/claude/mg/patch100.py").read())
exec(open("/home/claude/mg/patch101.py").read())
exec(open("/home/claude/mg/patch102.py").read())
exec(open("/home/claude/mg/patch103.py").read())
exec(open("/home/claude/mg/patch104.py").read())
exec(open("/home/claude/mg/patch105.py").read())
exec(open("/home/claude/mg/patch106.py").read())
exec(open("/home/claude/mg/patch107.py").read())
exec(open("/home/claude/mg/patch108.py").read())
exec(open("/home/claude/mg/patch109.py").read())
exec(open("/home/claude/mg/patch110.py").read())
exec(open("/home/claude/mg/patch111.py").read())
exec(open("/home/claude/mg/patch112.py").read())
exec(open("/home/claude/mg/patch113.py").read())
exec(open("/home/claude/mg/patch114.py").read())
exec(open("/home/claude/mg/patch115.py").read())
exec(open("/home/claude/mg/patch116.py").read())
exec(open("/home/claude/mg/patch117.py").read())
exec(open("/home/claude/mg/patch118.py").read())
exec(open("/home/claude/mg/patch119.py").read())
assert 'MTN_R' not in s and 'HILL_RAMP' not in s and 'GROUND,' not in s, 'leftover old map constants'
open(F,'w').write(s); print('patched',len(s))

# patch202: things too small to see that far away aren't drawn: every few frames, each small object out in the world
# (signs, lamps, rocks, crates, cars, chests, the clutter at the named places...) is left out of the drawing when it's
# further than it could matter for its size (a metre-sized thing past 90 m, a five-metre one past 200 m...). It
# stays where it is and works as before; it's only skipped when drawing (and casting shadows).
rep("""function stepProps(dt){""","""const FARCULL={t:0,list:[],seen:new WeakSet(),n:-1};
function farCullAdd(o){ FARCULL.seen.add(o); if(o.isLight||o.isCamera||o.isInstancedMesh||o.isSprite||o.isPoints||o.isLineSegments) return; if(o.userData&&(o.userData.noCull||o.userData.piece||o.userData.batch)) return;
  if(o===VCLOUD.sky||(typeof skyDome!=='undefined'&&o===skyDome)||(typeof OCEAN!=='undefined'&&(o===OCEAN.sea||(OCEAN.falls||[]).includes(o)))) return; if(typeof WATER!=='undefined'&&WATER.meshes.includes(o)) return;
  if(typeof BR!=='undefined'&&BR.wall===o) return; if(typeof BRBUS!=='undefined'&&BRBUS.g===o) return;
  const meshes=[]; o.traverse(m=>{ if(m.isMesh&&!m.isInstancedMesh) meshes.push(m); }); if(!meshes.length) return; const bb=new THREE.Box3().setFromObject(o); if(bb.isEmpty()) return; const s=bb.getBoundingSphere(new THREE.Sphere());
  if(s.radius>40) return; FARCULL.list.push({o,meshes,c:s.center.clone().sub(o.position),r:s.radius,far:false}); }
function stepFarCull(dt){ FARCULL.t-=dt; if(FARCULL.t>0) return; FARCULL.t=0.25;
  if(scene.children.length!==FARCULL.n){ FARCULL.n=scene.children.length; const tb=new Set(); townBatch.forEach(b=>b.meshes.forEach(m=>tb.add(m))); for(const o of scene.children) if(!FARCULL.seen.has(o)&&!tb.has(o)) farCullAdd(o); }
  const cp=camera.position, ext=Math.max(1,Math.min(4,70/(camera.fov||70))); let w=0; const L=FARCULL.list;
  for(let i=0;i<L.length;i++){ const e=L[i], o=e.o; if(o.parent!==scene){ if(e.far) for(const m of e.meshes) m.layers.set(0); FARCULL.seen.delete(o); continue; } L[w++]=e; // (gone: forget it)
    const x=o.position.x+e.c.x-cp.x, y=o.position.y+e.c.y-cp.y, z=o.position.z+e.c.z-cp.z, d=Math.sqrt(x*x+y*y+z*z)-e.r, lim=Math.min(650,Math.max(90,e.r*40))*ext, far=d>lim;
    if(far!==e.far){ e.far=far; for(const m of e.meshes) m.layers.set(far?1:0); } } L.length=w; }
function stepProps(dt){ try{ stepFarCull(dt); }catch(e){ if(!FARCULL.err){ FARCULL.err=1; console.warn('farcull',e); } }""")
rep("""  const H=createHero(o.jacket,Object.assign({},o,ex)); heroLodPrep(H); H.back=bk||'auto'; return H; }""","""  const H=createHero(o.jacket,Object.assign({},o,ex)); heroLodPrep(H); H.back=bk||'auto'; H.group.userData.noCull=true; return H; } // (people are never left out for distance: you can scope them)""")
rep("""b.far=new THREE.Mesh(botFarGeo(b.h.outfit),bakedMat(false)); b.far.castShadow=false;""","""b.far=new THREE.Mesh(botFarGeo(b.h.outfit),bakedMat(false)); b.far.userData.noCull=true; b.far.castShadow=false;""")
# the paintings, lamps, rugs and curtains in a town's houses are only drawn when you're near that town
rep("""const meshes=[]; byMat.forEach((ms,mat)=>{ const mm=new THREE.Mesh(mergeWorld(ms),mat);""","""const meshes=[]; byMat.forEach((ms,mat)=>{ const mm=new THREE.Mesh(mergeWorld(ms),mat); if(ms[0]&&ms[0].userData.decor) mm.userData.decorBatch=true;""")
rep("""townBatch.forEach((b,t)=>{ const on=Math.hypot(t.x-cx,t.z-cz)<900; b.meshes.forEach(m=>{ m.visible=on; }); });""","""townBatch.forEach((b,t)=>{ const dd=Math.hypot(t.x-cx,t.z-cz), on=dd<900, ins=dd<t.R+60; b.meshes.forEach(m=>{ m.visible=on&&(!m.userData.decorBatch||ins); }); });""")
# (skipping far things when drawing must not let shots through them: pieces are never culled, and the shot ray sees
# every layer)
rep("""  if(typeof BR!=='undefined'&&BR.wall===o) return; if(typeof BRBUS!=='undefined'&&BRBUS.g===o) return;""","""  if(typeof BR!=='undefined'&&BR.wall===o) return; if(typeof BRBUS!=='undefined'&&BRBUS.g===o) return;
  { let pc=false; o.traverse(m=>{ if(m.userData&&m.userData.piece) pc=true; }); if(pc) return; }""")
rep("""const ray=new THREE.Raycaster();""","""const ray=new THREE.Raycaster(); ray.layers.enableAll();""")

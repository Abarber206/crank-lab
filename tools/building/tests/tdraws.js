// what's being drawn in a battle royale scene: objects in view by kind, draw calls and triangles per pass
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,BR,BRBUS,townBatch,FOREST,TOWNS,SPAWN,terrainH,renderMain,localHero,chests,karts,props,drops,pieces,DECO,TERR'),{vp:{width:1280,height:720}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000});
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(800); await pg.evaluate(()=>{ const t=T.TOWNS.find(t=>!t.kind); T.P.sky=null; T.P.bus=false; T.P.pos.set(t.x+20,T.terrainH(t.x+20,t.z)+0.2,t.z); T.P.hp=1e6; T.BR.bots.forEach((o,i)=>{ if(i<12){ o.sky=null; o.bus=false; const x=t.x+Math.cos(i)*25,z=t.z+Math.sin(i)*25; o.pos.set(x,T.terrainH(x,z)+0.2,z); } }); });
 await sleep(6000);
 const r=await pg.evaluate(()=>{ const I=T.renderer.info; I.autoReset=false; I.reset(); T.renderMain(); const tot={calls:I.render.calls,tris:I.render.triangles};
   // visible meshes by owner (no frustum test)
   const cat=new Map(), add=(k)=>cat.set(k,(cat.get(k)||0)+1); const owner=new Map();
   T.BR.bots.forEach(b=>b.h.group.traverse(o=>owner.set(o,'bot'))); T.localHero.group.traverse(o=>owner.set(o,'me'));
   T.townBatch.forEach(bb=>bb.meshes.forEach(m=>owner.set(m,'town')));
   T.chests.forEach(c=>c.g&&owner.set(c.g,'chest')); T.karts.forEach(k=>k.g&&owner.set(k.g,'kart')); T.props.forEach(p=>p.g&&owner.set(p.g,'prop:'+p.kind)); T.drops.forEach(d=>d.g&&owner.set(d.g,'drop')); T.pieces.forEach(p=>p.group&&owner.set(p.group,p.owner==='world'?'piece:world':'piece:built'));
   if(T.DECO&&T.DECO.meshes) T.DECO.meshes.forEach(m=>owner.set(m,'deco')); T.TERR.chunks.forEach(c=>(c.m||[]).forEach(m=>m&&owner.set(m,'terrain')));
   T.scene.traverseVisible(o=>{ if(!(o.isMesh||o.isLine||o.isLineSegments||o.isPoints||o.isSprite)) return; let k=owner.get(o); if(!k){ let p=o; while(p&&!owner.get(p)) p=p.parent; k=p?owner.get(p):(o.isInstancedMesh?'instanced':o.isSprite?'sprite':'other'); }
     if(k==='other'){ let top=o; while(top.parent&&top.parent!==T.scene) top=top.parent; k='other:'+(top===o?'mesh':'group'+top.children.length)+':'+(o.material&&o.material.type)+':'+(o.geometry&&o.geometry.type); } add(k); });
   const perBot=[]; T.BR.bots.slice(0,3).forEach(b=>{ let n=0; b.h.group.traverseVisible(o=>{ if(o.isMesh) n++; }); perBot.push(n); });
   const L=[]; T.scene.children.forEach(o=>{ if(!o.visible||!o.isMesh||owner.get(o)||!(o.material&&o.material.type==='MeshLambertMaterial')) return; if(!o.geometry.boundingSphere) o.geometry.computeBoundingSphere(); const bs=o.geometry.boundingSphere, c=bs.center.clone().applyMatrix4(o.matrixWorld); L.push([Math.round(bs.radius),Math.round(c.distanceTo(T.camera.position)),o.geometry.attributes.position.count,o.material.vertexColors?'vc':'', o.material.map?'map':'',o.name||'',o.userData?Object.keys(o.userData).join('/'):'' ]); });
   const hist={}; L.forEach(r=>{ const k=(r[0]<2?'r<2':r[0]<8?'r<8':r[0]<30?'r<30':'big')+(r[1]<100?' near':r[1]<300?' mid':' far'); hist[k]=(hist[k]||0)+1; });
   return {hist,sample:L.slice(0,8),tot,cat:[...cat].sort((a,b)=>b[1]-a[1]).slice(0,25),perBot,botsVisible:T.BR.bots.filter(b=>b.h.group.visible).length}; });
 console.log(JSON.stringify(r)); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

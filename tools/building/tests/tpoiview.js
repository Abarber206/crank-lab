// aerial pictures of the points of interest (and a few low views).  node tpoiview.js kind [views]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const kind=process.argv[2]||'factory', views=(process.argv[3]||'air,ne,sw').split(',');
 const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,TOWNS,P,camera,settings,TOD,pieces,chests,STATICS,townBatch'),{vp:{width:1280,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.32; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(9000);
 const info=await pg.evaluate(k=>{ const t=T.TOWNS.find(x=>x.kind===k); T.P.pos.set(t.x+60,t.h+0.1,t.z+60); let n=0; T.pieces.forEach(p=>{ if(p.town===t) n++; }); return {name:t.name,pieces:n,chests:T.chests.filter(c=>Math.hypot(c.x-t.x,c.z-t.z)<50).length,statics:T.STATICS.filter(s=>s.solid&&s.solid.deco&&Math.hypot(s.x-t.x,s.z-t.z)<60).length}; },kind);
 console.log(JSON.stringify(info)); await sleep(4000);
 for(const v of views){ const url=await pg.evaluate(([k,v])=>{ const t=T.TOWNS.find(x=>x.kind===k), THREE=window.THREE, cam=new THREE.PerspectiveCamera(v==='air'?50:55,1280/800,0.5,2000);
     const V={air:[0,95,70,0,0,0],ne:[48,24,-48,0,4,0],sw:[-48,22,48,0,4,0],nw:[-46,18,-46,0,5,0],se:[46,18,46,0,5,0],low1:[18,2.5,-3,30,3,-30],low2:[-3,2.5,18,-30,3,30],in1:[12,2.2,12,24,2,22],in2:[-14,2.2,10,-24,2,24]}[v];
     T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); cam.position.set(t.x+V[0],t.h+V[1],t.z+V[2]); cam.lookAt(t.x+V[3],t.h+V[4],t.z+V[5]); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/png'); },[kind,v]);
   require('fs').writeFileSync('/home/claude/work/poi_'+kind+'_'+v+'.png',Buffer.from(url.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

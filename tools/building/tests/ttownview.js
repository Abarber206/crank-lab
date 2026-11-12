// aerial pictures of towns.  node ttownview.js [townIndexes] [views] [file]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const ids=(process.argv[2]||'0,1').split(',').map(Number), views=(process.argv[3]||'top').split(','), file=process.argv[4]||'/home/claude/crank-lab/index.html';
 const {pg,errs}=await open(b,page(file,'scene,renderer,TOWNS,P,settings,TOD,townBatch'),{vp:{width:1280,height:1000}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.32; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(9000);
 for(const id of ids){ await pg.evaluate(k=>{ const t=T.TOWNS[k]; T.P.pos.set(t.x+10,t.h+0.1,t.z+10); },id); await sleep(5000);
  for(const v of views){ const url=await pg.evaluate(([k,v])=>{ const t=T.TOWNS[k], THREE=window.THREE;
     let cam; if(v==='top'){ const s=100; cam=new THREE.OrthographicCamera(-s*1.28,s*1.28,s,-s,1,600); cam.position.set(t.x,t.h+300,t.z+0.01); cam.lookAt(t.x,t.h,t.z); }
     else { cam=new THREE.PerspectiveCamera(55,1280/1000,0.5,2000); const V={ne:[70,40,-70],sw:[-70,40,70],nw:[-70,35,-70],se:[70,35,70],st:[6,2.2,6]}[v]; cam.position.set(t.x+V[0],t.h+V[1],t.z+V[2]); cam.lookAt(t.x,t.h+2,t.z); }
     T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/png'); },[id,v]);
   require('fs').writeFileSync('/home/claude/work/town'+id+'_'+v+'.png',Buffer.from(url.split(',')[1],'base64')); } }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

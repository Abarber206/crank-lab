// the forest from a few distances: a close look at the trees, the middle distance, the far woods, and from the sky.  node ttrees.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,P,camera,settings,TOD,props,terrainH,FOREST,stepForest,CAMH'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.props,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(9000);
 // a tree in a meadow-ish spot with others around
 const spot=await pg.evaluate(()=>{ const trees=T.props.filter(p=>p.kind==='tree'&&p.alive); let best=null,bn=0; for(let k=0;k<trees.length;k+=7){ const p=trees[k]; const n=trees.filter(q=>Math.hypot(q.x-p.x,q.z-p.z)<40).length; if(n>bn&&n<60){ bn=n; best=p; } } return {x:best.x,z:best.z,y:T.terrainH(best.x,best.z),s:best.s}; }); console.log('tree scale',spot.s);
 await pg.evaluate(s=>{ T.P.pos.set(s.x+14,s.y+0.1,s.z+14); },spot); await sleep(5000);
 const views={near:[19,2,15,0,7,0],mid:[120,34,95,0,4,0],far:[330,70,280,0,0,0],sky:[30,180,30,0,0,0],under:[4,1.7,3,0,8,0]};
 for(const [k,V] of Object.entries(views)){ const url=await pg.evaluate(([s,V])=>{ const THREE=window.THREE, cam=new THREE.PerspectiveCamera(55,1280/760,0.3,3000); cam.position.set(s.x+V[0],s.y+V[1],s.z+V[2]); cam.lookAt(s.x+V[3],s.y+V[4],s.z+V[5]);
     T.camera.position.copy(cam.position); T.stepForest(1); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/png'); },[spot,V]);
   require('fs').writeFileSync('/home/claude/work/trees_'+k+'.png',Buffer.from(url.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

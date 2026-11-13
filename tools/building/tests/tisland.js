// the island on its cliffs: from afar, the waterfall, the view out to sea from the edge, the lagoon
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,P,settings,TOD,terrainH,WGEN,OCEAN,SPAWN,MAP_R,camera,townBatch'),{vp:{width:1280,height:720}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OCEAN,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); }); await sleep(7000);
 const info=await pg.evaluate(()=>{ const S=T.WGEN.sea(), a=Math.atan2(S.nz,S.nx); return {a,falls:T.OCEAN.falls.length,mists:T.OCEAN.mists.length}; }); console.log(JSON.stringify(info));
 const views=[['above',info.a,0,'above'],['fall',info.a,0,'fall'],['edge',info.a+2.2,0,'edge'],['lagoon',info.a,0,'lagoon'],['lip',info.a+0.05,0,'lip']];
 for(const [n,a] of views){ await pg.evaluate(([n,a])=>{ T.TOD.fix=0.3; const C=T.SPAWN, R=n==='lagoon'?700:n==='far'?0:n==='fall'?790:770, x=C[0]+Math.cos(a)*R, z=C[2]+Math.sin(a)*R; T.P.pos.set(x,T.terrainH(x,z)+0.1,z); },[n,a]); await sleep(6000);
   const u=await pg.evaluate(([n,a])=>{ const THREE=window.THREE, C=T.SPAWN, cam=new THREE.PerspectiveCamera(55,1280/720,0.5,6000), ca=Math.cos(a), sa=Math.sin(a), E=T.WGEN.edgeR(ca*800,sa*800);
     if(n==='above'){ cam.position.set(C[0]+ca*600-sa*250,260,C[2]+sa*600+ca*250); cam.lookAt(C[0]+ca*E,-30,C[2]+sa*E); }
     else if(n==='fall'){ const px=-sa, pz=ca; cam.position.set(C[0]+ca*(E+120)+px*60,-20,C[2]+sa*(E+120)+pz*60); cam.lookAt(C[0]+ca*E,-28,C[2]+sa*E); }
     else if(n==='edge'){ const x=C[0]+ca*(E-6), z=C[2]+sa*(E-6), y=T.terrainH(x,z)+2; cam.position.set(x,y,z); cam.lookAt(x+ca*100-sa*30,y-18,z+sa*100+ca*30); }
     else if(n==='lip'){ const S=T.WGEN.sea(), x=C[0]+ca*(E-30), z=C[2]+sa*(E-30); cam.position.set(x-sa*20,S.Y+7,z+ca*20); cam.lookAt(x+ca*30+sa*40,S.Y-4,z+sa*30-ca*40); }
     else { const x=C[0]+ca*690, z=C[2]+sa*690, y=T.terrainH(x,z)+3; cam.position.set(x,y,z); cam.lookAt(C[0]+ca*E,y-6,C[2]+sa*E); }
     T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },[n,a]);
   require('fs').writeFileSync('/home/claude/work/isle_'+n+'.jpg',Buffer.from(u.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

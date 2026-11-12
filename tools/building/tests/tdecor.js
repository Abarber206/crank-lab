// the decorations: counts, and pictures of a campsite, a power line, a hay field, the dock, a bench, a river boat, a point of interest
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,TOWNS,P,settings,TOD,townBatch,DECOR,terrainH,STATICS,chests'),{vp:{width:1280,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS&&T.DECOR,null,{timeout:180000});
 console.log(await pg.evaluate(()=>JSON.stringify({camps:T.DECOR.camps.length,chests:T.DECOR.chests.length,poles:T.DECOR.poles,meshes:T.DECOR.items,farms:(T.DECOR.farms||[]).length,dock:!!T.DECOR.dock,bench:!!T.DECOR.bench,rboat:!!T.DECOR.rboat,statics:T.STATICS.length,allChests:T.chests.length})));
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(8000);
 const shots=await pg.evaluate(()=>{ const D=T.DECOR, o=[]; if(D.camps[0]) o.push(['camp',D.camps[0][0],D.camps[0][1],0,9]); if(D.camps[3]) o.push(['camp2',D.camps[3][0],D.camps[3][1],2,9]); if(D.pole) o.push(['pole',D.pole[0],D.pole[1],D.pole[2]+1.2,22]); if(D.farms) o.push(['farm',D.farms[0][0],D.farms[0][1],D.farms[0][2]+0.6,34]);
   if(D.dock) o.push(['dock',D.dock[0],D.dock[1],D.dock[2]+2.4,18]); if(D.bench) o.push(['bench',D.bench[0],D.bench[1],D.bench[2]+0.5,7]); if(D.rboat) o.push(['rboat',D.rboat[0],D.rboat[1],0.8,8]); const f=T.TOWNS.find(t=>t.kind==='timber'); o.push(['timber',f.x,f.z,0.7,52]); const g=T.TOWNS.find(t=>t.kind==='factory'); o.push(['factory',g.x,g.z,2.2,52]); return o; });
 for(const [n,x,z,a,dist] of shots){ await pg.evaluate(([x,z])=>{ T.TOD.fix=0.3; T.P.pos.set(x+3,T.terrainH(x+3,z+3)+0.1,z+3); },[x,z]); await sleep(5000);
   const url=await pg.evaluate(([x,z,a,dist])=>{ const THREE=window.THREE, cam=new THREE.PerspectiveCamera(55,1280/800,0.3,3000), y=T.terrainH(x,z); cam.position.set(x+Math.sin(a)*dist,y+dist*0.45+1.5,z+Math.cos(a)*dist); cam.lookAt(x,y+0.8,z);
     T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },[x,z,a,dist]);
   require('fs').writeFileSync('/home/claude/work/decor_'+n+'.jpg',Buffer.from(url.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

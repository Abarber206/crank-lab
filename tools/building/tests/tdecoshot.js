// before/after: everything breakable within 25 m of a town street, broken
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,P,settings,TOD,DECO,DECOR,terrainH,townBatch,decoBreak'),{vp:{width:1000,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.DECO&&T.DECOR&&T.DECOR.bench,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.querySelector('.mode[data-mode=fight]').click(); document.querySelector('#play').click(); }); await sleep(7000);
 const [x,z]=T_=await pg.evaluate(()=>{ T.TOD.fix=0.3; const [x,z]=T.DECOR.bench; T.P.pos.set(x+2,T.terrainH(x,z)+0.1,z+2); return [x,z]; }); await sleep(4000);
 const shot=async n=>{ const u=await pg.evaluate(([x,z])=>{ const THREE=window.THREE, cam=new THREE.PerspectiveCamera(60,1000/640,0.3,800), y=T.terrainH(x,z); cam.position.set(x+4,y+13,z+4); cam.lookAt(x,y+0.8,z); T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },[x,z]); require('fs').writeFileSync('/home/claude/work/decoshot_'+n+'.jpg',Buffer.from(u.split(',')[1],'base64')); };
 await shot('before'); const n=await pg.evaluate(([x,z])=>{ let n=0; T.DECO.objs.forEach(o=>{ if(!o.gone&&Math.hypot(o.c.x-x,o.c.z-z)<25){ T.decoBreak(o); n++; } }); return n; },[x,z]); await sleep(2500); await shot('after');
 console.log('broke',n); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

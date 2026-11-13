// the battle bus: from your seat on it (the game's own camera), from the side, and from below as it passes over
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,BR,BRBUS,TOD,terrainH'),{vp:{width:1280,height:720}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on&&T.BRBUS.on,null,{timeout:120000});
 await pg.evaluate(()=>{ T.TOD.fix=0.3; T.BRBUS.t=T.BRBUS.T*0.3; }); await sleep(4000);
 const shot=async n=>{ const u=await pg.evaluate(()=>T.renderer.domElement.toDataURL('image/jpeg',0.88)); require('fs').writeFileSync('/home/claude/work/bus_'+n+'.jpg',Buffer.from(u.split(',')[1],'base64')); };
 { const u=await pg.evaluate(()=>{ T.renderer.render(T.scene,T.camera); return T.renderer.domElement.toDataURL('image/jpeg',0.88); }); require('fs').writeFileSync('/home/claude/work/bus_ride.jpg',Buffer.from(u.split(',')[1],'base64')); }
 for(const [n,f] of [['side',[16,-6,6]],['front',[-8,0,-22]],['below',[6,-40,10]]]){
   const u=await pg.evaluate(f=>{ const THREE=window.THREE, G=T.BRBUS.g, cam=new THREE.PerspectiveCamera(50,1280/720,0.5,6000), q=new THREE.Vector3(...f).applyAxisAngle(new THREE.Vector3(0,1,0),T.BRBUS.yaw); cam.position.copy(G.position).add(q); cam.lookAt(G.position.x,G.position.y+5,G.position.z); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.88); },f);
   require('fs').writeFileSync('/home/claude/work/bus_'+n+'.jpg',Buffer.from(u.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

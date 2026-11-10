const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,camera,horde'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(4000);
 await pg.evaluate(()=>{ T.horde.t=9999; window.cam=new THREE.PerspectiveCamera(60,1100/640,0.1,4000); const R0=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>R0(s,c===T.camera?cam:c); const t=T.TOWNS[5]; T.P.pos.set(t.x,T.terrainH(t.x,t.z)+0.2,t.z); T.P.hp=1e9; cam.position.set(t.x+60,T.terrainH(t.x,t.z)+420,t.z+60); cam.lookAt(t.x,T.terrainH(t.x,t.z),t.z); });
 await sleep(6000); await pg.screenshot({path:'fog_a.png'});
 await pg.evaluate(()=>{ const t=T.TOWNS[5]; cam.position.set(t.x+10,T.terrainH(t.x,t.z)+70,t.z+10); cam.lookAt(t.x,T.terrainH(t.x,t.z),t.z); }); await sleep(4000); await pg.screenshot({path:'fog_b.png'});
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

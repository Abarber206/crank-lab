const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,skyDrop,camera'),{vp:{width:1000,height:580}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(800);
 await pg.evaluate(()=>{ T.skyDrop(T.P.pos.x,T.P.pos.z,1500); T.P.pitch=-0.5; setInterval(()=>{ if(T.P.sky){ T.P.vel.y=-55; T.P.vel.x=8; if(T.P.pos.y<700) T.P.pos.y=1400; } },16); });
 await sleep(7000); await pg.screenshot({path:'sky_fall.png'}); console.log(await pg.evaluate(()=>T.camera.fov.toFixed(1)), errs.join('\n')||'no errors'); await b.close(); })();

const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 await pg.evaluate(()=>{ const t=T.TOWNS[2]; T.P.pos.set(t.x+6,T.terrainH(t.x+6,t.z+2)+0.1,t.z+2); T.P.vel.set(0,0,0); T.P.yaw=-2.0; T.P.pitch=0.02; }); await sleep(4000); await pg.screenshot({path:'aw_road.png'});
 await pg.evaluate(()=>{ T.P.pos.set(2.5,0.1,2.5); T.P.down={by:'x',w:'x',t0:performance.now(),noMate:-1e9}; T.P.hp=10; }); await sleep(4000); await pg.screenshot({path:'aw_down.png'});
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

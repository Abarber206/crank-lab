const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,get AB2(){return AB}'),{vp:{width:1000,height:580}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=true; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5&&T.AB2&&T.AB2.active,null,{timeout:120000}); await sleep(2500);
 await pg.evaluate(()=>{ const A=T.AB2; T.P.yaw=Math.atan2(-(A.pos.x-T.P.pos.x),-(A.pos.z-T.P.pos.z))+0.25; T.P.pitch=0.02; }); await sleep(2500);
 await pg.screenshot({path:'ally.png'}); console.log(errs.join('\n')||'no errors'); await b.close(); })();

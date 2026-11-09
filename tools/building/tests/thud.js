const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,horde,selectGun,selectPiece,giveMats,syncMats,get AB2(){return AB}'),{vp:{width:1280,height:720}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=true; T.settings.infMats=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(2500);
 await pg.evaluate(()=>{ T.P.inv[0]='ar'; T.P.inv[1]='pump'; T.P.ammo.ar=30; T.P.res.medium=120; T.P.sh=62; T.P.hp=84; T.giveMats('wood',170); T.giveMats('brick',100); T.selectGun('ar'); T.syncMats(); }); await sleep(3500); await pg.screenshot({path:'hud_gun.png'});
 await pg.evaluate(()=>{ T.selectPiece('wall'); }); await sleep(3000); await pg.screenshot({path:'hud_build.png'});
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

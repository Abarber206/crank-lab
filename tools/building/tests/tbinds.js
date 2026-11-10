// reload and rotate can share R: in build mode R rotates (no reload), with a gun out R reloads (no rotate)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,selectGun,selectPiece,pressAction,BIND_CTX'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1200);
 const r=await pg.evaluate(()=>{ const o={}; T.selectPiece('wall'); const r0=T.P.rot; T.pressAction('reload'); T.pressAction('rotate'); o.buildRot=T.P.rot!==r0; o.buildReload=T.P.reloadT>0;
   T.selectGun('ar'); T.P.ammo.ar=3; const r1=T.P.rot; T.pressAction('rotate'); T.pressAction('reload'); o.gunRot=T.P.rot!==r1; o.gunReload=T.P.reloadT>0; return o; });
 console.log(JSON.stringify(r), r.buildRot&&!r.buildReload&&!r.gunRot&&r.gunReload?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

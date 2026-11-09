// unarmed Buddy fights with the pickaxe
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,horde,settings,renderer,newZombie,chests,get AB2(){return AB}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=true; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.AB2&&T.AB2.active,null,{timeout:60000}); await sleep(1500);
 await pg.evaluate(()=>{ T.chests.forEach(c=>{ c.open=true; }); const A=T.AB2; A.wpn=null; T.newZombie('husk',A.pos.x+5,A.pos.z); }); const k0=await pg.evaluate(()=>T.horde.kills);
 await pg.waitForFunction(k=>T.horde.kills>k,k0,{timeout:40000}).catch(()=>{});
 const r=await pg.evaluate(k=>({kill:T.horde.kills>k,wpn:T.AB2.wpn}),k0); console.log(JSON.stringify(r), r.kill&&!r.wpn?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

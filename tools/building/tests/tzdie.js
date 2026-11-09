const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,newZombie,zombieHurt,horde,settings,ZT'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.mode='horde'; document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const z=T.newZombie(Object.keys(T.ZT)[0],T.P.pos.x+5,T.P.pos.z+5); T.zombieHurt(z,99999,'me'); await new Promise(r=>setTimeout(r,2500)); return {alive:z.alive,visible:z.m.g.visible,gone:!T.horde.zs.has(z.id)}; });
 console.log(JSON.stringify(r), !r.alive&&(r.gone||!r.visible)?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

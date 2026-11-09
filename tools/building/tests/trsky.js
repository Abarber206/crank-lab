const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,settings,respawn,terrainH'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(2500);
 const r=await pg.evaluate(()=>{ T.P.sky=null; document.getElementById('respawn').click(); return JSON.stringify({sky:T.P.sky&&T.P.sky.phase,h:Math.round(T.P.pos.y-T.terrainH(T.P.pos.x,T.P.pos.z))}); });
 console.log(r, /"sky":"fall"/.test(r)?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

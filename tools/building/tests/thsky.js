const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,settings,horde,terrainH'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ const c=[...document.querySelectorAll('[data-mode]')].find(e=>e.dataset.mode==='horde'); if(c) c.click(); else T.settings.mode='horde'; });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(4000);
 const r=await pg.evaluate(()=>JSON.stringify({mode:T.settings.mode,horde:T.horde.on,sky:T.P.sky&&T.P.sky.phase,h:Math.round(T.P.pos.y-T.terrainH(T.P.pos.x,T.P.pos.z))}));
 console.log(r); console.log(/"sky":"(fall|glide)"/.test(r)&&/"horde":true/.test(r)?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

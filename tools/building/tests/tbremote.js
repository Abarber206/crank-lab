// the emote wheel opens in Battle royale (on the ground) as it does elsewhere.  node tbremote.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,BRBUS,terrainH,pressAction,releaseAction,get EW(){return EW}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000});
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(600); await pg.evaluate(()=>{ T.P.sky=null; T.P.bus=false; const x=T.P.pos.x, z=T.P.pos.z; T.P.pos.set(x,T.terrainH(x,z)+0.05,z); T.P.vel.set(0,0,0); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const o={ground:T.P.onGround,bus:!!T.P.bus,sky:!!T.P.sky}; T.pressAction('emote'); await new Promise(r=>setTimeout(r,500)); o.open=!!T.EW.open; o.vis=!document.getElementById('emoWheel').hidden; T.releaseAction('emote'); return o; });
 console.log(JSON.stringify(r)); console.log(r.open&&r.vis?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

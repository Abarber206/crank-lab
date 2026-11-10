// glider energy: level glide is steady; looking down dives and speeds up; looking up after a dive climbs for a bit;
// holding the nose up bleeds speed until it stalls and sinks again
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,skyDrop,deployGlider,settings,renderer,SPAWN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await sleep(1500);
 await pg.evaluate(()=>{ T.skyDrop(T.P.pos.x,T.P.pos.z,900); T.P.sky.t=5; T.deployGlider(T.P); T.P.pitch=0; });
 const at=async(pitch,ms)=>{ await pg.evaluate(p=>{ window._pt=p; if(!window._lock){ window._lock=true; setInterval(()=>{ T.P.pitch=window._pt; },16); } },pitch); await sleep(ms);
   return pg.evaluate(()=>({as:+(T.P.sky&&T.P.sky.as||0).toFixed(1),vy:+T.P.vel.y.toFixed(1),hs:+Math.hypot(T.P.vel.x,T.P.vel.z).toFixed(1),ph:T.P.sky&&T.P.sky.phase})); };
 const lvl=await at(0,4000), dive=await at(-0.75,4000), climb=await at(0.65,900), stall=await at(0.65,7000), back=await at(0,4000);
 console.log(JSON.stringify({lvl,dive,climb,stall,back}));
 const ok=lvl.ph==='glide'&&Math.abs(lvl.as-13)<2&&lvl.vy<-1&&lvl.vy>-3&&lvl.hs/-lvl.vy>5&&dive.as>24&&dive.vy<-18&&climb.vy>1&&stall.as<10&&stall.vy<0&&back.vy<0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

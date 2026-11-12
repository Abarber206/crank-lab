// Battle royale bots fight: two armed bots 20 m apart in the open find and shoot each other; a bot notices you standing
// in the open and shoots you, but takes longer to notice you crouched and still.  node tbrfight.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,terrainH,waterAt,SPAWN,TOWNS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 const setup=()=>pg.evaluate(()=>{ // an open flat spot away from towns; everyone else far away
   let sx=0, sz=0; for(let k=0;k<500;k++){ const x=T.SPAWN[0]+(Math.random()-.5)*900, z=T.SPAWN[2]+(Math.random()-.5)*900; if(T.waterAt(x,z)>-999||T.TOWNS.some(t=>Math.hypot(t.x-x,t.z-z)<t.R+40)) continue; let flat=true; for(let i=-3;i<=3;i++) if(Math.abs(T.terrainH(x+i*8,z)-T.terrainH(x,z))>2.5) flat=false; if(flat){ sx=x; sz=z; break; } }
   T.BR.storm.cx=sx; T.BR.storm.cz=sz; T.BR.storm.r=5000; T.BR.storm.tx=sx; T.BR.storm.tz=sz; T.BR.storm.tr=4000; T.BR.storm.t=999; T.BR.storm.state="wait"; T.BR.over=true; T.BR.overT=1e9;
   T.P.bus=false; for(const b of T.BR.bots){ b.bus=false; b.sky=null; b.pos.set(sx+3000,0,sz); b.alive=false; b.h.group.visible=false; }
   return [sx,sz]; });
 const [sx,sz]=await setup();
 const duel=await pg.evaluate(async([sx,sz])=>{ const [a,c]=T.BR.bots; for(const [b,dx] of [[a,-10],[c,10]]){ b.alive=true; b.h.group.visible=true; b.hp=100; b.sh=0; b.wpn='ar'; b.ammo=30; b.reloadT=0; b.aw.clear(); b.tgt=null; b.dest={pts:[[sx+dx,sz,3]],i:0,linger:999}; b.pos.set(sx+dx,T.terrainH(sx+dx,sz)+0.1,sz); b.vel.set(0,0,0); b.skill=0.6; }
   T.P.pos.set(sx,T.terrainH(sx,sz+400),sz+400); T.P.hp=1e6;
   await new Promise(r=>setTimeout(r,12000)); return {a:Math.round(a.hp),c:Math.round(c.hp),aAlive:a.alive,cAlive:c.alive}; },[sx,sz]);
 const spot=await pg.evaluate(async([sx,sz])=>{ const out={}; for(const crouch of [false,true]){ for(const b of T.BR.bots){ b.alive=false; b.h.group.visible=false; }
     const c=T.BR.bots[2]; c.alive=true; c.h.group.visible=true; c.hp=100; c.sh=0; c.wpn='ar'; c.ammo=30; c.aw.clear(); c.tgt=null; c.dest={pts:[[sx,sz,3]],i:0,linger:999}; c.pos.set(sx,T.terrainH(sx,sz)+0.1,sz); c.vel.set(0,0,0); c.skill=0.5; c.yaw=0;
     T.P.pos.set(sx,T.terrainH(sx,sz-35)+0.05,sz-35); T.P.vel.set(0,0,0); T.P.hp=100; T.P.sh=100; T.BR.out=false; T.P.crouch=crouch; window.__crouch=crouch;
     const t0=performance.now(); let tAware=-1; while(performance.now()-t0<15000){ await new Promise(r=>setTimeout(r,200)); T.P.crouch=crouch; if(c.tgt===T.P&&tAware<0) tAware=(performance.now()-t0)/1000; if(T.P.hp+T.P.sh<200) break; }
     out[crouch?'crouched':'standing']={aware:+tAware.toFixed(1),hurt:200-Math.round(T.P.hp+T.P.sh)}; }
   return out; },[sx,sz]);
 console.log(JSON.stringify({duel,spot}));
 const ok=(duel.a<100||duel.c<100)&&spot.standing.aware>=0&&spot.standing.hurt>0&&(spot.crouched.aware<0||spot.crouched.aware>spot.standing.aware);
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

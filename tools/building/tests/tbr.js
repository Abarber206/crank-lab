// Battle royale: 19 bots drop in with you; they land, loot guns, notice and fight (each other too), the storm closes
// and hurts anyone outside it; your shots hit bots; the HUD shows who's alive and the storm timer. Fast-forwards the
// storm.  node tbr.js [shots-prefix]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const shots=process.argv[2]; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,BR,drops,brUpdate,brFoes,WEAPONS,selectGun,playerShoot,isDead,MAP_R,SPAWN'),shots?{vp:{width:1000,height:640}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await sleep(2500);
 const s0=await pg.evaluate(()=>({on:T.BR.on,bots:T.BR.bots.length,sky:T.BR.bots.filter(b=>b.sky).length,hud:!document.getElementById('brHud').hidden,alive:document.getElementById('brAlive').textContent,psky:!!T.P.sky}));
 console.log('start',JSON.stringify(s0));
 // let them land and loot for a while (skip your own drop: put you on the ground, out of the way)
 await pg.evaluate(()=>{ T.P.sky=null; T.P.pos.set(T.SPAWN[0],T.P.pos.y,T.SPAWN[2]); T.P.hp=1e6; T.P.sh=0; });
 let landed=0, armed=0; let after=0; for(let i=0;i<130;i++){ await sleep(1000); const r=await pg.evaluate(()=>({l:T.BR.bots.filter(b=>b.alive&&!b.sky).length,a:T.BR.bots.filter(b=>b.alive&&b.wpn).length,k:T.BR.bots.reduce((s,b)=>s+b.kills,0),al:T.BR.bots.filter(b=>b.alive).length})); landed=r.l; armed=r.a; if(i%10===9) console.log('t',i+1,JSON.stringify(r)); if(r.l>=15) after++; if(r.a>=8||after>60) break; }
 // a bot in front of you: shoot it
 const hit=await pg.evaluate(async()=>{ const b=T.BR.bots.find(b=>b.alive&&!b.sky); if(!b) return null; b.thinkT=99; const p=T.P.pos.clone(); b.pos.set(p.x,p.y,p.z-6); b.vel.set(0,0,0); b.hp=100; b.sh=0;
   T.P.inv[0]='ar'; T.P.ammo.ar=30; T.selectGun('ar'); T.P.equipT=0; T.P.yaw=0; T.P.pitch=-0.05; T.camera.position.set(p.x,p.y+1.6,p.z); T.camera.lookAt(b.pos.x,b.pos.y+1.2,b.pos.z); T.camera.updateMatrixWorld();
   const h0=b.hp; for(let i=0;i<5;i++){ T.P.gunT=0; T.playerShoot(); await new Promise(r=>setTimeout(r,120)); } b.thinkT=0; return {h0,h1:b.hp,alive:b.alive}; });
 // the storm: jump it ahead, someone outside takes damage
 const st=await pg.evaluate(async()=>{ const S=T.BR.storm; S.t=0.01; await new Promise(r=>setTimeout(r,600)); S.t=0.05; await new Promise(r=>setTimeout(r,2500)); const b=T.BR.bots.find(b=>b.alive&&!b.sky); const far=T.MAP_R; b.pos.set(S.cx+S.r+30,b.pos.y,S.cz); b.thinkT=99; const h0=b.hp; await new Promise(r=>setTimeout(r,2200)); const h1=b.hp; b.thinkT=0; return {ph:S.ph,state:S.state,r:Math.round(S.r),h0,h1,wall:T.BR.wall.visible,timer:document.getElementById('brStorm').textContent}; });
 if(shots){ await pg.evaluate(()=>{ T.P.hp=100; }); await pg.screenshot({path:shots+'_hud.png',timeout:200000}); await pg.keyboard.press('KeyM').catch(()=>{}); await sleep(800); await pg.screenshot({path:shots+'_map.png',timeout:200000}); }
 const r={s0,landed,armed,hit,st}; console.log(JSON.stringify(r));
 const ok=s0.on&&s0.bots===19&&s0.sky>=15&&s0.hud&&landed>=15&&armed>=4&&hit&&(hit.h1<hit.h0||!hit.alive)&&st.h1<st.h0&&st.wall;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,8).join('\n')||'no errors'); await b.close(); })();

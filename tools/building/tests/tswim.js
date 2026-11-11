// swimming: dropped into deep water from 30 m you land unhurt and swim; head above the water treading and swimming;
// no shooting or aiming; you swim slower than you run; you climb out onto the shore. node tswim.js [shots-prefix]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const shots=process.argv[2]; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,waterAt,waterDepth,camera,WEAPONS,selectGun,playerShoot,bullets,localHero,SPAWN,canAim,adsOn,RUN'),shots?{vp:{width:900,height:560}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const spot=await pg.evaluate(()=>{ const S=T.SPAWN; let best=null; for(let k=0;k<400000&&!best;k++){ const a=k*2.399, d=600+(k%4000)*0.055, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d;
   if(T.waterDepth(x,z)>3.2&&T.waterDepth(x+6,z)>3&&T.waterDepth(x-6,z)>3&&T.waterDepth(x,z+6)>3&&T.waterDepth(x,z-6)>3){ // and a shore within 40 m
     for(let q=0;q<16&&!best;q++){ const aa=q*Math.PI/8; for(let r=8;r<70;r+=2){ const sx=x+Math.cos(aa)*r, sz=z+Math.sin(aa)*r; if(T.waterDepth(sx,sz)<0.05&&T.waterAt(sx,sz)<-999&&Math.hypot(sx-S[0],sz-S[2])<Math.hypot(x-S[0],z-S[2])-5){ best={x,z,w:T.waterAt(x,z),ya:Math.atan2(-(sx-x),-(sz-z)),shore:r}; break; } } } } }
   return best; });
 console.log('spot',JSON.stringify(spot));
 if(shots) await pg.evaluate(()=>{ window.__shots=1; });
 const out=await pg.evaluate(async(sp)=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms)), o={};
   T.P.inv[0]='ar'; T.P.ammo.ar=30; T.selectGun('ar'); T.P.equipT=0;
   T.P.pos.set(sp.x,window.__shots?sp.w-1.3:sp.w+30,sp.z); T.P.vel.set(0,0,0); T.P.onGround=!!window.__shots; T.P.yaw=sp.ya+Math.PI; T.P.pitch=0; const hp0=T.P.hp;
   await wait(3500); o.landedHp=T.P.hp-hp0; o.swim=!!T.P.swim; o.y=+(T.P.pos.y-sp.w).toFixed(2);
   const head=()=>{ const v=new THREE.Vector3(); T.localHero.rig.head.getWorldPosition(v); return +(v.y-sp.w).toFixed(2); };
   o.headStill=head(); const a0=T.P.ammo.ar, nb=T.bullets.length; T.P.gunT=0; T.playerShoot(); o.shot=T.P.ammo.ar!==a0||T.bullets.length!==nb; o.canAim=T.canAim();
   return o; },spot);
 if(shots){ await pg.evaluate(()=>{ T.P.yaw+=1.9; }); await sleep(2500); await pg.screenshot({path:shots+'_tread.png',timeout:200000}); }
 // swim away from the shore, then back toward it and out
 if(shots) await pg.evaluate(()=>{ T.P.yaw-=1.9; }); await pg.keyboard.down('KeyW'); await sleep(shots?6000:1500); const mid=await pg.evaluate(()=>{ const v=new THREE.Vector3(); T.localHero.rig.head.getWorldPosition(v); return {head:+(v.y-T.waterAt(T.P.pos.x,T.P.pos.z)).toFixed(2),sp:+Math.hypot(T.P.vel.x,T.P.vel.z).toFixed(2),run:T.RUN,swim:!!T.P.swim}; });
 if(shots){ await pg.screenshot({path:shots+'_swim.png',timeout:200000}); }
 await pg.keyboard.up('KeyW'); await pg.evaluate(sp=>{ T.P.yaw=sp.ya; },spot); await pg.keyboard.down('KeyW');
 let outT=-1; for(let i=0;i<70;i++){ await sleep(500); const s=await pg.evaluate(()=>({swim:!!T.P.swim,wd:T.waterDepth(T.P.pos.x,T.P.pos.z)})); if(!s.swim&&s.wd<0.3){ outT=i*0.5; break; } } await pg.keyboard.up('KeyW');
 const r={...out,...mid,ashoreAfter:outT}; console.log(JSON.stringify(r));
 const ok=r.landedHp===0&&r.swim&&r.headStill>0.05&&r.head>0.0&&!r.shot&&!r.canAim&&r.swim&&r.sp>1&&r.sp<r.run*0.7&&outT>=0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

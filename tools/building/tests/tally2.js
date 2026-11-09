// smarter Buddy: rides shotgun in your buggy and gets out with you; backs away from a creature in its face; catches up when left behind
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,horde,settings,renderer,newZombie,karts,enterKart,exitKart,chests,get AB2(){return AB}'),{fast:true,norender:true});
 const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+d);
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=true; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.AB2&&T.AB2.active,null,{timeout:60000}); await sleep(1000);
 await pg.evaluate(()=>{ T.horde.t=9999; T.chests.forEach(c=>c.open=true); const k=T.karts[0]; T.P.pos.set(k.x+2,k.y+0.1,k.z); const A=T.AB2; A.pos.set(k.x-2,k.y+0.1,k.z+1); A.vel.set(0,0,0); T.enterKart(k,0); });
 await pg.waitForFunction(()=>!!T.AB2.kart,null,{timeout:15000}).catch(()=>{});
 const r1=await pg.evaluate(()=>({in:!!T.AB2.kart,seat:T.karts[0].seats[1],d:+T.AB2.pos.distanceTo(new THREE.Vector3(T.karts[0].x,T.AB2.pos.y,T.karts[0].z)).toFixed(1)}));
 ok('rides shotgun',r1.in&&r1.seat==='ally'&&r1.d<1.5,JSON.stringify(r1));
 await pg.evaluate(()=>T.exitKart(true)); await sleep(700);
 const r2=await pg.evaluate(()=>({in:!!T.AB2.kart,seat:T.karts[0].seats[1],d:+Math.hypot(T.AB2.pos.x-T.karts[0].x,T.AB2.pos.z-T.karts[0].z).toFixed(1)}));
 ok('gets out when you do',!r2.in&&!r2.seat&&r2.d<5,JSON.stringify(r2));
 // armed, creature in its face: it backs off rather than standing there
 const d0=await pg.evaluate(()=>{ const A=T.AB2; T.P.pos.set(40,T.P.pos.y,40); A.pos.set(44,T.P.pos.y,40); A.vel.set(0,0,0); A.wpn='ar'; A.hp=1e6; const z=T.newZombie('brute',A.pos.x+3,A.pos.z); z.rise=0; z.hp=1e6; window.Z=z; return 3; });
 await sleep(1500); const r3=await pg.evaluate(()=>({d:+Z.pos.distanceTo(T.AB2.pos).toFixed(1),sp:+Math.hypot(T.AB2.vel.x,T.AB2.vel.z).toFixed(1)}));
 ok('backs away from a creature up close',r3.sp>2,JSON.stringify(r3));
 // left far behind: catches up
 await pg.evaluate(()=>{ Z.alive=false; T.P.pos.set(-300,T.P.pos.y,-250); }); await sleep(2500);
 const r4=await pg.evaluate(()=>+Math.hypot(T.AB2.pos.x-T.P.pos.x,T.AB2.pos.z-T.P.pos.z).toFixed(1)); ok('catches up when left behind',r4<12,String(r4));
 R.forEach(x=>console.log(x)); console.log(errs.join('\n')||'no errors'); await b.close(); })();

// solo horde with a bot teammate: it drops in, fights, revives you, gets revived, fetches your card to a van, and you reboot it
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,netDrop,P,AB,RB,VANS,horde,settings,renderer,hordeHurtMe,allyHurt,useDown,useUp,findUseTarget,newZombie,net,get AB2(){return AB}'),{fast:true,norender:true});
 const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+d);
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); });
 const optVis=await pg.evaluate(()=>!document.getElementById('allyOpt').hidden); await pg.evaluate(()=>document.getElementById('hordeBot').click());
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(3000);
 const a0=await pg.evaluate(()=>{ const A=T.AB2; return A&&{active:A.active,vis:A.h.group.visible,d:+A.pos.distanceTo(T.P.pos).toFixed(1)}; });
 ok('option shows for horde, teammate drops in with you',optVis&&a0&&a0.active&&a0.vis&&a0.d<15,JSON.stringify(a0));
 const g0=await pg.evaluate(()=>T.AB2.wpn); ok('teammate starts with no gun',g0===null,String(g0));
 // a gun on the ground near you: it goes and takes it
 await pg.evaluate(()=>{ const A=T.AB2; for(const c of []) ; T.netDrop('pump',1,new THREE.Vector3(A.pos.x+6,A.pos.y+1,A.pos.z),new THREE.Vector3(0,1,0)); });
 await pg.waitForFunction(()=>!!T.AB2.wpn,null,{timeout:40000}).catch(()=>{}); ok('teammate picks up a gun',await pg.evaluate(()=>!!T.AB2.wpn),await pg.evaluate(()=>String(T.AB2.wpn)));
 // it shoots a zombie
 await pg.evaluate(()=>{ const A=T.AB2; T.newZombie('husk',A.pos.x+10,A.pos.z); }); const k0=await pg.evaluate(()=>T.horde.kills);
 await pg.waitForFunction(k=>T.horde.kills>k,k0,{timeout:30000}).catch(()=>{}); ok('teammate kills a zombie',await pg.evaluate(k=>T.horde.kills>k,k0),'');
 // you get knocked: it revives you
 await pg.evaluate(()=>{ T.horde.zs.forEach(z=>z.alive=false); T.P.sh=0; T.hordeHurtMe(999,T.P.pos); });
 const d1=await pg.evaluate(()=>!!T.P.down); await pg.waitForFunction(()=>!T.P.down,null,{timeout:30000}).catch(()=>{});
 ok('knocked, then revived by the teammate',d1&&await pg.evaluate(()=>!T.P.down&&Math.round(T.P.hp)===30),await pg.evaluate(()=>JSON.stringify({down:!!T.P.down,hp:T.P.hp})));
 // it gets knocked: you revive it
 await pg.evaluate(()=>{ const A=T.AB2; A.sh=0; T.allyHurt(999); }); await sleep(300);
 const d2=await pg.evaluate(()=>!!T.AB2.down);
 await pg.evaluate(()=>{ const A=T.AB2; T.P.pos.set(A.pos.x+0.8,A.pos.y,A.pos.z); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(0.8,0); }); await sleep(300);
 const lab=await pg.evaluate(()=>{ const t=T.findUseTarget(); return t&&t.label; }); await pg.evaluate(()=>T.useDown());
 await pg.waitForFunction(()=>!T.AB2.down,null,{timeout:20000}).catch(()=>{}); await pg.evaluate(()=>T.useUp());
 ok('teammate knocked, you revive it',d2&&/Revive Buddy/.test(lab||'')&&await pg.evaluate(()=>!T.AB2.down&&!T.AB2.dead),lab);
 // you bleed out: it grabs your card and reboots you at a van
 await pg.evaluate(()=>{ T.P.sh=0; T.hordeHurtMe(999,T.P.pos); }); await sleep(200); await pg.evaluate(()=>{ T.P.hp=0.05; }); await sleep(800);
 const w=await pg.evaluate(()=>({wait:!!T.RB.wait,card:T.RB.cards.has(T.net.id)}));
 await pg.waitForFunction(()=>(T.RB.cards.get(T.net.id)||{}).holder==='ally',null,{timeout:30000}).catch(()=>{}); const held=await pg.evaluate(()=>(T.RB.cards.get(T.net.id)||{}).holder);
 await pg.waitForFunction(()=>!T.RB.wait,null,{timeout:150000}).catch(()=>{});
 const r3=await pg.evaluate(()=>({wait:!!T.RB.wait,dead:T.net.dead,over:T.horde.phase}));
 ok('you bleed out, it carries your card to a van and reboots you',w.wait&&w.card&&held==='ally'&&!r3.wait&&!r3.dead&&r3.over!=='over',JSON.stringify({w,held,r3}));
 // it bleeds out: you grab its card and reboot it
 await pg.waitForFunction(()=>!T.P.sky,null,{timeout:60000}).catch(()=>{});
 await pg.evaluate(()=>{ const A=T.AB2; A.sh=0; A.sky=null; T.allyHurt(999); A.down.hp=0.01; }); await sleep(800);
 const c=await pg.evaluate(()=>{ const c=T.RB.cards.get('ally'); return c&&{x:c.x,y:c.y,z:c.z}; });
 await pg.evaluate(c=>{ T.P.pos.set(c.x+0.8,c.y,c.z); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(0.8,0); },c); await sleep(300); await pg.evaluate(()=>T.useDown());
 await pg.waitForFunction(()=>T.RB.carry.has('ally'),null,{timeout:20000}).catch(()=>{}); await pg.evaluate(()=>T.useUp());
 const v=await pg.evaluate(()=>{ const v=T.VANS[0]; T.P.pos.set(v.tx,v.y+0.05,v.tz); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(-(v.x-v.tx),-(v.z-v.tz)); return v.id; }); await sleep(400);
 await pg.evaluate(()=>T.useDown()); await pg.waitForFunction(()=>!T.AB2.dead,null,{timeout:30000}).catch(()=>{}); await pg.evaluate(()=>T.useUp());
 ok('teammate card: you carry it to a van and reboot it',!!c&&await pg.evaluate(()=>!T.AB2.dead&&T.AB2.active&&!T.RB.cards.has('ally')),JSON.stringify(c));
 R.forEach(x=>console.log(x)); console.log(errs.join('\n')||'no errors'); await b.close(); })();

// reboot cards: in a horde party the guest goes down and drops a card; the host grabs it, takes it to a van, holds
// Interact and the guest comes back from the sky with no loot. Both screens agree at every step.
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,RB,VANS,onHit,useDown,useUp,horde,renderer,settings,camera,findUseTarget,TOWNS',
  '<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+d);
 const H=await open(b,html,{name:'H',fast:!!process.env.FAST,norender:!!process.env.FAST,vp:{width:900,height:520}}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]) await X.pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 for(const X of [H,C]) await X.pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); });
 await H.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Austin']); await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Buddy']);
 await H.pg.evaluate(()=>{ document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('hostBtn').click(); }); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000});
 await sleep(2000); await C.pg.evaluate(()=>document.getElementById('readyBtn').click()); await sleep(1500); await H.pg.evaluate(()=>document.getElementById('startMatch').click()); await sleep(1000);
 await H.pg.evaluate(()=>document.getElementById('play').click()); await C.pg.evaluate(()=>document.getElementById('play').click()); await sleep(3000);
 ok('vans placed',await H.pg.evaluate(()=>T.VANS.length>=4),await H.pg.evaluate(()=>T.VANS.length+' vans'));
 // the guest goes down next to the host
 await C.pg.evaluate(()=>{ T.P.pos.set(T.P.pos.x,T.P.pos.y,T.P.pos.z); T.onHit({id:'zombie',dmg:999,w:'zombie'}); }); await sleep(600); await C.pg.evaluate(()=>{ T.P.hp=0.1; }); await sleep(2500);
 0&&console.log('DBG',await C.pg.evaluate(()=>JSON.stringify({horde:T.horde.on,pl:[...T.net.players.values()].map(p=>({id:p.id,alive:p.alive,team:p.team,flags:p.flags}))})));
 console.log('S',await C.pg.evaluate(()=>JSON.stringify({w:!!T.RB.wait,d:T.net.dead,hp:T.P.hp,role:T.net.role,cards:[...T.RB.cards.keys()]})));
 const s1=await C.pg.evaluate(()=>({wait:!!T.RB.wait,dead:T.net.dead,card:T.RB.cards.has(T.net.id),hud:!document.getElementById('rbWait').hidden})), gid=await C.pg.evaluate(()=>T.net.id);
 await H.pg.waitForFunction(id=>T.RB.cards.has(id),gid,{timeout:30000}).catch(()=>{}); const h1=await H.pg.evaluate(id=>{ const c=T.RB.cards.get(id); return c?{x:c.x,y:c.y,z:c.z}:null; },gid);
 ok('guest waits for a reboot',s1.wait&&s1.dead&&s1.card&&s1.hud,JSON.stringify(s1)); ok('host sees the card',!!h1,JSON.stringify(h1));
 // a look at the card
 await H.pg.evaluate(c=>{ window.cam=new THREE.PerspectiveCamera(50,900/520,0.05,3000); const Rr=T.renderer.render.bind(T.renderer); window.useCam=true; T.renderer.render=(s,cc)=>Rr(s,cc===T.camera&&useCam?cam:cc); cam.position.set(c.x+1.7,c.y+1.5,c.z+1.7); cam.lookAt(c.x,c.y+1.1,c.z); },h1);
 await sleep(1500); await H.pg.screenshot({path:'rb_card.png'});
 await H.pg.evaluate(c=>{ cam.position.set(c.x+14,c.y+6,c.z+14); cam.lookAt(c.x,c.y+4,c.z); },h1); await sleep(800); await H.pg.screenshot({path:'rb_beam.png'});
 // the host walks up and holds Interact
 await H.pg.evaluate(c=>{ T.P.pos.set(c.x+0.8,c.y,c.z); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(0.8,0); },h1); await sleep(400);
 const lab=await H.pg.evaluate(()=>{ const t=T.findUseTarget(); return t&&t.label; });
 await H.pg.evaluate(()=>T.useDown()); await H.pg.waitForFunction(id=>T.RB.carry.has(id),gid,{timeout:20000}).catch(()=>{}); await H.pg.evaluate(()=>T.useUp()); await sleep(1500);
 const s2=await H.pg.evaluate(id=>({carry:T.RB.carry.has(id),hud:!document.getElementById('rbCarry').hidden,txt:document.getElementById('rbCarryT').textContent}),gid);
 const c2=await C.pg.evaluate(()=>({holder:(T.RB.cards.get(T.net.id)||{}).holder,msg:document.getElementById('rbMsg').textContent}));
 ok('grab prompt',/Buddy/.test(lab||''),lab); ok('host carries the card',s2.carry&&s2.hud,JSON.stringify(s2)); ok('guest knows who has it',c2.holder==='h'&&/has your card/.test(c2.msg),JSON.stringify(c2));
 // to the nearest van, hold Interact at its terminal
 const v=await H.pg.evaluate(()=>{ let best=null,bd=1e9; T.VANS.forEach(v=>{ const d=Math.hypot(v.x-T.P.pos.x,v.z-T.P.pos.z); if(d<bd){ bd=d; best=v; } }); return {id:best.id,tx:best.tx,tz:best.tz,x:best.x,z:best.z,y:best.y}; });
 await H.pg.evaluate(v=>{ T.P.pos.set(v.tx,v.y+0.05,v.tz); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(-(v.x-v.tx),-(v.z-v.tz)); cam.position.set(v.tx+(v.tx-v.x)*3.2,v.y+3,v.tz+(v.tz-v.z)*3.2); cam.lookAt(v.x,v.y+1.6,v.z); },v); await sleep(600);
 const lab2=await H.pg.evaluate(()=>{ const t=T.findUseTarget(); return t&&t.label; });
 await H.pg.screenshot({path:'rb_van.png'});
 await H.pg.evaluate(()=>T.useDown()); await H.pg.waitForFunction(()=>T.VANS.some(v=>v.prog>0.4),null,{timeout:60000}).catch(()=>{}); await H.pg.screenshot({path:'rb_van_charge.png'}); await H.pg.waitForFunction(()=>T.RB.carry.size===0,null,{timeout:90000}).catch(()=>{}); await H.pg.evaluate(()=>T.useUp()); await sleep(2500);
 await H.pg.screenshot({path:'rb_van_fire.png'});
 const c3=await C.pg.evaluate(()=>({wait:!!T.RB.wait,dead:T.net.dead,sky:!!T.P.sky,guns:T.P.inv.filter(Boolean).length,card:T.RB.cards.has(T.net.id),y:T.P.pos.y}));
 const h3=await H.pg.evaluate(id=>({card:T.RB.cards.has(id),carry:T.RB.carry.size,cd:T.VANS.find(v=>v.cd>performance.now())!=null,guestAlive:(T.net.players.get(id)||{}).alive}),gid);
 ok('van prompt',/Reboot Buddy/.test(lab2||''),lab2); ok('guest rebooted (no loot)',!c3.wait&&!c3.dead&&c3.guns===0&&!c3.card,JSON.stringify(c3)); ok('host: card gone, van charging',!h3.card&&!h3.carry&&h3.cd,JSON.stringify(h3));
 // solo fallback: guest goes down again, host leaves the party -> no teammates -> guest respawns on their own
 await C.pg.evaluate(()=>{ T.P.sky=null; T.onHit({id:'zombie',dmg:999,w:'zombie'}); }); await sleep(1200); await H.pg.evaluate(()=>{ T.P.hp=0; T.onHit&&0; });
 R.forEach(x=>console.log(x)); console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

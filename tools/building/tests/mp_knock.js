// knocked: in a horde party the guest hits 0 HP and goes down (crawling, 10 HP bleeding); the host revives them
// (back up at 30 HP); knocked again and left alone, they bleed out and their reboot card drops
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,RB,onHit,useDown,useUp,horde,renderer,settings,findUseTarget',
  '<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+d);
 const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]) await X.pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 for(const X of [H,C]) await X.pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); });
 await H.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Austin']); await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Buddy']);
 await H.pg.evaluate(()=>{ document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('hostBtn').click(); }); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000});
 await sleep(2000); await C.pg.evaluate(()=>document.getElementById('readyBtn').click()); await sleep(1500); await H.pg.evaluate(()=>document.getElementById('startMatch').click()); await sleep(1000);
 await H.pg.evaluate(()=>document.getElementById('play').click()); await C.pg.evaluate(()=>document.getElementById('play').click()); await sleep(3000);
 const gid=await C.pg.evaluate(()=>T.net.id);
 await C.pg.evaluate(()=>T.onHit({id:'zombie',dmg:999,w:'zombie'})); await sleep(1500);
 const c1=await C.pg.evaluate(()=>({down:!!T.P.down,hp:+T.P.hp.toFixed(1),dead:T.net.dead,panel:document.getElementById('rbT').textContent}));
 const t0=await C.pg.evaluate(()=>{ const p=T.P.pos.clone(); T.P.vel.set(0,0,0); return [p.x,p.z]; });
 ok('guest knocked, not eliminated',c1.down&&!c1.dead&&c1.hp<=10&&c1.hp>8&&c1.panel==='Knocked',JSON.stringify(c1));
 await H.pg.waitForFunction(id=>{ const pl=T.net.players.get(id); return pl&&(pl.flags&256); },gid,{timeout:15000}).catch(()=>{});
 const h1=await H.pg.evaluate(id=>{ const pl=T.net.players.get(id); T.P.pos.set(pl.pos.x+0.9,pl.pos.y,pl.pos.z); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(0.9,0); return {flag:!!(pl.flags&256)}; },gid); await sleep(300);
 const lab=await H.pg.evaluate(()=>{ const t=T.findUseTarget(); return t&&t.label; });
 ok('host sees them down and gets a Revive prompt',h1.flag&&/Revive Buddy/.test(lab||''),JSON.stringify(h1)+' '+lab);
 await H.pg.evaluate(()=>T.useDown()); await C.pg.waitForFunction(()=>!T.P.down,null,{timeout:20000}).catch(()=>{}); await H.pg.evaluate(()=>T.useUp()); await sleep(800);
 const c2=await C.pg.evaluate(()=>({down:!!T.P.down,hp:Math.round(T.P.hp),dead:T.net.dead}));
 ok('revived at 30 HP',!c2.down&&!c2.dead&&c2.hp===30,JSON.stringify(c2));
 // knocked again; nobody comes: bleed out -> eliminated -> card
 await C.pg.evaluate(()=>T.onHit({id:'zombie',dmg:999,w:'zombie'})); await sleep(500); await C.pg.evaluate(()=>{ T.P.hp=0.2; }); await sleep(2500);
 const c3=await C.pg.evaluate(()=>({down:!!T.P.down,dead:T.net.dead,wait:!!T.RB.wait,card:T.RB.cards.has(T.net.id)}));
 await H.pg.waitForFunction(id=>T.RB.cards.has(id),gid,{timeout:15000}).catch(()=>{}); const h3=await H.pg.evaluate(id=>T.RB.cards.has(id),gid);
 ok('bled out: eliminated with a reboot card',!c3.down&&c3.dead&&c3.wait&&c3.card&&h3,JSON.stringify(c3)+' host card '+h3);
 R.forEach(x=>console.log(x)); console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

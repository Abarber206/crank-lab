// a buggy in a party: the host drives it, a friend sees it move and hops in the passenger seat, the host gets out
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,karts,enterKart,exitKart,simKart','<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const H=await open(b,html,{name:'H',fast:true,norender:true,url:'http://127.0.0.1:9104/'}), C=await open(b,html,{name:'C',fast:true,norender:true,url:'http://127.0.0.1:9104/'});
 for(const X of [H,C]){ await X.pg.waitForFunction(()=>window.T&&T.karts,null,{timeout:120000}); await X.pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); }); }
 await H.pg.evaluate(()=>document.getElementById('hostBtn').click()); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000}); await sleep(2000);
 await H.pg.evaluate(()=>{ const k=T.karts[0]; T.enterKart(k,0); window.__d=setInterval(()=>T.simKart(k,{fw:1,st:0.25,hb:false},0.03),30); });
 await sleep(6000);
 const a=await C.pg.evaluate(()=>{ const k=T.karts[0], pl=[...T.net.players.values()][0]; return {driver:k.driver,moved:+Math.hypot(k.x-k.home.x,k.z-k.home.z).toFixed(1),seated:!!(pl&&pl.kart&&pl.kart.seat===0)}; });
 const hpos=await H.pg.evaluate(()=>{ const k=T.karts[0]; return [k.x,k.z]; }), cpos=await C.pg.evaluate(()=>{ const k=T.karts[0]; return [k.x,k.z]; });
 await H.pg.evaluate(()=>{ clearInterval(window.__d); }); await sleep(2500);
 await C.pg.evaluate(()=>{ const k=T.karts[0]; T.enterKart(k,1); }); await sleep(2500);
 const c=await H.pg.evaluate(()=>{ const k=T.karts[0]; return {seat1:k.seats[1]}; }), gid=await C.pg.evaluate(()=>T.net.id);
 await H.pg.evaluate(()=>{ T.exitKart(true); }); await sleep(3000);
 const d=await C.pg.evaluate(()=>{ const k=T.karts[0]; return {driver:k.driver,pos:[k.x,k.z],me:!!T.P.kart}; }), hk=await H.pg.evaluate(()=>{ const k=T.karts[0]; return [k.x,k.z]; });
 const gap=Math.hypot(d.pos[0]-hk[0],d.pos[1]-hk[1]), lag=Math.hypot(hpos[0]-cpos[0],hpos[1]-cpos[1]);
 const ok=a.driver==='h'&&a.moved>5&&a.seated&&c.seat1===gid&&d.driver===null&&gap<1&&d.me;
 console.log((ok?'PASS':'FAIL')+' driving, riding along and parking sync — '+JSON.stringify({a,lagWhileDriving:+lag.toFixed(2),c,gid,d,parkedGap:+gap.toFixed(2)}));
 console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

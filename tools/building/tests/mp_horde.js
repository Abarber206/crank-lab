// two players in a horde match: the guest sees the host's creatures (all four kinds) and a Hurler's throw, no errors either side
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,horde,newZombie,gooL,settings,ZT,renderer',
  '<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+d);
 const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]) await X.pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await H.pg.evaluate(()=>{ document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('hostBtn').click(); }); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000});
 await sleep(2000); console.log('before start: guest',await C.pg.evaluate(()=>T.net.role));
 await C.pg.evaluate(()=>document.getElementById('readyBtn').click()); await sleep(1500); await H.pg.evaluate(()=>{ document.getElementById('startMatch').click(); }); await sleep(1000);
 await H.pg.evaluate(()=>document.getElementById('play').click()); await C.pg.evaluate(()=>document.getElementById('play').click());
 await H.pg.waitForFunction(()=>T.horde.on,null,{timeout:60000});
 await H.pg.evaluate(()=>{ T.horde.t=999; ['husk','runner','brute'].forEach((t,i)=>T.newZombie(t,T.P.pos.x+(i-1)*3,T.P.pos.z-30)); const z=T.newZombie('hurler',T.P.pos.x,T.P.pos.z-15); z.thrCd=0; });
 await C.pg.evaluate(()=>{ window.SAWG=0; (function w(){ window.SAWG=Math.max(window.SAWG,T.gooL.length); requestAnimationFrame(w); })(); });
 let seen=null; for(let i=0;i<40;i++){ await sleep(1500); await H.pg.evaluate(()=>{ T.horde.t=999; });
   console.log('t',i,'host frame',await H.pg.evaluate(()=>T.renderer.info.render.frame),'guest',await C.pg.evaluate(()=>T.net.role+' gap '+Math.round(performance.now()-(T.net.hostSeen||0))+' toast '+document.getElementById('toast').textContent));
   seen=await C.pg.evaluate(()=>({on:T.horde.on,kinds:[...new Set([...T.horde.zs.values()].map(z=>z.type))].sort().join(','),goo:window.SAWG})); if(seen.kinds.split(',').length>=4&&seen.goo>0) break; }
 console.log('host conns',await H.pg.evaluate(()=>JSON.stringify([...T.net.conns.values()].map(c=>c.open))),'host horde',await H.pg.evaluate(()=>T.horde.on+' '+T.horde.zs.size+' role '+T.net.role),'guest',await C.pg.evaluate(()=>T.net.role+' hostOpen '+(T.net.host&&T.net.host.open)));
 ok('the guest sees all four kinds of creature',seen.kinds.split(',').length>=4,JSON.stringify(seen));
 ok('the guest sees a Hurler throw',seen.goo>0,'chunks seen '+seen.goo);
 console.log(R.join('\n')); console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

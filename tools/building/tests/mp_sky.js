// a player skydiving and then gliding shows that way on a friend's screen
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9102,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,terrainH','<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9102,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]){ await X.pg.waitForFunction(()=>window.T&&T.P,null,{timeout:120000}); await X.pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); }); }
 await H.pg.evaluate(()=>document.getElementById('hostBtn').click()); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.fill('#jcode',code); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000}); await sleep(2000);
 const setPhase=ph=>H.pg.evaluate(ph=>{ clearInterval(window.__k); const P=T.P; window.__k=setInterval(()=>{ P.pos.y=T.terrainH(P.pos.x,P.pos.z)+200; P.vel.set(0,ph==='fall'?-40:-6.5,0); P.onGround=false; P.sky={phase:ph,t:2,dive:0,jumpWas:false,gt:1}; },30); },ph);
 const look=()=>C.pg.evaluate(()=>{ const pl=[...T.net.players.values()][0]; if(!pl) return null; const g=pl.h.group; return {flags:pl.flags, rx:+g.rotation.x.toFixed(2), glider:!!(pl.h.glider&&pl.h.glider.visible)}; });
 await setPhase('fall'); await sleep(5000); const f=await look();
 await setPhase('glide'); await sleep(5000); const g=await look();
 await H.pg.evaluate(()=>{ clearInterval(window.__k); T.P.sky=null; T.P.pos.y=T.terrainH(T.P.pos.x,T.P.pos.z); T.P.vel.set(0,0,0); T.P.onGround=true; }); await sleep(6000); const n=await look();
 const ok=f&&(f.flags&64)&&f.rx<-0.8&&!f.glider && g&&(g.flags&128)&&g.glider&&g.rx>-0.4 && n&&!(n.flags&192)&&!n.glider&&Math.abs(n.rx)<0.05;
 console.log((ok?'PASS':'FAIL')+' freefall / glide / landed seen by the guest — '+JSON.stringify({f,g,n}));
 console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

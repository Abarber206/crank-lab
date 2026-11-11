// a party match: both players drop from high up close together, with just a pickaxe
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9103,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,terrainH,startMatch','<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9103,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]){ await X.pg.waitForFunction(()=>window.T&&T.P,null,{timeout:180000}); await X.pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); }); }
 await H.pg.evaluate(()=>document.getElementById('hostBtn').click()); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000}); await sleep(2000);
 await H.pg.evaluate(()=>T.startMatch()); await sleep(1500); const early=await C.pg.evaluate(()=>!!T.P.sky);
 await C.pg.evaluate(()=>document.getElementById('readyBtn').click()); await sleep(2000); await H.pg.evaluate(()=>T.startMatch()); await sleep(3000);
 const st=pg=>pg.evaluate(()=>({x:T.P.pos.x,z:T.P.pos.z,h:Math.round(T.P.pos.y-T.terrainH(T.P.pos.x,T.P.pos.z)),sky:T.P.sky&&T.P.sky.phase,inv:T.P.inv.filter(Boolean).length}));
 const h=await st(H.pg), g=await st(C.pg), d=Math.hypot(h.x-g.x,h.z-g.z);
 console.log((!early&&h.sky&&g.sky&&h.h>400&&g.h>400&&d<25&&h.inv===0&&g.inv===0?'PASS':'FAIL')+' '+JSON.stringify({host:h,guest:g,apart:+d.toFixed(1),startedBeforeReady:early}));
 console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

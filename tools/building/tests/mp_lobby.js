// party lobby: both players show on the host's stage with name tags; the guest's tag shows Ready after readying up
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,party,renderer','<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch();
 const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]) await X.pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await H.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Austin']); await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Buddy']);
 await H.pg.evaluate(()=>document.getElementById('hostBtn').click()); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['jcode',code]); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000});
 await sleep(2500); await C.pg.evaluate(()=>document.getElementById('readyBtn').click()); await H.pg.waitForFunction(()=>/Ready/.test(document.getElementById('lobbyPlates').textContent),null,{timeout:20000}).catch(()=>{}); await sleep(800);
 const plates=await H.pg.evaluate(()=>[...document.querySelectorAll('#lobbyPlates span')].map(s=>s.textContent));

 console.log(JSON.stringify(plates), plates.length===2&&/Buddy.*Ready/.test(plates.join())?'PASS':'FAIL');
 console.log([...H.errs,...C.errs].join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

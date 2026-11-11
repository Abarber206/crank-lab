// friends: B adds A by account number, A accepts the request, both see each other online; A invites B to the lobby,
// B presses Join and is in A's party, standing on A's lobby pads. Needs the peer and express packages.
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,party,FR,LOBBY','<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9101,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const res=[]; const ok=(n,c,d)=>{ res.push(c); console.log((c?'PASS ':'FAIL ')+n+(d!==undefined?' — '+JSON.stringify(d):'')); };
 const A=await open(b,html,{name:'A',fast:true,norender:true}), B=await open(b,html,{name:'B',fast:true,norender:true});
 for(const X of [A,B]) await X.pg.waitForFunction(()=>window.T&&T.FR&&T.FR.peer&&T.FR.peer.open,null,{timeout:180000});
 await A.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Austin']); await B.pg.evaluate(([i,v])=>{ document.getElementById(i).value=v; },['pname','Buddy']);
 const aId=await A.pg.evaluate(()=>T.FR.acct), bId=await B.pg.evaluate(()=>T.FR.acct); ok('account numbers',/^\d{8}$/.test(aId)&&/^\d{8}$/.test(bId)&&aId!==bId,[aId,bId]);
 ok('number shown on Profile',await A.pg.evaluate(()=>document.getElementById('acctNum').textContent.replace(/\s/g,''))===aId);
 await B.pg.evaluate(id=>{ document.getElementById('fAdd').value=id; document.getElementById('fAddBtn').click(); },aId.slice(0,4)+' '+aId.slice(4));
 await A.pg.waitForFunction(id=>T.FR.list.some(f=>f.id===id&&f.st==='in'),bId,{timeout:40000}).catch(()=>{});
 const req=await A.pg.evaluate(()=>({list:T.FR.list,btn:!!document.querySelector('#fReqs [data-acc]'),tab:document.querySelector('.mtabs button[data-tab=friends]').textContent})); ok('A gets the request',req.btn&&/\(1\)/.test(req.tab),req);
 await A.pg.evaluate(()=>document.querySelector('#fReqs [data-acc]').click());
 await B.pg.waitForFunction(id=>T.FR.list.some(f=>f.id===id&&f.st==='friend'),aId,{timeout:30000}).catch(()=>{});
 const both=[await A.pg.evaluate(id=>({f:(T.FR.list.find(f=>f.id===id)||{}).st,on:T.FR.online.has(id),name:(T.FR.list.find(f=>f.id===id)||{}).name}),bId),await B.pg.evaluate(id=>({f:(T.FR.list.find(f=>f.id===id)||{}).st,on:T.FR.online.has(id),name:(T.FR.list.find(f=>f.id===id)||{}).name}),aId)];
 ok('friends on both sides, online, with names',both.every(x=>x.f==='friend'&&x.on)&&both[0].name==='Buddy'&&both[1].name==='Austin',both);
 await A.pg.evaluate(id=>document.querySelector('#fList [data-inv="'+id+'"]').click(),bId);
 await B.pg.waitForFunction(()=>!document.getElementById('invitePop').hidden,null,{timeout:40000}).catch(()=>{});
 const pop=await B.pg.evaluate(()=>({shown:!document.getElementById('invitePop').hidden,text:document.getElementById('invText').textContent})); ok('B gets the invite',pop.shown&&/Austin/.test(pop.text),pop);
 await B.pg.evaluate(()=>document.getElementById('invJoin').click());
 await B.pg.waitForFunction(()=>T.net.role==='client',null,{timeout:60000}).catch(()=>{}); await sleep(3500);
 const codes=[await A.pg.evaluate(()=>[T.net.role,T.net.code]),await B.pg.evaluate(()=>[T.net.role,T.net.code])]; ok('B is in A\'s party',codes[0][0]==='host'&&codes[1][0]==='client'&&codes[0][1]===codes[1][1],codes);
 const lob=await A.pg.evaluate(()=>[...document.querySelectorAll('#lobbyPlates span')].map(s=>s.textContent)); ok('both on A\'s lobby pads',lob.length===2&&lob.some(t=>/Buddy/.test(t)),lob);
 console.log([...A.errs,...B.errs].filter(e=>!/peer-unavailable|Could not connect to peer/.test(e)).join('\n')||'no errors'); console.log(res.every(Boolean)?'ALL PASS':'SOME FAILED'); await b.close(); srv.close(); process.exit(0); })();

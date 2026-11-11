// in a party, a rifle shot is seen by the other player as a bullet in flight (a harmless one), not an instant line
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9101,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,P,net,renderer,settings,bullets,WEAPONS,selectGun,playerShoot,terrainH',
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
 const fire=()=>H.pg.evaluate(()=>{ T.P.inv[0]='sniper'; T.P.ammo.sniper=1; T.selectGun('sniper'); T.P.equipT=0; T.P.gunT=0; T.P.reloadT=0; T.P.pitch=0.5; });
 await fire(); await sleep(600); const hp0=await C.pg.evaluate(()=>T.P.hp+T.P.sh);
 await H.pg.evaluate(()=>{ T.P.pitch=0.5; T.P.gunT=0; T.P.equipT=0; T.playerShoot(); });
 let seen=null; for(let q=0;q<40&&!seen;q++){ seen=await C.pg.evaluate(()=>{ const g=T.bullets.find(b=>b.ghost); return g?{ghost:true,speed:Math.round(g.v.length()),n:T.bullets.length}:null; }); if(!seen) await sleep(25); }
 const own=await H.pg.evaluate(()=>T.bullets.filter(b=>!b.ghost).length); await sleep(2500);
 const after=await C.pg.evaluate(()=>({left:T.bullets.length,hp:T.P.hp+T.P.sh}));
 ok('the guest sees the bullet fly',!!seen&&seen.ghost&&Math.abs(seen.speed-300)<12,JSON.stringify(seen)+' host own '+own);
 ok('it lands or runs out and does no harm',after.left===0&&after.hp===hp0,JSON.stringify(after));
 console.log(R.join('\n')); console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

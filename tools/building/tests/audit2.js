// polish audit, part 2: horde HUD on desktop and phones, knocked panel, menus
const {sleep,page,launch}=require('./h.js'); const fs=require('fs'); const path=require('path');
(async()=>{ const b=await launch();
 const mk=async(vp,touch)=>{ const ctx=await b.newContext(Object.assign({viewport:vp},touch?{hasTouch:true,isMobile:true,deviceScaleFactor:1}:{})); const pg=await ctx.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
   const NM=path.join(__dirname,'node_modules'); for(const [pat,f] of [['**/three.min.js','three/build/three.min.js'],['**/peerjs.min.js','peerjs/dist/peerjs.min.js']]) await pg.route(pat,r=>r.fulfill({body:fs.readFileSync(path.join(NM,f)),contentType:'text/javascript'}));
   await pg.route('https://fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
   const html=page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,horde,newZombie,hordeHurtMe,net,get AB2(){return AB}').replace('<script>\n','<script>\ntry{ localStorage.setItem("cranklab.settings",JSON.stringify({shadows:'+(!touch)+',grassLevel:"'+(touch?'off':'medium')+'",clouds:"simple",skyDrop:false,bot:"off",hordeBot:true,mode:"horde"})); }catch(e){}\n');
   await pg.route('http://127.0.0.1:9101/',r=>r.fulfill({body:html,contentType:'text/html'})); await pg.goto('http://127.0.0.1:9101/'); await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); return {pg,errs,ctx}; };
 const run=async(tag,vp,touch)=>{ const {pg,errs,ctx}=await mk(vp,touch); const shot=async(nm,fn)=>{ try{ if(fn) await pg.evaluate(fn); await sleep(3000); await pg.screenshot({path:'au_'+tag+'_'+nm+'.png'}); console.log('shot',tag,nm); }catch(e){ console.log('ERR',tag,nm,String(e).slice(0,160)); } };
   await sleep(2500); await shot('lobby');
   if(tag==='desk'){ await pg.click('[data-tab=settings]'); await shot('settings'); await pg.click('[data-tab=controls]'); await shot('controls'); await pg.click('[data-tab=play]'); }
   await pg.evaluate(()=>document.getElementById('play').click()); await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(2500);
   await shot('break',()=>{ T.P.yaw=0.5; });
   await shot('wave',()=>{ T.horde.t=0.01; }); await sleep(1500);
   await shot('zombies',()=>{ const p=T.P.pos, f=[-Math.sin(T.P.yaw),-Math.cos(T.P.yaw)]; for(let i=0;i<5;i++) T.newZombie(['husk','runner','brute','hurler','husk'][i],p.x+f[0]*(7+i*1.5)+(i-2)*1.6,p.z+f[1]*(7+i*1.5)); });
   await shot('knocked',()=>{ T.horde.zs.forEach(z=>z.alive=false); T.P.sh=0; T.hordeHurtMe(999,T.P.pos); });
   console.log(tag,errs.join(';')||'no errors'); await ctx.close(); };
 await run('desk',{width:1100,height:640},false);
 await run('port',{width:390,height:844},true);
 await run('land',{width:844,height:390},true);
 await b.close(); })();

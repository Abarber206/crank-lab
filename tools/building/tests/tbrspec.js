// BR end of life: eliminated -> summary with stats -> spectate (camera follows a living bot, Next cycles) -> lobby;
// the feed names the weapon and distance; inside the storm the view goes purple
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,camera,renderer,brHurtMe,brHurtBot,WEAPONS,SPAWN,terrainH,TOD,renderMain'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(1500);
 const r={};
 // the storm: stand outside it
 await pg.evaluate(()=>{ T.TOD.fix=0.3; const S=T.BR.storm; T.P.sky=null; T.P.bus=false; S.r=40; const x=S.cx+120, z=S.cz; T.P.pos.set(x,T.terrainH(x,z)+0.1,z); T.P.hp=1e6; }); await sleep(4000);
 { const u=await pg.evaluate(()=>{ T.BR.stK=1; T.renderMain(); return T.renderer.domElement.toDataURL('image/jpeg',0.85); }); require('fs').writeFileSync('/home/claude/work/br_storm.jpg',Buffer.from(u.split(',')[1],'base64')); }
 r.stK=await pg.evaluate(()=>+(T.BR.stK||0).toFixed(2));
 // a kill by you, then you get eliminated
 await pg.evaluate(()=>{ const S=T.BR.storm; S.r=5000; T.P.hp=100; const v=T.BR.bots.find(b=>b.alive); v.sky=null; v.bus=false; T.WEAPONS; T.P.wpn=T.P.wpn||'ar'; T.brHurtBot(v,500,null,null); const k=T.BR.bots.find(b=>b.alive); k.sky=null; k.bus=false; k.pos.set(T.P.pos.x+20,T.P.pos.y,T.P.pos.z); k.wpn=k.wpn||'ar'; T.brHurtMe(500,k); });
 await sleep(2500);
 r.feed=await pg.evaluate(()=>document.getElementById('feed')?document.getElementById('feed').innerText.slice(0,300):'');
 r.end=await pg.evaluate(()=>({shown:!document.getElementById('brEnd').hidden,place:document.getElementById('brEndP').textContent,by:document.getElementById('brEndBy').textContent,k:document.getElementById('brEndK').textContent,d:document.getElementById('brEndD').textContent,t:document.getElementById('brEndT').textContent}));
 { const u=await pg.evaluate(()=>T.renderer.domElement.toDataURL('image/jpeg',0.85)); }
 await pg.screenshot({path:'/home/claude/work/br_end.png',timeout:150000}).catch(()=>{});
 await pg.evaluate(()=>document.getElementById('brEndS').click()); await sleep(1500);
 r.spec=await pg.evaluate(()=>({tag:!document.getElementById('specTag').hidden,name:document.getElementById('specName').textContent,d:T.BR.spec?+T.camera.position.distanceTo(T.BR.spec.pos).toFixed(1):null}));
 await pg.screenshot({path:'/home/claude/work/br_spec.png',timeout:150000}).catch(()=>{});
 await pg.evaluate(()=>document.getElementById('specNext').click()); await sleep(800); r.spec2=await pg.evaluate(()=>document.getElementById('specName').textContent);
 await pg.evaluate(()=>document.getElementById('specLeave').click()); let off=false; for(let q=0;q<8&&!off;q++){ await sleep(500); off=await pg.evaluate(()=>!T.BR.on); } r.left=off;
 console.log(JSON.stringify(r,null,1));
 const ok=r.stK>0.2&&r.end.shown&&r.spec.tag&&r.spec.d<25&&r.spec2!==r.spec.name&&r.left;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

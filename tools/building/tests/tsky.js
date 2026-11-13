// far skydivers: baked in the freefall pose and under a glider (not a tilted A-pose), baked ahead, and pictured
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,renderer,TOWNS,terrainH,camera,BOT_SKY,BOT_SKYQ,localHero,TOD'),{vp:{width:900,height:560},log:false});
 pg.on('console',m=>{ if(m.type()==='warning') console.log('  [warn]',m.text().slice(0,200)); });
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(3000);
 const q0=await pg.evaluate(()=>({baked:T.BOT_SKY.size,q:T.BOT_SKYQ.length,outfits:new Set(T.BR.bots.map(b=>b.h&&b.h.outfit)).size}));
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T*0.55; T.scene.visible=false; }); await sleep(1500);
 await pg.evaluate(()=>{ const t=T.TOWNS.find(t=>t.name==='Gearworks'); T.P.sky=null; T.P.bus=false; T.P.pos.set(t.x,T.terrainH(t.x,t.z)+0.1,t.z); T.P.hp=1e6; }); await sleep(6000); await pg.evaluate(()=>{ T.scene.visible=true; });
 const r=await pg.evaluate(()=>{ const k={}; T.BR.bots.forEach(b=>{ const s=(b.sky?b.sky.phase:'-')+'/'+(b.far&&b.far.visible?b.farK:'near-or-hidden'); k[s]=(k[s]||0)+1; }); return {baked:T.BOT_SKY.size,q:T.BOT_SKYQ.length,k,keys:[...T.BOT_SKY.keys()].slice(0,4)}; });
 await pg.evaluate(()=>{ const bb=T.BR.bots.filter(b=>b.sky&&b.sky.phase==='fall'&&b.far&&b.far.visible)[3]; if(bb){ bb.sky.phase='glide'; bb._forced=1; } }); await sleep(2500);
 // a picture: one falling and one gliding bot, from close behind and below
 for(const ph of ['fall','glide']){ const u=await pg.evaluate(ph=>{ const bb=T.BR.bots.find(b=>b.sky&&b.sky.phase===ph&&b.far&&b.far.visible&&b.farK===ph); if(!bb) return null; T.TOD.fix=0.3; const cam=new THREE.PerspectiveCamera(40,900/560,0.1,3000), p=bb.far.position;
     cam.position.set(p.x+5,p.y-2.5,p.z+5); cam.lookAt(p.x,p.y+0.6,p.z); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },ph);
   if(u) require('fs').writeFileSync(`/home/claude/work/sky_${ph}.jpg`,Buffer.from(u.split(',')[1],'base64')); else console.log('no',ph,'bot drawn far'); }
 console.log(JSON.stringify(q0),JSON.stringify(r)); const ok=r.baked>=2&&r.q===0&&!Object.keys(r.k).some(s=>/^(fall|glide)\/stand/.test(s));
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

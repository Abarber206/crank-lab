// material icons from 3D models with count badges; the gun stats card (ground and inventory)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,settings,TOD,ICON_IMG,syncMats,spawnDrop,camera,terrainH,statCard'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.renderer.info.render.frame>5,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.infMats=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(8000); await pg.evaluate(()=>{ T.TOD.fix=0.3; T.P.mats={wood:120,brick:45,metal:7}; T.syncMats(); }); await pg.waitForFunction(()=>["mat_wood","mat_brick","mat_metal"].every(k=>T.ICON_IMG.has(k)),null,{timeout:60000}).catch(()=>{}); await sleep(1000); await pg.evaluate(()=>T.syncMats()); await sleep(500);
 const st=await pg.evaluate(()=>({mats:['mat_wood','mat_brick','mat_metal'].map(k=>!!T.ICON_IMG.get(k)),stock:document.getElementById('matStock').innerHTML.slice(0,160),hidden:document.getElementById('matStock').hidden}));
 console.log(JSON.stringify(st)); await pg.screenshot({path:'/home/claude/work/icons_hud.png'});
 // the mats themselves, big
 for(const k of ['mat_wood','mat_brick','mat_metal']){ const u=await pg.evaluate(k=>T.ICON_IMG.get(k),k); if(u) require('fs').writeFileSync('/home/claude/work/icon_'+k+'.png',Buffer.from(u.split(',')[1],'base64')); }
 // a gun on the ground in front of you
 await pg.evaluate(()=>{ const fx=-Math.sin(T.P.yaw), fz=-Math.cos(T.P.yaw), x=T.P.pos.x+fx*1.3, z=T.P.pos.z+fz*1.3; T.spawnDrop('pump_l',5,new THREE.Vector3(x,T.terrainH(x,z)+0.6,z),new THREE.Vector3()); T.P.pitch=-0.5; }); await sleep(3500);
 const card=await pg.evaluate(()=>{ const lc=document.getElementById('lootCard'); return {hidden:lc.hidden,txt:lc.textContent.slice(0,120)}; }); console.log(JSON.stringify(card)); await pg.screenshot({path:'/home/claude/work/icons_card.png'});
 await pg.keyboard.press('Tab'); await sleep(1500); await pg.screenshot({path:'/home/claude/work/icons_inv.png'});
 const ok=st.mats.every(Boolean)&&!card.hidden&&/Damage/.test(card.txt);
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

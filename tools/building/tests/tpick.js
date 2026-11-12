// the pickaxe at rest: the hero standing still with the pickaxe out, seen from the side and from behind.  FILE=... node tpick.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/pk'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,localHero,terrainH,TOD,selectGun'),{vp:{width:700,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.localHero,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(2500);
 await pg.evaluate(()=>{ window.__v=0; const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera){ const p=T.localHero.group.position, y=T.P.yaw+[Math.PI/2,Math.PI*0.8][window.__v]; c.position.set(p.x-Math.sin(y)*2.6,p.y+1.4,p.z-Math.cos(y)*2.6); c.lookAt(p.x,p.y+1.1,p.z); c.updateMatrixWorld(); } R(s,c); }; });
 await sleep(2500); await pg.screenshot({path:pre+'_side.png',timeout:200000}); await pg.evaluate(()=>{ window.__v=1; }); await sleep(1500); await pg.screenshot({path:pre+'_back.png',timeout:200000});
 const st=await pg.evaluate(()=>{ const r=T.localHero.rig, v=new THREE.Vector3(), h=new THREE.Vector3(); r.pick.children[0].getWorldPosition(v); r.head.getWorldPosition(h); return {pickVis:r.pick.visible,pickTopAboveHead:+(v.y-h.y).toFixed(2),inv:T.P.inv&&T.P.inv.slice?T.P.inv.slice(0,3):null,sel:T.P.sel}; }); console.log(JSON.stringify(st));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

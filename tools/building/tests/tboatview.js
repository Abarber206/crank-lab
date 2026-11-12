// pictures of a moored boat from four sides and from above, close up.  node tboatview.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/bv'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,karts,waterDepth,TOD'),{vp:{width:900,height:600}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 await pg.evaluate(()=>{ const k=T.karts.filter(k=>k.boat).sort((a,b)=>T.waterDepth(b.x,b.z)-T.waterDepth(a.x,a.z))[0]; window.__k=k; T.P.pos.set(k.x+8,k.y+30,k.z); window.__v={a:0,d:6,h:2.5};
   const set=()=>{ const v=window.__v, c=T.camera, y=k.yaw+v.a; c.position.set(k.x-Math.sin(y)*v.d,k.y+v.h,k.z-Math.cos(y)*v.d); c.lookAt(k.x,k.y+0.5,k.z); c.updateMatrixWorld(); };
   const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera) set(); R(s,c); }; const G=T.camera.getWorldDirection.bind(T.camera); T.camera.getWorldDirection=v=>{ set(); return G(v); }; });
 const only=(process.env.VIEWS||'').split(',').filter(Boolean); for(const [nm,v] of [['front',{a:0,d:4,h:1.6}],['side',{a:Math.PI/2,d:4,h:1.2}],['back',{a:Math.PI,d:4,h:1.8}],['q',{a:Math.PI*0.75,d:4.5,h:3.2}],['top',{a:Math.PI*0.9,d:1.5,h:6}],['drv',{a:Math.PI,d:1.3,h:1.9}],['bowlow',{a:0.35,d:3,h:0.8}]]){ if(only.length&&!only.includes(nm)) continue; await pg.evaluate(v=>{ window.__v=v; },v); await sleep(2200); await pg.screenshot({path:pre+'_'+nm+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

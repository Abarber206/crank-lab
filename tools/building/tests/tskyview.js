// pictures from high in the sky over a town (for depth fighting and shadow banding): node tskyview.js out-prefix [height] [pitch] [yaw] [town]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,camera,skyDrop,deployGlider,sun,sunFar,TOD,SUN_DIR'),{vp:{width:1000,height:620}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000});
 const [pre,hgt,pit,yw,tn,glide]=[process.argv[2]||'/home/claude/work/sky',+(process.argv[3]||450),+(process.argv[4]||-0.75),+(process.argv[5]||0.6),+(process.argv[6]||2),process.env.GLIDE];
 if(process.env.TODF) await pg.evaluate(v=>{ T.TOD.fix=v; },+process.env.TODF);
 const r=await pg.evaluate(([h,pit,yw,tn,gl])=>{ const t=T.TOWNS[tn], x=t.x+Math.sin(yw)*h*0.9, z=t.z+Math.cos(yw)*h*0.9; T.skyDrop(x,z,h); if(gl) T.deployGlider(T.P); const hold=T.P.pos.clone();
   const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera){ T.P.pos.copy(hold); T.P.vel.set(0,-0.01,0); T.P.yaw=yw; T.P.pitch=pit; } R(s,c); }; return {x,z,h,near:T.camera.near,far:T.camera.far}; },[hgt,pit,yw,tn,glide]);
 console.log(JSON.stringify(r)); await sleep(2500); await pg.screenshot({path:pre+'_a.png',timeout:200000}); await sleep(300); await pg.screenshot({path:pre+'_b.png',timeout:200000});
 console.log(JSON.stringify(await pg.evaluate(()=>({near:T.camera.near,y:T.P.pos.y,sky:T.P.sky&&T.P.sky.phase})))); console.log(errs.join('\n')||'no errors'); await b.close(); })();

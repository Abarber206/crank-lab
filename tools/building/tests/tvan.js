// pictures of a Reboot Van from four sides (and its terminal screen close up): node tvan.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/van'; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,get VANS(){return VANS},terrainH,TOD'),{vp:{width:900,height:560}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.VANS&&T.VANS.length,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.22; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 for(const [nm,a,d,h] of [['back',-0.6,7.5,1.6],['side',1.57,7,1.5],['front',3.6,7.5,2.0],['term',1.4,3.4,1.7],['roof',2.4,6,4.5]].filter(v=>!process.env.VIEWS||process.env.VIEWS.split(',').includes(v[0]))){
  await pg.evaluate(([a,d,h])=>{ const v=T.VANS[0]; T.P.pos.set(v.x+30,T.terrainH(v.x+30,v.z)+0.1,v.z); const ya=v.yaw+a; window.__cam={p:[v.x+Math.sin(ya)*d,v.y+h,v.z+Math.cos(ya)*d],t:[v.x,v.y+1.4,v.z]};
    if(!window.__hk){ window.__hk=1; const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera&&window.__cam){ c.position.set(...window.__cam.p); c.lookAt(...window.__cam.t); c.updateMatrixWorld(); } R(s,c); }; } },[a,d,h]);
  await sleep(2500); await pg.screenshot({path:pre+'_'+nm+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

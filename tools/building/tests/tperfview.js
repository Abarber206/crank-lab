// screenshot of the town with the Performance preset (shadows on alternate frames, LODs, merged vans) and the FPS counter.  node tperfview.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,TOD,PERF,camera,FPS,fpsTick,get playing(){return playing},get locked(){return locked}'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(14000);
 await pg.evaluate(()=>{ const t=T.TOWNS[0]; T.P.pos.set(t.x+6,T.terrainH(t.x+6,t.z+4)+0.05,t.z+4); T.P.yaw=0.6; T.P.pitch=-0.12; T.P.vel.set(0,0,0); });
 await sleep(15000);
 await pg.evaluate(()=>{ const n=performance.now()+1e4; for(let i=0;i<80;i++) T.fpsTick(6,n+i*6.5); });
 const r=await pg.evaluate(()=>({dbg:[T.playing,T.locked,T.FPS,T.settings.showFps,document.querySelector('#fpsHud').hidden,getComputedStyle(document.querySelector('#fpsHud')).display],target:T.PERF.target,auto:T.renderer.shadowMap.autoUpdate,fps:(document.querySelector('#fpsHud')||{}).textContent,fpsVis:!!document.querySelector('#fpsHud')&&getComputedStyle(document.querySelector('#fpsHud')).display!=='none'}));
 await pg.screenshot({path:'perf_town.png'}); console.log(JSON.stringify(r));
 const ok=r.target===165&&r.auto===false&&r.fpsVis; console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

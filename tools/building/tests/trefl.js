// reflections beside tall ground: from a boat's height on the sea near cliffs, looking along the shore with the
// cliffs off to one side, and turned a little each way.  FILE=... node trefl.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/rf'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,SPAWN,terrainH,waterAt,waterDepth,TOD'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.SPAWN,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const sp=await pg.evaluate(()=>{ const S=T.SPAWN; for(let k=0;k<300000;k++){ const a=k*2.399, d=300+(k%3000)*0.17, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d; if(T.waterDepth(x,z)<2) continue;
   for(let q=0;q<16;q++){ const aa=q*Math.PI/8, cx=x+Math.cos(aa)*70, cz=z+Math.sin(aa)*70; if(T.terrainH(cx,cz)>22&&T.waterDepth(x+Math.cos(aa+1.57)*60,z+Math.sin(aa+1.57)*60)>0.5) return {x,z,w:T.waterAt(x,z),aa}; } } return null; });
 console.log(JSON.stringify(sp)); if(!sp){ await b.close(); return; }
 await pg.evaluate(sp=>{ T.P.pos.set(sp.x,sp.w-1.2,sp.z); T.P.vel.set(0,0,0); window.__cam=1; window.__yaw=sp.aa+1.57-0.9; const set=()=>{ const c=T.camera, y=window.__yaw; c.position.set(sp.x,sp.w+2.6,sp.z); c.lookAt(sp.x+Math.cos(y)*50,sp.w+0.5,sp.z+Math.sin(y)*50); c.updateMatrixWorld(); };
   const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera) set(); R(s,c); }; const G=T.camera.getWorldDirection.bind(T.camera); T.camera.getWorldDirection=v=>{ set(); return G(v); }; },sp);
 for(const [nm,dy] of [['a',0],['b',0.5]]){ await pg.evaluate(dy=>{ window.__yaw+=dy; },dy); await sleep(3000); await pg.screenshot({path:pre+'_'+nm+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

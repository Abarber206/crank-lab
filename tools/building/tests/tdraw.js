// drawing work per frame (calls, triangles, far-shadow redraws, terrain meshes built) standing, skydiving and gliding
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,skyDrop,deployGlider,SPAWN,FARS,sunFar,TERR,camera'),{vp:{width:640,height:400}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click();
   const I=T.renderer.info; I.autoReset=false; window.__F={calls:0,tris:0,n:0,far:0,lastT:0,chunks:0}; const R=T.renderer.render.bind(T.renderer); let lastFrame=-1;
   T.renderer.render=(s,c)=>{ if(c===T.camera){ const F=window.__F; F.calls+=I.render.calls; F.tris+=I.render.triangles; F.n++; if(T.FARS.t!==F.lastT){ F.far++; F.lastT=T.FARS.t; } I.reset(); } R(s,c); }; });
 await sleep(4000);
 const meas=async(label,setup)=>{ await pg.evaluate(setup); await sleep(2500); await pg.evaluate(()=>{ Object.assign(window.__F,{calls:0,tris:0,n:0,far:0}); window.__ch0=T.TERR.chunks.reduce((a,c)=>a+c.m.filter(Boolean).length,0); });
   await sleep(5000); const F=await pg.evaluate(()=>({...window.__F,y:Math.round(T.P.pos.y),ch:T.TERR.chunks.reduce((a,c)=>a+c.m.filter(Boolean).length,0)-window.__ch0})); console.log(label,JSON.stringify({frames:F.n,calls:Math.round(F.calls/F.n),ktris:Math.round(F.tris/F.n/1000),farShadowRedraws:F.far,newTerrainMeshes:F.ch,y:F.y})); };
 await meas('standing',()=>{});
 await meas('skydiving',()=>{ const S=T.SPAWN; T.skyDrop(S[0]+80,S[2]-120,560); });
 await meas('gliding',()=>{ const S=T.SPAWN; T.skyDrop(S[0]-200,S[2]+90,200); T.deployGlider(T.P); });
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

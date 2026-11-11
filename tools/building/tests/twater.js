// pictures of water joins: where each river reaches the sea and where streams join the main river, from a person's eye
// height on the bank, looking along the water.  node twater.js out-prefix [which...]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/wj'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,WORLD,SPAWN,terrainH,waterAt,TOD'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.WORLD,null,{timeout:180000}); if(process.env.NOREFL) await pg.evaluate(()=>{ window.__norefl=1; });
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.22; if(window.__norefl) T.settings.reflect=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const spots=await pg.evaluate(()=>{ const S=T.SPAWN, out=[]; T.WORLD.rivers.forEach((rv,i)=>{ const p=rv.pts, n=p.length; let q=n-1;
     if(rv.into>=0){ out.push({nm:'join'+i,x:S[0]+p[n-1][0],z:S[2]+p[n-1][1],dx:p[n-1][0]-p[n-6][0],dz:p[n-1][1]-p[n-6][1]}); }
     else { for(let k=0;k<n;k++) if(p[k][2]<=-1.48){ q=k; break; } out.push({nm:'mouth'+i,x:S[0]+p[q][0],z:S[2]+p[q][1],dx:p[q][0]-p[Math.max(0,q-6)][0],dz:p[q][1]-p[Math.max(0,q-6)][1]}); } }); return out; });
 const want=process.argv.slice(3); console.log(JSON.stringify(spots.map(s=>s.nm)));
 for(const sp of spots){ if(want.length&&!want.includes(sp.nm)) continue;
  await pg.evaluate(sp=>{ const l=Math.hypot(sp.dx,sp.dz)||1, ux=sp.dx/l, uz=sp.dz/l; // stand back upstream on the bank, looking down the water to the join
    const cx=sp.x-ux*16-uz*6, cz=sp.z-uz*16+ux*6, cy=Math.max(T.terrainH(cx,cz),T.waterAt(cx,cz))+2.4; T.P.pos.set(cx,T.terrainH(cx,cz),cz); T.P.vel.set(0,0,0);
    window.__cam={p:[cx,cy,cz],t:[sp.x+ux*6,Math.max(T.waterAt(sp.x,sp.z),T.terrainH(sp.x,sp.z)),sp.z+uz*6]};
    if(!window.__hk){ window.__hk=1; const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera&&window.__cam){ c.position.set(...window.__cam.p); c.lookAt(...window.__cam.t); c.updateMatrixWorld(); } R(s,c); }; const G=T.camera.getWorldDirection.bind(T.camera); T.camera.getWorldDirection=v=>{ if(window.__cam){ T.camera.position.set(...window.__cam.p); T.camera.lookAt(...window.__cam.t); T.camera.updateMatrixWorld(); } return G(v); }; } },sp);
  await sleep(3500); await pg.screenshot({path:pre+'_'+sp.nm+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

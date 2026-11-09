const {sleep,page,launch,open}=require('./h.js'); const tag=process.argv[2]||'a';
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','chests,LVL,P,renderer,camera,TOWNS,terrainH,settings,houseStair'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); T.settings.skyDrop=false; });
 await pg.evaluate(()=>document.getElementById('play').click()); await pg.waitForFunction(()=>T.renderer.info.render.frame>3,null,{timeout:120000});
 await pg.evaluate(()=>{ window.cam=new THREE.PerspectiveCamera(70,900/520,0.05,2000); const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>R(s,c===T.camera?cam:c);
   const t=T.TOWNS[6]; window.H=t.houses.find(h=>h.floors>1&&h.w*h.d>=6)||t.houses.find(h=>h.floors>1); window.S=T.houseStair(H); });
 const shot=async(name,fn)=>{ for(let i=0;i<6;i++) await pg.evaluate(fn); await sleep(300); await pg.screenshot({path:`hs_${tag}_${name}.png`}); };
 const info=await pg.evaluate(()=>JSON.stringify({i0:H.i0,j0:H.j0,w:H.w,d:H.d,L:H.L,side:H.side,cells:S.cells,top:S.top}));
 console.log(info);
 // camera inside, several views
 const v=(fx,fz,y,lx,lz,ly)=>`(()=>{ const C=5, x0=H.i0*C, z0=H.j0*C, y0=H.L*4; T.P.pos.set(x0-20,y0,z0-20); cam.position.set(x0+${fx}*H.w*C,y0+${y},z0+${fz}*H.d*C); cam.lookAt(x0+${lx}*H.w*C,y0+${ly},z0+${lz}*H.d*C); return new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))); })()`;
 
 
 
 
 await shot('out',v(-0.6,-0.6,9,0.5,0.5,6));
 
 console.log(await pg.evaluate(()=>{ let att=0, houses=0; T.TOWNS.forEach(t=>t.houses.forEach(h=>{ houses++; const top=(h.L+h.floors)*T.LVL; if(T.chests.some(c=>Math.abs(c.y-top)<0.6&&c.x>=h.i0*5&&c.x<=(h.i0+h.w)*5&&c.z>=h.j0*5&&c.z<=(h.j0+h.d)*5)) att++; })); return 'attic chests '+att+' of '+houses+' houses'; }));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

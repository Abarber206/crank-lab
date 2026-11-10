const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,pieces,TOWNS,destroyPiece,terrainH,camera,chunks'),{vp:{width:1000,height:580}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(800);
 const n=await pg.evaluate(async()=>{ const t=T.TOWNS[2], h=t.houses[0], C=5; const w=[...T.pieces.values()].find(p=>p.type==='wall'&&p.skin&&!p.inner&&p.town===t&&p.l===h.L&&p.mask===511); const X=w.axis==='x', cx=X?w.i*C:(w.i+.5)*C, cz=X?(w.j+.5)*C:w.j*C;
   const out=w.out||1, ox=X?out*6:0, oz=X?0:out*6; T.P.pos.set(cx+ox,T.terrainH(cx+ox,cz+oz)+0.2,cz+oz); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(-(cx-T.P.pos.x),-(cz-T.P.pos.z)); T.P.pitch=0.05; window.W=w; window.HP=new THREE.Vector3(cx+ox*0.05,w.l*4+1.5,cz+oz*0.05); await new Promise(r=>setTimeout(r,2500));
   // slow the debris down so the (slow) test renderer catches it mid-flight
   T.destroyPiece(W,HP); T.chunks.forEach(c=>{ c.life+=30; }); const n=T.chunks.length; const st=T.chunks.map(c=>c); let k=0; const iv=setInterval(()=>{ if(++k>3){ clearInterval(iv); st.forEach(c=>{ c.v.set(0,0,0); c.w.set(0,0,0); c.v.y=0; }); const hold=setInterval(()=>st.forEach(c=>{ c.v.set(0,18*0.016,0); }),8); } },16); return n; });
 await sleep(6000); await pg.screenshot({path:'brk_house.png'}); console.log(n, errs.join('\n')||'no errors'); await b.close(); })();

const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,pieces,TOWNS'),{vp:{width:1000,height:600}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1000);
 for(const [nm,pick] of [['a',0],['b',7],['c',20]]){
  await pg.evaluate(k=>{ const ws=[...T.pieces.values()].filter(p=>p.inner&&p.mask!==511); const w=ws[k%ws.length]; const C=5, X=w.axis==='x', cx=X?w.i*C:(w.i+.5)*C, cz=X?(w.j+.5)*C:w.j*C;
    T.P.pos.set(cx+(X?3.4:1.2),w.l*4+0.2,cz+(X?1.2:3.4)); T.P.vel.set(0,0,0); T.P.yaw=Math.atan2(-(cx-T.P.pos.x),-(cz-T.P.pos.z)); T.P.pitch=0.05; },pick);
  await sleep(4000); await pg.screenshot({path:'in_'+nm+'.png'}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

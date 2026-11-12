// the map photo: taken in the lobby, then the minimap in play.  writes map_photo.jpg, map_mini.png
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,settings,renderBigMapImage,P,TOWNS,terrainH'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.renderer.info.render.frame>5,null,{timeout:180000}); await sleep(4000);
 const r=await pg.evaluate(()=>{ const t0=performance.now(), c=T.renderBigMapImage(); window.bigMapImg=c; return {ms:Math.round(performance.now()-t0),w:c.width,url:c.toDataURL('image/jpeg',0.9)}; });
 console.log('photo',r.w,'px in',r.ms,'ms'); require('fs').writeFileSync('/home/claude/work/map_photo.jpg',Buffer.from(r.url.split(',')[1],'base64'));
 await sleep(1500); await pg.screenshot({path:'/home/claude/work/map_lobby_after.png'});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(8000); await pg.evaluate(()=>{ const t=T.TOWNS[0]; T.P.pos.set(t.x+3,T.terrainH(t.x+3,t.z+3)+0.1,t.z+3); }); await sleep(4000);
 const m=await pg.evaluate(()=>document.getElementById('mini').toDataURL('image/png')); require('fs').writeFileSync('/home/claude/work/map_mini.png',Buffer.from(m.split(',')[1],'base64'));
 await pg.keyboard.press('KeyM'); await sleep(2500); await pg.screenshot({path:'/home/claude/work/map_big.png'});
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

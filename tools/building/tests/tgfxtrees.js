// the lobby's trees after switching graphics preset performance -> quality (and back): no flat discs or sideways trees
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,settings,scene,camera'),{vp:{width:1280,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.renderer.info.render.frame>5,null,{timeout:180000}); await sleep(5000);
 for(const v of ['performance','quality','balanced','quality']){ await pg.evaluate(v=>{ const s=document.getElementById('gfxSel'); s.value=v; s.dispatchEvent(new Event('change')); },v); await sleep(5000);
   const u=await pg.evaluate(()=>{ T.renderer.render(T.scene,T.camera); return T.renderer.domElement.toDataURL('image/jpeg',0.85); }); require('fs').writeFileSync('/home/claude/work/gfx_'+v+'.jpg',Buffer.from(u.split(',')[1],'base64')); }
 console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

// node tview.js out.png "<js run in page that places T.P; has T>" 
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,WORLD,SPAWN,camera,STATICS,props,SIGNS,TOD'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(600);
 const shots=process.argv.slice(2); for(let i=0;i<shots.length;i+=2){ const r=await pg.evaluate(shots[i+1]); if(r) console.log(JSON.stringify(r)); await sleep(1200); await pg.screenshot({path:shots[i],timeout:150000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

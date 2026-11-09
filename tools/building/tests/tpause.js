// after playing, the pause menu is the compact panel (no lobby backdrop); before playing it's the lobby
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000}); await sleep(500);
 const a=await pg.evaluate(()=>document.getElementById('menu').classList.contains('lobby'));
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 await pg.keyboard.press('Escape'); await pg.evaluate(()=>{ document.exitPointerLock&&document.exitPointerLock(); }); await sleep(300);
 await pg.evaluate(()=>{ const m=document.getElementById('menu'); if(m.hidden){ m.hidden=false; } }); await pg.evaluate(()=>new Promise(r=>setTimeout(r,50)));
 const c=await pg.evaluate(()=>{ document.querySelector('[data-tab=locker]').click(); return document.getElementById('menu').classList.contains('lobby'); });
 console.log(JSON.stringify({lobbyBefore:a,lobbyPaused:c}), a&&!c?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

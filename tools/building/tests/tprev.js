const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,wallet,EMOTE_LIST'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(3500);
 await pg.click('[data-tab=shop]'); await sleep(800); await pg.evaluate(()=>document.querySelector('#shopGrid .ofit').click()); await sleep(2500); await pg.screenshot({path:'pv_shop.png'});
 await pg.evaluate(()=>{ const c=[...document.querySelectorAll('#shopGrid .ofit')].find(b=>b.querySelector('svg.emo')); c&&c.click(); }); await sleep(1800); await pg.screenshot({path:'pv_shop_dance.png'});
 await pg.click('[data-tab=locker]'); await sleep(800); await pg.evaluate(()=>document.querySelector('#emotesBox [data-id=dance]').click()); await sleep(1500); await pg.screenshot({path:'pv_locker.png'});
 const ok=await pg.evaluate(()=>({inLocker:document.getElementById('stage').parentNode.dataset.tab,canvas:document.getElementById('stageC').width})); console.log(JSON.stringify(ok));
 await pg.click('[data-tab=play]'); await sleep(600); console.log(await pg.evaluate(()=>document.getElementById('stage').parentNode.dataset.tab), errs.join('\n')||'no errors'); await b.close(); })();

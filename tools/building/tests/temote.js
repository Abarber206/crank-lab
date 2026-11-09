// dances: the shop sells them, a bought dance shows in the Locker and becomes your emote, the lobby hero dances it, and it plays in game
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,wallet,EMOTE_LIST,shopRotation,startEmote,localHero'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(3000);
 const r=await pg.evaluate(async()=>{ const out={}; const vis=()=>[...document.querySelectorAll('#emotesBox .ofit')].filter(b=>!b.hidden).map(b=>b.dataset.id);
   out.start=vis(); out.shopDances=T.shopRotation().filter(x=>x[0]==='e').map(x=>x[1].id);
   T.wallet.pts=3000; window._locker.offerBuy('e',T.EMOTE_LIST.find(e=>e.id==='floss')); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200));
   out.after=vis(); out.equipped=T.settings.emote; return out; });
 await pg.click('[data-tab=locker]'); await sleep(400); await pg.evaluate(()=>document.getElementById('emotesBox').scrollIntoView()); await sleep(300); await pg.screenshot({path:'em_locker.png'});
 await pg.click('[data-tab=shop]'); await sleep(600); await pg.screenshot({path:'em_shop.png'});
 await pg.click('[data-tab=play]'); await pg.evaluate(()=>{ window._stagePrev={id:'disco',t0:performance.now()}; }); await sleep(1800); await pg.screenshot({path:'em_stage.png'});
 // in game
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 const g=await pg.evaluate(()=>{ T.startEmote('floss'); return !!T.P.emote; });
 console.log(JSON.stringify(r),g);
 console.log(r.start.join()==='wave,dance,cheer,salute'&&r.shopDances.length===2&&r.after.includes('floss')&&r.equipped==='floss'&&g?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

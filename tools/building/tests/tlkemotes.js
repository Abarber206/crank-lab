// the Locker emote section with every emote owned.  node tlkemotes.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,wallet,saveWallet,EMOTE_LIST'),{vp:{width:1300,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(1500);
 await pg.evaluate(()=>{ T.EMOTE_LIST.forEach(e=>{ if(e.shop) T.wallet.owned.push('e:'+e.id); }); T.saveWallet(); window.renderShop(); document.querySelector('button[data-tab=locker]').click(); });
 await sleep(800); await pg.evaluate(()=>document.getElementById('wheelSlots').scrollIntoView()); await sleep(1200);
 await pg.screenshot({path:'/home/claude/work/lk_emotes.png',timeout:200000}); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

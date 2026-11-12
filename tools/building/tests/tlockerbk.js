// screenshots of the Locker's Back bling row (with cape on) and the Item Shop.  node tlockerbk.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,wallet,saveWallet,get _locker(){return _locker}'),{vp:{width:1400,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T._locker,null,{timeout:180000}); await sleep(2000);
 await pg.evaluate(()=>{ T.wallet.owned.push('o:ember','o:nightfall'); T.saveWallet(); window.renderShop(); document.querySelector('button[data-tab=locker]').click(); });
 await sleep(1500); await pg.evaluate(()=>{ T._locker.pickBk('wings'); document.getElementById('backs').scrollIntoView(); }); await sleep(6000);
 await pg.screenshot({path:'/home/claude/work/lk_backs.png',timeout:200000});
 await pg.evaluate(()=>document.querySelector('button[data-tab=shop]').click()); await sleep(4000);
 await pg.screenshot({path:'/home/claude/work/lk_shop.png',timeout:200000});
 console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

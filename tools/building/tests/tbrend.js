// getting in and out: pressing Play in Battle royale shows the loading screen for 10 seconds before the match; when you're
// eliminated you're back in the lobby a few seconds later (not dropped into another match).  node tbrend.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,brPlayerOut'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await sleep(1500);
 const a=await pg.evaluate(()=>({load:!document.getElementById('loadScr').hidden,on:T.BR.on,num:document.getElementById('lsNum').textContent}));
 const t0=Date.now(); await pg.waitForFunction(()=>T.BR.on,null,{timeout:60000}); const took=(Date.now()-t0)/1000+1.5;
 const b1=await pg.evaluate(()=>({load:!document.getElementById('loadScr').hidden}));
 await pg.evaluate(()=>T.brPlayerOut('a test')); await sleep(9500);
 const c=await pg.evaluate(()=>({menu:!document.getElementById('menu').hidden,on:T.BR.on,play:document.getElementById('play').textContent}));
 await sleep(2000); const d=await pg.evaluate(()=>({on:T.BR.on,load:!document.getElementById('loadScr').hidden}));
 console.log(JSON.stringify({a,took:+took.toFixed(1),b1,c,d}));
 const ok=a.load&&!a.on&&took>9&&took<16&&c.menu&&!c.on&&!d.on&&!d.load; console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

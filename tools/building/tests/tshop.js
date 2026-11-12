// fresh player: locker shows only Rook + Steel Pick; the shop shows 2 outfits + 1 pickaxe with a timer; buying moves an item into the locker
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,shopRotation,shopRotationIds,wallet,settings'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(3500);
 await pg.evaluate(()=>document.querySelector('button[data-tab=locker]').click()); await sleep(500); await pg.screenshot({path:'sh_locker.png'});
 const r=await pg.evaluate(()=>{ const vis=sel=>[...document.querySelectorAll(sel+' .ofit')].filter(b=>!b.hidden).map(b=>b.dataset.id);
   const rot=T.shopRotation().map(([k,it])=>k+':'+it.id); let repeats=0; const S0=Math.floor(Date.now()/(20*60*1000)); for(let s=S0-100;s<S0+100;s++){ const a=T.shopRotation(s).map(x=>x[0]+x[1].id), p=T.shopRotation(s-1).map(x=>x[0]+x[1].id); if(a.some(id=>p.includes(id))) repeats++; if(a.length!==7) repeats+=100; }
   return {outfits:vis('#outfits'),picks:vis('#picks'),rot,repeats,timer:document.getElementById('shopTimer').textContent}; });
 await pg.evaluate(()=>document.querySelector('button[data-tab=shop]').click()); await sleep(600); await pg.screenshot({path:'sh_shop.png'});
 const n=await pg.evaluate(()=>document.querySelectorAll('#shopGrid .ofit').length);
 // buy the first shop item with points
 const bought=await pg.evaluate(async()=>{ T.wallet.cb=5000; window._locker.offerBuy('o',T.shopRotation()[0][1]); await new Promise(r=>setTimeout(r,100)); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200));
   const id=T.shopRotation()[0][1].id; const lk=document.querySelector(`#outfits [data-id="${id}"], #picks [data-id="${id}"]`); return {id,inLocker:lk&&!lk.hidden,owned:document.querySelector('#shopGrid .own')!=null}; });
 console.log(JSON.stringify(r),n,JSON.stringify(bought));
 console.log(r.outfits.join()==='rook'&&r.picks.join()==='steel'&&n===7&&r.repeats===0&&bought.inLocker&&bought.owned?'PASS':'FAIL');
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

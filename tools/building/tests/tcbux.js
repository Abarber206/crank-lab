// Crank Bux: the wallet shows Crank Bux (no points anywhere in the menu); "Get Crank Bux" shows your points and what
// each pack costs, converts after a confirm; shop prices are in Crank Bux; too few Crank Bux offers to get more.
// node tcbux.js [shots-prefix]   (VP=844x390 for a phone)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const vp=(process.env.VP||'1280x760').split('x').map(Number), shots=process.argv[2];
 const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,shopRotation,wallet,settings'),{vp:{width:vp[0],height:vp[1]}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(2500);
 const r={};
 await pg.evaluate(()=>{ T.wallet.pts=5000; T.wallet.cb=0; T.wallet.owned=[]; window.renderWallet&&renderWallet(); });
 console.log(errs.join('\n')); r.head=await pg.evaluate(()=>document.querySelector('.mhead').innerText.replace(/\s+/g,' '));
 await pg.evaluate(()=>document.querySelector('button[data-tab=shop]').click()); await sleep(600);
 r.costs=await pg.evaluate(()=>[...document.querySelectorAll('#shopGrid .cost')].map(e=>e.textContent.trim()));
 r.shopText=await pg.evaluate(()=>document.querySelector('[data-tab=shop].mtab').innerText.includes('pts'));
 await pg.evaluate(()=>document.getElementById('cbGet').click()); await sleep(300);
 r.box=await pg.evaluate(()=>({open:!document.getElementById('cbBox').hidden,pts:document.getElementById('cbPts').textContent,packs:[...document.querySelectorAll('.cbpack')].map(b=>(b.disabled?'x':'')+b.querySelector('b').textContent+'/'+b.querySelector('em').textContent)}));
 if(shots) await pg.screenshot({path:shots+'_box.png'});
 await pg.evaluate(()=>document.querySelectorAll('.cbpack')[2].click()); await sleep(200);
 r.conf=await pg.evaluate(()=>document.getElementById('cbConf').innerText);
 await pg.evaluate(()=>document.getElementById('cbYes').click()); await sleep(300);
 r.after=await pg.evaluate(()=>({pts:T.wallet.pts,cb:T.wallet.cb,head:document.getElementById('cbV').textContent,boxPts:document.getElementById('cbPts').textContent,saved:JSON.parse(localStorage.getItem('cranklab.wallet')).cb}));
 await pg.evaluate(()=>document.getElementById('cbClose').click()); await sleep(200);
 // a 2,500 legendary outfit with 1,200: offers Crank Bux; then a cheap one: buys
 r.short=await pg.evaluate(async()=>{ const it=T.shopRotation().slice().sort((x,y)=>window._locker.price(y[0],y[1])-window._locker.price(x[0],x[1]))[0]; window._locker.offerBuy(it[0],it[1]); await new Promise(r=>setTimeout(r,50));
   const t=document.getElementById('buyOk').textContent, c=window._locker.price(it[0],it[1]); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,100)); const op=!document.getElementById('cbBox').hidden; document.getElementById('cbClose').click(); return {t,c,opensBox:op,cb:T.wallet.cb}; });
 if(shots){ await sleep(300); await pg.screenshot({path:shots+'_buy.png'}); }
 r.cheap=await pg.evaluate(async()=>{ const all=T.shopRotation(), it=all.find(([k,it])=>k!=='o'&&window._locker.price(k,it)<=T.wallet.cb&&!window._locker.owned(k,it)); if(!it) return null; const c=window._locker.price(it[0],it[1]), cb0=T.wallet.cb;
   window._locker.offerBuy(it[0],it[1]); await new Promise(r=>setTimeout(r,50)); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200)); return {c,spent:cb0-T.wallet.cb,owned:window._locker.owned(it[0],it[1]),pts:T.wallet.pts}; });
 if(shots){ await pg.evaluate(()=>document.querySelector('button[data-tab=shop]').click()); await sleep(500); await pg.screenshot({path:shots+'_shop.png'}); }
 console.log(JSON.stringify(r,null,1));
 const ok=/Crank Bux/i.test(r.head)&&!/pts|points/i.test(r.head)&&!r.shopText&&r.costs.length===7&&r.box.open&&r.box.pts==='5,000'&&r.box.packs.join()==='200/800 points,600/2,200 points,1,200/4,000 points,x2,500/7,800 points'
   &&/4,000 points/.test(r.conf)&&r.after.pts===1000&&r.after.cb===1200&&r.after.head==='1,200'&&r.after.saved===1200&&r.short.t==='Get Crank Bux'&&r.short.opensBox&&r.short.cb===1200&&(!r.cheap||(r.cheap.spent===r.cheap.c&&r.cheap.owned&&r.cheap.pts===1000));
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

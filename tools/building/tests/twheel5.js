// the 5-slot emote wheel: defaults, pick a slot then an emote, swap, remove, buy fills an empty slot, the in-game wheel shows them.  node twheel5.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,settings,wallet,EMOTE_LIST,EW,emoBuild,get _locker(){return _locker}'),{vp:{width:1300,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T._locker,null,{timeout:180000}); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const L=T._locker, W=()=>T.settings.wheel.slice(), out={}, slot=k=>document.querySelectorAll('#wheelSlots .wslot')[k], card=id=>document.querySelector(`#emotesBox [data-id="${id}"]`);
   out.def=W(); out.quick=T.settings.emote;
   slot(1).click(); card('dance').click(); out.swap=W();                   // dance was in slot 1, wave in 2: picking slot 2 then dance swaps them
   slot(0).querySelector('.wx').click(); out.removed=W(); out.quick2=T.settings.emote;
   T.wallet.cb=5000; L.offerBuy('e',T.EMOTE_LIST.find(e=>e.id==='floss')); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200)); out.bought=W();
   L.offerBuy('e',T.EMOTE_LIST.find(e=>e.id==='robot')); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200)); out.bought2=W();
   L.offerBuy('e',T.EMOTE_LIST.find(e=>e.id==='hype')); document.getElementById('buyOk').click(); await new Promise(r=>setTimeout(r,200)); out.full=W(); // wheel full: it isn't forced in
   slot(3).click(); card('hype').click(); out.replaced=W();
   T.emoBuild(); out.ring=T.EW.ids.slice(); out.badges=[...document.querySelectorAll('#emotesBox .ofit i.wn')].map(i=>i.parentNode.dataset.id+i.textContent);
   return out; });
 await pg.evaluate(()=>{ document.querySelector('button[data-tab=locker]').click(); }); await sleep(800); await pg.evaluate(()=>document.getElementById('wheelSlots').scrollIntoView()); await sleep(1500);
 await pg.screenshot({path:'/home/claude/work/wheel5.png',timeout:200000});
 console.log(JSON.stringify(r));
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const ok=eq(r.def,['dance','wave','cheer','salute',null])&&r.quick==='dance'&&eq(r.swap,['wave','dance','cheer','salute',null])&&eq(r.removed,[null,'dance','cheer','salute',null])&&r.quick2==='dance'
   &&eq(r.bought,['floss','dance','cheer','salute',null])&&eq(r.bought2,['floss','dance','cheer','salute','robot'])&&eq(r.full,r.bought2)&&eq(r.replaced,['floss','dance','cheer','hype','robot'])&&eq(r.ring,r.replaced)&&r.badges.length===5;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

// back bling is its own slot: take it off, put any owned one on any outfit, it goes out over the network.  node tback.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,settings,saveSettings,OUTFITS,BACKS,heroFor,reskin,localHero,wallet,saveWallet,get _locker(){return _locker},get state(){return typeof stateMsg==="function"?stateMsg():null}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T._locker,null,{timeout:180000}); await sleep(1500);
 const r=await pg.evaluate(()=>{ const cnt=h=>{ let n=0; h.rig.pack.traverse(o=>{ if(o.isMesh) n+=o.geometry.attributes.position.count; }); return n; };
   const out={};
   const a=T.heroFor(T.OUTFITS[0],'steel','auto'), none=T.heroFor(T.OUTFITS[0],'steel','none'), cape=T.heroFor(T.OUTFITS[0],'steel','cape'), wings=T.heroFor(T.OUTFITS[0],'steel','wings');
   out.auto=cnt(a); out.none=cnt(none); out.cape=cnt(cape); out.wings=cnt(wings);
   // the rook owns the pack (its own) and nothing else; the cape comes with Ember (owned from the start)
   const L=T._locker; out.ownCape0=L.owned('b',T.BACKS.find(x=>x.id==='cape')); T.wallet.owned.push('o:ember'); T.saveWallet(); out.ownPack=L.owned('b',T.BACKS.find(x=>x.id==='pack')); out.ownCape=L.owned('b',T.BACKS.find(x=>x.id==='cape')); out.ownBanner=L.owned('b',T.BACKS.find(x=>x.id==='banner')); out.ownNone=L.owned('b',T.BACKS[0]);
   // wear the cape on Rook
   L.pickBk('cape'); out.setting=T.settings.back; out.heroBack=T.localHero.back; out.heroCnt=cnt(T.localHero);
   out.card=!!document.querySelector('#backs [data-id="cape"].on'); out.hiddenBanner=document.querySelector('#backs [data-id="banner"]').hidden;
   L.pickBk('none'); out.noneCnt=cnt(T.localHero); L.pickBk('auto'); out.autoCnt=cnt(T.localHero);
   // a locked one opens the buy box instead
   L.pickBk('banner'); out.buyShown=!document.getElementById('buyBox').hidden; out.stillAuto=T.settings.back;
   return out; });
 console.log(JSON.stringify(r));
 const ok=r.none===0&&r.cape>0&&r.wings>0&&r.auto>0&&r.ownPack&&!r.ownCape0&&r.ownCape&&r.cape!==r.auto&&!r.ownBanner&&r.ownNone&&r.setting==='cape'&&r.heroBack==='cape'&&r.heroCnt===r.cape&&r.card&&r.hiddenBanner&&r.noneCnt===0&&r.autoCnt===r.auto&&r.buyShown&&r.stillAuto==='auto';
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

# ---------- 59. start with one outfit and one pickaxe; the Locker holds only what you own; the Item Shop rotates
# every 20 minutes (same items for everyone, picked from the clock) with two outfits and a pickaxe ----------
import re
m=re.search(r'      <div class="shopbar"><p>Outfits and pickaxes with a price unlock with points\..*?</p></div>\n',s,re.S); assert m
s=s.replace(m.group(0),'      <div class="shopbar" hidden></div>\n      <p class="lkempty" id="lkHint">Get more outfits and pickaxes in the <b>Item Shop</b>.</p>\n')
rep("  const owned=(k,it)=>!it.shop||wallet.owned.includes(k+':'+it.id), price=(k,it)=>PRICE[k][it.rarity]||500;",
    "  const FREE={o:'rook',p:'steel'}, owned=(k,it)=>(k==='e'?!it.shop:it.id===FREE[k])||wallet.owned.includes(k+':'+it.id), price=(k,it)=>PRICE[k][it.rarity]||500;")
# locker cards: only what you own shows; nothing in the locker carries a price any more
rep("""      const own=owned(k,it); b.classList.toggle('locked',!own); b.classList.toggle('afford',!own&&wallet.pts>=price(k,it));
      let pr=b.querySelector('.price'); if(own){ if(pr) pr.remove(); } else { if(!pr){ pr=document.createElement('i'); pr.className='price'; b.appendChild(pr); } pr.textContent=price(k,it).toLocaleString(); } }));""",
"""      const own=owned(k,it); b.hidden=!own; b.classList.remove('locked','afford'); const pr=b.querySelector('.price'); if(pr) pr.remove(); }));""")
rep('<div class="shophead"><h2>Item Shop</h2><p>Earn points in <b>Zombie horde</b> and spend them here. Bought items go straight to your Locker.</p></div>',
    '<div class="shophead"><h2>Item Shop</h2><p>Spend the points you earn in <b>Zombie horde</b>. Bought items go straight to your Locker.</p><p class="shoptimer">New items in <b id="shopTimer">20:00</b></p></div>')
rep(".shophead{border-radius:10px;padding:14px 16px}",".shophead{border-radius:10px;padding:14px 16px;position:relative} .shoptimer{position:absolute;top:14px;right:16px;font:800 italic 15px/1 var(--font-hud)!important;letter-spacing:.06em;text-transform:uppercase;color:#ffe08a!important} .shoptimer b{font-size:19px;color:#fff} .lkempty{margin:0 0 10px;color:var(--muted);font-size:14px}")
rep("@media (max-width:820px){\n","@media (max-width:820px){\n  .shoptimer{position:static!important;margin-top:8px!important}\n")
rep("  const items=[...OUTFITS.filter(o=>o.shop).map(it=>['o',it]),...PICKAXES.filter(p=>p.shop).map(it=>['p',it])];",
    "  const items=shopRotation();")
rep("function renderItemShop(){",r"""const SHOP_MS=20*60*1000;
// what's on sale in a rotation: a pure function of the 20-minute slot, so every player sees the same shop
function shopRotationIds(slot){ const r=seeded(slot*7919+101), pick=(list,n,k)=>{ const pool=list.slice(), out=[]; while(out.length<n&&pool.length) out.push(k+':'+pool.splice(Math.floor(r()*pool.length),1)[0].id); return out; };
  return {o:pick(OUTFITS.filter(o=>o.id!=='rook'),7,'o'),p:pick(PICKAXES.filter(p=>p.id!=='steel'),5,'p'),e:pick(EMOTE_LIST.filter(e=>e.shop),5,'e')}; } // a short ranked list per kind
const SHOP_EPOCH=Math.floor(Date.UTC(2026,0,1)/SHOP_MS), shopMemo=new Map(), SHOP_N={o:3,p:2,e:2}; // 3 outfits, 2 pickaxes, 2 dances
function shopRotationAt(slot){ // walk forward from a fixed start so everyone agrees exactly, and nothing repeats two rotations running
  if(slot<=SHOP_EPOCH){ const ids=shopRotationIds(slot); return [...ids.o.slice(0,3),...ids.p.slice(0,2),...ids.e.slice(0,2)]; }
  if(shopMemo.has(slot)) return shopMemo.get(slot);
  let k=slot-1; while(k>SHOP_EPOCH&&!shopMemo.has(k)) k--; let prev=k<=SHOP_EPOCH?shopRotationAt(k):shopMemo.get(k);
  for(let q=k+1;q<=slot;q++){ const ids=shopRotationIds(q), next=[]; for(const kk of ['o','p','e']) next.push(...ids[kk].filter(id=>!prev.includes(id)).slice(0,SHOP_N[kk])); prev=next; shopMemo.set(q,prev); }
  return prev; }
function shopRotation(slot=Math.floor(Date.now()/SHOP_MS)){ return shopRotationAt(slot).map(x=>{ const [k,id]=x.split(':'); return [k,k==='o'?OUTFITS.find(o=>o.id===id):k==='p'?PICKAXES.find(p=>p.id===id):EMOTE_LIST.find(e=>e.id===id)]; }).filter(x=>x[1]); }
let shopSlot=-1;
setInterval(()=>{ const left=SHOP_MS-(Date.now()%SHOP_MS), el=$('shopTimer'); if(el){ const m=Math.floor(left/60000), sec=Math.floor(left/1000)%60; el.textContent=m+':'+String(sec).padStart(2,'0'); }
  const sl=Math.floor(Date.now()/SHOP_MS); if(sl!==shopSlot){ const fresh=shopSlot>=0; shopSlot=sl; renderItemShop(); if(fresh&&!menu.hidden) toast('The Item Shop has new items'); } },1000);
function renderItemShop(){""")
rep("wallet.pts-=c; wallet.owned.push(k+':'+it.id); saveWallet(); renderWallet();","wallet.pts-=c; wallet.owned.push(k+':'+it.id); saveWallet(); renderWallet(); renderShop();")

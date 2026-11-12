# patch150: Crank Bux. The Item Shop sells for Crank Bux instead of points. Points (still earned in Zombie horde) are
# turned into Crank Bux in packs, at a steep rate (3-4 points a Crank Buck; the bigger packs are a little cheaper),
# and points only show in that "Get Crank Bux" window, which tells you what each pack costs and what you have.
# Prices: outfits 800 / 1,200 / 1,500 / 2,000 / 2,500 (common to legendary); pickaxes and dances 200 / 200 / 400 / 400 / 800.
# The wallet at the top right shows Crank Bux; tapping it opens the "Get Crank Bux" window.
CBX='<svg class="cbx" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10.4" fill="#27b4ee" stroke="#0a5a88" stroke-width="1.5"/><circle cx="12" cy="12" r="7.6" fill="none" stroke="#c8f3ff" stroke-width="1" opacity=".75"/><path d="M15.3 8.7a4.7 4.7 0 1 0 0 6.6" fill="none" stroke="#fff" stroke-width="2.7" stroke-linecap="round"/><path d="M15.4 15.3l2.2 2.2" stroke="#fff" stroke-width="1.9" stroke-linecap="round"/><circle cx="18.1" cy="18" r="1.45" fill="#ffd84a" stroke="#0a5a88" stroke-width=".6"/></svg>'
rep("""      <div class="wallet" title="Points: earned by taking down zombies. Spend them in the Locker."><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#ffcf4a"/><circle cx="12" cy="12" r="7" fill="none" stroke="#b07a16" stroke-width="2"/><path d="M12 7v10M9 9.5h4.5a1.8 1.8 0 0 1 0 3.6h-3a1.8 1.8 0 0 0 0 3.6H15" fill="none" stroke="#7a520c" stroke-width="1.8" stroke-linecap="round"/></svg><b id="ptsV">0</b><span>pts</span></div>""",
"""      <button class="wallet" id="cbWallet" type="button" title="Crank Bux: spend them in the Item Shop. Tap to get more.">"""+CBX+"""<b id="cbV">0</b><span>Crank Bux</span><i class="cbplus" aria-hidden="true">+</i></button>""")
rep("""<div id="invitePop" hidden>""","""<div id="cbBox" hidden role="dialog" aria-modal="true" aria-labelledby="cbTitle"><div class="cbcard">
  <h3 id="cbTitle">"""+CBX+"""Get Crank Bux</h3>
  <p class="cbhave">You have <b id="cbPts">0</b> points</p>
  <div class="cbpacks" id="cbPacks"></div>
  <div class="cbconf" id="cbConf" hidden><p></p><button class="btn primary" id="cbYes" type="button">Convert</button><button class="btn" id="cbBack" type="button">Back</button></div>
  <p class="cbnote">Earn points by taking down zombies in <b>Zombie horde</b>. Converting can't be undone.</p>
  <button class="btn cbclose" id="cbClose" type="button">Close</button>
</div></div>
<div id="invitePop" hidden>""")
rep("""<p>Spend the points you earn in <b>Zombie horde</b>. Bought items go straight to your Locker.</p>""",
"""<p>Spend Crank Bux here. Turn the points you earn in <b>Zombie horde</b> into Crank Bux. Bought items go straight to your Locker.</p><button class="btn primary cbget" id="cbGet" type="button">"""+CBX+"""Get Crank Bux</button>""")
# styles
rep("""#invitePop{position:fixed;""","""button.wallet{cursor:pointer;-webkit-appearance:none;appearance:none;font:800 italic 18px/1 var(--font-hud);color:#bff0ff;border-color:rgba(80,200,255,.45)} button.wallet:hover{filter:brightness(1.12)} button.wallet:active{transform:scale(.97)}
#menu.lobby .wallet{border-color:rgba(90,205,255,.6)}
.cbx{width:1.25em;height:1.25em;flex:none;vertical-align:-.25em} .wallet .cbx{width:24px;height:24px}
.cbplus{font:900 15px/1 system-ui,sans-serif;font-style:normal;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;background:#27b4ee;color:#fff;margin-left:2px}
.shopgrid .cost .cbx{width:16px;height:16px} .shopgrid .cost{color:#bff0ff}
.cbget{margin-top:10px;display:inline-flex;align-items:center;gap:8px}
#buyBox{position:fixed;left:50%;bottom:max(18px,env(safe-area-inset-bottom,0px));transform:translateX(-50%);width:min(560px,calc(100vw - 24px));z-index:58;background:rgba(8,20,56,.96);border:2px solid rgba(90,205,255,.6);border-radius:12px;padding:12px 14px;box-shadow:0 12px 34px rgba(0,0,0,.5);color:#fff}
#buyBox[hidden]{display:none} #buyBox small{color:rgba(225,236,255,.8)}
#cbBox{position:fixed;inset:0;z-index:62;display:grid;place-items:center;background:rgba(2,8,24,.72);padding:16px;backdrop-filter:blur(4px)} #cbBox[hidden]{display:none}
.cbcard{width:min(620px,100%);max-height:calc(100vh - 32px);overflow-y:auto;background:linear-gradient(180deg,#0d2a66,#071638);border:2px solid rgba(90,205,255,.6);border-radius:14px;padding:18px;color:#fff;box-shadow:0 18px 50px rgba(0,0,0,.55);position:relative}
.cbcard h3{margin:0 0 6px;display:flex;align-items:center;gap:10px;font:800 italic 26px/1.1 var(--font-hud);text-transform:uppercase;letter-spacing:.03em} .cbcard h3 .cbx{width:32px;height:32px}
.cbhave{margin:0 0 14px;color:rgba(225,236,255,.85)} .cbhave b{color:#ffe08a;font:800 italic 18px/1 var(--font-hud)}
.cbpacks{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px}
.cbpack{position:relative;display:flex;flex-direction:column;align-items:center;gap:6px;padding:16px 8px 12px;border-radius:10px;border:2px solid rgba(90,205,255,.35);background:radial-gradient(circle at 50% 30%,rgba(60,180,255,.35),rgba(10,30,80,.6) 70%);color:#fff;cursor:pointer;font:inherit}
.cbpack:hover:not(:disabled){border-color:#7fe3ff;filter:brightness(1.1)} .cbpack:disabled{opacity:.5;cursor:default}
.cbpack .cbx{width:40px;height:40px} .cbpack b{font:800 italic 24px/1 var(--font-hud)} .cbpack small{font:700 11px/1 var(--font-hud);letter-spacing:.12em;text-transform:uppercase;color:#bff0ff}
.cbpack em{font-style:normal;margin-top:4px;padding:5px 10px;border-radius:999px;background:#ffd21a;color:#1a1400;font:800 13px/1 var(--font-hud)} .cbpack:disabled em{background:rgba(255,255,255,.18);color:#fff}
.cbpack i{position:absolute;top:-9px;left:50%;transform:translateX(-50%);white-space:nowrap;font:800 10px/1 var(--font-hud);letter-spacing:.1em;text-transform:uppercase;font-style:normal;background:#ff6a3d;color:#fff;border-radius:4px;padding:3px 6px}
.cbconf{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px;padding:12px;border-radius:10px;background:rgba(255,255,255,.08)} .cbconf[hidden]{display:none} .cbconf p{margin:0;flex:1;min-width:180px}
.cbnote{margin:14px 0 0;font-size:13px;color:rgba(225,236,255,.7)} .cbclose{margin-top:12px}
#invitePop{position:fixed;""")
# the wallet
rep("""const wallet={pts:0,owned:[]};""","""const wallet={pts:0,cb:0,owned:[]};
const CB_PACKS=[{cb:200,pts:800},{cb:600,pts:2200},{cb:1200,pts:4000,tag:'Popular'},{cb:2500,pts:7800,tag:'Best value'}];""")
rep("""if(typeof w.pts==='number'&&isFinite(w.pts)) wallet.pts=Math.max(0,Math.floor(w.pts));""","""if(typeof w.pts==='number'&&isFinite(w.pts)) wallet.pts=Math.max(0,Math.floor(w.pts)); if(typeof w.cb==='number'&&isFinite(w.cb)) wallet.cb=Math.max(0,Math.floor(w.cb));""")
rep("""function renderWallet(bump){ const v=$('ptsV'); if(v) v.textContent=wallet.pts.toLocaleString(); const w=v&&v.parentNode; if(bump&&w){ w.classList.remove('bump'); void w.offsetWidth; w.classList.add('bump'); }
  const hv=$('hudPts'); if(hv) hv.textContent=wallet.pts.toLocaleString(); if(typeof renderShop==='function') renderShop(); }""",
"""function renderWallet(bump){ const v=$('cbV'); if(v) v.textContent=wallet.cb.toLocaleString(); const w=v&&v.parentNode; if(bump&&w){ w.classList.remove('bump'); void w.offsetWidth; w.classList.add('bump'); }
  if(!$('cbBox').hidden) renderCbBox(); if(typeof renderShop==='function') renderShop(); }
// "Get Crank Bux": the one place points are shown, and what each pack costs in them
let cbPick=null, cbAfter=null;
function renderCbBox(){ $('cbPts').textContent=wallet.pts.toLocaleString(); const box=$('cbPacks'); box.innerHTML='';
  CB_PACKS.forEach((p,i)=>{ const b=document.createElement('button'); b.type='button'; b.className='cbpack'; const can=wallet.pts>=p.pts; b.disabled=!can;
    b.innerHTML=(p.tag?`<i>${p.tag}</i>`:'')+`"""+CBX+"""<b>${p.cb.toLocaleString()}</b><small>Crank Bux</small><em>${p.pts.toLocaleString()} points</em>`+(can?'':`<small>${(p.pts-wallet.pts).toLocaleString()} more points</small>`);
    b.addEventListener('click',()=>{ audioInit(); cbPick=i; const c=$('cbConf'); c.hidden=false; c.querySelector('p').innerHTML=`Turn <b>${p.pts.toLocaleString()} points</b> into <b>${p.cb.toLocaleString()} Crank Bux</b>? You'll have ${(wallet.pts-p.pts).toLocaleString()} points left.`; $('cbYes').focus(); });
    box.appendChild(b); });
  if(cbPick!==null&&wallet.pts<CB_PACKS[cbPick].pts){ cbPick=null; $('cbConf').hidden=true; } }
function openCbBox(after){ cbAfter=after||null; cbPick=null; $('cbConf').hidden=true; $('cbBox').hidden=false; renderCbBox(); }
function closeCbBox(){ $('cbBox').hidden=true; cbPick=null; const f=cbAfter; cbAfter=null; if(f) f(); }
$('cbWallet').addEventListener('click',()=>{ audioInit(); openCbBox(); });
$('cbGet').addEventListener('click',()=>{ audioInit(); openCbBox(); });
$('cbClose').addEventListener('click',closeCbBox);
$('cbBox').addEventListener('click',e=>{ if(e.target.id==='cbBox') closeCbBox(); });
$('cbBack').addEventListener('click',()=>{ cbPick=null; $('cbConf').hidden=true; });
$('cbYes').addEventListener('click',()=>{ if(cbPick===null) return; const p=CB_PACKS[cbPick]; if(wallet.pts<p.pts) return;
  wallet.pts-=p.pts; wallet.cb+=p.cb; saveWallet(); cbPick=null; $('cbConf').hidden=true; sfx('win'); toast('+'+p.cb.toLocaleString()+' Crank Bux'); renderWallet(true); });
addEventListener('keydown',e=>{ if(e.code==='Escape'&&!$('cbBox').hidden){ e.stopPropagation(); closeCbBox(); } },true);""")
# prices in Crank Bux
rep("""  const PRICE={o:{common:150,uncommon:300,rare:600,epic:1000,legendary:1600},p:{common:100,uncommon:200,rare:400,epic:700,legendary:1100},e:{common:100,uncommon:250,rare:450,epic:700,legendary:1000}};""",
"""  const PRICE={o:{common:800,uncommon:1200,rare:1500,epic:2000,legendary:2500},p:{common:200,uncommon:200,rare:400,epic:400,legendary:800},e:{common:200,uncommon:200,rare:400,epic:400,legendary:800}}; // in Crank Bux""")
rep("""price=(k,it)=>PRICE[k][it.rarity]||500;""","""price=(k,it)=>PRICE[k][it.rarity]||800;""")
rep("""  const offerBuy=(k,it)=>{ offer={k,it}; const c=price(k,it), can=wallet.pts>=c;
    buy.hidden=false; buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'} · <b>${c.toLocaleString()} pts</b>`+(can?'':`<br><small>You need ${(c-wallet.pts).toLocaleString()} more. Take down zombies in Zombie horde to earn points.</small>`);
    $('buyOk').disabled=!can; $('buyOk').textContent=can?'Buy for '+c.toLocaleString():'Not enough points'; };
  $('buyOk').addEventListener('click',()=>{ if(!offer) return; const {k,it}=offer, c=price(k,it); if(owned(k,it)||wallet.pts<c) return;
    wallet.pts-=c;""",
"""  const offerBuy=(k,it)=>{ offer={k,it}; const c=price(k,it), can=wallet.cb>=c;
    buy.hidden=false; buy.querySelector('p').innerHTML=`<b>${it.name}</b> · ${RNAME[it.rarity]} ${k==='o'?'outfit':k==='e'?'dance':'pickaxe'} · <b>"""+CBX+""" ${c.toLocaleString()}</b>`+(can?'':`<br><small>You need ${(c-wallet.cb).toLocaleString()} more Crank Bux.</small>`);
    $('buyOk').disabled=false; $('buyOk').textContent=can?'Buy for '+c.toLocaleString():'Get Crank Bux'; };
  $('buyOk').addEventListener('click',()=>{ if(!offer) return; const {k,it}=offer, c=price(k,it); if(owned(k,it)) return;
    if(wallet.cb<c){ const o=offer; openCbBox(()=>{ if(offer===o&&!owned(o.k,o.it)) offerBuy(o.k,o.it); }); return; }
    wallet.cb-=c;""")
rep("""(!own&&wallet.pts>=c?' afford':'');""","""(!own&&wallet.cb>=c?' afford':'');""")
rep("""(own?'<b class="own">Owned</b>':`<b class="cost">${c.toLocaleString()}</b>`)""","""(own?'<b class="own">Owned</b>':`<b class="cost">"""+CBX+"""${c.toLocaleString()}</b>`)""")
rep(""".shopgrid .cost::before{content:"";width:14px;height:14px;border-radius:50%;background:#ffcf4a;box-shadow:inset 0 0 0 2px #b07a16}""","")

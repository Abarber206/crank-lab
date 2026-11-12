# patch167: the emote wheel holds 5 emotes you choose. In the Locker, five slots sit above your emotes: pick a slot,
# then an emote to put in it (if that emote is already on the wheel the two swap); the x on a slot empties it.
# Slot 1 is what a quick tap of the Emote key plays. The wheel in game (and in the lobby) shows exactly these five.
rep("""if(!EMOTES[settings.emote]) settings.emote='dance';""","""if(!EMOTES[settings.emote]) settings.emote='dance';
if(!Array.isArray(settings.wheel)) settings.wheel=[settings.emote,...['dance','wave','cheer','salute'].filter(x=>x!==settings.emote)].slice(0,4).concat([null]);
settings.wheel=settings.wheel.slice(0,5).map(x=>EMOTES[x]?x:null); while(settings.wheel.length<5) settings.wheel.push(null);""")
rep("""      <h3 class="lk">Emotes</h3>
      <p class="lkempty">The one you pick plays on your Emote key.</p>""","""      <h3 class="lk">Emote wheel</h3>
      <p class="lkempty">Your wheel holds five. Pick a slot, then an emote below to put in it. Slot 1 plays on a quick tap of the Emote key.</p>
      <div id="wheelSlots" class="wheelslots" role="listbox" aria-label="Emote wheel slots"></div>
      <h3 class="lk">Emotes</h3>""")
rep(""".ofit.on{border-color:#ffe14d;""",""".wheelslots{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-bottom:14px;max-width:470px}
.wslot{position:relative;aspect-ratio:1/1;border:2px dashed rgba(255,255,255,.28);border-radius:10px;background:rgba(255,255,255,.04);color:#fff;cursor:pointer;padding:0;font:inherit;display:flex;align-items:flex-end;justify-content:center;overflow:hidden}
.wslot.full{border-style:solid;background:linear-gradient(160deg,rgba(80,120,220,.35),rgba(20,40,110,.55))}
.wslot.sel{border-color:#ffe14d;box-shadow:0 0 0 2px #ffe14d,0 0 16px rgba(255,225,77,.4)}
.wslot>b{position:absolute;left:6px;top:4px;font:800 italic 13px/1 var(--font-hud);opacity:.85}
.wslot svg.emo{position:absolute;left:18%;top:8%;width:64%;height:58%;pointer-events:none}
.wslot span{position:relative;width:100%;padding:3px 3px 5px;font:800 italic 11px/1.05 var(--font-hud);letter-spacing:.03em;text-transform:uppercase;text-align:center;background:linear-gradient(transparent,rgba(5,10,20,.8))}
.wslot.empty span{background:none;opacity:.6;padding-bottom:40%}
.wslot .wx{position:absolute;right:3px;top:3px;width:20px;height:20px;border-radius:50%;border:0;background:rgba(0,0,0,.55);color:#fff;font:700 13px/20px system-ui;padding:0;cursor:pointer}
.wslot .wx:hover{background:#c0392b}
.emotes .ofit i.wn{position:absolute;left:5px;top:5px;min-width:18px;height:18px;border-radius:9px;background:#ffe14d;color:#1a1f33;font:800 12px/18px var(--font-hud);font-style:normal;text-align:center;z-index:1}
.ofit.on{border-color:#ffe14d;""")
rep("""  const pickEm=id=>{ const it=EMOTE_LIST.find(e=>e.id===id); if(!it) return; if(!owned('e',it)){ offerBuy('e',it); return; } buy.hidden=true; settings.emote=id; saveSettings(); mark(ebox,id); audioInit(); window._stagePrev={id,t0:performance.now()}; };""",
    """  const W=settings.wheel, wbox=$('wheelSlots'); let wsel=Math.max(0,W.indexOf(null));
  const wheelSave=()=>{ settings.emote=W.find(x=>x)||'dance'; saveSettings(); };
  const renderWheel=()=>{ wbox.innerHTML=''; W.forEach((id,k)=>{ const b=document.createElement('button'); b.type='button'; b.className='wslot'+(id?' full':' empty')+(k===wsel?' sel':''); b.setAttribute('role','option'); b.setAttribute('aria-selected',k===wsel);
      b.innerHTML=`<b>${k+1}</b>`+(id?emoteIcon(id)+`<span>${EMOTES[id].name}</span><button type="button" class="wx" aria-label="Take ${EMOTES[id].name} off the wheel">×</button>`:'<span>Empty</span>');
      b.addEventListener('click',e=>{ if(e.target.classList.contains('wx')){ e.stopPropagation(); W[k]=null; wsel=k; wheelSave(); renderWheel(); return; } wsel=k; renderWheel(); if(id){ audioInit(); window._stagePrev={id,t0:performance.now()}; } });
      wbox.appendChild(b); });
    ebox.querySelectorAll('.ofit').forEach(b=>{ const k=W.indexOf(b.dataset.id); b.classList.toggle('on',k>=0); b.setAttribute('aria-selected',k>=0); let n=b.querySelector('i.wn'); if(k>=0){ if(!n){ n=document.createElement('i'); n.className='wn'; b.prepend(n); } n.textContent=k+1; } else if(n) n.remove(); }); };
  const pickEm=(id,quiet)=>{ const it=EMOTE_LIST.find(e=>e.id===id); if(!it) return; if(!owned('e',it)){ offerBuy('e',it); return; } buy.hidden=true;
    const at=W.indexOf(id); if(at!==wsel){ if(at>=0){ W[at]=W[wsel]; W[wsel]=id; } else if(quiet&&!W.includes(null)){ /* a full wheel stays as you set it: swap it in from the Locker */ } else { if(W[wsel]&&W.includes(null)&&quiet) wsel=W.indexOf(null); W[wsel]=id; } }
    { const nx=W.indexOf(null); if(nx>=0) wsel=nx; } // move on to the next empty slot
    wheelSave(); renderWheel(); audioInit(); window._stagePrev={id,t0:performance.now()}; };""")
rep("""  if(!owned('e',EMOTE_LIST.find(e=>e.id===settings.emote)||{})){ settings.emote='dance'; saveSettings(); }
  mark(ebox,settings.emote); renderShop();""","""  W.forEach((id,k)=>{ if(id&&!owned('e',EMOTES[id]&&EMOTE_LIST.find(e=>e.id===id)||{})) W[k]=null; }); if(!W.some(x=>x)) W[0]='dance'; wsel=Math.max(0,W.indexOf(null)); wheelSave();
  renderWheel(); renderShop();""")
rep("""  window._locker={owned,price,pick,pickPk,pickEm,pickBk,offerBuy};""","""  window._locker={owned,price,pick,pickPk,pickEm,pickBk,offerBuy,renderWheel,get wsel(){ return wsel; },set wsel(v){ wsel=v; renderWheel(); }};""")
# buying puts the new emote in an empty slot when there is one
rep("""    if(k==='o') pick(it.id); else if(k==='e') pickEm(it.id); else if(k==='b') pickBk(it.id); else pickPk(it.id); });""",
    """    if(k==='o') pick(it.id); else if(k==='e') pickEm(it.id,true); else if(k==='b') pickBk(it.id); else pickPk(it.id); });""")
# the in-game wheel: exactly your five
rep("""function emoOwned(){ const L=window._locker; const ids=EMOTE_LIST.filter(e=>!L||L.owned('e',e)).map(e=>e.id); const fav=settings.emote; ids.sort((a,b)=>(b===fav)-(a===fav)); return ids.slice(0,8); }""",
    """function emoOwned(){ const L=window._locker, ok=id=>id&&EMOTES[id]&&(!L||L.owned('e',EMOTE_LIST.find(e=>e.id===id))); const w=(settings.wheel||[]).filter(ok);
  return w.length?w:EMOTE_LIST.filter(e=>!L||L.owned('e',e)).map(e=>e.id).slice(0,5); }""")
rep("""      if(own){ if(k==='o') L.pick(it.id); else if(k==='e') L.pickEm(it.id); else if(k==='b') L.pickBk(it.id); else L.pickPk(it.id); toast('Equipped '+it.name);""",
    """      if(own){ if(k==='o') L.pick(it.id); else if(k==='e') L.pickEm(it.id,true); else if(k==='b') L.pickBk(it.id); else L.pickPk(it.id); toast(k==='e'?(settings.wheel.includes(it.id)?it.name+' is on your emote wheel':'Your wheel is full: swap it in from the Locker'):'Equipped '+it.name);""")

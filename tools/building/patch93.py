# ---------- 93. a live preview of your character in the Locker and the Item Shop: wearing the outfit, holding the pickaxe,
# or doing the dance (with its beat) you click on ----------
rep("function stageVisible(){ return !menu.hidden&&menu.classList.contains('lobby')&&!document.querySelector('.mtab[data-tab=play]').hidden; }",
    "function stageVisible(){ const st=$('stage'); return !menu.hidden&&menu.classList.contains('lobby')&&!!st&&!st.parentNode.hidden; }")
rep("  if(name==='shop'&&window.renderItemShop) renderItemShop(); setTimeout(syncLobby,0);",
    "  if(name==='shop'&&window.renderItemShop) renderItemShop(); setTimeout(syncLobby,0);\n  { const stg=$('stage'), sec=document.querySelector('.mtab[data-tab=\"'+name+'\"]'); if(stg&&sec&&(name==='play'||name==='locker'||name==='shop')&&stg.parentNode!==sec) sec.prepend(stg); window._stageLook=null; window._stagePrev=null; window._stagePickT=0; }")
rep("#menu.lobby .mtab[data-tab=play]>.stage{display:block;grid-column:1;",
r"""#menu.lobby .mtab[data-tab=locker],#menu.lobby .mtab[data-tab=shop]{grid-template-columns:minmax(0,1.6fr) minmax(240px,1fr);column-gap:22px}
#menu.lobby .mtab[data-tab=locker]>*,#menu.lobby .mtab[data-tab=shop]>*{grid-column:1}
#menu.lobby .mtab[data-tab=locker]>.stage,#menu.lobby .mtab[data-tab=shop]>.stage{display:block;grid-column:2;grid-row:1 / span 20;position:sticky;top:8px;height:min(66vh,580px);min-height:300px}
@media (max-width:820px){ #menu.lobby .mtab[data-tab=locker],#menu.lobby .mtab[data-tab=shop]{grid-template-columns:minmax(0,1fr)} #menu.lobby .mtab[data-tab=locker]>.stage,#menu.lobby .mtab[data-tab=shop]>.stage{grid-column:1;grid-row:auto;position:relative;height:36vh;min-height:220px} }
#menu.lobby .mtab[data-tab=play]>.stage{display:block;grid-column:1;""")
rep("  const me={me:true,name:(net.role?net.name:($('pname').value.trim()||net.name))||'Player',o:outfitIdx(settings.outfit),pk:settings.pickaxe,ready:true};",
    "  const lk=window._stageLook||{}, me={me:true,name:(net.role?net.name:($('pname').value.trim()||net.name))||'Player',o:lk.o!=null?lk.o:outfitIdx(settings.outfit),pk:lk.pk||settings.pickaxe,ready:true};")
rep("st={bare:true,pos:e.pos,vel:_stZ,","st={bare:!(i===0&&(window._stagePickT||0)>now),pos:e.pos,vel:_stZ,")
rep("    animateRig(e.h,st,dt); e.h.rig.pick.visible=false;",
    "    animateRig(e.h,st,dt); e.h.rig.pick.visible=i===0&&(window._stagePickT||0)>now&&!st.emote;\n    if(i===0&&st.emote&&EMOTES[st.emote.id].beat){ const bb=Math.floor(st.emote.t*EMOTES[st.emote.id].beat); if(bb!==S.beat){ S.beat=bb; if(AC) sfx(bb%4===2?'beat_snare':'beat_kick'); } }")
rep("  const pickPk=id=>{ const it=PICKAXES[pickIdx(id)]; if(!owned('p',it)){ offerBuy('p',it); return; } buy.hidden=true; settings.pickaxe=id; saveSettings(); wear(); mark(pbox,id); };",
    "  const pickPk=id=>{ const it=PICKAXES[pickIdx(id)]; if(!owned('p',it)){ offerBuy('p',it); return; } buy.hidden=true; settings.pickaxe=id; saveSettings(); wear(); mark(pbox,id); window._stagePrev=null; window._stagePickT=performance.now()+8000; };")
rep("buy.hidden=true; settings.emote=id; saveSettings(); mark(ebox,id); window._stagePrev={id,t0:performance.now()}; };","buy.hidden=true; settings.emote=id; saveSettings(); mark(ebox,id); audioInit(); window._stagePrev={id,t0:performance.now()}; };")
rep("    b.addEventListener('click',()=>{ if(own){ if(k==='o') L.pick","    b.addEventListener('click',()=>{ audioInit(); if(k==='o'){ window._stageLook={o:outfitIdx(it.id)}; window._stagePrev=null; } else if(k==='p'){ window._stageLook={pk:it.id}; window._stagePrev=null; window._stagePickT=performance.now()+12000; } else { window._stageLook=null; window._stagePrev={id:it.id,t0:performance.now()}; }\n      if(own){ if(k==='o') L.pick")

# ---------- 83. HUD rework (keyboard and mouse): shield and health as wide flat bars bottom-centre with the ammo count over
# them, the weapon bar bottom-right with its name above, material counts stacked above that, and a squad panel top-left
# (you and your teammates, with their state). Phones keep their own layout. ----------
rep('<div class="hud" id="feed"></div>','<div class="hud" id="squad" hidden></div>\n<div class="hud" id="feed"></div>')
rep("#xAmmo.low{color:#ff8a78}",r"""#xAmmo.low{color:#ff8a78}
#squad{top:calc(env(safe-area-inset-top,0px) + 12px);left:calc(env(safe-area-inset-left,0px) + 12px);display:grid;gap:5px;min-width:190px}
#squad .sq{display:grid;gap:3px;padding:6px 10px 7px;background:linear-gradient(90deg,rgba(8,14,26,.72),rgba(8,14,26,.25));border-left:3px solid #3f8fff;border-radius:2px}
#squad .sq.me{border-left-color:#ffe14d} #squad .sq.bad{border-left-color:#ff6a4a}
#squad .sq b{font:800 italic 15px/1 var(--font-hud);letter-spacing:.04em;text-shadow:0 1px 2px #000;display:flex;justify-content:space-between;gap:10px} #squad .sq b em{font-style:italic;font-size:12px;color:#ffb09a;letter-spacing:.08em;text-transform:uppercase}
#squad .sq i{display:block;height:4px;background:rgba(255,255,255,.14);border-radius:1px;overflow:hidden} #squad .sq i u{display:block;height:100%}
#squad .sq i.s u{background:var(--shield)} #squad .sq i.h u{background:var(--health)}
body.touch #squad{display:none}
body:not(.touch) #feed{top:calc(env(safe-area-inset-top,0px) + 12px);left:calc(env(safe-area-inset-left,0px) + 214px)}
body:not(.touch) #bottom{left:0;right:0;transform:none;bottom:0;height:0;display:block}
body:not(.touch) #vitals{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(env(safe-area-inset-bottom,0px) + 14px);width:min(380px,36vw);gap:3px}
body:not(.touch) .vit{grid-template-columns:20px 1fr;gap:7px}
body:not(.touch) .vit::before{content:"";grid-column:1;grid-row:1;justify-self:center;width:15px;height:17px;background:#e9f4ff;filter:drop-shadow(0 1px 1px rgba(0,0,0,.7))}
body:not(.touch) .vit.sh::before{clip-path:polygon(50% 0,100% 16%,100% 56%,50% 100%,0 56%,0 16%)}
body:not(.touch) .vit.hp::before{clip-path:polygon(34% 0,66% 0,66% 34%,100% 34%,100% 66%,66% 66%,66% 100%,34% 100%,34% 66%,0 66%,0 34%,34% 34%)}
body:not(.touch) .vit .bar{grid-column:2;grid-row:1;height:22px;transform:none;border:0;border-radius:2px;background:rgba(8,14,26,.72);box-shadow:0 0 0 1px rgba(0,0,0,.35)}
body:not(.touch) .vit.hp .bar{height:24px}
body:not(.touch) .vit b{grid-column:2;grid-row:1;z-index:1;justify-self:start;align-self:center;padding-left:9px;font-size:16px;text-align:left;text-shadow:0 1px 2px rgba(0,0,0,.9)}
body:not(.touch) .vit b::after{content:" | 100";opacity:.65;font-size:13px}
body:not(.touch) #wbar,body:not(.touch) #bbar{position:absolute;right:calc(env(safe-area-inset-right,0px) + 14px);bottom:calc(env(safe-area-inset-bottom,0px) + 14px)}
body:not(.touch) .wname{position:absolute;right:calc(env(safe-area-inset-right,0px) + 16px);bottom:calc(env(safe-area-inset-bottom,0px) + 86px);padding:0;font-size:17px;white-space:nowrap}
body:not(.touch) .slot{border-radius:3px}
body:not(.touch) #xAmmo{left:50%;top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + 72px);transform:translateX(-50%);font-size:26px;opacity:1;padding:3px 12px 2px;background:rgba(8,14,26,.5);border-radius:3px;font-variant-numeric:tabular-nums}
body:not(.touch) #matStock{top:auto;bottom:calc(env(safe-area-inset-bottom,0px) + 116px);display:flex;gap:5px}
body:not(.touch) #matStock span{flex-direction:column;gap:4px;min-width:50px;padding:6px 6px 5px;justify-content:center;font-size:17px;border-radius:3px}
body:not(.touch) #matStock i{width:22px;height:22px}
@media (max-width:900px){ body:not(.touch) #vitals{left:calc(env(safe-area-inset-left,0px) + 14px);transform:none;width:240px} body:not(.touch) #xAmmo{left:134px} }""")
rep("function updateCombatHUD(){\n  stepDmgNums(lastDt);","""function squadTick(){ const el=$('squad'); if(!el||isTouch) return; const on=!$('vitals').hidden&&playing&&(horde.on||!!net.role); if(el.hidden===on) el.hidden=!on; if(!on) return;
  const R=v=>Math.max(0,Math.min(100,Math.round(v))), rows=[{n:net.name||$('pname').value.trim()||'You',sh:R(P.sh),hp:R(P.hp),me:1,st:P.down?'Knocked':isDead()?'Eliminated':''}];
  net.players.forEach(pl=>{ if(pl.id!=='bot'&&sameTeam(pl)) rows.push({n:pl.name||'Player',sh:R(pl.sh||0),hp:null,st:!pl.alive?'Eliminated':(pl.flags&256)?'Knocked':''}); });
  if(typeof AB!=='undefined'&&AB&&AB.active) rows.push({n:'Buddy',sh:R(AB.sh),hp:R(AB.dead?0:AB.down?AB.hp*10:AB.hp),st:AB.dead?'Eliminated':AB.down?'Knocked':''});
  const html=rows.map(r=>`<div class="sq${r.me?' me':''}${r.st?' bad':''}"><b>${esc(r.n)}${r.st?`<em>${r.st}</em>`:''}</b><i class="s"><u style="width:${r.sh}%"></u></i>${r.hp==null?'':`<i class="h"><u style="width:${r.hp}%"></u></i>`}</div>`).join('');
  if(html!==squadTick.h){ squadTick.h=html; el.innerHTML=html; } }
function updateCombatHUD(){
  stepDmgNums(lastDt); squadTick();""")

# ---------- 31. map buildings can't be edited; Interact swaps what you're holding for a weapon on the ground ----------
rep("function canEdit(p,who){\n  if(!p.owner||","function canEdit(p,who){\n  if(p.owner==='world') return false; // houses and garages on the map: farm them, break them, never edit them\n  if(!p.owner||")
# when your slots are full, Interact on a weapon or item swaps it for the one in your hands (that one drops at your feet)
rep("""  if(t.kind==='drop'){ const d=t.d; if(!canTake(d)){ if(performance.now()-fullToastT>1500){ fullToastT=performance.now(); toast('Inventory full – press '+codeName(settings.binds.inventory||'Tab')+' to swap'); } return; } takeDrop(d,null); }""",
"""  if(t.kind==='drop'){ const d=t.d;
    if(!canTake(d)){ const i=swapSlotFor(d);
      if(i>=0){ dropFromSlot(i); takeDrop(d,i); if(net.role!=='client') selectSlot(i); return; }
      if(performance.now()-fullToastT>1500){ fullToastT=performance.now(); toast('Inventory full – hold a weapon or item to swap it'); } return; }
    takeDrop(d,null); }""")
rep("function canTake(d){","""// the slot a full inventory would swap: the one in your hands (not the pickaxe)
function swapSlotFor(d){ if(AMMO_T[d.item]||P.slot<0||!P.inv[P.slot]||P.useT>0) return -1; return isWeapon(d.item)||isItem(d.item)||d.item==='nade'?P.slot:-1; }
function canTake(d){""")
rep("consider(d.pos.x,d.pos.y,d.pos.z,1.9,{kind:'drop',d,label:'Pick up '+itemInfo(d.item).name+(isWeapon(d.item)&&d.item!=='nade'?'':' ×'+d.n)}); });",
    "const nm=itemInfo(d.item).name+(isWeapon(d.item)&&d.item!=='nade'?'':' ×'+d.n), sw=canTake(d)?-1:swapSlotFor(d); consider(d.pos.x,d.pos.y,d.pos.z,1.9,{kind:'drop',d,label:sw>=0?'Swap '+itemInfo(P.inv[sw]).name+' for '+nm:'Pick up '+nm}); });")
rep("if(m.to===net.id&&m.item) grant(m.item,m.n,sw==null?null:sw); }","if(m.to===net.id&&m.item){ grant(m.item,m.n,sw==null?null:sw); if(sw!=null&&P.inv[sw]===m.item) selectSlot(sw); } }")
# --- scopes zoom: the mouse wheel steps through three magnifications on PC; on touch screens the scope opens a step closer ---
rep('<div id="scope" hidden><i class="h"></i><i class="v"></i><i class="m"></i><i class="c"></i></div>','<div id="scope" hidden><i class="h"></i><i class="v"></i><i class="m"></i><i class="c"></i><b id="scopeZ"></b></div>')
rep("#scope{--R:min(34vh,34vw)}","#scope{--R:min(34vh,34vw)}\n#scopeZ{position:absolute;left:50%;top:calc(50% + var(--R) - 34px);transform:translateX(-50%);font:800 italic 15px/1 var(--font-hud);color:rgba(255,255,255,.85);text-shadow:0 1px 3px #000;letter-spacing:.04em}")
rep("let scopeOn=false;","let scopeOn=false, scopeLvl=0; const SCOPE_STEPS=[1,0.6,0.36]; // field of view multiplied on top of the scope's own zoom")
rep("if(on!==scopeOn){ scopeOn=on; $('scope').hidden=!on; document.body.classList.toggle('scoped',on); } }",
    "if(on!==scopeOn){ scopeOn=on; $('scope').hidden=!on; document.body.classList.toggle('scoped',on); scopeLvl=on&&isTouch?1:0; applyFov(); scopeLabel(); } }")
rep("function applyFov(){","""function scopeLabel(){ const el=$('scopeZ'); if(!el||!scopeOn) return; el.textContent=(settings.fov/camera.fov).toFixed(1).replace(/\\.0$/,'')+'×'; }
function scopeZoom(dir){ const n=Math.max(0,Math.min(SCOPE_STEPS.length-1,scopeLvl+dir)); if(n===scopeLvl) return; scopeLvl=n; applyFov(); scopeLabel(); sfx('scope_click'); }
function applyFov(){""")
rep("  camera.updateProjectionMatrix();\n}","  if(AW.scope) camera.fov*=1+(SCOPE_STEPS[scopeLvl]-1)*adsK;\n  camera.updateProjectionMatrix();\n}")
rep("  if(!playing||isTouch) return;\n  e.preventDefault();\n  const c=e.deltaY<0?'WheelUp':'WheelDown';","  if(!playing||isTouch) return;\n  e.preventDefault();\n  if(scopeOn){ scopeZoom(e.deltaY<0?1:-1); return; } // through a scope the wheel zooms\n  const c=e.deltaY<0?'WheelUp':'WheelDown';")
s=s.replace("*(scopeOn?0.45:1)*(edit?settings.editSens:1)","*(scopeOn?0.45*Math.sqrt(SCOPE_STEPS[scopeLvl]):1)*(edit?settings.editSens:1)")
rep("    case 'kart_start':","    case 'scope_click': knock(2600,0.03,0.08,8); knock(1700,0.03,0.05,8,0.025); break;\n    case 'kart_start':")
rep("  if(adsK!==prevK) applyFov();","  if(adsK!==prevK){ applyFov(); scopeLabel(); }")

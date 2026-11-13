# patch204: harvesting like Fortnite (harvest.js): a weak point to hit for double damage that moves each time you hit
# it, and a health bar for whatever you're breaking
rep("""function swing(fromImpact){""",open('/home/claude/mg/harvest.js').read().rstrip()+"""
function swing(fromImpact){""")
rep("""    if(dh&&dh.s.dobj&&!dh.s.dobj.gone&&(!hit||dh.t<hit.distance)){ const pt=o.addScaledVector(d,dh.t); dmgNum(pt,PICK_DMG,'build'); sfx('pick_hit'); decoDamage(dh.s.dobj,PICK_DMG,pt,true); return; } }""",
"""    if(dh&&dh.s.dobj&&!dh.s.dobj.gone&&(!hit||dh.t<hit.distance)){ const pt=o.addScaledVector(d,dh.t), ob=dh.s.dobj, m=harvHit({key:ob,point:pt.clone(),normal:d.clone().negate(),boxes:dh.s.boxes,big:true}), dmg=PICK_DMG*m;
      dmgNum(pt,dmg,m>1?'head':'build'); sfx('pick_hit'); decoDamage(ob,dmg,pt,true); harvBar('Object',ob.gone?0:ob.hp,ob.hp0||ob.hp); return; } }""")
rep("""  if(hit&&hit.object.userData.piece&&hit.object.userData.piece.isProp){ propHit(hit.object.userData.piece,PICK_DMG,hit.point,true); return; }""",
"""  if(hit&&hit.object.userData.piece&&hit.object.userData.piece.isProp){ const pp=hit.object.userData.piece, d0=aimDir(), m=harvHit({key:pp,point:hit.point.clone(),normal:harvNormal(hit,d0),mesh:hit.object,big:pp.kind!=='furn'}); pp.hpMax=pp.hpMax||Math.max(pp.hp,(PROP_T[pp.kind]||{}).hp||pp.hp);
    if(m>1) dmgNum(hit.point,PICK_DMG*m,'head'); propHit(pp,PICK_DMG*m,hit.point,true); harvBar(PROP_NAME[pp.kind]||'Object',pp.hp,pp.hpMax); return; }""")
rep("""  if(hit){ const hp_=hit.object.userData.piece; dmgNum(hit.point,PICK_DMG,'build'); sfx('pick_hit'); damagePiece(hp_,PICK_DMG,hit.point);""",
"""  if(hit){ const hp_=hit.object.userData.piece, m=hp_?harvHit({key:hp_,point:hit.point.clone(),normal:harvNormal(hit,aimDir()),mesh:hit.object,big:true}):1; dmgNum(hit.point,PICK_DMG*m,m>1?'head':'build'); sfx('pick_hit'); damagePiece(hp_,PICK_DMG*m,hit.point); if(hp_) harvBar(pieceName(hp_),pieces.has(hp_.key)?hp_.hp:0,hp_.maxHp||hp_.hp);""")
# the bar under the crosshair
rep("""<div id="stormFx" hidden></div>""","""<div id="harvBar" class="hud" hidden><span id="harvName"></span><span class="hb"><i id="harvFill"></i></span><span id="harvNum"></span></div><div id="stormFx" hidden></div>""")
rep("""#stormFx{""","""#harvBar{left:50%;top:calc(50% + 46px);transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:3px;pointer-events:none;font:800 italic 13px/1 var(--font-hud);text-transform:uppercase;letter-spacing:.04em;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.8)}
#harvBar .hb{width:150px;height:9px;border-radius:5px;background:rgba(8,14,30,.6);box-shadow:0 0 0 1px rgba(255,255,255,.35);overflow:hidden} #harvBar .hb i{display:block;height:100%;width:100%;background:linear-gradient(#7ee36f,#3fae3a);transition:width .12s}
#harvBar.low .hb i{background:linear-gradient(#ffb15a,#e0622a)} #harvNum{font-size:11px;opacity:.9;font-style:normal}
#stormFx{""")
rep("  stepOcean(lastDt); stepIndoor(lastDt);","  stepOcean(lastDt); stepIndoor(lastDt); try{ stepHarv(lastDt); }catch(e){}")

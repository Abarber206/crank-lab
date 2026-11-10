# ---------- 62. knocked down (DBNO) before the reboot card ----------
# In a party with a teammate still standing, hitting 0 HP knocks you down instead: you drop and crawl slowly at 10 HP,
# which bleeds away over ~30 s (hits drain it faster). A teammate holds Interact on you for a few seconds to revive you
# (you stand up with 30 HP). Bleed out and you're eliminated: your reboot card drops and the reboot system takes over.
rep("    case 'rb_tick':","""    case 'rb_down': tone('sine',300,140,0.5,0.12); noise(500,0.3,0.15,0.8,0,'lowpass',150); break;
    case 'rb_up': tone('triangle',440,660,0.18,0.1); tone('triangle',660,990,0.25,0.09,0.12); noise(4000,0.2,0.05,1,0.05,'highpass'); break;
    case 'rb_tick':""")
rep('<span class="rbt">Eliminated</span>','<span class="rbt" id="rbT">Eliminated</span>')
rep("#rbWait .rbt{","#rbWait.down{border-color:rgba(255,120,90,.55)} #rbWait.down .rbbar i{background:linear-gradient(90deg,#ff5a3a,#ffb07a)} #rbWait .rbt{")
# you got hit: knocked instead of eliminated when a teammate can come for you; hits on a downed player drain its 10 HP
rep("  if(hurt(P,m.dmg)){ net.dead=true; net.deaths++; animEvent(localHero,'die'); const e={type:'elim',id:net.id,by:m.id,w:m.w}; onElim(e); netSend(e);\n    afterDeath(); }",
    "  if(P.down){ P.hp-=Math.max(1,m.dmg*0.25); if(P.hp<=0) rbBleedOut(); return; }\n  if(hurt(P,m.dmg)){ if(rbCanKnock()){ rbKnock(m.id,m.w); return; } net.dead=true; net.deaths++; animEvent(localHero,'die'); const e={type:'elim',id:net.id,by:m.id,w:m.w}; onElim(e); netSend(e);\n    afterDeath(); }")
# no shooting, building, items, interacting or jumping while down; crawling is slow
rep("function fireDown(src){\n  if(isDead()||P.sky||","function fireDown(src){\n  if(isDead()||P.down||P.sky||")
rep("function tryPlace(type,E=P){\n  if(E===P&&isDead()||E.sky||E.kart) return false;","function tryPlace(type,E=P){\n  if(E===P&&(isDead()||P.down)||E.sky||E.kart) return false;")
rep("  const ms=(1-0.35*adsK)*(P.useT>0?0.55:1); moveBody(P,fw*ms,st*ms,isHeld('jump')||touchJump,dt);",
    "  const ms=(1-0.35*adsK)*(P.useT>0?0.55:1)*(P.down?0.2:1); moveBody(P,fw*ms,st*ms,(isHeld('jump')||touchJump)&&!P.down,dt);")
rep("    if(isDead()){ P.vel.x=0; P.vel.z=0; fireHeld=false; heldPiece=null; if(edit) exitEdit(false); } else moveInput(dt);",
    "    if(isDead()){ P.vel.x=0; P.vel.z=0; fireHeld=false; heldPiece=null; if(edit) exitEdit(false); } else moveInput(dt);\n    if(P.down){ fireHeld=false; heldPiece=null; adsHeld=false; P.crouch=false; P.useT=0; P.emote=null; if(edit) exitEdit(false); }")
rep("  if(!playing||isDead()||edit||invOpen||P.sky) return null;","  if(!playing||isDead()||P.down||edit||invOpen||P.sky) return null;")
# everyone sees you down: a state flag, and the crawl pose
rep("|(P.sky?(P.sky.phase==='glide'?128:64):0);\n  return {type:'st'","|(P.sky?(P.sky.phase==='glide'?128:64):0)|(P.down?256:0);\n  return {type:'st'")
rep("animateRig(localHero,{slope:slopeFor(P),","animateRig(localHero,{down:!!P.down,slope:slopeFor(P),")
rep("emote:pl.emote,sky:(pl.flags&128)?'glide':(pl.flags&64)?'fall':null,","emote:pl.emote,down:!!(pl.flags&256),sky:(pl.flags&128)?'glide':(pl.flags&64)?'fall':null,")
rep("  // ----- skydiving / gliding; afterwards the body levels out and the glider folds away -----\n  if(S.sky){ animateSky(H,S,dt); return; }",
r"""  // ----- knocked down: face down, dragging yourself along on your forearms -----
  if(S.down){ A.downT=Math.min(1,(A.downT||0)+dt*2.2); const e=A.downT*A.downT*(3-2*A.downT), set=(o,ax,v,f)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,f||sm); };
    G.rotation.x=lerp(G.rotation.x,-1.38*e,Math.min(1,dt*10)); G.rotation.z=0; G.position.y=S.pos.y+0.3*e;
    A.crawl=(A.crawl||0)+dt*(1.2+Math.min(1.5,sp)*4.5); const c1=Math.sin(A.crawl), c2=Math.sin(A.crawl+Math.PI), mvK=Math.min(1,sp/0.6);
    r.hips.position.y=lerp(r.hips.position.y,0.94,sm); set(r.hips,'x',0); set(r.hips,'y',0.12*c1*mvK); set(r.hips,'z',0); set(r.spine,'x',-0.1); set(r.spine,'y',0); set(r.chest,'x',-0.15); set(r.chest,'y',-0.1*c1*mvK); set(r.chest,'z',0);
    set(r.neck,'x',-0.75); set(r.neck,'y',0); set(r.neck,'z',0);
    set(r.armL.sh,'x',2.5+0.45*c1*mvK); set(r.armR.sh,'x',2.5+0.45*c2*mvK); set(r.armL.sh,'z',-0.35); set(r.armR.sh,'z',0.35); set(r.armL.sh,'y',0); set(r.armR.sh,'y',0);
    set(r.armL.el,'x',0.9+0.5*Math.max(0,-c1)*mvK); set(r.armR.el,'x',0.9+0.5*Math.max(0,-c2)*mvK); set(r.armL.wr,'x',0.3); set(r.armR.wr,'x',0.3);
    for(const [L,cc] of [[r.legL,c2],[r.legR,c1]]){ set(L.hp,'x',-0.08+0.35*Math.max(0,cc)*mvK); set(L.hp,'z',0); set(L.kn,'x',-0.25-0.75*Math.max(0,cc)*mvK); set(L.an,'x',0.5); }
    for(const k of GUN_MODELS) if(r[k]) r[k].visible=false; r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; r.pick.visible=false;
    if(H.glider) H.glider.visible=false; return; }
  A.downT=0;
  // ----- skydiving / gliding; afterwards the body levels out and the glider folds away -----
  if(S.sky){ animateSky(H,S,dt); return; }""")
# downed teammates don't count as standing
rep("function rbMatesUp(){ let n=0; net.players.forEach(pl=>{ if(pl.id!=='bot'&&pl.alive&&sameTeam(pl)) n++; }); return n; }",
    "function rbMatesUp(){ let n=0; net.players.forEach(pl=>{ if(pl.id!=='bot'&&pl.alive&&!(pl.flags&256)&&sameTeam(pl)) n++; }); return n; }")
rep("function rbTargets(consider){ if(!net.role) return; const now=performance.now();",
r"""function rbTargets(consider){ if(!net.role) return; const now=performance.now();
  net.players.forEach(pl=>{ if(pl.id==='bot'||!pl.alive||!(pl.flags&256)||!sameTeam(pl)) return; const rv=RB.rev.get(pl.id)||0;
    consider(pl.pos.x,pl.pos.y,pl.pos.z,2.3,{kind:'revive',pri:3,pl,label:'Revive '+(pl.name||'teammate'),prog:()=>RB.rev.get(pl.id)||0,busy:()=>(RB.rev.get(pl.id)||0)>0?'Reviving '+(pl.name||'teammate'):null}); });""")
rep("var VANS; var RB={cards:new Map(),","var VANS; var RB={rev:new Map(),cards:new Map(),")
rep("var RB_TTL=100, RB_GRAB_T=1.0, RB_BOOT_T=4, RB_VAN_CD=25;","var RB_TTL=100, RB_GRAB_T=1.0, RB_BOOT_T=4, RB_VAN_CD=25, RB_REV_T=3.5, RB_DOWN_HP=10, RB_BLEED=30, RB_UP_HP=30;")
rep("function onRb(m){ const now=performance.now();",r"""function rbCanKnock(){ return !!net.role&&(horde.on||+settings.team>0)&&rbMatesUp()>0&&!P.sky&&!P.down; }
function rbKnock(by,w){ kartForget(); P.down={by,w,t0:performance.now(),noMate:0}; P.hp=RB_DOWN_HP; P.sh=0; P.crouch=false; P.useT=0; P.reloadT=0; if(edit) exitEdit(false); if(mode==='build') selectPick();
  animEvent(localHero,'hurt'); sfx('rb_down'); banner('Knocked','Hang on · a teammate can revive you',2); rbSend({op:'down',id:net.id,by,w}); }
function rbBleedOut(){ if(!P.down) return; const d=P.down; P.down=null; P.hp=0; net.dead=true; net.deaths++; animEvent(localHero,'die'); const e={type:'elim',id:net.id,by:d.by||net.id,w:d.w||'zombie'}; onElim(e); netSend(e); afterDeath(); }
function onRb(m){ const now=performance.now();
  if(m.op==='down'){ if(m.id!==net.id){ const pl=net.players.get(m.id), nm=esc((pl&&pl.name)||'A teammate'); if(pl&&sameTeam(pl)){ feed(`<b>${nm}</b> is down · hold Interact on them to revive`); if(pl.pos) sfxAt('rb_down',pl.pos); } else if(m.by===net.id) feed(`You knocked <b>${nm}</b>`); } return; }
  if(m.op==='rev'){ RB.rev.delete(m.id); if(m.id===net.id&&P.down){ P.down=null; P.hp=RB_UP_HP; P.sh=0; animEvent(localHero,'revive'); sfx('rb_up'); const pl=net.players.get(m.by); banner('Revived','by '+((pl&&pl.name)||'a teammate'),1.6); rbSend({op:'up',id:net.id,by:m.by}); } return; }
  if(m.op==='up'){ RB.rev.delete(m.id); if(m.by===net.id){ const pl=net.players.get(m.id); feed(`You revived <b>${esc((pl&&pl.name)||'a teammate')}</b>`); sfx('rb_up'); } return; }""")
# the hold-to-revive, the bleed-out, and the knocked panel
rep("function stepReboot(dt){ if(!net.role&&!RB.cards.size) return; const now=performance.now(), T=now/1000;",
r"""function stepReboot(dt){ if(!net.role&&!RB.cards.size&&!P.down) return; const now=performance.now(), T=now/1000;
  // reviving someone: hold Interact on them
  net.players.forEach(pl=>{ const on=useHeld&&useTgt&&useTgt.kind==='revive'&&useTgt.pl===pl&&!isDead()&&!P.down&&(pl.flags&256); let v=RB.rev.get(pl.id)||0;
    if(on){ if(v>=0){ v+=dt/RB_REV_T; if(v>=1){ v=-1; rbSend({op:'rev',id:pl.id,by:net.id}); setTimeout(()=>{ if(RB.rev.get(pl.id)===-1) RB.rev.delete(pl.id); },2500); } RB.rev.set(pl.id,v); } }
    else if(v>0){ v=Math.max(0,v-dt*2); if(v>0) RB.rev.set(pl.id,v); else RB.rev.delete(pl.id); }
    if(!(pl.flags&256)&&v>=0) RB.rev.delete(pl.id); });
  // you, down: bleeding out (and right away if nobody's left standing to come for you)
  if(P.down){ P.hp-=dt*RB_DOWN_HP/RB_BLEED; if(rbMatesUp()===0){ P.down.noMate+=dt; if(P.down.noMate>2) P.hp=0; } else P.down.noMate=0;
    if(P.hp<=0||isDead()) rbBleedOut(); }""")
rep("  const el=$('rbWait');\n  if(RB.wait){",
r"""  const el=$('rbWait'); el.classList.toggle('down',!!P.down);
  if(P.down){ if(el.hidden) el.hidden=false; if($('rbT').textContent!=='Knocked') $('rbT').textContent='Knocked'; let rv=null; net.players.forEach(pl=>{ if(!rv&&pl.alive&&!(pl.flags&256)&&sameTeam(pl)&&Math.hypot(pl.pos.x-P.pos.x,pl.pos.z-P.pos.z)<2.6) rv=pl; });
    const msg=rv?(rv.name||'A teammate')+' is here · hang on':'Crawl to cover · a teammate can revive you'; if($('rbMsg').textContent!==msg) $('rbMsg').textContent=msg;
    const sub='Bleeding out · '+Math.max(0,Math.ceil(P.hp))+' HP'; if($('rbSub').textContent!==sub) $('rbSub').textContent=sub; $('rbBar').style.transform='scaleX('+Math.max(0,P.hp/RB_DOWN_HP).toFixed(3)+')'; }
  else if(RB.wait&&$('rbT').textContent!=='Eliminated') $('rbT').textContent='Eliminated';
  if(RB.wait){""")
rep("  if(!RB.wait&&!el.hidden) el.hidden=true;","  if(!RB.wait&&!P.down&&!el.hidden) el.hidden=true;")
# leaving, respawning or a new match clears being down
rep("function rbReset(){","function rbReset(){ P.down=null; RB.rev.clear();")
rep("function respawn(){ animEvent(localHero,'revive');","function respawn(){ P.down=null; animEvent(localHero,'revive');")
# zombies leave downed players alone (otherwise a swarm finishes you before anyone can reach you)
rep("function hordeTargets(){ const a=[]; if(!(net.dead||P.hp<=0)) a.push(P); net.players.forEach(pl=>{ if(pl.alive&&pl.id!=='bot') a.push(pl); }); return a; }",
    "function hordeTargets(){ const a=[]; if(!(net.dead||P.hp<=0||P.down)) a.push(P); net.players.forEach(pl=>{ if(pl.alive&&pl.id!=='bot'&&!(pl.flags&256)) a.push(pl); }); return a; }")
rep('Update: Nov 9 · new lobby &amp; Item Shop, realistic gun sounds, glass windows, buggy fixes','Update: Nov 9 · knocked &amp; revive, reboot cards &amp; vans, new lobby &amp; Item Shop, realistic gun sounds')

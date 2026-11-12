# patch163: fixes from play-testing.
#  - Zombie horde with other players: once you're knocked the zombies leave you alone (a claw already on its way, or a
#    thrown chunk, used to finish you off in a second, so it looked like you just died). Same for a knocked teammate.
#  - The storm wall only shows during a Battle royale match, never behind the lobby.
#  - The mode button under the Play button says "Battle royale" when that's the mode.
#  - The new sound code can't stop the game: anything odd about a sound's position is ignored rather than thrown.
rep("""function zombieDamage(who,dmg,from){ // the host hands out creature damage
  if(who===P) hordeHurtMe(dmg,from);""","""function zombieDamage(who,dmg,from){ // the host hands out creature damage
  if((who===P&&P.down)||(who===AB&&AB&&AB.down)||(who.flags&256)) return; // knocked: left alone
  if(who===P) hordeHurtMe(dmg,from);""")
rep("""  if(P.down){ P.hp-=Math.max(1,m.dmg*0.25); if(P.hp<=0) rbBleedOut(); return; }""","""  if(P.down){ if(m.id==='zombie') return; P.hp-=Math.max(1,m.dmg*0.25); if(P.hp<=0) rbBleedOut(); return; }""")
rep("""$('modeName').textContent=m==='horde'?'Zombie horde':'Build fight';""","""$('modeName').textContent=m==='horde'?'Zombie horde':m==='br'?'Battle royale':'Build fight';""")
rep("""  const W=BR.wall; W.position.set(S.cx,-60,S.cz);""","""  const W=BR.wall; W.visible=!lobbyActive(); W.position.set(S.cx,-60,S.cz);""")
rep("""  $('stormFx').hidden=!(playing&&!BR.out&&!P.bus&&brOut(P,S));""","""  $('stormFx').hidden=!(playing&&!BR.out&&!P.bus&&!lobbyActive()&&brOut(P,S));""")
rep("""function panAt(p,pos){ if(p.positionX){""","""function panAt(p,pos){ if(!pos||!isFinite(pos.x)||!isFinite(pos.y)||!isFinite(pos.z)) return; if(p.positionX){""")
rep("""function audioListen(){ if(!AC) return; const L=AC.listener,""","""function audioListen(){ try{ audioListen0(); }catch(e){} }
function audioListen0(){ if(!AC) return; const L=AC.listener,""")
rep("""  if(sfxPos){ const p=mkPanner(); panAt(p,sfxPos); n.connect(p).connect(master); } else n.connect(master);""","""  let panned=false; if(sfxPos) try{ const p=mkPanner(); panAt(p,sfxPos); n.connect(p).connect(master); panned=true; }catch(e){} if(!panned) n.connect(master);""")
rep("""  return {g,p,set(v,pos){ g.gain.setTargetAtTime(v,AC.currentTime,0.15); if(pos) panAt(p,pos); },""","""  return {g,p,set(v,pos){ try{ g.gain.setTargetAtTime(v,AC.currentTime,0.15); if(pos) panAt(p,pos); }catch(e){} },""")
# the emote wheel opens anywhere in a match (on the bus, skydiving, in a car); an emote picked in the air plays when you land
rep("""function emoKeyDown(){ if(!playing||isDead()||P.down||P.sky||P.kart) { startEmote(settings.emote); return; } emoOpen('key'); }""",
"""function emoKeyDown(){ if(!playing||isDead()||P.down) { startEmote(settings.emote); return; } emoOpen('key'); }""")
rep("""    else if(act==='emote'){ if(P.kart||P.sky||P.down) startEmote(settings.emote); else emoOpen('touch'); }""","""    else if(act==='emote'){ if(P.down) startEmote(settings.emote); else emoOpen('touch'); }""")
rep("""function emoPlay(id,how){ if(how==='lobby'){ LOBBY.emote={id,t:0,beat:-1,n:((LOBBY.emote&&LOBBY.emote.n)|0)+1}; audioInit(); return; } P.emote=null; startEmote(id); }""",
"""function emoPlay(id,how){ if(how==='lobby'){ LOBBY.emote={id,t:0,beat:-1,n:((LOBBY.emote&&LOBBY.emote.n)|0)+1}; audioInit(); return; } P.emote=null; if(!P.onGround||P.sky||P.bus||P.kart){ P.emoteQ=id; toast('Emote when you land'); return; } startEmote(id); }""")
rep("""    combatTick(dt);""","""    combatTick(dt); if(P.emoteQ&&P.onGround&&!P.sky&&!P.bus&&!P.kart){ const q=P.emoteQ; P.emoteQ=null; startEmote(q); }""")
# riding the bus: the near plane moves out too (house roofs far below were flickering, as they once did skydiving)
rep("""  { let nr=0.08; if(P.sky){""","""  { let nr=0.08; if(P.bus){ const clr=camera.position.y-terrainH(camera.position.x,camera.position.z); nr=Math.max(0.08,Math.min(camDist*0.45,clr*0.15,6)); } else if(P.sky){""")
# no sound under the loading screen
rep("""  el.hidden=false; LOAD.on=true; const t0=performance.now(), T=secs*1000; let lastN=-1, tipT=t0;""","""  el.hidden=false; LOAD.on=true; if(master) master.gain.setTargetAtTime(0,AC.currentTime,0.05); const t0=performance.now(), T=secs*1000; let lastN=-1, tipT=t0;""")
rep("""if(n<=3&&n>0) sfx('equip'); }""","""}""")
rep("""    if(k<1) requestAnimationFrame(step); else { LOAD.on=false; setTimeout(()=>{ el.hidden=true; },250); if(done) done(); } };""","""    if(k<1) requestAnimationFrame(step); else { LOAD.on=false; if(master) master.gain.setTargetAtTime(0.9,AC.currentTime,0.3); setTimeout(()=>{ el.hidden=true; },250); if(done) done(); } };""")
rep("""function hideLoading(){ LOAD.on=false; $('loadScr').hidden=true; }""","""function hideLoading(){ if(LOAD.on&&master) master.gain.setTargetAtTime(0.9,AC.currentTime,0.3); LOAD.on=false; $('loadScr').hidden=true; }""")
# a slower storm: about 15 minutes from the first circle to the last
rep("""const BR_N=19, BR_SHRINK=[[60,0.62,45],[50,0.4,40],[45,0.24,35],[40,0.13,30],[35,0.06,25],[30,0,25]]""","""const BR_N=19, BR_SHRINK=[[150,0.62,90],[120,0.4,75],[100,0.24,65],[90,0.13,55],[75,0.06,45],[60,0,40]]""")
# emotes only on the ground: in the air (bus, skydiving, a jump) or in a car the wheel doesn't open and nothing is saved for later
rep("""function emoKeyDown(){ if(!playing||isDead()||P.down) { startEmote(settings.emote); return; } emoOpen('key'); }""",
"""const emoAir=()=>P.sky||P.bus||P.kart||!P.onGround;
function emoKeyDown(){ if(playing&&emoAir()){ toast('Land first to emote'); return; } if(!playing||isDead()||P.down) { startEmote(settings.emote); return; } emoOpen('key'); }""")
rep("""    else if(act==='emote'){ if(P.down) startEmote(settings.emote); else emoOpen('touch'); }""","""    else if(act==='emote'){ if(emoAir()) toast('Land first to emote'); else if(P.down) startEmote(settings.emote); else emoOpen('touch'); }""")
rep("""P.emote=null; if(!P.onGround||P.sky||P.bus||P.kart){ P.emoteQ=id; toast('Emote when you land'); return; } startEmote(id); }""","""P.emote=null; if(emoAir()) return; startEmote(id); }""")
rep("""    combatTick(dt); if(P.emoteQ&&P.onGround&&!P.sky&&!P.bus&&!P.kart){ const q=P.emoteQ; P.emoteQ=null; startEmote(q); }""","""    combatTick(dt);""")
rep("""function startEmote(id){
  if(!EMOTES[id]||isDead()||edit||!P.onGround) return;""","""function startEmote(id){
  if(!EMOTES[id]||isDead()||edit||!P.onGround||P.sky||P.bus||P.kart) return;""")

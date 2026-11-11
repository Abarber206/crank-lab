# patch143: the lobby, closer. The camera comes in so you fill the lower two thirds of the screen with the lighthouse
# behind; every tab other than the lobby has its own solid background (and the world isn't drawn behind it); and an
# emote wheel, in the lobby and in a match: up to eight of the emotes you own around a ring.
#   Lobby: the Emote button opens it; pick one and your hero does it on its pad (your party sees it on theirs).
#   Match, computer: hold the Emote key, move the mouse toward one and let go (a quick tap plays your Locker emote).
#   Match, phone: tap the emote button, tap one.
s=s.replace("</style>","""
#menu.lobby:not(.l3d)::before{background:radial-gradient(ellipse 90% 70% at 50% 0%,#18307e 0%,#0c1c55 45%,#060e2c 100%);-webkit-backdrop-filter:none;backdrop-filter:none}
#emoWheel{position:fixed;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;background:rgba(2,8,24,.35);touch-action:none}
#emoWheel[hidden]{display:none}
#emoWheel .ring{position:relative;width:min(78vmin,440px);height:min(78vmin,440px);border-radius:50%;background:radial-gradient(circle,rgba(6,14,40,.2) 0 27%,rgba(6,14,40,.86) 28% 100%);border:2px solid rgba(255,255,255,.28);box-shadow:0 12px 40px rgba(0,0,0,.45)}
#emoWheel .sl{position:absolute;left:50%;top:50%;width:22%;height:22%;transform:translate(-50%,-50%);border:0;border-radius:50%;background:rgba(255,255,255,.06);color:#fff;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0;transition:background .08s,transform .08s}
#emoWheel .sl .emo{width:62%;height:62%}
#emoWheel .sl.on{background:linear-gradient(#ffe866,#ffc61a);transform:translate(-50%,-50%) scale(1.12)}
#emoWheel .sl.on .emo g{stroke:#1a1300}#emoWheel .sl.on .emo circle{fill:#1a1300}
#emoWheel .mid{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:26%;text-align:center;color:#fff;font:900 italic clamp(14px,2.4vmin,20px)/1.1 var(--font-hud);text-transform:uppercase;letter-spacing:.04em;pointer-events:none}
#emoWheel .mid small{display:block;margin-top:4px;font:600 11px/1.2 var(--font-ui,system-ui);font-style:normal;text-transform:none;letter-spacing:0;opacity:.7}
#lobbyEmote{display:flex;align-items:center;gap:6px}
#lobbyEmote svg{width:20px;height:20px}
</style>""",1)
rep("""<div id="invitePop" hidden>""","""<div id="emoWheel" hidden><div class="ring" id="emoRing"><div class="mid" id="emoMid">Emotes</div></div></div>
<div id="invitePop" hidden>""")
# the lobby camera: in close
rep("base=cam.clone().addScaledVector(dir,7.4);","base=cam.clone().addScaledVector(dir,3.7);")
rep("pads=[[0,0],[-2.5,1.3],[2.5,1.3],[-4.8,2.7]]","pads=[[0,0],[-1.7,1.1],[1.7,1.1],[-3.2,2.2]]")
rep("cam=new THREE.Vector3(cx,Y+2.0,cz), look=new THREE.Vector3(L.x+rx*side*4,Y+6.2,L.z+rz*side*4);","cam=new THREE.Vector3(cx,Y+1.45,cz), look=new THREE.Vector3(L.x+rx*side*4,Y+3.6,L.z+rz*side*4);")
# no world behind a solid tab
rep("""  if(LOBBY.on?!(isTouch&&(++_lobbySkip%2)):""","""  if(LOBBY.on&&!menu.classList.contains('l3d')){ /* a solid tab covers the world */ }
  else if(LOBBY.on?!(isTouch&&(++_lobbySkip%2)):""")
rep("""  if(lob){ $('play').textContent=""","""  if(LOBBY.on&&!menu.classList.contains('l3d')&&EW.open) emoClose();
  if(lob){ $('play').textContent=""")
# lobby heroes can emote
rep("""    const st={bare:true,pos:LOBBY._v.set(pp.x,y+0.09,pp.z),vel:_stZ,yaw,pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:null};""",
"""    const le=lobbyEmoteOf(e,i,dt);
    const st={bare:true,pos:LOBBY._v.set(pp.x,y+0.09,pp.z),vel:_stZ,yaw,pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:le};""")
rep("""    LOBBY.heroes.push({h,plate:sp,i}); }); }""","""    LOBBY.heroes.push({h,plate:sp,i,id:x.id,me:!!x.me}); }); }
// who on the pads is emoting: you (LOBBY.emote), or a party member (their state carries it)
function lobbyEmoteOf(e,i,dt){ let em=null;
  if(e.me) em=LOBBY.emote; else { const pl=e.id&&net.players.get(e.id); if(pl&&pl.lobEmo){ em=pl.lobEmo; } }
  if(!em) return null; em.t+=dt; const E=EMOTES[em.id]; if(!E||em.t>E.dur){ if(e.me) LOBBY.emote=null; else { const pl=net.players.get(e.id); if(pl) pl.lobEmo=null; } return null; }
  if(e.me&&E.beat&&AC){ const b=Math.floor(em.t*E.beat); if(b!==em.beat){ em.beat=b; emoteBeat(em.id,b); } }
  return em; }""")
rep("""function stageLineup(){ // who stands on the stage: you in the middle, party to either side""","""function stageLineup(){ // who stands on the stage: you in the middle, party to either side (with their ids)""")
rep("""list.forEach(x=>{ if(x.id!==net.id) out.push({name:x.name,o:x.o|0,pk:'steel',ready:x.ready,lead:x.lead}); });""","""list.forEach(x=>{ if(x.id!==net.id) out.push({id:x.id,name:x.name,o:x.o|0,pk:'steel',ready:x.ready,lead:x.lead}); });""")
# the lobby emote goes out with your state, and comes in with theirs
rep("""P.emote?EMOTE_IDS.indexOf(P.emote.id)+1:0],k:kartNet(""","""P.emote?EMOTE_IDS.indexOf(P.emote.id)+1:0],le:LOBBY.emote?[EMOTE_IDS.indexOf(LOBBY.emote.id),LOBBY.emote.n|0]:undefined,k:kartNet(""")
rep("""  { const ei=s[12]|0, eid=ei?EMOTE_IDS[ei-1]:null;""","""  { const le=m.le; if(Array.isArray(le)&&EMOTE_IDS[le[0]]){ if(!pl.lobEmo||pl.lobEmoN!==le[1]){ pl.lobEmo={id:EMOTE_IDS[le[0]],t:0,beat:-1}; pl.lobEmoN=le[1]; } } else if(!le){ pl.lobEmoN=-1; } }
  { const ei=s[12]|0, eid=ei?EMOTE_IDS[ei-1]:null;""")
# the wheel
rep("""/* ---------- the 3D lobby: out on the water off the coastal town, looking at the lighthouse ---------- */""",r"""/* ---------- the emote wheel ---------- */
const EW={open:false,sel:-1,ids:[],mx:0,my:0,how:null,t0:0};
function emoOwned(){ const L=window._locker; const ids=EMOTE_LIST.filter(e=>!L||L.owned('e',e)).map(e=>e.id); const fav=settings.emote; ids.sort((a,b)=>(b===fav)-(a===fav)); return ids.slice(0,8); }
function emoBuild(){ const ring=$('emoRing'); ring.querySelectorAll('.sl').forEach(b=>b.remove()); const ids=EW.ids=emoOwned(), n=ids.length;
  ids.forEach((id,k)=>{ const a=-Math.PI/2+k*2*Math.PI/n, b=document.createElement('button'); b.type='button'; b.className='sl'; b.dataset.k=k;
    b.style.left=(50+Math.cos(a)*36)+'%'; b.style.top=(50+Math.sin(a)*36)+'%'; b.innerHTML=emoteIcon(id); b.title=EMOTES[id].name;
    b.addEventListener('pointerenter',()=>emoSel(k)); b.addEventListener('click',e=>{ e.stopPropagation(); emoPick(k); }); ring.appendChild(b); }); emoSel(-1); }
function emoSel(k){ EW.sel=k; $('emoRing').querySelectorAll('.sl').forEach(b=>b.classList.toggle('on',+b.dataset.k===k)); const id=EW.ids[k];
  $('emoMid').innerHTML=id?EMOTES[id].name:'Emotes'+(EW.how==='key'?'<small>move the mouse, let go</small>':EW.how==='lobby'||EW.how==='touch'?'<small>tap one</small>':''); }
function emoOpen(how){ if(EW.open) return; EW.how=how; emoBuild(); if(!EW.ids.length){ toast('No emotes yet'); return; } EW.open=true; EW.mx=EW.my=0; EW.t0=performance.now(); $('emoWheel').hidden=false; if(how!=='key') emoSel(-1); }
function emoClose(){ EW.open=false; $('emoWheel').hidden=true; }
function emoPick(k){ const id=EW.ids[k], how=EW.how; emoClose(); if(!id) return; emoPlay(id,how); }
function emoPlay(id,how){ if(how==='lobby'){ LOBBY.emote={id,t:0,beat:-1,n:((LOBBY.emote&&LOBBY.emote.n)|0)+1}; audioInit(); return; } P.emote=null; startEmote(id); }
$('emoWheel').addEventListener('click',e=>{ if(e.target.id==='emoWheel'||e.target.id==='emoRing') emoClose(); });
// the computer in a match: hold the key, move the mouse toward an emote, let go; a quick tap plays your Locker emote
function emoKeyDown(){ if(!playing||isDead()||P.down||P.sky||P.kart) { startEmote(settings.emote); return; } emoOpen('key'); }
function emoKeyUp(){ if(!EW.open||EW.how!=='key') return; const quick=performance.now()-EW.t0<300&&EW.sel<0; const k=EW.sel; emoClose(); if(quick) startEmote(settings.emote); else if(k>=0) emoPlay(EW.ids[k],'key'); }
addEventListener('mousemove',e=>{ if(!EW.open||EW.how!=='key') return; EW.mx+=e.movementX||0; EW.my+=e.movementY||0; const r=Math.hypot(EW.mx,EW.my); if(r>220){ EW.mx*=220/r; EW.my*=220/r; }
  if(r<36) { if(EW.sel!==-1) emoSel(-1); return; } const n=EW.ids.length, a=Math.atan2(EW.my,EW.mx)+Math.PI/2, k=((Math.round(a/(2*Math.PI/n))%n)+n)%n; if(k!==EW.sel) emoSel(k); },true);

/* ---------- the 3D lobby: out on the water off the coastal town, looking at the lighthouse ---------- */""")
# no looking around while the wheel is open (the mouse is choosing)
rep("""addEventListener('mousemove',e=>{
  if(isTouch||!playing||(!locked&&!lockFailed)) return;""","""addEventListener('mousemove',e=>{
  if(isTouch||!playing||(!locked&&!lockFailed)||EW.open) return;""")
rep("""  else if(a==='emote') startEmote(settings.emote);
  else if(a==='map') toggleMap();""","""  else if(a==='emote') emoKeyDown();
  else if(a==='map') toggleMap();""")
rep("""function releaseAction(a){
  if(a==='interact') useUp();""","""function releaseAction(a){
  if(a==='emote') emoKeyUp();
  if(a==='interact') useUp();""")
rep("""    else if(act==='emote') startEmote(settings.emote);
    else if(act==='use') useDown();""","""    else if(act==='emote'){ if(P.kart||P.sky||P.down) startEmote(settings.emote); else emoOpen('touch'); }
    else if(act==='use') useDown();""")
# the lobby's Emote button, beside Invite friends
rep("""<button class="btn" type="button" id="pdInvite">Invite friends</button>""","""<button class="btn" type="button" id="lobbyEmote"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="2"/><circle cx="9" cy="10" r="1.3" fill="#fff"/><circle cx="15" cy="10" r="1.3" fill="#fff"/><path d="M8 14.5c1.2 1.6 6.8 1.6 8 0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>Emote</button><button class="btn" type="button" id="pdInvite">Invite friends</button>""")
rep("""  $('pdInvite').addEventListener('click',()=>showTab('friends'));""","""  $('pdInvite').addEventListener('click',()=>showTab('friends')); $('lobbyEmote').addEventListener('click',e=>{ e.stopPropagation(); emoOpen('lobby'); });""")
# pausing or leaving the game closes the wheel
rep("""function openMenu(){ if(mapOpen) toggleMap(false);""","""function openMenu(){ if(typeof EW!=='undefined'&&EW.open&&EW.how!=='lobby') emoClose(); if(mapOpen) toggleMap(false);""")
# short screens (a phone on its side): the camera stands back a little, so the hero clears the tab bar; name tags never
# sit on the tabs; the dock buttons stay on one line
rep("camera.position.copy(S.cam); camera.lookAt(S.look); camera.updateMatrixWorld();","camera.position.copy(S.cam); if(S.dir&&innerHeight<560){ camera.position.addScaledVector(S.dir,-1.3); camera.position.y+=0.12; } camera.lookAt(S.look); camera.updateMatrixWorld();")
rep("e.plate.style.top=((1-v.y)/2*h)+'px'; e.plate.hidden=v.z>1; }); }","e.plate.style.top=Math.max(LOBBY.tabB||0,(1-v.y)/2*h)+'px'; e.plate.hidden=v.z>1; }); { const tb=document.querySelector('#menu .mtabs'); LOBBY.tabB=tb?tb.getBoundingClientRect().bottom+30:0; } }")
s=s.replace("#lobbyEmote{display:flex;align-items:center;gap:6px}","#lobbyEmote{display:flex;align-items:center;gap:6px}\n#partyDock .btn{white-space:nowrap}\n@media (max-height:500px){ #partyDock .btn{padding:8px 11px;font-size:13px} #lobbyEmote svg{width:16px;height:16px} }",1)

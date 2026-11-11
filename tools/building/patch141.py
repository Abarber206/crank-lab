# patch141: a real lobby. The lobby is the world itself: out on the water off the coastal town, looking at the
# lighthouse, the beach and the mountains behind, with you (and your party) standing on floating pads. No HUD. Tabs
# across the top (Lobby, Locker, Item Shop, Friends, Profile, Settings, Controls); the mode and a big Play button in the
# bottom right; your party bottom left. The party-code box moved to the Friends tab, your name and team to Profile.
# From the pause menu you can go back to the lobby.
s=s.replace("</style>","""
/* ---------- the 3D lobby ---------- */
body.lobby3d .hud,body.lobby3d #tui,body.lobby3d #vitals{visibility:hidden!important}
#menu.lobby{background:transparent}
#menu.lobby::before{display:none}
#menu.lobby::after{height:30vh;background:linear-gradient(transparent,rgba(2,10,30,.45))}
#menu.lobby:not(.l3d)::before{display:block;content:"";position:fixed;inset:0;background:rgba(4,12,38,.6);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);-webkit-mask:none;mask:none}
#menu.lobby .mhead h1{font-size:clamp(20px,2.4vw,28px)}
#menu.lobby .mtabs{margin:0 auto 10px;background:rgba(6,14,40,.55);border-radius:12px;padding:5px;overflow-x:auto;scrollbar-width:none;max-width:100%}
#menu.lobby .mtabs::-webkit-scrollbar{display:none}
#menu.lobby .mtabs button{font:800 italic 17px/1 var(--font-hud);letter-spacing:.04em;text-transform:uppercase;color:#fff;padding:11px 16px 9px;white-space:nowrap;flex:0 0 auto}
#menu.lobby .mtabs button.on{color:#141000;background:linear-gradient(#fff36b,#ffd21a);box-shadow:0 3px 0 #b98d00}
#menu.lobby.l3d .mtab[data-tab=play]{display:block;min-height:0}
#menu.lobby.l3d .mtab[data-tab=play]>*:not(#lobbyDock):not(#partyDock):not(#lobbyPlates){display:none!important}
#lobbyPlates{position:fixed;inset:0;pointer-events:none;z-index:0}
#lobbyPlates span{position:absolute;transform:translate(-50%,-100%);font:900 italic 15px/1 var(--font-hud);letter-spacing:.06em;text-transform:uppercase;color:#fff;background:rgba(6,14,40,.72);padding:6px 10px 5px;border-radius:6px;white-space:nowrap}
#lobbyPlates span.me{color:#141000;background:#ffd21a}
#lobbyPlates span i{display:block;font:700 11px/1.2 var(--font-ui,system-ui);font-style:normal;letter-spacing:.02em;opacity:.85;text-transform:none;margin-top:2px}
#lobbyDock{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));display:flex;align-items:stretch;gap:10px;z-index:2}
#lobbyDock #play{margin:0;min-width:min(34vw,300px);font:900 italic clamp(30px,4vw,46px)/1 var(--font-hud);letter-spacing:.05em;text-transform:uppercase;padding:18px 26px 16px;color:#141000;background:linear-gradient(#fff685,#ffd61f 55%,#ffc400);border:0;border-radius:10px;box-shadow:0 6px 0 #b98d00,0 10px 26px rgba(0,0,30,.45)}
#lobbyDock #play:active{transform:translateY(4px);box-shadow:0 2px 0 #b98d00}
#modeBtn{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:4px;min-width:150px;padding:10px 16px;border-radius:10px;border:2px solid rgba(255,255,255,.85);background:rgba(6,14,40,.62);color:#fff;cursor:pointer;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
#modeBtn small{font:700 11px/1 var(--font-ui,system-ui);letter-spacing:.14em;opacity:.75}
#modeBtn b{font:900 italic 20px/1 var(--font-hud);letter-spacing:.04em;text-transform:uppercase}
#modePop{position:absolute;right:0;bottom:calc(100% + 10px);width:min(560px,92vw);padding:12px;border-radius:12px;background:rgba(6,14,40,.86);border:1px solid rgba(255,255,255,.18);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
#modePop h3{margin:0 0 8px;color:#fff;font:900 italic 18px/1 var(--font-hud);text-transform:uppercase;letter-spacing:.05em}
#modePop .modes{display:grid;grid-template-columns:1fr 1fr;gap:8px}
#modePop .allyopt{margin-top:8px}
#partyDock{position:fixed;left:max(16px,env(safe-area-inset-left,0px));bottom:max(16px,env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;align-items:flex-start;gap:8px;z-index:2;max-width:42vw}
#partyDock .pdlist{display:flex;flex-direction:column;gap:4px}
#partyDock .pdlist span{color:#fff;background:rgba(6,14,40,.62);padding:6px 10px;border-radius:6px;font:700 14px/1.2 var(--font-ui,system-ui)}
#partyDock .pdlist span em{font-style:normal;opacity:.7;margin-left:6px;font-size:12px}
#partyDock .btn{background:rgba(6,14,40,.62);color:#fff;border:1px solid rgba(255,255,255,.35)}
#menu:not(.lobby) #modeBtn,#menu:not(.lobby) #partyDock,#menu:not(.lobby) #lobbyPlates,#menu:not(.lobby) #modePop{display:none}
#menu:not(.lobby) #lobbyDock{position:static;margin:8px 0}
body.touch #pdFs{display:none}
#menu.lobby .mtab[data-tab=friends],#menu.lobby .mtab[data-tab=profile]{max-width:760px;margin:0 auto}
.mtab[data-tab=profile] .pcard,.mtab[data-tab=friends] .pcard{background:rgba(4,18,64,.55);border:1px solid rgba(255,255,255,.16);border-radius:10px;padding:16px;margin-bottom:12px;color:#fff}
.pcard h2,.pcard h3{margin:0 0 10px;font:900 italic 20px/1 var(--font-hud);text-transform:uppercase;letter-spacing:.05em;color:#fff}
.pcard .acct{font:900 34px/1 var(--font-hud);letter-spacing:.12em;color:#ffd21a}
.pcard .row{display:flex;flex-wrap:wrap;gap:10px;align-items:end}
.pcard p{color:rgba(225,236,255,.82);margin:8px 0 0}
#toLobby{display:none}
#menu:not(.lobby):not(.inparty) #toLobby{display:inline-block}
@media (max-height:500px){ #lobbyDock #play{font-size:30px;padding:12px 18px 10px;min-width:170px} #modeBtn{min-width:120px;padding:6px 12px} #modeBtn b{font-size:16px} #menu.lobby .mtabs button{font-size:14px;padding:8px 11px 7px} #menu.lobby .mtabs{margin-bottom:4px} }
</style>""",1)

# tabs: Lobby, Locker, Item Shop, Friends, Profile, Settings, Controls
rep("""      <button type="button" role="tab" data-tab="play" class="on">Play</button>
      <button type="button" role="tab" data-tab="locker">Locker</button>
      <button type="button" role="tab" data-tab="shop">Item Shop</button>""",
"""      <button type="button" role="tab" data-tab="play" class="on" id="tabPlay">Lobby</button>
      <button type="button" role="tab" data-tab="locker">Locker</button>
      <button type="button" role="tab" data-tab="shop">Item Shop</button>
      <button type="button" role="tab" data-tab="friends">Friends</button>
      <button type="button" role="tab" data-tab="profile">Profile</button>""")
rep("""    <section class="mtab" data-tab="locker" hidden>""","""    <section class="mtab" data-tab="friends" hidden>
      <div class="pcard" id="friendsCard"><h2>Friends</h2><p>Add a friend with the account number on their Profile tab.</p></div>
    </section>
    <section class="mtab" data-tab="profile" hidden>
      <div class="pcard"><h2>Profile</h2><div class="row" id="profName"></div></div>
      <div class="pcard"><h3>Your account number</h3><div class="row"><span class="acct" id="acctNum">—</span><button class="btn" id="acctCopy" type="button">Copy</button></div><p>Friends type this in on their Friends tab to add you.</p></div>
      <div class="pcard"><h3>Team</h3><div class="row" id="profTeam"></div></div>
    </section>
    <section class="mtab" data-tab="locker" hidden>""")
rep("""<button class="btn" id="fs">Fullscreen</button></div>""","""<button class="btn" id="fs">Fullscreen</button><button class="btn" id="toLobby" type="button">Back to lobby</button></div>""")

rep("""/* ---------- lobby stage: your hero (and party) on a lit pad, rendered on its own small canvas while the lobby shows ---------- */""",
r"""/* ---------- the 3D lobby: out on the water off the coastal town, looking at the lighthouse ---------- */
const LOBBY={on:false,spot:null,heroes:[],key:'',pads:[],fixTOD:false,_v:new THREE.Vector3(),_f:new THREE.Vector3()};
function lobbySpot(){ if(LOBBY.spot) return LOBBY.spot; const S=WGEN.sea(), t=TOWNS[0];
  let L=t&&t.poi&&t.poi.shore?t.poi:null, nx=S?S.nx:0, nz=S?S.nz:1, Y=S?S.Y:0;
  if(!L||!S){ const x=SPAWN[0], z=SPAWN[2]; LOBBY.spot={cam:new THREE.Vector3(x+30,terrainH(x+30,z)+3,z),look:new THREE.Vector3(x,terrainH(x,z)+4,z),pads:[],water:false}; return LOBBY.spot; }
  let d=14; while(d<160&&terrainH(L.x+nx*d,L.z+nz*d)>Y-0.4) d+=2; // out past the beach into water
  const side=-0.28, fx=-nx, fz=-nz, rx=-fz, rz=fx; // look back at the shore, a little from one side
  const cx=L.x+nx*(d+15)+rx*side*12, cz=L.z+nz*(d+15)+rz*side*12, cam=new THREE.Vector3(cx,Y+2.0,cz), look=new THREE.Vector3(L.x+rx*side*4,Y+6.2,L.z+rz*side*4);
  const dir=new THREE.Vector3(look.x-cx,0,look.z-cz).normalize(), rgt=new THREE.Vector3(-dir.z,0,dir.x), base=cam.clone().addScaledVector(dir,7.4); base.y=Y;
  const pads=[[0,0],[-2.5,1.3],[2.5,1.3],[-4.8,2.7]].map(([a,b])=>new THREE.Vector3(base.x+rgt.x*a+dir.x*b,Y,base.z+rgt.z*a+dir.z*b));
  LOBBY.spot={cam,look,pads,Y,dir,water:true}; return LOBBY.spot; }
let _padGeo=null, _padMat=null, _ringMat=null;
function lobbyPad(){ if(!_padGeo){ _padGeo=new THREE.CylinderGeometry(1.05,0.9,0.32,40); _padMat=new THREE.MeshPhongMaterial({color:0x1fb6a6,shininess:70,specular:0x3a6a66,emissive:0x0a3a36}); _ringMat=new THREE.MeshBasicMaterial({color:0x9ffff0}); }
  const g=new THREE.Group(), p=new THREE.Mesh(_padGeo,_padMat); p.position.y=-0.08; p.receiveShadow=true; p.castShadow=true; g.add(p);
  const r=new THREE.Mesh(new THREE.TorusGeometry(1.0,0.035,8,64),_ringMat); r.rotation.x=Math.PI/2; r.position.y=0.085; g.add(r); scene.add(g); return g; }
function lobbyActive(){ return !menu.hidden&&menu.classList.contains('lobby'); } // behind every lobby tab (blurred behind the others)
function lobbySync(){ const L=stageLineup(), key=L.map(x=>x.o+'/'+x.pk+'/'+x.name+'/'+(x.ready?1:0)+'/'+(x.lead?1:0)).join('|'); if(key===LOBBY.key) return; LOBBY.key=key;
  LOBBY.heroes.forEach(e=>scene.remove(e.h.group)); LOBBY.heroes=[]; const pl=$('lobbyPlates'); pl.innerHTML='';
  L.forEach((x,i)=>{ const h=heroFor(OUTFITS[x.o]||OUTFITS[0],x.pk); h.group.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } }); scene.add(h.group);
    const sp=document.createElement('span'); sp.className=x.me?'me':''; sp.textContent=x.name; if(!x.me) sp.insertAdjacentHTML('beforeend','<i>'+(x.lead?'Leader':x.ready?'Ready':'Not ready')+'</i>'); pl.appendChild(sp);
    LOBBY.heroes.push({h,plate:sp,i}); }); }
function lobbyView(dt){ const on=lobbyActive(); document.body.classList.toggle('lobby3d',on); menu.classList.toggle('l3d',on&&!document.querySelector('.mtab[data-tab=play]').hidden);
  if(!on){ if(LOBBY.on){ LOBBY.on=false; LOBBY.heroes.forEach(e=>e.h.group.visible=false); LOBBY.pads.forEach(p=>p.visible=false); hero.visible=true; if(LOBBY.fixTOD){ TOD.fix=null; LOBBY.fixTOD=false; } camera.near=0.08; applyFov(); } return; }
  const S=lobbySpot(); LOBBY.on=true; lobbySync(); if(TOD.fix==null){ TOD.fix=0.2; LOBBY.fixTOD=true; } // a bright morning
  camera.position.copy(S.cam); camera.lookAt(S.look); camera.updateMatrixWorld(); { const fv=camera.aspect<1?62:46; if(camera.near!==0.08||Math.abs(camera.fov-fv)>0.01){ camera.near=0.08; camera.fov=fv; camera.updateProjectionMatrix(); } }
  hero.visible=false; skyDome.position.copy(camera.position);
  // the shadow boxes follow the pads, not you
  { const foc=S.pads[0]||S.look, st=(sc.right-sc.left)/sun.shadow.mapSize.x, a=Math.round(foc.dot(_lX)/st)*st, b=Math.round(foc.dot(_lY)/st)*st, c=foc.dot(SUN_DIR);
    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,c); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); placeFarShadow(foc); }
  const t=performance.now()*0.001, n=LOBBY.heroes.length, w=innerWidth, h=innerHeight;
  while(LOBBY.pads.length<n) LOBBY.pads.push(lobbyPad());
  LOBBY.pads.forEach((p,i)=>{ p.visible=i<n; });
  LOBBY.heroes.forEach((e,i)=>{ const pp=S.pads[i]||S.pads[0]||S.look, bob=S.water?Math.sin(t*1.3+i*1.7)*0.05:0, y=(S.water?S.Y+0.2:pp.y)+bob, pad=LOBBY.pads[i];
    pad.position.set(pp.x,y-0.0,pp.z); pad.rotation.z=Math.sin(t*1.1+i)*0.025; pad.rotation.x=Math.cos(t*0.9+i)*0.025;
    e.h.group.visible=true; const yaw=Math.atan2(S.cam.x-pp.x,S.cam.z-pp.z)+Math.PI+(i===0?0:i===1?0.25:-0.25);
    const st={bare:true,pos:LOBBY._v.set(pp.x,y+0.09,pp.z),vel:_stZ,yaw,pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:null};
    animateRig(e.h,st,dt); e.h.group.updateMatrixWorld(true);
    const v=LOBBY._f.set(pp.x,y+2.3,pp.z).project(camera); e.plate.style.left=((v.x+1)/2*w)+'px'; e.plate.style.top=((1-v.y)/2*h)+'px'; e.plate.hidden=v.z>1; }); }
// the dock in the bottom right (the mode, Play), your party bottom left; the party box goes to the Friends tab, name and team to Profile
(function lobbyDom(){ const sec=document.querySelector('.mtab[data-tab=play]');
  const plates=document.createElement('div'); plates.id='lobbyPlates'; sec.appendChild(plates);
  const dock=document.createElement('div'); dock.id='lobbyDock'; dock.innerHTML='<div id="modePop" hidden><h3>Mode</h3></div><button type="button" id="modeBtn"><small>MODE</small><b id="modeName">Build fight</b></button>'; sec.appendChild(dock);
  const pop=$('modePop'); pop.appendChild($('modeCards')); pop.appendChild($('allyOpt')); dock.appendChild($('play'));
  $('modeBtn').addEventListener('click',e=>{ e.stopPropagation(); pop.hidden=!pop.hidden; });
  document.addEventListener('click',e=>{ if(!pop.hidden&&!pop.contains(e.target)&&e.target!==$('modeBtn')) pop.hidden=true; });
  $('modeCards').addEventListener('click',()=>setTimeout(()=>{ pop.hidden=true; lobbyLabels(); },0));
  const pd=document.createElement('div'); pd.id='partyDock'; pd.innerHTML='<div class="pdlist" id="pdList"></div><div class="row" style="display:flex;gap:8px"><button class="btn" type="button" id="pdInvite">Invite friends</button><button class="btn" type="button" id="pdLeave" hidden>Leave party</button><button class="btn" type="button" id="pdFs">Fullscreen</button></div>'; sec.appendChild(pd);
  $('pdInvite').addEventListener('click',()=>showTab('friends')); $('pdLeave').addEventListener('click',()=>leaveGame());
  // the party box (codes, the member list) lives on the Friends tab now
  document.querySelector('.mtab[data-tab=friends]').appendChild($('partyBox'));
  $('profName').appendChild($('pname').closest('label')); $('profTeam').appendChild($('teamSel').closest('label'));
  $('toLobby').addEventListener('click',()=>{ if(net.role) return; if(horde.on) hordeStop(); P.everPlayed=false; respawn(); syncLobby(); showTab('play'); lobbyLabels(); });
  $('pdFs').addEventListener('click',()=>$('fs').click());
  setInterval(lobbyLabels,500); })();
function lobbyLabels(){ const lob=menu.classList.contains('lobby'), m=net.role==='client'?(party.mode||settings.mode):settings.mode; $('modeName').textContent=m==='horde'?'Zombie horde':'Build fight';
  $('tabPlay').textContent=lob?'Lobby':'Game';
  if(lob){ $('play').textContent=net.role&&!party.live?(net.role==='host'?'Play':(party.readyMe?'Ready ✓':'Ready')):'Play'; }
  const L=stageLineup(); $('pdList').innerHTML=''; if(net.role) L.forEach(x=>{ const s=document.createElement('span'); s.textContent=x.name+(x.me?' (you)':''); if(!x.me) s.insertAdjacentHTML('beforeend','<em>'+(x.lead?'Leader':x.ready?'Ready':'Not ready')+'</em>'); $('pdList').appendChild(s); });
  $('pdLeave').hidden=!net.role; }

/* ---------- lobby stage: your hero (and party) on a lit pad, rendered on its own small canvas while the lobby shows ---------- */""")
# the loop: the lobby camera after the game camera; in the lobby the world is drawn every frame (every other on phones)
rep("""  fitView(); updateCamera(); stepTerrain(camera.position.x,camera.position.z); animateHero(dt); updateGhost(); updateHUD();
  if(!(menu.classList.contains('lobby')&&!menu.hidden&&(++_lobbySkip%4))){ renderClouds(); renderReflection(); renderMain(); }""",
"""  fitView(); updateCamera(); lobbyView(dt); stepTerrain(camera.position.x,camera.position.z); animateHero(dt); if(LOBBY.on) hero.visible=false; updateGhost(); updateHUD();
  if(LOBBY.on?!(isTouch&&(++_lobbySkip%2)):!(menu.classList.contains('lobby')&&!menu.hidden&&(++_lobbySkip%4))){ renderClouds(); renderReflection(); renderMain(); }""")
# the old pad stage is for the Locker and Shop only now
rep("""function stageVisible(){ const st=$('stage'); return !menu.hidden&&menu.classList.contains('lobby')&&!!st&&!st.parentNode.hidden; }""",
    """function stageVisible(){ const st=$('stage'); return !menu.hidden&&menu.classList.contains('lobby')&&!!st&&!st.parentNode.hidden&&st.parentNode.dataset.tab!=='play'; }""")

# Play in a party lobby: the leader starts the match, everyone else readies up
rep("""function startPlay(){
  audioInit();""","""function startPlay(){
  audioInit();
  if(menu.classList.contains('lobby')&&net.role&&!party.live){ if(net.role==='host') startMatch(); else $('readyBtn').click(); setTimeout(lobbyLabels,50); return; }""")

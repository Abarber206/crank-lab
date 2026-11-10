# ---------- 58. the lobby: a Fortnite-style front end. Blue stage with your hero (and your party) standing on a lit pad,
# big tabs across the top, a yellow PLAY button, and an Item Shop beside the Locker. Pausing mid-match keeps the compact panel. ----------
rep('<button type="button" role="tab" data-tab="locker">Locker</button>','<button type="button" role="tab" data-tab="locker">Locker</button>\n      <button type="button" role="tab" data-tab="shop">Item Shop</button>')
rep('<section class="mtab" data-tab="play">\n','<section class="mtab" data-tab="play">\n      <div class="stage" id="stage" aria-hidden="true"><canvas id="stageC"></canvas><div class="plates" id="plates"></div><p class="stagehint">Drag to spin</p></div>\n')
rep('<section class="mtab" data-tab="settings" hidden>','''<section class="mtab" data-tab="shop" hidden>
      <div class="shophead"><h2>Item Shop</h2><p>Earn points in <b>Zombie horde</b> and spend them here. Bought items go straight to your Locker.</p></div>
      <div id="shopGrid" class="shopgrid"></div>
    </section>
    <section class="mtab" data-tab="settings" hidden>''')
rep('#menu *{touch-action:pan-y}',r'''#menu *{touch-action:pan-y}
.stage{display:none}
#menu.lobby{background:radial-gradient(ellipse 70% 80% at 36% 58%,#4d9bff 0%,#2462e8 30%,#1238b0 58%,#081d63 100%);padding:0}
#menu.lobby::before{content:"";position:fixed;inset:0;pointer-events:none;background:repeating-conic-gradient(from -8deg at 36% 64%,rgba(255,255,255,.055) 0 5deg,transparent 5deg 13deg);-webkit-mask:radial-gradient(ellipse 75% 75% at 36% 60%,#000 20%,transparent 75%);mask:radial-gradient(ellipse 75% 75% at 36% 60%,#000 20%,transparent 75%)}
#menu.lobby::after{content:"";position:fixed;left:0;right:0;bottom:0;height:22vh;pointer-events:none;background:linear-gradient(transparent,rgba(4,14,52,.55))}
#menu.lobby .panel{position:relative;z-index:1;width:100%;max-width:1320px;min-height:100%;background:none;box-shadow:none;border-radius:0;padding:calc(env(safe-area-inset-top,0px) + 14px) max(18px,env(safe-area-inset-right,0px)) calc(env(safe-area-inset-bottom,0px) + 18px) max(18px,env(safe-area-inset-left,0px));grid-template-rows:auto auto 1fr;grid-template-columns:minmax(0,1fr);align-content:start}
#menu.lobby .mhead{position:relative}
#menu.lobby .panel h1{color:#fff;font-size:clamp(26px,3.4vw,38px);text-shadow:0 3px 0 #0a2a8a,0 0 24px rgba(120,190,255,.55)}
#menu.lobby .wallet{background:rgba(5,20,70,.55);border-color:rgba(255,225,77,.55);backdrop-filter:blur(6px)}
#menu.lobby .mtabs{border-bottom:0;gap:2px;background:rgba(4,18,64,.42);border-radius:8px;padding:4px;width:max-content;max-width:100%;min-width:0;box-sizing:border-box;backdrop-filter:blur(6px)}
#menu.lobby .mtabs button{color:rgba(255,255,255,.72);font-size:18px;padding:11px 18px 9px;border-radius:6px;border-bottom:0}
#menu.lobby .mtabs button.on{color:#0b1640;background:linear-gradient(#fff,#dfe9ff);box-shadow:0 2px 0 #ffe14d inset,0 -3px 0 #ffe14d inset}
#menu.lobby .mtabs button:hover:not(.on){color:#fff;background:rgba(255,255,255,.1)}
#menu.lobby .mtab[data-tab=play]{grid-template-columns:minmax(0,1.25fr) minmax(300px,420px);align-items:start;column-gap:28px}
#menu.lobby .mtab[data-tab=play]>*{grid-column:2}
#menu.lobby .mtab[data-tab=play]>.stage{display:block;grid-column:1;grid-row:1 / span 30;position:relative;height:min(74vh,700px);min-height:340px}
#menu.lobby .stage canvas{position:absolute;inset:0;width:100%;height:100%;cursor:grab;touch-action:none}
#menu.lobby .stage canvas:active{cursor:grabbing}
.plates{position:absolute;inset:0;pointer-events:none}
.plates span{position:absolute;transform:translate(-50%,-100%);white-space:nowrap;font:800 italic 15px/1 var(--font-hud);letter-spacing:.06em;text-transform:uppercase;color:#fff;background:rgba(5,18,64,.7);border:1px solid rgba(255,255,255,.25);border-radius:4px;padding:5px 9px 4px}
.plates span.me{background:#ffe14d;color:#15123a;border-color:#fff3a8}
.plates span i{font-style:normal;color:#9ff59a;margin-left:6px}
.stagehint{position:absolute;left:50%;bottom:-4px;transform:translateX(-50%);margin:0;font:700 12px/1 var(--font-hud);letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.5)}
#menu.lobby .sub{color:rgba(225,236,255,.78)}
#menu.lobby .mtab[data-tab=play]>.sub:not(#verTag){display:none}
#menu.lobby .mode,#menu.lobby .mp,#menu.lobby .set,#menu.lobby .locker,#menu.lobby .bindlist,#menu.lobby .shophead{background:rgba(4,18,64,.5);border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(8px)}
#menu.lobby .mp{border-radius:10px;padding:14px}
#menu.lobby .locker{border-radius:10px;padding:14px}
#menu.lobby .mode.on{background:rgba(30,80,200,.62);border-color:#ffe14d;box-shadow:0 0 0 1px #ffe14d inset,0 8px 24px rgba(0,0,0,.25)}
#menu.lobby .mode[data-mode=horde].on{border-color:#ff7a5a;box-shadow:0 0 0 1px #ff7a5a inset,0 8px 24px rgba(0,0,0,.25)}
#menu.lobby .modes{grid-template-columns:1fr 1fr}
#menu.lobby .actions{display:grid;grid-template-columns:1fr auto;gap:8px}
#menu.lobby #play{grid-column:1 / -1;font:900 italic clamp(30px,3.2vw,42px)/1 var(--font-hud);letter-spacing:.05em;text-transform:uppercase;padding:18px 20px 16px;color:#1a1300;background:linear-gradient(#fff685,#ffd61f 55%,#ffc400);border-radius:9px;box-shadow:0 6px 0 #b98d00,0 14px 34px rgba(0,0,30,.45);transition:transform .08s,box-shadow .08s}
#menu.lobby #play:hover{transform:translateY(-1px);filter:brightness(1.04)}
#menu.lobby #play:active{transform:translateY(4px);box-shadow:0 2px 0 #b98d00,0 8px 20px rgba(0,0,30,.4)}
#menu.lobby #respawn,#menu.lobby #clear{display:none}
#menu.lobby .btn:not(.primary){background:rgba(255,255,255,.14);color:#fff}
#menu.lobby .btn:not(.primary):hover{background:rgba(255,255,255,.22)}
.shophead{border-radius:10px;padding:14px 16px} .shophead h2{margin:0 0 4px} .shophead p{margin:0;color:var(--muted);font-size:14px}
#menu.lobby .shophead p{color:rgba(225,236,255,.8)}
.shopgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.shopgrid .ofit{aspect-ratio:3/4;border-radius:8px}
.shopgrid .ofit.tool{aspect-ratio:3/4}
.shopgrid .ofit img{object-fit:contain}
.shopgrid .ofit span{font-size:16px;padding:22px 6px 8px}
.shopgrid .cost{position:absolute;top:8px;right:8px;display:flex;align-items:center;gap:4px;font:800 italic 15px/1 var(--font-hud);color:#ffe08a;background:rgba(5,14,40,.78);border-radius:999px;padding:4px 9px 4px 5px}
.shopgrid .cost::before{content:"";width:14px;height:14px;border-radius:50%;background:#ffcf4a;box-shadow:inset 0 0 0 2px #b07a16}
.shopgrid .own{position:absolute;top:8px;left:8px;font:800 12px/1 var(--font-hud);letter-spacing:.12em;text-transform:uppercase;color:#0f2a0f;background:#9ff59a;border-radius:4px;padding:4px 7px}
.shopgrid .kind{display:block;font:700 10px/1.2 var(--font-hud);letter-spacing:.12em;opacity:.75;font-style:normal}
.shopgrid .ofit.afford{border-color:rgba(255,225,77,.7)}
.shopgrid .empty{grid-column:1 / -1;color:var(--muted)}
#menu.lobby .shopgrid .empty{color:rgba(225,236,255,.8)}
@media (max-width:820px){
  #menu.lobby .mtab[data-tab=play]{grid-template-columns:minmax(0,1fr)}
  #menu.lobby .mtab[data-tab=play]>*{grid-column:1}
  #menu.lobby .mtab[data-tab=play]>.stage{grid-row:auto;height:44vh;min-height:250px}
  #menu.lobby .mtabs button{font-size:15px;padding:9px 12px 8px}
}
@media (max-height:500px) and (orientation:landscape){
  #menu.lobby .mtab[data-tab=play]{grid-template-columns:minmax(0,1fr) minmax(260px,46%)}
  #menu.lobby .mtab[data-tab=play]>*{grid-column:2}
  #menu.lobby .mtab[data-tab=play]>.stage{grid-column:1;grid-row:1 / span 30;height:calc(100vh - 90px);min-height:200px}
  #menu.lobby #play{font-size:28px;padding:12px}
}''')
# the locker shares its buy flow with the shop
rep("  pick(OUTFITS[outfitIdx(settings.outfit)].id); renderShop();","  pick(OUTFITS[outfitIdx(settings.outfit)].id); renderShop();\n  window._locker={owned,price,pick,pickPk,offerBuy};")
rep("""    if(offer) offerBuy(offer.k,offer.it); };""","""    if(offer) offerBuy(offer.k,offer.it); if(window.renderItemShop) renderItemShop(); };""")
rep("""function showTab(name){""","""function showTab(name){ const bb=$('buyBox'); if(bb){ if(name==='shop') $('shopGrid').before(bb); else if(name==='locker') document.querySelector('.locker .shopbar').after(bb); bb.hidden=true; }
  if(name==='shop'&&window.renderItemShop) renderItemShop(); setTimeout(syncLobby,0);""")
rep("function openMenu(){ if(mapOpen) toggleMap(false); menu.hidden=false;","function openMenu(){ if(mapOpen) toggleMap(false); menu.hidden=false; setTimeout(syncLobby,0);")
rep("  $('play').classList.toggle('pulse',party.pendingStart&&!playing);","  $('play').classList.toggle('pulse',party.pendingStart&&!playing); if(typeof syncLobby==='function') setTimeout(syncLobby,0);")
rep("\n/* ---------- controller (standard gamepad mapping) ----------",r"""
/* ---------- lobby stage: your hero (and party) on a lit pad, rendered on its own small canvas while the lobby shows ---------- */
var _stage=null;
function inLobby(){ return !P.everPlayed||(!!net.role&&!party.live); }
function syncLobby(){ const lob=inLobby(); menu.classList.toggle('lobby',lob); if(lob&&!menu.hidden) stageStart(); }
function stageVisible(){ return !menu.hidden&&menu.classList.contains('lobby')&&!document.querySelector('.mtab[data-tab=play]').hidden; }
function stageInit(){ const c=$('stageC'), r=new THREE.WebGLRenderer({canvas:c,antialias:true,alpha:true}); r.setClearColor(0,0); r.setPixelRatio(Math.min(devicePixelRatio,2));
  r.shadowMap.enabled=true; r.shadowMap.type=THREE.PCFSoftShadowMap;
  const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x2a3a7a,0.75));
  const key=new THREE.DirectionalLight(0xfff4e2,0.95); key.position.set(2.5,5,-4.5); key.castShadow=true; key.shadow.mapSize.set(1024,1024); Object.assign(key.shadow.camera,{left:-5,right:5,top:4,bottom:-1,near:0.5,far:14}); key.shadow.bias=-0.0008; sc.add(key);
  const rim=new THREE.DirectionalLight(0x7fc0ff,0.9); rim.position.set(-3,2.5,4); sc.add(rim); const fill=new THREE.PointLight(0x6aa8ff,0.5,9); fill.position.set(0,0.5,-2.5); sc.add(fill);
  // the pad: a dark glossy disc, a glowing edge, a soft pool of light underneath
  const padM=new THREE.MeshPhongMaterial({color:0x10225e,shininess:40,specular:0x2a3c90}), pad=new THREE.Mesh(new THREE.CylinderGeometry(1.15,1.25,0.14,64),padM); pad.position.y=-0.07; pad.receiveShadow=true; sc.add(pad);
  const ring=new THREE.Mesh(new THREE.TorusGeometry(1.2,0.022,8,96),new THREE.MeshBasicMaterial({color:0x9fd4ff})); ring.rotation.x=Math.PI/2; ring.position.y=0.002; sc.add(ring);
  const gc=document.createElement('canvas'); gc.width=gc.height=128; const gg=gc.getContext('2d'), grd=gg.createRadialGradient(64,64,0,64,64,64); grd.addColorStop(0,'rgba(140,200,255,.5)'); grd.addColorStop(0.7,'rgba(140,200,255,.12)'); grd.addColorStop(1,'rgba(140,200,255,0)'); gg.fillStyle=grd; gg.fillRect(0,0,128,128);
  const glow=new THREE.Mesh(new THREE.PlaneGeometry(3.8,3.8),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(gc),transparent:true,depthWrite:false})); glow.rotation.x=-Math.PI/2; glow.position.y=-0.13; 
  const cam=new THREE.PerspectiveCamera(30,1,0.1,60);
  _stage={r,sc,cam,ring,pad,extra:[],heroes:[],key:'',spin:0,spinV:0,drag:null,on:false,last:0,w:0,h:0};
  c.addEventListener('pointerdown',e=>{ _stage.drag={x:e.clientX}; c.setPointerCapture(e.pointerId); });
  c.addEventListener('pointermove',e=>{ if(!_stage.drag) return; const dx=e.clientX-_stage.drag.x; _stage.drag.x=e.clientX; _stage.spin+=dx*0.012; _stage.spinV=dx*0.012*60; });
  const up=()=>{ _stage.drag=null; }; c.addEventListener('pointerup',up); c.addEventListener('pointercancel',up); }
function stageLineup(){ // who stands on the stage: you in the middle, party to either side
  const me={me:true,name:(net.role?net.name:($('pname').value.trim()||net.name))||'Player',o:outfitIdx(settings.outfit),pk:settings.pickaxe,ready:true};
  const out=[me]; if(net.role){ const list=net.role==='host'?partyMembers():party.list; list.forEach(x=>{ if(x.id!==net.id) out.push({name:x.name,o:x.o|0,pk:'steel',ready:x.ready,lead:x.lead}); }); }
  return out.slice(0,4); }
function stageSync(){ const S=_stage, L=stageLineup(), key=L.map(x=>x.o+'/'+x.pk+'/'+x.name+'/'+(x.ready?1:0)).join('|');
  if(key===S.key) return; S.key=key;
  S.heroes.forEach(h=>S.sc.remove(h.h.group)); S.heroes=[]; S.extra.forEach(m=>S.sc.remove(m)); S.extra=[]; const plates=$('plates'); plates.innerHTML='';
  const spots=[[0,0],[-1.95,0.7],[1.95,0.7],[-3.7,1.5]];
  L.forEach((x,i)=>{ const h=heroFor(OUTFITS[x.o]||OUTFITS[0],x.pk); h.group.traverse(o=>{ if(o.isMesh){ o.castShadow=true; o.receiveShadow=true; } }); S.sc.add(h.group);
    const pl=document.createElement('span'); pl.className=x.me?'me':''; pl.textContent=x.name; if(!x.me&&x.ready) pl.insertAdjacentHTML('beforeend','<i>'+(x.lead?'Leader':'Ready')+'</i>'); plates.appendChild(pl);
    const [sx,sz]=spots[i]; if(i){ const p2=S.pad.clone(), r2=S.ring.clone(); r2.material=S.ring.material; [p2,r2].forEach(m=>{ m.position.x=sx; m.position.z=sz; m.scale.setScalar(0.62); S.sc.add(m); S.extra.push(m); }); p2.scale.y=1; } S.heroes.push({h,pos:new THREE.Vector3(sx,0,sz),yaw:i?(sx<0?0.35:-0.35):0.3,plate:pl,ph:Math.random()*6}); });
  S.ring.scale.setScalar(L.length>1?1:1); }
const _stZ=new THREE.Vector3(), _stH=new THREE.Vector3();
function stageFrame(now){ const S=_stage; if(!S||!S.on) return; if(!stageVisible()){ S.on=false; return; } requestAnimationFrame(stageFrame);
  const dt=Math.min(0.05,S.last?(now-S.last)/1000:1/60); S.last=now; stageSync();
  const c=S.r.domElement, w=c.clientWidth|0, h=c.clientHeight|0; if(!w||!h) return;
  if(w!==S.w||h!==S.h){ S.w=w; S.h=h; S.r.setSize(w,h,false); S.cam.aspect=w/h; S.cam.updateProjectionMatrix(); }
  const n=S.heroes.length, wide=n>1?Math.min(1,0.55+n*0.15):0; // pull the camera back a little for a party
  S.cam.position.set(0.2,1.2+wide*0.3,-5.1-wide*3.6); S.cam.lookAt(0,0.78,wide*0.5);
  if(!S.drag){ S.spinV*=Math.exp(-3*dt); S.spin+=S.spinV*dt*0.2; S.spin*=Math.exp(-0.9*dt); }
  S.heroes.forEach((e,i)=>{ const st={pos:e.pos,vel:_stZ,yaw:e.yaw+(i===0?S.spin:0),pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:null};
    animateRig(e.h,st,dt); e.h.rig.pick.visible=false;
    e.h.group.updateMatrixWorld(true); _stH.copy(e.pos); _stH.y+=2.15; _stH.project(S.cam);
    e.plate.style.left=((_stH.x+1)/2*w)+'px'; e.plate.style.top=Math.max(34,(1-_stH.y)/2*h)+'px'; e.plate.hidden=_stH.z>1; });
  S.ring.material.color.setHSL(0.58,1,0.72+0.08*Math.sin(now*0.002));
  S.r.render(S.sc,S.cam); }
function stageStart(){ try{ if(!_stage) stageInit(); }catch(e){ return; } if(_stage.on) return; if(!stageVisible()) return; _stage.on=true; _stage.last=0; requestAnimationFrame(stageFrame); }
/* ---------- item shop: everything that costs points, as big cards; owned ones say so and equip on a tap ---------- */
function renderItemShop(){ const g=$('shopGrid'), L=window._locker; if(!g||!L) return; g.innerHTML='';
  const items=[...OUTFITS.filter(o=>o.shop).map(it=>['o',it]),...PICKAXES.filter(p=>p.shop).map(it=>['p',it])];
  const R=['legendary','epic','rare','uncommon','common']; items.sort((a,b)=>R.indexOf(a[1].rarity)-R.indexOf(b[1].rarity)||(a[0]<b[0]?-1:1));
  if(!items.length){ g.innerHTML='<p class="empty">Nothing in the shop right now.</p>'; return; }
  items.forEach(([k,it])=>{ const own=L.owned(k,it), c=L.price(k,it), b=document.createElement('button'); b.type='button'; b.className='ofit '+it.rarity+(k==='p'?' tool':'')+(!own&&wallet.pts>=c?' afford':'');
    const src=document.querySelector(`#${k==='o'?'outfits':'picks'} [data-id="${it.id}"] img`);
    b.innerHTML=(src?`<img alt="" src="${src.src}">`:'')+(own?'<b class="own">Owned</b>':`<b class="cost">${c.toLocaleString()}</b>`)+`<span></span>`;
    const sp=b.querySelector('span'); sp.textContent=it.name; sp.insertAdjacentHTML('beforeend',`<small class="kind">${RNAME[it.rarity]} ${k==='o'?'outfit':'pickaxe'}</small>`);
    b.addEventListener('click',()=>{ if(own){ if(k==='o') L.pick(it.id); else L.pickPk(it.id); toast('Equipped '+it.name); renderItemShop(); } else L.offerBuy(k,it); });
    g.appendChild(b); }); }
window.renderItemShop=renderItemShop;
setTimeout(()=>{ syncLobby(); renderItemShop(); },80); setTimeout(renderItemShop,2500);

/* ---------- controller (standard gamepad mapping) ----------""")
# in the lobby the world behind the opaque backdrop only needs an occasional frame
rep("  renderClouds(); renderer.render(scene,camera);","  if(!(menu.classList.contains('lobby')&&!menu.hidden&&(++_lobbySkip%4))){ renderClouds(); renderer.render(scene,camera); }")
rep("const menu=$('menu');","const menu=$('menu'); let _lobbySkip=0;")
rep('Update: Nov 8 · dune buggies &amp; garages, smoother roads, skydive &amp; glider, scope zoom','Update: Nov 9 · new lobby &amp; Item Shop, realistic gun sounds, glass windows, buggy fixes')

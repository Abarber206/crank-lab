# patch196: match feel in battle royale
#  - the feed says what each elimination was made with and from how far
#  - when you're out, a summary (place, eliminations, damage, time survived, materials gathered) with Spectate and
#    Return to lobby; spectating follows whoever got you (then whoever's left), Space or click for the next player
#  - winning shows VICTORY ROYALE over the same summary
#  - inside the storm the world goes purple and murky, with lightning
rep("""#stormFx{""","""#brEnd{position:fixed;inset:0;z-index:40;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at center,rgba(10,16,40,.55),rgba(4,8,22,.86));font-family:var(--font-hud);color:#fff;text-align:center}
#brEnd .bx{min-width:min(440px,92vw);padding:26px 30px;border-radius:16px;background:rgba(14,22,52,.82);box-shadow:0 18px 60px rgba(0,0,0,.5)}
#brEnd .pl{font:900 italic 64px/1 var(--font-hud);letter-spacing:.02em;color:#ffe08a;text-shadow:0 4px 0 rgba(0,0,0,.35)} #brEnd .vr{font:900 italic 44px/1.05 var(--font-hud);color:#ffd23a;text-shadow:0 0 24px rgba(255,190,40,.6),0 4px 0 rgba(0,0,0,.4);margin-bottom:6px}
#brEnd .by{margin:8px 0 18px;color:#c9d6f5;font-size:15px} #brEnd .gr{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:20px} #brEnd .gr div{background:rgba(255,255,255,.07);border-radius:10px;padding:10px 6px}
#brEnd .gr b{display:block;font:900 26px/1.1 var(--font-hud);color:#fff} #brEnd .gr span{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#9fb0d8}
#brEnd .bt{display:flex;gap:10px;justify-content:center} #brEnd button{font:800 15px var(--font-hud);text-transform:uppercase;letter-spacing:.05em;border:0;border-radius:10px;padding:12px 20px;cursor:pointer;background:#3d7bf2;color:#fff} #brEnd button.alt{background:rgba(255,255,255,.14)}
#specTag{position:fixed;left:50%;bottom:118px;transform:translateX(-50%);z-index:12;background:rgba(6,14,40,.78);color:#fff;border-radius:10px;padding:9px 14px;font:800 14px var(--font-hud);text-transform:uppercase;letter-spacing:.04em;display:flex;gap:12px;align-items:center}
#specTag button{font:800 12px var(--font-hud);text-transform:uppercase;border:0;border-radius:8px;padding:7px 10px;background:rgba(255,255,255,.16);color:#fff;cursor:pointer}
#stormFlash{position:fixed;inset:0;pointer-events:none;z-index:3;background:rgba(235,225,255,.0);transition:background .08s}
#stormFx{""")
rep("""<div id="stormFx" hidden></div>""","""<div id="stormFx" hidden></div><div id="stormFlash"></div><div id="brEnd" hidden><div class="bx"><div class="vr" id="brEndV" hidden>Victory Royale</div><div class="pl" id="brEndP">#1</div><div class="by" id="brEndBy"></div>
<div class="gr"><div><b id="brEndK">0</b><span>Eliminations</span></div><div><b id="brEndD">0</b><span>Damage dealt</span></div><div><b id="brEndT">0:00</b><span>Time survived</span></div><div><b id="brEndM">0</b><span>Materials gathered</span></div></div>
<div class="bt"><button id="brEndS">Spectate</button><button id="brEndL" class="alt">Return to lobby</button></div></div></div><div id="specTag" hidden><span id="specName"></span><button id="specNext">Next</button><button id="specLeave">Lobby</button></div>""")
# stats
rep("""  BR.on=true; BR.claimed=new Set(); BR.out=false;""","""  BR.on=true; BR.claimed=new Set(); BR.matsGot=0; BR.dmg=0; BR.t0=performance.now(); BR.tOut=0; BR.mats0=null; BR.spec=null; BR.leave=false; BR.endUp=false; BR.killer=null; $('brEnd').hidden=true; $('specTag').hidden=true; BR.out=false;""")
rep("""function brHurtBot(b,dmg,from,w){ if(!b.alive) return;""","""function brHurtBot(b,dmg,from,w){ if(!b.alive) return; if(!from) BR.dmg=(BR.dmg||0)+Math.min(dmg,b.hp+b.sh);""")
# the feed: weapon and distance
rep("""  if(!from&&byName==='You'){ BR.kills++; feed('<b>You</b> eliminated <b>'+esc(b.name)+'</b>'); }
  else if(from){ from.kills++; feed('<b>'+esc(from.name)+'</b> eliminated <b>'+esc(b.name)+'</b>'); }""","""  const how=(w,E)=>' <span style="opacity:.75">· '+esc(w&&WEAPONS[w]?WEAPONS[w].name:'Pickaxe')+' · '+Math.round(E.pos.distanceTo(b.pos))+' m</span>';
  if(!from&&byName==='You'){ BR.kills++; feed('<b>You</b> eliminated <b>'+esc(b.name)+'</b>'+how(mode==='gun'?P.wpn:null,P)); }
  else if(from){ from.kills++; feed('<b>'+esc(from.name)+'</b> eliminated <b>'+esc(b.name)+'</b>'+how(from.wpn,from)); }""")
rep("""  if(hurt(P,dmg)) brPlayerOut(b.name); }""","""  if(hurt(P,dmg)){ BR.killer=b; BR.killW=b.wpn; BR.killD=Math.round(b.pos.distanceTo(P.pos)); brPlayerOut(b.name); } }""")
rep("""feed('<b>You</b> were eliminated by <b>'+esc(by)+'</b>',true);""","""feed('<b>You</b> were eliminated by <b>'+esc(by)+'</b>'+(BR.killer&&BR.killer.name===by?' <span style="opacity:.75">· '+esc(BR.killW&&WEAPONS[BR.killW]?WEAPONS[BR.killW].name:'Pickaxe')+' · '+BR.killD+' m</span>':''),true); BR.tOut=performance.now(); setTimeout(()=>brShowEnd(false,by),1600);""")
# match end: no auto exit while you're out (spectate or leave); winning shows the summary too
rep("""    else if(BR.out&&!TL.has(0)&&BR.overT<=0){ BR.over=true; BR.overT=7; } }""","""    else if(BR.out&&!TL.has(0)&&(BR.leave||TL.size<=1)){ BR.over=true; BR.overT=BR.leave?0.05:6; if(!BR.leave){ const w=[...BR.bots].find(b=>b.alive); if(w) feed('<b>'+esc(w.name)+'</b> won the match'); } } }""")
rep("""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); BR.over=true; BR.overT=7; }""","""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),3); sfx('win'); addPoints(150+40*BR.kills); BR.over=true; BR.overT=9; BR.tOut=performance.now(); setTimeout(()=>brShowEnd(true),1500); }""")
rep("""function brStop(){ BR.on=false;""","""function brShowEnd(won,by){ if(!BR.on) return; BR.endUp=true; const T_=Math.max(0,((BR.tOut||performance.now())-(BR.t0||performance.now()))/1000), mm=Math.floor(T_/60)+':'+String(Math.floor(T_%60)).padStart(2,'0');
  $('brEndV').hidden=!won; $('brEndP').textContent='#'+(won?1:BR.place); $('brEndBy').textContent=won?'Last one standing':by?'Eliminated by '+by+(BR.killW&&WEAPONS[BR.killW]?' · '+WEAPONS[BR.killW].name:'')+(BR.killD!=null?' · '+BR.killD+' m':''):'';
  $('brEndK').textContent=BR.kills; $('brEndD').textContent=Math.round(BR.dmg||0); $('brEndT').textContent=mm; $('brEndM').textContent=Math.round(BR.matsGot||0); $('brEndS').hidden=won||!BR.bots.some(b=>b.alive);
  $('brEnd').hidden=false; if(document.pointerLockElement){ invUnlocking=true; try{ document.exitPointerLock(); }catch(e){} } } // (free the mouse for the buttons without pausing)
function brSpecPick(step){ const alive=BR.bots.filter(b=>b.alive); if(!alive.length){ BR.spec=null; return; } let i=BR.spec?alive.indexOf(BR.spec):-1;
  if(i<0&&!step&&BR.killer&&BR.killer.alive){ BR.spec=BR.killer; } else { i=(i+(step||1)+alive.length)%alive.length; BR.spec=alive[i]; } $('specName').textContent='Spectating '+BR.spec.name; }
$('brEndS').onclick=()=>{ $('brEnd').hidden=true; brSpecPick(0); $('specTag').hidden=!BR.spec; };
$('brEndL').onclick=$('specLeave').onclick=()=>{ $('brEnd').hidden=true; $('specTag').hidden=true; BR.leave=true; if(BR.over) BR.overT=0.05; };
$('specNext').onclick=()=>brSpecPick(1);
addEventListener('keydown',e=>{ if(BR.on&&BR.out&&BR.spec&&!$('specTag').hidden&&(e.code==='Space'||e.code==='KeyN')){ brSpecPick(1); e.preventDefault(); } });
// spectating: the camera rides behind whoever you're watching; the storm: purple murk and lightning when you're in it
const _spV=new THREE.Vector3();
function brView(dt){ if(!BR.on) return;
  if(BR.out&&BR.spec&&!$('specTag').hidden){ if(!BR.spec.alive){ brSpecPick(1); if(!BR.spec){ $('specTag').hidden=true; return; } } const b=BR.spec, fx=-Math.sin(b.yaw), fz=-Math.cos(b.yaw);
    _spV.set(b.pos.x-fx*4.2+fz*0.9,b.pos.y+2.4,b.pos.z-fz*4.2-fx*0.9); camera.position.lerp(_spV,Math.min(1,dt*6)); camera.lookAt(b.pos.x+fx*6,b.pos.y+1.4,b.pos.z+fz*6); }
}
function brStormTint(){ if(!BR.on) return; const dt=Math.min(0.1,lastDt||0.016); const S=BR.storm; if(!S||!scene.fog) return; const c=camera.position, inS=!P.bus&&Math.hypot(c.x-S.cx,c.z-S.cz)>S.r;
  BR.stK=(BR.stK||0)+((inS?1:0)-(BR.stK||0))*Math.min(1,dt*1.5); const k=BR.stK;
  if(k>0.01){ const fc=scene.fog.color.clone(), fn=scene.fog.near, bg=scene.background&&scene.background.isColor?scene.background.clone():null; scene.fog.color.lerp(_stCol,k*0.75); scene.fog.near=scene.fog.near+(0.02-scene.fog.near)*k; if(scene.background&&scene.background.isColor) scene.background.lerp(_stCol,k*0.6); const rs_=typeof skyTint==='function'?skyTint(_stZc,_stCol,_stHc,k*0.8,0.8):()=>{};
    BR.ltT=(BR.ltT||2)-dt; if(BR.ltT<=0&&inS){ BR.ltT=2.5+Math.random()*4; const f=$('stormFlash'); f.style.background='rgba(235,225,255,.42)'; setTimeout(()=>{ f.style.background='rgba(235,225,255,0)'; },90); setTimeout(()=>{ f.style.background='rgba(235,225,255,.25)'; setTimeout(()=>f.style.background='rgba(235,225,255,0)',70); },180); setTimeout(()=>{ sfxGain=0.5; sfx('storm_close'); sfxGain=1; },350+Math.random()*700); }
    return ()=>{ rs_(); scene.fog.color.copy(fc); scene.fog.near=fn; if(bg) scene.background.copy(bg); }; } return null; }
const _stCol=new THREE.Color(0x5a2a8a), _stZc=new THREE.Color(0x3a1a66), _stHc=new THREE.Color(0x8a52c0);
function brStop(){ BR.on=false; try{ $('brEnd').hidden=true; $('specTag').hidden=true; }catch(e){}""")
rep("""frPoll(dt); fitView(); updateCamera(); audioListen();""","""frPoll(dt); fitView(); updateCamera(); try{ brView(dt); }catch(e){} audioListen();""")
rep("""function renderMain(){""","""function renderMain(){ let sv_=null; try{ sv_=brStormTint(); }catch(e){} try{ renderMain0(); } finally{ if(sv_) sv_(); } }
function renderMain0(){""")
rep("""function giveMats(mat,n,point){ if(infMats()||n<=0) return;""","""function giveMats(mat,n,point){ if(infMats()||n<=0) return; if(BR.on&&!BR.out) BR.matsGot=(BR.matsGot||0)+n;""")

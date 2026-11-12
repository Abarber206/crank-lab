# patch162: getting in and out of matches.
#  - A loading screen: the island, the mode, a bar filling over 10 seconds with a countdown, tips, and who's coming.
#    Shown before a party match starts (on everyone's screen) and before a Battle royale match.
#  - Party matches still need everyone ready; once they are and the leader starts, everyone loads in together for
#    10 seconds, then the match begins.
#  - Battle royale: when you're eliminated (once your team is out) or you win, you go back to the lobby after a few
#    seconds instead of straight into another match. Press Play for the next one.
rep("""<div id="stormFx" hidden></div>""","""<div id="stormFx" hidden></div>
<div id="loadScr" hidden><canvas id="loadMap"></canvas><div class="lsIn"><p class="lsMode" id="lsMode">Battle royale</p><h2 id="lsTitle">Loading in</h2><p class="lsSub" id="lsSub"></p>
  <div class="lsBar"><i id="lsFill"></i></div><p class="lsCount"><b id="lsNum">10</b></p><ul id="lsWho"></ul><p class="lsTip" id="lsTip"></p></div></div>""")
rep("""#stormFx{position:fixed;""","""#loadScr{position:fixed;inset:0;z-index:70;display:grid;place-items:center;background:radial-gradient(ellipse at 50% 40%,#173a8a 0%,#0a1840 55%,#040a1e 100%);overflow:hidden;color:#fff} #loadScr[hidden]{display:none}
#loadMap{position:absolute;left:50%;top:50%;width:min(120vh,120vw);height:min(120vh,120vw);transform:translate(-50%,-50%) rotate(-8deg);opacity:.32;filter:saturate(1.2) blur(1px);animation:lsDrift 10s linear forwards}
@keyframes lsDrift{from{transform:translate(-50%,-50%) rotate(-8deg) scale(1)}to{transform:translate(-50%,-50%) rotate(-4deg) scale(1.12)}}
.lsIn{position:relative;text-align:center;width:min(640px,90vw);padding:24px} .lsMode{margin:0;font:800 italic 15px/1 var(--font-hud);letter-spacing:.2em;text-transform:uppercase;color:#ffd21a}
.lsIn h2{margin:10px 0 6px;font:800 italic clamp(34px,7vw,64px)/1 var(--font-hud);text-transform:uppercase;letter-spacing:.02em;text-shadow:0 4px 18px rgba(0,0,0,.5)} .lsSub{margin:0 0 22px;color:rgba(225,236,255,.85)}
.lsBar{height:14px;border-radius:999px;background:rgba(255,255,255,.14);overflow:hidden;box-shadow:inset 0 0 0 2px rgba(255,255,255,.12)} .lsBar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#ffd21a,#ff9a3c);border-radius:999px}
.lsCount{margin:14px 0 6px;font:800 italic 40px/1 var(--font-hud)} #lsWho{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px;justify-content:center} #lsWho li{background:rgba(6,14,40,.7);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:6px 12px;font:700 13px var(--font-hud)} #lsWho li b{color:#9ff59a}
.lsTip{margin:20px 0 0;color:rgba(225,236,255,.8);font-size:14px;min-height:2.6em}
#stormFx{position:fixed;""")
rep("""var mapOpen=false, bigMapImg=null;""","""var mapOpen=false, bigMapImg=null;
// the loading screen: title, a bar over secs seconds, then done()
const LS_TIPS=['Crouch and keep still: the bots take longer to notice you.','Bots hear gunfire: every shot tells them where you are.','Watch the dashed circle on the map: that is where the storm closes to next.',
  'Doors open as you walk into them, and bots use them too.','Chests restock after a while; floor loot is in every house.','The storm hurts more every phase. Move early.','Jump from the bus where the dashed line passes nearest to where you want to land.',
  'Build a quick wall between you and a sniper.','Teammates go after whoever is shooting you.','Boats are the fastest way along the rivers.'];
const LOAD={on:false};
function showLoading(mode,sub,secs,who,done){ const el=$('loadScr'); if(!bigMapImg) try{ bigMapImg=renderBigMapImage(); }catch(e){}
  if(bigMapImg){ const c=$('loadMap'); c.width=c.height=Math.min(1024,bigMapImg.width); c.getContext('2d').drawImage(bigMapImg,0,0,c.width,c.height); c.style.animation='none'; void c.offsetWidth; c.style.animation=''; }
  $('lsMode').textContent=mode; $('lsTitle').textContent='Loading in'; $('lsSub').textContent=sub||''; $('lsWho').innerHTML=(who||[]).map(n=>'<li><b>✓</b> '+esc(n)+'</li>').join('');
  let tip=Math.floor(Math.random()*LS_TIPS.length); $('lsTip').textContent=LS_TIPS[tip];
  el.hidden=false; LOAD.on=true; const t0=performance.now(), T=secs*1000; let lastN=-1, tipT=t0;
  const step=now=>{ if(!LOAD.on) return; const k=Math.min(1,(now-t0)/T), n=Math.ceil(secs*(1-k)); $('lsFill').style.width=(k*100).toFixed(1)+'%'; if(n!==lastN){ lastN=n; $('lsNum').textContent=n>0?n:'GO'; if(n<=3&&n>0) sfx('equip'); }
    if(now-tipT>4200){ tipT=now; tip=(tip+1)%LS_TIPS.length; $('lsTip').textContent=LS_TIPS[tip]; }
    if(k<1) requestAnimationFrame(step); else { LOAD.on=false; setTimeout(()=>{ el.hidden=true; },250); if(done) done(); } };
  requestAnimationFrame(step); }
function hideLoading(){ LOAD.on=false; $('loadScr').hidden=true; }""")
# party: everyone loads in together once all are ready
rep("""function startMatch(){
  if(net.role!=='host') return;
  if(!party.live&&!partyAllReady()){ toast('Waiting for everyone to ready up'); return; }""","""function startMatch(){
  if(net.role!=='host') return;
  if(!party.live&&!partyAllReady()){ toast('Waiting for everyone to ready up'); return; }
  if(LOAD.on) return;
  if(!party.live){ const who=partyMembers().map(x=>x.name||'Player'), mn={fight:'Build fight',horde:'Zombie horde',br:'Battle royale'}[settings.mode]||'Match';
    netSend({type:'loading',mode:mn,secs:10,who}); showLoading(mn,'Everyone is ready',10,who,startMatchNow); return; }
  startMatchNow(); }
function startMatchNow(){
  if(net.role!=='host') return;""")
rep("""  else if(m.type==='start') onPartyStart(m);""","""  else if(m.type==='start'){ hideLoading(); onPartyStart(m); }
  else if(m.type==='loading'){ showLoading(m.mode||'Match','The leader started the match',Math.max(1,Math.min(15,+m.secs||10)),Array.isArray(m.who)?m.who.slice(0,8).map(String):[],null); }""")
rep("""function onPartyLobby(){ party.live=false;""","""function onPartyLobby(){ hideLoading(); party.live=false;""")
# Battle royale: load in for 10 seconds first; afterwards back to the lobby
rep("""  if(brMine()&&playing&&!BR.on) brStart();""","""  if(brMine()&&playing&&!BR.on&&!BR.loading){ BR.loading=true; const ts=settings.brTeam||1; showLoading('Battle royale',ts===1?'Solo · 20 players':['','','Duos','Trios','Squads'][ts]+' · '+Math.ceil(20/ts)+' teams',10,[net.name||$('pname').value.trim()||'You'],()=>{ BR.loading=false; if(brMine()&&playing) brStart(); }); }
  if(BR.loading){ P.vel.x=0; P.vel.z=0; fireHeld=false; }""")
rep("""  else { BR.overT-=dt; if(BR.overT<=0){ BR.on=false; brStart(); } }""","""  else { BR.overT-=dt; if(BR.overT<=0){ brStop(); try{ document.exitPointerLock(); }catch(e){} openMenu(); showTab('play'); setTimeout(()=>{ $('play').textContent='Play'; },80); toast('Back in the lobby'); } }""")
rep("""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); BR.over=true; BR.overT=8; } }""","""banner('Victory Royale!','#1 · '+BR.kills+(BR.kills===1?' elimination':' eliminations'),7); sfx('win'); addPoints(150+40*BR.kills); BR.over=true; BR.overT=7; } }""")

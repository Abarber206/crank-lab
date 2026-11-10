# ---------- 22. fewer obvious messages; the horde's wave shows as a bar under the compass that fades in and out ----------
def drop(a,b): rep(a,b)
# obvious feedback the screen already shows
drop("syncMode(); toast(MATERIALS[buildMat].name); }","syncMode(); }")
drop("$('respawn').addEventListener('click',()=>{ respawn(); toast('Respawned'); });","$('respawn').addEventListener('click',()=>{ respawn(); });")
drop("clearBuilds(); netOp({op:'clear'}); toast('Builds cleared'); });","clearBuilds(); netOp({op:'clear'}); });")
drop("saveSettings(); renderBinds(); toast('Binds reset'); });","saveSettings(); renderBinds(); });")
s=s.replace(" banner('Back in','',1); },3000); }"," },3000); }")
drop("  banner(settings.mode==='horde'?'Zombie horde':'Build fight','Match started',2);\n","")
drop("respawn(); banner(m.mode==='horde'?'Zombie horde':'Build fight','The leader started the match',2.5); sfx('win');","respawn(); sfx('win');")
drop("net.dead=false; updateRoomUI(); toast('Party '+code+' created'); });","net.dead=false; updateRoomUI(); });")
drop("$('leaveBtn').addEventListener('click',()=>{ leaveGame(); toast('Left the party'); });","$('leaveBtn').addEventListener('click',()=>{ leaveGame(); });")
drop("if(AMMO_T[item]){ P.res[item]=Math.min(AMMO_T[item].max,(P.res[item]|0)+n); sfx('ammo_pick'); toast('+'+n+' '+AMMO_T[item].name.toLowerCase()+' ammo'); }",
     "if(AMMO_T[item]){ P.res[item]=Math.min(AMMO_T[item].max,(P.res[item]|0)+n); sfx('ammo_pick'); }")
drop("sfx('pickup'); toast('Picked up '+itemInfo(item).name); }","sfx('pickup'); }")
drop("sfx('ammo_pick'); toast('+'+n+' '+AMMO_T[W.ammo].name.toLowerCase()+' ammo'); }","sfx('ammo_pick'); }")
drop("P.inv[i]=item; P.ammo[item]=n; sfx('pickup'); toast('Picked up '+WEAPONS[item].name); } }","P.inv[i]=item; P.ammo[item]=n; sfx('pickup'); } }")
# the horde: the wave bar says it all
drop("  banner('Wave '+horde.wave,horde.toSpawn+' zombies incoming',2.2); sfx('wave');","  sfx('wave');")
drop("  banner('Zombie horde','Build a fort – the first wave comes in 20 s',3); syncBot(); refreshTeamMarkers();","  syncBot(); refreshTeamMarkers();")
drop("      banner('Wave '+horde.wave+' cleared','Next wave in 15 s – patch up your fort',3); sfx('win'); hordeHeal();","      sfx('win'); hordeHeal();")
drop("  if(m.heal){ hordeHeal(); banner('Wave '+horde.wave+' cleared','Next wave in 15 s – patch up your fort',3); sfx('win'); return; }","  if(m.heal){ hordeHeal(); sfx('win'); return; }")
drop("syncBot(); refreshTeamMarkers(); banner('Zombie horde','The host started a horde – build a fort!',3); }","syncBot(); refreshTeamMarkers(); }")
drop("  if(m.w>horde.wave&&m.ph==='wave'){ banner('Wave '+m.w,'Zombies incoming',2.2); sfx('wave'); }","  if(m.w>horde.wave&&m.ph==='wave') sfx('wave');")
drop("function waveBonus(w){ const n=WAVE_PTS(w); addPoints(n); toast('+'+n+' pts for clearing wave '+w);","function waveBonus(w){ const n=WAVE_PTS(w); addPoints(n); WAVEBAR.bonus=n;")
drop("if(m.wave) toast('+'+m.n+' pts for clearing wave '+m.wave); }","if(m.wave) WAVEBAR.bonus=m.n; }")
# the wave bar
drop('    <span class="chip red" id="cWave" hidden><small>WAVE</small><b id="waveN">1</b><small id="waveL"></small></span>\n','')
drop('<div class="hud" id="banner">','<div class="hud" id="waveHud"><div class="wt"><b id="whT"></b><span id="whS"></span></div><div class="wb"><i id="whF"></i></div></div>\n<div class="hud" id="banner">')
drop("#banner{left:50%;top:30%;","""#waveHud{left:50%;top:calc(env(safe-area-inset-top,0px) + 48px);transform:translate(-50%,-6px);width:min(300px,70vw);opacity:0;transition:opacity .7s,transform .7s;display:grid;gap:4px}
#waveHud.on{opacity:1;transform:translate(-50%,0)}
#waveHud .wt{display:flex;justify-content:space-between;align-items:baseline;font:800 italic 17px/1 var(--font-hud);text-transform:uppercase;letter-spacing:.04em;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.85)}
#waveHud .wt span{font-size:14px;color:#e9c8ff}
#waveHud .wb{height:7px;border-radius:4px;background:rgba(14,10,24,.6);box-shadow:0 0 0 1px rgba(233,200,255,.25) inset;overflow:hidden}
#waveHud .wb i{display:block;height:100%;width:100%;transform-origin:left;background:linear-gradient(90deg,#9b4dff,#ff6ad2);transition:transform .35s}
#waveHud.brk .wb i{background:linear-gradient(90deg,#4aa8ff,#9fe0ff)}
#waveHud.urgent .wb i{background:linear-gradient(90deg,#ff8a3c,#ffd04a);animation:whPulse .5s ease-in-out infinite alternate}
#waveHud.urgent .wt span{color:#ffd04a}
@keyframes whPulse{to{opacity:.55}}
body.touch #waveHud{top:calc(env(safe-area-inset-top,0px) + 10px)}
@media (orientation:portrait){#waveHud{top:calc(env(safe-area-inset-top,0px) + 10px)}}
#banner{left:50%;top:30%;""")
a=s.index("function updateHordeHUD(){"); b=s.index("\n\n",a)
s=s[:a]+"""/* The wave bar under the compass: the wave number and how many are left (it drains as you kill), or the build
   countdown between waves (it drains to the next wave). It shows up when something changes (a wave starts, a kill,
   the break begins) and fades away after a few seconds; in the last 5 seconds of a break it stays up and pulses. */
const WAVEBAR={key:'',shown:0,total:0,brk:1,phase:'',wave:-1,bonus:0,txt:''};
function updateHordeHUD(){
  const on=horde.on; $('cKills').hidden=!on; const el=$('waveHud');
  if(!on||horde.phase==='over'||horde.phase==='idle'){ el.classList.remove('on'); WAVEBAR.phase=''; return; }
  $('killN').textContent=horde.kills;
  let alive=0; horde.zs.forEach(z=>{ if(z.alive) alive++; });
  const now=performance.now(); let title, sub, fill, urgent=false, brk=horde.phase==='break';
  if(brk){ if(WAVEBAR.phase!=='break') WAVEBAR.brk=Math.max(1,horde.t); WAVEBAR.brk=Math.max(WAVEBAR.brk,horde.t); const t=Math.max(0,Math.ceil(horde.t));
    title=horde.wave?'Wave '+horde.wave+' cleared':'Build your fort'; if(horde.wave&&WAVEBAR.bonus) title+=' · +'+WAVEBAR.bonus+' pts';
    sub='Wave '+(horde.wave+1)+' in '+t+'s'; fill=Math.max(0,horde.t)/WAVEBAR.brk; urgent=horde.t<=5; }
  else { if(WAVEBAR.phase!=='wave'||WAVEBAR.wave!==horde.wave){ WAVEBAR.total=0; WAVEBAR.bonus=0; } const left=alive+(horde.toSpawn|0); WAVEBAR.total=Math.max(WAVEBAR.total,left);
    title='Wave '+horde.wave; sub=left+' left'; fill=WAVEBAR.total?left/WAVEBAR.total:0; }
  WAVEBAR.phase=horde.phase; WAVEBAR.wave=horde.wave;
  const key=title+'|'+(brk?'':sub); if(key!==WAVEBAR.key){ WAVEBAR.key=key; WAVEBAR.shown=now; }
  el.classList.toggle('on',urgent||now-WAVEBAR.shown<3500); el.classList.toggle('urgent',urgent); el.classList.toggle('brk',brk&&!urgent);
  const txt=title+'|'+sub; if(txt!==WAVEBAR.txt){ WAVEBAR.txt=txt; $('whT').textContent=title; $('whS').textContent=sub; }
  $('whF').style.transform='scaleX('+Math.max(0,Math.min(1,fill)).toFixed(3)+')';
}"""+s[b:]
# guns hit 25% softer (players, the bot and creatures alike); build damage stays the same
rep("const WEAPONS={};\nfor(const [id,B] of Object.entries(BASE_WEAPONS)){\n  WEAPONS[id]=Object.assign({id,base:id,model:id},B);",
    "const WEAPONS={}, GUN_DMG=0.75; // every gun's damage is scaled by this (builds take the same damage as before)\nfor(const [id,B] of Object.entries(BASE_WEAPONS)){\n  WEAPONS[id]=Object.assign({id,base:id,model:id},B,{dmg:Math.round(B.dmg*GUN_DMG*10)/10,build:(B.build||1)/GUN_DMG});")
rep("rarity:rar,dmg:Math.round(B.dmg*k*10)/10,","rarity:rar,dmg:Math.round(B.dmg*GUN_DMG*k*10)/10,")

# ---------- 65. drop in through the clouds: every drop from the sky (first time in, a match start, Respawn, a respawn
# after going down) opens with a short fall through a white cloud bank that parts to show the island below. The cloud
# hides the move, so drops now land at random spots all over the map (a party still drops together: everyone picks the
# same spot from the match number). ----------
rep('<div id="hurtfx"></div>','<div id="hurtfx"></div>\n<div id="cloudFx" hidden></div>')
rep('#hurtfx{position:fixed;',r'''#cloudFx{position:fixed;inset:0;pointer-events:none;z-index:4;overflow:hidden;background:radial-gradient(ellipse at 50% 60%,#ffffff 0%,#eef4fb 55%,#d9e6f3 100%);opacity:0}
#cloudFx i{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,1) 0%,rgba(255,255,255,.92) 45%,rgba(240,246,252,.55) 70%,rgba(240,246,252,0) 100%);filter:blur(6px);will-change:transform,opacity}
#cloudFx.go{animation:cloudIn 2.3s ease-in forwards}
#cloudFx.go i{animation:puffUp 2.3s cubic-bezier(.5,0,.75,.4) forwards}
@keyframes cloudIn{0%{opacity:1}35%{opacity:1}100%{opacity:0}}
@keyframes puffUp{0%{transform:translate(0,0) scale(1);opacity:1}100%{transform:translate(var(--dx),-130vh) scale(2.6);opacity:.2}}
#hurtfx{position:fixed;''')
rep("    case 'rb_tick':","    case 'cloud': noise(700,1.9,0.16,0.45,0,'bandpass',260); noise(2600,1.2,0.06,0.6,0.05,'highpass',900); break;\n    case 'rb_tick':")
rep("const SKY_AUTO=85, SKY_FIRST=620, SKY_MATCH=520, SKY_BACK=160;",r"""const SKY_AUTO=85, SKY_FIRST=620, SKY_MATCH=520, SKY_BACK=160;
// a random open spot somewhere on the island (not up a mountainside); r is a random-number source (seeded for parties)
function randomDropSpot(r=Math.random){ const h0=terrainH(SPAWN[0],SPAWN[2]);
  for(let i=0;i<80;i++){ const a=r()*Math.PI*2, d=Math.sqrt(r())*640, x=SPAWN[0]+Math.cos(a)*d, z=SPAWN[2]+Math.sin(a)*d;
    if(slopeAt(x,z)[0]<0.3&&terrainH(x,z)<h0+70) return [x,z]; }
  return [SPAWN[0],SPAWN[2]]; }
// the screen goes white and the cloud bank rushes up past you as you fall out of it
function cloudFx(){ const el=document.getElementById('cloudFx'); if(!el) return;
  if(!el.children.length) for(let i=0;i<16;i++){ const p=document.createElement('i'), s=30+Math.random()*55; p.style.cssText=`width:${s}vmax;height:${s*0.62}vmax;left:${Math.random()*110-25}%;top:${40+Math.random()*80}%;--dx:${(Math.random()-0.5)*40}vw;animation-delay:${Math.random()*0.25}s`; el.appendChild(p); }
  el.hidden=false; el.classList.remove('go'); void el.offsetWidth; el.classList.add('go'); sfx('cloud');
  clearTimeout(cloudFx.t); cloudFx.t=setTimeout(()=>{ el.classList.remove('go'); el.hidden=true; },2500); }
function cloudDrop(x,z,h){ cloudFx(); skyDrop(x,z,h); }""")
# first time in
rep("emptyLoadout(); skyDrop(SPAWN[0],SPAWN[2],SKY_FIRST); } } // the first time in: from the sky","emptyLoadout(); const sp=randomDropSpot(); cloudDrop(sp[0],sp[1],SKY_FIRST); } } // the first time in: from the sky")
# Respawn button
rep("emptyLoadout(); const a=Math.random()*6.283, r=12+Math.random()*25; skyDrop(SPAWN[0]+Math.cos(a)*r,SPAWN[2]+Math.sin(a)*r,SKY_BACK); } });","emptyLoadout(); const sp=randomDropSpot(); P.pos.set(sp[0],terrainH(sp[0],sp[1]),sp[1]); cloudDrop(sp[0],sp[1],SKY_BACK); } });")
# respawn after going down in a room
rep("function rbRespawnNow(){ net.dead=false; const a=Math.random()*Math.PI*2, r=8+Math.random()*20; respawn(); P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); if(skyDropAllowed()) skyDrop(P.pos.x,P.pos.z,SKY_BACK); }",
    "function rbRespawnNow(){ net.dead=false; respawn(); if(skyDropAllowed()){ const sp=randomDropSpot(); P.pos.set(sp[0],terrainH(sp[0],sp[1]),sp[1]); emptyLoadout(); cloudDrop(sp[0],sp[1],SKY_BACK); } else { const a=Math.random()*Math.PI*2, r=8+Math.random()*20; P.pos.set(SPAWN[0]+Math.cos(a)*r,0,SPAWN[2]+Math.sin(a)*r); } }")
# solo horde start
rep("if(skyDropAllowed()){ const a=Math.random()*6.283; skyDrop(SPAWN[0]+Math.cos(a)*20,SPAWN[2]+Math.sin(a)*20,SKY_MATCH); } }","if(skyDropAllowed()){ const sp=randomDropSpot(); cloudDrop(sp[0],sp[1],SKY_MATCH); } }")
# party match: the same random spot for everyone, each a few metres apart
rep("function matchDrop(){ const r=seeded(1000+party.seq), a=r()*6.283, cx=SPAWN[0]+Math.cos(a)*30, cz=SPAWN[2]+Math.sin(a)*30;","function matchDrop(){ const r=seeded(1000+party.seq), [cx,cz]=randomDropSpot(r);")
rep("  emptyLoadout(); skyDrop(cx+Math.cos(b)*d,cz+Math.sin(b)*d,SKY_MATCH); }","  emptyLoadout(); cloudDrop(cx+Math.cos(b)*d,cz+Math.sin(b)*d,SKY_MATCH); }")

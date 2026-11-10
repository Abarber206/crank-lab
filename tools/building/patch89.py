# ---------- 89. slim pause menu, fewer messages, far things fade fully into the haze, HUD bars never overlap the weapon bar ----------
# (a) paused mid-match: just Resume / Respawn / Fullscreen with the Settings and Controls tabs (Locker, Item Shop, mode
# cards, the bot option, the blurb and the party box belong to the lobby; the party box stays if you're in a party)
rep("#menu *{touch-action:pan-y}",r"""#menu *{touch-action:pan-y}
#menu:not(.lobby) .mtabs button[data-tab=locker],#menu:not(.lobby) .mtabs button[data-tab=shop],#menu:not(.lobby) #modeCards,#menu:not(.lobby) #allyOpt,#menu:not(.lobby) .mtab[data-tab=play]>.sub,#menu:not(.lobby) #clear{display:none}
#menu:not(.lobby):not(.inparty) #partyBox{display:none}
#menu:not(.lobby) .panel{width:min(560px,100%)}
#menu:not(.lobby) .mtab[data-tab=settings] .set{grid-template-columns:1fr}""")
rep("function syncLobby(){ const lob=inLobby(); menu.classList.toggle('lobby',lob);","function syncLobby(){ const lob=inLobby(); menu.classList.toggle('lobby',lob); menu.classList.toggle('inparty',!!net.role); if(!lob){ const cur=document.querySelector('.mtabs button.on'); if(cur&&(cur.dataset.tab==='locker'||cur.dataset.tab==='shop')) showTab('play'); }")
# (b) messages: no feed line when Buddy picks up a gun; a build shows only its health (no Anchored / Supported / holding-up line), houses just their bar
rep("feed('<b>Buddy</b> picked up '+(itemInfo(d.item).name||'a gun')); ","")
rep("  $('pieceHpT').textContent=(p.skin?'House · farms '+MATERIALS[p.mat].name.toLowerCase():MATERIALS[p.mat].name)+' '+Math.ceil(p.hp)+' / '+p.maxHp;","  $('pieceHpT').textContent=p.skin&&p.owner==='world'?'':MATERIALS[p.mat].name+' '+Math.ceil(p.hp)+' / '+p.maxHp;")
rep("  const n=dependentsOf(p), st=grounded(p)?'Anchored':'Supported';\n  $('pieceHpS').textContent=st+(n?' · holding up '+n:'')+(growing.has(p)?' · building':'');","  $('pieceHpS').textContent='';")
# (c) haze: only the terrain keeps a little of itself at any distance (so the far ranges still read); everything else fades right out
rep("float fogFactor = clamp( 1.0 - exp( - fogNear * exp( - fy0 / fH ) * fk * fogDepth ), 0.0, 0.93 );","float fogFactor = clamp( 1.0 - exp( - fogNear * exp( - fy0 / fH ) * fk * fogDepth ), 0.0, FOG_CAP );")
rep("THREE.ShaderChunk.fog_pars_fragment='#ifdef USE_FOG\\n\\tuniform vec3 fogColor;","THREE.ShaderChunk.fog_pars_fragment='#ifndef FOG_CAP\\n#define FOG_CAP 0.992\\n#endif\\n#ifdef USE_FOG\\n\\tuniform vec3 fogColor;")
rep("const terrainMat=new THREE.MeshLambertMaterial({map:groundTexture(14),vertexColors:true,color:0xb6cfb0});","const terrainMat=new THREE.MeshLambertMaterial({map:groundTexture(14),vertexColors:true,color:0xb6cfb0}); terrainMat.defines=Object.assign({},terrainMat.defines||{},{FOG_CAP:'0.93'});")
# (d) HUD: on narrower windows the shield/health bars sit bottom-left so they never run under the weapon bar
rep("@media (max-width:900px){ body:not(.touch) #vitals{left:calc(env(safe-area-inset-left,0px) + 14px);transform:none;width:240px} body:not(.touch) #xAmmo{left:134px} }",
    "@media (max-width:1300px){ body:not(.touch) #vitals{left:calc(env(safe-area-inset-left,0px) + 14px);transform:none;width:min(360px,calc(100vw - 460px))} body:not(.touch) #xAmmo{left:calc(14px + min(180px,50vw - 230px))} }")

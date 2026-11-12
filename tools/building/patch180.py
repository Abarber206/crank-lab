# patch180: material icons drawn from real 3D models, like the sketches: wood is a little pile of three logs showing
# their ringed ends, brick is a block of grey stone, metal is a stack of steel I-beams. The count sits in a round badge
# to the left of each. Guns get a stats card: when you look at a gun on the ground (above the pick-up prompt), and for
# the selected slot in the inventory: damage, fire rate, damage per second, magazine and reload, as bars against the
# best in the game.
rep("""function iconModel(id){
  const g=new THREE.Group();""","""// the material models for the icons
let _matTex=null;
function matTex(){ if(_matTex) return _matTex; const mk=(w,h,f)=>{ const c=document.createElement('canvas'); c.width=w; c.height=h; f(c.getContext('2d'),w,h); const t=new THREE.CanvasTexture(c); t.anisotropy=4; return t; }, R=seeded(31337);
  _matTex={
    bark:mk(256,96,(g,w,h)=>{ g.fillStyle='#b98544'; g.fillRect(0,0,w,h); for(let i=0;i<340;i++){ const y=R()*h, x=R()*w, l=20+R()*90; g.strokeStyle=`rgba(${55+R()*35|0},${32+R()*20|0},14,${0.35+R()*0.45})`; g.lineWidth=0.6+R()*1.6; g.beginPath(); g.moveTo(x,y); g.bezierCurveTo(x+l*0.3,y+(R()-.5)*4,x+l*0.7,y+(R()-.5)*4,x+l,y+(R()-.5)*3); g.stroke(); }
      const kx=w*0.55, ky=h*0.45; for(let r=16;r>2;r-=3){ g.strokeStyle=`rgba(60,38,18,${0.25+0.05*(16-r)})`; g.lineWidth=1.4; g.beginPath(); g.ellipse(kx,ky,r*1.7,r*0.8,0,0,7); g.stroke(); } g.fillStyle='rgba(50,30,14,.7)'; g.beginPath(); g.ellipse(kx,ky,6,3,0,0,7); g.fill(); }),
    end:mk(128,128,(g,w,h)=>{ const c=w/2; g.fillStyle='#ecd096'; g.fillRect(0,0,w,h); for(let r=8;r<58;r+=4+R()*3){ g.strokeStyle=`rgba(${150+R()*30|0},${105+R()*20|0},60,.75)`; g.lineWidth=1.3; g.beginPath(); g.ellipse(c+(R()-.5)*2,c+(R()-.5)*2,r,r*(0.95+R()*0.08),R(),0,7); g.stroke(); }
      g.lineWidth=7; g.strokeStyle='#b8663e'; g.beginPath(); g.arc(c,c,59,0,7); g.stroke(); g.lineWidth=3; g.strokeStyle='#7a4a2a'; g.beginPath(); g.arc(c,c,62.5,0,7); g.stroke();
      g.fillStyle='#8a5a2e'; g.beginPath(); g.arc(c,c,3.5,0,7); g.fill(); g.strokeStyle='rgba(90,55,25,.8)'; g.lineWidth=1.4; for(let k=0;k<3;k++){ const a=R()*6.28; g.beginPath(); g.moveTo(c+Math.cos(a)*6,c+Math.sin(a)*6); g.lineTo(c+Math.cos(a)*(30+R()*20),c+Math.sin(a)*(30+R()*20)); g.stroke(); } }),
    stone:mk(256,128,(g,w,h)=>{ g.fillStyle='#6c7179'; g.fillRect(0,0,w,h); for(let i=0;i<3000;i++){ const v=R(); g.fillStyle=v<.5?'rgba(30,33,38,.3)':'rgba(170,176,184,.22)'; g.fillRect(R()*w,R()*h,1+R()*2,1+R()*2); }
      for(let i=0;i<90;i++){ const x=R()*w, y=R()*h, a=(R()-.5)*1.2, l=6+R()*22; g.strokeStyle=`rgba(35,38,44,${0.3+R()*0.4})`; g.lineWidth=1+R()*1.5; g.beginPath(); g.moveTo(x,y); g.lineTo(x+Math.cos(a)*l,y+Math.sin(a)*l); g.stroke(); }
      g.strokeStyle='rgba(30,32,36,.55)'; g.lineWidth=1.5; g.beginPath(); g.moveTo(w*0.62,0); g.lineTo(w*0.58,h*0.3); g.lineTo(w*0.66,h*0.55); g.lineTo(w*0.6,h); g.stroke(); }) };
  return _matTex; }
function matModel(m){ const g=new THREE.Group(), T=matTex();
  if(m==='wood'){ const side=new THREE.MeshLambertMaterial({map:T.bark}), end=new THREE.MeshLambertMaterial({map:T.end});
    for(const [x,y,z,r,l] of [[0,0.22,0.235,0.22,0.95],[0.06,0.22,-0.235,0.22,0.9],[0.12,0.6,0,0.21,0.85]]){ const c=new THREE.Mesh(new THREE.CylinderGeometry(r,r*1.04,l,22),[side,end,end]); c.rotation.z=Math.PI/2; c.position.set(x-l/2+0.45,y,z); g.add(c); } }
  else if(m==='brick'){ const b=new THREE.Mesh(rbox(1.05,0.5,0.6,0.06),new THREE.MeshLambertMaterial({map:T.stone})); b.position.y=0.25; g.add(b);
    const chip=new THREE.Mesh(new THREE.DodecahedronGeometry(0.08,0),new THREE.MeshLambertMaterial({color:0x7c8188})); chip.position.set(0.62,0.05,0.25); g.add(chip); }
  else { const sh=new THREE.Shape(), F=0.3, Hh=0.3, tw=0.06, tf=0.06; sh.moveTo(-F/2,0); sh.lineTo(F/2,0); sh.lineTo(F/2,tf); sh.lineTo(tw/2,tf); sh.lineTo(tw/2,Hh-tf); sh.lineTo(F/2,Hh-tf); sh.lineTo(F/2,Hh); sh.lineTo(-F/2,Hh); sh.lineTo(-F/2,Hh-tf); sh.lineTo(-tw/2,Hh-tf); sh.lineTo(-tw/2,tf); sh.lineTo(-F/2,tf); sh.lineTo(-F/2,0);
    const geo=new THREE.ExtrudeGeometry(sh,{depth:0.95,bevelEnabled:true,bevelThickness:0.008,bevelSize:0.008,bevelSegments:1}), cut=new THREE.MeshPhongMaterial({color:0x4c5560,specular:0x444444,shininess:30}), face=new THREE.MeshPhongMaterial({color:0x6f7d8c,specular:0xc8d4e0,shininess:60});
    for(const [x,y,z] of [[0,0,0.17],[0.05,0,-0.17],[0.1,0.3,0]]){ const b=new THREE.Mesh(geo,[cut,face]); b.rotation.y=Math.PI/2; b.position.set(x-0.47,y,z); g.add(b); } }
  return g; }
function iconModel(id){
  const g=new THREE.Group();
  if(typeof id==='string'&&id.startsWith('mat_')){ g.add(matModel(id.slice(4))); g.rotation.set(0.42,-0.72,0); return g; }""")
# matIcon: the 3D picture when it's ready (the flat one until then)
rep("""function matIcon(m){ return""","""function matIcon(m){ const u=ICON_IMG.get('mat_'+m); if(u) return `<img src="${u}" alt="" style="width:100%;height:100%;object-fit:contain;display:block">`; if(u===undefined) queueIcons(['mat_'+m]); return matIcon0(m); }
function matIcon0(m){ return""")
rep("""    if(iconQ.length) requestAnimationFrame(step); else { iconBusy=false; if(iconR){ iconR.dispose(); if(iconR.forceContextLoss) iconR.forceContextLoss(); iconR=null; } renderSlots(); if(invOpen) renderInv(); } };""",
    """    if(iconQ.length) requestAnimationFrame(step); else { iconBusy=false; if(iconR){ iconR.dispose(); if(iconR.forceContextLoss) iconR.forceContextLoss(); iconR=null; } renderSlots(); if(invOpen) renderInv(); { const sw=$('matSw'); if(sw) sw.dataset.m=''; } if(typeof syncMats==='function') syncMats(); } };""")
# the stock: a round count badge to the left of each picture
rep("""st.innerHTML=MAT_ORDER.map(m=>`<span class="${m===buildMat?'on':''}"><i class="mi">${matIcon(m)}</i>${(P.mats&&P.mats[m])|0}</span>`).join('');""",
    """st.innerHTML=MAT_ORDER.map(m=>`<span class="${m===buildMat?'on':''}"><b class="mc">${(P.mats&&P.mats[m])|0}</b><i class="mi">${matIcon(m)}</i></span>`).join('');""")
rep("""#matStock i{width:18px;height:18px;display:block}""","""#matStock i{width:30px;height:30px;display:block} #matStock i img{filter:drop-shadow(0 1px 1px rgba(0,0,0,.6))}
#matStock .mc{order:-1;min-width:26px;height:26px;padding:0 4px;border-radius:13px;display:grid;place-items:center;background:rgba(14,18,24,.82);border:2px solid #d8b878;font:800 13px/1 "Chakra Petch",sans-serif;font-style:normal;color:#fff;margin-right:-10px;position:relative;z-index:1}""")
rep("""body:not(.touch) #matStock i{width:22px;height:22px}""","""body:not(.touch) #matStock i{width:40px;height:40px} body:not(.touch) #matStock span{flex-direction:row;align-items:center}""")
rep("""  $('invMats').innerHTML=MAT_ORDER.map(m=>`<span><i style="background:#${MATERIALS[m].chip.toString(16).padStart(6,'0')}"></i>${MATERIALS[m].name}<b>${infMats()?'∞':(P.mats[m]|0)}</b></span>`).join('');""",
    """  $('invMats').innerHTML=MAT_ORDER.map(m=>`<span><i class="imat">${matIcon(m)}</i>${MATERIALS[m].name}<b>${infMats()?'∞':(P.mats[m]|0)}</b></span>`).join('');
  { const id=P.inv[invSel]; $('invStats').innerHTML=id?statCard(id):''; }""")
rep("""    <div id="invSlots" class="islots"></div>""","""    <div id="invSlots" class="islots"></div>
    <div id="invStats"></div>""")
# ---- gun stats
rep("""function renderInv(){""","""// a gun's numbers and bars (the bars against the best gun in the game); for heals, what they do
function gunNums(W){ const ex=!!W.proj, dmg=ex?0:W.dmg*(W.pellets||1), fr=1/W.rate; return {ex,dmg,fr,dps:dmg*fr,mag:W.mag||1,rel:W.reload!=null?W.reload:(W.shell||0.5)*(W.mag||1)}; } // (a shotgun loaded shell by shell: the time to fill it)
let _statMax=null;
function statMax(){ if(_statMax) return _statMax; const M={dmg:1,fr:1,dps:1,mag:1,rel:1}; Object.values(WEAPONS).forEach(W=>{ if(W.throw) return; const n=gunNums(W); M.dmg=Math.max(M.dmg,n.dmg); M.fr=Math.max(M.fr,n.fr); M.dps=Math.max(M.dps,n.dps); M.mag=Math.max(M.mag,n.mag); M.rel=Math.max(M.rel,n.rel); }); return _statMax=M; }
function statCard(id){ const I=itemInfo(id), col='#'+(RCOL[I.rarity]||0xffffff).toString(16).padStart(6,'0');
  const head=`<div class="sc-h"><svg viewBox="0 0 48 48">${iconOf(id)}</svg><div><b style="color:${col}">${esc(I.name)}</b><small>${I.rarity}</small></div></div>`;
  if(WEAPONS[id]&&id!=='nade'){ const W=WEAPONS[id], n=gunNums(W), M=statMax(), bar=(lab,v,max,txt,inv)=>`<div class="sc-r"><span>${lab}</span><i><u style="width:${Math.max(4,Math.min(100,100*(inv?1-(v-0.5)/max:v/max))).toFixed(0)}%;background:${col}"></u></i><b>${txt}</b></div>`;
    return `<div class="statc">${head}${n.ex?`<div class="sc-r"><span>Damage</span><i><u style="width:100%;background:${col}"></u></i><b>Explosive</b></div>`:bar('Damage',n.dmg,M.dmg,Math.round(n.dmg)+(W.pellets>1?` <small>(${W.pellets}×${W.dmg})</small>`:''))}
      ${bar('Fire rate',n.fr,M.fr,n.fr.toFixed(1)+'/s')}${n.ex?'':bar('DPS',n.dps,M.dps,Math.round(n.dps))}${bar('Magazine',n.mag,M.mag,n.mag)}${bar('Reload',n.rel,M.rel,n.rel.toFixed(1)+' s',true)}
      <div class="sc-f"><span>Headshot ×${(W.head||1).toFixed(2).replace(/0$/,'')}</span><span>${AMMO_T[W.ammo]?AMMO_T[W.ammo].name:''}</span>${W.auto?'<span>Automatic</span>':''}</div></div>`; }
  if(ITEMS[id]){ const T=ITEMS[id]; return `<div class="statc">${head}<div class="sc-f"><span>${T.stat==='hp'?'+'+T.amt+' health, up to '+T.cap:'+'+T.amt+' shield, up to '+T.cap}</span><span>${T.use.toFixed(1)} s to use</span><span>Stacks to ${T.max}</span></div></div>`; }
  return `<div class="statc">${head}</div>`; }
function renderInv(){""")
rep("""<div class="hud" id="chestBar" hidden>""","""<div class="hud" id="lootCard" hidden></div>
<div class="hud" id="chestBar" hidden>""")
rep("""#bigmapC{width:100%;height:100%;display:block;cursor:crosshair}""","""#bigmapC{width:100%;height:100%;display:block;cursor:crosshair}
.statc{background:linear-gradient(180deg,rgba(18,24,34,.94),rgba(10,14,20,.94));border:1px solid rgba(255,255,255,.14);border-radius:6px;padding:10px 12px;color:#fff;font:600 13px/1.2 "Chakra Petch",sans-serif;min-width:260px;max-width:340px}
.statc .sc-h{display:flex;gap:10px;align-items:center;margin-bottom:6px} .statc .sc-h svg{width:64px;height:40px;flex:none} .statc .sc-h b{font:800 italic 18px/1 "Barlow Condensed",sans-serif;text-transform:uppercase;display:block} .statc .sc-h small{opacity:.7;text-transform:capitalize}
.statc .sc-r{display:grid;grid-template-columns:76px 1fr 74px;gap:8px;align-items:center;margin:4px 0} .statc .sc-r span{opacity:.8} .statc .sc-r i{height:7px;background:rgba(255,255,255,.12);border-radius:4px;overflow:hidden;display:block} .statc .sc-r u{display:block;height:100%;border-radius:4px}
.statc .sc-r b{text-align:right;font-weight:800} .statc .sc-r b small{opacity:.7;font-weight:600} .statc .sc-f{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:6px;opacity:.85;font-size:12px}
#lootCard{left:50%;bottom:calc(env(safe-area-inset-bottom,0px) + 318px);transform:translateX(-50%);pointer-events:none} #invStats{margin:10px 0 0;display:flex;justify-content:center} #invStats:empty{display:none}
#invMats .imat{width:26px;height:26px;display:inline-block;vertical-align:middle;background:none!important;border-radius:0!important} #invMats .imat svg{width:100%;height:100%}""")
# show the card while you look at a gun or a heal on the ground
rep("""  showing=!!useTgt; if(showing){""","""  { const lc=$('lootCard'), d=useTgt&&useTgt.kind==='drop'?useTgt.d:null, key=d?d.item:''; if(lc.dataset.k!==key){ lc.dataset.k=key; lc.innerHTML=key?statCard(key):''; lc.hidden=!key; } }
  showing=!!useTgt; if(showing){""")

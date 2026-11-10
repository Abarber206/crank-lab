# ---------- 86. reboot van polish and material icons ----------
# (a) the van: big REBOOT lettering on its blind side, a dish that turns, a glowing pad where you stand to use it (bright
# while you're carrying a card), a hologram card turning over the roof while someone needs rebooting, and a hum up close
rep("  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);\n  const flare=",
r"""  { const cv=document.createElement('canvas'); cv.width=512; cv.height=128; const q=cv.getContext('2d'); q.fillStyle='#1f5fd8'; q.fillRect(0,0,512,128); q.fillStyle='#ff7a1a'; q.fillRect(0,112,512,16);
    q.save(); q.translate(64,60); q.lineWidth=11; q.strokeStyle='#fff'; q.beginPath(); q.arc(0,0,34,0.5,5.6); q.stroke(); q.fillStyle='#fff'; q.beginPath(); q.moveTo(34*Math.cos(5.6)+16,34*Math.sin(5.6)-2); q.lineTo(34*Math.cos(5.6)-12,34*Math.sin(5.6)-18); q.lineTo(34*Math.cos(5.6)-8,34*Math.sin(5.6)+16); q.fill(); q.restore();
    q.fillStyle='#fff'; q.font='900 italic 74px "Arial Black",Arial,sans-serif'; q.textBaseline='middle'; q.fillText('REBOOT',128,62);
    const sign=new THREE.Mesh(new THREE.PlaneGeometry(2.5,0.62),new THREE.MeshPhongMaterial({map:new THREE.CanvasTexture(cv),shininess:50})); sign.rotation.y=-Math.PI/2; sign.position.set(-1.066,2.1,0.55); g.add(sign); }
  const pad=new THREE.Mesh(new THREE.RingGeometry(0.55,0.72,40).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:0x7fc8ff,transparent:true,opacity:0.35,blending:THREE.AdditiveBlending,depthWrite:false,fog:false})); pad.position.set(1.75,0.09,0.55); g.add(pad);
  const holo=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.7,0.03),new THREE.MeshBasicMaterial({color:0x9fd8ff,transparent:true,opacity:0.75,blending:THREE.AdditiveBlending,depthWrite:false,fog:false})); holo.position.set(-0.35,3.75,-0.1); holo.visible=false; g.add(holo);
  g.position.set(x,y,z); g.rotation.y=yaw; scene.add(g);
  const flare=""")
rep("  return {x,y,z,yaw,g,scr,beacon,flare,cd:0,","  return {x,y,z,yaw,g,scr,beacon,flare,dish,pad,holo,cd:0,")
rep("    const ready=now>=v.cd; if(v.scr.material!==(ready?_vanMats.ready:_vanMats.wait))",
r"""    { const dv=Math.hypot(v.x-P.pos.x,v.z-P.pos.z); if(dv<160){ v.dish.rotation.y+=dt*0.5; const need=rbNeeded(), carry=RB.carry.size>0;
        v.pad.material.opacity=(carry?0.6+0.3*Math.sin(T*5):0.22)*(now>=v.cd?1:0.4); const ps=carry?1+0.08*Math.sin(T*5):1; v.pad.scale.set(ps,1,ps);
        v.holo.visible=need&&now>=v.cd; if(v.holo.visible){ v.holo.rotation.y+=dt*2.2; v.holo.position.y=3.75+0.1*Math.sin(T*2.4+v.id); v.holo.material.opacity=0.55+0.25*Math.sin(T*6+v.id); }
        if(dv<14&&AC){ v.humT=(v.humT||0)-dt; if(v.humT<=0){ v.humT=1.9; sfxAt('van_hum',new THREE.Vector3(v.x,v.y+1.5,v.z)); } } } }
    const ready=now>=v.cd; if(v.scr.material!==(ready?_vanMats.ready:_vanMats.wait))""")
rep("    case 'rb_tick':","    case 'van_hum': tone('sine',58,58,2.0,0.035); tone('sine',116,117,2.0,0.012); tone('triangle',880,880,0.05,0.008,1.0); break;\n    case 'rb_tick':")
rep("function stepReboot(dt){ if(!net.role&&!RB.cards.size&&!P.down&&!(AB&&AB.active)) return;","function stepReboot(dt){")
# (b) material icons: planks, bricks and a steel plate instead of flat colour chips
rep("function syncMats(){",r"""function matIcon(m){ return m==='wood'?'<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="5.4" rx="1" fill="#e0b070"/><rect x="2" y="9.3" width="20" height="5.4" rx="1" fill="#cf9a58"/><rect x="2" y="15.6" width="20" height="5.4" rx="1" fill="#e0b070"/><path d="M5 5.7h7M14 12h6M6 18.3h9" stroke="#8a5a2a" stroke-width="1" stroke-linecap="round"/><circle cx="17" cy="5.7" r="1" fill="#8a5a2a"/><circle cx="8" cy="12" r="1" fill="#8a5a2a"/></svg>'
  :m==='brick'?'<svg viewBox="0 0 24 24"><rect x="1.5" y="3" width="21" height="18" rx="1.5" fill="#d9cfc2"/><g fill="#c23f33"><rect x="2.5" y="4" width="9" height="4.6" rx=".6"/><rect x="12.5" y="4" width="9" height="4.6" rx=".6"/><rect x="2.5" y="9.7" width="4.2" height="4.6" rx=".6"/><rect x="7.7" y="9.7" width="8.6" height="4.6" rx=".6"/><rect x="17.3" y="9.7" width="4.2" height="4.6" rx=".6"/><rect x="2.5" y="15.4" width="9" height="4.6" rx=".6"/><rect x="12.5" y="15.4" width="9" height="4.6" rx=".6"/></g></svg>'
  :'<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="18" rx="2" fill="#9aa6b2"/><path d="M2 9l20-5M2 16l20-5M6 21l16-4" stroke="#c9d3dc" stroke-width="2.2" opacity=".8"/><rect x="2" y="3" width="20" height="18" rx="2" fill="none" stroke="#5d6772" stroke-width="1.6"/><g fill="#4d5660"><circle cx="5.2" cy="6.2" r="1.1"/><circle cx="18.8" cy="6.2" r="1.1"/><circle cx="5.2" cy="17.8" r="1.1"/><circle cx="18.8" cy="17.8" r="1.1"/></g></svg>'; }
function syncMats(){ { const sw=$('matSw'); if(sw&&sw.dataset.m!==buildMat){ sw.dataset.m=buildMat; sw.innerHTML=matIcon(buildMat); sw.style.background='none'; sw.style.boxShadow='none'; } }""")
rep("st.innerHTML=MAT_ORDER.map(m=>`<span class=\"${m===buildMat?'on':''}\"><i style=\"background:#${MATERIALS[m].chip.toString(16).padStart(6,'0')}\"></i>${(P.mats&&P.mats[m])|0}</span>`).join('');",
    "st.innerHTML=MAT_ORDER.map(m=>`<span class=\"${m===buildMat?'on':''}\"><i class=\"mi\">${matIcon(m)}</i>${(P.mats&&P.mats[m])|0}</span>`).join('');")
rep("#matStock i{width:14px;height:14px;border-radius:3px;box-shadow:inset 0 0 0 2px rgba(0,0,0,.35)}","#matStock i{width:18px;height:18px;display:block} #matStock i svg,#matSw svg{width:100%;height:100%;display:block;filter:drop-shadow(0 1px 1px rgba(0,0,0,.5))}")
rep("$('matName').textContent=MATERIALS[buildMat].name; $('matSw').style.background='#'+MATERIALS[buildMat].chip.toString(16).padStart(6,'0');","$('matName').textContent=MATERIALS[buildMat].name; { const sw=$('matSw'); if(sw.dataset.m!==buildMat&&typeof matIcon==='function'){ sw.dataset.m=buildMat; sw.innerHTML=matIcon(buildMat); sw.style.background='none'; sw.style.boxShadow='none'; } }")

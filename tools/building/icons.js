/* ---------- item icons, rendered from the real models ----------
   Every weapon's icon is a picture of the same 3D gun you hold (its stock, magazine, sights, muzzle device and
   rarity trim), drawn side-on and slightly turned. Items and ammo use their loot models. The pictures are made
   once, a few at a time after loading; until a picture is ready the old flat icon stands in. */
const ICON_IMG=new Map(); let iconR=null, iconQ=[], iconBusy=false;
function iconKey(id){ return WEAPONS[id]?WEAPONS[id].model+'|'+WEAPONS[id].rarity:id; }
function iconModel(id){
  const g=new THREE.Group();
  if(WEAPONS[id]){ if(!lootTmpl) lootTmpl=heroFor(OUTFITS[0]);
    const LW=WEAPONS[id], src=LW.model==='ar'?'gun':LW.model, w=lootTmpl.rig[src].clone(true); w.visible=true; w.position.set(0,0,0); w.rotation.set(0,0,0); w.scale.setScalar(1);
    w.traverse(o=>{ if(o.isMesh&&o.userData.trim){ o.material=o.material.clone(); o.material.color.setHex(RCOL[LW.rarity]); } o.visible=o.visible!==false; });
    // hand space is -y forward, -z up: turn it so the muzzle points right and the top is up, showing its right side
    const hold=new THREE.Group(); hold.add(w); hold.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(new THREE.Vector3(0,0,1),new THREE.Vector3(-1,0,0),new THREE.Vector3(0,-1,0)));
    g.add(hold); g.rotation.set(0.12,-0.42,0.06); }
  else { const m=lootModel0(id); g.add(m); g.rotation.set(0.45,-0.6,0); }
  return g; }
function renderIcon(id){
  const S=128; if(!iconR){ iconR=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true}); iconR.setPixelRatio(1); iconR.setSize(S,S); iconR.setClearColor(0,0);
    iconR.scene=new THREE.Scene(); iconR.scene.add(new THREE.HemisphereLight(0xffffff,0x4a5568,0.9)); const k=new THREE.DirectionalLight(0xffffff,0.9); k.position.set(-2,3,5); iconR.scene.add(k);
    const rim=new THREE.DirectionalLight(0xbfe4ff,0.55); rim.position.set(3,2,-4); iconR.scene.add(rim); iconR.cam=new THREE.OrthographicCamera(-1,1,1,-1,0.01,50); iconR.cam.position.set(0,0,10); iconR.cam.lookAt(0,0,0); }
  const sc=iconR.scene, m=iconModel(id); sc.add(m); m.updateMatrixWorld(true);
  const bb=new THREE.Box3().setFromObject(m), c=bb.getCenter(new THREE.Vector3()), sz=bb.getSize(new THREE.Vector3()), half=Math.max(sz.x,sz.y)/2*1.08||1;
  m.position.sub(c); const cam=iconR.cam; cam.left=-half; cam.right=half; cam.top=half; cam.bottom=-half; cam.updateProjectionMatrix();
  iconR.render(sc,cam); const url=iconR.domElement.toDataURL('image/png'); sc.remove(m); return url; }
// a few pictures per frame so loading never stutters
function pumpIcons(){ if(iconBusy) return; iconBusy=true;
  const step=()=>{ let n=0; while(iconQ.length&&n<4){ const id=iconQ.shift(), k=iconKey(id); if(!ICON_IMG.has(k)){ try{ ICON_IMG.set(k,renderIcon(id)); }catch(e){ ICON_IMG.set(k,null); } n++; } }
    if(iconQ.length) requestAnimationFrame(step); else { iconBusy=false; if(iconR){ iconR.dispose(); if(iconR.forceContextLoss) iconR.forceContextLoss(); iconR=null; } renderSlots(); if(invOpen) renderInv(); } };
  requestAnimationFrame(step); }
function queueIcons(ids){ ids.forEach(id=>{ if(!ICON_IMG.has(iconKey(id))&&!iconQ.includes(id)) iconQ.push(id); }); if(iconQ.length) pumpIcons(); }

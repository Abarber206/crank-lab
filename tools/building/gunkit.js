/* ---------- gun kit by rarity ----------
   The same gun is built up differently at each rarity, so you can tell them apart by shape: a common one is bare, an
   uncommon one gets an angled foregrip, a rare one a vertical grip and a red-dot sight, an epic one adds an extended
   magazine and a muzzle brake, and a legendary one carries a scope, a longer magazine still, a long compensator and a
   laser module. Works on the gun in your hands (the rig's own model), on dropped loot and on the inventory pictures
   (which are clones of it). Only the small rarity stripe on the gun is coloured. */
const GUN_ATT={}, _gAtt=new WeakMap(), _gMag=new WeakMap(); // (weak maps, not userData: userData is copied as JSON when a model is cloned)
const KIT_GRIP=new Set(['ar','smg','mg','burst','heavyar','infantry','dmr','tac','ssmg','lmg','sniper','hunting']), KIT_SIGHT=new Set(['ar','smg','mg','burst','heavyar','infantry','tac','ssmg','lmg','csmg','heavysg','dmr']),
  KIT_BRAKE=new Set(['ar','smg','mg','burst','heavyar','infantry','dmr','ssmg','lmg','sniper','hunting','csmg']), KIT_SCOPE_OWN=new Set(['sniper','hunting']);
const gunSrc=(r,mdl)=>r[mdl==='ar'?'gun':mdl], gunMuz=(r,mdl)=>r['muzzle_'+mdl]||(mdl==='pump'?r.muzzlePump:r.muzzleAR), gunMagG=(r,mdl)=>mdl==='ar'?r.arMag:r['magG_'+mdl]||null;
const pathOf=(root,o)=>{ const p=[]; while(o&&o!==root){ const par=o.parent; if(!par) return null; p.unshift(par.children.indexOf(o)); o=par; } return o===root?p:null; }, atPath=(root,p)=>{ let o=root; for(const i of p){ o=o&&o.children[i]; } return o; };
// where kit goes, measured once per model on the template: the top of the receiver (sight), the underside of the
// handguard (grip), the side of the handguard (laser), the muzzle, and the top of the magazine
function gunAttSpots(G,mdl,muz,mag){ if(GUN_ATT[mdl]) return GUN_ATT[mdl]; G.updateMatrixWorld(true); const inv=new THREE.Matrix4().copy(G.matrixWorld).invert(), M=new THREE.Matrix4(), v=new THREE.Vector3(), meshes=[];
  // (the gun's parts are merged into a few meshes: cast rays at them, in the gun's own space)
  G.traverse(o=>{ if(!o.isMesh||!o.geometry||o.userData.att||o.material===inkMat) return; let p=o; while(p&&p!==G){ if(p===mag) return; p=p.parent; } meshes.push(o); });
  const rc=new THREE.Raycaster(), hit=(o,d)=>{ const O=G.localToWorld(new THREE.Vector3(...o)), D=G.localToWorld(new THREE.Vector3(...o).add(new THREE.Vector3(...d))).sub(O).normalize(); rc.set(O,D); rc.far=5; const h=rc.intersectObjects(meshes,false)[0]; return h?G.worldToLocal(h.point.clone()):null; };
  const my=muz?muz.y:-0.5, at=y=>{ const t=hit([0,y,-1],[0,0,1]), b=hit([0,y,1],[0,0,-1]); const zm=t&&b?(t.z+b.z)/2:null, sd=zm!=null?hit([1,y,zm],[-1,0,0]):null; return {top:t&&t.z,bot:b&&b.z,side:sd&&sd.x,zm}; };
  let magTop=null; if(mag){ mag.updateMatrixWorld(true); mag.traverse(o=>{ if(!o.isMesh||!o.geometry||o.material===inkMat) return; M.multiplyMatrices(inv,o.matrixWorld); const pa=o.geometry.attributes.position; for(let i=0;i<pa.count;i++){ v.fromBufferAttribute(pa,i).applyMatrix4(M); magTop=magTop==null?v.z:Math.min(magTop,v.z); } }); }
  const s=at(my*0.3), h=at(my*0.62);
  return GUN_ATT[mdl]={sight:s.top==null?null:[0,my*0.3,s.top],grip:h.bot==null?null:[0,my*0.62,h.bot],laser:h.side==null?null:[h.side,my*0.62,h.zm],muz:muz?[muz.x,muz.y,muz.z]:null,magTop}; }
function gunAttach(G,mdl){ let A=_gAtt.get(G); if(A) return A; A={}; _gAtt.set(G,A); const at=GUN_ATT[mdl]; if(!at) return A; G.children.filter(c=>c.userData.att).forEach(c=>G.remove(c)); // (a clone brings its template's kit along: start clean)
  const mk=(geo,mat,x,y,z,rx)=>{ const m=new THREE.Mesh(geo,mat); m.position.set(x,y,z); if(rx) m.rotation.x=rx; m.userData.att=true; m.castShadow=true; return m; }, kit=(spot)=>{ const g=new THREE.Group(); g.position.set(...spot); g.userData.att=true; G.add(g); return g; };
  const blk=toon(0x1d2127), pol=toon(0x2b3038), stl=toon(0x585f69);
  if(at.grip&&KIT_GRIP.has(mdl)){ // uncommon: angled foregrip (a wedge); rare up: a vertical grip with finger ridges
    const afg=kit(at.grip); afg.add(mk(rbox(0.026,0.1,0.016,0.004),pol,0,0,0.008)); { const w=mk(rbox(0.024,0.075,0.03,0.006),pol,0,0.012,0.025); w.rotation.x=-0.55; afg.add(w); } A.afg=afg;
    const vg=kit(at.grip); vg.add(mk(rbox(0.026,0.05,0.016,0.004),pol,0,0,0.008)); vg.add(mk(new THREE.CylinderGeometry(0.014,0.016,0.085,12).rotateX(Math.PI/2),pol,0,0,0.055));
    for(const z of [0.04,0.06,0.08]) vg.add(mk(new THREE.TorusGeometry(0.0155,0.0025,6,14),blk,0,0,z)); vg.add(mk(new THREE.CylinderGeometry(0.018,0.018,0.008,12).rotateX(Math.PI/2),blk,0,0,0.1)); A.vg=vg; }
  if(at.sight&&KIT_SIGHT.has(mdl)&&mdl!=='ar'){ // red dot: a low mount, an open hood with a tinted lens and the dot
    const rd=kit(at.sight); rd.add(mk(rbox(0.034,0.07,0.012,0.003),blk,0,0,-0.006));
    rd.add(mk(rbox(0.038,0.012,0.04,0.004),blk,0,-0.02,-0.03)); for(const sx of [-1,1]) rd.add(mk(rbox(0.006,0.03,0.04,0.002),blk,sx*0.016,-0.008,-0.03)); rd.add(mk(rbox(0.038,0.03,0.006,0.002),blk,0,-0.008,-0.052));
    rd.add(mk(new THREE.PlaneGeometry(0.026,0.03),new THREE.MeshPhongMaterial({color:0x7fd0ff,transparent:true,opacity:0.45,specular:0xffffff,shininess:120,side:THREE.DoubleSide}),0,-0.02,-0.03,Math.PI/2));
    rd.add(mk(new THREE.SphereGeometry(0.003,6,4),new THREE.MeshBasicMaterial({color:0xff2020}),0,-0.018,-0.03)); A.dot=rd; }
  if(at.sight&&(KIT_SIGHT.has(mdl)||mdl==='ar')&&!KIT_SCOPE_OWN.has(mdl)){ // legendary: a scope on rings
    const sc=kit([at.sight[0],at.sight[1],at.sight[2]-(mdl==='ar'?0.03:0)]); for(const y of [-0.03,0.03]) sc.add(mk(rbox(0.026,0.014,0.03,0.003),blk,0,y,-0.012));
    sc.add(mk(new THREE.CylinderGeometry(0.018,0.018,0.17,16),blk,0,0,-0.04)); for(const [y,r] of [[-0.09,0.025],[0.08,0.022]]) sc.add(mk(new THREE.CylinderGeometry(r,0.018,0.035,16),blk,0,y,-0.04));
    sc.add(mk(new THREE.CylinderGeometry(0.008,0.008,0.016,10).rotateX(Math.PI/2),stl,0,0,-0.062)); sc.add(mk(new THREE.CylinderGeometry(0.008,0.008,0.016,10).rotateZ(Math.PI/2),stl,0.024,0,-0.04));
    sc.add(mk(new THREE.CircleGeometry(0.023,16),LENS_MAT,0,-0.1076,-0.04,Math.PI/2)); A.scope=sc; }
  if(at.muz&&KIT_BRAKE.has(mdl)){ // epic: a squat brake with ports; legendary: a long ported compensator
    const br=kit([at.muz[0],at.muz[1]+0.03,at.muz[2]]); br.add(mk(new THREE.CylinderGeometry(0.016,0.016,0.06,14),blk,0,0,0)); for(const y of [-0.012,0.012]) br.add(mk(new THREE.BoxGeometry(0.036,0.008,0.012),blk,0,y,0)); A.brake=br;
    const cp=kit([at.muz[0],at.muz[1],at.muz[2]]); cp.add(mk(new THREE.CylinderGeometry(0.019,0.017,0.13,16),blk,0,-0.04,0)); for(let i=0;i<4;i++) cp.add(mk(new THREE.BoxGeometry(0.008,0.012,0.042),stl,0,-0.08+i*0.026,0)); cp.add(mk(new THREE.TorusGeometry(0.019,0.003,6,16).rotateX(Math.PI/2),stl,0,-0.105,0)); A.comp=cp; }
  if(at.laser&&KIT_GRIP.has(mdl)){ const lz=kit(at.laser); lz.add(mk(rbox(0.022,0.06,0.03,0.004),blk,0.011,0,0)); lz.add(mk(new THREE.CylinderGeometry(0.006,0.006,0.008,10),new THREE.MeshBasicMaterial({color:0x5dff7a}),0.014,-0.032,0.005)); A.laser=lz; }
  return A; }
function applyGunKit(G,mdl,rarity,tmplRig){
  if(!G) return; const T0=gunSrc(tmplRig,mdl), muz=gunMuz(tmplRig,mdl), mg0=gunMagG(tmplRig,mdl); if(!T0) return; gunAttSpots(T0,mdl,muz&&muz.parent===T0?muz.position:null,mg0);
  const A=gunAttach(G,mdl), ri=RARITIES.indexOf(rarity), on=(o,v)=>{ if(o) o.visible=!!v; };
  on(A.afg,ri===1); on(A.vg,ri>=2); on(A.dot,ri===2||ri===3); on(A.scope,ri===4); on(A.brake,ri===3); on(A.comp,ri===4); on(A.laser,ri===4);
  // the magazine: longer from epic up (stretched down from its top, so it stays seated)
  const at=GUN_ATT[mdl]; if(mg0&&at&&at.magTop!=null){ const p=pathOf(T0,mg0), mg=p&&atPath(G,p); if(mg){ let o=_gMag.get(mg); if(!o){ o={z:mg.position.z,s:mg.scale.z}; _gMag.set(mg,o); }
    const k=ri===4?1.45:ri===3?1.28:1; mg.scale.z=o.s*k; mg.position.z=o.z+(at.magTop-o.z)*(1-k); } } }

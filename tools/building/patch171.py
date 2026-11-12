# patch171: new trees (see trees.js): stylised alders and pines from leaf cards and curving limbs, one draw per tree
# kind, and picture-on-cards impostors for the middle and far distance (so the far forest matches the near trees and
# costs a fraction of the old blob models).
TREES_JS=open('/home/claude/mg/trees.js').read()
rep("""/* ---------- the forest ----------""",TREES_JS+"""
/* ---------- the forest ----------""")
rep("""function propVariant(kind,variant){ const key=kind+variant; let v=propGeos.get(key); if(v) return v;""",
    """function propVariant(kind,variant){ const key=kind+variant; let v=propGeos.get(key); if(v) return v;
  if(kind==='tree'||kind==='pine'){ v=treeVariant(kind,variant); propGeos.set(key,v); return v; }""")
rep("""const NEAR_TREE=130, FAR_TREE=1500;""","""const NEAR_TREE=115, MID_TREE=290, FAR_TREE=1500;""")
rep("""  for(const kind of ['tree','pine']){ const n=trees.filter(p=>p.kind===kind).length;
    FOREST.near[kind]=[...Array(8)].map((_,v)=>{ const V=propVariant(kind,v); return mk(V.geo,V.mat,trees.filter(p=>p.kind===kind&&p.id%8===v).length,true); });
    FOREST.far[kind]=[...Array(4)].map((_,v)=>mk(farTreeGeo(kind,v),propVariant(kind,0).mat,trees.filter(p=>p.kind===kind&&p.id%4===v).length,false));
    FOREST.mid[kind]=FOREST.far[kind].map(f=>{ const m=mk(f.geometry,f.material,f.instanceMatrix.count,true); m.customDepthMaterial=midDepth; return m; }); }""",
    """  buildImpostors(); const impDepth=IMP.depth.clone(); impDepth.onBeforeCompile=midDepth.onBeforeCompile; // middle trees shadow only into the wide shadow map
  for(const kind of ['tree','pine']){ const cnt=v=>trees.filter(p=>p.kind===kind&&p.id%8===v).length;
    FOREST.near[kind]=[...Array(8)].map((_,v)=>{ const V=propVariant(kind,v), m=mk(V.geo,V.mat,cnt(v),true); m.customDepthMaterial=V.depth; return m; });
    FOREST.mid[kind]=[...Array(8)].map((_,v)=>{ const m=mk(impostorGeo(kind,v,3),IMP.mat,cnt(v),true); m.customDepthMaterial=impDepth; return m; });
    FOREST.far[kind]=[...Array(8)].map((_,v)=>mk(impostorGeo(kind,v,2),IMP.mat,cnt(v),false)); }""")
rep("""function stepForest(dt){ if(!FOREST.near) return; FOREST.t-=dt;""","""function stepForest(dt){ TREE_U.time.value=performance.now()/1000; if(!FOREST.near) return; FOREST.t-=dt;""")
rep("""    if(d2<N2) push(FOREST.near[p.kind][p.id%8],p); else if(d2<46000) push(FOREST.mid[p.kind][p.id%4],p); else if(d2<420000||(d2<1000000?p.id%2===0:p.id%3===0)) push(FOREST.far[p.kind][p.id%4],p); }""",
    """    if(d2<N2) push(FOREST.near[p.kind][p.id%8],p); else if(d2<MID_TREE*MID_TREE) push(FOREST.mid[p.kind][p.id%8],p); else if(d2<420000||(d2<1000000?p.id%2===0:p.id%3===0)) push(FOREST.far[p.kind][p.id%8],p); }""")
rep("""function treeMesh(p){ if(p.g.children.length) return p.g.children[0]; const V=propVariant(p.kind,p.id%8), m=new THREE.Mesh(V.geo,V.mat); m.castShadow=m.receiveShadow=true;""",
    """function treeMesh(p){ if(p.g.children.length) return p.g.children[0]; const V=propVariant(p.kind,p.id%8), m=new THREE.Mesh(V.geo,V.mat); m.castShadow=m.receiveShadow=true; if(V.depth) m.customDepthMaterial=V.depth;""")
# a chopped tree doesn't shrink away: it tips over, crashes down in a burst of leaves, and the fallen trunk sinks into the ground
rep("""function propBreak(p,quiet){
  if(!p.alive) return; p.alive=false; p.hp=0; p.respawnT=35+Math.random()*45; p.grow=1; p.dying=0.35;""","""function propBreak(p,quiet){
  if(!p.alive) return; p.alive=false; p.hp=0; p.respawnT=35+Math.random()*45; p.grow=1; p.dying=0.35;
  if(p.lazy){ p.dying=TREE_FALL; p.landed=false; p.yaw0=p.g.rotation.y; const a=(typeof P!=='undefined'&&Math.hypot(P.pos.x-p.x,P.pos.z-p.z)<12)?Math.atan2(p.x-P.pos.x,p.z-P.pos.z):((p.id*2.399)%6.283); p.fallA=a; }""")
rep("""    if(p.dying>0){ p.dying-=dt; const k=Math.max(0.01,p.dying/0.35); p.g.scale.setScalar(p.s*k); if(p.dying<=0) p.g.visible=false; }""",
    """    if(p.dying>0&&p.lazy){ p.dying-=dt; treeFall(p); if(p.dying<=0){ p.g.visible=false; p.g.position.y=p.base; p.g.rotation.set(0,p.yaw0||0,0); } }
    else if(p.dying>0){ p.dying-=dt; const k=Math.max(0.01,p.dying/0.35); p.g.scale.setScalar(p.s*k); if(p.dying<=0) p.g.visible=false; }""")
rep("""    if(p.wob>0){ p.wob=Math.max(0,p.wob-dt*4);""","""    if(p.wob>0&&!(p.dying>0)){ p.wob=Math.max(0,p.wob-dt*4);""")
rep("""function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true;""","""function propRevive(p){ p.alive=true; p.hp=p.maxHp; p.grow=0; p.dying=0; p.g.visible=true; if(p.lazy){ p.g.position.y=p.base; p.g.rotation.set(0,p.yaw0!=null?p.yaw0:p.g.rotation.y,0); }""")
rep("""let propCullT=0;""","""let propCullT=0;
const TREE_FALL=2.3, _tfQ=new THREE.Quaternion(), _tfY=new THREE.Quaternion(), _tfA=new THREE.Vector3();
function treeFall(p){ const e=TREE_FALL-Math.max(0,p.dying), T1=1.25;
  const ang=e<T1?Math.PI/2*Math.pow(e/T1,2.2):Math.PI/2-0.08*Math.exp(-(e-T1)*9)*Math.abs(Math.sin((e-T1)*22)); // speeding up as it goes, a little bounce on landing
  _tfA.set(Math.cos(p.fallA),0,-Math.sin(p.fallA)); _tfQ.setFromAxisAngle(_tfA,ang); _tfY.setFromAxisAngle(new THREE.Vector3(0,1,0),p.yaw0||0); p.g.quaternion.copy(_tfQ).multiply(_tfY);
  if(e>=T1&&!p.landed){ p.landed=true; const h=5*p.s, x=p.x+Math.sin(p.fallA)*h*0.75, z=p.z+Math.cos(p.fallA)*h*0.75, at=new THREE.Vector3(x,p.base+0.6,z);
    burst(at,26,7,0.3,p.kind==='pine'?leafMatPine:leafMat); burst(at,12,4,0.22,dustMat); if(at.distanceTo(P.pos)<90) sfxAt('break_wood',at); }
  p.g.position.y=p.base-(e>T1+0.45?(e-T1-0.45)/(TREE_FALL-T1-0.45)*1.6*p.s:0); } // then the trunk settles into the ground
const leafMat=new THREE.MeshBasicMaterial({color:0x8fc24a}), leafMatPine=new THREE.MeshBasicMaterial({color:0x4f8a52});""")
rep("""  else if(!moving&&p.g.parent){ scene.remove(p.g); p.g.scale.set(p.s,p.s*(p.hs||1),p.s); p.g.rotation.x=p.g.rotation.z=0;""","""  else if(!moving&&p.g.parent){ scene.remove(p.g); p.g.scale.set(p.s,p.s*(p.hs||1),p.s); p.g.position.y=p.base; p.g.rotation.set(0,p.yaw0!=null?p.yaw0:p.g.rotation.y,0);""")

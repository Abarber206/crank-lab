/* ---------- the horde: Austin's purple creatures ----------
   After his drawing: no eyes, a head that rises into a crown of flame, and ragged holes torn right through them.
   The holes, the face and the flame tips burn from inside (they light up at dusk and read from across a field).
   Every creature hunches forward on bent legs, its head jutting out and its long blade arms hanging low with hooked
   claws. The skin is mottled and veined, darkest at the hands and feet, with a bony ridge down the back.
   The three kinds look and move differently:
     Walkers (husk)   hunched and lurching, dragging their right leg
     Runners          skinny and crouched almost on all fours, arms reaching to the ground like front legs
     Brutes           huge humped shoulders, a small head, spiked shoulders and a molten orange glow
     Hurlers          a cluster of glowing growths on the right shoulder; they tear chunks off and lob them at you
   Every creature also gets its own random layout of holes and veins (picked by its id, the same on every screen). */
const ZATK=0.62, ZSTRIKE=0.3; // an attack: 0.32 s wind-up (rear back, arms up), then a 0.3 s lunge that rakes down
let zScreechAt=0;
const zGlowMats=new Map();
function zGlowM(c,amt){ const k=c+':'+amt; let m=zGlowMats.get(k); if(!m){ m=new THREE.MeshPhongMaterial({color:c}); m.userData.part=true; m.userData.glow=amt; zGlowMats.set(k,m); } return m; }
function makeZombie(type,variant){
  const T=ZT[type], g=new THREE.Group(); g.rotation.order='YXZ'; variant=(variant|0)%8;
  const part=(geo,mat,parent,x=0,y=0,z=0)=>{ const m=new THREE.Mesh(geo,typeof mat==='number'?toon(mat):mat); m.position.set(x,y,z); parent.add(m); return m; };
  const grp=(parent,x=0,y=0,z=0)=>{ const q=new THREE.Group(); q.position.set(x,y,z); parent.add(q); return q; };
  const aux=[], sub=(parent,x,y,z)=>{ const q=grp(parent,x,y,z); aux.push(q); return q; }; // helper groups, folded into their joint before baking
  const R={type}, brute=type==='brute', thin=type==='runner', hurl=type==='hurler', body=T.body, light=T.light, dark=T.dark;
  const wound=zGlowM(T.wound,0.7), core=zGlowM(T.core,1), flameLow=zGlowM(T.light,0.28), claw=T.claw, vein=T.vein;
  const ls=makeZombie.ls||(makeZombie.ls=new THREE.SphereGeometry(.5,10,7));
  const rnd=seeded(7919*(variant+1)+ZCODE.indexOf(type)*104729);
  // mottled skin: soft blotches and darker patches, baked into the vertex colours
  const sd=rnd()*100, mott=(x,y,z)=>(Math.sin(x*23+sd)+Math.sin(y*19+sd*1.3)+Math.sin(z*29+sd*.7)+Math.sin((x-y)*31+sd*2.1)+Math.sin((y+z)*17+sd*.4))/5;
  const tint=(gg,ext)=>{ const pa=gg.attributes.position, C=new Float32Array(pa.count*3);
    for(let i=0;i<pa.count;i++){ const x=pa.getX(i), y=pa.getY(i), z=pa.getZ(i); let m=0.9+0.16*mott(x,y,z); if(mott(x*2.3+5,y*2.3,z*2.3)>0.42) m*=0.74; if(ext) m*=ext(x,y,z);
      C[i*3]=C[i*3+1]=C[i*3+2]=m; }
    gg.setAttribute('color',new THREE.BufferAttribute(C,3)); return gg; };
  // a body of revolution, flattened front to back, optionally curved; the profile is subdivided so the skin has detail
  const dense=prof=>{ const o=[prof[0]]; for(let i=1;i<prof.length;i++){ const [r0,y0]=prof[i-1], [r1,y1]=prof[i], n=Math.max(1,Math.ceil(Math.abs(y1-y0)/0.045)); for(let k=1;k<=n;k++) o.push([r0+(r1-r0)*k/n,y0+(y1-y0)*k/n]); } return o; };
  const lathe=(prof,sz,seg,bend,ext)=>{ const gg=new THREE.LatheGeometry(dense(prof).map(([r,y])=>new THREE.Vector2(Math.max(r,0.0005),y)),seg||18); gg.scale(1,1,sz||1);
    if(bend){ const pa=gg.attributes.position; for(let i=0;i<pa.count;i++){ const y=pa.getY(i); pa.setZ(i,pa.getZ(i)+bend[0]*y*y); pa.setX(i,pa.getX(i)+bend[1]*y*y); } }
    gg.computeVertexNormals(); return ext===false?gg:tint(gg,ext); };
  const rAt=(prof,y)=>{ for(let i=1;i<prof.length;i++){ const [r0,y0]=prof[i-1], [r1,y1]=prof[i]; if((y>=y0&&y<=y1)||(y<=y0&&y>=y1)){ const t=(y-y0)/((y1-y0)||1); return r0+(r1-r0)*t; } } return prof[prof.length-1][0]; };
  // a hole: a ragged dark rim around a glowing hollow, with a white-hot slit deep inside; its front (-z) faces out
  const gash=(parent,x,y,z,w,h,ry,rz)=>{ const o=sub(parent,x,y,z); o.rotation.set(0,ry||0,rz||0);
    part(ls,dark,o,0,0,0).scale.set(w*1.08,h*1.06,w*0.3);
    const rim2=part(ls,dark,o,w*0.3*(rnd()-.5),-h*0.14,0); rim2.scale.set(w*(0.6+rnd()*0.35),h*(0.7+rnd()*0.3),w*0.3); rim2.rotation.z=(rnd()-.5)*1.4;
    part(ls,wound,o,0,0,-w*0.05).scale.set(w*0.7,h*0.8,w*0.26);
    const slit=part(ls,core,o,0,-h*0.04,-w*0.09); slit.scale.set(w*0.24,h*0.62,w*0.22); slit.rotation.z=(rnd()-.5)*0.5; };
  const gashOn=(parent,prof,sz,y,a,w,h)=>{ const r=rAt(prof,y), nx=Math.sin(a), nz=-Math.cos(a)*sz, nl=Math.hypot(nx,nz)||1;
    gash(parent,nx*r*0.97,y,nz*r*0.97,w,h,Math.atan2(-nx/nl,-nz/nl),(rnd()-.5)*1.2); };
  // a dark vein winding over a lathe surface from y0 to y1
  const veinOn=(parent,prof,sz,y0,y1,a0,rad)=>{ const pts=[]; let a=a0; const n=7;
    for(let i=0;i<=n;i++){ const y=y0+(y1-y0)*i/n, r=rAt(prof,y)+rad*0.6; a+=(rnd()-.5)*0.5; pts.push(new THREE.Vector3(Math.sin(a)*r,y,-Math.cos(a)*r*sz)); }
    part(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts),12,rad,4,false),vein,parent); };
  const mirrorX=gg=>{ gg.scale(-1,1,1); const sw=(a,n)=>{ const A=a.array; for(let i=0;i<a.count;i+=3) for(let k=0;k<n;k++){ const t=A[(i+1)*n+k]; A[(i+1)*n+k]=A[(i+2)*n+k]; A[(i+2)*n+k]=t; } };
    for(const k of ['position','normal','uv']) if(gg.attributes[k]) sw(gg.attributes[k],gg.attributes[k].itemSize); gg.computeVertexNormals(); return gg; };
  // the shape of each kind
  const K=brute?{G:1.45,hip:1.0,tilt:-0.4,head:0.26,hs:0.66,sh:1.55,L:1.3,W:.24,knee:.13,spikes:4}
         :thin? {G:.8,hip:.8,tilt:-1.02,head:0.86,hs:.92,sh:1,L:1.32,W:.1,knee:.3,spikes:6}
         :hurl? {G:1.05,hip:1.0,tilt:-0.42,head:0.3,hs:.95,sh:1.12,L:1.16,W:.15,knee:.16,spikes:2}
         :      {G:1,hip:1.0,tilt:-0.5,head:0.34,hs:1,sh:1.05,L:1.18,W:.13,knee:.16,spikes:3};
  const G=K.G; R.hipY=K.hip; R.tilt=K.tilt; R.headTilt=K.head;
  R.hips=grp(g,0,K.hip,0);
  part(lathe([[0,-.13],[.07*G,-.12],[.122*G,-.04],[.126*G,.06],[.115*G,.14]],.7),body,R.hips);
  // legs: a thigh down to a knee bent forward, then a long shin that narrows to a needle point on the ground
  R.legL=grp(R.hips,-.075*G,-.06,0); R.legR=grp(R.hips,.075*G,-.06,0);
  const kneeY=-(K.hip-.06)*0.5, footY=-(K.hip-.06), lt=Math.hypot(kneeY,K.knee), lsn=Math.hypot(footY-kneeY,K.knee+.03);
  const thP=[[0,.04],[.085*G,.02],[.09*G,-.08],[.078*G,-lt*.6],[.064*G,-lt]], shP=[[.062*G,0],[.055*G,-lsn*.3],[.04*G,-lsn*.65],[.02*G,-lsn*.9],[.003,-lsn]];
  const dk=(len)=>(x,y)=>1-0.42*Math.pow(Math.min(1,Math.max(0,-y/len)),1.4);
  for(const [Lg,s] of [[R.legL,-1],[R.legR,1]]){
    const th=sub(Lg,0,0,0); th.rotation.x=Math.asin(K.knee/lt); part(lathe(thP,.86,14,null,(x,y)=>1-0.12*Math.min(1,-y/lt)),body,th);
    part(ls,body,Lg,0,kneeY,-K.knee).scale.set(.13*G,.13*G,.12*G);
    const sh=sub(Lg,0,kneeY,-K.knee); sh.rotation.x=-Math.asin((K.knee+.03)/lsn);
    part(lathe(shP,.86,12,[0,s*-0.02],(x,y)=>0.88*dk(lsn)(x,y)),body,sh);
    if(rnd()<0.7) veinOn(sh,shP,.86,-.05,-lsn*.6,(rnd()-.5)*1.4,.006*G); }
  // torso: narrow waist, a long chest, wide (Brutes: huge) shoulders, into a neck that juts forward
  R.spine=grp(R.hips,0,.12,0); R.spine.rotation.x=K.tilt;
  const S=K.sh, tprof=[[.112*G,-.1],[.118*G,0],[.125*G,.1],[.15*G*(1+(S-1)*.4),.26],[.19*G*S,.42],[.21*G*S,.52],[.18*G*S,.6],[.11*G,.68],[.07*G,.74],[.06*G,.82]];
  part(lathe(tprof,.62,22),body,R.spine).castShadow=true;
  if(brute){ part(ls,body,R.spine,0,.55,.1*G).scale.set(.55*G,.36*G,.34*G); // the hump between the shoulders
    for(const s of [-1,1]) for(let q=0;q<2;q++){ const sp=sub(R.spine,s*(.2+q*.08)*G*S,.6-q*.05,.02); sp.rotation.set(-.2,0,-s*(.5+q*.35)); part(lathe([[.045*G,0],[.025*G,.1],[.002,.2+q*.04]],1,7,null,false),dark,sp); } }
  if(hurl){ // the growths it throws: swollen, glowing pods bulging off the right shoulder and upper back
    for(let q=0;q<7;q++){ const r=(.06+rnd()*.05)*G, a=0.5+q*0.32+(rnd()-.5)*.2, y=.42+rnd()*.24, rr=rAt(tprof,y);
      const px=Math.sin(a)*rr*.95, pz=-Math.cos(a)*rr*.62*.95, o=sub(R.spine,px,y,pz); o.rotation.y=Math.atan2(-px,-pz);
      part(ls,body,o,0,0,0).scale.set(r*2.1,r*2,r*1.4); part(ls,dark,o,0,0,-r*.62).scale.set(r*1.5,r*1.45,r*.7);
      part(ls,wound,o,0,0,-r*.7).scale.set(r*1.2,r*1.15,r*.6); part(ls,core,o,0,r*.1,-r*.82).scale.set(r*.55,r*.5,r*.4); } }
  // a bony ridge of spikes down the back, pointing back and up
  for(let q=0;q<K.spikes;q++){ const y=.18+q*(.5/K.spikes), r=rAt(tprof,y)*.62, sp=sub(R.spine,0,y,r*.9); sp.rotation.x=1.05+q*.05;
    part(lathe([[.03*G,0],[.016*G,.06],[.002,.1+(brute?.05:0)+(thin?.03:0)]],1,6,null,false),dark,sp); }
  for(let q=0,n=brute?5:thin?4:3;q<n;q++) veinOn(R.spine,tprof,.62,.02+rnd()*.15,.38+rnd()*.3,(rnd()-.5)*2.4,.007*G);
  // head: a long neck-head that narrows up into the flames; a big dark hole burning in the face instead of eyes
  R.head=grp(R.spine,0,.8,-.03); R.head.rotation.set(K.head,0,.06); R.head.scale.setScalar(K.hs);
  const hprof=[[.062*G,-.02],[.085*G,.05],[.096*G,.14],[.088*G,.25],[.07*G,.36],[.048*G,.48],[.026*G,.6],[.008,.72],[.001,.78]];
  part(lathe(hprof,.85,16,[0.05,0.07]),body,R.head);
  gashOn(R.head,hprof,.85,.16+rnd()*.05,(rnd()-.5)*0.5,.13,.11+rnd()*.04);
  if(rnd()<0.5) gashOn(R.head,hprof,.85,.3+rnd()*.06,(rnd()<.5?-1:1)*(.6+rnd()*.5),.06,.07);
  R.jaw=grp(R.head,0,.05,-.02);
  // the flame crown: curling licks lit from within, burning white-hot at the tips
  R.crown=grp(R.head,0,.12,0);
  const fl=brute?[[0,.78,.085,0,-.12],[.06,.62,.07,.34,.06],[-.065,.66,.07,-.38,.1],[.05,.46,.055,.66,-.04],[-.055,.48,.055,-.7,-.08],[.02,.4,.06,.18,.26],[-.02,.36,.05,-.22,-.3],[.0,.3,.05,.05,.4]]
               :[[0,.7,.07,0,-.1],[.05,.55,.06,.32,.05],[-.055,.58,.06,-.38,.08],[.04,.4,.045,.64,-.04],[-.045,.42,.045,-.68,-.06],[0,.34,.05,.16,.24],[.0,.3,.045,-.1,-.32]];
  fl.forEach(([x,h,r,lz,lx],q)=>{ const f=sub(R.crown,x*G,.0,q%2?.015:-.01); f.rotation.set(lx,0,lz);
    const prof=[]; for(let i=0;i<=8;i++){ const t=i/8; prof.push([r*G*(1-t)*(1+0.4*Math.sin(t*Math.PI)),h*t]); }
    const cg=lathe(prof,.72,9,null,false), pa=cg.attributes.position, ph=rnd()*6;
    for(let i=0;i<pa.count;i++){ const t=pa.getY(i)/h; pa.setX(i,pa.getX(i)+Math.sin(t*4.5+ph)*0.05*t*t*h/.5); pa.setZ(i,pa.getZ(i)+Math.cos(t*3.5+ph)*0.025*t*t); }
    cg.computeVertexNormals(); part(cg,q===0?body:flameLow,f);
    const tp=[]; for(let i=0;i<=5;i++){ const t=i/5; tp.push([r*G*.5*(1-t),h*(0.58+0.42*t)]); }
    const tg=lathe(tp,.72,7,null,false), tpa=tg.attributes.position; for(let i=0;i<tpa.count;i++){ const t=tpa.getY(i)/h; tpa.setX(i,tpa.getX(i)+Math.sin(t*4.5+ph)*0.05*t*t*h/.5); } tg.computeVertexNormals();
    part(tg,core,f); });
  const glow=new THREE.Mesh(new THREE.SphereGeometry(.5,12,8),new THREE.MeshBasicMaterial({color:T.core,transparent:true,opacity:.16,blending:THREE.AdditiveBlending,depthWrite:false}));
  glow.scale.set(.16,.36,.14); glow.position.set(0,.36,0); glow.renderOrder=3; R.crown.add(glow); R.crownGlow=glow;
  // arms: long slim blades hanging low from the shoulders, a notch in the edge, three hooked claws at the end
  R.armL=grp(R.spine,-.19*G*S,.6,0); R.armR=grp(R.spine,.19*G*S,.6,0);
  R.armL0=R.armR0=-K.tilt*0.92+(thin?0.15:0.12); // hang down (a little forward) whatever the hunch
  const L=K.L, Wd=K.W, th=brute?.026:.016, U=L*0.48, F=L-U;
  // each arm: an upper blade from the shoulder to the elbow, and a forearm blade (its own joint) down to the hooked claws
  R.foreL=grp(R.armL,0,-U,0); R.foreR=grp(R.armR,0,-U,0); R.elbow0=thin?0.25:0.32;
  const ex=sh=>{ const g_=new THREE.ExtrudeGeometry(sh,{depth:th,bevelEnabled:true,bevelThickness:.01,bevelSize:.009,bevelSegments:2,curveSegments:8}); g_.translate(0,0,-th/2); return g_; };
  for(const [A,Fo,s] of [[R.armL,R.foreL,-1],[R.armR,R.foreR,1]]){
    const su=new THREE.Shape(); su.moveTo(-.02,.05); su.quadraticCurveTo(Wd*.4,.03,Wd*.6,-.1); su.lineTo(Wd*.92,-U-.04); su.lineTo(-.04,-U-.04); su.lineTo(-.045,-.1); su.lineTo(-.02,.05);
    const sf=new THREE.Shape(); sf.moveTo(-.04,.04); sf.lineTo(Wd*.92,.04); sf.lineTo(Wd,-F*.02); sf.lineTo(Wd*.72,-F*.15); sf.lineTo(Wd*.86,-F*.31);
    sf.quadraticCurveTo(Wd*.66,-F*.77,Wd*.22,-F*.94); sf.lineTo(Wd*.05,-F*.8); sf.quadraticCurveTo(-.02,-F*.4,-.04,.04);
    const vu=new THREE.Shape(); vu.moveTo(0,-.1); vu.quadraticCurveTo(Wd*.45,-U*.6,Wd*.4,-U); vu.lineTo(Wd*.36,-U); vu.quadraticCurveTo(Wd*.37,-U*.6,-.012,-.1);
    const vf=new THREE.Shape(); vf.moveTo(Wd*.4,0); vf.quadraticCurveTo(Wd*.46,-F*.4,Wd*.3,-F*.72); vf.lineTo(Wd*.27,-F*.72); vf.quadraticCurveTo(Wd*.38,-F*.4,Wd*.36,0);
    const bu=ex(su), bf=ex(sf), gu=new THREE.ExtrudeGeometry(vu,{depth:.003,bevelEnabled:false}), gf=new THREE.ExtrudeGeometry(vf,{depth:.003,bevelEnabled:false});
    if(s<0){ mirrorX(bu); mirrorX(bf); mirrorX(gu); mirrorX(gf); }
    tint(bu,(x,y)=>1-0.2*Math.min(1,Math.max(0,-y/U))); tint(bf,(x,y)=>0.8-0.32*Math.pow(Math.min(1,Math.max(0,-y/F)),1.3));
    const fu=sub(A,0,0,0); fu.rotation.y=s*0.28; part(bu,body,fu); part(gu,vein,fu,0,0,-(th/2+.012));
    const ff=sub(Fo,0,0,0); ff.rotation.y=s*0.28; part(bf,body,ff); part(gf,vein,ff,0,0,-(th/2+.012));
    part(ls,body,Fo,s*Wd*.42,0,0).scale.set(Wd*1.05+.04,.12*G,.09*G); // the elbow knuckle, covering the joint
    for(let q=0;q<3;q++){ const c=sub(ff,s*Wd*(.08+q*.07),-F*(.84+q*.03),0); c.rotation.set(-0.5-q*.1,0,s*(q-1)*.25);
      part(lathe([[.016*G,0],[.012*G,-.06],[.006*G,-.13],[.001,-.19-q*.02]],1,6,[-0.9,0],false),claw,c); }
    if(rnd()<(brute?0.9:0.6)){ const up_=rnd()<.5; gash(up_?fu:ff,s*Wd*(.3+rnd()*.3),up_?-U*(.3+rnd()*.5):-F*(.2+rnd()*.45),-(th/2+.01),.06*G,.13+rnd()*.06,0,(rnd()-.5)); } }
  // its own random holes: on the chest and flanks, through the back, and one or two on the legs
  const nT=brute?6:thin?3:4;
  for(let k=0;k<nT;k++){ const front=rnd()<0.7, a=front?(rnd()-.5)*1.6:(rnd()<.5?-1:1)*(1.3+rnd()*1.2), y=.1+rnd()*.5;
    gashOn(R.spine,tprof,.62,y,a,(.09+rnd()*.09)*G,.14+rnd()*.2); }
  for(let k=0,n=rnd()<0.6?1:2;k<n;k++){ const Lg=rnd()<.5?R.legL:R.legR, tp=Lg.children.find(c=>c.rotation&&c.rotation.x>0)||Lg; gashOn(tp,thP,.86,-lt*(.3+rnd()*.4),(rnd()-.5)*1.4,.07*G,.13+rnd()*.08); }
  if(hurl){ // the chunk it is about to throw, shown in its right hand while it winds up
    const lump=new THREE.Mesh(makeZombie.ls,new THREE.MeshBasicMaterial({color:T.core})); lump.scale.setScalar(.2*G); lump.position.set(Wd*.15,-F*.76,-.06); lump.visible=false; R.foreR.add(lump); R.lump=lump; }
  // fold every helper group's meshes into the joint above it (innermost first), so each joint bakes to one mesh
  for(let i=aux.length-1;i>=0;i--){ const q=aux[i], P_=q.parent; q.updateMatrix();
    [...q.children].forEach(c=>{ c.updateMatrix(); c.matrix.premultiply(q.matrix); c.matrix.decompose(c.position,c.quaternion,c.scale); P_.add(c); }); P_.remove(q); }
  // the hitbox, measured from the model at rest (per kind, unscaled): skull, flame base, and spheres up the legs and spine
  if(!T.hit){ R.armL.rotation.set(R.armL0,0,-.12); R.armR.rotation.set(R.armR0,0,.12); R.foreL.rotation.x=R.foreR.rotation.x=R.elbow0; g.updateMatrixWorld(true); // the idle pose
    const head=[], body=[], add=(L,o,x,y,z,r)=>{ const p=o.localToWorld(new THREE.Vector3(x,y,z)); L.push([+p.y.toFixed(3),+(-p.z).toFixed(3),+r.toFixed(3),+p.x.toFixed(3)]); };
    // head: the skull, up the long head, into the flames
    for(const [y,r] of [[.12,.1],[.28,.09],[.46,.095],[.66,.095],[.86,.075]]) add(head,R.head,0,y,0,r*G*K.hs+.02);
    // body: each bent leg, the spine (as wide as the torso there), each arm blade
    for(const Lg of [R.legL,R.legR]) for(let k=0;k<=6;k++){ const t=k/6, y=t<.5?footY+(kneeY-footY)*t*2:kneeY*(1-(t-.5)*2), zz=t<.5?-K.knee*t*2:-K.knee*(1-(t-.5)*2); add(body,Lg,0,y,zz,.1*G); }
    for(let y=-.1;y<=.76;y+=.11) add(body,R.spine,0,y,0,rAt(tprof,y)*.88+.02);
    for(const [A,Fo,s_] of [[R.armL,R.foreL,-1],[R.armR,R.foreR,1]]){ for(let k=1;k<=3;k++) add(body,A,s_*Wd*.45,-U*k/3,0,Math.max(.075,Wd*.7)); for(let k=1;k<=3;k++) add(body,Fo,s_*Wd*.45,-F*k/3.2,0,Math.max(.075,Wd*.7)); }
    if(brute) add(body,R.spine,0,.55,.1*G,.27*G);
    if(hurl) add(body,R.spine,.15*G,.55,0,.15*G);
    T.hit={head,body,top:Math.max(...head.map(h=>h[0]))}; }
  bakeStatic(g,R,'creature:'+type+':'+variant);
  g.scale.setScalar(T.sc); scene.add(g);
  return {g,R};
}

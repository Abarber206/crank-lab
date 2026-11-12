# patch154: a more lifelike body (the humanoid list).
#  Silhouette: sloping shoulders (a trapezius from the neck down to each shoulder); a V-shaped torso (wider chest, a
#  narrower waist above the belt, the lower back curving in); limbs that taper (fuller upper arms and thighs, slimmer
#  knees, ankles, elbows and wrists); a head with a brow ridge, set-in eye sockets, a jaw and a chin.
#  Clothes and gear: the shirt hangs a little over the belt; creases behind the knees and inside the elbows; the
#  trousers bunch where they go into the boots; backpack straps that lie on the chest and over the shoulders (with a
#  contact shadow and buckles) instead of floating boards; boots with a wider toe and a real heel.
#  Materials: matte skin and cloth, a soft sheen on leather (belt, boots, gloves), glassy reflective goggle lenses;
#  darker contact shading under the chin and under the belt.
#  Lighting on the Locker stage: a warm key light, a cool fill, a subtle rim.
#  Posture: standing still the weight settles on one leg (hips tilted one way, shoulders the other), knees and elbows
#  soften, the arms hang a little away from the body and the fingers curl naturally, more towards the little finger.

# --- torso: V-taper and a lower back that curves in
rep("""  pz(organ([[-.045,.146,.096,.104],[.02,.136,.094,.098],[.09,.138,.096,.098],[.16,.146,.1,.102],[.2,.15,.1,.103]],22),C.jacket,rig.spine);""",
"""  pz(organ([[-.045,.146,.096,.104],[.02,.129,.093,.09],[.09,.133,.096,.091],[.16,.146,.1,.1],[.2,.152,.1,.103]],22),C.jacket,rig.spine);
  if(top!=='armor'&&top!=='suit') pz(organ([[.035,.135,.095,.092],[.006,.157,.105,.113],[-.006,.159,.106,.115]],22,1),C.jacket,rig.spine); // the shirt hangs over the belt""")
rep("""  pz(organ([[-.03,.14,.098,.102],[.03,.156,.104,.11],[.09,.17,.11,.118],[.15,.178,.112,.122],[.2,.176,.104,.12],[.235,.15,.088,.108],[.262,.095,.066,.086],[.285,.058,.052,.058]],22),C.jacket,rig.chest);""",
"""  const CHR=[[-.03,.14,.098,.102],[.03,.153,.104,.11],[.09,.176,.11,.118],[.15,.188,.112,.122],[.2,.186,.104,.12],[.235,.157,.088,.108],[.262,.098,.066,.086],[.285,.058,.052,.058]];
  pz(organ(CHR,22),C.jacket,rig.chest);
  [-1,1].forEach(sx=>pz(sph(.07),C.jacket,rig.chest,sx*.1,.243,.012,[0,0,sx*-.42],[1.45,.62,1.05])); // trapezius: the shoulders slope down from the neck""")
# --- backpack straps that lie on the body
rep("""  if(back==='pack'||back==='jetpack'){ part(rbox(.045,.27,.02,.01),C.packD,rig.chest,-.1,.13,-.115,null,null,0.005); part(rbox(.045,.27,.02,.01),C.packD,rig.chest,.1,.13,-.115,null,null,0.005); }""",
"""  if(back==='pack'||back==='jetpack'){ const chAt=y=>{ let i=0; while(i<CHR.length-2&&CHR[i+1][0]<y) i++; const a=CHR[i], b=CHR[i+1], t=Math.max(0,Math.min(1,(y-a[0])/(b[0]-a[0]))); return [a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t,a[3]+(b[3]-a[3])*t]; };
    const shadeC=new THREE.Color(C.jacket).multiplyScalar(.5).getHex();
    [-1,1].forEach(sx=>{ const x=sx*.095, pts=[];
      for(let y=-.02;y<=.235;y+=.025){ const [rx,df]=chAt(y); pts.push(new THREE.Vector3(x,y,-df*Math.sqrt(Math.max(0.05,1-(x/rx)*(x/rx)))-.004)); }
      [[.255,-.066],[.279,-.036],[.291,.002],[.285,.044],[.262,.084],[.232,.114],[.2,.128]].forEach(([y,z])=>pts.push(new THREE.Vector3(sx*.1,y,z)));
      part(strapGeo(pts,.046,.008,.002),C.packD,rig.chest,0,0,0,null,null,0); part(strapGeo(pts,.062,.002,-.0015),shadeC,rig.chest,0,0,0,null,null,0); // the strap, its contact shadow
      const [rx,df]=chAt(.1); part(rbox(.056,.024,.01,.004),C.steel,rig.chest,x,.1,-df*Math.sqrt(Math.max(0.05,1-(x/rx)*(x/rx)))-.012,null,null,0); }); }""")
rep("""function createHero(jacketHex,opts){""","""// a flat strap following points on the body: width w, thickness th, raised off the surface by lift (outwards from the spine)
function strapGeo(pts,w,th,lift){ const P=[], I=[], n=pts.length, T=new THREE.Vector3(), N=new THREE.Vector3(), B=new THREE.Vector3(), c=new THREE.Vector3();
  for(let i=0;i<n;i++){ const a=pts[Math.max(0,i-1)], b=pts[Math.min(n-1,i+1)]; T.subVectors(b,a).normalize(); c.set(pts[i].x*0.35,Math.min(pts[i].y,.2),0); N.subVectors(pts[i],c); N.addScaledVector(T,-N.dot(T)).normalize(); B.crossVectors(T,N).normalize();
    for(const [u,v] of [[-1,0],[1,0],[1,1],[-1,1]]){ const p=pts[i].clone().addScaledVector(B,u*w/2).addScaledVector(N,lift+v*th); P.push(p.x,p.y,p.z); } }
  for(let i=0;i<n-1;i++) for(let k=0;k<4;k++){ const a=i*4+k, b=i*4+(k+1)%4, c2=a+4, d=b+4; I.push(a,c2,b, b,c2,d); }
  I.push(0,1,2, 0,2,3); const e=(n-1)*4; I.push(e,e+2,e+1, e,e+3,e+2);
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); g.setIndex(I); g.computeVertexNormals(); return g; }
function createHero(jacketHex,opts){""")
# --- limbs that taper
rep("""    else pz(organ([[.045,.045,.05,.052],[.02,.06,.062,.064],[-.04,.059,.064,.064],[-.12,.051,.057,.053],[-.2,.046,.049,.047],[-.27,.043,.045,.045],[-.31,.041,.043,.043]],16),C.jacket,sh);""",
"""    else pz(organ([[.045,.045,.05,.052],[.02,.061,.063,.065],[-.04,.062,.066,.066],[-.12,.053,.058,.055],[-.2,.045,.047,.046],[-.27,.04,.042,.042],[-.31,.039,.041,.041]],16),C.jacket,sh);""")
rep("""    pz(organ([[.04,.04,.043,.045],[.0,.043,.045,.048],[-.05,.045,.047,.047],[-.12,.04,.041,.04],[-.19,.033,.032,.031],[-.245,.03,.027,.026]],16),fc,el);""",
"""    pz(organ([[.04,.038,.041,.043],[.0,.04,.042,.045],[-.06,.047,.048,.048],[-.12,.041,.041,.04],[-.19,.032,.031,.03],[-.245,.028,.026,.025]],16),fc,el);
    if(top!=='tee') [[.014,.12],[-.01,-.1]].forEach(([y,a])=>pz(rbox(.042,.004,.008,.002),C.jacketD,el,0,y,-.043,[a,0,0])); // creases inside the elbow""")
rep("""    pz(organ([[.05,.07,.08,.084,sx*.004],[-.03,.081,.09,.097,sx*.003],[-.12,.08,.088,.091,sx*.001],[-.24,.07,.076,.074,-sx*.006],[-.34,.06,.064,.062,-sx*.011],[-.4,.056,.062,.056,-sx*.013],[-.44,.052,.056,.052,-sx*.013]],18),C.pants,hp);""",
"""    pz(organ([[.05,.07,.08,.084,sx*.004],[-.03,.086,.094,.1,sx*.003],[-.12,.083,.09,.093,sx*.001],[-.24,.07,.076,.074,-sx*.006],[-.34,.058,.062,.06,-sx*.011],[-.4,.055,.061,.055,-sx*.013],[-.44,.052,.056,.052,-sx*.013]],18),C.pants,hp);""")
rep("""    pz(organ([[.05,.054,.058,.054,-sx*.013],[.0,.056,.064,.055,-sx*.013],[-.06,.054,.052,.062,-sx*.011],[-.13,.057,.047,.07,-sx*.009],[-.22,.048,.043,.056,-sx*.005],[-.31,.041,.039,.043,-sx*.002],[-.385,.041,.041,.043,0]],18),C.pants,kn);""",
"""    pz(organ([[.05,.054,.058,.054,-sx*.013],[.0,.055,.063,.054,-sx*.013],[-.06,.054,.052,.062,-sx*.011],[-.13,.057,.047,.07,-sx*.009],[-.22,.047,.042,.055,-sx*.005],[-.3,.039,.037,.041,-sx*.002],[-.385,.041,.041,.043,0]],18),C.pants,kn);
    [[.012,.15],[-.012,-.1]].forEach(([y,a])=>pz(rbox(.05,.004,.008,.002),C.pantsD,kn,-sx*.013,y,.052,[a,0,0])); // creases behind the knee
    pz(organ([[-.285,.041,.039,.043,-sx*.002],[-.31,.047,.045,.049,-sx*.001],[-.335,.046,.045,.048,0]],18,1),C.pants,kn); // where the trousers bunch into the boot""")
# --- boots: wider toe box, a real heel
rep("""[.12,.053,.028,.034,0,-.092],[.17,.049,.025,.03,0,-.094],[.2,.037,.02,.022,0,-.096]],16),C.boot,an); // the foot""",
"""[.12,.058,.029,.034,0,-.092],[.17,.057,.026,.031,0,-.094],[.2,.045,.021,.023,0,-.096]],16),C.boot,an); // the foot""")
rep("""    pz(rbox(.108,.022,.292,.01),C.sole,an,0,-.119,-.062); pz(rbox(.098,.016,.085,.006),C.sole,an,0,-.128,.03);""",
"""    pz(rbox(.12,.022,.296,.01),C.sole,an,0,-.119,-.062); pz(rbox(.1,.036,.086,.006),C.sole,an,0,-.112,.032); // the sole, standing out round the boot, and a heel block""")
# --- contact shading: under the chin, under the belt
rep("""  pz(organ([[-.03,.062,.054,.064],[.03,.051,.05,.056],[.09,.047,.05,.054],[.13,.05,.05,.05]],16),C.skin,rig.neck);""",
"""  pz(organ([[-.03,.062,.054,.064],[.03,.051,.05,.056],[.09,.047,.05,.054],[.13,.05,.05,.05]],16),C.skin,rig.neck);
  pz(organ([[.085,.0478,.0508,.0548],[.13,.0508,.0508,.0508]],16,1),new THREE.Color(C.skin).multiplyScalar(.74).getHex(),rig.neck); // shade under the jaw""")
rep("""pz(rbox(.052,.038,.012,.004),C.steel,rig.hips,0,.078,-.103);""","""pz(rbox(.052,.038,.012,.004),C.steel,rig.hips,0,.078,-.103);
  pz(organ([[.056,.1505,.0985,.1085],[.036,.1495,.0975,.1075]],22,1),new THREE.Color(C.pants).multiplyScalar(.55).getHex(),rig.hips); // shade under the belt""")
# --- head: brow ridge, eye sockets, jaw and chin
rep("""      Y-=f*0.006*G(ax,0.08)*G(y+0.9,0.02); }""","""      Y-=f*0.006*G(ax,0.08)*G(y+0.9,0.02);
      Z+=f*(0.008*G(y-0.34,0.006)*G(ax-0.32,0.1)-0.006*G(ax-0.39,0.012)*G(y-0.21,0.005)+0.007*G(ax,0.03)*G(y+0.8,0.012)); } // brow ridge, the hollow under it, the chin
    if(y<-0.25) X*=1-0.08*G(y+0.72,0.03)*(z<0.25?1:0.3); // the jaw narrows to the chin""")
# --- materials
rep("""function gunSurf(c,s){ const k=c+':'+s; let m=surfMats.get(k); if(!m){ m=new THREE.MeshPhongMaterial({color:c,shininess:16,specular:0x1c1c1c}); m.userData.part=true;""",
"""const SURF_LOOK={9:[4,0x070707],10:[5,0x080808],11:[44,0x3a3632],12:[6,0x0c0b0a],13:[26,0x242424]}; // cloth matte; leather a soft sheen; skin matte; hair a little gloss
function gunSurf(c,s){ const k=c+':'+s; let m=surfMats.get(k); if(!m){ const L=SURF_LOOK[s]; m=new THREE.MeshPhongMaterial({color:c,shininess:L?L[0]:16,specular:L?L[1]:0x1c1c1c}); m.userData.part=true;""")
rep("""const lm=new THREE.Mesh(lens,toon(C.lens));""","""const lm=new THREE.Mesh(lens,LENS_MAT); { const gl=new THREE.Mesh(new THREE.CircleGeometry(.007,10),LENS_GLINT); gl.position.set(-.011,.011,.001); lm.add(gl); }""")
rep("""const OUTLINES=false;""","""const OUTLINES=false;
const LENS_MAT=new THREE.MeshPhongMaterial({color:0x1b2c3e,emissive:0x0f2238,specular:0xffffff,shininess:220}), LENS_GLINT=new THREE.MeshBasicMaterial({color:0xe8f6ff,transparent:true,opacity:0.8}); // glassy goggle lenses""")
# --- three-point lighting on the stage
rep("""  const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x2a3a7a,0.75));
  const key=new THREE.DirectionalLight(0xfff4e2,0.95);""","""  const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x2a3a7a,0.5));
  const key=new THREE.DirectionalLight(0xffe0bc,1.12);""")
rep("""  const rim=new THREE.DirectionalLight(0x7fc0ff,0.9); rim.position.set(-3,2.5,4); sc.add(rim); const fill=new THREE.PointLight(0x6aa8ff,0.5,9); fill.position.set(0,0.5,-2.5); sc.add(fill);""",
"""  const rim=new THREE.DirectionalLight(0xcfe6ff,0.5); rim.position.set(-3,2.5,4); sc.add(rim); const fill=new THREE.PointLight(0x6aa8ff,0.22,9); fill.position.set(0,0.5,-2.5); sc.add(fill);
  const fill2=new THREE.DirectionalLight(0x9cbcff,0.42); fill2.position.set(-3.5,1.6,-3); sc.add(fill2); // warm key, cool fill, a subtle rim""")
# --- posture at rest
rep("""      T.knL+=-0.06*Math.max(0,Math.sin(A.t*0.55)); T.knR+=-0.06*Math.max(0,-Math.sin(A.t*0.55));""",
"""      T.knL+=-0.06*Math.max(0,Math.sin(A.t*0.55)); T.knR+=-0.06*Math.max(0,-Math.sin(A.t*0.55));
      { const cp=Math.min(1,A.idleT*1.2); // contrapposto: the weight on the right leg, the left knee eased, the shoulders against the hips
        T.hipsZ+=0.05*cp; T.chZ-=0.055*cp; T.hpLz-=0.05*cp; T.hpRz-=0.05*cp; T.knL-=0.16*cp; T.hpL+=0.06*cp; T.knR-=0.035*cp;
        if(bounceArms){ T.shLz-=0.07*cp; T.shRz+=0.07*cp; T.elL+=0.14*cp; T.elR+=0.14*cp; } }""")
# --- relaxed fingers: each finger a little more curled than the one before it
rep("""const set=(a,name,ty,tz)=>{ const P=HAND_POSE[name], f=a.fj; for(let i=0;i<4;i++){ const q=P[i?1:0]; f.mcp[i].rotation.x+=(q[0]-f.mcp[i].rotation.x)*k; f.pip[i].rotation.x+=(q[1]-f.pip[i].rotation.x)*k; f.dip[i].rotation.x+=(q[2]-f.dip[i].rotation.x)*k; }""",
"""const set=(a,name,ty,tz)=>{ const P=HAND_POSE[name], f=a.fj, rl=name==='relax'?1:0; for(let i=0;i<4;i++){ const q=P[i?1:0], g=rl*i; f.mcp[i].rotation.x+=(q[0]+0.07*g-f.mcp[i].rotation.x)*k; f.pip[i].rotation.x+=(q[1]+0.1*g-f.pip[i].rotation.x)*k; f.dip[i].rotation.x+=(q[2]+0.05*g-f.dip[i].rotation.x)*k; }""")
# shoulders: a lower, smaller cap on top of each arm, so the line runs down the trapezius into the arm instead of a ball
rep("""    else pz(organ([[.045,.045,.05,.052],[.02,.061,.063,.065],""","""    else pz(organ([[.03,.038,.044,.046],[.005,.058,.061,.063],""")
# the jacket's pockets and chest badge sit on the chest's curve instead of standing off it like boxes
rep("""  pz(organ(CHR,22),C.jacket,rig.chest);""","""  pz(organ(CHR,22),C.jacket,rig.chest);
  const chAt=y=>{ let i=0; while(i<CHR.length-2&&CHR[i+1][0]<y) i++; const a=CHR[i], b=CHR[i+1], t=Math.max(0,Math.min(1,(y-a[0])/(b[0]-a[0]))); return [a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t,a[3]+(b[3]-a[3])*t]; };
  const onChest=(x,y,lift)=>{ const [rx,df]=chAt(y), u=Math.min(0.95,Math.abs(x)/rx), s=Math.sqrt(1-u*u); return [-df*s-lift, Math.sign(x)*Math.atan(df*u/(rx*s))]; }; // the front surface at (x,y), and its turn""")
rep("""    [-1,1].forEach(sx=>{ part(rbox(.075,.07,.02,.012),C.jacketL,rig.chest,sx*.11,.07,-.11,null,null,0.004); });""",
"""    [-1,1].forEach(sx=>{ const [z,ry]=onChest(sx*.122,.07,.004); part(rbox(.062,.066,.012,.005),C.jacketL,rig.chest,sx*.122,.07,z,[0,ry,0],null,0.004); });""")
rep("""part(rbox(.08,.06,.02,.015),C.jacketL,rig.chest,.09,.14,-.112,null,null,0.005);""","""{ const [z,ry]=onChest(.088,.15,.004); part(rbox(.07,.055,.012,.006),C.jacketL,rig.chest,.088,.15,z,[0,ry,0],null,0.005); }""")
rep("""  if(back==='pack'||back==='jetpack'){ const chAt=y=>{ let i=0; while(i<CHR.length-2&&CHR[i+1][0]<y) i++; const a=CHR[i], b=CHR[i+1], t=Math.max(0,Math.min(1,(y-a[0])/(b[0]-a[0]))); return [a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t,a[3]+(b[3]-a[3])*t]; };""",
"""  if(back==='pack'||back==='jetpack'){""")
rep("""    [-1,1].forEach(sx=>{ const x=sx*.095, pts=[];""","""    [-1,1].forEach(sx=>{ const x=sx*.07, pts=[];""")
rep("""lm.position.set(sx*.05,.24,-.147);""","""lm.position.set(sx*.05,.2405,-.1505);""")
rep("""const LENS_MAT=new THREE.MeshPhongMaterial({color:0x1b2c3e,emissive:0x0f2238,specular:0xffffff,shininess:220})""","""const LENS_MAT=new THREE.MeshPhongMaterial({color:0x3a6688,emissive:0x173a5c,specular:0xffffff,shininess:200,side:THREE.DoubleSide})""")
rep("""const gl=new THREE.Mesh(new THREE.CircleGeometry(.007,10),LENS_GLINT); gl.position.set(-.011,.011,.001);""","""const gl=new THREE.Mesh(new THREE.CircleGeometry(.008,10),LENS_GLINT); gl.position.set(-.011,.011,.0015); gl.scale.set(1.6,.7,1); gl.rotation.z=.6;""")
rep("""LENS_GLINT=new THREE.MeshBasicMaterial({color:0xe8f6ff,transparent:true,opacity:0.8});""","""LENS_GLINT=new THREE.MeshBasicMaterial({color:0xe8f6ff,transparent:true,opacity:0.85,side:THREE.DoubleSide});""")

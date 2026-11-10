# ---------- 119. people instead of nutcrackers: the body is rebuilt on real proportions from smooth organic shapes (hips,
# waist, ribcage and shoulders, thighs that taper to a knee, calves, proper boots), longer arms, a smaller sculpted head
# with a real face, and hands with a thumb and four jointed fingers that close round whatever they hold. Cloth, denim,
# leather, skin and hair are drawn as such. Back items and hair sit on the body and barely swing. ----------

# --- surfaces for the body: 9 cloth, 10 denim, 11 leather, 12 skin, 13 hair
rep("""      else { // glass: a lens
        sSpec=8.0; sShin=8.0; sMetal=1.0; } } }`)""","""      else if(sK<8.5){ // glass: a lens
        sSpec=8.0; sShin=8.0; sMetal=1.0; }
      else if(sK<9.5){ // cloth: soft, uneven, no shine
        diffuseColor.rgb*=(0.9+0.12*fine)*(0.84+0.26*sn(p*vec3(26.0,9.0,26.0))); sSpec=0.2; sShin=0.5; }
      else if(sK<10.5){ // denim: twill streaks, paler where it rubs
        float st=sn(vec3(p.x*800.0,p.y*46.0,p.z*800.0)); diffuseColor.rgb*=(0.82+0.24*st)*(0.86+0.22*sn(p*vec3(20.0,7.0,20.0))); diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*1.3+0.03,ed*0.5); sSpec=0.25; sShin=0.5; }
      else if(sK<11.5){ // leather: creased, a dull shine, scuffed edges
        diffuseColor.rgb*=0.8+0.3*sn(p*300.0)*mid+0.08*fine; diffuseColor.rgb=mix(diffuseColor.rgb,diffuseColor.rgb*1.35+0.04,ed*0.4); sSpec=1.7; sShin=1.5; }
      else if(sK<12.5){ // skin: even, soft, light catching the edge
        diffuseColor.rgb*=0.96+0.06*mid; sSpec=0.5; sShin=0.8; sRim=0.2; }
      else { // hair: strands
        float hs=sn(vec3(p.x*460.0,p.y*24.0,p.z*460.0)); diffuseColor.rgb*=0.72+0.52*hs; sSpec=1.6; sShin=2.5; } } }`)""")
rep("void main() {\\n  float sSpec=1.0, sShin=1.0, sMetal=0.0;","void main() {\\n  float sSpec=1.0, sShin=1.0, sMetal=0.0, sRim=0.0;")
rep("""    outgoingLight+=env*surfEnv*sMetal*(0.07+0.45*fr)*(0.3+diffuseColor.rgb); }`)""","""    outgoingLight+=env*surfEnv*sMetal*(0.07+0.45*fr)*(0.3+diffuseColor.rgb); }
  if(sRim>0.0){ float fr=pow(1.0-max(dot(normal,normalize(vViewPosition)),0.0),3.0); outgoingLight+=diffuseColor.rgb*vec3(1.0,0.72,0.6)*fr*sRim*(0.35+0.65*surfEnv); }`)""")

# --- a smooth solid through cross-sections, and the sculpted skull
rep("// an oval skull with a slightly narrower jaw\nlet skullGeo=null;",r"""// A smooth organic solid through cross-sections [y, half-width, front depth, back depth, centre x, centre z] (front is -z),
// rounded off at both ends: limbs, torsos, necks, boots.
function organ(R,seg=18,sub=3){ const key='org'+JSON.stringify(R)+seg+'/'+sub; let g=rboxCache.get(key); if(g) return g;
  const cr=(a,b,c,d,t)=>0.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t), rings=[];
  for(let i=0;i<R.length-1;i++){ const p0=R[Math.max(0,i-1)], p1=R[i], p2=R[i+1], p3=R[Math.min(R.length-1,i+2)];
    for(let s=0;s<sub;s++){ const t=s/sub, q=[]; for(let k=0;k<6;k++) q.push(cr(p0[k]||0,p1[k]||0,p2[k]||0,p3[k]||0,t)); rings.push(q); } }
  { const q=[]; for(let k=0;k<6;k++) q.push(R[R.length-1][k]||0); rings.push(q); }
  const P=[], I=[], n=rings.length, down=rings[0][0]>rings[n-1][0]?1:-1;
  const ring=(q,sc,dy)=>{ for(let k=0;k<seg;k++){ const a=k/seg*Math.PI*2, s=Math.sin(a); P.push(q[4]+q[1]*sc*Math.cos(a),q[0]+dy,q[5]+(s<0?q[2]:q[3])*sc*s); } };
  { const q=rings[0], h=Math.min(q[1],q[2],q[3])*0.38*down; ring(q,0.45,h*0.85); ring(q,0.8,h*0.45); }                 // a rounded end
  for(const q of rings) ring(q,1,0);
  { const q=rings[n-1], h=Math.min(q[1],q[2],q[3])*0.38*down; ring(q,0.8,-h*0.45); ring(q,0.45,-h*0.85); }
  const m=P.length/3/seg;
  for(let i=0;i<m-1;i++) for(let k=0;k<seg;k++){ const a=i*seg+k, b=i*seg+(k+1)%seg, c=(i+1)*seg+(k+1)%seg, d=(i+1)*seg+k; I.push(a,b,c,a,c,d); }
  { const q=rings[0], h=Math.min(q[1],q[2],q[3])*0.38*down, c=P.length/3; P.push(q[4],q[0]+h,q[5]); for(let k=0;k<seg;k++) I.push(c,(k+1)%seg,k); }
  { const q=rings[n-1], h=Math.min(q[1],q[2],q[3])*0.38*down, c=P.length/3, o=(m-1)*seg; P.push(q[4],q[0]-h,q[5]); for(let k=0;k<seg;k++) I.push(c,o+k,o+(k+1)%seg); }
  let vol=0; for(let i=0;i<I.length;i+=3){ const a=I[i]*3, b=I[i+1]*3, c=I[i+2]*3; vol+=P[a]*(P[b+1]*P[c+2]-P[b+2]*P[c+1])-P[a+1]*(P[b]*P[c+2]-P[b+2]*P[c])+P[a+2]*(P[b]*P[c+1]-P[b+1]*P[c]); }
  if(vol<0) for(let i=0;i<I.length;i+=3){ const t=I[i+1]; I[i+1]=I[i+2]; I[i+2]=t; }                                    // faces point outwards
  g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); g.setIndex(I); g.computeVertexNormals(); rboxCache.set(key,g); return g; }
// the same, lying along z (a foot): sections [distance forward, half-width, depth below, height above, centre x, centre height]
function organZ(R,seg=16,sub=3){ const key='orz'+JSON.stringify(R)+seg+'/'+sub; let g=rboxCache.get(key); if(g) return g; g=organ(R,seg,sub).clone(); g.rotateX(-Math.PI/2); rboxCache.set(key,g); return g; }
// a skull with a face on it: brow ridge, eye sockets, cheekbones, the swell round the mouth, a chin, the angle of the jaw
let skull2=null;
function headGeo2(){ if(skull2) return skull2; const g=new THREE.SphereGeometry(1,44,32), p=g.attributes.position, G=(a,s)=>Math.exp(-a*a/s);
  for(let i=0;i<p.count;i++){ const x=p.getX(i), y=p.getY(i), z=p.getZ(i), lo=Math.max(0,-y), ax=Math.abs(x);
    let X=x*0.112*(1-0.27*Math.pow(lo,2.2)), Z=z*(z>0?0.125*(1-0.45*lo):0.118*(1-0.1*lo*lo)), Y=y*(y<0?0.15:0.138);
    if(z<0){ const f=-z;
      Z+=f*(0.011*G(ax-0.40,0.035)*G(y-0.09,0.02)-0.005*G(y-0.30,0.012)*(1-0.5*G(ax,0.02))-0.004*G(ax-0.5,0.05)*G(y+0.12,0.03)-0.005*G(ax,0.10)*G(y+0.48,0.03)-0.008*G(ax,0.06)*G(y+0.84,0.02));
      Y-=f*0.006*G(ax,0.08)*G(y+0.9,0.02); }
    if(z<0.3) X*=1+0.04*G(y+0.55,0.03);
    p.setXYZ(i,X,Y,Z); }
  g.computeVertexNormals(); return skull2=g; }
// an oval skull with a slightly narrower jaw
let skullGeo=null;""")

# --- colours carry a surface
rep("  // part(geometry, color, parent, x,y,z, rotation, scale, inkWidth)\n  const part=(geo,col,parent,x=0,y=0,z=0,rot,scl,w=0.011)=>{\n    const m=new THREE.Mesh(geo,toon(col));",
    """  const SURF_OF=new Map(); [[C.skin,12],[C.hair,13],[C.jacket,9],[C.jacketD,9],[C.jacketL,9],[C.pants,10],[C.pantsD,10],[C.boot,11],[C.sole,11],[C.glove,11],[C.pack,9],[C.packD,9],[C.roll,9],[C.wood,3],[C.steel,6],[C.metal,1],[C.metalL,1]].forEach(([c,s])=>{ if(!SURF_OF.has(c)) SURF_OF.set(c,s); });
  // part(geometry, color, parent, x,y,z, rotation, scale, inkWidth)
  const part=(geo,col,parent,x=0,y=0,z=0,rot,scl,w=0.011)=>{
    const m=new THREE.Mesh(geo,typeof col==='number'&&SURF_OF.has(col)?gunSurf(col,SURF_OF.get(col)):toon(col));""")

# --- pelvis and torso
a=s.index("  // pelvis\n  rig.hips=grp(hero,0,0.94,0);"); b=s.index("  if(top==='jacket'||top==='racer'){",a)
s=s[:a]+r"""  // pelvis: hips and seat, a belt with its buckle, the pouch on the hip
  const pz=(geo,col,par,x=0,y=0,z=0,rot,scl)=>part(geo,col,par,x,y,z,rot,scl,0);
  rig.hips=grp(hero,0,0.94,0);
  pz(organ([[.105,.146,.095,.104],[.06,.15,.098,.108],[.01,.158,.1,.12],[-.04,.161,.098,.124],[-.09,.146,.088,.112],[-.125,.09,.066,.08],[-.142,.05,.04,.05]],22),C.pants,rig.hips);
  pz(organ([[.1,.155,.101,.111],[.056,.1585,.103,.1145]],22,1),C.sole,rig.hips); pz(rbox(.052,.038,.012,.004),C.steel,rig.hips,0,.078,-.103);
  pz(rbox(.06,.09,.04,.014),C.packD,rig.hips,.172,.0,.02); // hip pouch (shells/mags come from here)
  rig.pouch=grp(rig.hips,.19,.0,-.02);
  // torso: a waist that narrows, a ribcage that fills out to the shoulders and slopes up into the neck
  rig.spine=grp(rig.hips,0,.09,0);
  pz(organ([[-.045,.146,.096,.104],[.02,.136,.094,.098],[.09,.138,.096,.098],[.16,.146,.1,.102],[.2,.15,.1,.103]],22),C.jacket,rig.spine);
  rig.chest=grp(rig.spine,0,.16,0);
  pz(organ([[-.03,.14,.098,.102],[.03,.156,.104,.11],[.09,.17,.11,.118],[.15,.178,.112,.122],[.2,.176,.104,.12],[.235,.15,.088,.108],[.262,.095,.066,.086],[.285,.058,.052,.058]],22),C.jacket,rig.chest);
  pz(organ([[.01,.1465,.1015,.1035],[-.026,.1425,.0995,.1015]],22,1),C.jacketD,rig.chest); // hem band
  pz(new THREE.CylinderGeometry(.06,.074,.05,18,1,true),C.jacketD,rig.chest,0,.272,.004);
"""+s[b:]
rep("part(bodyLathe([[.15,.0],[.165,-.12],[.18,-.3]],.72),C.jacket,rig.hips,0,.04,0,null,null,0); // tails (open lathe)","part(bodyLathe([[.176,.0],[.186,-.12],[.198,-.3]],.72),C.jacket,rig.hips,0,.04,0,null,null,0); // tails (open lathe)")
rep("[.03,.11,.19].forEach(y=>part(bodyLathe([[.162+y*.06,y],[.164+y*.06,y+.025]],.63),C.jacketD,rig.chest,0,0,0,null,null,0));","[.03,.11,.19].forEach(y=>part(bodyLathe([[.162+y*.1,y],[.164+y*.1,y+.025]],.67),C.jacketD,rig.chest,0,0,0,null,null,0));")
rep("part(rbox(.035,.28,.23,.008),C.accent,rig.chest,sx*.12,.12,0,null,null,0); part(rbox(.03,.2,.21,.006),C.accent,rig.spine,sx*.1,.07,0,null,null,0); }); part(rbox(.39,.03,.226,.006),C.accent,rig.chest,0,.21,0,null,null,0); }",
    "part(rbox(.035,.26,.238,.008),C.accent,rig.chest,sx*.12,.11,.002,null,null,0); part(rbox(.03,.2,.212,.006),C.accent,rig.spine,sx*.1,.07,.002,null,null,0); }); }")

# --- neck, head, face
a=s.index("  // head\n  rig.neck=grp(rig.chest,0,.27,0);"); b=s.index("  rig.tuft=grp(rig.head,0,.28,.02);",a)
s=s[:a]+r"""  // head: a neck with some width to it, a smaller skull, and a face (set-in eyes with irises, a nose with a bridge, lips)
  rig.neck=grp(rig.chest,0,.27,0);
  pz(organ([[-.03,.062,.054,.064],[.03,.051,.05,.056],[.09,.047,.05,.054],[.13,.05,.05,.05]],16),C.skin,rig.neck);
  rig.head=grp(rig.neck,0,.07,0); rig.head.scale.set(.75,.81,.81); // a real head-to-body ratio (about seven and a half heads tall)
  const skinD=new THREE.Color(C.skin).multiplyScalar(.8).getHex(), lipC=new THREE.Color(C.skin).lerp(new THREE.Color(0xa8504e),.5).getHex(); SURF_OF.set(skinD,12); SURF_OF.set(lipC,12);
  pz(headGeo2(),C.skin,rig.head,0,.135,0);
  [-1,1].forEach(sx=>{ pz(sph(.03),C.skin,rig.head,sx*.112,.126,.014,null,[.3,.95,.62]); pz(sph(.018),skinD,rig.head,sx*.119,.126,.008,null,[.22,.8,.55]); });             // ears
  pz(organ([[.172,.0075,.005,.008,0,-.108],[.148,.009,.009,.009,0,-.112],[.126,.012,.016,.011,0,-.114],[.11,.0165,.022,.012,0,-.113],[.099,.0145,.014,.011,0,-.111]],12),C.skin,rig.head); // nose
  [-1,1].forEach(sx=>pz(sph(.0095),C.skin,rig.head,sx*.0135,.105,-.119,null,[1,.8,1]));
  pz(sph(.02),lipC,rig.head,0,.0645,-.1125,null,[1.05,.19,.42]); pz(sph(.02),lipC,rig.head,0,.0525,-.1115,null,[.9,.25,.44]);                                                   // lips
  rig.lids=[-1,1].map(sx=>pz(sph(.019),C.skin,rig.head,sx*.044,.1635,-.106,null,[1.2,.42,.52]));
  rig.eyes=[-1,1].map(sx=>{ const e=grp(rig.head,sx*.044,.148,-.106); pz(sph(.015),0xece8e1,e,0,0,0,null,[1.15,.66,.5]); pz(sph(.0075),opts.eye||0x4a3423,e,0,0,-.0058,null,[1,1,.4]); pz(sph(.0038),0x0c0a0a,e,0,0,-.0082,null,[1,1,.4]); pz(sph(.0016),0xffffff,e,.003,.003,-.0096); return e; });
  rig.brows=[-1,1].map(sx=>pz(rbox(.044,.0065,.01,.003),C.hair,rig.head,sx*.046,.182,-.117,[0,0,sx*-.12]));
  rig.mouth=pz(rbox(.036,.004,.008,.002),0x55292a,rig.head,0,.0585,-.117);
"""+s[b:]

# --- arms and hands
a=s.index("  // arms\n  const arm=sx=>{"); b=s.index("  rig.armL=arm(-1); rig.armR=arm(1);",a)
s=s[:a]+r"""  // arms: a shoulder that rounds into the upper arm, an elbow, a forearm that narrows to the wrist; and a hand with a palm,
  // a thumb and four fingers of three joints each (palm side -z, thumb on the outside), posed by poseHands()
  const arm=sx=>{
    const sh=grp(rig.chest,sx*.19,.21,0); sh.rotation.order='XZY'; const UL=.29, FL=.26, G_=C.glove;
    if(top==='tee'){ pz(organ([[.045,.045,.05,.052],[.02,.06,.062,.064],[-.04,.059,.064,.064],[-.1,.054,.058,.056],[-.135,.052,.056,.054]],16),C.jacket,sh); pz(organ([[-.09,.047,.052,.05],[-.2,.043,.047,.045],[-.27,.04,.042,.042],[-.31,.038,.04,.04]],16),C.skin,sh); }
    else pz(organ([[.045,.045,.05,.052],[.02,.06,.062,.064],[-.04,.059,.064,.064],[-.12,.051,.057,.053],[-.2,.046,.049,.047],[-.27,.043,.045,.045],[-.31,.041,.043,.043]],16),C.jacket,sh);
    if(top==='armor') part(sph(.095),C.jacketL,sh,0,.0,0,null,[1.1,.75,1.1]);
    if(top==='suit') part(new THREE.TorusGeometry(.06,.014,8,16),C.accent,sh,0,-.14,0,[Math.PI/2,0,0],null,0);
    const el=grp(sh,0,-UL,0), fc=top==='tee'?C.skin:C.jacket;
    pz(organ([[.04,.04,.043,.045],[.0,.043,.045,.048],[-.05,.045,.047,.047],[-.12,.04,.041,.04],[-.19,.033,.032,.031],[-.245,.03,.027,.026]],16),fc,el);
    if(top!=='tee') pz(organ([[-.2,.036,.0345,.0335],[-.246,.035,.032,.031]],16,1),C.jacketD,el);                         // cuff
    const wr=grp(el,0,-FL,0), hg=grp(wr,0,0,0);
    pz(organ([[.022,.031,.025,.025],[-.012,.031,.021,.022],[-.034,.038,.016,.018]],14),G_,hg);                              // wrist
    pz(rbox(.084,.094,.03,.014),G_,hg,0,-.05,0); pz(rbox(.03,.052,.022,.011),G_,hg,sx*.028,-.036,-.012,[0,0,sx*.25]);        // palm, the pad at the base of the thumb
    const FX=[.031,.0105,-.0105,-.031], KY=[-.094,-.098,-.095,-.088], L1=[.042,.046,.043,.034], L2=[.026,.029,.027,.02], L3=[.021,.023,.022,.019], FR=[.0098,.0102,.0096,.0086];
    const fj={mcp:[],pip:[],dip:[]}, seg=(par,len,r)=>{ pz(limbGeo(r,r*.93,len),G_,par); pz(sph(r),G_,par); };
    FX.forEach((x,i)=>{ const m=grp(hg,sx*x,KY[i],-.001); seg(m,L1[i],FR[i]); const p=grp(m,0,-L1[i],0); seg(p,L2[i],FR[i]*.93); const d=grp(p,0,-L2[i],0); seg(d,L3[i],FR[i]*.86); pz(sph(FR[i]*.82),G_,d,0,-L3[i],0);
      fj.mcp.push(m); fj.pip.push(p); fj.dip.push(d); });
    const t0=grp(hg,sx*.037,-.03,-.008), t1=grp(t0,0,-.038,0), t2=grp(t1,0,-.03,0); t0.rotation.order='ZXY';
    pz(limbGeo(.0128,.0118,.038),G_,t0); pz(sph(.0128),G_,t0); pz(limbGeo(.0112,.0104,.03),G_,t1); pz(sph(.0114),G_,t1); pz(limbGeo(.0102,.0092,.026),G_,t2); pz(sph(.0102),G_,t2); pz(sph(.009),G_,t2,0,-.026,0);
    const fing=grp(wr,0,-.068,0), hand=grp(wr,0,-.098,-.032);
    return {sh,el,wr,fing,hand,hg,fj,th:[t0,t1,t2],side:sx,a:UL,b:FL};
  };
"""+s[b:]

# --- legs and boots
a=s.index("  // legs\n  const leg=sx=>{"); b=s.index("  rig.legL=leg(-1); rig.legR=leg(1);",a)
s=s[:a]+r"""  // legs: thighs that angle in to the knee, a kneecap, a calf, a cuff over a boot with a real foot in it
  const leg=sx=>{
    const hp=grp(rig.hips,sx*.08,-.05,0); hp.rotation.order='XZY';
    pz(organ([[.05,.07,.08,.084,sx*.004],[-.03,.081,.09,.097,sx*.003],[-.12,.08,.088,.091,sx*.001],[-.24,.07,.076,.074,-sx*.006],[-.34,.06,.064,.062,-sx*.011],[-.4,.056,.062,.056,-sx*.013],[-.44,.052,.056,.052,-sx*.013]],18),C.pants,hp);
    const kn=grp(hp,0,-.4,0);
    pz(organ([[.05,.054,.058,.054,-sx*.013],[.0,.056,.064,.055,-sx*.013],[-.06,.054,.052,.062,-sx*.011],[-.13,.057,.047,.07,-sx*.009],[-.22,.048,.043,.056,-sx*.005],[-.31,.041,.039,.043,-sx*.002],[-.385,.041,.041,.043,0]],18),C.pants,kn);
    pz(organ([[-.335,.0435,.0425,.0455,-sx*.001],[-.388,.0435,.0435,.0455,0]],18,1),C.pantsD,kn);                           // cuff
    const an=grp(kn,0,-.37,0);
    pz(organ([[.06,.046,.047,.05],[.01,.045,.047,.05],[-.045,.045,.05,.052],[-.09,.047,.056,.054]],16),C.boot,an);          // boot shaft
    pz(organZ([[-.078,.03,.02,.03,0,-.09],[-.05,.045,.03,.05,0,-.088],[.0,.049,.031,.06,0,-.088],[.06,.051,.03,.046,0,-.09],[.12,.053,.028,.034,0,-.092],[.17,.049,.025,.03,0,-.094],[.2,.037,.02,.022,0,-.096]],16),C.boot,an); // the foot
    pz(rbox(.108,.022,.292,.01),C.sole,an,0,-.119,-.062); pz(rbox(.098,.016,.085,.006),C.sole,an,0,-.128,.03);              // sole and heel
    for(let q=0;q<3;q++) pz(rbox(.05,.006,.008,.003),C.sole,an,0,-.043-q*.012,-.062-q*.022,[-.75,0,0]);                    // laces
    const foot=grp(an,0,-.13,-.06);
    return {hp,kn,an,foot,side:sx};
  };
"""+s[b:]

# --- arms are longer now
rep("  const sh=arm.sh, a=0.25, b=0.23;","  const sh=arm.sh, a=arm.a||0.25, b=arm.b||0.23;")

# --- hands close round what they hold
rep("const _pkY=new THREE.Vector3(0,1,0);\nfunction pickTwoHands(H,S){","""// Hands. Each finger joint is turned towards a pose: loose at rest, a fist round a tool's handle, flat for editing; a gun's
// grip is held with the hand turned upright beside it, the first finger lying along the trigger; the other hand comes in
// from the side under the fore-end and curls up round it.
const HAND_POSE={relax:[[.22,.32,.18],[.32,.42,.24],[.3,.55,.12,.15]],fist:[[1.0,1.45,.85],[1.05,1.5,.9],[.9,.1,.45,.6]],pgrip:[[.2,.9,.5],[1.25,1.3,.5],[.7,.22,.3,.35]],
  cradle:[[1.2,.8,.4],[1.2,.8,.4],[1.15,.25,.55,.6]],wrap:[[1.25,1.3,.5],[1.25,1.3,.5],[.7,.22,.3,.35]],flat:[[.04,.08,.04],[.06,.1,.05],[.15,.85,.05,.05]]};
// how the other hand joins in (0 not at all, 1 an upright foregrip, 2 cupping the firing hand; otherwise under the fore-end), and where a grip sits in the firing hand
const GUN_SUPPORT={nade:0,burst:1,glauncher:1,pistol:2,revolver:2,hcannon:2,gatling:3}, GUN_HOLD={pump:[0,-.025,0],hunting:[0,-.025,0],infantry:[0,-.025,0],dbarrel:[0,-.025,0],sniper:[0,-.02,0],revolver:[0,-.02,0],gatling:[0,-.03,-.05]};
const _gv1=new THREE.Vector3(), _gv2=new THREE.Vector3(), _gv3=new THREE.Vector3();
function poseHands(H,S,dt){ const r=H.rig; if(!r.armR||!r.armR.fj) return; const k=1-Math.exp(-(dt||0.016)*18);
  const emo=S.emote&&EMOTES[S.emote.id], building=!!S.building&&!emo, gun=!building&&!emo&&!S.editing&&!S.sky&&!S.down?S.gun:false, mdl=gun?modelOf(gun):null, held=gun&&mdl!=='nade';
  const tool=!gun&&((r.pick&&r.pick.visible)||(r.hammer&&r.hammer.visible)), two=tool&&r.armL.fing.rotation.x>1.1;
  const set=(a,name,ty,tz)=>{ const P=HAND_POSE[name], f=a.fj; for(let i=0;i<4;i++){ const q=P[i?1:0]; f.mcp[i].rotation.x+=(q[0]-f.mcp[i].rotation.x)*k; f.pip[i].rotation.x+=(q[1]-f.pip[i].rotation.x)*k; f.dip[i].rotation.x+=(q[2]-f.dip[i].rotation.x)*k; }
    const t=P[2], T=a.th; T[0].rotation.x+=(t[0]-T[0].rotation.x)*k; T[0].rotation.z+=(a.side*t[1]-T[0].rotation.z)*k; T[1].rotation.x+=(t[2]-T[1].rotation.x)*k; T[2].rotation.x+=(t[3]-T[2].rotation.x)*k;
    a.hg.rotation.y+=(ty-a.hg.rotation.y)*k; a.hg.rotation.z+=(tz-a.hg.rotation.z)*k; };
  set(r.armR,held?'pgrip':tool||mdl==='nade'?'fist':S.editing?'flat':'relax',held?Math.PI/2:0,0);
  const sp=held?GUN_SUPPORT[mdl]:0; const und=sp===undefined||sp===3; set(r.armL,held?(sp===0?'relax':sp===3?'fist':sp?'wrap':'cradle'):two?'fist':S.editing?'flat':'relax',held?(und?0.6:sp?-0.97:0):0,held&&und?1.35:0);
  const gh=held&&GUN_HOLD[mdl]||[0,0,0], hp=r.armR.hand.position, mx=held?-.032+gh[0]:0, my=held?-.092+gh[1]:-.098, mz=held?-.06+gh[2]:-.032; hp.x+=(mx-hp.x)*k; hp.y+=(my-hp.y)*k; hp.z+=(mz-hp.z)*k; }
const _pkY=new THREE.Vector3(0,1,0), _p2c=new THREE.Vector3();
function pickTwoHands(H,S){""")
rep("  if(S.bare) return; r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; }",
    "  if(S.bare) return; r.armR.wr.getWorldQuaternion(_p2q); t.sub(_p2c.set(0,-.098,-.032).applyQuaternion(_p2q)); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; } // the wrist sits back from the handle so the fist closes on it")
rep("  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); }","  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); poseHands(H,S,dt); }")
# the other hand reaches the fore-end from the side
rep("    grip.getWorldPosition(_ikT); const gripW=_ikT.clone();","    grip.getWorldPosition(_ikT); const gripW=_ikT.clone();\n    if(r.armL.fj){ const sp=GUN_SUPPORT[mdl], gx=_gv1.set(1,0,0).applyQuaternion(_hq), gy=_gv2.set(0,1,0).applyQuaternion(_hq), gz=_gv3.set(0,0,1).applyQuaternion(_hq); // the wrist stands off from what the hand holds\n      if(sp===1) gripW.addScaledVector(gx,-.036).addScaledVector(gy,.092).addScaledVector(gz,.06); else if(sp===2) gripW.addScaledVector(gx,-.058).addScaledVector(gy,.085).addScaledVector(gz,.07); else if(sp===3) gripW.addScaledVector(gx,-.0956).addScaledVector(gy,.0215).addScaledVector(gz,.032); else if(sp===undefined) gripW.addScaledVector(gx,-.074).addScaledVector(gy,.011).addScaledVector(gz,.015); }")

# --- less floaty: the pack and the hair barely swing
rep("  r.pack.rotation.x=A.pack+0.06*k;","  r.pack.rotation.x=A.pack*0.25+0.015*k;")
rep("  r.tuft.rotation.x=-A.tuft*0.6;","  r.tuft.rotation.x=-A.tuft*0.2;")
# eyelids rest over the top of the eye; face paint lies on the cheek
rep("  r.lids.forEach(l=>{ l.position.y=lerp(l.position.y,.168-(1-blink)*.022,0.6); l.scale.y=lerp(l.scale.y,.2+(1-blink)*.9,0.6); });","  r.lids.forEach(l=>{ l.position.y=lerp(l.position.y,.1635-(1-blink)*.016,0.6); l.scale.y=lerp(l.scale.y,.42+(1-blink)*.7,0.6); });")
rep("[-1,1].forEach(sx=>part(rbox(.03,.025,.012,.006),0x1a1f29,rig.head,sx*.07,.1,-.128,[0,0,sx*.3],null,0)); // face paint","[-1,1].forEach(sx=>part(rbox(.03,.02,.005,.002),0x1a1f29,rig.head,sx*.07,.1,-.097,[0,sx*-.7,sx*.3],null,0)); // face paint")
# back items lie against the back
rep("const gt=grp(rig.pack,0,-.2,.05); gt.rotation.z=.75;","const gt=grp(rig.pack,0,-.2,.012); gt.rotation.z=.75;")
rep("part(sd,C.pack,rig.pack,0,-.07,.03); part(new THREE.TorusGeometry(.2,.018,8,24),C.packD,rig.pack,0,-.07,.03,null,null,0.004);\n    part(sph(.05),0xc9d2dc,rig.pack,0,-.07,.06,null,[1,1,.6],0.005);\n    [0,Math.PI/2].forEach(a=>part(rbox(.34,.025,.008,.004),C.accent,rig.pack,0,-.07,.053,[0,0,a],null,0));",
    "part(sd,C.pack,rig.pack,0,-.07,.012); part(new THREE.TorusGeometry(.2,.018,8,24),C.packD,rig.pack,0,-.07,.012,null,null,0.004);\n    part(sph(.05),0xc9d2dc,rig.pack,0,-.07,.042,null,[1,1,.6],0.005);\n    [0,Math.PI/2].forEach(a=>part(rbox(.34,.025,.008,.004),C.accent,rig.pack,0,-.07,.035,[0,0,a],null,0));")
rep("const sw=grp(rig.pack,0,-.05,.03); sw.rotation.z=.7;","const sw=grp(rig.pack,0,-.05,.01); sw.rotation.z=.7;")

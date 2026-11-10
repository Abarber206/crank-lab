  /* ---------- the armoury ----------
     Gun space: f forward along the barrel, u up (hand space is -y forward, -z up, +x right); the firing hand holds the
     grip at the origin. Each gun is cut from side profiles to its own outline, in gun steel, polymer, wood or paint. */
  const mS=gunSurf(0x2d3036,1), mSD=gunSurf(0x191b1f,1), mSG=gunSurf(0x545a62,1), mP=gunSurf(0x202328,2), mPG=gunSurf(0x3a3e45,2), mR=gunSurf(0x15171a,5),
        mWal=gunSurf(0x6a4020,3), mWalD=gunSurf(0x4a2c15,3), mWd=gunSurf(0x9a6730,3), mLam=gunSurf(0x8c4a20,3), mBr=gunSurf(0x7b828a,6), mBrass=gunSurf(0xc9a54a,7), mHole=toon(0x060709),
        mOD=gunSurf(0x4c5637,4), mODp=gunSurf(0x4a5535,2), mTan=gunSurf(0x9c8562,2), mBake=gunSurf(0x7a3416,2), mLens=gunSurf(0x2d5f86,8), mLensR=gunSurf(0x8a2b22,8), mShell=gunSurf(0xb5302a,2);
  const PF=(W,m,pts,w,bev=.004,x=0)=>p0(prof(pts.map(q=>[-q[0],-q[1]]),w,bev),m,W,x,0,0);                    // a side profile [f,u] of width w
  const BX=(W,m,f0,f1,u0,u1,w,r=.004,x=0)=>p0(rbox(w,Math.abs(f1-f0),Math.abs(u1-u0),r),m,W,x,-(f0+f1)/2,-(u0+u1)/2);
  const CY=(W,m,r,f0,f1,u,x=0,seg=14)=>p0(cylY(r,Math.abs(f1-f0),seg),m,W,x,-(f0+f1)/2,-u);                 // along the barrel
  const CN=(W,m,rb_,rf_,f0,f1,u,x=0,seg=14)=>p0(new THREE.CylinderGeometry(rb_,rf_,Math.abs(f1-f0),seg),m,W,x,-(f0+f1)/2,-u); // tapering (back radius, front radius)
  const PIN=(W,m,r,len,f,u,x=0)=>p0(cylX(r,len),m,W,x,-f,-u);                                               // across the gun
  const POST=(W,m,r,u0,u1,f,x=0,seg=10)=>p0(cylY(r,Math.abs(u1-u0),seg),m,W,x,-f,-(u0+u1)/2,[Math.PI/2,0,0]); // upright
  const TILT=(W,m,f,u,len,ht,w,a,r=.004,x=0)=>p0(rbox(w,len,ht,r),m,W,x,-f,-u,[a,0,0]);                     // a box turned about the cross axis (a>0: front up / bottom forward)
  const TR=(W,name,f0,f1,u0,u1,w,x=0)=>trim(rbox(w,Math.abs(f1-f0),Math.abs(u1-u0),.002),W,x,-(f0+f1)/2,-(u0+u1)/2,null,null,name); // rarity colour
  const MK=(name,m,g,mg)=>marks(name,[0,-m[0],-m[1]],g.length>2?g:[0,-g[0],-g[1]],mg.length>2?mg:[0,-mg[0],-mg[1]]);
  const mkW=(name)=>{ const g=grp(rig.armR.hand,0,0,0); rig[name]=g; return g; };
  const railG=len=>{ const k='rail'+Math.round(len*1000); let g=rboxCache.get(k); if(g) return g; const L=[], b=new THREE.BoxGeometry(.017,len,.004); b.translate(0,0,-.002); L.push(b);
    for(let y=-len/2+.004;y<len/2-.003;y+=.0101){ const t=new THREE.BoxGeometry(.021,.0056,.0045); t.translate(0,y,-.00625); L.push(t); } g=mergeGeos(L); rboxCache.set(k,g); return g; };
  const RAIL=(W,f0,f1,u,m=mSD)=>p0(railG(f1-f0),m,W,0,-(f0+f1)/2,-u);                                         // a slotted accessory rail sitting on height u
  const GRIP=(W,m,rb,y0=.03,w=.034)=>{ p0(prof(gripPts(y0,rb),w,.005),m,W,0,0,0); p0(new THREE.TorusGeometry(.026,.004,6,14,Math.PI),mSD,W,0,y0-.058,rb,GUARD); p0(rbox(.006,.008,.022,.002),mSD,W,0,y0-.052,rb+.012,[-.3,0,0]); };
  const TRIG=(W,y,z,r=.024)=>{ p0(new THREE.TorusGeometry(r,.004,6,14,Math.PI),mSD,W,0,y,z,GUARD); p0(rbox(.006,.008,.022,.002),mSD,W,0,y+.006,z+.012,[-.3,0,0]); };
  const MAGC=(W,m,f,u,n,sl,w,d,a0,da)=>{ let y=-f, z=-u, a=a0; for(let q=0;q<n;q++){ p0(rbox(w,d,sl+.008,.004),m,W,0,y-Math.sin(a)*sl/2,z+Math.cos(a)*sl/2,[a,0,0]); p0(rbox(w+.002,.004,sl,.001),mSD,W,0,y-Math.sin(a)*sl/2+d*.3*Math.cos(a),z+Math.cos(a)*sl/2+d*.3*Math.sin(a),[a,0,0]); y-=Math.sin(a)*sl; z+=Math.cos(a)*sl; a+=da; }
    p0(rbox(w+.004,d+.006,.01,.003),mSD,W,0,y,z,[a-da,0,0]); };                                               // a curved magazine, from its top
  const MAGP=(W,m,f,u,len,d,a0,bend,w,cap=mSD)=>{ const N=6, A=[], B=[]; let cf=f, cu=u, a=a0; for(let q=0;q<=N;q++){ const c=Math.cos(a), s_=Math.sin(a); A.push([cf+c*d/2,cu+s_*d/2]); B.push([cf-c*d/2,cu-s_*d/2]); if(q<N){ cf+=s_*len/N; cu-=c*len/N; a+=bend/N; } }
    PF(W,m,A.concat(B.reverse()),w,.003); TILT(W,cap,cf,cu,d+.008,.012,w+.004,a-bend/N,.003); };                                // a magazine in one curved piece, from the middle of its top
  const FLASH=(W,f,u,r,len)=>{ CY(W,mSD,r,f,f+len,u,0,10); for(let q=0;q<4;q++){ const a=q*Math.PI/2+Math.PI/4; p0(rbox(.003,len*.6,.003,.001),mHole,W,Math.cos(a)*r,-(f+len*.55),-u+Math.sin(a)*r); } return f+len; };
  const BRAKE=(W,f,u,r,len)=>{ BX(W,mSD,f,f+len,u-r,u+r,r*2.4,r*.5); for(const k of [.3,.7]) for(const sx of [-1,1]) BX(W,mHole,f+len*k-.007,f+len*k+.007,u-r*.55,u+r*.55,.003,.001,sx*r*1.2); return f+len; };
  const SUPP=(W,f,u,r,len,m=mSD)=>{ CY(W,m,r,f,f+len,u,0,18); for(const k of [.05,.5,.95]) CY(W,mS,r+.0012,f+len*k-.004,f+len*k+.004,u,0,18); p0(cylY(r*.32,.002,10),mHole,W,0,-(f+len)-.0006,-u); return f+len; };
  const LENS=(W,m,r,f,u,front)=>p0(new THREE.CircleGeometry(r,18),m,W,0,-f,-u,[front?Math.PI/2:-Math.PI/2,0,0]);
  const RDOT=(W,f,u)=>{ BX(W,mSD,f-.022,f+.022,u,u+.016,.026,.003); CY(W,mSD,.017,f-.032,f+.032,u+.032,0,16); CY(W,mSD,.019,f+.02,f+.032,u+.032,0,16); POST(W,mSD,.007,u+.046,u+.058,f); PIN(W,mSD,.007,.05,f,u+.032);
    LENS(W,mLensR,.0145,f+.0326,u+.032,true); LENS(W,mLens,.0145,f-.0326,u+.032,false); };
  const HOLO=(W,f,u)=>{ BX(W,mSD,f-.03,f+.03,u,u+.018,.03,.003); for(const sx of [-1,1]) BX(W,mSD,f-.012,f+.03,u+.016,u+.054,.004,.001,sx*.015); BX(W,mSD,f-.012,f+.03,u+.05,u+.056,.034,.002); BX(W,mLens,f+.02,f+.0215,u+.018,u+.05,.027,.0004); };
  // a telescopic sight on rings, sitting on a rail at height u; returns its centre height
  const SCOPE=(W,f0,f1,u,obj=.024,tube=.0125)=>{ const fm=(f0+f1)/2, c=u+.012+tube+.01; CY(W,mSD,tube,f0+.05,f1-.07,c,0,16); CN(W,mSD,.019,tube,f0+.03,f0+.055,c,0,16); CY(W,mSD,.019,f0,f0+.032,c,0,16); CN(W,mSD,tube,obj,f1-.075,f1-.045,c,0,16); CY(W,mSD,obj,f1-.047,f1,c,0,16);
    BX(W,mSD,fm-.016,fm+.016,c-.016,c+.016,.032,.006); POST(W,mSD,.011,c+.014,c+.034,fm); PIN(W,mSD,.011,.03,fm,c,.02);
    for(const fr of [fm-.055,fm+.055]){ CY(W,mS,tube+.004,fr-.008,fr+.008,c,0,14); BX(W,mS,fr-.008,fr+.008,u+.004,c-tube+.002,.018,.003); }
    LENS(W,mLens,obj-.002,f1+.0006,c,true); LENS(W,mLens,.016,f0-.0006,c,false); return c; };
  const BIPOD=(W,f,u,len)=>{ BX(W,mSD,f-.015,f+.015,u-.012,u+.004,.04,.004); for(const sx of [-1,1]){ BX(W,mSD,f,f+len,u-.012,u-.003,.008,.003,sx*.019); BX(W,mR,f+len-.02,f+len,u-.014,u-.001,.012,.003,sx*.019); } };
  const SLOTS=(W,f0,n,step,len,u0,u1,hw)=>{ for(let q=0;q<n;q++) for(const sx of [-1,1]) BX(W,mHole,f0+q*step,f0+q*step+len,u0,u1,.003,.001,sx*hw); };

  // ---- assault rifle: a flat-top carbine, slim slotted handguard, red dot, collapsible stock, curved steel magazine
  rig.gun=grp(rig.armR.hand,0,0,0);
  { const W=rig.gun, ub=.058; GRIP(W,mP,.022);
    PF(W,mS,[[-.08,.036],[-.08,0],[-.058,-.022],[.03,-.022],[.045,-.012],[.068,-.012],[.07,-.05],[.128,-.054],[.132,.036]],.046);   // lower receiver and magazine well
    PF(W,mS,[[-.082,.036],[.135,.036],[.135,.082],[.122,.088],[-.066,.088],[-.082,.072]],.05);                                   // upper receiver
    BX(W,mHole,-.02,.052,.05,.068,.004,.001,.0245); BX(W,mS,-.046,-.024,.05,.072,.012,.004,.027); PIN(W,mS,.006,.02,-.058,.06,.03);  // ejection port, deflector, forward assist
    PIN(W,mSD,.0035,.05,-.06,.02); PIN(W,mSD,.0035,.05,.115,.012); PIN(W,mSD,.005,.052,.02,.004);                              // pins and selector
    BX(W,mSD,-.1,-.066,.078,.088,.06,.003); RAIL(W,-.06,.132,.088);                                                              // charging handle, top rail
    BX(W,mS,.135,.44,.03,.088,.044,.014); RAIL(W,.135,.44,.088); SLOTS(W,.165,5,.055,.035,.052,.064,.022); CY(W,mSD,.027,.132,.15,ub,0,16); // handguard, barrel nut
    for(let q=0;q<4;q++) BX(W,mHole,.17+q*.065,.2+q*.065,.029,.031,.012,.001);
    CY(W,mSD,.0085,.44,.535,ub); FLASH(W,.535,ub,.0115,.045);                                                                    // barrel, flash hider
    BX(W,mSD,.4,.43,.0925,.103,.02,.003); BX(W,mSD,-.055,-.03,.0925,.103,.02,.003); RDOT(W,.03,.0925);                           // folded sights, red dot
    CY(W,mS,.0135,-.3,-.08,.052); CY(W,mSD,.019,-.094,-.08,.052,0,12);                                                           // buffer tube, castle nut
    PF(W,mP,[[-.165,.074],[-.305,.074],[-.322,.064],[-.322,-.05],[-.3,-.056],[-.262,-.018],[-.195,.022],[-.165,.03]],.04,.006); BX(W,mR,-.334,-.32,-.052,.068,.042,.004); // stock, butt pad
    rig.arMag=grp(W,0,0,0); PF(rig.arMag,mSG,[[.074,-.04],[.124,-.04],[.142,-.16],[.136,-.192],[.092,-.186],[.082,-.15]],.022,.003);
    for(const k of [.3,.6]) PF(rig.arMag,mSD,[[.079+k*.012,-.06-k*.11],[.123+k*.017,-.062-k*.11],[.1235+k*.017,-.066-k*.11],[.0795+k*.012,-.064-k*.11]],.0235,.001);
    TR(W,'ar',.2,.3,.068,.076,.047); TR(W,'ar',-.28,-.2,.05,.057,.042);
    rig.muzzleAR=grp(W,0,-.585,-ub); rig.gripAR=grp(W,0,-.3,-.03); rig.magAR=grp(W,0,-.115,.2); }

  // ---- pump shotgun: walnut stock and a ribbed sliding fore-end on a blued steel receiver
  rig.pump=grp(rig.armR.hand,0,0,0);
  { const W=rig.pump, ub=.064, ut=.036;
    PF(W,mWal,[[-.005,.078],[-.33,.064],[-.335,-.058],[-.315,-.064],[-.14,-.012],[-.09,-.012],[-.105,-.088],[-.098,-.1],[-.055,-.104],[-.045,-.094],[-.03,-.05],[-.012,-.012],[0,.01]],.042,.008); // stock with its grip
    BX(W,mR,-.348,-.333,-.06,.066,.044,.005);
    PF(W,mS,[[-.05,.02],[-.035,-.012],[.19,-.012],[.19,.082],[-.03,.082],[-.055,.062]],.046,.006); TRIG(W,-.025,.012);         // receiver
    BX(W,mHole,.05,.14,.044,.066,.003,.001,.0235); BX(W,mHole,.03,.14,-.0135,-.011,.028,.001); PIN(W,mSD,.004,.05,.02,.03); PIN(W,mSD,.004,.05,.15,.02);
    CY(W,mSD,.0115,.19,.69,ub); CY(W,mS,.0105,.19,.6,ut); CY(W,mSD,.0125,.6,.615,ut); BX(W,mSD,.57,.585,ut-.012,ub+.013,.03,.006);    // barrel, magazine tube, clamp
    p0(sph(.0045),mBrass,W,0,-.682,-(ub+.0135)); for(const sx of [-1,1]) BX(W,mS,.19,.33,ut-.004,ut+.004,.003,.001,sx*.018);     // bead, action bars
    rig.slide=grp(W,0,-.33,-.025); p0(rbox(.05,.17,.054,.022),mWal,rig.slide,0,0,-.011); for(let q=0;q<7;q++) p0(rbox(.052,.006,.056,.003),mWalD,rig.slide,0,-.066+q*.022,-.011);
    rig.gripPump=grp(rig.slide,0,0,.016);
    TR(W,'pump',.02,.14,.0835,.0885,.03);
    rig.muzzlePump=grp(W,0,-.695,-ub); rig.portPump=grp(W,0,-.1,.04); }
  rig.muzzle=rig.muzzleAR;

  // ---- submachine gun: round-topped stamped receiver, cocking tube over the barrel, slim curved magazine, ring front sight
  { const W=mkW('smg'), ub=.05; GRIP(W,mP,.004);
    PF(W,mP,[[-.082,.036],[-.082,.0],[-.06,-.006],[.062,-.006],[.068,.036]],.04);
    PF(W,mS,[[-.086,.034],[.21,.034],[.21,.07],[.2,.082],[-.072,.082],[-.086,.07]],.042,.012); BX(W,mHole,.02,.075,.05,.066,.003,.001,.0215);
    PF(W,mS,[[.07,.036],[.07,-.03],[.118,-.036],[.122,.036]],.034); MAGP(W,mSD,.096,-.03,.2,.036,.04,.36,.022);
    CY(W,mS,.0125,.2,.385,.074); CY(W,mSD,.014,.385,.392,.074); PIN(W,mSD,.006,.026,.33,.074,-.02); p0(sph(.009),mP,W,-.036,-.33,-.074);       // cocking tube and handle
    CY(W,mSD,.008,.2,.42,ub); CY(W,mSD,.0105,.398,.408,ub);
    PF(W,mP,[[.21,.02],[.36,.024],[.372,.04],[.372,.062],[.21,.062]],.046,.012);                                                 // handguard
    BX(W,mSD,.375,.395,.084,.092,.016,.003); p0(new THREE.TorusGeometry(.014,.003,6,16),mSD,W,0,-.385,-.106,[Math.PI/2,0,0]); POST(W,mSD,.002,.092,.106,.385); // hooded front sight
    POST(W,mSD,.012,.082,.098,-.045,0,12); CY(W,mSD,.022,-.092,-.086,.058,0,14);                                                 // drum rear sight, end cap
    PF(W,mP,[[-.088,.078],[-.3,.07],[-.3,-.03],[-.28,-.036],[-.2,.03],[-.088,.04]],.036,.006); BX(W,mR,-.312,-.298,-.032,.072,.038,.004);
    TR(W,'smg',.02,.12,.038,.045,.0435); MK('smg',[.425,ub],[.29,.02],[.115,-.24]); }

  // ---- machine gun: belt-fed, feed cover on top, soft ammunition pouch, heat shield and a folded bipod
  { const W=mkW('mg'), ub=.05; GRIP(W,mP,.02);
    PF(W,mS,[[-.11,-.02],[.3,-.02],[.3,.078],[-.11,.078]],.056,.005); PF(W,mSG,[[-.09,.078],[.16,.078],[.16,.098],[.14,.104],[-.07,.104],[-.09,.094]],.058,.005); RAIL(W,-.07,.13,.104);
    BX(W,mHole,.03,.1,.04,.066,.003,.001,.0285); PIN(W,mSD,.006,.03,.2,.05,.03);
    BX(W,mOD,.03,.17,-.15,-.022,.1,.02,-.012); BX(W,mODp,.025,.175,-.03,-.018,.104,.006,-.012); for(let q=0;q<5;q++) PIN(W,mBrass,.0045,.032,.05+q*.011,.07+q*.002,-.04);  // pouch, belt
    CY(W,mSD,.0105,.3,.74,ub); CY(W,mSD,.007,.3,.6,ub-.024); BX(W,mS,.31,.57,ub+.014,ub+.027,.036,.005); SLOTS(W,.33,5,.046,.026,ub+.016,ub+.024,.018);
    PF(W,mP,[[.3,-.014],[.52,.0],[.52,.036],[.3,.036]],.05,.012); BX(W,mSD,.6,.62,ub-.03,ub+.05,.014,.004); CN(W,mSD,.011,.018,.74,.79,ub);
    BX(W,mSD,.31,.39,.108,.116,.012,.004,.03); for(const f of [.315,.385]) BX(W,mSD,f-.005,f+.005,.08,.11,.008,.002,.03);            // carrying handle
    BIPOD(W,.5,.0,.24);
    PF(W,mP,[[-.11,.076],[-.33,.07],[-.345,.055],[-.345,-.05],[-.32,-.058],[-.25,.005],[-.11,.012]],.042,.006); BX(W,mSD,-.33,-.25,.076,.086,.02,.004);
    TR(W,'mg',-.06,.1,.082,.09,.0595); MK('mg',[.79,ub],[.4,-.006],[.1,-.18]); }

  // ---- minigun: six barrels in clamps on a motor housing, top handle, feed chute down to an ammunition can
  { const W=mkW('gatling'), u0=.02; p0(prof(gripPts(.06,.062),.036,.005),mP,W,0,0,0); p0(rbox(.006,.008,.022,.002),mSD,W,0,.012,.074,[-.3,0,0]);
    CY(W,mS,.072,-.1,.14,u0,0,22); BX(W,mSD,-.09,.12,-.062,-.02,.09,.01); CY(W,mSD,.046,-.175,-.1,u0,0,16); CY(W,mBr,.02,-.185,-.175,u0,0,12); CY(W,mSG,.064,.14,.166,u0,0,22);
    for(const f of [-.06,0,.06]) CY(W,mSD,.0735,f-.004,f+.004,u0,0,22);
    rig.barrels=grp(W,0,-.42,-u0);
    for(let q=0;q<6;q++){ const a=q/6*Math.PI*2; p0(cylY(.0095,.56),mSD,rig.barrels,Math.cos(a)*.036,0,Math.sin(a)*.036); }
    p0(cylY(.012,.5),mS,rig.barrels,0,0,0); [.2,0,-.18].forEach(y=>p0(cylY(.05,.014,18),mSG,rig.barrels,0,y,0)); p0(cylY(.054,.034,18),mS,rig.barrels,0,-.262,0);
    CY(W,mSD,.011,0,.2,.15); for(const f of [.012,.188]) POST(W,mSD,.008,.085,.15,f);                                              // top handle
    BX(W,mOD,-.08,.09,-.15,-.03,.09,.012,-.105); BX(W,mODp,-.085,.095,-.04,-.026,.094,.005,-.105); for(let q=0;q<4;q++) TILT(W,mSG,-.01+q*.004,-.01+q*.016,.05,.014,.034,0,.004,-.07-q*.004); // can and chute
    trim(cylY(.0745,.03,22),W,0,.06,-u0,null,null,'gatling');
    rig.muzzle_gatling=grp(W,0,-.72,-u0); rig.grip_gatling=grp(W,0,-.1,-.15); rig.mag_gatling=grp(W,-.12,0,.14); }

  // ---- rocket launcher: a slim tube with a flared venturi, wooden heat guard, optical sight and a bulbous warhead
  { const W=mkW('rpg'), ub=.05, mT=gunSurf(0x3b4136,4); GRIP(W,mWd,.0);
    BX(W,mS,-.075,.075,.0,.028,.03,.006); CY(W,mT,.026,-.34,.45,ub,0,18); CN(W,mT,.052,.026,-.5,-.34,ub,0,18); CY(W,mSD,.054,-.512,-.5,ub,0,18); CN(W,mT,.026,.034,.4,.45,ub,0,18);
    CY(W,mWd,.034,-.3,-.03,ub,0,18); for(const f of [-.29,-.165,-.04]) CY(W,mSD,.0352,f-.006,f+.006,ub,0,18);
    PF(W,mWd,[[-.17,.026],[-.13,.026],[-.14,-.07],[-.185,-.07]],.03,.008);                                                       // rear handgrip
    BX(W,mSD,.0,.1,.085,.125,.03,.008,-.034); CY(W,mSD,.014,.1,.13,.105,-.034,12); LENS(W,mLens,.012,.1306,.105,true); BX(W,mSD,.02,.06,.07,.09,.012,.003,-.03);  // sight
    BX(W,mSD,.3,.31,.076,.1,.006,.002); BX(W,mSD,-.02,-.01,.076,.096,.012,.002);
    CY(W,mOD,.014,.45,.52,ub,0,14); CN(W,mOD,.014,.047,.52,.6,ub,0,18); CY(W,mOD,.047,.6,.7,ub,0,18); CN(W,mOD,.047,.014,.7,.86,ub,0,18); CY(W,mBr,.009,.86,.885,ub,0,10); CY(W,mSD,.0478,.62,.632,ub,0,18);
    trim(cylY(.0275,.05,18),W,0,-.22,-ub,null,null,'rpg');
    MK('rpg',[.89,ub],[.26,.024],[-.4,ub]); }

  // ---- grenade: a segmented body, fuse, safety lever and pin
  { const W=mkW('nade'), mG=gunSurf(0x4a5a34,4);
    p0(sph(.045),mG,W,0,-.03,0,null,[1,1.15,1]); for(const y of [-.052,-.03,-.008]) p0(new THREE.TorusGeometry(.0445*(y===-.03?1:.9),.0022,5,22),mSD,W,0,y,0,[Math.PI/2,0,0]);
    for(let q=0;q<6;q++){ const a=q/6*Math.PI; p0(new THREE.TorusGeometry(.0455,.002,5,22),mSD,W,0,-.03,0,[0,a,0],[1,1.15,1]); }
    p0(cylY(.014,.022,10),mSD,W,0,-.03,-.052,[Math.PI/2,0,0]); p0(rbox(.02,.03,.012,.004),mSG,W,0,-.03,-.068);
    p0(rbox(.014,.004,.07,.002),mSG,W,0,-.076,-.03,[.25,0,0]); p0(rbox(.014,.03,.004,.002),mSG,W,0,-.052,-.07,[-.5,0,0]);       // lever
    p0(new THREE.TorusGeometry(.014,.003,6,14),mBr,W,.022,-.03,-.07);
    rig.muzzle_nade=grp(W,0,-.05,0); rig.grip_nade=grp(W,-.03,-.03,.06); rig.mag_nade=grp(W,0,-.03,0); }

  // ---- pistol: polymer frame, steel slide with serrations, accessory rail
  { const W=mkW('pistol'); p0(prof(gripPts(.035,.007),.032,.006),mP,W,0,0,0); PF(W,mR,[[-.03,-.03],[-.058,-.03],[-.07,-.09],[-.042,-.09]],.0335,.001);
    PF(W,mP,[[-.072,.03],[.124,.03],[.124,.006],[.112,-.004],[.02,-.006],[-.02,.0],[-.072,.006]],.03,.004); TRIG(W,-.02,.007,.021);
    for(let q=0;q<3;q++) BX(W,mHole,.078+q*.012,.084+q*.012,-.0075,-.005,.02,.001); BX(W,mSD,-.094,-.034,-.126,-.114,.03,.003);
    const SL=grp(W,0,0,0); rig.slide_pistol=SL;
    PF(SL,mS,[[-.072,.03],[.126,.03],[.126,.058],[.118,.066],[-.064,.066],[-.072,.058]],.034,.005);
    for(let q=0;q<6;q++) BX(SL,mSD,-.062+q*.007,-.059+q*.007,.034,.062,.0355,.001); for(let q=0;q<3;q++) BX(SL,mSD,.094+q*.007,.097+q*.007,.034,.062,.0355,.001);
    BX(SL,mBr,.03,.076,.052,.0665,.018,.002,.009); BX(SL,mSD,.108,.116,.066,.074,.006,.002); BX(SL,mSD,-.066,-.056,.066,.074,.022,.002);
    CY(W,mBr,.0065,.12,.13,.045,0,12); p0(cylY(.004,.002,8),mHole,W,0,-.1306,-.045);
    TR(SL,'pistol',.02,.09,.036,.042,.0352);
    marks('pistol',[0,-.135,-.045],[0,0,0],[0,.035,.11]); }

  // ---- revolver: fluted cylinder in a steel frame, full underlug barrel with a rib, walnut grips
  { const W=mkW('revolver'), ub=.052;
    PF(W,mS,[[-.05,.066],[-.014,.078],[.088,.078],[.088,.012],[.03,-.004],[.0,-.004],[-.02,.02],[-.052,.03]],.03,.005);
    const CYL=grp(W,0,-.045,-.034); rig.cyl_revolver=CYL; p0(cylY(.031,.056,18),mS,CYL,0,0,0);
    for(let q=0;q<6;q++){ const a=q/6*Math.PI*2+Math.PI/6; p0(cylY(.0055,.04,8),mSD,CYL,Math.cos(a)*.0305,-.01,Math.sin(a)*.0305); }
    CY(W,mS,.0105,.088,.262,ub); PF(W,mS,[[.088,.012],[.256,.022],[.256,.046],[.088,.046]],.018,.006); BX(W,mS,.088,.262,.061,.068,.012,.002);
    PF(W,mSD,[[.225,.068],[.258,.068],[.258,.073],[.25,.08]],.006,.001); CY(W,mBr,.004,.092,.17,.03,0,8); p0(cylY(.0055,.002,8),mHole,W,0,-.2626,-ub);
    PF(W,mSD,[[-.056,.06],[-.04,.07],[-.062,.094],[-.072,.088]],.012,.003); BX(W,mSD,-.03,-.016,.078,.084,.014,.002);          // hammer, rear sight
    PF(W,mWal,[[-.018,.012],[-.05,.03],[-.078,.0],[-.112,-.085],[-.1,-.102],[-.06,-.106],[-.045,-.092],[-.025,-.04],[-.002,-.01]],.036,.011); PIN(W,mBrass,.007,.0375,-.056,-.03);
    TRIG(W,-.012,-.003,.021);
    TR(W,'revolver',.11,.2,.03,.036,.02);
    marks('revolver',[0,-.268,-ub],[0,0,0],[0,-.045,-.034]); }

  // ---- hand cannon: bright steel, a heavy fixed barrel with a sloped nose and a short slide behind it
  { const W=mkW('hcannon'); p0(prof(gripPts(.035,.007),.038,.006),mR,W,0,0,0);
    PF(W,mBr,[[-.076,.024],[.15,.024],[.15,.0],[.03,-.008],[-.02,.0],[-.076,.006]],.036,.004); TRIG(W,-.02,.007,.022); BX(W,mSD,-.096,-.034,-.128,-.114,.036,.003);
    PF(W,mBr,[[.07,.03],[.205,.03],[.205,.058],[.196,.08],[.07,.08]],.036,.011); BX(W,mSD,.075,.19,.08,.086,.014,.002); CY(W,mSD,.011,.196,.207,.052,0,12); p0(cylY(.0075,.002,10),mHole,W,0,-.2076,-.052);
    const SL=grp(W,0,0,0); rig.slide_hcannon=SL; PF(SL,mBr,[[-.076,.024],[.07,.024],[.07,.082],[-.062,.082],[-.076,.068]],.04,.006);
    for(let q=0;q<6;q++) TILT(SL,mSG,-.058+q*.009,.052,.003,.05,.0415,.25,.001); BX(SL,mHole,.02,.06,.066,.083,.02,.002,.008);
    BX(SL,mSD,-.07,-.058,.082,.091,.024,.002); BX(W,mSD,.185,.193,.086,.094,.006,.002); PF(SL,mSD,[[-.078,.05],[-.07,.05],[-.074,.074],[-.086,.07]],.012,.002);
    TR(W,'hcannon',.09,.18,.036,.043,.0375);
    marks('hcannon',[0,-.212,-.052],[0,0,0],[0,.035,.11]); }

  // ---- bolt-action sniper: olive thumbhole chassis, heavy fluted barrel, big brake, long scope, bipod
  { const W=mkW('sniper'), ub=.05; TRIG(W,-.028,.0);
    PF(W,mODp,[[-.09,-.002],[.07,-.008],[.4,.012],[.4,.038],[-.09,.038]],.05,.01);                                              // fore-end
    PF(W,mODp,[[.0,.0],[-.085,.04],[-.1,.086],[-.37,.086],[-.376,-.062],[-.352,-.068],[-.2,-.072],[-.09,-.112],[-.045,-.108],[-.03,-.05],[-.01,-.012]],.042,.008); PF(W,mHole,[[-.088,.022],[-.102,-.062],[-.15,-.056],[-.19,-.01],[-.175,.04],[-.125,.052]],.0432,.0005); // thumbhole stock
    BX(W,mSD,-.33,-.16,.09,.106,.034,.008); for(const f of [-.3,-.19]) POST(W,mS,.004,.082,.092,f); BX(W,mR,-.392,-.374,-.064,.088,.044,.006);   // cheek piece, butt pad
    CY(W,mS,.02,-.09,.2,.054,0,16); BX(W,mHole,.03,.1,.056,.07,.003,.001,.0195); RAIL(W,-.06,.17,.074);
    CN(W,mSD,.0135,.0105,.2,.72,ub,0,14); for(let q=0;q<4;q++){ const a=q*Math.PI/2+Math.PI/4; p0(rbox(.003,.34,.003,.001),mHole,W,Math.cos(a)*.0118,-.46,-ub+Math.sin(a)*.0118); }
    BRAKE(W,.72,ub,.016,.07); PF(W,mSD,[[.062,-.006],[.13,-.004],[.134,-.055],[.07,-.058]],.03,.004); BIPOD(W,.34,.012,.22);
    SCOPE(W,-.1,.25,.074,.028,.015);
    const BG=grp(W,0,.03,-.054); rig.bolt_sniper=BG; p0(cylY(.016,.07,12),mBr,BG,0,0,0); p0(cylX(.007,.05,8),mBr,BG,.04,.012,0); p0(sph(.013),mSD,BG,.068,.014,0);
    TR(W,'sniper',.16,.3,.022,.03,.0515); MK('sniper',[.79,ub],[.27,.004],[.1,-.09]); }

  // ---- hunting rifle: a one-piece walnut sporter, slim blued barrel, open sights, brass fittings
  { const W=mkW('hunting'), ub=.05;
    PF(W,mWal,[[.36,.02],[.36,.04],[-.06,.044],[-.078,.066],[-.105,.07],[-.36,.05],[-.365,-.07],[-.34,-.076],[-.16,-.02],[-.11,-.03],[-.1,-.09],[-.06,-.1],[-.045,-.09],[-.03,-.03],[0,-.006],[.1,-.008]],.042,.009);
    BX(W,mSD,-.378,-.363,-.072,.052,.044,.005); BX(W,mSD,.36,.372,.018,.042,.038,.006); PIN(W,mBrass,.006,.0445,-.075,-.07);
    CY(W,mS,.017,-.07,.17,.052,0,16); BX(W,mHole,.03,.1,.054,.066,.003,.001,.0165); CN(W,mSD,.011,.008,.17,.7,ub);
    PF(W,mSD,[[.655,.058],[.69,.058],[.69,.062],[.68,.072]],.006,.001); p0(sph(.003),mBrass,W,0,-.683,-.073); BX(W,mSD,.24,.27,.06,.07,.014,.002); TRIG(W,-.026,.006); BX(W,mS,.02,.11,-.012,-.007,.024,.002);
    const BG=grp(W,0,.03,-.052); rig.bolt_hunting=BG; p0(cylY(.0145,.07,12),mBr,BG,0,0,0); p0(cylX(.006,.045,8),mBr,BG,.036,.012,0); p0(sph(.012),mBr,BG,.06,.014,0);
    TR(W,'hunting',.3,.345,.021,.039,.0435); MK('hunting',[.705,ub],[.26,.009],[.06,-.04]); }

  // ---- scoped rifle: a skeleton laminate stock, slotted wooden handguard, long flash hider, ribbed magazine, side-mounted scope
  { const W=mkW('dmr'), ub=.055; GRIP(W,mLam,.004);
    PF(W,mS,[[-.1,-.004],[.16,-.004],[.16,.06],[.15,.072],[-.085,.072],[-.1,.06]],.04); for(let q=0;q<4;q++) BX(W,mSD,-.06+q*.045,-.052+q*.045,.06,.073,.041,.001);
    PF(W,mLam,[[-.1,.066],[-.36,.052],[-.36,.028],[-.1,.04]],.036,.007); PF(W,mLam,[[-.335,.052],[-.366,.052],[-.366,-.07],[-.342,-.074],[-.33,-.04]],.036,.007); PF(W,mLam,[[-.345,-.072],[-.34,-.046],[-.075,-.08],[-.07,-.106]],.034,.007);
    BX(W,mSD,-.3,-.16,.05,.074,.03,.01); BX(W,mSD,-.378,-.364,-.072,.054,.038,.004);
    PF(W,mLam,[[.16,.02],[.4,.026],[.4,.07],[.16,.074]],.044,.01); SLOTS(W,.2,4,.048,.026,.05,.06,.0222); BX(W,mSD,.39,.42,.02,.076,.046,.006);
    CY(W,mSD,.0075,.16,.66,ub); CY(W,mSD,.007,.42,.5,.073); BX(W,mSD,.49,.51,ub,.08,.014,.004); BX(W,mSD,.6,.615,ub,ub+.045,.01,.003); p0(new THREE.TorusGeometry(.011,.0025,6,14),mSD,W,0,-.6075,-(ub+.05),[Math.PI/2,0,0]);
    FLASH(W,.66,ub,.0105,.07); PF(W,mSD,[[.03,-.004],[.088,-.004],[.104,-.088],[.05,-.094]],.026,.004); for(const k of [.25,.5,.75]) BX(W,mS,.04+k*.014,.09+k*.014,-.008-k*.082,-.004-k*.082,.0275,.001);
    BX(W,mSD,-.02,.11,.03,.082,.006,.002,-.0225); RAIL(W,-.03,.12,.078); SCOPE(W,-.07,.2,.078,.021,.012);
    TR(W,'dmr',.2,.33,.03,.037,.0455); MK('dmr',[.735,ub],[.28,.023],[.075,-.12]); }

  // ---- burst rifle: a bullpup, the magazine behind the grip in a one-piece body, built-in tube sight, folding foregrip
  { const W=mkW('burst'), ub=.062; GRIP(W,mTan,.0);
    PF(W,mTan,[[-.365,.09],[-.365,-.06],[-.34,-.068],[-.215,-.068],[-.2,-.03],[-.1,-.024],[-.085,.0],[.06,.0],[.075,.02],[.11,.026],[.11,.09]],.05,.01);
    TILT(W,mTan,.005,-.056,.15,.014,.03,.78,.006); BX(W,mR,-.38,-.363,-.062,.092,.052,.006);                                         // hand guard bow, butt pad
    PF(W,mPG,[[-.2,-.06],[-.142,-.06],[-.128,-.19],[-.192,-.2]],.026,.004); for(const k of [.3,.6]) BX(W,mP,-.196+k*.01,-.138+k*.012,-.066-k*.13,-.06-k*.13,.0275,.001);   // magazine
    PF(W,mSG,[[-.25,.09],[.13,.09],[.13,.104],[-.25,.104]],.04,.004); BX(W,mHole,-.2,-.13,.07,.086,.003,.001,.0255);
    for(const f of [-.06,.09]) BX(W,mSG,f-.012,f+.012,.1,.14,.022,.004); CY(W,mSG,.017,-.085,.115,.152,0,16); LENS(W,mLens,.0145,.1156,.152,true); LENS(W,mLens,.0145,-.0856,.152,false);
    CY(W,mSD,.009,.11,.38,ub); CY(W,mS,.016,.11,.15,ub,0,12); FLASH(W,.38,ub,.012,.05); CY(W,mS,.016,.155,.19,ub,0,12); BX(W,mP,.156,.19,-.06,.05,.03,.012);   // barrel, foregrip
    TR(W,'burst',-.33,-.24,.02,.03,.0515); MK('burst',[.43,ub],[.19,.03],[-.165,-.21]); }

  // ---- heavy rifle: stamped receiver with a ribbed cover, laminate furniture, gas tube over the barrel, deeply curved magazine
  { const W=mkW('heavyar'), ub=.056; GRIP(W,mLam,.0);
    PF(W,mS,[[-.1,.0],[.19,.0],[.19,.05],[-.1,.05]],.04,.004); PF(W,mS,[[-.1,.05],[.16,.05],[.16,.07],[.15,.078],[-.08,.078],[-.1,.066]],.038,.009); for(let q=0;q<4;q++) BX(W,mSD,-.05+q*.045,-.042+q*.045,.066,.0795,.036,.002);
    for(const [f,u] of [[-.07,.02],[.0,.03],[.15,.03],[.17,.012]]) PIN(W,mSD,.004,.0415,f,u); BX(W,mHole,.03,.1,.052,.064,.003,.001,.0205); PIN(W,mSD,.005,.028,.1,.058,.026);
    BX(W,mSD,.16,.2,.05,.086,.03,.004); TILT(W,mSD,.2,.09,.07,.006,.014,.08,.002);                                              // rear sight block and leaf
    PF(W,mLam,[[.19,.006],[.33,.014],[.33,.05],[.19,.05]],.044,.011); CY(W,mLam,.0145,.2,.32,.078,0,12); CY(W,mSD,.008,.32,.41,.078); PF(W,mSD,[[.39,ub],[.43,ub],[.42,.086],[.4,.086]],.02,.004);
    CY(W,mSD,.0085,.19,.57,ub); CY(W,mS,.0025,.33,.55,ub-.014,0,6); BX(W,mSD,.5,.52,ub,ub+.052,.012,.003); p0(new THREE.TorusGeometry(.011,.0025,6,14),mSD,W,0,-.51,-(ub+.05),[Math.PI/2,0,0]);
    CY(W,mSD,.0115,.57,.6,ub,0,10); TILT(W,mSD,.602,ub+.004,.012,.02,.02,.5,.003);                                               // slanted muzzle brake
    BX(W,mS,.085,.15,-.012,.002,.036,.004); MAGP(W,mBake,.118,-.004,.2,.058,.1,.8,.026);
    PF(W,mLam,[[-.1,.046],[-.34,.02],[-.345,-.07],[-.325,-.076],[-.1,.004]],.036,.008); BX(W,mSD,-.356,-.342,-.072,.022,.038,.004);
    TR(W,'heavyar',-.04,.08,.008,.016,.0415); MK('heavyar',[.61,ub],[.265,.011],[.17,-.2]); }

  // ---- infantry rifle: a full wooden stock with a handguard over the barrel, box magazine, long slotted flash hider, aperture sight
  { const W=mkW('infantry'), ub=.054, mFg=gunSurf(0x5a3a22,2);
    PF(W,mWd,[[.33,.012],[.33,.038],[-.07,.042],[-.085,.064],[-.11,.068],[-.36,.046],[-.365,-.072],[-.34,-.078],[-.16,-.022],[-.11,-.032],[-.1,-.09],[-.06,-.1],[-.045,-.09],[-.03,-.03],[0,-.008],[.12,-.01]],.044,.009);
    BX(W,mS,-.378,-.363,-.074,.048,.046,.005); PF(W,mS,[[-.08,.04],[.17,.04],[.17,.066],[-.06,.072],[-.08,.06]],.036,.006); CY(W,mFg,.0165,.17,.4,.062,0,14); BX(W,mS,.325,.345,.01,.07,.048,.006);
    CY(W,mSD,.008,.17,.6,ub); CY(W,mSD,.008,.4,.52,ub-.021); BX(W,mSD,.51,.525,ub-.03,ub+.01,.014,.003); FLASH(W,.6,ub,.011,.08);
    BX(W,mSD,.6,.612,ub,ub+.04,.008,.002); for(const sx of [-1,1]) BX(W,mSD,.598,.614,ub+.012,ub+.045,.003,.001,sx*.009);         // front sight and its wings
    BX(W,mSD,-.072,-.04,.068,.078,.03,.004); for(const sx of [-1,1]) BX(W,mSD,-.07,-.05,.076,.094,.004,.001,sx*.013); POST(W,mSD,.006,.078,.09,-.058);
    BX(W,mS,.02,.16,.05,.058,.006,.002,.02); PIN(W,mS,.006,.024,.03,.054,.03); TRIG(W,-.026,.008);
    PF(W,mSD,[[.02,-.008],[.085,-.008],[.092,-.1],[.03,-.106]],.028,.004); BX(W,mS,.026,.094,-.112,-.102,.03,.003);
    TR(W,'infantry',.15,.25,.016,.024,.0455); MK('infantry',[.685,ub],[.25,.0],[.06,-.13]); }

  // ---- tactical shotgun: black, pistol grip and a tube stock, top rail with ghost-ring sights, shells in a side carrier
  { const W=mkW('tac'), ub=.066, ut=.04; GRIP(W,mR,.0);
    PF(W,mS,[[-.07,.0],[.2,.0],[.2,.082],[-.04,.082],[-.07,.06]],.044,.006); RAIL(W,-.03,.18,.082); BX(W,mHole,.05,.14,.046,.066,.003,.001,.0225); PIN(W,mS,.005,.03,.1,.056,.028);
    BX(W,mSD,-.035,-.02,.09,.114,.024,.004); BX(W,mHole,-.036,-.019,.098,.108,.012,.001);                                        // ghost ring
    CY(W,mSD,.012,-.3,-.06,.05); PF(W,mP,[[-.255,.08],[-.33,.08],[-.336,-.05],[-.31,-.056],[-.29,.02],[-.255,.03]],.04,.006); BX(W,mR,-.348,-.334,-.052,.082,.042,.004); BX(W,mP,-.25,-.15,.06,.08,.03,.008);
    CY(W,mSD,.0115,.2,.66,ub); CY(W,mSD,.011,.2,.6,ut); CY(W,mS,.0125,.6,.618,ut); BX(W,mSD,.555,.57,ut-.012,ub+.013,.03,.006);
    PF(W,mP,[[.2,.014],[.43,.02],[.43,.056],[.2,.056]],.05,.014); for(let q=0;q<6;q++) BX(W,mR,.225+q*.032,.24+q*.032,.016,.05,.0515,.003);
    BX(W,mSD,.635,.648,ub+.01,ub+.03,.006,.002); for(const sx of [-1,1]) BX(W,mSD,.63,.652,ub+.008,ub+.034,.003,.001,sx*.009);
    BX(W,mP,.01,.13,.008,.06,.008,.003,-.026); for(let q=0;q<5;q++){ POST(W,mShell,.0095,.014,.058,.024+q*.023,-.034); POST(W,mBrass,.0098,.008,.016,.024+q*.023,-.034); }
    TR(W,'tac',.03,.15,.066,.074,.0455); MK('tac',[.665,ub],[.32,.016],[.1,-.03]); }

  // ---- double barrel: side-by-side barrels on a bright engraved action with twin hammers, walnut stock and fore-end
  { const W=mkW('dbarrel');
    p0(rbox(.058,.13,.07,.01),mBr,W,0,-.045,-.04); p0(rbox(.06,.05,.004,.002),mSD,W,0,-.06,-.076); for(const sx of [-1,1]){ p0(rbox(.008,.03,.03,.003),mSD,W,sx*.02,.012,-.082,[.5,0,0]); p0(rbox(.004,.07,.03,.001),mSG,W,sx*.0295,-.05,-.04); }
    const HB=grp(W,0,-.11,-.012); rig.hinge_dbarrel=HB;                                                                // hinge pin: barrels tip down to load
    [-1,1].forEach(sx=>p0(cylY(.018,.46,14),mSD,HB,sx*.019,-.23,-.038)); p0(rbox(.012,.46,.012,.003),mS,HB,0,-.23,-.057); p0(sph(.006),mBrass,HB,0,-.455,-.066);
    [-1,1].forEach(sx=>p0(new THREE.CircleGeometry(.012,12),mBrass,HB,sx*.019,.0005,-.038,[-Math.PI/2,0,0]));          // shell rims, seen when open
    p0(rbox(.054,.22,.038,.012),mWal,HB,0,-.12,-.008); p0(rbox(.055,.14,.004,.002),mWalD,HB,0,-.12,.008);              // fore-end
    p0(prof([[.005,-.075],[.33,-.062],[.335,.058],[.315,.064],[.14,.012],[.085,.01],[.105,.088],[.098,.1],[.055,.104],[.045,.094],[.03,.05],[.012,.012],[0,-.01]],.044,.008),mWal,W,0,0,0); // stock + grip
    p0(rbox(.046,.016,.122,.005),mSD,W,0,.342,-.001);
    p0(new THREE.TorusGeometry(.024,.004,6,12,Math.PI),mBr,W,0,-.03,-.005,GUARD); [-.026,-.012].forEach(y=>p0(rbox(.005,.006,.02,.002),mSD,W,0,y,.008,[-.3,0,0]));
    trim(rbox(.062,.05,.03,.004),W,0,-.06,-.035,null,null,'dbarrel');
    rig.muzzle_dbarrel=grp(HB,0,-.465,-.038); rig.grip_dbarrel=grp(HB,0,-.12,.011); rig.mag_dbarrel=grp(W,0,-.1,-.05); }

  // ---- heavy shotgun: a long boxy one-piece body, big drum magazine, shrouded barrel, raised sight bar
  { const W=mkW('heavysg'), ub=.06; GRIP(W,mP,.0);
    PF(W,mPG,[[-.36,.1],[-.36,-.045],[-.33,-.052],[-.13,-.014],[-.09,.0],[.26,.0],[.26,.1]],.058,.012); BX(W,mR,-.375,-.358,-.047,.102,.06,.006);
    BX(W,mP,-.1,.2,.1,.113,.026,.004); for(const f of [-.09,.19]) BX(W,mSD,f-.01,f+.01,.113,.132,.02,.004); BX(W,mHole,.03,.12,.05,.074,.003,.001,.0295); PIN(W,mS,.006,.03,.16,.085,.032);
    CY(W,mSD,.022,.26,.44,ub,0,16); for(let q=0;q<4;q++) for(const a of [-.6,.6,Math.PI-.6,Math.PI+.6]) p0(cylX(.005,.006,8),mHole,W,Math.cos(a)*.021,-.29-q*.04,-ub+Math.sin(a)*.021,[0,-a,0]);
    CY(W,mSD,.0145,.44,.5,ub); CY(W,mS,.017,.488,.5,ub,0,12); p0(cylY(.0105,.002,10),mHole,W,0,-.5006,-ub);
    BX(W,mSD,.055,.125,-.03,.0,.04,.004); p0(cylX(.074,.06,26),mSD,W,0,-.09,.085); p0(cylX(.03,.066,16),mS,W,0,-.09,.085); for(let q=0;q<8;q++) p0(rbox(.063,.004,.04,.001),mS,W,0,-.09-Math.sin(q*Math.PI/4)*.052,.085+Math.cos(q*Math.PI/4)*.052,[q*Math.PI/4,0,0]);
    TR(W,'heavysg',-.3,-.16,.06,.07,.0595); MK('heavysg',[.505,ub],[.35,.038],[.09,-.18]); }

  // ---- compact SMG: a stamped box receiver with the magazine up through the grip, stubby barrel, wire stock
  { const W=mkW('csmg'), ub=.045;
    PF(W,mS,[[-.12,.012],[.16,.012],[.16,.07],[.15,.078],[-.11,.078],[-.12,.07]],.044,.004); for(const u of [.03,.05]) BX(W,mSD,-.1,.14,u-.003,u+.003,.0455,.002);
    PF(W,mP,[[-.078,.014],[-.008,.014],[-.014,-.1],[-.072,-.1]],.036,.007); PF(W,mR,[[-.07,-.01],[-.018,-.01],[-.022,-.09],[-.066,-.09]],.0375,.001); TRIG(W,-.034,-.012,.022);
    BX(W,mSD,-.064,-.022,-.235,-.1,.024,.003); BX(W,mS,-.068,-.018,-.243,-.232,.028,.003);
    POST(W,mP,.009,.078,.096,.05); BX(W,mSD,.13,.142,.078,.098,.006,.002); for(const sx of [-1,1]){ BX(W,mSD,.126,.146,.078,.1,.003,.001,sx*.01); BX(W,mSD,-.1,-.08,.078,.1,.003,.001,sx*.01); }
    CY(W,mSD,.009,.16,.225,ub); CY(W,mS,.0165,.16,.186,ub,0,10); PF(W,mP,[[.02,.014],[.15,.014],[.15,-.012],[.035,-.012]],.042,.009);
    for(const sx of [-1,1]) BX(W,mSD,-.3,-.12,.05,.058,.006,.003,sx*.017); BX(W,mSD,-.312,-.298,.0,.078,.042,.004);
    TR(W,'csmg',-.05,.05,.058,.066,.0455); MK('csmg',[.23,ub],[.095,-.012],[-.043,-.25]); }

  // ---- suppressed SMG: grey, a fat shrouded suppressor for a handguard, wire stock, straight magazine, holographic sight
  { const W=mkW('ssmg'), ub=.058; GRIP(W,mPG,.0);
    PF(W,mPG,[[-.086,.03],[-.086,.0],[.05,.0],[.06,-.03],[.105,-.03],[.11,.03]],.042); PF(W,mSG,[[-.09,.03],[.12,.03],[.12,.084],[-.076,.084],[-.09,.07]],.046); RAIL(W,-.07,.34,.084);
    BX(W,mHole,.01,.06,.05,.066,.003,.001,.0235); PIN(W,mSD,.005,.03,.09,.066,-.026);
    CY(W,mSG,.027,.12,.36,ub,0,18); for(let q=0;q<5;q++) for(const a of [-.5,.5,Math.PI-.5,Math.PI+.5]) p0(cylX(.0055,.006,8),mHole,W,Math.cos(a)*.026,-.15-q*.044,-ub+Math.sin(a)*.026,[0,-a,0]);
    SUPP(W,.36,ub,.021,.13,mSD);
    for(const sx of [-1,1]) CY(W,mSD,.005,-.26,-.09,.052,sx*.018,8); PF(W,mP,[[-.26,.082],[-.292,.082],[-.292,-.03],[-.272,-.036],[-.26,.0]],.046,.006);
    PF(W,mSD,[[.064,-.03],[.1,-.03],[.108,-.17],[.07,-.172]],.022,.003); HOLO(W,.02,.0925);
    TR(W,'ssmg',.0,.1,.036,.044,.0475); MK('ssmg',[.49,ub],[.24,.031],[.09,-.2]); }

  // ---- light machine gun: a flat pan magazine on top, perforated barrel shroud, cone flash hider, wooden stock, bipod
  { const W=mkW('lmg'), ub=.05; GRIP(W,mWd,.0);
    PF(W,mS,[[-.1,.0],[.2,.0],[.2,.062],[-.1,.062]],.04,.005); BX(W,mHole,.05,.12,.03,.046,.003,.001,.0205); PIN(W,mS,.006,.03,.14,.03,.028);
    POST(W,mSD,.105,.066,.086,.06,0,30); POST(W,mS,.1,.086,.09,.06,0,30); POST(W,mSD,.03,.09,.097,.06,0,16); for(let q=0;q<12;q++){ const a=q*Math.PI/6; p0(rbox(.07,.006,.004,.001),mSD,W,Math.cos(a)*.064,-.06+Math.sin(a)*.064,-.091,[0,0,a]); }   // pan magazine
    PF(W,mWd,[[-.1,.054],[-.33,.03],[-.336,-.075],[-.312,-.08],[-.2,-.03],[-.1,-.004]],.04,.009); BX(W,mSD,-.348,-.334,-.077,.032,.042,.004);
    CY(W,mS,.02,.2,.5,ub,0,16); for(let q=0;q<6;q++) for(const a of [-.6,.6,Math.PI-.6,Math.PI+.6]) p0(cylX(.006,.006,8),mHole,W,Math.cos(a)*.019,-.23-q*.045,-ub+Math.sin(a)*.019,[0,-a,0]);
    CY(W,mSD,.0095,.5,.62,ub); CN(W,mSD,.011,.025,.62,.68,ub,0,16); CY(W,mSD,.009,.2,.52,ub-.031); BX(W,mSD,.55,.565,ub,ub+.04,.008,.002); for(const sx of [-1,1]) BX(W,mSD,.546,.569,ub+.012,ub+.044,.003,.001,sx*.009);
    BX(W,mSD,-.06,-.03,.062,.08,.02,.004); BIPOD(W,.5,ub-.04,.2);
    TR(W,'lmg',-.06,.04,.012,.022,.0415); MK('lmg',[.685,ub],[.33,.01],[.06,.1]); }

  // ---- grenade launcher: a six-chamber cylinder, short fat barrel, top rail with a reflex sight, foregrip, folding stock
  { const W=mkW('glauncher'), ub=.045; GRIP(W,mP,.01);
    BX(W,mS,-.06,.06,-.01,.08,.044,.008); CY(W,mOD,.066,.06,.2,ub,0,22); for(let q=0;q<6;q++){ const a=q/6*Math.PI*2+Math.PI/6; p0(cylY(.021,.142,12),mOD,W,Math.cos(a)*.05,-.13,-ub+Math.sin(a)*.05); }
    for(const f of [.062,.198]) CY(W,mSD,.0675,f-.004,f+.004,ub,0,22); CY(W,mS,.05,.2,.216,ub,0,18);
    CY(W,mSD,.026,.216,.47,ub,0,16); CY(W,mS,.03,.45,.47,ub,0,16); p0(cylY(.021,.002,14),mHole,W,0,-.4706,-ub);
    BX(W,mS,-.05,.3,ub+.068,ub+.078,.022,.003); RAIL(W,-.04,.29,ub+.078); HOLO(W,.06,ub+.0865);
    BX(W,mSD,.27,.33,.008,.02,.03,.004); TILT(W,mP,.3,-.036,.03,.09,.03,.12,.011);                                               // foregrip
    CY(W,mSD,.007,-.28,-.06,.06); BX(W,mR,-.3,-.28,-.02,.088,.04,.009);
    TR(W,'glauncher',-.05,.05,.082,.09,.0455); MK('glauncher',[.48,ub],[.315,.005],[.13,ub]); }

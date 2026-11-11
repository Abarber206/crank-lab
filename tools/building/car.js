  } else if(p.kind==='car'){
    /* A car: the lower body is its side profile (with wheel arches) extruded across and rounded at the edges; the
       cabin is a narrower block of tinted glass on top, with a painted roof panel and pillars along its edges. Then
       tyres with hubcaps, bumpers, lights, grille, plates, mirrors, door seams, handles and a dark sill. Four body
       styles (sedan, hatchback, pickup, SUV) and eight paints; a few are rusting. */
    const style=variant%4, paint=[0xc23b2f,0x2f6fb0,0xd9a62b,0x2f8f86,0xe6e6df,0x34373e,0x5f8a4e,0xd8702f][variant], rusty=variant===2||variant===5||variant===7;
    const dk=new THREE.Color(paint).multiplyScalar(0.55).getHex(), glass=0x2c3e50, trim=0x2a2d33, chrome=0xc4cad1;
    const W=1.6, BV=.1, HW=W/2+BV, wx=1.3, wr=.42;
    const S=[ // lower body top line (rear bumper round to the nose), cabin [rear base, rear top, front top, front base], B pillars
      {low:[[-1.98,.95],[-1.55,1.03],[1.7,1.0],[1.98,.84]], cab:[[-1.1,1.0],[-.62,1.47],[.42,1.47],[1.0,1.0]], pil:[-.1]},
      {low:[[-1.96,1.04],[1.7,1.0],[1.98,.84]], cab:[[-1.9,1.0],[-1.64,1.5],[.4,1.5],[1.0,1.0]], pil:[-.66,.02]},
      {low:[[-1.98,1.06],[1.74,1.03],[1.98,.88]], cab:[[-.44,1.0],[-.44,1.62],[.5,1.62],[1.04,1.0]], pil:[]},
      {low:[[-1.97,1.08],[1.74,1.06],[1.98,.9]], cab:[[-1.93,1.04],[-1.9,1.71],[.56,1.72],[1.1,1.04]], pil:[-1.2,-.32]}][style];
    const ext=(shape,depth,bv,bs,seg)=>{ const e=new THREE.ExtrudeGeometry(shape,{depth,bevelEnabled:true,bevelThickness:bv,bevelSize:bs,bevelSegments:seg||2,curveSegments:10}); e.translate(0,0,-depth/2); return e; };
    // lower body with wheel arches
    const sh=new THREE.Shape(), y0=.36;
    sh.moveTo(1.98,y0); sh.lineTo(wx+wr+.08,y0); sh.absarc(wx,y0+.02,wr+.08,0,Math.PI,false); sh.lineTo(-wx+wr+.08,y0);
    sh.absarc(-wx,y0+.02,wr+.08,0,Math.PI,false); sh.lineTo(-1.98,y0); S.low.forEach(([x,y])=>sh.lineTo(x,y)); sh.lineTo(1.98,y0);
    propPart(ext(sh,W,BV,.07,3),paint,g,0,0,0,0,0,0,0);
    // the cabin: tinted glass, a little narrower than the body
    const [c0,c1,c2,c3]=S.cab, cs=new THREE.Shape(); cs.moveTo(c0[0],c0[1]-.04); cs.lineTo(c1[0],c1[1]); cs.lineTo(c2[0],c2[1]); cs.lineTo(c3[0],c3[1]-.04); cs.lineTo(c0[0],c0[1]-.04);
    const CW=W-.1; propPart(ext(cs,CW,.05,.02,1),glass,g,0,0,0,0,0,0,0);
    const CH=CW/2+.05; // cabin half-width
    // roof panel and pillars in the body colour
    const rs=new THREE.Shape(); rs.moveTo(c1[0]-.03,c1[1]-.05); rs.lineTo(c1[0]-.01,c1[1]+.035); rs.lineTo(c2[0]+.01,c2[1]+.035); rs.lineTo(c2[0]+.03,c2[1]-.05); rs.lineTo(c1[0]-.03,c1[1]-.05);
    propPart(ext(rs,CW+.02,.04,.02,1),paint,g,0,0,0,0,0,0,0);
    const pillar=(a,b)=>{ const dx=b[0]-a[0], dy=b[1]-a[1], L=Math.hypot(dx,dy), ang=Math.atan2(dy,dx);
      for(const sz of [-1,1]) propPart(rbox(L+.04,.08,.06,.02),paint,g,(a[0]+b[0])/2,(a[1]+b[1])/2,sz*(CH+.005),0,0,ang,0); };
    pillar(c3,c2); pillar(c0,c1); // A and C pillars along the glass edges
    S.pil.forEach(x=>{ const yb=1.0, yt=c1[1]+(c2[1]-c1[1])*(x-c1[0])/(c2[0]-c1[0]); for(const sz of [-1,1]) propPart(rbox(.09,yt-yb,.06,.02),paint,g,x,(yt+yb)/2,sz*(CH+.005),0,0,0,0); });
    if(style===2){ propPart(rbox(1.4,.05,W-.06,.02),0x23262b,g,-1.2,1.07,0,0,0,0,0); // the open bed with its rails
      for(const sz of [-1,1]) propPart(rbox(1.52,.08,.07,.03),dk,g,-1.2,1.12,sz*(HW-.04),0,0,0,0);
      propPart(rbox(.07,.08,HW*2-.08,.03),dk,g,-1.95,1.12,0,0,0,0,0); }
    if(style===3) for(const sz of [-1,1]) propPart(rbox(1.9,.05,.06,.02),trim,g,-.7,1.79,sz*.6,0,0,0,0); // roof rails
    // wheels: tyre, hubcap, hub
    for(const [x,z] of [[wx,1],[-wx,1],[wx,-1],[-wx,-1]]){ const zz=z*(HW-.12);
      const t=new THREE.CylinderGeometry(wr,wr,.3,18); t.rotateX(Math.PI/2); propPart(t,0x1b1d21,g,x,wr,zz,0,0,0,0);
      const hc=new THREE.CylinderGeometry(.24,.26,.32,12); hc.rotateX(Math.PI/2); propPart(hc,rusty?0x8a8f96:chrome,g,x,wr,zz,0,0,0,0);
      const nut=new THREE.CylinderGeometry(.07,.07,.34,8); nut.rotateX(Math.PI/2); propPart(nut,0x5a5f66,g,x,wr,zz,0,0,0,0); }
    // bumpers, grille, lights, plates (just proud of the rounded nose and tail)
    const noseY=S.low[S.low.length-1][1], hoodY=S.low[S.low.length-2][1], tailY=S.low[0][1], bump=style>=2?trim:chrome;
    propPart(rbox(.22,.26,HW*2+.04,.08),bump,g,2.0,.5,0,0,0,0,0); propPart(rbox(.22,.26,HW*2+.04,.08),bump,g,-2.0,.5,0,0,0,0,0);
    propPart(rbox(.06,Math.max(.14,noseY-.7),.9,.02),trim,g,2.06,(noseY+.64)/2,0,0,0,0,0);
    for(const sz of [-1,1]){ propPart(rbox(.06,.13,.34,.03),0xfff2c4,g,2.05,noseY-.13,sz*.6,0,0,0,0);
      propPart(rbox(.06,.15,.3,.03),0xc8262b,g,-2.05,tailY-.14,sz*.62,0,0,0,0); }
    propPart(rbox(.03,.13,.42,.01),0xf2f0e6,g,-2.12,.5,0,0,0,0,0); propPart(rbox(.03,.13,.42,.01),0xf2f0e6,g,2.12,.5,0,0,0,0,0);
    // mirrors, door seams and handles, a dark sill
    for(const sz of [-1,1]){ propPart(rbox(.16,.12,.16,.04),paint,g,c3[0]-.08,1.08,sz*(HW+.06),0,0,0,0);
      propPart(rbox(2.9,.12,.04,.03),dk,g,0,.45,sz*(HW-.005),0,0,0,0);
      const doors=style===2?[1.0,-.4]:style===1?[1.0,.0,-.66]:style===3?[1.06,-.3,-1.2]:[1.0,-.08,-1.08];
      doors.forEach(x=>propPart(rbox(.025,.5,.03,.005),0x1c1e22,g,x,.76,sz*(HW+.004),0,0,0,0));
      doors.slice(0,-1).forEach(x=>propPart(rbox(.16,.035,.03,.01),chrome,g,x-.24,.9,sz*(HW+.008),0,0,0,0)); }
    if(rusty){ for(let k=0;k<4;k++){ const sz=q()<.5?-1:1; propPart(rbox(.3+q()*.4,.16+q()*.18,.03,.04),0x7a4224,g,(q()-.5)*2.6,.55+q()*.3,sz*(HW+.006),0,0,0,0); }
      propPart(rbox(.6,.03,.55,.03),0x8a4a2a,g,1.4,hoodY+.08,(q()-.5)*.5,0,0,0,0); }

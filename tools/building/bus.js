function brBusModel(){ if(BRBUS.g) return BRBUS.g;
  // The battle bus: a proper city bus (rounded body, a row of side windows, a raked windscreen with a lit destination
  // sign, a folding door, wheel arches with hubcaps, lights, mirrors, a roof pod) slung under a big striped hot-air
  // balloon on four straps, with a load ring and a burner that roars now and then. The front of the bus is -z.
  const g=new THREE.Group(), BL=0x2c6fe0, BLD=0x1f53b0, WH=0xf4f6f8;
  const L=(c,o)=>new THREE.MeshLambertMaterial(Object.assign({color:c},o||{})), PH=(c,s,o)=>new THREE.MeshPhongMaterial(Object.assign({color:c,specular:s||0x445566,shininess:60},o||{}));
  const paint=PH(BL,0x6688aa), paintD=PH(BLD,0x445577), white=PH(WH,0x888888), glass=PH(0x18283c,0xbcd4ee,{shininess:110}), chrome=PH(0xc9ced4,0xffffff,{shininess:90}), dark=L(0x1b1d22), rub=L(0x15161a);
  const add=(geo,mat,x,y,z,sh)=>{ const m=new THREE.Mesh(geo,mat); m.position.set(x,y,z); m.castShadow=sh!==false; g.add(m); return m; };
  const box=(w,h,d,mat,x,y,z,r)=>add(rbox(w,h,d,r==null?Math.min(w,h,d)*0.12:r),mat,x,y,z);
  const W=2.62, LEN=10.4, Y0=-1.05; // width, length, the floor line
  // body: a dark skirt, the blue body, a white window band, a white roof with rounded edges
  box(W,0.62,LEN,paintD,0,Y0+0.05,0,0.2); box(W+0.02,1.18,LEN-0.06,paint,0,Y0+0.92,0,0.24); box(W+0.03,0.12,LEN-0.1,white,0,Y0+0.38,0,0.05); // skirt, body, rub strip
  box(W,1.08,LEN-0.2,white,0,Y0+1.98,0,0.34); box(W-0.18,0.28,LEN-0.6,white,0,Y0+2.52,0,0.14);                                           // window band and roof
  // side windows: a row of tinted panes with pillars, both sides (the front one is the door on the right)
  const nW=6, wz0=-LEN/2+2.15, wz1=LEN/2-0.75, step=(wz1-wz0)/nW;
  for(const s of [-1,1]) for(let i=0;i<nW;i++){ const z=wz0+step*(i+0.5); add(rbox(0.06,0.78,step-0.22,0.05),glass,s*(W/2+0.005),Y0+2.02,z,false); }
  // the door: two tall panes, right side, behind the front wheel
  for(const dz of [-0.33,0.33]) add(rbox(0.06,1.75,0.58,0.05),glass,W/2+0.006,Y0+1.25,-LEN/2+1.45+dz,false);
  add(new THREE.BoxGeometry(0.07,1.85,0.06),chrome,W/2+0.01,Y0+1.25,-LEN/2+1.45,false);
  // windscreen (raked), destination sign above it, rear window
  { const ws=add(rbox(W-0.32,1.25,0.08,0.06),glass,0,Y0+1.9,-LEN/2-0.02,false); ws.rotation.x=-0.12; }
  { const c=document.createElement('canvas'); c.width=256; c.height=40; const x=c.getContext('2d'); x.fillStyle='#120d02'; x.fillRect(0,0,256,40); x.fillStyle='#ffb52e'; x.font='bold 28px monospace'; x.textAlign='center'; x.textBaseline='middle'; x.fillText('CRANK LAB',128,21);
    const t=new THREE.CanvasTexture(c); add(new THREE.PlaneGeometry(1.9,0.3),new THREE.MeshBasicMaterial({map:t}),0,Y0+2.66,-LEN/2+0.04-0.002,false).rotation.y=Math.PI; }
  add(rbox(W-0.5,0.85,0.06,0.05),glass,0,Y0+2.05,LEN/2+0.01,false);
  // side livery: the name along each side, and a yellow stripe
  { const c=document.createElement('canvas'); c.width=512; c.height=64; const x=c.getContext('2d'); x.font='italic 900 46px sans-serif'; x.textAlign='center'; x.textBaseline='middle'; x.lineWidth=8; x.strokeStyle='#0d2a66'; x.strokeText('BATTLE BUS',256,34); x.fillStyle='#ffffff'; x.fillText('BATTLE BUS',256,34);
    const t=new THREE.CanvasTexture(c), m=new THREE.MeshBasicMaterial({map:t,transparent:true}); for(const s of [-1,1]){ const p=add(new THREE.PlaneGeometry(4.6,0.58),m,s*(W/2+0.03),Y0+1.0,0.6,false); p.rotation.y=s*Math.PI/2; } }
  box(W+0.04,0.1,LEN-0.3,L(0xffc531),0,Y0+1.5,0,0.04);
  // front: grille, headlights, indicators, bumper, plate; back: tail lights, bumper, engine grille, exhaust
  const F=-LEN/2;
  box(1.3,0.42,0.06,dark,0,Y0+0.85,F-0.01,0.03); for(let i=0;i<4;i++) box(1.2,0.04,0.02,chrome,0,Y0+0.7+i*0.1,F-0.045,0);
  for(const s of [-1,1]){ add(new THREE.CylinderGeometry(0.17,0.17,0.08,16).rotateX(Math.PI/2),new THREE.MeshBasicMaterial({color:0xfff6cf}),s*0.98,Y0+0.85,F-0.03,false); box(0.22,0.12,0.06,L(0xff9a1f,{emissive:0x5a2a00}),s*0.98,Y0+0.58,F-0.02,0.03); }
  box(W+0.06,0.32,0.22,rub,0,Y0+0.2,F-0.05,0.08); box(0.62,0.17,0.03,L(0xf5f2e2),0,Y0+0.22,F-0.17,0.02);
  box(W+0.06,0.32,0.22,rub,0,Y0+0.2,-F+0.05,0.08); box(1.6,0.5,0.04,dark,0,Y0+0.85,-F+0.01,0.03);
  for(const s of [-1,1]) box(0.2,0.42,0.06,L(0xd8241c,{emissive:0x400000}),s*1.06,Y0+1.0,-F+0.01,0.03);
  add(new THREE.CylinderGeometry(0.07,0.07,0.5,10).rotateX(Math.PI/2),chrome,-0.9,Y0-0.12,-F+0.05);
  // mirrors on arms
  for(const s of [-1,1]){ box(0.5,0.05,0.05,dark,s*(W/2+0.2),Y0+2.25,F+0.18,0.02); box(0.07,0.46,0.22,dark,s*(W/2+0.43),Y0+2.0,F+0.18,0.03); }
  // wheels with arches and hubcaps
  for(const [zz,s] of [[F+1.95,-1],[F+1.95,1],[-F-2.25,-1],[-F-2.25,1]]){
    box(0.06,0.78,1.42,dark,s*(W/2+0.004),Y0+0.05,zz,0.03); // the wheel well
    const tyre=add(new THREE.CylinderGeometry(0.55,0.55,0.38,22).rotateZ(Math.PI/2),rub,s*(W/2-0.2),Y0-0.28,zz); add(new THREE.CylinderGeometry(0.3,0.3,0.06,16).rotateZ(Math.PI/2),chrome,s*(W/2-0.0),Y0-0.28,zz,false);
    add(new THREE.CylinderGeometry(0.09,0.09,0.08,8).rotateZ(Math.PI/2),dark,s*(W/2+0.03),Y0-0.28,zz,false); }
  // roof: a pod (air conditioning) and the four strap hooks
  box(1.5,0.3,2.4,white,0,Y0+2.78,1.2,0.12); box(1.2,0.08,1.9,L(0xb9c0c8),0,Y0+2.95,1.2,0.04);
  const HK=[[-1.05,-3.9],[1.05,-3.9],[-1.05,3.9],[1.05,3.9]]; for(const [x,z] of HK) box(0.18,0.2,0.18,chrome,x,Y0+2.72,z,0.05);
  // the balloon: a smooth teardrop envelope in alternating gores, a yellow band, the skirt and the load ring
  const B=new THREE.Group(); B.position.y=Y0+14.5; g.add(B); BRBUS.balloon=B; const R=7.2, prof=[];
  for(let i=0;i<=24;i++){ const t=i/24, a=-Math.PI/2+t*Math.PI*1.08; let r=Math.cos(Math.min(a,Math.PI/2))*R, y=Math.sin(Math.min(a,Math.PI/2))*R*1.08; if(t<0.32){ const k=t/0.32; r=0.9*R*0.32+(r-0.9*R*0.32)*k*k*(3-2*k)+ (1-k)*R*0.02; } prof.push(new THREE.Vector2(Math.max(0.01,r),y)); }
  prof[0].set(R*0.29,-R*1.0); // the open mouth at the bottom
  const env=new THREE.LatheGeometry(prof,48), col=[], cA=new THREE.Color(0x2f72e6), cB=new THREE.Color(0xf6f7f9), cY=new THREE.Color(0xffc531);
  // (colour by triangle, so the gores have crisp edges)
  const envN=env.toNonIndexed(), pn=envN.attributes.position; for(let i=0;i<pn.count;i+=3){ let x=0,z=0,y0=1e9,y1=-1e9; for(let k=0;k<3;k++){ x+=pn.getX(i+k); z+=pn.getZ(i+k); y0=Math.min(y0,pn.getY(i+k)); y1=Math.max(y1,pn.getY(i+k)); } const y=(y0+y1)/2;
    const seg=Math.floor(((Math.atan2(z,x)+Math.PI)/(Math.PI*2))*12)%12, band=Math.abs(y+R*0.55)<R*0.09, c=band?cY:seg%2?cA:cB; for(let k=0;k<3;k++) col.push(c.r,c.g,c.b); }
  envN.setAttribute('color',new THREE.Float32BufferAttribute(col,3));
  const envM=new THREE.Mesh(envN,new THREE.MeshPhongMaterial({vertexColors:true,specular:0x2a2a2a,shininess:20,emissive:0x262a30,side:THREE.DoubleSide})); envM.castShadow=true; B.add(envM);
  { const top=new THREE.Mesh(new THREE.CylinderGeometry(1.1,1.1,0.2,24),PH(0xffc531)); top.position.y=R*1.08+0.02; B.add(top); }
  // load ring and burner just under the mouth
  const ringY=-R*1.0-2.2; { const ring=new THREE.Mesh(new THREE.TorusGeometry(1.25,0.07,8,28).rotateX(Math.PI/2),chrome); ring.position.y=ringY; B.add(ring);
    const bur=new THREE.Mesh(new THREE.CylinderGeometry(0.42,0.5,0.55,14),dark); bur.position.y=ringY+0.35; B.add(bur);
    for(let i=0;i<4;i++){ const a=i*Math.PI/2+Math.PI/4, s=new THREE.Mesh(new THREE.CylinderGeometry(0.035,0.035,2.3,6),chrome); s.position.set(Math.cos(a)*0.95,ringY+1.1,Math.sin(a)*0.95); s.rotation.set(Math.sin(a)*0.25,0,-Math.cos(a)*0.25); B.add(s); } // ring to the mouth
    const fl=new THREE.Mesh(new THREE.ConeGeometry(0.42,2.0,12),new THREE.MeshBasicMaterial({color:0xffa030,transparent:true,opacity:0.85,depthWrite:false})); fl.position.y=ringY+1.6; B.add(fl); BRBUS.flame=fl;
    const fc=new THREE.Mesh(new THREE.ConeGeometry(0.2,1.2,10),new THREE.MeshBasicMaterial({color:0xfff2b0,transparent:true,opacity:0.9,depthWrite:false})); fc.position.y=ringY+1.3; fl.add(fc); fc.position.set(0,-0.2,0); }
  // the four straps: from each roof hook to the load ring (and the mouth ropes above it)
  const strapM=L(0x4a3c2c); for(const [x,z] of HK){ const a=new THREE.Vector3(x,Y0+2.8,z), b=new THREE.Vector3(Math.sign(x)*0.88,B.position.y+ringY,Math.sign(z)*0.88), len=a.distanceTo(b), s=new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.045,len,6),strapM);
    s.position.copy(a).add(b).multiplyScalar(0.5); s.lookAt(b); s.rotateX(Math.PI/2); s.castShadow=true; g.add(s); }
  g.visible=false; scene.add(g); return BRBUS.g=g; }

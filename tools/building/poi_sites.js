/* ---- the sites ---- each returns its buildings (pieces with their loot spots) and draws its decoration. Layouts are
   in world cells counted from the site's middle (c(i)), decoration in metres from it (X(x), Z(z)). No streets run
   through a site: the roads stop at its edge and the ground takes over. */
const POI_BUILD={};
function poiSkin(style,paint,mat,extra){ return {mat,roof:extra&&extra.roof,s:Object.assign({style,paint,roof:extra&&extra.roofCol||0},extra&&extra.s||{})}; }
const poiSpot=(i,j,l,dx,dz,yaw)=>({x:(i+.5)*CELL+(dx||0),y:l*LVL,z:(j+.5)*CELL+(dz||0),yaw:yaw||0});
function poiCtx(t){ const ci=Math.round(t.x/CELL), cj=Math.round(t.z/CELL), r=seeded(t.seed+31);
  return {ci,cj,C:CELL,y0:t.h,r,i:a=>ci+a,j:b=>cj+b,X:x=>ci*CELL+x,Z:z=>cj*CELL+z,
    jit:(a)=>(r()*2-1)*a,                                                  // a little randomness for decoration
    inR:(x,z,pad)=>Math.hypot(ci*CELL+x-t.x,cj*CELL+z-t.z)<t.R-1-(pad||0),
    // which of the four road ends (west, east, north, south) a road actually comes in at
    roads:()=>{ townBulbs(t); return t.dead.map(d=>!d); } }; }
const rectIn=(x0,z0,x1,z1,pad)=>(x,z)=>x>x0-pad&&x<x1+pad&&z>z0-pad&&z<z1+pad;
const discIn=(cx,cz,r)=>(x,z)=>Math.hypot(x-cx,z-cz)<r;
const anyIn=list=>(x,z)=>list.some(f=>f(x,z));
function poiFind(K,i,j,l){ return K.P.find(q=>q.type==='floor'&&q.i===i&&q.j===j&&q.l===l); }
/* a lorry, in its own frame (x across, z forward, y up) turned by yaw and set down at x,y,z: a conventional tractor
   (hood, grille, lights, a cab with glass and a sleeper, steps, tanks, stacks, mirrors) and/or a trailer (a ribbed
   box with doors and lights, or a flatbed with stakes and a load of logs), on proper wheels. o.cab: the paint, or
   null for a trailer left on its landing legs; o.trailer: 'box', 'logs' or null; o.tcol: the trailer's colour. Solid
   in pieces along its length, so it can be climbed and stood on. Returns the far ends (for keeping clutter off it). */
function poiRig(D,x,y,z,yaw,o){ o=o||{}; const PI=Math.PI, cy=Math.cos(yaw), sy=Math.sin(yaw);
  const put=(g,c,lx,ly,lz,glow)=>{ g.translate(lx,ly,lz); D.geo(g,c,x,y,z,[0,yaw,0],glow); };
  const B=(w,h,d,lx,ly,lz,c,glow)=>put(new THREE.BoxGeometry(w,h,d),c,lx,ly+h/2,lz,glow);
  const Cx=(r,len,lx,ly,lz,c,seg)=>{ const g=new THREE.CylinderGeometry(r,r,len,seg||14); g.rotateZ(PI/2); put(g,c,lx,ly,lz); };
  const Cz=(r,len,lx,ly,lz,c,seg)=>{ const g=new THREE.CylinderGeometry(r,r*1.04,len,seg||12); g.rotateX(PI/2); put(g,c,lx,ly,lz); };
  const Cy=(r,h,lx,ly,lz,c,seg)=>put(new THREE.CylinderGeometry(r,r,h,seg||10),c,lx,ly+h/2,lz);
  const W2=(lx,lz)=>[x+lx*cy+lz*sy,z-lx*sy+lz*cy];
  const solid=(x0,x1,y0_,y1,z0,z1)=>{ const n=Math.max(1,Math.ceil((z1-z0)/2)); for(let k=0;k<n;k++){ const za=z0+(z1-z0)*k/n, zb=z0+(z1-z0)*(k+1)/n; let a=1e9,b=1e9,c=-1e9,d=-1e9;
      for(const [lx,lz] of [[x0,za],[x1,za],[x0,zb],[x1,zb]]){ const [wx,wz]=W2(lx,lz); a=Math.min(a,wx); b=Math.min(b,wz); c=Math.max(c,wx); d=Math.max(d,wz); }
      const sh=Math.abs(sy*cy)>0.2?0.35:0; D.solid(a+sh,y+y0_,b+sh,c-sh,y+y1,d-sh); } }; // (a diagonal one is trimmed a little so its boxes don't reach far past the body)
  const DK=0x1d1f22, CHROME=0xc4cad1, GLASS=0x2c3e50, FRAME=0x2a2d31;
  const wheel=(lz,dual)=>{ for(const s of [-1,1]) for(const xw of dual?[1.06,0.74]:[1.06]){ Cx(0.52,0.3,s*xw,0.52,lz,DK,16); Cx(0.3,0.32,s*xw,0.52,lz,0xb5bcc2,12); Cx(0.1,0.34,s*xw,0.52,lz,0x55585c,8); } Cx(0.09,1.9,0,0.52,lz,FRAME,6); };
  let front=-1.4, back=-1.4;
  if(o.cab!=null){ const c=o.cab, dk=new THREE.Color(c).multiplyScalar(0.6).getHex(); front=4.6; back=-3.6; D.obj('metal',o.trailer?1500:700); // (a lorry and its trailer are one thing to break)
    B(0.14,0.28,7.6,-0.48,0.72,0.4,FRAME); B(0.14,0.28,7.6,0.48,0.72,0.4,FRAME);                             // frame rails
    B(2.5,0.38,0.26,0,0.42,4.47,CHROME); B(0.5,0.12,0.3,0,0.3,4.5,DK);                                        // bumper
    B(2.2,1.0,1.75,0,1.0,3.47,c); B(2.0,0.16,1.6,0,2.0,3.42,c); B(2.24,0.08,1.78,0,1.95,3.47,dk);              // the hood, with a crease
    B(1.3,0.92,0.06,0,1.05,4.36,CHROME); for(let k=0;k<6;k++) B(1.18,0.05,0.08,0,1.12+k*0.14,4.38,0x2a2d33);    // the grille
    for(const s of [-1,1]){ B(0.34,0.2,0.06,s*0.9,1.4,4.36,0xfff3cf,true); B(0.12,0.08,0.06,s*1.0,1.2,4.36,0xffa53a,true);
      B(0.42,0.1,1.5,s*1.08,1.36,3.45,dk); B(0.36,0.42,0.1,s*1.08,0.95,2.72,DK); }                              // lights, front fenders and splash guards
    B(2.4,2.15,2.0,0,1.05,1.6,c);                                                                          // the cab
    B(2.1,0.82,0.06,0,2.2,2.62,GLASS); B(0.06,0.82,0.08,0,2.2,2.63,c); B(2.3,0.08,0.34,0,3.06,2.72,DK);        // windscreen, centre post, sun visor
    for(let k=0;k<5;k++) B(0.1,0.06,0.06,-0.6+k*0.3,3.22,2.56,0xffa53a,true);                                 // roof marker lights
    for(const s of [-1,1]){ B(0.06,0.72,0.95,s*1.21,2.24,1.95,GLASS); B(0.05,1.5,0.05,s*1.215,1.2,1.42,DK); B(0.04,0.06,0.22,s*1.23,1.95,1.62,CHROME);
      B(0.36,0.07,0.7,s*1.2,0.72,2.05,CHROME); B(0.36,0.07,0.7,s*1.2,1.08,2.05,CHROME);                     // door window, seam, handle, steps
      B(0.4,0.04,0.04,s*1.4,2.45,2.45,DK); B(0.06,0.5,0.24,s*1.6,2.15,2.45,DK); B(0.04,0.42,0.18,s*1.63,2.19,2.45,0x8fb6d0); // mirror
      Cz(0.32,1.4,s*1.0,0.98,0.6,CHROME,14); Cz(0.33,0.05,s*1.0,0.98,0.2,0x8a8f96,14); Cz(0.33,0.05,s*1.0,0.98,1.0,0x8a8f96,14); // fuel tanks with straps
      Cy(0.09,3.2,s*1.12,1.0,-1.02,CHROME,8); Cy(0.11,0.3,s*1.12,3.9,-1.02,DK,8);                          // exhaust stacks
      B(0.5,0.42,0.6,s*0.95,0.62,-1.55,DK); B(0.5,0.62,0.05,s*1.0,0.22,-3.55,DK); }                        // battery box, mud flaps
    B(2.4,2.4,1.5,0,1.05,-0.15,c); B(2.42,0.1,1.52,0,1.6,-0.15,dk); B(2.3,0.45,1.9,0,3.2,0.75,dk);            // the sleeper, a stripe, the roof fairing
    B(1.6,0.12,1.2,0,1.12,-2.45,FRAME); B(0.5,0.06,0.5,0,1.24,-2.45,0x55585c);                                // fifth wheel
    wheel(3.47,false); wheel(-2.0,true); wheel(-3.1,true);
    solid(-1.25,1.25,0,3.45,-0.9,4.6); solid(-1.25,1.25,0,1.25,-3.6,-1.4); if(!o.trailer) D.end(); }
  if(o.trailer){ const TL=o.len||10.4, tz=o.cab!=null?-1.4-TL/2:0, tc=o.tcol||0xe9e7df, bk=tz-TL/2, fr=tz+TL/2; back=bk; if(o.cab==null){ front=fr; D.obj('metal',900); }
    B(1.0,0.26,TL-0.6,0,0.92,tz,FRAME); wheel(bk+1.6,true); wheel(bk+2.85,true);
    for(const s of [-1,1]){ B(0.5,0.6,0.05,s*1.0,0.2,bk+0.9,DK); }
    if(o.cab==null||o.legs){ const lg=fr-2.2; for(const s of [-1,1]){ B(0.13,1.1,0.13,s*0.8,0.12,lg,FRAME); B(0.32,0.06,0.32,s*0.8,0,lg,FRAME); } B(1.6,0.08,0.08,0,0.6,lg,FRAME); B(0.08,0.08,0.3,0.9,0.75,lg+0.15,CHROME); }
    if(o.trailer==='box'){ const rib=new THREE.Color(tc).multiplyScalar(0.86).getHex();
      B(2.5,2.85,TL,0,1.18,tz,tc); B(2.56,0.12,TL+0.04,0,4.0,tz,0x8e9aa3); B(2.56,0.2,TL+0.04,0,1.08,tz,FRAME);
      for(let zz=bk+0.6;zz<fr-0.3;zz+=1.15) for(const s of [-1,1]) B(0.04,2.7,0.07,s*1.27,1.25,zz,rib);
      for(const s of [-1,1]){ B(0.03,0.38,TL*0.72,s*1.27,2.6,tz+0.3,o.stripe||0xc0392b); B(0.04,0.5,TL*0.5,s*1.25,0.48,tz+0.6,0x8e9aa3);   // a stripe, the side skirts
        B(0.26,0.13,0.05,s*1.0,1.0,bk-0.03,0xd21f1f,true); B(0.08,0.08,0.05,s*1.2,3.85,bk-0.03,0xd21f1f,true); B(0.08,0.08,0.05,s*1.2,3.85,fr+0.03,0xffa53a,true);
        for(const xx of [0.35,0.85]) B(0.05,2.55,0.05,s*xx,1.3,bk-0.06,CHROME); for(const yy of [1.6,3.4]) B(0.14,0.18,0.06,s*1.2,yy,bk-0.04,DK); } // lock bars, hinges
      B(0.06,2.7,0.08,0,1.25,bk-0.05,rib); B(2.3,0.14,0.14,0,0.55,bk+0.25,DK); for(const s of [-1,1]) B(0.12,0.5,0.12,s*0.9,0.6,bk+0.3,DK);    // door seam, under-run bar
      solid(-1.25,1.25,0.6,4.05,bk,fr); }
    else { const deck=0x3a3d42; B(2.5,0.22,TL,0,1.18,tz,deck); B(2.4,0.04,TL-0.1,0,1.4,tz,0x6b4a2e); for(const s of [-1,1]) B(0.26,0.13,0.05,s*1.0,1.0,bk-0.03,0xd21f1f,true);
      for(let zz=bk+0.7;zz<fr;zz+=2.3){ B(2.5,0.16,0.22,0,1.42,zz,DK); for(const s of [-1,1]) B(0.12,1.5,0.12,s*1.22,1.42,zz,DK); }
      const LG=[[-0.8,0],[0,0],[0.8,0],[-0.4,0.68],[0.4,0.68],[0,1.36]], LC=[0x8a5a32,0x7a4e2c,0x94643a];
      LG.forEach(([lx,ly],k)=>{ const r=0.38+((k*37)%5)*0.012, len=TL-0.4-(k%3)*0.25; Cz(r,len,lx,1.58+0.38+ly,tz,LC[k%3],12); for(const e of [-1,1]) Cz(r*0.9,0.03,lx,1.96+ly,tz+e*(len/2+0.01),0xd9b077,12); });
      solid(-1.25,1.25,0.6,1.58+2.1,bk,fr); }
    D.end(); }
  return [W2(0,front),W2(0,back)]; }
// a solid for a box turned by yaw (half sizes hw across, hl along, from y0 to y1): short pieces along its length, each
// only as big as its own corner-to-corner span, so a turned thing has no invisible corners standing off it
function solidTurned(D,x,z,yaw,hw,hl,y0,y1){ const s=Math.sin(yaw), c=Math.cos(yaw), n=Math.max(1,Math.ceil(hl*2/(Math.abs(s*c)>0.05?0.9:2.4)));
  for(let k=0;k<n;k++){ const f=-hl+hl*2*(k+0.5)/n, cx=x+s*f, cz=z+c*f, h=hl/n, ex=Math.abs(c)*hw+Math.abs(s)*h, ez=Math.abs(s)*hw+Math.abs(c)*h; D.solid(cx-ex,y0,cz-ez,cx+ex,y1,cz+ez); } }
// is a point within m metres of the line between two ends (a lorry's footprint, for keeping clutter off it)
const nearSeg=(px,pz,[[ax,az],[bx,bz]],m)=>{ const dx=bx-ax, dz=bz-az, t=Math.max(0,Math.min(1,((px-ax)*dx+(pz-az)*dz)/(dx*dx+dz*dz||1))); return Math.hypot(px-ax-dx*t,pz-az-dz*t)<m; };

/* Gearworks: a long factory hall with a mezzanine and stairs to the roof, a high-bay warehouse with a loading dock,
   an office block, a boiler house and smokestack, storage tanks, a container yard under a gantry crane, trailers and
   pallets parked about. Asphalt. */
POI_BUILD.factory=(t,D)=>{ const K=poiKit(t), L=K.L, X_=poiCtx(t), {i,j,X,Z,y0,jit,r}=X_, blds=[];
  const metal=poiSkin('corr',0,'metal',{s:{floor:'concrete',tread:'plate',beam:0x2c3036}}), metal2=poiSkin('corr',1,'metal',{s:{floor:'concrete',tread:'plate',beam:0x2c3036}}), metal3=poiSkin('corr',2,'metal',{s:{floor:'concrete',tread:'plate',beam:0x2c3036}});
  const office=poiSkin('lab',1,'brick',{s:{floor:'tile',tread:'plate',beam:0x3e454c}}), plate=poiSkin('corr',0,'metal',{s:{floor:'plate',tread:'plate',beam:0x2c3036}}), roofS=poiSkin('corr',0,'metal',{s:{floor:'tar',beam:0x2c3036}});
  const pad=[];
  // --- the main hall: cells -5..0 by -6..-3 (30 x 20 m), two storeys tall; a mezzanine along the north side
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-5), j0=j(-6);
    K.slab(i0,j0,6,4,L,metal); K.slab(i0,j0,6,2,L+1,plate); K.slab(i0,j0,6,4,L+2,roofS,(a,b)=>a===i0+4&&b===j0);
    K.shell(i0,j0,6,4,L,2,metal,(f,k,s)=>{ if(s===0){ if(f==='s') return k===1||k===2?POI_OPEN:k===4?POI_DOOR:k===5?POI_WIN:511; if(f==='n') return k===5?POI_OPEN:511; if(f==='e') return k===3?POI_DOOR:511; return k===2?POI_WIN:511; } return (k+(f==='n'?1:0))%2?POI_WIN:511; });
    K.shell(i0,j0,6,4,L+2,1,roofS,()=>POI_LOW);
    K.ramp(i0,j0+2,L,3,plate); K.ramp(i0+4,j0,L+1,0,plate);                          // up the west end to the mezzanine; along it to the roof
    for(let a=1;a<6;a++) K.wallZ(i0+a,j0+2,L+1,POI_LOW,plate);                        // the mezzanine rail
    const dk=poiFind(K,i0+2,j0,L+1); if(dk) poiFix(dk,[[2.2,0.9,0.8,2.6,0,1.1,0x3a4048],[2.0,0.5,0.08,2.6,0.9,0.8,0x1d2329,false],[1.8,0.4,0.05,2.6,0.95,0.77,0x3aa7d8,false,true],[0.55,0.9,0.55,2.4,0,2.3,0x2c3036]]);
    const ac=poiFind(K,i0+2,j0+2,L+2); if(ac) poiFix(ac,[[1.6,1.2,1.6,2.5,0,2.5,0x9aa2a8],[1.2,0.15,1.2,2.5,1.2,2.5,0x6b737a]]);
    const ac2=poiFind(K,i0+4,j0+3,L+2); if(ac2) poiFix(ac2,[[1.2,0.9,2.2,1.8,0,2.4,0x9aa2a8],[0.9,0.12,1.9,1.8,0.9,2.4,0x6b737a]]);
    sp.chest.push(poiSpot(i0+1,j0,L+1,0,1.2),poiSpot(i0+5,j0+3,L),poiSpot(i0+1,j0+3,L+2)); sp.floor.push(poiSpot(i0+4,j0+1,L+1),poiSpot(i0+2,j0+3,L),poiSpot(i0+5,j0+2,L+2));
    blds.push({pieces:K.P.slice(n0),spots:sp,kind:'hall'}); pad.push(rectIn(-25,-30,5,-10,4));
    // inside: a conveyor line, stamping presses under the mezzanine, a lathe, crates
    const zc=-14.6; D.box(17,0.7,1.4,X(-6),y0,Z(zc),0x3b4046); D.box(17.2,0.12,1.2,X(-6),y0+0.7,Z(zc),0x23262a); for(let x=-14.2;x<2.4;x+=0.9) D.tube(0.09,1.3,X(x),y0+0.84,Z(zc),0x9aa3ab,[Math.PI/2,0,0]); D.solid(X(-14.5),y0,Z(zc)-0.7,X(2.5),y0+0.84,Z(zc)+0.7);
    for(const x of [-12,-3]){ const zz=-24.5; D.sbox(2.6,1.1,2.6,X(x),y0,Z(zz),0x55606a); for(const [dx,dz] of [[-1,-1],[1,-1],[-1,1],[1,1]]) D.box(0.4,2.3,0.4,X(x+dx),y0+1.1,Z(zz+dz),0x2d3238);
      D.sbox(2.8,0.6,2.8,X(x),y0+2.4,Z(zz),0xe0a326); D.box(1.6,0.9,1.6,X(x),y0+1.3,Z(zz),0x9aa3ab); D.solid(X(x)-1.2,y0+1.1,Z(zz)-1.2,X(x)+1.2,y0+2.4,Z(zz)+1.2); }
    D.sbox(3.2,1.1,1,X(-7.5),y0,Z(-19.5),0x4f6d6a); D.box(0.9,0.5,0.8,X(-8.6),y0+1.1,Z(-19.5),0x2c3036); D.tube(0.12,2.2,X(-7.3),y0+1.35,Z(-19.5),0xb5bcc2,[0,0,Math.PI/2]);
    for(const [x,z,h,c] of [[-22.5,-12.4,0,0xa9814e],[-22.5,-12.4,1.2,0x9b7a4d],[-21.2,-11.6,0,0xa9814e],[-17,-27.5,0,0x6f8a9b],[-15.7,-26.4,0,0xa9814e],[-16.4,-27,1.2,0x9b7a4d]]) D.sbox(1.2,1.2,1.2,X(x),y0+h,Z(z),c); }
  // --- the warehouse: cells 3..5 by -4..0 (15 x 25 m), one tall bay with racking, a loading dock on the west side
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(3), j0=j(-4);
    K.slab(i0,j0,3,5,L,metal2); K.slab(i0,j0,3,5,L+2,roofS);
    K.shell(i0,j0,3,5,L,2,metal2,(f,k,s)=>{ if(s===0){ if(f==='w') return k===1||k===3?POI_OPEN:511; if(f==='n') return k===1?POI_DOOR:511; return 511; } return f==='e'||f==='w'?(k%2?POI_WIN:511):511; });
    K.shell(i0,j0,3,5,L+2,1,roofS,()=>POI_LOW);
    for(const x of [19.6,23.6]){ for(const z of [-17,-11,-5,1]) for(const dx of [-0.55,0.55]) D.box(0.12,5.4,0.12,X(x+dx),y0,Z(z),0x2f5f9a);
      for(const h of [0.15,1.9,3.65,5.3]){ D.box(1.2,0.1,18.2,X(x),y0+h,Z(-8),0xd48a1c); D.solid(X(x)-0.6,y0+h,Z(-17.1),X(x)+0.6,y0+h+0.1,Z(1.1)); }
      for(let z=-16.2;z<0.5;z+=1.6) for(const h of [0.25,2.0,3.75]) if(r()<0.72) D.box(1.0,1.1,1.2,X(x),y0+h,Z(z),[0xa9814e,0x9b7a4d,0x6f8a9b,0x8a9a6a][Math.floor(r()*4)]); }
    { const fx=X(16.5), fz=Z(-12); D.sbox(1.4,1.2,2.4,fx,y0,fz,0xe8b420); D.box(1.2,1.0,1.0,fx,y0+1.2,fz+0.5,0x3a3d42); D.box(0.1,2.6,0.1,fx-0.5,y0,fz-1.3,0x2a2d31); D.box(0.1,2.6,0.1,fx+0.5,y0,fz-1.3,0x2a2d31); D.box(1.1,0.08,0.9,fx,y0+0.2,fz-1.75,0x55585c); }
    D.sbox(3.4,1.25,7,X(13.3),y0,Z(-12.5),0x8f8c86); D.box(3.5,0.1,7.1,X(13.3),y0+1.25,Z(-12.5),0xe0a326); for(const z of [-15.2,-9.8]) D.box(0.4,1.1,1.2,X(11.4),y0,Z(z),0x1d1f22); // the dock, with bumpers
    sp.chest.push(poiSpot(i0+2,j0+4,L,0,0),poiSpot(i0,j0,L,0,0)); sp.floor.push(poiSpot(i0+1,j0+2,L),poiSpot(i0+1,j0+4,L)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'warehouse'}); pad.push(rectIn(10,-20,30,5,5)); }
  // --- the office block: cells -7..-6 by 1..3, two floors, flat roof
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-7), j0=j(1);
    K.slab(i0,j0,2,3,L,office); K.slab(i0,j0,2,3,L+1,office,(a,b)=>a===i0+1&&b===j0+1); K.slab(i0,j0,2,3,L+2,roofS);
    K.shell(i0,j0,2,3,L,2,office,(f,k,s)=>s===0&&f==='e'&&k===0?POI_DOOR:s===0&&f==='n'&&k===1?POI_DOOR:POI_WIN); K.shell(i0,j0,2,3,L+2,1,office,()=>POI_LOW); K.ramp(i0+1,j0+1,L,1,office);
    for(const [a,b,l] of [[0,0,L],[0,2,L+1],[1,0,L+1],[0,1,L]]){ const fl=poiFind(K,i0+a,j0+b,l); if(fl) poiFix(fl,[[1.6,0.75,0.8,2.5,0,1.6,0xc9cdd2],[1.6,0.06,0.8,2.5,0.75,1.6,0x8a6a48],[0.6,0.4,0.05,2.5,0.81,1.4,0x1d2329,false],[0.5,0.32,0.04,2.5,0.85,1.375,0x5ec8ff,false,true],[0.55,0.9,0.55,2.6,0,2.6,0x2c3036]]); }
    sp.chest.push(poiSpot(i0,j0+2,L+1,0,1.3),poiSpot(i0,j0+2,L)); sp.floor.push(poiSpot(i0,j0+1,L+1)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'office'}); pad.push(rectIn(-35,5,-25,20,4));
    for(let k=0;k<5;k++){ const x=-22+k*2.7+jit(0.2); D.box(2.3,0.12,4.6,X(x),y0+0.01,Z(10),0xe9e7df); } } // parking bays by the office
  // --- the boiler house and smokestack, and two storage tanks
  { D.sbox(8,5,6,X(2),y0,Z(14),0x7a4a3a); D.sbox(8.4,0.35,6.4,X(2),y0+5,Z(14),0x35302e); D.box(1.6,2.4,0.15,X(2),y0,Z(10.93),0x2e2a28); D.box(2.0,0.2,0.2,X(2),y0+2.4,Z(10.92),0x5a3428); for(const dx of [-0.9,0.9]) D.box(0.2,2.6,0.2,X(2+dx),y0,Z(10.92),0x5a3428);
    D.box(8.1,0.28,6.1,X(2),y0+3.3,Z(14),0x5a3428); D.box(8.1,0.4,6.1,X(2),y0,Z(14),0x4a4440); for(const [dx,dz] of [[-4,-3],[4,-3],[-4,3],[4,3]]) D.box(0.5,5,0.5,X(2+dx),y0,Z(14+dz),0x6a3e30);
    for(const dz of [-1.2,1.2]){ D.box(0.12,1.0,1.6,X(-2.04),y0+2.0,Z(14+dz),0x3a3d42); for(let k=0;k<5;k++) D.box(0.16,0.05,1.5,X(-2.06),y0+2.1+k*0.18,Z(14+dz),0x55585c); }
    for(const dx of [-2,1.5]){ D.box(1.2,0.8,1.2,X(2+dx),y0+5.35,Z(14.5),0x6b737a); D.box(1.5,0.1,1.5,X(2+dx),y0+6.15,Z(14.5),0x4a4f55); D.box(0.2,0.35,0.2,X(2+dx),y0+6.25,Z(14.5),0x4a4f55); } D.box(0.6,0.3,0.4,X(-0.5),y0+2.2,Z(10.88),0xd23a2a); D.box(0.5,0.5,0.3,X(5),y0+1.0,Z(10.9),0x2e86c1); for(const x of [-0.5,4.5]) D.box(1.2,1.1,0.15,X(x),y0+2.6,Z(10.93),0xffd98a,null,true);
    const sx=X(8.5), sz=Z(19); D.scyl(2.1,26,sx,y0,sz,0x8a4a3a,16); D.cyl(1.4,2.1,0.1,sx,y0+26,sz,0x2e2a28,16); for(const h of [8,15,22]) D.cyl(2.18,2.18,0.7,sx,y0+h,sz,0xe9e4d8,16);
    for(let h=0.5;h<25;h+=0.6) D.box(0.6,0.06,0.06,sx,y0+h,sz-2.15,0x2b2f35); for(const dx of [-0.28,0.28]) D.box(0.06,25,0.06,sx+dx,y0,sz-2.15,0x2b2f35);
    D.tube(0.45,3.4,X(7.3),y0+3.2,Z(16.4),0x55585c,[0,0.9,Math.PI/2]);
    for(const [x,z] of [[-15,22],[-8.6,26]]){ D.scyl(2.6,7,X(x),y0,Z(z),0xd7dadc,18); D.cyl(0.4,2.6,0.8,X(x),y0+7,Z(z),0xbcc1c5,18); for(const h of [2.3,4.6]) D.cyl(2.65,2.65,0.12,X(x),y0+h,Z(z),0x9aa1a8,18); }
    D.sbox(4.1,0.12,1.1,X(-11.8),y0+7,Z(24),0x6b737a); for(const dz of [-0.55,0.55]) D.box(4.1,1,0.06,X(-11.8),y0+7.1,Z(24+dz),0xe0a326);
    pad.push(discIn(2,14,7),discIn(8.5,19,4),discIn(-12,24,7)); }
  // --- the container yard (south-east) under a gantry crane, stacks of odd heights, a few left at an angle
  { const cols=[0xc0392b,0x2e86c1,0x27ae60,0xd68910,0x7d3c98,0x17a589,0xa04000,0x5d6d7e];
    const cont=(x,z,lv,yaw)=>{ const c=cols[Math.floor(r()*cols.length)], xx=X(x), zz=Z(z), y=y0+lv*2.6, s=Math.sin(yaw), co=Math.cos(yaw);
      const g=new THREE.BoxGeometry(6.1,2.6,2.44); D.geo(g,c,xx,y+1.3,zz,[0,yaw,0]);
      for(let q=-2.7;q<=2.71;q+=0.45){ const gg=new THREE.BoxGeometry(0.12,2.3,2.5); gg.translate(q,0,0); D.geo(gg,c,xx,y+1.3,zz,[0,yaw,0]); }
      for(const dy of [0.06,2.54]){ const gg=new THREE.BoxGeometry(6.14,0.12,2.48); D.geo(gg,0x2a2d31,xx,y+dy,zz,[0,yaw,0]); }
      const dg=new THREE.BoxGeometry(0.08,2.3,2.2); dg.translate(3.06,0,0); D.geo(dg,0x3a3d42,xx,y+1.3,zz,[0,yaw,0]);
      solidTurned(D,xx,zz,yaw+Math.PI/2,1.22,3.05,y,y+2.6); };
    [[17,15,0,0.02],[17,15,1,-0.03],[24.6,15.4,0,0.05],[17.4,18.6,0,0],[24,18.8,0,-0.04],[24,18.8,1,0.03],[24,18.8,2,0],[18.2,24.5,0,0.12],[25.2,24,0,-0.08],[31,13,0,1.57],[30.8,20.6,0,1.62]].forEach(([x,z,lv,yw])=>cont(x,z,lv,yw));
    for(const z of [11,28]) for(const x of [14,29]){ D.sbox(0.6,11,0.6,X(x),y0,Z(z),0xe0a326); } for(const z of [11,28]) D.sbox(15.6,0.9,0.9,X(21.5),y0+11,Z(z),0xe0a326); for(const x of [14,29]) D.box(0.7,0.7,17.6,X(x),y0+11.2,Z(19.5),0xe0a326);
    D.box(15,1.4,2.6,X(21.5),y0+11.9,Z(21),0xd4991c); D.box(2.4,2,2.4,X(22),y0+12.4,Z(21),0x3a3d42); D.tube(0.04,6,X(21.6),y0+9,Z(21),0x222222); D.tube(0.04,6,X(22.4),y0+9,Z(21),0x222222); D.box(1.4,0.5,0.5,X(22),y0+5.8,Z(21),0xe0a326);
    pad.push(rectIn(13,10,33,29,3)); }
  // --- trailers, pallets, barrels and barriers left about the yard; floodlights
  { const rigs=[];
    rigs.push(poiRig(D,X(-14),y0,Z(-3.5),1.42,{trailer:'box',tcol:0xe9e7df,stripe:0x2e86c1,len:9.6}));                   // a trailer left on its legs
    { const yw=1.66, fx=Math.sin(yw), fz=Math.cos(yw); rigs.push(poiRig(D,X(-6+fx*6.2),y0,Z(1.2+fz*6.2),yw,{cab:0xc0392b,trailer:'box',tcol:0x2e86c1,stripe:0xf2c418,len:9.6})); } // backed up, ready to go
    rigs.push(poiRig(D,X(-1),y0,Z(26),0.35,{trailer:'box',tcol:0xc0392b,stripe:0xe9e7df,len:9.6}));
    rigs.push(poiRig(D,X(-33),y0,Z(-17),Math.PI,{cab:0x2f6fb0,trailer:'box',tcol:0xd7dadc,stripe:0xc0392b,len:9.6}));      // another along the west side
    const onRig=(x,z,m)=>rigs.some(e=>nearSeg(X(x),Z(z),e,m));
    for(let k=0;k<9;k++){ const x=-20+r()*36, z=-6+r()*12; if(onRig(x,z,2.4)||Math.hypot(x+3,z-4)<1.8||Math.hypot(x+3,z+5)<1.8) continue; const h=r()<0.4?2:1;
      for(let q=0;q<h;q++) D.sbox(1.2,0.15,1.2,X(x),y0+q*0.9,Z(z),0x8c6a3f), D.sbox(1.1,0.75,1.1,X(x),y0+0.15+q*0.9,Z(z),[0xa9814e,0x6f8a9b,0xd7dadc][Math.floor(r()*3)]); }
    for(let k=0;k<7;k++){ const x=6+r()*5, z=-26+r()*6; D.scyl(0.32,0.9,X(x),y0,Z(z),[0x2e86c1,0xc0392b,0x3c8d3c][k%3],10); }
    for(const [x,z,yw] of [[-30,-4,0.1],[-30,2.4,-0.15],[36,-6,1.5],[-3,33,0.2]]){ const g=new THREE.BoxGeometry(3,0.9,0.6); D.geo(g,0xd8d4cc,X(x),y0+0.45,Z(z),[0,yw,0]); solidTurned(D,X(x),Z(z),yw+Math.PI/2,0.3,1.5,y0,y0+0.9); }
    for(const [x,z] of [[-8,-6],[8,-30],[10,6],[-27,-6],[-20,15],[32,8]]){ D.box(0.25,9,0.25,X(x),y0,Z(z),0x55606a); D.box(1.6,0.6,0.5,X(x),y0+9,Z(z),0x2c3036); D.box(1.4,0.08,0.4,X(x),y0+8.95,Z(z),0xfff3cf,null,true); D.solid(X(x)-0.15,y0,Z(z)-0.15,X(x)+0.15,y0+9,Z(z)+0.15); }
    // a pipe run on stands from the boiler house to the hall
    const run=[[1,11],[-3,4],[-3,-5],[-3,-9.7]]; for(let k=0;k<run.length-1;k++){ const [xa,za]=run[k], [xb,zb]=run[k+1], len=Math.hypot(xb-xa,zb-za), yaw=Math.atan2(xb-xa,zb-za); D.tube(0.3,len,X((xa+xb)/2),y0+6.4,Z((za+zb)/2),0x2f7f6b,[Math.PI/2,yaw,0]); }
    for(const [x,z] of run.slice(1,3)){ D.sbox(0.4,6.2,0.4,X(x),y0,Z(z),0x6b737a); D.box(1.2,0.2,1.2,X(x),y0+6.1,Z(z),0x55606a); }
    // a gatehouse where the north road comes in: a booth with windows all round and a striped barrier arm, raised
    { const bx=X(8), bz=Z(-34); D.obj('metal',420); D.box(2.4,0.2,2.4,bx,y0,bz,0x8f8c86); D.box(2.2,1.1,2.2,bx,y0+0.2,bz,0xd7dadc); D.box(2.2,1.0,2.2,bx,y0+1.3,bz,0x2c3e50); for(const [dx,dz] of [[-1.05,-1.05],[1.05,-1.05],[-1.05,1.05],[1.05,1.05]]) D.box(0.12,1.0,0.12,bx+dx,y0+1.3,bz+dz,0xd7dadc);
      D.box(2.8,0.22,2.8,bx,y0+2.3,bz,0x3a3d42); D.box(0.8,0.3,0.06,bx,y0+2.0,bz-1.13,0xf2c418); D.box(0.9,1.9,0.06,bx+0.5,y0+0.2,bz+1.12,0x8e9aa3); D.solid(bx-1.2,y0,bz-1.2,bx+1.2,y0+2.5,bz+1.2); D.end();
      D.obj('metal',150); D.box(0.5,1.1,0.5,bx-1.6,y0,bz-0.6,0x3a3d42); for(let k=0;k<8;k++){ const g=new THREE.BoxGeometry(0.14,0.14,0.75); g.translate(0,0,-0.38-k*0.75); D.geo(g,k%2?0xe9e7df:0xc0392b,bx-1.6,y0+1.0,bz-0.6,[1.05,Math.PI/2,0]); } D.solid(bx-1.85,y0,bz-0.85,bx-1.35,y0+1.1,bz-0.35); D.end(); }
    pad.push(rectIn(-36,-23,-30,-4,2),rectIn(5,-37,11,-31,1),rectIn(-4,30,4,40,2),rectIn(30,-5,40,5,2),rectIn(-4,-40,4,-30,2)); }
  poiGround(t,'asphalt',anyIn(pad),2.5);
  return blds; };

/* Fort Granite: a curtain wall, off-centre on the site, with gates only where roads come in; a wall walk with
   battlements; corner towers (one fallen to a ruin); a tall keep built into the south-east corner; a barracks, a
   smithy, a stable, a well and a training yard laid out unevenly inside. */
POI_BUILD.castle=(t,D)=>{ const K=poiKit(t), L=K.L, X_=poiCtx(t), {i,j,X,Z,y0,C,jit,r}=X_, blds=[], roads=X_.roads();
  const stone=poiSkin('stone',0,'brick',{s:{floor:'stone',tread:'stone',beam:0x8f877a}}), stone2=poiSkin('stone',1,'brick',{s:{floor:'stone',tread:'stone',beam:0x8f877a}}), stone3=poiSkin('stone',2,'brick',{s:{floor:'stone',tread:'stone',beam:0x8f877a}});
  const wood=poiSkin('log',0,'wood',{roof:'brick',roofCol:1,s:{floor:'plank',tread:'plank',beam:0x5a3a1e}}), wood2=poiSkin('log',1,'wood',{roof:'wood',roofCol:1,s:{floor:'plank',tread:'plank',beam:0x5a3a1e}});
  const n0=K.P.length, sp={chest:[],floor:[]};
  const W=i(-6), E=i(5), N=j(-6), S=j(5);                                      // the wall lines: 55 x 55 m, west and north of the site's middle
  const gW=roads[0], gE=roads[1], gN=roads[2], gS=roads[3];
  const keep={i0:i(2),j0:j(2)};                                                 // 3x3 in the south-east corner, its outer walls are the curtain
  const ruin={i0:W,j0:j(3)};                                                    // the south-west tower has fallen
  const towerAt=[{i0:W,j0:N,ns:'n',ew:'w'},{i0:E-2,j0:N,ns:'n',ew:'e'}];
  const inTower=(ii,jj)=>[...towerAt,ruin].some(tw=>ii>=tw.i0&&ii<tw.i0+2&&jj>=tw.j0&&jj<tw.j0+2)||ii>=keep.i0&&jj>=keep.j0&&ii<keep.i0+3&&jj<keep.j0+3;
  const gate=(side,k)=>(side==='w'?gW:side==='e'?gE:side==='n'?gN:gS)&&(k===-1||k===0);
  // the curtain wall, two storeys; every so often a slit window up top
  for(let k=-6;k<=4;k++) for(const l of [L,L+1]){ const m=l===L+1&&(k+6)%4===2?POI_WIN:511;
    if(!(l===L&&gate('w',k))&&!(k>=3&&k<=4)) K.wallX(W,j(k),l,m,stone);
    if(!(l===L&&gate('e',k))&&!(k>=2)) K.wallX(E,j(k),l,m,stone);
    if(!(l===L&&gate('n',k))) K.wallZ(i(k),N,l,m,stone);
    if(!(l===L&&gate('s',k))&&!(k>=2)&&!(k<=-5)) K.wallZ(i(k),S,l,m,stone); }
  // the wall walk with battlements, between the towers and the keep
  const walk=[]; for(let k=-4;k<=4;k++){ if(k<=2) walk.push([W,j(k)]); if(k<=1) walk.push([E-1,j(k)]); if(k<=2) walk.push([i(k),N]); if(k>=-4&&k<=1) walk.push([i(k),S-1]); }
  for(const [a,b] of walk){ if(inTower(a,b)) continue; K.floor(a,b,L+2,stone); if(a===W) K.wallX(W,b,L+2,POI_MERLON,stone); if(a===E-1) K.wallX(E,b,L+2,POI_MERLON,stone); if(b===N) K.wallZ(a,N,L+2,POI_MERLON,stone); if(b===S-1) K.wallZ(a,S,L+2,POI_MERLON,stone); }
  // stairs up to it: one flight along the inside of the east wall from beside its gate, one along the west wall
  K.ramp(E-2,j(-2),L,3,stone); K.ramp(E-2,j(-3),L+1,3,stone); K.floor(E-2,j(-4),L+2,stone);
  K.ramp(W+1,j(1),L,3,stone); K.ramp(W+1,j(0),L+1,3,stone); K.floor(W+1,j(-1),L+2,stone);
  // the standing towers: a tall ground room, a room at wall-walk height with doors to both walks, a lookout above
  for(const tw of towerAt){ const {i0,j0,ns,ew}=tw, sideI=ew==='e'?i0+1:i0, stairCell=[sideI,j0+1], topCell=[sideI,j0];
    K.slab(i0,j0,2,2,L,stone2); K.slab(i0,j0,2,2,L+2,stone2); K.slab(i0,j0,2,2,L+3,stone2,(a,b)=>a===stairCell[0]&&b===stairCell[1]);
    K.shell(i0,j0,2,2,L,3,stone2,(f,k,s)=>{ const innerEW=ew==='e'?f==='w':f==='e', innerNS=f==='s';
      if(s===2){ if(innerNS&&i0+k===sideI) return POI_DOOR; if(innerEW&&k===0) return POI_DOOR; return innerEW||innerNS?511:POI_WIN; }
      if(s===0&&innerEW&&k===1) return POI_DOOR; if(s===1&&!innerEW&&!innerNS&&k===0) return POI_WIN; return 511; });
    K.ramp(stairCell[0],stairCell[1],L+2,3,stone2); K.shell(i0,j0,2,2,L+3,1,stone2,()=>POI_MERLON);
    const top=poiFind(K,ew==='e'?i0:i0+1,j0,L+3); if(top) poiFix(top,[[0.12,4.4,0.12,2.6,0,2.4,0x3a2a1e],[1.7,1.05,0.05,3.45,3.1,2.4,ew==='e'?0xb3262e:0x2a5ea8,false],[1.2,0.6,0.7,2.2,0,1.0,0x2a2a2e],[0.3,0.3,1.5,2.2,0.45,0.2,0x1f1f22]]);
    sp.chest.push(poiSpot(ew==='e'?i0:i0+1,j0+1,L+2)); sp.floor.push(poiSpot(ew==='e'?i0:i0+1,j0,L)); }
  // the fallen tower: the ground storey and broken stumps of the next, rubble in and around it
  { const {i0,j0}=ruin; K.slab(i0,j0,2,2,L,stone3); const JAG=[511&~(64|128),511&~(256),511&~(128|256),511&~64];
    K.shell(i0,j0,2,2,L,2,stone3,(f,k,s)=>s===0?(f==='e'&&k===0?POI_DOOR:511):JAG[(k+(f==='n'?1:f==='e'?2:0))%4]&~(f==='s'||f==='w'?(k?32|256:8|64):0));
    for(let q=0;q<26;q++){ const x=(i0-X_.ci)*C+r()*14-2, z=(j0-X_.cj)*C+r()*14-2; if(!X_.inR(x,z,1)) continue; const sz=0.25+r()*0.75, x0=(i0-X_.ci)*C, z0=(j0-X_.cj)*C, m=sz+0.2; if(Math.abs(x-x0)<m||Math.abs(z-(z0+2*C))<m||Math.abs(x-x0-2*C)<m&&z>z0-m&&z<z0+2*C+m||Math.abs(z-z0)<m&&x>x0-m&&x<x0+2*C+m) continue; const g=new THREE.DodecahedronGeometry(sz,1); g.scale(1,0.6,1);
      D.geo(g,[0x8f897d,0x7d776c,0x9a9488][q%3],X(x),y0+sz*0.35,Z(z),[r(),r()*6,r()]); if(sz>0.8) D.solid(X(x)-sz*0.6,y0,Z(z)-sz*0.6,X(x)+sz*0.6,y0+sz*0.6,Z(z)+sz*0.6); } }
  // portcullises raised in the gateways
  for(const [side,on] of [['w',gW],['e',gE],['n',gN],['s',gS]]){ if(!on) continue; const X0=side==='w'?W*C:side==='e'?E*C:null, Z0=side==='n'?N*C:side==='s'?S*C:null;
    for(let s=-4.6;s<=4.61;s+=0.66){ const x=X0!=null?X0:X_.ci*C+s, z=Z0!=null?Z0:X_.cj*C+s; D.box(0.1,1.3,0.1,x,y0+LVL-0.15,z,0x2a2a2e); }
    D.box(X0!=null?0.16:9.6,0.14,X0!=null?9.6:0.16,X0!=null?X0:X_.ci*C,y0+LVL-0.15,Z0!=null?Z0:X_.cj*C,0x2a2a2e);
    for(const s of [-5.6,5.6]){ const x=X0!=null?X0+(side==='w'?0.45:-0.45):X_.ci*C+s, z=Z0!=null?Z0+(side==='n'?0.45:-0.45):X_.cj*C+s; D.box(0.12,0.6,0.12,x,y0+2.2,z,0x3a2a1e); D.cyl(0.13,0.09,0.25,x,y0+2.8,z,0x2a2a2e,8); D.sph(0.14,x,y0+3.15,z,0xffa53a,[1,1.5,1],true); } }
  blds.push({pieces:K.P.slice(n0),spots:sp,kind:'walls'});
  // --- the keep: four storeys in the south-east corner, a great hall below, battlements and a flag on top
  { const n1=K.P.length, s2={chest:[],floor:[]}, {i0,j0}=keep;
    K.slab(i0,j0,3,3,L,stone2); K.slab(i0,j0,3,3,L+2,stone2,(a,b)=>a===i0+1&&b===j0+2); K.slab(i0,j0,3,3,L+3,stone2,(a,b)=>a===i0+2&&b===j0+1); K.slab(i0,j0,3,3,L+4,stone2,(a,b)=>a===i0+1&&b===j0);
    K.shell(i0,j0,3,3,L,4,stone2,(f,k,s)=>{ if(s===0){ if(f==='w'&&k===2) return POI_DOOR; if(f==='n'&&k===1) return POI_DOOR; return 511; }
      if(s===2){ if(f==='n'&&k===2) return POI_DOOR; if(f==='w'&&k===2) return POI_DOOR; } return k===1?POI_WIN:511; });
    K.shell(i0,j0,3,3,L+4,1,stone2,()=>POI_MERLON);
    K.ramp(i0,j0+2,L,0,stone2); K.ramp(i0+1,j0+2,L+1,0,stone2); K.ramp(i0+2,j0+1,L+2,3,stone2); K.ramp(i0+1,j0,L+3,2,stone2);
    const hx=(i0-X_.ci)*C, hz=(j0-X_.cj)*C;
    D.sbox(1.1,0.8,7.6,X(hx+9.5),y0,Z(hz+7.8),0x6b4a2e); for(const dx of [-1.2,1.2]) D.sbox(0.4,0.45,7.2,X(hx+9.5+dx),y0,Z(hz+7.8),0x5a3d26);
    D.sbox(1.6,0.6,1.6,X(hx+12.6),y0,Z(hz+12.4),0x7a6a58); D.box(1.2,1.6,0.25,X(hx+12.6),y0+0.6,Z(hz+13),0x8a2a2e); D.box(1.2,0.5,1.2,X(hx+12.6),y0+0.6,Z(hz+12.4),0x8a2a2e);
    for(const [dx,dz] of [[13.8,3.2],[13.8,8]]){ D.box(0.05,3.4,1.5,X(hx+dx+1.15),y0+3,Z(hz+dz),[0xb3262e,0x2a5ea8][dz>5?1:0]); } // banners on the hall wall
    const up=poiFind(K,i0+1,j0+1,L+2); if(up) poiFix(up,[[2,0.5,1.2,2.5,0,3.5,0x6b4a2e],[2,0.15,1.2,2.5,0.5,3.5,0xd9ccb4,false],[0.6,0.9,0.6,0.9,0,1,0x5a3d26]]);
    const up2=poiFind(K,i0+2,j0+2,L+3); if(up2) poiFix(up2,[[1.6,1.1,0.9,2.5,0,4.2,0x5a3d26],[0.8,0.8,0.8,1,0,1,0x7a5a36]]);
    const rf=poiFind(K,i0+1,j0+1,L+4); if(rf) poiFix(rf,[[0.16,6,0.16,2.5,0,2.5,0x3a2a1e],[2.2,1.3,0.06,3.62,4.5,2.5,0xb3262e,false]]);
    s2.chest.push(poiSpot(i0+1,j0,L),poiSpot(i0,j0+1,L+2),poiSpot(i0,j0+2,L+3)); s2.floor.push(poiSpot(i0+2,j0+2,L+4),poiSpot(i0+2,j0,L),poiSpot(i0+1,j0+1,L+3));
    blds.push({pieces:K.P.slice(n1),spots:s2,kind:'keep'}); }
  // --- the barracks: a log hall along the north wall
  { const n1=K.P.length, s2={chest:[],floor:[]}, i0=i(-4), j0=j(-4); K.slab(i0,j0,3,2,L,wood); K.shell(i0,j0,3,2,L,1,wood,(f,k)=>f==='s'&&k===1?POI_DOOR:f==='s'||f==='n'?(k===1?511:POI_WIN):511); K.roof(i0,j0,3,2,L+1,wood);
    for(const [x,z] of [[-18.6,-18.3],[-18.6,-11.7],[-9.4,-18.3],[-9.4,-11.7],[-14,-18.3]]){ D.sbox(1.0,0.45,2.1,X(x),y0,Z(z),0x6b4a2e); D.box(1.0,0.12,2.0,X(x),y0+0.45,Z(z),0xd9ccb4); }
    s2.chest.push(poiSpot(i0+2,j0,L,0,0.6)); s2.floor.push(poiSpot(i0,j0+1,L)); blds.push({pieces:K.P.slice(n1),spots:s2,kind:'barracks'}); }
  // --- the smithy: an open shed over a glowing forge, north-east
  { const n1=K.P.length, s2={chest:[],floor:[]}, i0=i(1), j0=j(-4); K.slab(i0,j0,2,2,L,stone3); K.shell(i0,j0,2,2,L,1,wood2,f=>f==='n'?511:POI_OPEN); K.roof(i0,j0,2,2,L+1,wood2);
    const fx=X(7.6), fz=Z(-17.6); D.sbox(2,1,2,fx,y0,fz,0x6e6458); D.box(1.6,0.12,1.6,fx,y0+1,fz,0xff6a1f,null,true); D.cyl(0.25,0.9,2.2,fx,y0+1.1,fz,0x3a3530,8); D.tube(0.25,3.6,fx,y0+5,fz,0x3a3530);
    D.sbox(0.5,0.6,0.5,X(11.4),y0,Z(-12.4),0x4a4440); D.box(0.9,0.25,0.4,X(11.4),y0+0.6,Z(-12.4),0x2a2a2e); D.solid(X(11.4)-0.45,y0+0.6,Z(-12.4)-0.2,X(11.4)+0.45,y0+0.85,Z(-12.4)+0.2);
    D.scyl(0.4,0.9,X(13.4),y0,Z(-18.6),0x6b4a2e,10); for(let k=0;k<5;k++) D.box(0.06,1.2,0.06,X(6.2+k*0.3),y0+0.2,Z(-19.5),0x9aa3ab);
    s2.chest.push(poiSpot(i0+1,j0+1,L,0.6,0.5)); blds.push({pieces:K.P.slice(n1),spots:s2,kind:'smithy'}); }
  // --- the stable, west side, and the hay and the trough
  { const n1=K.P.length, s2={chest:[],floor:[]}, i0=i(-4), j0=j(1); K.slab(i0,j0,2,3,L,wood2); K.shell(i0,j0,2,3,L,1,wood2,(f,k)=>f==='e'?POI_OPEN:f==='w'?511:k===0?POI_OPEN:511); K.roof(i0,j0,2,3,L+1,wood2);
    for(const z of [10,15]){ D.box(4.6,1.3,0.12,X(-17.5),y0,Z(z),0x6b4a2e); D.solid(X(-19.8),y0,Z(z)-0.06,X(-15.2),y0+1.3,Z(z)+0.06); }
    for(const [x,z,h] of [[-18,6.6,0],[-16.8,7.4,0],[-17.4,7,1.2],[-11,21.5,0],[-12.3,21,0]]){ D.sbox(1.2,1.2,1.2,X(x+jit(0.1)),y0+h,Z(z),0xd9b24a); }
    D.sbox(2.4,0.5,0.6,X(-13.5),y0,Z(12.5),0x5a3d26); D.box(2.2,0.12,0.45,X(-13.5),y0+0.45,Z(12.5),0x5a8ac8);
    s2.chest.push(poiSpot(i0,j0+2,L)); s2.floor.push(poiSpot(i0+1,j0+1,L)); blds.push({pieces:K.P.slice(n1),spots:s2,kind:'stable'}); }
  // the well, the training yard, a cart, stalls by the east gate, dirt worn into the cobbles
  { const wx=X(-9), wz=Z(-7.5); D.scyl(1.1,0.9,wx,y0,wz,0x8f877a,14); D.cyl(0.95,0.95,0.05,wx,y0+0.85,wz,0x2a4a6a,14); for(const dx of [-0.95,0.95]) D.box(0.15,2.2,0.15,wx+dx,y0+0.9,wz,0x5a3d26); D.box(2.3,0.12,0.12,wx,y0+3.05,wz,0x5a3d26); D.box(2.6,0.1,1.6,wx,y0+3.2,wz,0x8a3a2e);
    for(const [x,z] of [[6.2,12.4],[8.6,14.6],[6.4,17.2]]){ D.scyl(0.12,1.9,X(x),y0,Z(z),0x6b4a2e,6); D.box(1,0.12,0.12,X(x),y0+1.4,Z(z),0x6b4a2e,[0,r(),0]); D.sph(0.3,X(x),y0+1.9,Z(z),0xd9b24a); D.cyl(0.35,0.3,0.7,X(x),y0+0.8,Z(z),0xd9b24a,8); }
    for(const [x,z,yw] of [[5.4,19.6,0.3],[-6,21.2,-0.2]]){ const g=new THREE.BoxGeometry(1.6,1.6,0.2); D.geo(g,0xd9b24a,X(x),y0+1.4,Z(z),[0.25,yw,0]); D.cyl(0.6,0.6,0.22,X(x),y0+1.4,Z(z),0xf2efe6,16,[Math.PI/2+0.25,yw,0]); D.cyl(0.35,0.35,0.24,X(x),y0+1.4,Z(z),0xc8443c,16,[Math.PI/2+0.25,yw,0]); for(const sx of [-0.55,0.55]){ const lg=new THREE.BoxGeometry(0.1,1.5,0.1); lg.translate(sx,0.75,0.12); D.geo(lg,0x6b4a2e,X(x),y0,Z(z),[-0.12,yw,0]); } { const bl=new THREE.BoxGeometry(0.1,1.3,0.1); bl.translate(0,0.65,-0.55); D.geo(bl,0x6b4a2e,X(x),y0,Z(z),[0.35,yw,0]); } solidTurned(D,X(x),Z(z),yw+Math.PI/2,0.3,0.8,y0,y0+2.2); }
    { const g=new THREE.BoxGeometry(1.6,0.5,2.8); D.geo(g,0x6b4a2e,X(11),y0+0.75,Z(-7),[0,0.4,0]); for(const s of [-0.85,0.85]){ const w=new THREE.CylinderGeometry(0.55,0.55,0.12,12); w.rotateZ(Math.PI/2); w.translate(s,0,0.4); D.geo(w,0x4a3424,X(11),y0+0.55,Z(-7),[0,0.4,0]); } D.solid(X(11)-1.1,y0,Z(-7)-1.4,X(11)+1.1,y0+1,Z(-7)+1.4); }
    for(const [x,z,c] of [[9.2,6.6,0xb3262e],[17.6,6.2,0x2a5ea8]]){ D.sbox(3,0.9,1.2,X(x),y0,Z(z),0x6b4a2e); for(const dx of [-1.4,1.4]) for(const dz of [-0.5,0.9]) D.box(0.1,2.3,0.1,X(x+dx),y0,Z(z+dz),0x5a3d26);
      D.box(3.4,0.08,2,X(x),y0+2.3,Z(z+0.2),c,[0.25,0,0]); for(let k=0;k<4;k++) D.sph(0.16,X(x-1+k*0.66),y0+1.05,Z(z),[0xe23a3a,0xf2c014,0x7cbf3a,0xff8a3d][k]); } }
  // a trebuchet in the middle of the yard, its arm down and its sling laid out; supply crates and barrels by the
  // barracks and the smithy; a rack of spears by the training yard
  { const tx=X(-1), tz=Z(-1), WD=0x6b4a2e, WD2=0x5a3d26; D.obj('wood',800);
    for(const sx of [-1.3,1.3]){ D.box(0.36,0.36,6.2,tx+sx,y0,tz,WD); for(const [zc,a] of [[-1.0,0.38],[1.0,-0.38]]) D.box(0.3,5.4,0.3,tx+sx,y0+2.5-2.7+0.05,tz+zc,WD,[a,0,0]); D.box(0.2,0.2,3.2,tx+sx,y0+1.6,tz,WD2); }
    for(const zc of [-2.9,2.9,0]) D.box(2.96,0.3,0.3,tx,y0+(zc?0:0.36),tz+zc,WD2); D.tube(0.16,3.1,tx,y0+5,tz,0x3a3530,[0,0,Math.PI/2]);
    { const g=new THREE.BoxGeometry(0.3,0.3,8); g.translate(0,0,-1.5); D.geo(g,WD,tx,y0+5,tz,[-0.55,0,0]); const ez=2.5*Math.cos(0.55), ey=5+2.5*Math.sin(0.55);
      D.box(0.08,1.0,0.08,tx-0.3,y0+ey-1.0,tz+ez,0x2a2a2e); D.box(0.08,1.0,0.08,tx+0.3,y0+ey-1.0,tz+ez,0x2a2a2e); D.box(1.4,1.3,1.4,tx,y0+ey-2.3,tz+ez,0x7a6a58); for(const dy of [0.15,1.1]) D.box(1.46,0.1,1.46,tx,y0+ey-2.3+dy,tz+ez,0x2a2a2e);
      const lz=-5.5*Math.cos(0.55), ly=5-5.5*Math.sin(0.55); D.box(0.05,0.05,Math.hypot(ly,1.2),tx,y0+ly/2,tz+lz-0.6,0x8a7a5a,[-Math.atan2(ly,1.2),0,0]); D.sph(0.45,tx,y0+0.45,tz+lz-1.4,0x8f897d); D.box(0.7,0.06,0.5,tx,y0,tz+lz-1.4,0x8a7a5a); }
    D.solid(tx-1.5,y0,tz-3.1,tx+1.5,y0+0.4,tz+3.1); for(const sx of [-1.3,1.3]) D.solid(tx+sx-0.2,y0+0.4,tz-2.2,tx+sx+0.2,y0+5.2,tz+2.2); { const cz=tz+2.5*Math.cos(0.55), cy=y0+5+2.5*Math.sin(0.55)-2.3; D.solid(tx-0.7,cy,cz-0.7,tx+0.7,cy+1.3,cz+0.7); } D.end(); }
  for(const [x,z,h,c] of [[-3.6,-8.6,0,0x9c7a4c],[-2.4,-8.4,0,0x8a6a40],[-3.0,-8.5,1.0,0x9c7a4c],[-1.6,-9.4,0,0xa9814e]]){ D.obj('wood',110); D.sbox(1,1,1,X(x),y0+h,Z(z),c); D.box(1.02,0.1,1.02,X(x),y0+h+0.45,Z(z),0x6e5233); D.end(); }
  for(const [x,z] of [[3.6,-8.4],[3.0,-7.6],[4.2,-7.5]]){ D.obj('wood',120); D.scyl(0.36,0.9,X(x),y0,Z(z),0x7a5230,12); D.cyl(0.38,0.38,0.05,X(x),y0+0.25,Z(z),0x3a3a3a,12); D.cyl(0.38,0.38,0.05,X(x),y0+0.65,Z(z),0x3a3a3a,12); D.end(); }
  { const rx=X(7.5), rz=Z(10.8); D.obj('wood',140); for(const dx of [-1,1]) D.box(0.12,1.6,0.12,rx+dx,y0,rz,0x5a3d26); D.box(2.2,0.1,0.12,rx,y0+1.2,rz,0x5a3d26); D.box(2.2,0.1,0.4,rx,y0+0.25,rz,0x5a3d26);
    for(let k=0;k<5;k++){ D.box(0.05,2.4,0.05,rx-0.8+k*0.4,y0+0.3,rz+0.05,0x8a6a40,[0.12,0,0]); D.cyl(0.0,0.06,0.25,rx-0.8+k*0.4,y0+2.64,rz+0.2,0x9aa3ab,6,[0.12,0,0]); } D.solid(rx-1.1,y0,rz-0.25,rx+1.1,y0+1.6,rz+0.35); D.end(); }
  // a worn dirt apron outside the walls, out to each gate's road and round the ruin; cobbles inside (drawn over it)
  { const out=[rectIn(-34,-34,29,29,0)]; if(gW) out.push(rectIn(-42,-6,-30,6,0)); if(gE) out.push(rectIn(25,-6,41,6,0)); if(gN) out.push(rectIn(-6,-42,6,-30,0)); if(gS) out.push(rectIn(-6,25,6,41,0)); out.push(discIn(-27,22,9));
    poiGround(t,'dirt',anyIn(out),2.2); }
  poiGround(t,'cobble',rectIn(-30,-30,25,25,-1.5),1.2,rectIn(-30,-30,25,25,-0.2));
  return blds; };

/* Crater Labs: a two-storey research centre, an observatory dome, a hangar with a rover, a rocket on its pad beside a
   climbable service gantry (stairs all the way to the top and a bridge to the capsule), satellite dishes, solar
   panels, glowing tanks and a helipad. Concrete. */
POI_BUILD.labs=(t,D)=>{ const K=poiKit(t), L=K.L, X_=poiCtx(t), {i,j,X,Z,y0,C,jit,r}=X_, blds=[], pad=[];
  const lab=poiSkin('lab',0,'brick',{s:{floor:'tile',tread:'plate',beam:0x3e454c}}), lab2=poiSkin('lab',1,'metal',{s:{floor:'concrete',tread:'plate',beam:0x3e454c}});
  const roofS=poiSkin('lab',0,'brick',{s:{floor:'tar',beam:0x3e454c}}), steel=poiSkin('corr',1,'metal',{s:{floor:'plate',tread:'plate',beam:0xc0392b}});
  // --- the research centre: cells -6..-2 by -5..-3, two floors, flat roof
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-6), j0=j(-5);
    K.slab(i0,j0,5,3,L,lab); K.slab(i0,j0,5,3,L+1,lab,(a,b)=>a===i0+2&&b===j0+1); K.slab(i0,j0,5,3,L+2,roofS);
    K.shell(i0,j0,5,3,L,2,lab,(f,k,s)=>{ if(s===0){ if(f==='s'&&k===2) return POI_DOOR; if(f==='e'&&k===1) return POI_DOOR; } return k===0&&f==='w'?511:POI_WIN; });
    K.shell(i0,j0,5,3,L+2,1,lab,()=>POI_LOW); K.ramp(i0+2,j0+1,L,3,lab);
    for(const b of [j0,j0+2]) K.wallX(i0+3,b,L,POI_DOOR,lab,{inner:1});                // a partition with two doorways
    const bench=[[3.6,0.95,0.9,2.5,0,2.5,0xd5dade],[3.6,0.06,0.9,2.5,0.95,2.5,0x2c3e50],[0.25,0.5,0.25,1.4,1.0,2.4,0x9ae6ff,false,true],[0.25,0.35,0.25,2.4,1.0,2.6,0x7cff9a,false,true],[0.2,0.6,0.2,3.4,1.0,2.4,0xff9ae6,false,true]];
    for(const [a,b,l] of [[0,0,L],[4,2,L],[1,2,L+1],[4,0,L+1]]){ const fl=poiFind(K,i0+a,j0+b,l); if(fl) poiFix(fl,bench); }
    const desk=poiFind(K,i0+3,j0+2,L); if(desk) poiFix(desk,[[3.2,1.05,0.9,2.5,0,1.3,0xe9edf0],[3.2,0.08,1.0,2.5,1.05,1.3,0x22b3c4],[0.7,0.45,0.05,2.0,1.13,1.0,0x1d2329,false],[0.6,0.36,0.04,2.0,1.17,0.97,0x5ec8ff,false,true]]);
    const ant=poiFind(K,i0+1,j0+1,L+2); if(ant) poiFix(ant,[[0.15,7,0.15,2.5,0,2.5,0xc9d2dc],[0.3,0.3,0.3,2.5,7,2.5,0xff3b3b,false,true],[1.6,0.12,0.12,2.5,4.5,2.5,0xc9d2dc,false],[1.1,0.12,0.12,2.5,5.6,2.5,0xc9d2dc,false]]);
    sp.chest.push(poiSpot(i0,j0+2,L),poiSpot(i0+4,j0+1,L+1),poiSpot(i0+3,j0,L+2)); sp.floor.push(poiSpot(i0+1,j0+1,L),poiSpot(i0+3,j0+1,L+1),poiSpot(i0+1,j0,L));
    blds.push({pieces:K.P.slice(n0),spots:sp,kind:'research'}); pad.push(rectIn(-30,-25,-5,-10,4));
    // tanks of something glowing, in a row outside the east door
    for(const [x,z,c] of [[-1.6,-21.6,0x58ff8a],[-1.6,-18.4,0x58e8ff],[0.6,-23.2,0x58ff8a]]){ D.scyl(0.9,0.4,X(x),y0,Z(z),0x55606a,14); D.cyl(0.8,0.8,2.4,X(x),y0+0.4,Z(z),c,14,null,true); D.cyl(0.95,0.95,0.3,X(x),y0+2.8,Z(z),0x55606a,14); D.solid(X(x)-0.8,y0,Z(z)-0.8,X(x)+0.8,y0+3.1,Z(z)+0.8); } }
  // --- the observatory: a drum with a dome and the telescope out of its slit
  { const ox=-15, oz=17, R=6.5; D.scyl(R,6,X(ox),y0,Z(oz),0xe9edf0,28); D.cyl(R+0.2,R+0.2,0.4,X(ox),y0+6,Z(oz),0x9aa3ab,28);
    const dome=new THREE.SphereGeometry(R,28,14,0,Math.PI*2,0,Math.PI/2); D.geo(dome,0xdfe4e8,X(ox),y0+6.4,Z(oz));
    for(let h=0;h<R-0.5;h+=1.1){ const rr=Math.sqrt(R*R-h*h); D.solid(X(ox)-rr*0.7,y0+6.4+h,Z(oz)-rr*0.7,X(ox)+rr*0.7,y0+6.4+h+1.1,Z(oz)+rr*0.7); }
    { const g=new THREE.BoxGeometry(1.4,R*1.05,0.3); g.translate(0,R*0.5,R*0.62); D.geo(g,0x2c3036,X(ox),y0+6.4,Z(oz),[-0.6,0.7,0]); const tl=new THREE.CylinderGeometry(0.55,0.75,5.4,14); tl.rotateX(-0.9); D.geo(tl,0x3e454c,X(ox)+2.1,y0+10.5,Z(oz)+2.6,[0,0.7,0]); }
    D.box(1.8,2.4,0.3,X(ox),y0,Z(oz)-R+0.05,0x2c3036); D.box(2.6,0.12,1.2,X(ox),y0+2.4,Z(oz)-R-0.3,0x9aa3ab); pad.push(discIn(ox,oz,R+3)); }
  // --- the hangar: cells 2..4 by -7..-4, two storeys tall, its whole south end open
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(2), j0=j(-7);
    K.slab(i0,j0,3,4,L,lab2); K.slab(i0,j0,3,4,L+2,roofS);
    K.shell(i0,j0,3,4,L,2,lab2,(f,k,s)=>{ if(f==='s'&&k<=1) return null; if(f==='s') return 511; if(s===1) return k%2?POI_WIN:511; return f==='w'&&k===2?POI_DOOR:511; });
    K.shell(i0,j0,3,4,L+2,1,roofS,()=>POI_LOW);
    // the rover: six wheels, a cab, a mast
    { const rx=X(16), rz=Z(-24); D.sbox(2.6,1.0,4.6,rx,y0+0.7,rz,0xe9edf0); D.sbox(2.2,1.0,1.8,rx,y0+1.7,rz-1.1,0xd5dade); D.box(2.0,0.6,0.05,rx,y0+2.0,rz-2.02,0x5ec8ff,null,true);
      for(const dz of [-1.7,0,1.7]) for(const dx of [-1.45,1.45]){ const w=new THREE.CylinderGeometry(0.62,0.62,0.45,14); w.rotateZ(Math.PI/2); D.geo(w,0x2c3036,rx+dx,y0+0.62,rz+dz); }
      D.box(0.12,1.8,0.12,rx+0.8,y0+2.7,rz+1.4,0x9aa3ab); D.sph(0.45,rx+0.8,y0+4.6,rz+1.4,0xf2f2f2,[1,0.3,1]); }
    for(const [x,z,h] of [[12.2,-33.4,0],[13.5,-33,0],[12.8,-33.2,1.2],[23.6,-29.6,0]]) D.sbox(1.2,1.2,1.2,X(x),y0+h,Z(z),0x8a9aa8);
    sp.chest.push(poiSpot(i0+2,j0,L),poiSpot(i0,j0+1,L)); sp.floor.push(poiSpot(i0+1,j0+3,L)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'hangar'}); pad.push(rectIn(10,-35,25,-15,4),rectIn(12,-15,23,-6,2)); }
  // --- the rocket on its pad, and its service gantry: a stair tower of map pieces climbing six storeys
  { const n0=K.P.length, sp={chest:[],floor:[]}, P=i(1), Q=i(2), r0=j(1), r1=j(2), r2=j(3);
    K.ramp(P,r1,L,3,steel);
    for(let s=1;s<=5;s++){ const l=L+s, north=s%2===1, row=north?r0:r2;
      if(s<5){ K.floor(P,row,l,steel); K.floor(Q,row,l,steel); K.ramp(north?Q:P,r1,l,north?1:3,steel); }
      else { for(const c of [P,Q]) for(const rr of [r0,r1,r2]) if(!(c===P&&rr===r1)) K.floor(c,rr,l,steel); } }
    for(let s=1;s<=4;s++){ const l=L+s, row=s%2===1?r0:r2; K.wallZ(P,s%2===1?r0:r2+1,l,POI_LOW,steel); K.wallZ(Q,s%2===1?r0:r2+1,l,POI_LOW,steel); K.wallX(P,row,l,POI_LOW,steel); }
    K.wallZ(P,r0,L+5,POI_LOW,steel); K.wallZ(Q,r0,L+5,POI_LOW,steel); K.wallZ(P,r2+1,L+5,POI_LOW,steel); K.wallZ(Q,r2+1,L+5,POI_LOW,steel); for(const rr of [r0,r1,r2]) K.wallX(P,rr,L+5,POI_LOW,steel); K.wallX(Q+1,r0,L+5,POI_LOW,steel); K.wallX(Q+1,r2,L+5,POI_LOW,steel);
    const top=poiFind(K,Q,r0,L+5); if(top) poiFix(top,[[0.9,0.5,0.9,1.2,0,1.2,0x2c3036],[0.6,0.4,0.05,1.2,0.5,0.8,0x5ec8ff,false,true]]);
    sp.chest.push(poiSpot(Q,r2,L+5),poiSpot(P,r0,L+3)); sp.floor.push(poiSpot(Q,r0,L+1),poiSpot(P,r2,L+4)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'gantry'});
    // the steelwork round the tower, in red and white
    for(const [x,z] of [[5,5],[15,5],[5,20],[15,20]]){ for(let s=0;s<6;s++) D.box(0.35,LVL,0.35,X(x),y0+s*LVL,Z(z),s%2?0xf2f2f2:0xc0392b); D.solid(X(x)-0.18,y0,Z(z)-0.18,X(x)+0.18,y0+6*LVL,Z(z)+0.18); }
    for(let s=0;s<6;s++) for(const [x0,z0,x1,z1] of [[5,5,15,5],[5,20,15,20]]){ const g=new THREE.BoxGeometry(0.14,0.14,Math.hypot(x1-x0,LVL)); D.geo(g,0x9aa3ab,X((x0+x1)/2),y0+s*LVL+LVL/2,Z(z0),[0,Math.PI/2,s%2?0.68:-0.68]); }
    // the rocket
    const rx=X(21.5), rz=Z(12.5); D.sbox(11,0.6,11,rx,y0,rz,0x9aa3ab); D.box(4,0.62,4,rx,y0,rz,0x2c3036);
    D.scyl(1.9,22,rx,y0+2.2,rz,0xf2f2f2,20); for(const h of [6,13,20]) D.cyl(1.94,1.94,0.5,rx,y0+2.2+h,rz,0x2c3036,20);
    D.cyl(1.2,1.9,4,rx,y0+24.2,rz,0xf2f2f2,20); D.cyl(0.05,1.2,2.6,rx,y0+28.2,rz,0xc0392b,20); D.box(1.0,1.2,0.1,rx-1.92,y0+22.4,rz,0x2c3036);
    for(let k=0;k<4;k++){ const a=k*Math.PI/2+Math.PI/4, g=new THREE.BoxGeometry(0.2,4.2,2.2); g.translate(0,0,2.3); D.geo(g,0xc0392b,rx,y0+2.1+2.1,rz,[0,a,0]); D.cyl(0.55,0.75,1.2,rx+Math.sin(a)*1.1,y0+1.0,rz+Math.cos(a)*1.1,0x3e454c,12); }
    D.solid(rx-3,y0,rz-3,rx+3,y0+2.2,rz+3);
    D.sbox(4.4,0.2,1.4,X(17.4),y0+5*LVL-0.2,rz,0x9aa3ab); for(const dz of [-0.7,0.7]) D.box(4.4,1.0,0.06,X(17.4),y0+5*LVL,rz+dz,0xc0392b); // the bridge to the capsule hatch
    pad.push(rectIn(4,4,28,21,3)); }
  // --- satellite dishes, solar panels, a helipad with a helicopter, a guard hut
  { for(const [x,z,yw] of [[-35,14,0.6],[-26,25,1.3]]){ D.scyl(0.7,5,X(x),y0,Z(z),0xd5dade,12); D.box(2.2,0.8,2.2,X(x),y0,Z(z),0x9aa3ab); D.solid(X(x)-1.1,y0,Z(z)-1.1,X(x)+1.1,y0+0.8,Z(z)+1.1);
      const dish=new THREE.SphereGeometry(4.6,24,10,0,Math.PI*2,0,0.75); dish.scale(1,0.55,1); dish.rotateX(Math.PI); D.geo(dish,0xf2f2f2,X(x),y0+7.6,Z(z),[0.9,yw,0]);
      const back=dish.clone(); D.geo(back,0xb9c2c9,X(x),y0+7.55,Z(z),[0.9,yw,0]); const ft=new THREE.CylinderGeometry(0.06,0.06,3.6,6); ft.translate(0,1.8,0); D.geo(ft,0x55606a,X(x),y0+6.8,Z(z),[0.9,yw,0]); D.sph(0.35,X(x)+Math.sin(yw)*2.6,y0+9.2,Z(z)+Math.cos(yw)*2.6,0x2c3036); }
    for(let row=0;row<4;row++) for(let k=0;k<3;k++){ const x=-38.5+row*3.2, z=-6+k*6.2+jit(0.3); if(!X_.inR(x,z,2)) continue; const g=new THREE.BoxGeometry(2.4,0.08,5); D.geo(g,0x1f3a5f,X(x),y0+1.2,Z(z),[0,0,-0.5]); D.box(0.12,1.0,0.12,X(x),y0,Z(z),0x9aa3ab); D.solid(X(x)-1.1,y0,Z(z)-2.5,X(x)+1.1,y0+1.6,Z(z)+2.5); }
    { const hx=X(-3), hz=Z(29); const pd=new THREE.CylinderGeometry(6,6,0.25,32); D.geo(pd,0x6b737a,hx,y0+0.13,hz); D.solid(hx-4.2,y0,hz-4.2,hx+4.2,y0+0.25,hz+4.2);
      const ring=new THREE.TorusGeometry(5.2,0.18,6,40); ring.rotateX(Math.PI/2); D.geo(ring,0xf2f2f2,hx,y0+0.27,hz); for(const [w,d,dx] of [[0.6,4,-1.3],[0.6,4,1.3],[2,0.6,0]]) D.box(w,0.04,d,hx+dx,y0+0.26,hz,0xf2f2f2);
      const yw=0.8; D.geo(new THREE.SphereGeometry(1.5,16,10).scale(1,0.85,1.6),0xd35400,hx,y0+1.7,hz,[0,yw,0]); D.solid(hx-1.4,y0+0.25,hz-1.4,hx+1.4,y0+3,hz+1.4);
      { const tb=new THREE.CylinderGeometry(0.2,0.35,4.6,10); tb.rotateX(Math.PI/2); tb.translate(0,0,3.6); D.geo(tb,0xd35400,hx,y0+2.0,hz,[0,yw,0]); }
      for(const a of [0.3,2.4]){ const bl=new THREE.BoxGeometry(9,0.06,0.4); D.geo(bl,0x2c3036,hx,y0+3.25,hz,[0,a,0]); } D.cyl(0.12,0.12,0.6,hx,y0+2.7,hz,0x2c3036,8);
      for(const dx of [-1,1]){ const sk=new THREE.BoxGeometry(0.12,0.12,3.2); sk.translate(dx,0,0); D.geo(sk,0x2c3036,hx,y0+0.4,hz,[0,yw,0]); } pad.push(discIn(-3,29,7)); }
    D.sbox(2.6,2.6,2.6,X(32),y0,Z(5.5),0xe9edf0); D.box(2.8,0.2,2.8,X(32),y0+2.6,Z(5.5),0x22b3c4); D.box(1.2,0.8,0.05,X(32),y0+1.4,Z(4.18),0x5ec8ff,null,true); // the guard hut by the east gate
    D.box(5,0.12,0.12,X(35),y0+1.0,Z(3.2),0xc0392b,[0,0,0.35]); D.box(0.25,1.1,0.25,X(32.6),y0,Z(3.2),0x55606a);
    for(const [x,z] of [[-8,-4],[8,-8],[-20,4],[30,-4],[6,26],[-34,-14]]){ if(!X_.inR(x,z,1)) continue; D.box(0.2,7,0.2,X(x),y0,Z(z),0xc9d2dc); D.box(1.2,0.3,0.4,X(x),y0+7,Z(z),0x3e454c); D.box(1.0,0.06,0.3,X(x),y0+6.96,Z(z),0xfff3cf,null,true); D.solid(X(x)-0.1,y0,Z(z)-0.1,X(x)+0.1,y0+7,Z(z)+0.1); }
    pad.push(rectIn(-40,-12,-26,12,2),rectIn(-14,-10,40,8,3),rectIn(-4,26,4,40,2),rectIn(30,-5,40,5,2),discIn(-30,15,8)); }
  poiRig(D,X(-8.2),y0,Z(4),Math.PI/2,{cab:0xe6e6df,trailer:'box',tcol:0xf5f7f9,stripe:0x22b3c4,len:9.6}); pad.push(rectIn(-21,2,-2,6,1)); // a supply lorry in from the launch contractor
  poiGround(t,'concrete',anyIn(pad),2.4);
  return blds; };

/* Timber Yard: an open-sided sawmill with a big blade, log cabins (one with an upstairs), log piles and stacks of
   cut planks, a log loader, a flatbed loaded with logs, a wooden water tower, a campfire, stumps. Dirt and sawdust. */
POI_BUILD.timber=(t,D)=>{ const K=poiKit(t), L=K.L, X_=poiCtx(t), {i,j,X,Z,y0,C,jit,r}=X_, blds=[], pad=[];
  const logS=poiSkin('log',0,'wood',{roof:'wood',roofCol:1,s:{floor:'plank',tread:'plank',beam:0x5a3a1e}}), logS2=poiSkin('log',1,'wood',{roof:'wood',roofCol:3,s:{floor:'plank',tread:'plank',beam:0x4a2e16}});
  const shed=poiSkin('log',1,'wood',{roof:'wood',roofCol:0,s:{floor:'plank',tread:'plank',beam:0x4a2e16}});
  // --- the sawmill: cells -3..0 by -6..-4, open on three sides
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-3), j0=j(-6); K.slab(i0,j0,4,3,L,shed); K.shell(i0,j0,4,3,L,1,shed,f=>f==='n'?511:POI_OPEN); K.roof(i0,j0,4,3,L+1,shed);
    const bx=X(-6), bz=Z(-22.5); D.sbox(12,0.9,1.6,X(-6),y0,bz,0x6b4a2e); for(let x=-11.5;x<-0.5;x+=1.2) D.box(0.15,0.08,1.7,X(x),y0+0.9,bz,0x9aa3ab); // the carriage bed
    D.cyl(1.4,1.4,0.06,bx,y0+1.1,bz,0xc9d2dc,28,[0,0,Math.PI/2]); D.box(0.4,1.2,1.2,bx,y0+0.9,bz+0.9,0x3a3d42); // the blade
    D.scyl(0.45,9,X(-10.5),y0+0.9,bz,0x8a5a32,10); const lg=new THREE.CylinderGeometry(0.45,0.5,9,12); lg.rotateZ(Math.PI/2); D.geo(lg,0x8a5a32,X(-10.5),y0+1.35,bz); D.solid(X(-15),y0+0.9,bz-0.5,X(-6.5),y0+1.8,bz+0.5);
    for(const [x,z,s] of [[4,-21,1.6],[1,-16.8,1.4],[-9,-16.4,1.2]]){ const g=new THREE.ConeGeometry(s,s*0.7,12); D.geo(g,0xd9b77a,X(x),y0+s*0.35,Z(z)); }
    for(let k=0;k<4;k++) D.sbox(1.2,0.6,4.8,X(-13.5+k*0.0),y0+k*0.6,Z(-27.4),0xc89a62);
    sp.chest.push(poiSpot(i0+3,j0,L,0,0.8),poiSpot(i0,j0+2,L)); sp.floor.push(poiSpot(i0+2,j0+2,L)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'sawmill'}); pad.push(rectIn(-15,-30,5,-15,5)); }
  // --- a log cabin, north-east, one room with a porch
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(3), j0=j(-5); K.slab(i0,j0,2,2,L,logS); K.shell(i0,j0,2,2,L,1,logS,(f,k)=>f==='s'&&k===0?POI_DOOR:f==='n'?511:POI_WIN); K.roof(i0,j0,2,2,L+1,logS);
    D.sbox(10,0.3,2.3,X(20),y0,Z(-13.7),0x8a5a32); for(const x of [15.4,24.6]) D.box(0.2,2.48,0.2,X(x),y0+0.3,Z(-12.8),0x6b4a2e); D.box(10.2,0.15,2.6,X(20),y0+2.82,Z(-13.55),0x4a2e16,[0.12,0,0]);
    D.sbox(1.2,0.5,0.5,X(22),y0+0.3,Z(-13.4),0x6b4a2e); D.box(0.6,2.2,0.6,X(23.4),y0,Z(-21.6),0x6e6458); D.box(0.9,6.6,0.9,X(25.6),y0,Z(-20),0x8f877a); D.box(1.1,0.2,1.1,X(25.6),y0+6.6,Z(-20),0x6e6458); D.tube(0.12,1.4,X(24.45),y0+1.9,Z(-21.6),0x3a3530,[0,0,Math.PI/2]); D.solid(X(25.15),y0,Z(-20.45),X(26.05),y0+6.6,Z(-19.55)); // bench, stove, chimney
    sp.chest.push(poiSpot(i0+1,j0,L)); sp.floor.push(poiSpot(i0,j0,L)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'cabin'}); pad.push(rectIn(15,-25,25,-12,3)); }
  // --- the foreman's house, south-west: 2x3 with an upstairs
  { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-7), j0=j(1); K.slab(i0,j0,2,3,L,logS2); K.slab(i0,j0,2,3,L+1,logS2,(a,b)=>a===i0+1&&b===j0+1);
    K.shell(i0,j0,2,3,L,2,logS2,(f,k,s)=>s===0&&f==='e'&&k===2?POI_DOOR:k===1?POI_WIN:511); K.roof(i0,j0,2,3,L+2,logS2); K.ramp(i0+1,j0+1,L,3,logS2);
    const bed=poiFind(K,i0,j0,L+1); if(bed) poiFix(bed,[[2,0.5,1.2,2.5,0,1.2,0x6b4a2e],[2,0.15,1.2,2.5,0.5,1.2,0xb3262e,false]]);
    const tb=poiFind(K,i0,j0+2,L); if(tb) poiFix(tb,[[1.6,0.8,1.0,2.5,0,2.5,0x6b4a2e],[0.5,0.5,0.5,1.2,0,2.5,0x5a3d26],[0.5,0.5,0.5,3.8,0,2.5,0x5a3d26]]);
    sp.chest.push(poiSpot(i0,j0+2,L+1),poiSpot(i0,j0+1,L)); sp.floor.push(poiSpot(i0+1,j0+2,L+1)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'house'}); pad.push(rectIn(-35,5,-25,20,4));
    // a campfire with log seats in front
    const fx=X(-19), fz=Z(15); for(let k=0;k<7;k++){ const a=k/7*Math.PI*2; D.box(0.35,0.25,0.25,fx+Math.cos(a)*0.7,y0,fz+Math.sin(a)*0.7,0x6e6458,[0,a,0]); }
    D.cyl(0.08,0.55,0.9,fx,y0+0.1,fz,0xff8a1f,8,null,true); D.cyl(0.05,0.3,0.6,fx+0.15,y0+0.1,fz-0.1,0xffd24a,8,null,true);
    for(const a of [0.4,2.2,4.1]){ const g=new THREE.CylinderGeometry(0.3,0.3,2.2,10); g.rotateZ(Math.PI/2); D.geo(g,0x8a5a32,fx+Math.cos(a)*2.4,y0+0.3,fz+Math.sin(a)*2.4,[0,-a+Math.PI/2,0]); D.solid(fx+Math.cos(a)*2.4-0.8,y0,fz+Math.sin(a)*2.4-0.8,fx+Math.cos(a)*2.4+0.8,y0+0.55,fz+Math.sin(a)*2.4+0.8); } pad.push(discIn(-19,15,5)); }
  // --- log piles, plank stacks, the log loader, a loaded flatbed, the water tower, stumps
  { const pile=(x,z,yw,n)=>{ const s=Math.sin(yw), co=Math.cos(yw); let h=0; for(let row=n;row>0;row--){ for(let k=0;k<row;k++){ const off=(k-(row-1)/2)*0.95, rr=0.44+r()*0.06, g=new THREE.CylinderGeometry(rr,rr*1.05,7+r()*0.8,12); g.rotateX(Math.PI/2);
          D.geo(g,[0x8a5a32,0x7a4e2c,0x94643a][Math.floor(r()*3)],X(x+co*off),y0+0.45+h,Z(z-s*off),[0,yw,0]); } h+=0.8; }
        solidTurned(D,X(x),Z(z),yw,n*0.42,3.5,y0,y0+h*0.8); };
    pile(-25,-12,0.3,5); pile(12,9,1.3,4); pile(24,22,-0.4,5); pile(-8,24,2.0,3); pile(-27,-25,0.9,3);
    for(const [x,z,yw,n] of [[10,-6,0.1,4],[16,-4,0.2,3],[6,16,-0.5,5]]){ for(let q=0;q<n;q++){ const g=new THREE.BoxGeometry(2.4,0.38,4.8); D.geo(g,q%2?0xd9b077:0xc89a62,X(x),y0+0.12+q*0.4+0.19,Z(z),[0,yw+(q%2?0.03:0),0]); }
      solidTurned(D,X(x),Z(z),yw,1.25,2.45,y0,y0+0.12+n*0.4); D.box(2.6,0.12,5,X(x),y0,Z(z),0x8c6a3f,[0,yw,0]); }
    // the log loader: four big tyres, an engine house at the back, a glazed cab, a boom with its ram and a grapple
    { const lx=X(-18), lz=Z(-3), Y=0xe0a326, DKk=0x1d1f22, GL=0x4f6f86; D.obj('metal',650);
      D.box(2.6,0.8,4.6,lx,y0+0.5,lz,Y); D.box(2.7,0.1,4.7,lx,y0+1.3,lz,0x3a3d42);
      for(const sx of [-1,1]) for(const sz of [-1.45,1.45]){ const w=new THREE.CylinderGeometry(0.62,0.62,0.55,16); w.rotateZ(Math.PI/2); D.geo(w,DKk,lx+sx*1.35,y0+0.62,lz+sz); const h=new THREE.CylinderGeometry(0.32,0.32,0.57,10); h.rotateZ(Math.PI/2); D.geo(h,Y,lx+sx*1.35,y0+0.62,lz+sz); }
      D.box(2.2,1.2,1.5,lx,y0+1.4,lz+1.5,Y); for(let k=0;k<4;k++) D.box(1.6,0.06,0.05,lx,y0+1.65+k*0.22,lz+2.26,DKk); D.cyl(0.08,0.08,1.2,lx+0.7,y0+2.6,lz+1.2,0x3a3d42,8); D.box(2.3,0.12,1.6,lx,y0+2.6,lz+1.5,0x3a3d42);
      D.box(1.7,1.8,1.7,lx,y0+1.4,lz-0.5,GL); for(const [dx,dz] of [[-0.88,-1.38],[0.88,-1.38],[-0.88,0.38],[0.88,0.38]]) D.box(0.1,1.8,0.1,lx+dx,y0+1.4,lz+dz,Y); D.box(2.0,0.15,2.0,lx,y0+3.2,lz-0.5,Y); D.box(0.7,0.5,0.6,lx,y0+1.4,lz-0.3,0x3a3d42);
      { const g=new THREE.BoxGeometry(0.45,0.5,5.5); g.translate(0,0,-2.75); D.geo(g,Y,lx,y0+2.0,lz-1.6,[0.45,0,0]); const tipZ=lz-1.6-5.5*Math.cos(0.45), tipY=y0+2.0+5.5*Math.sin(0.45);
        const c=new THREE.BoxGeometry(0.16,0.16,3.83); c.translate(0,0,-1.92); D.geo(c,0xc4cad1,lx+0.32,y0+1.25,lz-0.8,[0.549,0,0]); D.box(0.22,0.22,1.6,lx+0.32,y0+1.25+0.4,lz-1.4,0x3a3d42,[0.549,0,0]);
        D.box(0.15,0.7,0.15,lx,tipY-0.75,tipZ,0x3a3d42); D.box(0.5,0.3,0.5,lx,tipY-1.05,tipZ,0x3a3d42); for(const dz of [-0.22,0.22]){ const t=new THREE.TorusGeometry(0.62,0.1,6,12,Math.PI); D.geo(t,DKk,lx,tipY-1.2,tipZ+dz,[0,0,Math.PI]); } }
      D.solid(lx-1.45,y0,lz-2.3,lx+1.45,y0+3.35,lz+2.3); D.end(); }
    // a lumber drying shed: open all round on posts, racks of stickered boards inside
    { const n0=K.P.length, sp={chest:[],floor:[]}, i0=i(-2), j0=j(0); K.slab(i0,j0,3,2,L,shed); K.shell(i0,j0,3,2,L,1,shed,()=>POI_OPEN); K.roof(i0,j0,3,2,L+1,shed);
      for(const x of [-7.6,-2.5,2.6]) for(const z of [1.5,8.5]){ D.obj('wood',300); for(const dx of [-2,2]) for(const dz of [-0.6,0.6]) D.box(0.14,2.25,0.14,X(x+dx),y0+0.1,Z(z+dz),0x5a3d26);
        for(let q=0;q<4;q++){ const h=y0+0.2+q*0.55, n=2+((q+Math.round(x))%2+2)%2; for(let b=0;b<n;b++) D.box(4.1,0.1,1.15,X(x),h+b*0.11,Z(z),b%2?0xd9b077:0xc89a62); for(const dx of [-1.6,0,1.6]) D.box(0.08,0.06,1.2,X(x+dx),h-0.06,Z(z),0x8a5a32); }
        D.solid(X(x)-2.1,y0,Z(z)-0.7,X(x)+2.1,y0+2.35,Z(z)+0.7); D.end(); }
      sp.chest.push(poiSpot(i0+1,j0,L,0,2.4)); sp.floor.push(poiSpot(i0+2,j0+1,L,0,-2.3),poiSpot(i0,j0+1,L,0,-2.3)); blds.push({pieces:K.P.slice(n0),spots:sp,kind:'shed'}); }
    // the wood chipper on its trailer, and the heap of chips it throws
    { const cx=X(-3), cz=Z(-7.5); D.obj('metal',380); D.box(1.5,1.1,2.2,cx,y0+0.55,cz,0xd8702f); D.box(1.5,0.12,2.3,cx,y0+1.65,cz,0x3a3d42);
      for(const s of [-1,1]){ const w=new THREE.CylinderGeometry(0.42,0.42,0.3,12); w.rotateZ(Math.PI/2); D.geo(w,0x1d1f22,cx+s*0.92,y0+0.42,cz+0.3); } D.box(0.12,0.12,1.6,cx,y0+0.45,cz+1.8,0x3a3d42); D.box(0.3,0.5,0.3,cx,y0,cz+2.5,0x3a3d42);
      { const hp=new THREE.BoxGeometry(1.3,0.9,1.0); D.geo(hp,0xd8702f,cx,y0+1.15,cz-1.5,[-0.35,0,0]); const mo=new THREE.BoxGeometry(1.0,0.62,0.04); mo.translate(0,0.06,-0.51); D.geo(mo,0x1d1f22,cx,y0+1.15,cz-1.5,[-0.35,0,0]); const lip=new THREE.BoxGeometry(1.36,0.08,0.5); lip.translate(0,-0.3,-0.7); D.geo(lip,0x3a3d42,cx,y0+1.15,cz-1.5,[-0.35,0,0]); }
      D.tube(0.22,1.8,cx+0.3,y0+2.4,cz+0.4,0xd8702f,[0,0,-0.6]); D.box(0.5,0.35,0.5,cx+0.9,y0+3.1,cz+0.4,0xd8702f); D.solid(cx-0.8,y0,cz-2.4,cx+0.8,y0+1.8,cz+2.6); D.end();
      D.obj('wood',200); const pg=new THREE.ConeGeometry(2.1,1.3,14); D.geo(pg,0xc8a060,X(2.2),y0+0.65,Z(-7.2)); D.solid(X(2.2)-1.3,y0,Z(-7.2)-1.3,X(2.2)+1.3,y0+0.7,Z(-7.2)+1.3); D.end(); }
    // a lorry with a full load of logs, parked by the south road
    const rig=poiRig(D,X(-13),y0,Z(30.5),Math.PI/2,{cab:0x2f8f86,trailer:'logs',len:10});
    { const wx=X(22), wz=Z(12); for(const [dx,dz] of [[-2,-2],[2,-2],[-2,2],[2,2]]){ D.box(0.35,8,0.35,wx+dx,y0,wz+dz,0x6b4a2e); D.solid(wx+dx-0.18,y0,wz+dz-0.18,wx+dx+0.18,y0+8,wz+dz+0.18); }
      for(const h of [2.6,5.2]){ D.box(4.4,0.15,0.15,wx,y0+h,wz-2,0x5a3d26); D.box(4.4,0.15,0.15,wx,y0+h,wz+2,0x5a3d26); D.box(0.15,0.15,4.4,wx-2,y0+h,wz,0x5a3d26); D.box(0.15,0.15,4.4,wx+2,y0+h,wz,0x5a3d26); }
      D.sbox(5.4,0.3,5.4,wx,y0+8,wz,0x5a3d26); D.scyl(2.5,3.6,wx,y0+8.3,wz,0x9a6a3d,18); for(const h of [0.6,1.8,3]) D.cyl(2.55,2.55,0.12,wx,y0+8.3+h,wz,0x2a2a2e,18); D.cyl(0.2,2.8,1.4,wx,y0+11.9,wz,0x4a2e16,18); }
    for(let k=0;k<14;k++){ const x=-38+r()*76, z=-38+r()*76; if(!X_.inR(x,z,1)) continue; if(Math.abs(x+6)<14&&z<-12&&z>-32) continue; if(Math.hypot(x-22,z-12)<5||Math.hypot(x+19,z-15)<4||x>-12&&x<7&&z>-11&&z<12||x>13&&x<27&&z>-26&&z<-10||x>-37&&x<-23&&z>3&&z<22||nearSeg(X(x),Z(z),rig,2.4)) continue;
      const rr=0.35+r()*0.3; D.cyl(rr,rr*1.15,0.5+r()*0.4,X(x),y0,Z(z),0x8a5a32,10); D.cyl(rr*0.95,rr*0.95,0.03,X(x),y0+0.52,Z(z),0xd9b077,10); if(k%4===0){ D.box(0.06,0.7,0.06,X(x)+0.1,y0+0.6,Z(z),0x6b4a2e,[0,0,0.3]); D.box(0.04,0.2,0.32,X(x)+0.28,y0+0.95,Z(z),0x9aa3ab,[0,0,0.3]); } }
    pad.push(rectIn(-30,-15,30,26,1),rectIn(-27,27,-6,34,1.5),rectIn(-40,-5,-28,5,2),rectIn(28,-5,40,5,2),rectIn(-4,26,4,40,2)); }
  poiGround(t,'dirt',anyIn(pad),2.8);
  return blds; };

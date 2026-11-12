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
  { D.sbox(8,5,6,X(2),y0,Z(14),0x7a4a3a); D.sbox(8.4,0.35,6.4,X(2),y0+5,Z(14),0x35302e); D.box(1.6,2.4,0.15,X(2),y0,Z(10.93),0x2e2a28); for(const x of [-0.5,4.5]) D.box(1.2,1.1,0.15,X(x),y0+2.6,Z(10.93),0xffd98a,null,true);
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
      const ex=Math.abs(co)*3.05+Math.abs(s)*1.22, ez=Math.abs(s)*3.05+Math.abs(co)*1.22; D.solid(xx-ex,y,zz-ez,xx+ex,y+2.6,zz+ez); };
    [[17,15,0,0.02],[17,15,1,-0.03],[24.6,15.4,0,0.05],[17.4,18.6,0,0],[24,18.8,0,-0.04],[24,18.8,1,0.03],[24,18.8,2,0],[18.2,24.5,0,0.12],[25.2,24,0,-0.08],[31,13,0,1.57],[30.8,20.6,0,1.62]].forEach(([x,z,lv,yw])=>cont(x,z,lv,yw));
    for(const z of [11,28]) for(const x of [14,29]){ D.sbox(0.6,11,0.6,X(x),y0,Z(z),0xe0a326); } for(const z of [11,28]) D.sbox(15.6,0.9,0.9,X(21.5),y0+11,Z(z),0xe0a326); for(const x of [14,29]) D.box(0.7,0.7,17.6,X(x),y0+11.2,Z(19.5),0xe0a326);
    D.box(15,1.4,2.6,X(21.5),y0+11.9,Z(21),0xd4991c); D.box(2.4,2,2.4,X(22),y0+12.4,Z(21),0x3a3d42); D.tube(0.04,6,X(21.6),y0+9,Z(21),0x222222); D.tube(0.04,6,X(22.4),y0+9,Z(21),0x222222); D.box(1.4,0.5,0.5,X(22),y0+5.8,Z(21),0xe0a326);
    pad.push(rectIn(13,10,33,29,3)); }
  // --- trailers, pallets, barrels and barriers left about the yard; floodlights
  { const trailer=(x,z,yaw,c)=>{ const g=new THREE.BoxGeometry(2.5,2.8,9); D.geo(g,c,X(x),y0+2.5,Z(z),[0,yaw,0]); const ch=new THREE.BoxGeometry(2.2,0.4,9); D.geo(ch,0x2a2d31,X(x),y0+0.95,Z(z),[0,yaw,0]);
      for(const s of [-3.2,-2.2]){ const w=new THREE.CylinderGeometry(0.5,0.5,2.3,12); w.rotateZ(Math.PI/2); w.translate(0,0,s); D.geo(w,0x1d1f22,X(x),y0+0.5,Z(z),[0,yaw,0]); }
      const s=Math.abs(Math.sin(yaw)), co=Math.abs(Math.cos(yaw)), ex=co*1.25+s*4.5, ez=s*1.25+co*4.5; D.solid(X(x)-ex,y0+0.7,Z(z)-ez,X(x)+ex,y0+3.9,Z(z)+ez); };
    trailer(-14,-3.5,1.42,0xe9e7df); trailer(-6,1.2,1.66,0x2e86c1); trailer(-1,26,0.35,0xc0392b);
    for(let k=0;k<9;k++){ const x=-20+r()*36, z=-6+r()*12; if(Math.abs(x+14)<5.5&&Math.abs(z+3.5)<2.5||Math.abs(x+6)<5.5&&Math.abs(z-1.2)<2.5||Math.hypot(x+3,z-4)<1.8||Math.hypot(x+3,z+5)<1.8) continue; const h=r()<0.4?2:1;
      for(let q=0;q<h;q++) D.sbox(1.2,0.15,1.2,X(x),y0+q*0.9,Z(z),0x8c6a3f), D.sbox(1.1,0.75,1.1,X(x),y0+0.15+q*0.9,Z(z),[0xa9814e,0x6f8a9b,0xd7dadc][Math.floor(r()*3)]); }
    for(let k=0;k<7;k++){ const x=6+r()*5, z=-26+r()*6; D.scyl(0.32,0.9,X(x),y0,Z(z),[0x2e86c1,0xc0392b,0x3c8d3c][k%3],10); }
    for(const [x,z,yw] of [[-30,-4,0.1],[-30,4.5,-0.15],[36,-6,1.5],[-3,33,0.2]]){ const g=new THREE.BoxGeometry(3,0.9,0.6); D.geo(g,0xd8d4cc,X(x),y0+0.45,Z(z),[0,yw,0]); D.solid(X(x)-1.5,y0,Z(z)-0.6,X(x)+1.5,y0+0.9,Z(z)+0.6); }
    for(const [x,z] of [[-8,-6],[8,-30],[10,6],[-27,-6],[-20,15],[32,8]]){ D.box(0.25,9,0.25,X(x),y0,Z(z),0x55606a); D.box(1.6,0.6,0.5,X(x),y0+9,Z(z),0x2c3036); D.box(1.4,0.08,0.4,X(x),y0+8.95,Z(z),0xfff3cf,null,true); D.solid(X(x)-0.15,y0,Z(z)-0.15,X(x)+0.15,y0+9,Z(z)+0.15); }
    // a pipe run on stands from the boiler house to the hall
    const run=[[1,11],[-3,4],[-3,-5],[-3,-9.7]]; for(let k=0;k<run.length-1;k++){ const [xa,za]=run[k], [xb,zb]=run[k+1], len=Math.hypot(xb-xa,zb-za), yaw=Math.atan2(xb-xa,zb-za); D.tube(0.3,len,X((xa+xb)/2),y0+6.4,Z((za+zb)/2),0x2f7f6b,[Math.PI/2,yaw,0]); }
    for(const [x,z] of run.slice(1,3)){ D.sbox(0.4,6.2,0.4,X(x),y0,Z(z),0x6b737a); D.box(1.2,0.2,1.2,X(x),y0+6.1,Z(z),0x55606a); }
    pad.push(rectIn(-22,-8,20,8,4),rectIn(-38,-5,-30,5,2),rectIn(-4,30,4,40,2),rectIn(30,-5,40,5,2),rectIn(-4,-40,4,-30,2)); }
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
    for(let q=0;q<26;q++){ const x=(i0-X_.ci)*C+r()*14-2, z=(j0-X_.cj)*C+r()*14-2; if(!X_.inR(x,z,1)) continue; const sz=0.25+r()*0.75, g=new THREE.DodecahedronGeometry(sz,1); g.scale(1,0.6,1);
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
    for(const [x,z,yw] of [[5.4,19.6,0.3],[-6,21.2,-0.2]]){ const g=new THREE.BoxGeometry(1.6,1.6,0.2); D.geo(g,0xd9b24a,X(x),y0+1.4,Z(z),[0.25,yw,0]); D.cyl(0.6,0.6,0.22,X(x),y0+1.4,Z(z),0xf2efe6,16,[Math.PI/2+0.25,yw,0]); D.cyl(0.35,0.35,0.24,X(x),y0+1.4,Z(z),0xc8443c,16,[Math.PI/2+0.25,yw,0]); D.solid(X(x)-0.8,y0,Z(z)-0.3,X(x)+0.8,y0+2.2,Z(z)+0.3); }
    { const g=new THREE.BoxGeometry(1.6,0.5,2.8); D.geo(g,0x6b4a2e,X(11),y0+0.75,Z(-7),[0,0.4,0]); for(const s of [-0.85,0.85]){ const w=new THREE.CylinderGeometry(0.55,0.55,0.12,12); w.rotateZ(Math.PI/2); w.translate(s,0,0.4); D.geo(w,0x4a3424,X(11),y0+0.55,Z(-7),[0,0.4,0]); } D.solid(X(11)-1.1,y0,Z(-7)-1.4,X(11)+1.1,y0+1,Z(-7)+1.4); }
    for(const [x,z,c] of [[9.2,6.6,0xb3262e],[17.6,6.2,0x2a5ea8]]){ D.sbox(3,0.9,1.2,X(x),y0,Z(z),0x6b4a2e); for(const dx of [-1.4,1.4]) for(const dz of [-0.5,0.9]) D.box(0.1,2.3,0.1,X(x+dx),y0,Z(z+dz),0x5a3d26);
      D.box(3.4,0.08,2,X(x),y0+2.3,Z(z+0.2),c,[0.25,0,0]); for(let k=0;k<4;k++) D.sph(0.16,X(x-1+k*0.66),y0+1.05,Z(z),[0xe23a3a,0xf2c014,0x7cbf3a,0xff8a3d][k]); } }
  // a worn dirt apron outside the walls, out to each gate's road and round the ruin; cobbles inside (drawn over it)
  { const out=[rectIn(-34,-34,29,29,0)]; if(gW) out.push(rectIn(-42,-6,-30,6,0)); if(gE) out.push(rectIn(25,-6,41,6,0)); if(gN) out.push(rectIn(-6,-42,6,-30,0)); if(gS) out.push(rectIn(-6,25,6,41,0)); out.push(discIn(-27,22,9));
    poiGround(t,'dirt',anyIn(out),2.2); }
  poiGround(t,'cobble',rectIn(-30,-30,25,25,-1.5),1.2,rectIn(-30,-30,25,25,-0.2));
  return blds; };

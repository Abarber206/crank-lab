/* ---------- things lying about the island ----------
   Campsites in forest clearings (tents, a fire ring, log seats, a chest), power lines on wooden poles along the main
   roads, fenced hay fields outside two farm towns, benches, bins and fire hydrants in town, a wooden dock with
   rowboats on the beach at Pebble Point and boats pulled up on the river banks, fallen logs and stumps in the woods,
   picnic tables by the road, and clutter round the points of interest to suit each one. All of it is seeded (the same
   for everyone in a match), merged into a few meshes per 64 m patch, and solid where you'd bump into it. */
const DECOR={chests:[],camps:[],poles:0,items:0};
function buildWorldDecor(){ const D=poiDecor(), r=seeded(60613), S=SPAWN, PI=Math.PI; TOWNS.forEach(t=>{ if(t.kind) planPOI(t); }); DECOR.s0=STATICS.length; // (planning a point of interest adds its own solids: get that done first)
  const slope=(x,z)=>{ const e=1.5; return Math.max(Math.abs(terrainH(x+e,z)-terrainH(x-e,z)),Math.abs(terrainH(x,z+e)-terrainH(x,z-e)))/(2*e); };
  const nearRiver=(x,z,pad)=>{ const c=worldCell(x,z); return c>=0&&WORLD.RVD&&WORLD.RVD[c]<WORLD.RVW[c]+pad; };
  const wet=(x,z,pad)=>{ for(const [a,b] of [[0,0],[pad,0],[-pad,0],[0,pad],[0,-pad]]) if(shoreAt(x+a,z+b)) return true; return nearRiver(x,z,pad+2); };
  const placed=[]; const free=(x,z,R)=>!placed.some(([px,pz,pr])=>Math.hypot(px-x,pz-z)<pr+R);
  const staticNear=(x,z,R)=>STATICS.some(s=>s.solid&&Math.abs(s.x-x)<R+3&&Math.abs(s.z-z)<R+3&&s.solid.boxes.some(b=>Math.hypot(Math.max(b[0]-x,0,x-b[3]),Math.max(b[2]-z,0,z-b[5]))<R));
  const open=(x,z,R)=>Math.hypot(x-S[0],z-S[2])<MAP_R-45&&Math.hypot(x-S[0],z-S[2])>FLAT_R+30&&!townAt(x,z,R+18)&&roadDistAt(x,z)>R+5&&!wet(x,z,R)&&slope(x,z)<0.2&&free(x,z,R);
  const clearProps=(x,z,R,kinds)=>propsNear(x,z,[],Math.ceil(R/PCELL)+1).forEach(p=>{ if(!p.gone&&(!kinds||kinds.includes(p.kind))&&Math.hypot(p.x-x,p.z-z)<R){ p.gone=true; p.alive=false; p.g.visible=false; } });
  const treesNear=(x,z,R)=>propsNear(x,z,[],Math.ceil(R/PCELL)+1).filter(p=>!p.gone&&(p.kind==='tree'||p.kind==='pine')&&Math.hypot(p.x-x,p.z-z)<R).length;
  const rot=(x,z,a)=>[x*Math.cos(a)+z*Math.sin(a),-x*Math.sin(a)+z*Math.cos(a)]; // local (x across, z along) turned by a
  const at=(cx,cz,a,lx,lz)=>{ const [u,v]=rot(lx,lz,a); return [cx+u,cz+v]; };
  const H=(x,z)=>terrainH(x,z), Hm=(x,z,r)=>Math.min(H(x,z),H(x+r,z),H(x-r,z),H(x,z+r),H(x,z-r),H(x+r*0.7,z+r*0.7),H(x-r*0.7,z+r*0.7),H(x+r*0.7,z-r*0.7),H(x-r*0.7,z-r*0.7))-0.03; // the lowest ground under a footprint: set things there and nothing hangs in the air on a slope
  const WOOD=0x7a5a3c, DARKWOOD=0x5a4030, BARK=0x6b4e34, STONE=0x8d8a84;
  // a lying log: length along local z (turned by a)
  const log=(x,y,z,a,len,rad,c,solid,pitch)=>{ if(solid) D.obj('wood',Math.round(60+len*rad*90)); const p=pitch||0, rise=Math.sin(p)*len/2; D.geo(new THREE.CylinderGeometry(rad,rad*1.05,len,10),c||BARK,x,y+rad,z,[PI/2-p,a,0]); D.geo(new THREE.CircleGeometry(rad*0.92,10),0xc8a878,...at(x,z,a,0,len/2+0.005).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+rad+rise,0]),[-p,a,0]);
    if(solid){ const [ex,ez]=rot(0,len/2,a), hx=Math.abs(ex)+rad, hz=Math.abs(ez)+rad; D.solid(x-hx,y-Math.abs(rise),z-hz,x+hx,y+rad*2*0.9+Math.abs(rise),z+hz,'log'); D.end(); } };
  // an A-frame tent, ridge along local z: w wide, h high, L long
  const tentGeo=(w,h,L)=>{ const g=new THREE.BufferGeometry(), a=w/2, b=L/2, P=[ -a,0,-b, 0,h,-b, 0,h,b,  -a,0,-b, 0,h,b, -a,0,b,   a,0,-b, a,0,b, 0,h,b,  a,0,-b, 0,h,b, 0,h,-b,   -a,0,-b, a,0,-b, 0,h,-b ];
    for(let i=P.length-9;i>=0;i-=9) P.push(P[i+6],P[i+7],P[i+8],P[i+3],P[i+4],P[i+5],P[i],P[i+1],P[i+2]); // both sides (the faces are one-sided)
    g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); return g; };
  const tent=(x,z,a,col)=>{ const y=Hm(x,z,1.5), w=2.3, h=1.55, L=2.8; D.obj('wood',160); D.geo(tentGeo(w,h,L),col,x,y,z,[0,a,0]);
    { const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute([-0.42,0,0, 0.42,0,0, 0,1.1,0, 0.42,0,0, -0.42,0,0, 0,1.1,0],3)); const [dx,dz]=at(x,z,a,0,L/2+0.02); D.geo(g,0x2a2620,dx,y+0.01,dz,[0,a,0]); } // the door
    for(const s of [-1,1]){ const [px,pz]=at(x,z,a,0,s*(L/2+0.05)); D.cyl(0.03,0.03,h+0.12,px,y,pz,0x9a9a9a,6); }
    for(const [sx,sz] of [[-1,-1],[1,-1],[-1,1],[1,1]]){ const [px,pz]=at(x,z,a,sx*(w/2+0.35),sz*(L/2-0.3)); D.cyl(0.02,0.02,0.25,px,H(px,pz)-0.05,pz,0xd0d0c8,4); } // pegs
    const [hx,hz]=[Math.abs(Math.sin(a))*L/2+Math.abs(Math.cos(a))*w/2,Math.abs(Math.cos(a))*L/2+Math.abs(Math.sin(a))*w/2]; D.solid(x-hx*0.8,y,z-hz*0.8,x+hx*0.8,y+h*0.85,z+hz*0.8); D.end(); };
  const crate=(x,y,z,s,a,c)=>{ D.obj('wood',110); D.box(s,s,s,x,y,z,c||0x9c7a4c,[0,a,0]); D.box(s*1.02,s*0.12,s*1.02,x,y+s*0.44,z,0x6e5233,[0,a,0]); D.solid(x-s*0.6,y,z-s*0.6,x+s*0.6,y+s,z+s*0.6); D.end(); };
  const drum=(x,y,z,c)=>{ D.obj('metal',130); D.scyl(0.32,0.92,x,y,z,c,14); D.cyl(0.33,0.33,0.04,x,y+0.3,z,0x3a3a3a,14); D.cyl(0.33,0.33,0.04,x,y+0.62,z,0x3a3a3a,14); D.end(); };
  const bale=(x,z,a,up)=>{ const y=Hm(x,z,0.8); D.obj('wood',120); if(up){ D.scyl(0.78,1.15,x,y,z,0xd6b45a,16); D.cyl(0.7,0.7,0.02,x,y+1.15,z,0xc49a3e,16); D.end(); return; }
    D.geo(new THREE.CylinderGeometry(0.78,0.78,1.2,16),0xd6b45a,x,y+0.74,z,[PI/2,a,0]); for(const s of [-1,1]){ const [ex,ez]=at(x,z,a,0,s*0.61); D.geo(new THREE.CircleGeometry(0.74,16),0xc49a3e,ex,y+0.74,ez,[0,a+(s>0?0:PI),0]); }
    const [hx,hz]=[Math.abs(Math.sin(a))*0.6+Math.abs(Math.cos(a))*0.78,Math.abs(Math.cos(a))*0.6+Math.abs(Math.sin(a))*0.78]; D.solid(x-hx,y,z-hz,x+hx,y+1.5,z+hz); D.end(); };
  const fenceRun=(ax,az,bx,bz,gap)=>{ const L=Math.hypot(bx-ax,bz-az), n=Math.max(1,Math.round(L/2.5)), a=Math.atan2(bx-ax,bz-az), G=f=>!!(gap&&gap(f)); // each panel (rails and its posts) breaks on its own
    for(let q=0;q<n;q++){ const f0=q/n, f1=(q+1)/n; if(G(f0)||G(f1)||G((f0+f1)/2)) continue; const x0=ax+(bx-ax)*f0, z0=az+(bz-az)*f0, x1=ax+(bx-ax)*f1, z1=az+(bz-az)*f1, y0=H(x0,z0), y1=H(x1,z1), l=Math.hypot(x1-x0,z1-z0), tilt=Math.atan2(y1-y0,l);
      D.obj('wood',90); D.box(0.14,1.25,0.14,x0,y0-0.1,z0,DARKWOOD,[0,a,0]); if(q===n-1||G((q+1.5)/n)) D.box(0.14,1.25,0.14,x1,y1-0.1,z1,DARKWOOD,[0,a,0]);
      for(const h of [0.5,1.0]) D.geo(new THREE.BoxGeometry(0.06,0.12,l+0.14),WOOD,(x0+x1)/2,(y0+y1)/2+h,(z0+z1)/2,[-tilt,a,0]);
      const st={x:(x0+x1)/2,z:(z0+z1)/2,solid:{boxes:[[Math.min(x0,x1)-0.1,Math.min(y0,y1),Math.min(z0,z1)-0.1,Math.max(x0,x1)+0.1,Math.max(y0,y1)+1.15,Math.max(z0,z1)+0.1]],key:'fencerail'+STATICS.length,mat:'wood',deco:1}}; STATICS.push(st); D.claim(st); D.end(); } };

  // ---- campsites: a clearing in the trees with two tents round a fire
  { let made=0; for(let tr=0;tr<900&&made<7;tr++){ const x=S[0]+(r()*2-1)*(MAP_R-80), z=S[2]+(r()*2-1)*(MAP_R-80); if(!open(x,z,11)) continue; if(treesNear(x,z,22)<6) continue; // (only out in the woods)
      let ok=true; for(let k=0;k<12&&ok;k++){ const a=k/12*2*PI, px=x+Math.cos(a)*7, pz=z+Math.sin(a)*7; if(Math.abs(H(px,pz)-H(x,z))>1.1||wet(px,pz,1)) ok=false; } if(!ok) continue;
      clearProps(x,z,9.5); placed.push([x,z,14]); made++; DECOR.camps.push([x,z]); const y=Hm(x,z,0.7), a0=r()*2*PI;
      // the fire ring: stones, crossed logs, embers
      D.obj('brick',220); for(let k=0;k<10;k++){ const a=k/10*2*PI, sx=x+Math.cos(a)*0.78, sz=z+Math.sin(a)*0.78; D.sph(0.16+r()*0.05,sx,H(sx,sz)+0.08,sz,STONE,[1.2,0.75,1]); }
      D.cyl(0.62,0.66,0.03,x,y,z,0x2c2622,16); for(let k=0;k<3;k++) D.geo(new THREE.CylinderGeometry(0.06,0.07,1.0,6),0x3a2a1c,x,y+0.14+k*0.03,z,[PI/2-0.25,a0+k*1.05,0]);
      D.sph(0.2,x,y+0.08,z,0xff7a2a,[1.4,0.45,1.4],true); D.sph(0.09,x+0.12,y+0.12,z-0.08,0xffc24a,null,true); D.solid(x-0.9,y,z-0.9,x+0.9,y+0.3,z+0.9); D.end();
      // two tents facing the fire, log seats between them
      const cols=[0xd8732e,0x3f7d4f,0x3b6aa8,0xc4b14a,0xa8443a], c1=cols[Math.floor(r()*cols.length)], c2=cols[Math.floor(r()*cols.length)];
      for(const [da,R,c] of [[0,4.4,c1],[2.2+r()*0.6,4.6,c2]]){ const a=a0+da, tx=x+Math.sin(a)*R, tz=z+Math.cos(a)*R; tent(tx,tz,a+PI,c); }
      for(const da of [1.1,4.0]){ const a=a0+da, lx=x+Math.sin(a)*2.3, lz=z+Math.cos(a)*2.3; log(lx,H(lx,lz)-0.06,lz,a+PI/2,1.9,0.2,BARK,true); }
      { const a=a0+5.1, cx=x+Math.sin(a)*2.6, cz=z+Math.cos(a)*2.6, cy=Hm(cx,cz,0.4); D.obj('metal',70); D.box(0.7,0.42,0.42,cx,cy,cz,0x2f6fb3,[0,a,0]); D.box(0.72,0.07,0.44,cx,cy+0.42,cz,0xf2f2ee,[0,a,0]); D.solid(cx-0.4,cy,cz-0.4,cx+0.4,cy+0.5,cz+0.4); D.end(); } // a cooler
      { const a=a0+3.2, px=x+Math.sin(a)*3.2, pz=z+Math.cos(a)*3.2, py=H(px,pz)-0.15; D.cyl(0.04,0.05,1.5,px,py,pz,DARKWOOD,6); D.box(0.16,0.22,0.16,px,py+1.5,pz,0x3a3a3a); D.box(0.1,0.12,0.1,px,py+1.55,pz,0xffe08a,null,true); } // a lantern on a stick
      { const a=a0+0.9+PI, cx=x+Math.sin(a)*5.6, cz=z+Math.cos(a)*5.6; DECOR.chests.push([cx,Hm(cx,cz,0.6)+0.02,cz,a+PI]); } } }

  // ---- power lines: wooden poles along the longest roads, three wires sagging between them
  { const roads=WORLD.roads.filter(rd=>!rd.street).map(rd=>({rd,n:rd.pts.length})).sort((A,B)=>B.n-A.n).slice(0,4);
    roads.forEach(({rd},ri)=>{ const p=rd.pts, n=p.length, side=ri%2?1:-1; let arc=0, next=20, prev=null;
      for(let q=1;q<n-1;q++){ arc+=Math.hypot(p[q][0]-p[q-1][0],p[q][1]-p[q-1][1]); if(arc<next) continue; next=arc+38;
        const a0=p[Math.max(0,q-3)], b0=p[Math.min(n-1,q+3)]; let tx=b0[0]-a0[0], tz=b0[1]-a0[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl;
        const x=S[0]+p[q][0]-tz*7.6*side, z=S[2]+p[q][1]+tx*7.6*side, y=H(x,z);
        const bad=(rd.deck&&rd.deck[q])||townAt(x,z,22)||wet(x,z,2)||roadDistAt(x,z)<6||slope(x,z)>0.55||staticNear(x,z,1.2);
        if(bad){ prev=null; continue; }
        clearProps(x,z,2.6,['tree','pine','rock']); const a=Math.atan2(tx,tz); const yb=Hm(x,z,0.2), po=D.obj('wood',240); D.cyl(0.13,0.16,9.2,x,yb-0.3,z,0x6b5a46,8); D.solid(x-0.18,yb-0.3,z-0.18,x+0.18,yb+8.9,z+0.18); DECOR.poles++; if(DECOR.poles===12) DECOR.pole=[x,z,a];
        D.box(2.5,0.14,0.14,x,y+8.3,z,0x5e4c3a,[0,a,0]); D.geo(new THREE.BoxGeometry(0.08,0.08,1.1),0x5e4c3a,...at(x,z,a+PI/2,0,0.45).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+7.95,0]),[0.75,a+PI/2,0]); // the cross-arm and its brace
        const ends=[-1.1,0,1.1].map(u=>{ const [ex,ez]=at(x,z,a+PI/2,0,u); const ey=y+(u===0?8.95:8.44); D.cyl(0.05,0.06,0.16,ex,ey,ez,0xd8dcd4,6); return [ex,ey+0.14,ez]; });
        if(prev&&Math.hypot(prev.x-x,prev.z-z)<52){ D.with(prev.po,po); for(let w=0;w<3;w++){ const A=prev.ends[w], B=ends[w], L=Math.hypot(B[0]-A[0],B[2]-A[2]), sag=0.012*L*L/10+0.6; let lp=A;
            for(let k=1;k<=10;k++){ const f=k/10, P=[A[0]+(B[0]-A[0])*f,A[1]+(B[1]-A[1])*f-sag*4*f*(1-f),A[2]+(B[2]-A[2])*f], dx=P[0]-lp[0], dy=P[1]-lp[1], dz=P[2]-lp[2], l=Math.hypot(dx,dy,dz);
              const g=new THREE.CylinderGeometry(0.022,0.022,l,4); g.translate(0,l/2,0); const qn=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),new THREE.Vector3(dx/l,dy/l,dz/l)); g.applyMatrix4(new THREE.Matrix4().makeRotationFromQuaternion(qn)); D.geo(g,0x222326,lp[0],lp[1],lp[2]); lp=P; } } }
        D.end(); prev={x,z,ends,po}; } }); }

  // ---- hay fields outside two farm towns: a rail fence round a mown field, round bales lying about
  { const farms=TOWNS.filter(t=>!t.kind&&/Bramble|Hollow|Willow/.test(t.name)).slice(0,2);
    for(const t of farms){ let done=false; for(let tr=0;tr<400&&!done;tr++){ const a=r()*2*PI, d=townRadAt(t,Math.cos(a),Math.sin(a))+24+r()*50, cx=t.x+Math.cos(a)*d, cz=t.z+Math.sin(a)*d, ya=r()*PI, W=30+r()*10, L=22+r()*8;
        const corners=[[-W/2,-L/2],[W/2,-L/2],[W/2,L/2],[-W/2,L/2]].map(([u,v])=>at(cx,cz,ya,u,v)); let ok=true;
        for(let u=-W/2;u<=W/2&&ok;u+=6) for(let v=-L/2;v<=L/2&&ok;v+=6){ const [px,pz]=at(cx,cz,ya,u,v); if(townAt(px,pz,6)||roadDistAt(px,pz)<7||wet(px,pz,2)||slope(px,pz)>0.24||!free(px,pz,2)||Math.hypot(px-S[0],pz-S[2])>MAP_R-40) ok=false; }
        if(!ok) continue; done=true; placed.push([cx,cz,Math.hypot(W,L)/2+4]); (DECOR.farms=DECOR.farms||[]).push([cx,cz,ya]);
        for(let u=-W/2-3;u<=W/2+3;u+=3) for(let v=-L/2-3;v<=L/2+3;v+=3){ const [px,pz]=at(cx,cz,ya,u,v); clearProps(px,pz,2.4,['tree','pine','rock']); }
        const toTown=Math.atan2(t.x-cx,t.z-cz); let gateSide=0, best=-2; for(let s=0;s<4;s++){ const A=corners[s], B=corners[(s+1)%4], mx=(A[0]+B[0])/2-cx, mz=(A[1]+B[1])/2-cz, dt=(mx*Math.sin(toTown)+mz*Math.cos(toTown))/Math.hypot(mx,mz); if(dt>best){ best=dt; gateSide=s; } }
        for(let s=0;s<4;s++){ const A=corners[s], B=corners[(s+1)%4]; fenceRun(A[0],A[1],B[0],B[1],s===gateSide?(f=>f>0.42&&f<0.58):null); }
        const nb=8+Math.floor(r()*6); for(let k=0;k<nb;k++){ const [bx,bz]=at(cx,cz,ya,(r()-0.5)*(W-6),(r()-0.5)*(L-6)); if(!free(bx,bz,1.2)) continue; placed.push([bx,bz,1.2]); bale(bx,bz,r()*PI,r()<0.3); }
        // a hay cart by the gate
        { const A=corners[gateSide], B=corners[(gateSide+1)%4], gx=(A[0]+B[0])/2, gz=(A[1]+B[1])/2, ox=(gx-cx), oz=(gz-cz), ol=Math.hypot(ox,oz), kx=gx-ox/ol*5+(B[0]-A[0])/Math.hypot(B[0]-A[0],B[1]-A[1])*4, kz=gz-oz/ol*5+(B[1]-A[1])/Math.hypot(B[0]-A[0],B[1]-A[1])*4, ky=Hm(kx,kz,1.4), ka=Math.atan2(B[0]-A[0],B[1]-A[1]); D.obj('wood',220);
          D.box(1.6,0.12,2.8,kx,ky+0.7,kz,WOOD,[0,ka,0]); for(const s of [-1,1]){ D.box(0.08,0.5,2.8,...at(kx,kz,ka,s*0.78,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,ky+0.82,0]),WOOD,[0,ka,0]); const [wx,wz]=at(kx,kz,ka,s*0.9,0); D.geo(new THREE.CylinderGeometry(0.55,0.55,0.1,14),DARKWOOD,wx,ky+0.55,wz,[0,ka,PI/2]); }
          D.geo(new THREE.BoxGeometry(0.08,0.08,1.6),WOOD,...at(kx,kz,ka,0,2.1).reduce((o,v,i)=>(o[i*2]=v,o),[0,ky+0.5,0]),[0.3,ka,0]); for(let k=0;k<3;k++){ const [hx,hz]=at(kx,kz,ka,(k-1)*0.5,0.2*(k%2)); D.sph(0.5,hx,ky+1.05,hz,0xdcbc66,[1,0.6,1.3]); }
          D.solid(kx-1.3,ky,kz-1.3,kx+1.3,ky+1.4,kz+1.3); D.end(); placed.push([kx,kz,2]); } } } }

  // ---- town streets: benches looking onto the street, a bin beside each, fire hydrants at the kerb
  const segD=(x,z,ax,az,bx,bz)=>{ const dx=bx-ax, dz=bz-az, L2=dx*dx+dz*dz||1e-6; let f=((x-ax)*dx+(z-az)*dz)/L2; f=f<0?0:f>1?1:f; return Math.hypot(x-ax-dx*f,z-az-dz*f); };
  const pathHit=(t,x,z,clr)=>t.houses.some(h=>{ const Dr=doorOf(h), X=h.side==='n'||h.side==='s', e=Math.sign((X?Dr.z:Dr.x)-h.sc)*(ROAD_HW+WALK_W-0.1); if(segD(x,z,Dr.x,Dr.z,X?Dr.x:h.sc+e,X?h.sc+e:Dr.z)<WALK_W/2+clr) return true;
    if(h.garage){ const f=garageFrame(h), m=f.p(2.5,0.02), e2=Math.sign((f.X?m[1]:m[0])-h.sc)*(ROAD_HW+0.05); if(segD(x,z,m[0],m[1],f.X?m[0]:h.sc+e2,f.X?h.sc+e2:m[1])<1.7+clr) return true; } return false; });
  for(const t of TOWNS){ if(t.kind||!t.segs) continue; const tr=seeded(t.seed+881); let benches=0, hyd=0;
    for(const Sg of t.segs){ if(Sg.hammer) continue; const L=Sg.b-Sg.a; for(let s=Sg.a+9;s<Sg.b-9;s+=7+tr()*9){
        const sd=tr()<0.5?-1:1, X=Sg.X;
        if(hyd<5&&tr()<0.35){ const ac=Sg.c+sd*(ROAD_HW+0.45), x=X?s:ac, z=X?ac:s; if(!(t.junc||[]).some(J=>Math.hypot(J[0]-x,J[1]-z)<6)&&!staticNear(x,z,1.2)&&!pathHit(t,x,z,0.5)){ const y=t.h+0.05; D.obj('metal',160); D.cyl(0.13,0.15,0.62,x,y,z,0xc4262b,10); D.sph(0.14,x,y+0.62,z,0xc4262b,[1,0.8,1]); D.tube(0.06,0.42,x,y+0.42,z,0xc4262b,[0,0,PI/2],8); D.tube(0.06,0.42,x,y+0.42,z,0xc4262b,[PI/2,0,0],8); D.solid(x-0.22,y,z-0.22,x+0.22,y+0.8,z+0.22); D.end(); hyd++; } continue; }
        if(benches>=6||tr()<0.45) continue;
        const ac=Sg.c+sd*(ROAD_HW+WALK_W+0.75), x=X?s:ac, z=X?ac:s; if((t.junc||[]).some(J=>Math.hypot(J[0]-x,J[1]-z)<9)||staticNear(x,z,1.6)||pathHit(t,x,z,1.3)||propsNear(x,z,[],1).some(p=>!p.gone&&Math.hypot(p.x-x,p.z-z)<2.4)) continue;
        const y=t.h+0.02, a=X?(sd>0?PI:0):(sd>0?-PI/2:PI/2); D.obj('wood',110); // facing the street
        D.box(1.8,0.07,0.45,x,y+0.45,z,WOOD,[0,a,0]); D.box(1.8,0.38,0.06,...at(x,z,a,0,-0.24).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.55,0]),WOOD,[0,a+0.0,0]);
        for(const u of [-0.75,0.75]){ const [lx,lz]=at(x,z,a,u,0); D.box(0.07,0.45,0.42,lx,y,lz,0x2b3036,[0,a,0]); }
        { const hx=Math.abs(Math.cos(a))*0.95+Math.abs(Math.sin(a))*0.32, hz=Math.abs(Math.sin(a))*0.95+Math.abs(Math.cos(a))*0.32; D.solid(x-hx,y,z-hz,x+hx,y+0.6,z+hz); } D.end(); benches++; if(!DECOR.bench) DECOR.bench=[x,z,a];
        { const [bx,bz]=at(x,z,a,1.45,0); D.obj('metal',80); D.cyl(0.26,0.22,0.8,bx,y,bz,0x3f5a46,12); D.cyl(0.28,0.28,0.06,bx,y+0.8,bz,0x2e4234,12); D.solid(bx-0.3,y,bz-0.3,bx+0.3,y+0.86,bz+0.3); D.end(); } } } }

  // ---- the beach at Pebble Point: a wooden dock out into the sea, a rowboat tied at the end, two pulled up on the sand
  const boat=(x,y,z,a,c,tilt,kp)=>{ D.obj('wood',200); const hull=new THREE.SphereGeometry(1,14,8,0,2*PI,PI/2,PI/2); hull.scale(0.78,0.5,1.95); D.geo(hull,c,x,y+0.5,z,[tilt||0,a,0]);
    const inner=new THREE.SphereGeometry(1,14,8,0,2*PI,PI/2,PI/2); inner.scale(-0.7,0.44,1.86); D.geo(inner,0x8a6440,x,y+0.52,z,[tilt||0,a,0]);
    for(const v of [-0.55,0.45]){ const [sx,sz]=at(x,z,a,0,v); D.box(1.3,0.06,0.28,sx,y+0.3,sz,0x9a7650,[tilt||0,a,0]); }
    for(const s of [-1,1]){ const [ox,oz]=at(x,z,a,s*0.35,0.1); D.geo(new THREE.CylinderGeometry(0.03,0.03,2.2,5),0xb08a5a,ox,y+0.42,oz,[PI/2-0.08,a+s*0.12,0]); }
    D.solid(x-1,y,z-1,x+1,y+0.75,z+1,kp); D.end(); };
  { const sea=WGEN.sea&&WGEN.sea(), t=TOWNS[0]; if(sea&&t) for(const off of [32,-32,48,-48,64,-64]){ const bx0=t.x-sea.nz*off, bz0=t.z+sea.nx*off; let s=20; while(s<300&&H(bx0+sea.nx*s,bz0+sea.nz*s)>sea.Y+0.35) s+=1;
      if(s<300){ const a=Math.atan2(sea.nx,sea.nz), x0=bx0+sea.nx*(s-7), z0=bz0+sea.nz*(s-7), len=24, dy=sea.Y+1.05; let ok=!staticNear(x0,z0,3)&&!staticNear(x0+sea.nx*12,z0+sea.nz*12,3)&&!townAt(x0,z0,-30)&&roadDistAt(x0,z0)>6;
        if(ok){ clearProps(x0,z0,5); for(let k=0;k<=len;k+=0.5){ const [px,pz]=at(x0,z0,a,0,k); clearProps(px,pz,2.4,['rock','tree','pine']); }
          const deckY=k=>{ const [px,pz]=at(x0,z0,a,0,k); return Math.max(dy,H(px,pz)+0.25); }; D.obj('wood',700);
          for(let k=0;k<len;k+=0.42){ const [px,pz]=at(x0,z0,a,0,k+0.21), y=deckY(k+0.21); D.box(2.6,0.09,0.36,px,y-0.09,pz,(Math.floor(k/0.42)%3?0x9a7650:0x8d6c48),[0,a,0]); }
          for(let k=1;k<len;k+=3){ for(const u of [-1.2,1.2]){ const [px,pz]=at(x0,z0,a,u,k), gy=H(px,pz), y=deckY(k); if(y-gy>0.3) D.cyl(0.12,0.12,y-gy+0.6,px,gy-0.5,pz,0x6b5038,8); } }
          for(const u of [-1.25,1.25]) for(let k=6;k<len;k+=2.5){ const [px,pz]=at(x0,z0,a,u,k), y=deckY(k); D.cyl(0.05,0.05,0.9,px,y,pz,0x6b5038,6); }
          for(const u of [-1.25,1.25]){ const [mx,mz]=at(x0,z0,a,u,(6+len)/2); D.geo(new THREE.BoxGeometry(0.07,0.07,len-6),0x7a5a3c,mx,deckY(len*0.6)+0.88,mz,[0,a,0]); }
          for(let k=0;k<len;k+=2){ const [px,pz]=at(x0,z0,a,0,k+1), y=deckY(k+1); const hx=Math.abs(Math.sin(a))*1+Math.abs(Math.cos(a))*1.3, hz=Math.abs(Math.cos(a))*1+Math.abs(Math.sin(a))*1.3; const st={x:px,z:pz,solid:{boxes:[[px-hx,y-0.3,pz-hz,px+hx,y,pz+hz]],key:'dock'+STATICS.length,mat:'wood',deco:1}}; STATICS.push(st); D.claim(st); } D.end();
          { const [bx,bz]=at(x0,z0,a,2.6,len-3); boat(bx,sea.Y-0.38,bz,a+0.1,0xe8e4da,0,'moored'); } // (afloat, tied up)
          for(const [u,v,c] of [[-6,-3,0xc0473a]]){ const [bx,bz]=at(x0,z0,a,u,v); if(!wet(bx,bz,0)||H(bx,bz)>sea.Y){ boat(bx,Hm(bx,bz,1.1)-0.06,bz,a+PI+(r()-0.5)*0.8,c,0.06); placed.push([bx,bz,3]); } }
          placed.push([x0,z0,8]); DECOR.dock=[x0,z0,a]; break; } } } }
  // and a few boats pulled up on the river banks
  if(WORLD.rivers) { let n=0; for(let tr=0;tr<400&&n<2;tr++){ const rv=WORLD.rivers[Math.floor(r()*WORLD.rivers.length)], p=rv.pts[Math.floor(r()*rv.pts.length)]; if(!p) continue;
      const q=rv.pts[Math.min(rv.pts.length-1,rv.pts.indexOf(p)+3)], tx=q[0]-p[0], tz=q[1]-p[1], tl=Math.hypot(tx,tz)||1, sd=r()<0.5?-1:1, off=(p[3]||4)+2.6, x=S[0]+p[0]-tz/tl*off*sd, z=S[2]+p[1]+tx/tl*off*sd;
      if(townAt(x,z,10)||roadDistAt(x,z)<8||slope(x,z)>0.25||shoreAt(x,z)&&waterAt(x,z)>H(x,z)||!free(x,z,3)||nearRiver(x,z,0.4)) continue; clearProps(x,z,3);
      boat(x,Hm(x,z,1.1)-0.05,z,Math.atan2(tx,tz)+(r()-0.5)*0.6,[0xc0473a,0x3f7d5f,0x3b6aa8,0xe8e4da][n%4],0.08); placed.push([x,z,3]); n++; if(!DECOR.rboat) DECOR.rboat=[x,z]; } }

  // ---- out in the woods: fallen logs and stumps
  { let logs=0, stumps=0; for(let tr=0;tr<3000&&(logs<40||stumps<60);tr++){ const x=S[0]+(r()*2-1)*(MAP_R-60), z=S[2]+(r()*2-1)*(MAP_R-60); if(!open(x,z,2.5)||treesNear(x,z,14)<3) continue;
      if(logs<40&&r()<0.5){ const a=r()*PI, len=4+r()*4, rad=0.28+r()*0.14; let ok=true; for(const s of [-1,1]){ const [ex,ez]=at(x,z,a,0,s*len/2); if(Math.abs(H(ex,ez)-H(x,z))>0.7||!open(ex,ez,1)) ok=false; } if(!ok) continue;
        clearProps(x,z,len/2+1,['rock']); { const [e1x,e1z]=at(x,z,a,0,len/2), [e2x,e2z]=at(x,z,a,0,-len/2), h1=H(e1x,e1z), h2=H(e2x,e2z), pt=Math.atan2(h1-h2,len); let dip=0; // tilted to follow the ground end to end, and let down onto its lowest point
          for(let k=-4;k<=4;k++){ const f=k/8, [sx,sz]=at(x,z,a,0,f*len); for(const w of [-rad*0.7,0,rad*0.7]){ const [qx,qz]=at(sx,sz,a,w,0); dip=Math.min(dip,H(qx,qz)-((h1+h2)/2+(h1-h2)*f)); } }
          log(x,(h1+h2)/2+dip-rad*0.22,z,a,len,rad,0x5e4630,true,pt); } { const [bx,bz]=at(x,z,a,0,len*0.15); D.geo(new THREE.CylinderGeometry(0.06,0.09,0.9,5),0x5e4630,bx,H(x,z)+rad*1.2,bz,[0.9,a+1.2,0]); } placed.push([x,z,len/2]); logs++; }
      else if(stumps<60){ const rad=0.3+r()*0.2, y=Hm(x,z,rad); D.obj('wood',90); D.cyl(rad*0.9,rad*1.15,0.45+r()*0.3,x,y-0.05,z,0x5e4630,9); D.solid(x-rad,y,z-rad,x+rad,y+0.5,z+rad); D.end(); placed.push([x,z,1]); stumps++; } } }

  // ---- picnic tables by the road, at the nicer stretches
  { let n=0; for(let tr=0;tr<600&&n<6;tr++){ const rd=WORLD.roads[Math.floor(r()*WORLD.roads.length)]; if(rd.street) continue; const q=6+Math.floor(r()*(rd.pts.length-12)), p=rd.pts[q], p2=rd.pts[q+2]; if(!p2) continue;
      const tx=p2[0]-p[0], tz=p2[1]-p[1], tl=Math.hypot(tx,tz)||1, sd=r()<0.5?-1:1, x=S[0]+p[0]-tz/tl*11*sd, z=S[2]+p[1]+tx/tl*11*sd; if(!open(x,z,3)) continue; clearProps(x,z,4);
      const y=Hm(x,z,1.2), a=Math.atan2(tx,tz); D.obj('wood',130); D.box(0.9,0.06,1.9,x,y+0.74,z,WOOD,[0,a,0]); for(const s of [-1,1]){ const [bx,bz]=at(x,z,a,s*0.78,0); D.box(0.3,0.05,1.9,bx,y+0.44,bz,WOOD,[0,a,0]); }
      for(const s of [-1,1]){ const [lx,lz]=at(x,z,a,0,s*0.7); D.box(1.9,0.06,0.08,lx,y+0.4,lz,DARKWOOD,[0,a,0]); D.geo(new THREE.BoxGeometry(0.07,0.95,0.07),DARKWOOD,...at(lx,lz,a,0.3,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.38,0]),[0,a,0.55]); D.geo(new THREE.BoxGeometry(0.07,0.95,0.07),DARKWOOD,...at(lx,lz,a,-0.3,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.38,0]),[0,a,-0.55]); }
      D.solid(x-1.2,y,z-1.2,x+1.2,y+0.8,z+1.2); D.end(); { const [bx,bz]=at(x,z,a,1.8,1.2); D.obj('metal',80); { const by=Hm(bx,bz,0.3); D.cyl(0.26,0.22,0.8,bx,by,bz,0x3f5a46,12); D.solid(bx-0.3,by,bz-0.3,bx+0.3,by+0.85,bz+0.3); D.end(); } } placed.push([x,z,4]); n++; } }

  // ---- round the points of interest: odds and ends to suit each one, out at the edges where nothing else stands
  for(const t of TOWNS){ if(!t.kind) continue; const pr=seeded(t.seed+3131); let n=0; const occ=new Set(); for(const bl of planPOI(t)) for(const p of bl.pieces) occ.add(p.i+','+p.j); // (the buildings aren't up yet: go by their plan)
    const built=(x,z)=>{ const ci=Math.floor(x/CELL), cj=Math.floor(z/CELL); for(let u=-1;u<=1;u++) for(let v=-1;v<=1;v++) if(occ.has((ci+u)+','+(cj+v))) return true; return false; };
    for(let tr=0;tr<260&&n<16;tr++){ const a=pr()*2*PI, d=t.R*(0.55+pr()*0.5), x=t.x+Math.cos(a)*d, z=t.z+Math.sin(a)*d, y=Hm(x,z,0.9);
      if(roadDistAt(x,z)<5.5||staticNear(x,z,2.2)||built(x,z)||wet(x,z,1)||slope(x,z)>0.3||!free(x,z,1.6)) continue;
      if(propsNear(x,z,[],1).some(p=>!p.gone&&Math.hypot(p.x-x,p.z-z)<2.5)) continue; placed.push([x,z,1.8]); n++; const ya=pr()*PI;
      if(t.kind==='factory'){ if(pr()<0.5){ drum(x,y,z,[0x2f5f9a,0xa83a2a,0x3d7a3a][Math.floor(pr()*3)]); if(pr()<0.6) drum(x+0.75,y,z+0.1,0x2f5f9a); } else { D.box(1.2,0.14,1.0,x,y,z,0x9c7a4c,[0,ya,0]); crate(x,y+0.14,z,0.8,ya); D.solid(x-0.7,y,z-0.7,x+0.7,y+0.14,z+0.7); } }
      else if(t.kind==='castle'){ const k=pr(); if(k<0.4) bale(x,z,ya,pr()<0.4); else if(k<0.75){ D.scyl(0.36,0.9,x,y,z,0x7a5230,12); D.cyl(0.38,0.38,0.05,x,y+0.25,z,0x3a3a3a,12); D.cyl(0.38,0.38,0.05,x,y+0.65,z,0x3a3a3a,12); } // a barrel
        else { D.cyl(0.06,0.06,4.2,x,y,z,DARKWOOD,6); D.box(0.9,1.5,0.04,x+0.48,y+2.5,z,[0x8a2a2a,0x2a4a8a,0x2f6a3a][Math.floor(pr()*3)]); D.solid(x-0.15,y,z-0.15,x+0.15,y+4.2,z+0.15); } } // a banner
      else if(t.kind==='labs'){ if(pr()<0.45){ crate(x,y,z,0.9,ya,0x8a8f96); D.box(0.92,0.12,0.06,...at(x,z,ya,0,0.46).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.4,0]),0xf2c418,[0,ya,0]); } else drum(x,y,z,0xe0b020); }
      else { if(pr()<0.6){ for(let k=0;k<3;k++) log(...at(x,z,ya,(k-1)*0.62,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,y,0]),ya,3.6,0.3,BARK,k===1); log(...at(x,z,ya,-0.31,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.52,0]),ya,3.6,0.3,BARK); log(...at(x,z,ya,0.31,0).reduce((o,v,i)=>(o[i*2]=v,o),[0,y+0.52,0]),ya,3.6,0.3,BARK);
          const [hx,hz]=[Math.abs(Math.sin(ya))*1.9+Math.abs(Math.cos(ya))*1,Math.abs(Math.cos(ya))*1.9+Math.abs(Math.sin(ya))*1]; D.solid(x-hx,y,z-hz,x+hx,y+1.1,z+hz); }
        else { D.cyl(0.42,0.5,0.55,x,y,z,0x5e4630,10); D.box(0.12,0.75,0.12,x,y+0.55,z,0x8a8a8a,[0.3,ya,0]); D.solid(x-0.5,y,z-0.5,x+0.5,y+0.6,z+0.5); } } } } // log piles; a stump with an axe

  const meshes=D.flush(); DECOR.items=meshes.length; DECOR.s1=STATICS.length; return meshes; }

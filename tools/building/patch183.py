# patch183: the island stands up out of the ocean. The ring of mountains round the edge is gone: the land rolls out to a
# rim of low hills and ends at a cliff (a wavy outline, rock faces with ledges) dropping some 70 m to open sea all
# round; the mountains are now far off across the water, a hazy range on the horizon. The bay by Pebble Point is a
# lagoon up on the island, and where it meets the edge it pours off the cliff in a waterfall, with spray and foam where
# it lands. You can walk (or drive, or sail) right up to the edge, but not over it.
rep("""      rid=ridged(wu*0.0016,wv*0.0016,6,21,0.44); h+=oR*(50+(170+230*oR)*rid); }""",
    """      rid=ridged(wu*0.0016,wv*0.0016,6,21,0.44); h+=Math.min(1,oR*3.2)*(6+18*rid); } // (just a rim of low hills now: the island ends at a cliff)""")
rep("""return h0+((g0+(bed-g0)*b)-h0)*w; } } } }""","""return cliff(u,v,d,h0+((g0+(bed-g0)*b)-h0)*w); } } } }""")
rep("""    return h<0?0:h; }
  // the sea:""","""    return cliff(u,v,d,h<0?0:h); }
  // the island's edge (a wavy line a little past the map's rim), the cliff down to the sea, and the far mountains
  const OCEAN_Y=-70, edgeR=(u,v)=>MAP_R+3+9*fbm(u*0.0045+3.7,v*0.0045-1.9,2,301)+3*fbm(u*0.017,v*0.017,2,302);
  function cliff(u,v,d,h){ if(d<MAP_R-30) return h; const er=edgeR(u,v), ec=er-(SEA?9*Math.max(0,Math.min(1,(SEA.Y-0.2-h)/0.6)):0); if(d<=ec) return h; // (under the lagoon the face is cut back under the water's lip, so the falls hang clear of the rock)
    const k=sstep(ec,ec+5,d), floor=OCEAN_Y-22-30*sstep(er+40,er+500,d); let y=h+(floor-h)*k;
    if(k>0&&k<1) y=Math.min(h-0.3*k,y+2.2*fbm(u*0.07,v*0.07,2,303)*Math.sin(k*Math.PI)); // a sheer face, a little rough
    const fm=sstep(2300,2950,d+260*fbm(u*0.0007,v*0.0007,2,304)); if(fm>0) y+=fm*(140+520*ridged(u*0.0011+7,v*0.0011-3,6,305,0.46)); // the mountains, far across the water
    return y; }
  // the sea:""")
rep("""  const seaW=(u,v)=>{ if(!SEA) return 0;""","""  const seaW=(u,v)=>{ if(!SEA) return 0; if(Math.sqrt(u*u+v*v)>edgeR(u,v)-1.5) return 0;""")
rep("""  return {genH,MASSIFS,setSea:s=>{ SEA=s; },""","""  return {genH,MASSIFS,edgeR,OCEAN_Y,setSea:s=>{ SEA=s; },""")
# the far terrain: further out (to the mountains), finer close to the island (the foot of the cliffs)
rep("""  const E=2400, S=16, xs=[-E,-WHALF,WHALF,E], tiles=[];
  for(let b=0;b<3;b++) for(let a=0;a<3;a++){ if(a===1&&b===1) continue; const u0=xs[a], u1=xs[a+1], v0=xs[b], v1=xs[b+1];""",
    """  const E=3616, xs=[-E,-1184,-WHALF,WHALF,1184,E], tiles=[]; // (every edge a whole number of steps)
  for(let b=0;b<5;b++) for(let a=0;a<5;a++){ if(a===2&&b===2) continue; const u0=xs[a], u1=xs[a+1], v0=xs[b], v1=xs[b+1], S=(a>=1&&a<=3&&b>=1&&b<=3)?8:32;""")
rep("""    if(u1-u0>=v1-v0){ const um=u0+Math.round((u1-u0)/2/S)*S; tiles.push([u0,um,v0,v1],[um,u1,v0,v1]); } else { const vm=v0+Math.round((v1-v0)/2/S)*S; tiles.push([u0,u1,v0,vm],[u0,u1,vm,v1]); } }
  for(const [u0,u1,v0,v1] of tiles){""","""    tiles.push([u0,u1,v0,v1,S]); }
  for(const [u0,u1,v0,v1,S] of tiles){""")
rep("""const camera=new THREE.PerspectiveCamera(settings.fov, innerWidth/innerHeight, 0.08, 3200);""","""const camera=new THREE.PerspectiveCamera(settings.fov, innerWidth/innerHeight, 0.08, 5600); // (far enough for the mountains across the sea)""")
# the ocean, and the waterfall
rep("""/* ---------- water ----------""","""/* ---------- the ocean round the island, and the waterfall off the lagoon ---------- */
const OCEAN={};
(function buildOcean(){ const Y=WGEN.OCEAN_Y, C=SPAWN;
  const wt=(()=>{ const c=document.createElement('canvas'); c.width=c.height=256; const g=c.getContext('2d'), R=seeded(7070); g.fillStyle='#1d5f8c'; g.fillRect(0,0,256,256);
    for(let i=0;i<900;i++){ const x=R()*256, y=R()*256, l=6+R()*22; g.strokeStyle=R()<0.5?'rgba(255,255,255,.10)':'rgba(10,40,70,.22)'; g.lineWidth=1+R()*1.5; g.beginPath(); g.moveTo(x,y); g.quadraticCurveTo(x+l/2,y-2-R()*2,x+l,y); g.stroke(); }
    const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.repeat.set(220,220); t.anisotropy=8; return t; })();
  const sea=new THREE.Mesh(new THREE.PlaneGeometry(13000,13000,1,1).rotateX(-Math.PI/2),new THREE.MeshPhongMaterial({color:0x8fb8d4,map:wt,specular:0x9cc4e0,shininess:70}));
  sea.position.set(C[0],Y,C[2]); sea.receiveShadow=false; sea.renderOrder=-2; scene.add(sea); OCEAN.sea=sea; OCEAN.tex=wt;
  // the waterfall: wherever the lagoon's water reaches the island's edge, a curtain of falling water down to the sea
  const S=WGEN.sea(); if(!S) return; const segs=[]; let cur=null; const a0=Math.atan2(S.nz,S.nx);
  for(let a=a0-1.0;a<=a0+1.0;a+=0.0025){ const ca=Math.cos(a), sa=Math.sin(a), er=WGEN.edgeR(ca*820,sa*820), r=er-2.2, c=worldCell(C[0]+ca*r,C[2]+sa*r), wet=c>=0&&WORLD.WS[c]>-999;
    if(wet){ if(!cur){ cur=[]; segs.push(cur); } cur.push([ca,sa,WGEN.edgeR(ca*er,sa*er)]); } else cur=null; }
  const streak=(()=>{ const c=document.createElement('canvas'); c.width=128; c.height=512; const g=c.getContext('2d'), R=seeded(9090); g.clearRect(0,0,128,512);
    g.fillStyle='rgba(200,225,240,0.32)'; g.fillRect(0,0,128,512); // a thin sheet everywhere, streaks on top (wrapping both ways: no seams)
    for(let i=0;i<340;i++){ const x=R()*128, w=1+R()*3.5, y=R()*512, l=80+R()*300, a=0.2+R()*0.6; for(const dx of [0,-128,128]) for(const dy of [0,-512]){ const gr=g.createLinearGradient(0,y+dy,0,y+dy+l); gr.addColorStop(0,'rgba(255,255,255,0)'); gr.addColorStop(0.5,`rgba(240,249,255,${a})`); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(x+dx,y+dy,w,l); } }
    const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; return t; })();
  const mist=(()=>{ const c=document.createElement('canvas'); c.width=c.height=64; const g=c.getContext('2d'), gr=g.createRadialGradient(32,32,0,32,32,32); gr.addColorStop(0,'rgba(255,255,255,.9)'); gr.addColorStop(0.5,'rgba(255,255,255,.35)'); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(0,0,64,64); return new THREE.CanvasTexture(c); })();
  OCEAN.falls=[]; OCEAN.mists=[];
  for(const sg of segs){ if(sg.length<6) continue; const pos=[], uv=[], col=[], idx=[], ROWS=22, top=S.Y, H_=top-Y; let arc=0;
    sg.forEach((p,i)=>{ if(i) arc+=Math.hypot((p[0]*p[2]-sg[i-1][0]*sg[i-1][2]),(p[1]*p[2]-sg[i-1][1]*sg[i-1][2]));
      const side=Math.min(1,Math.min(i,sg.length-1-i)/4); // thinner at its two ends
      for(let r=0;r<=ROWS;r++){ const t=r/ROWS, out=10*Math.sqrt(t)*(0.6+0.4*side)+t*5, R=p[2]-1.6+out, y=top+0.05-t*(H_+0.5);
        pos.push(C[0]+p[0]*R,y,C[2]+p[1]*R); uv.push(arc/9,t*H_/36); col.push(side,side,side); } });
    for(let i=0;i<sg.length-1;i++) for(let r=0;r<ROWS;r++){ const a=i*(ROWS+1)+r, b=a+ROWS+1; idx.push(a,b,a+1,b,b+1,a+1); }
    const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2)); g.setAttribute('color',new THREE.Float32BufferAttribute(col,3)); g.setIndex(idx); g.computeVertexNormals();
    for(const [sp,op,tint,ox] of [[1,0.78,0xcfe6f6,0],[1.7,0.5,0xffffff,0.37]]){ const tex=streak.clone(); tex.needsUpdate=true; tex.repeat.set(ox?1.3:1,1); tex.offset.x=ox;
      const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({map:tex,color:tint,transparent:true,opacity:op,depthWrite:false,side:THREE.DoubleSide,fog:true})); m.renderOrder=3; m.userData.sp=sp; scene.add(m); OCEAN.falls.push(m); }
    { const under=new THREE.Mesh(g,new THREE.MeshLambertMaterial({color:0x7fb2cf,emissive:0x2a4a5e,transparent:true,opacity:0.86,depthWrite:false,side:THREE.DoubleSide})); under.renderOrder=2; scene.add(under); }
    // spray where it lands, and white water spreading on the sea
    for(let i=0;i<sg.length;i+=3){ const p=sg[i], R=p[2]+12; for(let k=0;k<2;k++){ const s=new THREE.Sprite(new THREE.SpriteMaterial({map:mist,color:0xffffff,transparent:true,opacity:0.5,depthWrite:false}));
        const sc=10+Math.random()*12; s.scale.set(sc,sc,1); s.position.set(C[0]+p[0]*(R+Math.random()*6),Y+3+Math.random()*8+k*7,C[2]+p[1]*(R+Math.random()*6)); s.userData={y0:s.position.y,ph:Math.random()*6.28,sc}; scene.add(s); OCEAN.mists.push(s); } }
    { const fg=new THREE.CircleGeometry(1,24).rotateX(-Math.PI/2); for(let i=0;i<sg.length;i+=6){ const p=sg[i], R=p[2]+14, f=new THREE.Mesh(fg,new THREE.MeshBasicMaterial({map:mist,color:0xf2fbff,transparent:true,opacity:0.7,depthWrite:false}));
        f.scale.setScalar(16+Math.random()*10); f.position.set(C[0]+p[0]*R,Y+0.15,C[2]+p[1]*R); f.renderOrder=1; scene.add(f); } } }
})();
function stepOcean(dt){ const t=performance.now()/1000; if(OCEAN.tex){ OCEAN.tex.offset.x=t*0.004; OCEAN.tex.offset.y=t*0.0025; }
  if(OCEAN.falls) for(const m of OCEAN.falls) m.material.map.offset.y=t*0.55*m.userData.sp;
  if(OCEAN.mists) for(const s of OCEAN.mists){ const u=s.userData; s.position.y=u.y0+Math.sin(t*0.6+u.ph)*1.5; const k=1+0.12*Math.sin(t*0.9+u.ph); s.scale.set(u.sc*k,u.sc*k,1); s.material.opacity=0.38+0.14*Math.sin(t*1.1+u.ph); } }
// nobody goes over the edge: walking, gliding, driving or sailing, you stop at the cliff top
function keepOnIsland(E){ const u=E.pos.x-SPAWN[0], v=E.pos.z-SPAWN[2], d=Math.hypot(u,v); if(d<MAP_R-40) return; const er=WGEN.edgeR(u,v)-1.2; if(d<=er) return;
  const nx=u/d, nz=v/d; E.pos.x=SPAWN[0]+nx*er; E.pos.z=SPAWN[2]+nz*er; if(E.vel){ const vn=E.vel.x*nx+E.vel.z*nz; if(vn>0){ E.vel.x-=vn*nx; E.vel.z-=vn*nz; } } }
function keepKartOnIsland(k){ const u=k.x-SPAWN[0], v=k.z-SPAWN[2], d=Math.hypot(u,v); if(d<MAP_R-40) return; const er=WGEN.edgeR(u,v)-(k.boat?3:2); if(d<=er) return;
  const nx=u/d, nz=v/d; k.x=SPAWN[0]+nx*er; k.z=SPAWN[2]+nz*er; const vn=k.vx*nx+k.vz*nz; if(vn>0){ k.vx-=vn*nx*1.6; k.vz-=vn*nz*1.6; } }
/* ---------- water ----------""")
rep("""function moveBody(E,fw,st,jump,dt){ E.swim=!E.kart&&!E.sky&&swimSurface(E.pos)!==null; if(E.kart){ if(E.kart.seat===0) E.kart.k.inp={fw,st,hb:!!jump}; return; } if(E.sky){ skyMove(E,fw,st,jump,dt); return; } moveBody0(E,fw,st,jump,dt); }""",
    """function moveBody(E,fw,st,jump,dt){ E.swim=!E.kart&&!E.sky&&swimSurface(E.pos)!==null; if(E.kart){ if(E.kart.seat===0) E.kart.k.inp={fw,st,hb:!!jump}; return; } if(E.sky){ skyMove(E,fw,st,jump,dt); keepOnIsland(E); return; } moveBody0(E,fw,st,jump,dt); keepOnIsland(E); }""")
rep("""function stepKarts(dt){ if(!karts) return; const me=ME();""","""function stepKarts(dt){ if(!karts) return; const me=ME(); for(const k of karts) if(!k.dead) keepKartOnIsland(k);""")
rep("""  if(mapOpen){ stepMapView(lastDt); drawBigMap(); }""","""  if(mapOpen){ stepMapView(lastDt); drawBigMap(); }
  stepOcean(lastDt);""")
rep("""  g.fillStyle='#3d6b3a'; g.fillRect(0,0,S,S);
  const ox=P.pos.x, oz=P.pos.z,""","""  g.fillStyle='#1d5f8c'; g.fillRect(0,0,S,S);
  const ox=P.pos.x, oz=P.pos.z,""")
# the lagoon reaches right to the edge: recompute the ground on the rim ring too (seaW is 0 past the edge, which left the
# old land height there as a thin wall of spikes), and give the mouth a shallow lip so the water spills over it
rep("""if(o.gen.seaW(u,v)>0) H0[j*N+i]=genH(u,v); } } }""","""if(o.gen.seaW(u,v)>0||u*u+v*v>(MAP_R-45)*(MAP_R-45)) H0[j*N+i]=genH(u,v); } } }""")
rep("""bed=c<0?SEA.Y+0.25-c*0.05:SEA.Y-0.15-Math.min(9,c*0.05), b=""","""bed0=c<0?SEA.Y+0.25-c*0.05:SEA.Y-0.15-Math.min(9,c*0.05), lip=d>MAP_R-60?sstep(edgeR(u,v)-45,edgeR(u,v)-6,d):0, bed=bed0+(Math.max(bed0,Math.min(bed0+6,SEA.Y-1.1))-bed0)*lip, b=""")
# the lagoon's water sheet stops at the island's edge (it used to run out to the horizon at the lagoon's level): every
# vertex past the edge is pulled in onto it, and the far sheets go (the ocean down below is its own plane now)
rep("""const al=A0+a*ST, lat=-LW+b*ST, u=S.nx*al+px*lat, v=S.nz*al+pz*lat; pos.push(""","""const al=A0+a*ST, lat=-LW+b*ST; let u=S.nx*al+px*lat, v=S.nz*al+pz*lat; for(let it=0;it<4;it++){ const d=Math.hypot(u,v), e=WGEN.edgeR(u,v)-1.6; if(d>e){ u*=e/d; v*=e/d; } else break; } pos.push(""")
rep("""for(const gg of [g,g2]){ const m=new THREE.Mesh(gg,WATER.mat);""","""for(const gg of [g]){ const m=new THREE.Mesh(gg,WATER.mat);""")

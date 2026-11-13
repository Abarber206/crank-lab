/* ---------- trees ----------
   Broadleaf trees in the stylised alder look: a twisting trunk that splits into curving limbs, and a wide crown made of
   leafy clumps, each a cloud of cut-out leaf cards lit as one soft shape (bright yellow-green on top, deep green
   underneath and inside). Pines are stacked tiers of solid boughs with a jagged, drooping hem round a tapering trunk. Trunk, limbs and leaves
   share one texture atlas and one material, so a whole tree is one draw. Further away each tree becomes a picture of
   itself (rendered once at start-up) on crossed cards, with a top-down picture for when you look down from the sky. */
const TREE_ATLAS=(()=>{ const S=1024, c=document.createElement('canvas'); c.width=c.height=S; const g=c.getContext('2d');
  const rnd=(a,b)=>a+Math.random()*(b-a);
  // leaves (top left): a round cluster of many small leaves, dense in the middle, ragged at the edge; light and neutral so vertex colour tints it
  { const cx=256, cy=256; const leaf=(x,y,a,l,w,col,edge)=>{ g.save(); g.translate(x,y); g.rotate(a); g.beginPath(); g.moveTo(-l/2,0); g.quadraticCurveTo(-l*0.05,-w,l/2,0); g.quadraticCurveTo(-l*0.05,w,-l/2,0); g.closePath(); g.fillStyle=col; g.fill();
      g.strokeStyle=edge; g.lineWidth=0.9; g.stroke(); g.restore(); };
    const pal=['#9cc65c','#abd06a','#b9da78','#c7e288','#d4ea98','#e2f2b0'];
    for(let pass=0;pass<4;pass++) for(let k=0;k<520;k++){ const a=Math.random()*Math.PI*2, rr=Math.pow(Math.random(),pass<2?0.55:0.8)*(222-pass*26), x=cx+Math.cos(a)*rr, y=cy+Math.sin(a)*rr*0.94;
      leaf(x,y,a+rnd(-1.1,1.1),rnd(17,26),rnd(6.5,9.5),pal[Math.min(5,Math.floor(Math.random()*3)+pass)],pass<2?'rgba(60,100,35,.6)':'rgba(80,125,45,.45)'); } }
  // pine needles (top right): solid, light and neutral (vertex colour greens it); short needle strokes running down the
  // region (down the slope of a tier) with soft darker grooves between the boughs
  { g.save(); g.translate(512,0); g.fillStyle='#bcd6a8'; g.fillRect(0,0,512,512);
    for(let k=0;k<26;k++){ const x=k*20+rnd(-4,4); const gr=g.createLinearGradient(x-9,0,x+9,0); gr.addColorStop(0,'rgba(60,90,50,0)'); gr.addColorStop(0.5,'rgba(60,90,50,.28)'); gr.addColorStop(1,'rgba(60,90,50,0)'); g.fillStyle=gr; g.fillRect(x-9,0,18,512); }
    for(let k=0;k<5200;k++){ const x=Math.random()*512, y=Math.random()*512, len=rnd(9,18), a=Math.PI/2+rnd(-0.55,0.55);
      g.strokeStyle=['#d6e8c4','#a8c890','#c4dcae','#90b47a','#e2f0d2','#9cc084'][Math.floor(Math.random()*6)]; g.lineWidth=rnd(1.2,2.2); g.beginPath(); g.moveTo(x,y); g.lineTo(x+Math.cos(a)*len,y+Math.sin(a)*len); g.stroke(); }
    g.restore(); }
  // bark (two strips across the bottom half): warm brown with long fissures and lighter ridges
  for(const [y0,base,dark,light] of [[512,'#8a5a3a','rgba(50,28,14,.55)','rgba(200,150,105,.35)'],[768,'#6e4a30','rgba(40,22,10,.55)','rgba(170,125,90,.3)']]){ g.fillStyle=base; g.fillRect(0,y0,S,256);
    for(let k=0;k<160;k++){ const x=Math.random()*S, w=rnd(2,6); g.fillStyle=Math.random()<0.6?dark:light; g.fillRect(x,y0,w,256); }
    for(let k=0;k<50;k++){ g.fillStyle='rgba(40,22,10,.45)'; g.beginPath(); g.ellipse(Math.random()*S,y0+Math.random()*256,rnd(3,7),rnd(6,12),0,0,7); g.fill(); } }
  const t=new THREE.CanvasTexture(c); t.anisotropy=MAXANI; t.generateMipmaps=true; t.minFilter=THREE.LinearMipmapLinearFilter; return t; })();
// atlas regions (u0,v0,u1,v1), inset so mipmaps don't bleed between them
const TA={leaf:[0.012,0.512,0.488,0.988],pine:[0.512,0.53,0.988,0.97],bark:[0,0.262,1,0.488],pbark:[0,0.012,1,0.238]};
// one material for every near tree: cut-out leaves; both faces of a leaf card lit alike (as one soft clump), a little breeze in the leaves
const TREE_U={time:{value:0}};
function treeMatPatch(sh){ sh.uniforms.tTime=TREE_U.time;
  sh.vertexShader='uniform float tTime;\n'+sh.vertexShader.replace('#include <begin_vertex>',`#include <begin_vertex>
  { float leafy=step(0.5,uv.y)*smoothstep(2.4,6.0,position.y);
    #ifdef USE_INSTANCING
      vec2 ph=instanceMatrix[3].xz;
    #else
      vec2 ph=modelMatrix[3].xz;
    #endif
    float w=sin(tTime*1.7+ph.x*0.13+ph.y*0.11+position.y*0.6)+0.5*sin(tTime*2.9+ph.x*0.07-position.x*1.3);
    transformed.x+=w*0.05*leafy; transformed.z+=cos(tTime*1.3+ph.y*0.12+position.z)*0.04*leafy; }`);
  sh.fragmentShader=sh.fragmentShader.replace('reflectedLight.indirectDiffuse += ( gl_FrontFacing ) ? vIndirectFront : vIndirectBack;','reflectedLight.indirectDiffuse += vIndirectFront;')
    .replace('reflectedLight.directDiffuse = ( gl_FrontFacing ) ? vLightFront : vLightBack;','reflectedLight.directDiffuse = vLightFront;'); }
const treeMat=new THREE.MeshLambertMaterial({map:TREE_ATLAS,vertexColors:true,alphaTest:0.42,side:THREE.DoubleSide,emissive:0x1a1a10}); treeMat.onBeforeCompile=treeMatPatch; // (a little light of its own: shaded limbs and inner leaves stay warm, not black)
const treeDepth=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking,map:TREE_ATLAS,alphaTest:0.42,side:THREE.DoubleSide});

// a geometry builder: quads and tubes with uv into an atlas region and a vertex colour each
function TreeGeo(){ const P=[],N=[],U=[],Cc=[],I=[]; let n=0;
  const B={
    vert(x,y,z,nx,ny,nz,u,v,c){ P.push(x,y,z); N.push(nx,ny,nz); U.push(u,v); Cc.push(c.r,c.g,c.b); return n++; },
    // a tube along points with radii; uv round it across the region, along it up the region
    tube(pts,rad,seg,R,col){ const T=new THREE.Vector3(), A=new THREE.Vector3(), Bv=new THREE.Vector3(), up=new THREE.Vector3(0,1,0), base=n, rows=pts.length;
      for(let k=0;k<rows;k++){ const p=pts[k], q=pts[Math.min(rows-1,k+1)], o=pts[Math.max(0,k-1)]; T.subVectors(q,o).normalize(); A.crossVectors(T,Math.abs(T.y)>0.95?new THREE.Vector3(1,0,0):up).normalize(); Bv.crossVectors(T,A).normalize();
        for(let s=0;s<=seg;s++){ const a=s/seg*Math.PI*2, ca=Math.cos(a), sa=Math.sin(a), nx=A.x*ca+Bv.x*sa, ny=A.y*ca+Bv.y*sa, nz=A.z*ca+Bv.z*sa, r=rad[k];
          B.vert(p.x+nx*r,p.y+ny*r,p.z+nz*r,nx,ny,nz,R[0]+(R[2]-R[0])*(s/seg),R[1]+(R[3]-R[1])*(k/(rows-1)),col(k/(rows-1))); } }
      for(let k=0;k<rows-1;k++) for(let s=0;s<seg;s++){ const a=base+k*(seg+1)+s, b=a+1, c=a+seg+1, d=c+1; I.push(a,c,b,b,c,d); } },
    // a card: centre, two half-extent axes, its region, the normal each corner gets (soft clump lighting) and a colour per corner
    card(c,ax,ay,R,nrm,cols){ const corners=[[-1,-1],[1,-1],[1,1],[-1,1]], b0=n;
      corners.forEach(([sx,sy],q)=>{ const x=c.x+ax.x*sx+ay.x*sy, y=c.y+ax.y*sx+ay.y*sy, z=c.z+ax.z*sx+ay.z*sy, nn=nrm(x,y,z); B.vert(x,y,z,nn.x,nn.y,nn.z,sx<0?R[0]:R[2],sy<0?R[1]:R[3],cols[q]); });
      I.push(b0,b0+1,b0+2,b0,b0+2,b0+3); },
    tri(a,b,c){ I.push(a,b,c); },
    done(){ const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(N,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(U,2)); g.setAttribute('color',new THREE.Float32BufferAttribute(Cc,3)); g.setIndex(I); g.computeBoundingSphere(); g.computeBoundingBox(); return g; } };
  return B; }

function broadleafGeo(v){ const q=seeded(31337+v*7717), B=TreeGeo(), V=(x,y,z)=>new THREE.Vector3(x,y,z), lerp=(a,b,t)=>a+(b-a)*t;
  const hue=[[0x4a8a2c,0xc4e05a],[0x4f9030,0xcce466],[0x468428,0xbadb52],[0x56963a,0xd2e870],[0x488c2e,0xc0de58],[0x52902c,0xd0e25c],[0x42822a,0xb4d64e],[0x5a9a3a,0xd8ec78]][v%8];
  const dark=new THREE.Color(hue[0]), lite=new THREE.Color(hue[1]), bark=t=>new THREE.Color(1,1,1).multiplyScalar(0.78+0.22*t);
  // the trunk: leaning a little, twisting, flaring at the roots
  const H=lerp(3.2,3.9,q()), lean=[lerp(-0.25,0.25,q()),lerp(-0.25,0.25,q())], tw=q()*6.28, trunk=[], trad=[];
  for(let k=0;k<=8;k++){ const t=k/8, y=t*H; trunk.push(V(lean[0]*t*t+Math.sin(tw+t*3)*0.06,y,lean[1]*t*t+Math.cos(tw+t*3)*0.06)); trad.push(0.34-0.1*t+0.22*Math.pow(1-t,6)); }
  B.tube(trunk,trad,10,TA.bark,bark);
  for(let k=0;k<4;k++){ const a=k*1.57+q()*0.8, pts=[V(Math.cos(a)*0.2,0.5,Math.sin(a)*0.2),V(Math.cos(a)*0.55,0.12,Math.sin(a)*0.55),V(Math.cos(a)*0.85,-0.05,Math.sin(a)*0.85)]; B.tube(pts,[0.16,0.1,0.04],6,TA.bark,bark); } // roots
  // the limbs: three to five, growing out of the top of the trunk sideways first, then curving up to a clump
  const top=trunk[8], nL=3+Math.floor(q()*3), clumps=[], trR=k=>trad[Math.min(8,k)];
  for(let k=0;k<nL;k++){ const a=k/nL*6.283+q()*0.7, len=lerp(1.9,2.8,q()), rise=lerp(1.7,2.6,q()), ks=5+Math.floor(q()*3), s0=trunk[ks];
    const out=V(Math.cos(a),0,Math.sin(a)), p1=s0.clone().addScaledVector(out,len*0.55).add(V(0,rise*0.18,0)), tip=s0.clone().addScaledVector(out,len).add(V(0,rise,0));
    const pts=[]; for(let s2=0;s2<=7;s2++){ const t=s2/7; pts.push(V(lerp(lerp(s0.x,p1.x,t),lerp(p1.x,tip.x,t),t),lerp(lerp(s0.y,p1.y,t),lerp(p1.y,tip.y,t),t),lerp(lerp(s0.z,p1.z,t),lerp(p1.z,tip.z,t),t))); }
    const r0=trR(ks)*0.72; B.tube(pts,pts.map((_,q2)=>lerp(r0,0.05,Math.pow(q2/7,0.8))),7,TA.bark,bark);
    { const b=pts[4], a2=a+(q()<0.5?1.0:-1.0), tw2=V(b.x+Math.cos(a2)*1.1,b.y+0.9,b.z+Math.sin(a2)*1.1); B.tube([b,V((b.x+tw2.x)/2,(b.y+tw2.y)/2+0.12,(b.z+tw2.z)/2),tw2],[r0*0.45,r0*0.3,0.03],5,TA.bark,bark); clumps.push([tw2,lerp(1.2,1.6,q())]); }
    clumps.push([tip,lerp(1.55,2.0,q())]); }
  { const ext=[top,V(top.x+lean[0]*0.3,top.y+0.8,top.z+lean[1]*0.3),V(top.x+lean[0]*0.5,top.y+1.7,top.z+lean[1]*0.5)]; B.tube(ext,[trad[8],trad[8]*0.6,0.05],8,TA.bark,bark); }
  clumps.push([V(top.x+lerp(-0.5,0.5,q()),top.y+2.7,top.z+lerp(-0.5,0.5,q())),lerp(1.8,2.2,q())],[V(top.x,top.y+1.6,top.z),1.7]);
  // the crown's centre and extent, for lighting the clumps as one shape
  let cx=0,cy=0,cz=0; clumps.forEach(([p])=>{ cx+=p.x; cy+=p.y; cz+=p.z; }); cx/=clumps.length; cy/=clumps.length; cz/=clumps.length;
  let ylo=1e9, yhi=-1e9; clumps.forEach(([p,r])=>{ ylo=Math.min(ylo,p.y-r*0.7); yhi=Math.max(yhi,p.y+r); });
  const tmp=new THREE.Color();
  for(const [c,r] of clumps){ const nCard=Math.round(30+r*16);
    for(let k=0;k<nCard;k++){ // points over the clump's shell (flattened underneath), cards facing every which way
      const u=q()*2-1, ph=q()*6.283, sr=Math.sqrt(1-u*u), d=V(sr*Math.cos(ph),u,sr*Math.sin(ph)); if(d.y<0) d.y*=0.42; const f=Math.sqrt(q()), rr=r*(0.34+0.4*f);
      const p=V(c.x+d.x*rr,c.y+d.y*rr*0.78,c.z+d.z*rr), sz=lerp(0.44,0.64,q())*(0.75+r*0.2)*(1-0.3*f); // (the outermost leaves are the smallest)
      const nrm=V((q()-0.5)*0.35,(q()-0.5)*0.35,(q()-0.5)*0.35).add(d).normalize(), ax=V(0,1,0).cross(nrm); if(ax.lengthSq()<1e-3) ax.set(1,0,0); ax.normalize(); const ay=new THREE.Vector3().crossVectors(nrm,ax).normalize(), rot=q()*6.283;
      const axr=ax.clone().multiplyScalar(Math.cos(rot)).addScaledVector(ay,Math.sin(rot)).multiplyScalar(sz), ayr=ay.clone().multiplyScalar(Math.cos(rot)).addScaledVector(ax,-Math.sin(rot)).multiplyScalar(sz);
      const soft=(x,y,z)=>{ const a=V(x-c.x,(y-c.y)*1.2,z-c.z).normalize(), b=V(x-cx,(y-cy)*1.4,z-cz).normalize(); return a.multiplyScalar(0.55).add(b.multiplyScalar(0.45)).normalize(); };
      const col=(x,y,z)=>{ const h=Math.max(0,Math.min(1,(y-ylo)/(yhi-ylo))), out=Math.min(1,Math.hypot(x-c.x,(y-c.y)*1.2,z-c.z)/r), ao=0.72+0.28*out; tmp.copy(dark).lerp(lite,Math.pow(h,0.8)*0.8+0.2*out); return tmp.clone().multiplyScalar(ao); };
      const corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([sx,sy])=>{ const x=p.x+axr.x*sx+ayr.x*sy, y=p.y+axr.y*sx+ayr.y*sy, z=p.z+axr.z*sx+ayr.z*sy; return col(x,y,z); });
      B.card(p,axr,ayr,TA.leaf,soft,corners); } }
  return B.done(); }

function pineGeo(v){ const q=seeded(51511+v*6151), B=TreeGeo(), V=(x,y,z)=>new THREE.Vector3(x,y,z), lerp=(a,b,t)=>a+(b-a)*t;
  const hue=[[0x2a5e3c,0x7fb86c],[0x2e6440,0x88c074],[0x285a3a,0x78b268],[0x316a44,0x90c87c],[0x2b603e,0x80ba6e],[0x306842,0x8ac276],[0x26563a,0x74ac64],[0x336e46,0x96ce82]][v%8];
  const dark=new THREE.Color(hue[0]), lite=new THREE.Color(hue[1]), bark=t=>new THREE.Color(1,1,1).multiplyScalar(0.8+0.2*t), tmp=new THREE.Color();
  const H=lerp(6.4,7.4,q()), trunk=[], rad=[]; for(let k=0;k<=6;k++){ const t=k/6; trunk.push(V(Math.sin(t*2+v)*0.04,t*H,Math.cos(t*2+v)*0.04)); rad.push(0.28*(1-t*0.85)+0.12*Math.pow(1-t,5)); }
  B.tube(trunk,rad,8,TA.pbark,bark);
  const R=TA.pine, tiers=6+(v%2), col=(h,edge,under)=>tmp.copy(dark).lerp(lite,Math.min(1,0.12+0.55*h+0.35*edge)).multiplyScalar(under?0.55:1).clone();
  for(let ti=0;ti<tiers;ti++){ const t=ti/(tiers-1), y0=lerp(1.25,H*0.78,t), top=y0+lerp(2.1,1.5,t)+(ti===tiers-1?1.1:0), Rr=lerp(2.55,0.75,Math.pow(t,0.85))*(0.94+q()*0.12), N=Math.round(lerp(16,9,t)), rot=q()*6.283, tx=trunk[0].x, tz=trunk[0].z;
    // apex ring (near the trunk), the hem (alternating long boughs and short notches, drooping at the tips), the inner ring underneath
    const apex=[], hem=[], inner=[], h0=Math.min(1,(y0-1)/(H-1)), h1=Math.min(1,(top-1)/(H-1));
    for(let k=0;k<=N*2;k++){ const a=rot+k/(N*2)*6.283, long=k%2===0, rr=Rr*(long?1:0.74)*(0.94+0.12*Math.sin(k*1.7+v)), dy=long?-0.28-0.1*q():0.05, ca=Math.cos(a), sa=Math.sin(a), kk=k%(N*2)===0&&k>0;
      const u=R[0]+(R[2]-R[0])*(k/(N*2));
      const pa=V(tx+ca*0.16,top,tz+sa*0.16), ph=V(tx+ca*rr,y0+dy,tz+sa*rr), pi=V(tx+ca*rr*0.35,y0+0.45,tz+sa*rr*0.35);
      const na=V(ca*0.55,0.85,sa*0.55).normalize(), nh=V(ca,0.55,sa).normalize(), ni=V(ca*0.3,-1,sa*0.3).normalize();
      apex.push(B.vert(pa.x,pa.y,pa.z,na.x,na.y,na.z,u,R[3],col(h1,0,false))); hem.push(B.vert(ph.x,ph.y,ph.z,nh.x,nh.y,nh.z,u,R[1],col(h0,long?1:0.4,false)));
      inner.push(B.vert(pi.x,pi.y,pi.z,ni.x,ni.y,ni.z,u,R[1]+(R[3]-R[1])*0.3,col(h0,0,true))); }
    for(let k=0;k<N*2;k++){ B.tri(apex[k],hem[k],hem[k+1]); B.tri(apex[k],hem[k+1],apex[k+1]); B.tri(hem[k],inner[k],inner[k+1]); B.tri(hem[k],inner[k+1],hem[k+1]); } }
  return B.done(); }

function treeVariant(kind,v){ const geo=kind==='tree'?broadleafGeo(v):pineGeo(v); return {geo,mat:treeMat,depth:treeDepth}; }

/* impostors: each variant drawn once (side view and top view) into one texture, unlit (its colours only); the far
   trees are those pictures on crossed cards, lit with soft round normals like the real ones */
const IMP={rt:null,tile:256,cols:8,rows:4,size:{},mat:null,depth:null};
function buildImpostors(){ if(IMP.rt) return; const T=IMP.tile, W=T*IMP.cols, H=T*IMP.rows;
  const rt=new THREE.WebGLRenderTarget(W,H,{minFilter:THREE.LinearMipmapLinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat,generateMipmaps:true}); rt.texture.generateMipmaps=true;
  const sc=new THREE.Scene(), cam=new THREE.OrthographicCamera(-1,1,1,-1,0.1,100), mat=new THREE.MeshBasicMaterial({map:TREE_ATLAS,vertexColors:true,alphaTest:0.42,side:THREE.DoubleSide});
  const prevRT=renderer.getRenderTarget(), prevClr=renderer.getClearColor(new THREE.Color()), prevA=renderer.getClearAlpha(), prevAuto=renderer.autoClear, prevSh=renderer.shadowMap.enabled;
  renderer.setRenderTarget(rt); renderer.setClearColor(0x000000,0); renderer.clear(); renderer.autoClear=false; renderer.shadowMap.enabled=false;
  let tile=0; for(const kind of ['tree','pine']){ let S=0, y0=0; const geos=[]; for(let v=0;v<8;v++){ const g=propVariant(kind,v).geo; geos.push(g); const b=g.boundingBox; S=Math.max(S,b.max.y-b.min.y+0.4,(b.max.x-b.min.x)+0.4,(b.max.z-b.min.z)+0.4); y0=Math.min(y0,b.min.y); }
    IMP.size[kind]={S,y0};
    for(let v=0;v<8;v++){ const m=new THREE.Mesh(geos[v],mat); sc.add(m);
      for(const view of ['side','top']){ const k=tile++, cx=k%IMP.cols, cy=Math.floor(k/IMP.cols);
        if(view==='side'){ cam.left=-S/2; cam.right=S/2; cam.bottom=y0-0.2; cam.top=y0-0.2+S; cam.up.set(0,1,0); cam.position.set(0,0,40); cam.lookAt(0,0,0); } // (up before aiming: after a top view it was still pointing along z)
        else { cam.left=-S/2; cam.right=S/2; cam.top=S/2; cam.bottom=-S/2; cam.position.set(0,60,0); cam.up.set(0,0,-1); cam.lookAt(0,0,0); }
        cam.updateProjectionMatrix(); rt.viewport.set(cx*T,cy*T,T,T); rt.scissor.set(cx*T,cy*T,T,T); rt.scissorTest=true; renderer.setRenderTarget(rt); renderer.render(sc,cam); }
      sc.remove(m); } }
  rt.scissorTest=false; rt.viewport.set(0,0,W,H); rt.scissor.set(0,0,W,H); renderer.setRenderTarget(prevRT); renderer.setClearColor(prevClr,prevA); renderer.autoClear=prevAuto; renderer.shadowMap.enabled=prevSh;
  IMP.rt=rt; IMP.mat=new THREE.MeshLambertMaterial({map:rt.texture,alphaTest:0.3,side:THREE.DoubleSide,emissive:0x1a1a10}); IMP.mat.onBeforeCompile=sh=>{ impTopFade(sh); sh.fragmentShader=sh.fragmentShader.replace('reflectedLight.indirectDiffuse += ( gl_FrontFacing ) ? vIndirectFront : vIndirectBack;','reflectedLight.indirectDiffuse += vIndirectFront;').replace('reflectedLight.directDiffuse = ( gl_FrontFacing ) ? vLightFront : vLightBack;','reflectedLight.directDiffuse = vLightFront;'); };
  IMP.depth=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking,map:rt.texture,alphaTest:0.38,side:THREE.DoubleSide}); }
// the far model of one variant: n crossed cards with its side picture and a level card with its top picture
// the crown-from-above card only shows when you look down on the tree; from the side (or below) it folds away, so it
// never reads as a floating disc
function impTopFade(sh){ sh.vertexShader='attribute float topc;\n'+sh.vertexShader.replace('#include <project_vertex>',`#ifdef USE_INSTANCING
  if(topc>0.5){ vec4 wq=modelMatrix*instanceMatrix*vec4(transformed,1.0); vec3 vt=viewMatrix[3].xyz, cp=-vec3(dot(viewMatrix[0].xyz,vt),dot(viewMatrix[1].xyz,vt),dot(viewMatrix[2].xyz,vt)); float up=cp.y-wq.y, dh=length(cp.xz-wq.xz); if(up<dh*0.14) transformed=vec3(0.0,-1000.0,0.0); }
#endif
#include <project_vertex>`); }
function impostorGeo(kind,v,n){ const {S,y0}=IMP.size[kind], k0=(kind==='tree'?0:16)+v*2, T=IMP.tile, Wd=T*IMP.cols, Hd=T*IMP.rows, P=[],N=[],U=[],I=[];
  const reg=k=>{ const cx=k%IMP.cols, cy=Math.floor(k/IMP.cols), e=1.5; return [(cx*T+e)/Wd,(cy*T+e)/Hd,((cx+1)*T-e)/Wd,((cy+1)*T-e)/Hd]; };
  const cy=y0-0.2+S*0.55, put=(x,y,z,u,w)=>{ P.push(x,y,z); const nx=x, ny=(y-cy)*0.8+0.3, nz=z, l=Math.hypot(nx,ny,nz)||1; N.push(nx/l,ny/l,nz/l); U.push(u,w); return P.length/3-1; };
  const side=reg(k0), top=reg(k0+1);
  for(let k=0;k<n;k++){ const a=k/n*Math.PI, dx=Math.cos(a)*S/2, dz=Math.sin(a)*S/2, b=y0-0.2, t=b+S;
    const i0=put(-dx,b,-dz,side[0],side[1]), i1=put(dx,b,dz,side[2],side[1]), i2=put(dx,t,dz,side[2],side[3]), i3=put(-dx,t,-dz,side[0],side[3]); I.push(i0,i1,i2,i0,i2,i3); }
  const nSide=P.length/3;
  { const h=kind==='tree'?y0+S*0.62:y0+S*0.42, s=S/2, i0=put(-s,h,s,top[0],top[1]), i1=put(s,h,s,top[2],top[1]), i2=put(s,h,-s,top[2],top[3]), i3=put(-s,h,-s,top[0],top[3]); I.push(i0,i1,i2,i0,i2,i3); }
  const g=new THREE.BufferGeometry(); g.setAttribute('topc',new THREE.Float32BufferAttribute(P.map((v,i)=>i).filter(i=>i%3===0).map(i=>i/3>=nSide?1:0),1)); g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(N,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(U,2)); g.setIndex(I); g.computeBoundingSphere(); return g; }

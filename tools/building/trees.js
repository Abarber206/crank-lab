/* ---------- trees ----------
   Broadleaf trees in the stylised alder look: a twisting trunk that splits into curving limbs, and a wide crown made of
   leafy clumps, each a cloud of cut-out leaf cards lit as one soft shape (bright yellow-green on top, deep green
   underneath and inside). Pines are tiers of drooping needle sprays round a tapering trunk. Trunk, limbs and leaves
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
  // pine sprays (top right): a fan of twigs from the base (left) packed with needles, filling the card to a rounded tip
  { g.save(); g.translate(512,0); const twigs=[[-0.32,0.82],[0,1],[0.32,0.82]];
    for(const [sp,ln] of twigs){ const L=470*ln, ang=sp*0.55; for(let k=0;k<700;k++){ const t=Math.random(), x=22+Math.cos(ang)*t*L, y=256+Math.sin(ang)*t*L, half=(1-t*0.55)*1, len=rnd(22,42)*(1-t*0.35)*half, side=Math.random()<0.5?-1:1, a=ang+side*rnd(0.55,1.15);
        g.strokeStyle=['#7cab68','#6a9c5a','#8ebd76','#5a8c4e','#a2c888','#b4d49a'][Math.floor(Math.random()*6)]; g.lineWidth=rnd(2.2,3.6); g.beginPath(); g.moveTo(x,y); g.lineTo(x+Math.cos(a)*len,y+Math.sin(a)*len); g.stroke(); }
      g.strokeStyle='#6b4a2c'; g.lineWidth=5; g.beginPath(); g.moveTo(22,256); g.lineTo(22+Math.cos(ang)*L*0.95,256+Math.sin(ang)*L*0.95); g.stroke(); }
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
const treeMat=new THREE.MeshLambertMaterial({map:TREE_ATLAS,vertexColors:true,alphaTest:0.42,side:THREE.DoubleSide,emissive:0x1a1a10}); // a little light of its own: shaded limbs and inner leaves stay warm, not black treeMat.onBeforeCompile=treeMatPatch;
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
  for(const [c,r] of clumps){ const nCard=Math.round(18+r*10);
    for(let k=0;k<nCard;k++){ // points over the clump's shell (flattened underneath), cards facing every which way
      const u=q()*2-1, ph=q()*6.283, sr=Math.sqrt(1-u*u), d=V(sr*Math.cos(ph),u,sr*Math.sin(ph)); if(d.y<0) d.y*=0.42; const rr=r*(0.55+0.45*Math.sqrt(q()));
      const p=V(c.x+d.x*rr,c.y+d.y*rr*0.78,c.z+d.z*rr), sz=lerp(0.62,0.95,q())*(0.75+r*0.22);
      const nrm=V(q()-0.5,q()-0.5,q()-0.5).add(d).normalize(), ax=V(0,1,0).cross(nrm); if(ax.lengthSq()<1e-3) ax.set(1,0,0); ax.normalize(); const ay=new THREE.Vector3().crossVectors(nrm,ax).normalize(), rot=q()*6.283;
      const axr=ax.clone().multiplyScalar(Math.cos(rot)).addScaledVector(ay,Math.sin(rot)).multiplyScalar(sz), ayr=ay.clone().multiplyScalar(Math.cos(rot)).addScaledVector(ax,-Math.sin(rot)).multiplyScalar(sz);
      const soft=(x,y,z)=>{ const a=V(x-c.x,(y-c.y)*1.2,z-c.z).normalize(), b=V(x-cx,(y-cy)*1.4,z-cz).normalize(); return a.multiplyScalar(0.55).add(b.multiplyScalar(0.45)).normalize(); };
      const col=(x,y,z)=>{ const h=Math.max(0,Math.min(1,(y-ylo)/(yhi-ylo))), out=Math.min(1,Math.hypot(x-c.x,(y-c.y)*1.2,z-c.z)/r), ao=0.72+0.28*out; tmp.copy(dark).lerp(lite,Math.pow(h,0.8)*0.8+0.2*out); return tmp.clone().multiplyScalar(ao); };
      const corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([sx,sy])=>{ const x=p.x+axr.x*sx+ayr.x*sy, y=p.y+axr.y*sx+ayr.y*sy, z=p.z+axr.z*sx+ayr.z*sy; return col(x,y,z); });
      B.card(p,axr,ayr,TA.leaf,soft,corners); } }
  return B.done(); }

function pineGeo(v){ const q=seeded(51511+v*6151), B=TreeGeo(), V=(x,y,z)=>new THREE.Vector3(x,y,z), lerp=(a,b,t)=>a+(b-a)*t;
  const hue=[[0x2e6a44,0x8cc47a],[0x327048,0x94cc80],[0x2c6642,0x86be76],[0x36764c,0x9cd286],[0x2f6c46,0x8ac27a],[0x34724a,0x92c87e],[0x2a6240,0x80ba72],[0x387a4e,0xa2d68c]][v%8];
  const dark=new THREE.Color(hue[0]), lite=new THREE.Color(hue[1]), bark=t=>new THREE.Color(1,1,1).multiplyScalar(0.8+0.2*t);
  const H=lerp(6.2,7.0,q()), trunk=[], rad=[]; for(let k=0;k<=6;k++){ const t=k/6; trunk.push(V(Math.sin(t*2+v)*0.04,t*H,Math.cos(t*2+v)*0.04)); rad.push(0.27*(1-t*0.85)+0.12*Math.pow(1-t,5)); }
  B.tube(trunk,rad,8,TA.pbark,bark);
  const tiers=8, tmp=new THREE.Color();
  for(let ti=0;ti<tiers;ti++){ const t=ti/(tiers-1), y=lerp(1.5,H-0.15,t), R=lerp(2.5,0.55,Math.pow(t,0.9))*(0.92+q()*0.16), n=Math.round(lerp(13,6,t)), droop=lerp(0.62,0.4,t);
    for(let k=0;k<n;k++){ const a=k/n*6.283+ti*0.9+q()*0.35, dir=V(Math.cos(a),0,Math.sin(a)), side=V(-dir.z,0,dir.x);
      const L=R/Math.cos(droop), w=Math.min(1.25,6.283*R/n*0.85+0.35)*(0.9+q()*0.2), base=V(trunk[0].x+dir.x*0.1,y,trunk[0].z+dir.z*0.1);
      const ax=V(dir.x*Math.cos(droop),-Math.sin(droop),dir.z*Math.cos(droop)).multiplyScalar(L/2), c=base.clone().add(ax), ay=side.clone().multiplyScalar(w/2);
      const soft=(x,yy,z)=>V(x,(yy-H*0.42)*0.55+0.6,z).normalize();
      const cols=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([sx])=>{ const h=Math.min(1,(y-1.3)/(H-1.3)), tip=(sx+1)/2; tmp.copy(dark).lerp(lite,0.2+0.5*h+0.3*tip); return tmp.clone().multiplyScalar(0.7+0.3*tip); });
      B.card(c,ax,ay,TA.pine,soft,cols);
      const ay2=V(0,w*0.38,0).addScaledVector(side,w*0.12); B.card(c.clone().add(V(0,0.12,0)),ax,ay2,TA.pine,soft,cols); } }
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
  if(topc>0.5){ vec4 wq=modelMatrix*instanceMatrix*vec4(transformed,1.0); float up=cameraPosition.y-wq.y, dh=length(cameraPosition.xz-wq.xz); if(up<dh*0.14) transformed=vec3(0.0,-1000.0,0.0); }
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

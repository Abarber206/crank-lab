/* ---------- what makes a house a home ----------
   Framed paintings on the walls (high enough to clear the tall furniture), a lamp under every ceiling, a rug in some
   rooms, curtains at the windows. Each thing belongs to the wall or floor it's on: it's part of that piece's mesh (so it
   goes into the town's merged meshes), comes back when the piece is rebuilt, and goes when the piece is broken or the
   spot it hangs on is cut away. */
const HDECOR={tex:null,mats:null};
function hdecorMats(){ if(HDECOR.mats) return HDECOR.mats; const W=1024, H=768, c=document.createElement('canvas'); c.width=W; c.height=H; const g=c.getContext('2d'), R=seeded(4242), pick=a=>a[Math.floor(R()*a.length)];
  // eight paintings (256 x 256 each, two rows) and four rugs (the third row)
  for(let k=0;k<8;k++){ const x=(k%4)*256, y=Math.floor(k/4)*256; g.save(); g.beginPath(); g.rect(x,y,256,256); g.clip(); const kind=k%4;
    if(kind===0||kind===2){ // a landscape: sky, sun or moon, layered hills, maybe a lake
      const night=k===6, sk=g.createLinearGradient(0,y,0,y+256); sk.addColorStop(0,night?'#1c2a52':pick(['#7fb6e6','#f2a65a','#9fd0f0'])); sk.addColorStop(1,night?'#4b4f86':pick(['#fde7b8','#f7d08a','#e8f4ff'])); g.fillStyle=sk; g.fillRect(x,y,256,256);
      g.fillStyle=night?'#f4f0d0':'#fff2b0'; g.beginPath(); g.arc(x+60+R()*140,y+60+R()*30,18+R()*10,0,7); g.fill();
      for(let L=0;L<4;L++){ const base=y+120+L*32, col=night?['#2a3358','#232a4a','#1b2140','#141a33'][L]:['#9db6a8','#6f9a6c','#4f7d4c','#3a6238'][L]; g.fillStyle=col; g.beginPath(); g.moveTo(x,y+256);
        for(let s=0;s<=16;s++){ const xx=x+s*16; g.lineTo(xx,base-20*Math.sin(s*0.6+L*1.7+k)-14*R()); } g.lineTo(x+256,y+256); g.fill(); }
      if(kind===2){ g.fillStyle=night?'rgba(120,140,200,.5)':'rgba(120,180,220,.75)'; g.fillRect(x,y+215,256,41); } }
    else if(kind===1){ // flowers in a vase
      g.fillStyle=pick(['#efe3cc','#d8e4ea','#f3d9d2']); g.fillRect(x,y,256,256); g.fillStyle=pick(['#3d6a8a','#8a4b3d','#5a6b3a']); g.beginPath(); g.ellipse(x+128,y+200,40,46,0,0,7); g.fill(); g.fillRect(x+108,y+150,40,20);
      for(let f=0;f<9;f++){ const fx=x+70+R()*116, fy=y+50+R()*90; g.strokeStyle='#3f6b35'; g.lineWidth=3; g.beginPath(); g.moveTo(x+128,y+160); g.lineTo(fx,fy); g.stroke(); g.fillStyle=pick(['#e8494f','#f2c230','#f08ac0','#ffffff','#e86a2a']); for(let q=0;q<6;q++){ g.beginPath(); g.arc(fx+Math.cos(q)*9,fy+Math.sin(q)*9,8,0,7); g.fill(); } g.fillStyle='#f6d44a'; g.beginPath(); g.arc(fx,fy,6,0,7); g.fill(); } }
    else { // modern: blocks of colour with black lines
      g.fillStyle='#f4f1e8'; g.fillRect(x,y,256,256); for(let q=0;q<6;q++){ g.fillStyle=pick(['#d63a2f','#2f5fb3','#f2c230','#f4f1e8','#1f2a33']); g.fillRect(x+R()*200,y+R()*200,40+R()*120,40+R()*120); }
      g.strokeStyle='#15171a'; g.lineWidth=7; for(let q=0;q<4;q++){ const v=R()*256; g.beginPath(); q%2?(g.moveTo(x+v,y),g.lineTo(x+v,y+256)):(g.moveTo(x,y+v),g.lineTo(x+256,y+v)); g.stroke(); } }
    g.restore(); }
  for(let k=0;k<4;k++){ const x=k*256, y=512, cA=['#8a2b2b','#2b4a7a','#6b5a2a','#3d6b4f'][k], cB=['#e8c690','#d9d2c0','#c9e0d0','#f0e2c8'][k], cC=['#2b2420','#1d2433','#3a2a1a','#1f2a24'][k];
    g.fillStyle=cA; g.fillRect(x,y,256,256); g.strokeStyle=cB; g.lineWidth=10; g.strokeRect(x+14,y+14,228,228); g.lineWidth=4; g.strokeStyle=cC; g.strokeRect(x+28,y+28,200,200);
    g.fillStyle=cB; for(let q=0;q<5;q++){ const cx=x+128, cy=y+128, r=90-q*18; g.beginPath(); g.moveTo(cx,cy-r); g.lineTo(cx+r,cy); g.lineTo(cx,cy+r); g.lineTo(cx-r,cy); g.closePath(); g.fillStyle=q%2?cB:cC; g.fill(); } }
  const t=new THREE.CanvasTexture(c); t.anisotropy=4; HDECOR.tex=t;
  const L=(c,o)=>new THREE.MeshLambertMaterial(Object.assign({color:c},o||{}));
  return HDECOR.mats={art:L(0xffffff,{map:t}),frame:[L(0x4a3020),L(0x1f2124),L(0xb8913a)],curtain:[L(0xb8484a),L(0x5f7fa8),L(0xd9c9a3)],rod:L(0x3a3a3e),shade:L(0xf2ead8,{emissive:0x3a3020}),bulb:new THREE.MeshBasicMaterial({color:0xfff1c4})}; }
// the plan, worked out once per town when its houses are built: what goes on which piece
function planHouseDecor(t){ if(t.kind||!t.houses) return; const plan=t.decorPlan=new Map(), C=CELL, r=seeded(t.seed*7+99), add=(key,it)=>{ (plan.get(key)||plan.set(key,[]).get(key)).push(it); };
  const solid=(p,bit)=>p&&p.type==='wall'&&(p.mask==null||p.mask===511||!!(p.mask>>bit&1));
  for(const h of t.houses){ const st=h.floors>1?houseStair(h).cells:[], inStair=(i,j)=>st.some(c=>c[0]===i&&c[1]===j);
    for(let l=h.L;l<h.L+h.floors;l++) for(let a=0;a<h.w;a++) for(let b=0;b<h.d;b++){ const i=h.i0+a, j=h.j0+b, cx=(i+.5)*C, cz=(j+.5)*C, y0=l*LVL;
      // the lamp, under the ceiling (the floor above)
      const ce=pieces.get(`f${i}_${j}_${l+1}`); if(ce&&!inStair(i,j)) add(ce.key,{k:'lamp',x:cx,y:(l+1)*LVL-FT,z:cz});
      // a rug now and then
      const fl=pieces.get(`f${i}_${j}_${l}`); if(fl&&!inStair(i,j)&&r()<0.45) add(fl.key,{k:'rug',x:cx+(r()-.5)*0.6,y:y0+0.012,z:cz+(r()-.5)*0.6,rot:r()<0.5?0:Math.PI/2,v:Math.floor(r()*4)});
      if(inStair(i,j)) continue;
      // the four walls round this cell: a painting on a plain stretch, curtains at a window
      for(const [key,nx,nz,wx,wz] of [[`wx${i}_${j}_${l}`,1,0,i*C,cz],[`wx${i+1}_${j}_${l}`,-1,0,(i+1)*C,cz],[`wz${i}_${j}_${l}`,0,1,cx,j*C],[`wz${i}_${j+1}_${l}`,0,-1,cx,(j+1)*C]]){ const p=pieces.get(key); if(!p) continue;
        const fx=wx+nx*(WT/2+0.005), fz=wz+nz*(WT/2+0.005), ax=nx?0:1, az=nx?1:0; // along the wall
        if(solid(p,4)&&solid(p,1)&&r()<0.42){ const v=Math.floor(r()*8), wide=r()<0.6, w=wide?1.15:0.8, hh=wide?0.8:1.0; add(key,{k:'pic',x:fx,y:y0+2.45,z:fz,nx,nz,w,h:hh,v,f:Math.floor(r()*3),bit:4}); }
        for(let c=0;c<3;c++) if(p.mask!=null&&p.mask!==511&&!(p.mask>>(c+3)&1)&&(p.mask>>c&1)){ // a window in this column (a door has its bottom tile gone too)
          const off=(c-1)*C/3, px=fx+ax*off, pz=fz+az*off; add(key,{k:'curt',x:px,y:y0+2.95,z:pz,nx,nz,col:Math.floor(r()*3),bit:c}); } } } } }
function addHouseDecor(p){ const t=p.town, items=t&&t.decorPlan&&t.decorPlan.get(p.key); if(!items||!p.group) return; const M=hdecorMats(); p.group.updateMatrixWorld(true);
  const put=(geo,mat,x,y,z,ry)=>{ const m=new THREE.Mesh(geo,mat); const v=p.group.worldToLocal(new THREE.Vector3(x,y,z)); m.position.copy(v); if(ry) m.rotation.y=ry; m.castShadow=false; m.receiveShadow=true; m.userData.decor=true; m.userData.piece=p; p.group.add(m); return m; };
  for(const it of items){ if(it.bit!=null&&p.type==='wall'&&p.mask!=null&&p.mask!==511&&(it.k==='pic'?!(p.mask>>it.bit&1):!(p.mask>>it.bit&1))) continue; // its spot was cut away
    const ry=it.nx?(it.nx>0?Math.PI/2:-Math.PI/2):(it.nz>0?0:Math.PI);
    if(it.k==='pic'){ const ax=it.nx?0:1, az=it.nx?1:0, d=0.03; put(rbox(it.w+0.1,it.h+0.1,0.05,0.012),M.frame[it.f],it.x+it.nx*d,it.y,it.z+it.nz*d,ry);
      const g=new THREE.PlaneGeometry(it.w,it.h), u0=(it.v%4)/4, v0=1-(Math.floor(it.v/4)+1)*(256/768), uv=g.attributes.uv; for(let q=0;q<uv.count;q++) uv.setXY(q,u0+uv.getX(q)*0.25,v0+uv.getY(q)*(256/768)*0.96+0.004);
      put(g,M.art,it.x+it.nx*(d+0.028),it.y,it.z+it.nz*(d+0.028),ry); }
    else if(it.k==='rug'){ const g=new THREE.BoxGeometry(2.4,0.016,1.6), u0=it.v/4, uv=g.attributes.uv; for(let q=0;q<uv.count;q++) uv.setXY(q,u0+0.01+uv.getX(q)*0.23,0.01+uv.getY(q)*(256/768)*0.95); put(g,M.art,it.x,it.y,it.z,it.rot); }
    else if(it.k==='lamp'){ put(new THREE.CylinderGeometry(0.012,0.012,0.5,6),M.rod,it.x,it.y-0.25,it.z); put(new THREE.CylinderGeometry(0.14,0.36,0.28,18,1,true),M.shade,it.x,it.y-0.62,it.z).material.side=THREE.DoubleSide; put(new THREE.SphereGeometry(0.09,10,8),M.bulb,it.x,it.y-0.7,it.z); }
    else if(it.k==='curt'){ const ax=it.nx?0:1, az=it.nx?1:0, d=0.07, tw=CELL/3; put(new THREE.CylinderGeometry(0.018,0.018,tw+0.7,6).rotateZ(Math.PI/2),M.rod,it.x+it.nx*d,it.y,it.z+it.nz*d,it.nx?Math.PI/2:0);
      for(const s of [-1,1]){ const g=new THREE.BoxGeometry(0.42,1.75,0.035,6,1,1), pa=g.attributes.position; for(let q=0;q<pa.count;q++){ const xx=pa.getX(q); pa.setZ(q,pa.getZ(q)+0.03*Math.sin(xx*22)); } g.computeVertexNormals();
        put(g,M.curtain[it.col],it.x+ax*s*(tw/2+0.12)+it.nx*(d+0.02),it.y-0.9,it.z+az*s*(tw/2+0.12)+it.nz*(d+0.02),ry); } } } }

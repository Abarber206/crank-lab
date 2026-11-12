/* ---------- points of interest ----------
   Four of the ten sites are not towns but whole themed places: Gearworks (a factory), Fort Granite (a castle),
   Crater Labs (a research base with a rocket) and Timber Yard (a sawmill). Their buildings are ordinary map pieces
   (walls, floors, stairs, roofs) like the houses, so they stand, take damage, break and hold loot on their floors;
   the machinery, containers, rocket and the rest are solid decoration you can climb on. Each site is laid out on the
   town grid, but freely: no streets run through, the roads stop at the edge, and nothing is mirrored. */
const POI_WIN=511&~16, POI_DOOR=511&~18, POI_OPEN=448, POI_LOW=7, POI_MERLON=47;
const POI_STYLE={stone:1,corr:1,lab:1,log:1};
Object.assign(HOUSE_PAINT,{stone:[0xd9d3c6,0xc7bfae,0xb5afa4],corr:[0xb5523b,0x8e9aa3,0x3f8580,0xd2a23c],lab:[0xf5f7f9,0xe3eaef],log:[0xc08a52,0x9a6a3d]});
// the wall faces for the new styles: plain, with a window, a door, or a wide opening (only a lintel left)
function poiWallKind(m){ m=m==null?511:m; return m===POI_WIN?'win':m===POI_DOOR?'door':m===POI_OPEN?'garage':'plain'; }
function poiWallTex(style,kind){
  return houseTex(512,(g,hg,mg,S)=>{ const a=S/3, b=2*S/3;
    if(style==='stone'){ // ashlar: courses of squared blocks, each its own tone, sunk mortar joints
      g.fillStyle='#ece8df'; g.fillRect(0,0,S,S); const rh=S/8;
      for(let r=0;r<8;r++){ let x=-(r%2)*40-Math.random()*20; while(x<S){ const w=60+Math.random()*50, v=200+Math.random()*55;
          g.fillStyle=`rgb(${v},${v-4},${v-10})`; g.fillRect(x+2,r*rh+2,w-4,rh-4); speckle(g,x,r*rh,w,rh,18,'40,36,30','255,255,255');
          hg.fillStyle=gv(150+Math.random()*30); hg.fillRect(x+2,r*rh+2,w-4,rh-4); x+=w; } }
      g.fillStyle='rgba(70,64,56,.55)'; for(let r=0;r<=8;r++) g.fillRect(0,r*rh-2,S,4);
      if(kind==='win'||kind==='door'||kind==='garage'){ const y1=kind==='win'?a:kind==='door'?a:0, top=kind==='garage'?a:a; // dressed stone round the opening
        for(let k=0;k<5;k++){ const x=a-26+k*((b-a+52)/5); trimRect(g,hg,mg,x+1,top-26,(b-a+52)/5-2,24,'#bdb6a8',215); }
        if(kind!=='garage'){ trimRect(g,hg,mg,a-26,a,24,(kind==='win'?b:S)-a,'#bdb6a8',210); trimRect(g,hg,mg,b+2,a,24,(kind==='win'?b:S)-a,'#bdb6a8',210); }
        if(kind==='win') trimRect(g,hg,mg,a-30,b,b-a+60,16,'#a59e90',220); } }
    else if(style==='corr'){ // corrugated sheet: vertical ribs, a concrete plinth, rust streaks
      g.fillStyle='#f2f2f0'; g.fillRect(0,0,S,S);
      for(let x=0;x<S;x+=16){ const gr=g.createLinearGradient(x,0,x+16,0); gr.addColorStop(0,'rgba(0,0,0,.16)'); gr.addColorStop(.5,'rgba(255,255,255,.2)'); gr.addColorStop(1,'rgba(0,0,0,.16)'); g.fillStyle=gr; g.fillRect(x,0,16,S);
        const hr=hg.createLinearGradient(x,0,x+16,0); hr.addColorStop(0,gv(100)); hr.addColorStop(.5,gv(185)); hr.addColorStop(1,gv(100)); hg.fillStyle=hr; hg.fillRect(x,0,16,S); }
      for(let k=0;k<14;k++){ const x=Math.random()*S, y=Math.random()*S*0.6, h=60+Math.random()*160, gr=g.createLinearGradient(0,y,0,y+h); gr.addColorStop(0,'rgba(120,60,20,.22)'); gr.addColorStop(1,'rgba(120,60,20,0)'); g.fillStyle=gr; g.fillRect(x,y,6+Math.random()*8,h); }
      trimRect(g,hg,mg,0,0,S,12,'#3a3d42',150); trimRect(g,hg,mg,0,S-34,S,34,'#9a968e',175); speckle(g,0,S-34,S,34,160,'40,40,40','255,255,255');
      if(kind==='win'){ trimRect(g,hg,mg,a-10,a-10,b-a+20,10,'#2c3036',150); trimRect(g,hg,mg,a-10,b,b-a+20,10,'#2c3036',150); trimRect(g,hg,mg,a-10,a,10,b-a,'#2c3036',150); trimRect(g,hg,mg,b,a,10,b-a,'#2c3036',150); }
      if(kind==='door'){ trimRect(g,hg,mg,a-10,a-10,b-a+20,10,'#2c3036',150); trimRect(g,hg,mg,a-10,a,10,S-a,'#2c3036',150); trimRect(g,hg,mg,b,a,10,S-a,'#2c3036',150);
        trimRect(g,hg,mg,a+20,a-48,b-a-40,26,'#f2c94c',180); g.fillStyle='#1c1c1c'; for(let x=a+24;x<b-24;x+=18) g.fillRect(x,a-44,9,18); } // a hazard-striped sign over the door
      if(kind==='garage'){ trimRect(g,hg,mg,0,a-14,S,14,'#2c3036',150); for(let x=0;x<S;x+=32){ g.fillStyle=(x/32)%2?'#1c1c1c':'#f2c94c'; g.fillRect(x,a-12,32,10); } } } // yellow and black hazard bar on the lintel
    else if(style==='lab'){ // smooth white cladding panels, a teal band, dark window frames
      g.fillStyle='#f6f7f8'; g.fillRect(0,0,S,S); for(let x=0;x<S;x+=S/4){ g.fillStyle='rgba(0,0,0,.18)'; g.fillRect(x,0,2,S); hg.fillStyle=gv(100); hg.fillRect(x,0,3,S); }
      g.fillStyle='rgba(0,0,0,.14)'; g.fillRect(0,S/2,S,2); hg.fillStyle=gv(100); hg.fillRect(0,S/2,S,3); speckle(g,0,0,S,S,120,'60,60,60','255,255,255');
      trimRect(g,hg,mg,0,0,S,14,'#5d666e',160); trimRect(g,hg,mg,0,S-22,S,22,'#3e454c',160);
      if(kind!=='garage'&&kind!=='door') trimRect(g,hg,mg,0,S*0.12,S,18,'#22b3c4',180);
      if(kind==='win'){ trimRect(g,hg,mg,a-8,a-8,b-a+16,8,'#2a3138',150); trimRect(g,hg,mg,a-8,b,b-a+16,8,'#2a3138',150); trimRect(g,hg,mg,a-8,a,8,b-a,'#2a3138',150); trimRect(g,hg,mg,b,a,8,b-a,'#2a3138',150); }
      if(kind==='door'){ trimRect(g,hg,mg,a-8,a-8,b-a+16,8,'#2a3138',150); trimRect(g,hg,mg,a-8,a,8,S-a,'#2a3138',150); trimRect(g,hg,mg,b,a,8,S-a,'#2a3138',150); trimRect(g,hg,mg,a-40,a-46,b-a+80,22,'#22b3c4',180); }
      if(kind==='garage'){ trimRect(g,hg,mg,0,a-12,S,12,'#2a3138',150); } }
    else { // log cabin: round logs, notched corners, chinking between
      g.fillStyle='#efe6d6'; g.fillRect(0,0,S,S); const rh=S/9;
      for(let r=0;r<9;r++){ const y=r*rh, gr=g.createLinearGradient(0,y,0,y+rh); gr.addColorStop(0,'rgba(0,0,0,.28)'); gr.addColorStop(.35,'rgba(255,240,210,.18)'); gr.addColorStop(1,'rgba(40,20,0,.38)'); g.fillStyle=gr; g.fillRect(0,y,S,rh);
        const hr=hg.createLinearGradient(0,y,0,y+rh); hr.addColorStop(0,gv(90)); hr.addColorStop(.4,gv(200)); hr.addColorStop(1,gv(90)); hg.fillStyle=hr; hg.fillRect(0,y,S,rh);
        for(let k=0;k<6;k++){ g.fillStyle='rgba(70,40,15,.18)'; g.fillRect(Math.random()*S,y+rh*0.3+Math.random()*rh*0.4,40+Math.random()*90,2); } // grain
        trimRect(g,hg,mg,0,y+rh-4,S,4,'#d8ccb4',120); }
      for(const x of [0,S-14]) for(let r=0;r<9;r++){ g.fillStyle='rgba(90,55,25,.6)'; g.beginPath(); g.ellipse(x+7,r*rh+rh/2,8,rh/2-3,0,0,7); g.fill(); } // log ends at the corners
      if(kind==='win'){ trimRect(g,hg,mg,a-12,a-12,b-a+24,12,'#5a3a1e',170); trimRect(g,hg,mg,a-16,b,b-a+32,14,'#5a3a1e',190); trimRect(g,hg,mg,a-12,a,12,b-a,'#5a3a1e',170); trimRect(g,hg,mg,b,a,12,b-a,'#5a3a1e',170); }
      if(kind==='door'){ trimRect(g,hg,mg,a-12,a-12,b-a+24,12,'#5a3a1e',170); trimRect(g,hg,mg,a-12,a,12,S-a,'#5a3a1e',170); trimRect(g,hg,mg,b,a,12,S-a,'#5a3a1e',170); }
      if(kind==='garage') trimRect(g,hg,mg,0,a-14,S,14,'#5a3a1e',170); }
  },3); }
// floors, stair treads and trim for the new styles
const poiFloorTex=new Map();
function poiFloorMat(kind){ return houseMat('pf'+kind,()=>{ let t=poiFloorTex.get(kind); if(!t){ t=houseTex(256,(g,hg,mg,S)=>{
      if(kind==='stone'){ g.fillStyle='#9d978b'; g.fillRect(0,0,S,S); for(let r=0;r<4;r++) for(let c=0;c<4;c++){ const v=125+Math.random()*45; g.fillStyle=`rgb(${v},${v-3},${v-9})`; g.fillRect(c*64+2,r*64+2,60,60); hg.fillStyle=gv(150+Math.random()*30); hg.fillRect(c*64+2,r*64+2,60,60); } speckle(g,0,0,S,S,300,'30,30,30','255,255,255'); }
      else if(kind==='tar'){ g.fillStyle='#4a4c4f'; g.fillRect(0,0,S,S); speckle(g,0,0,S,S,900,'0,0,0','200,200,200'); g.fillStyle='rgba(0,0,0,.25)'; for(let y=0;y<S;y+=64) g.fillRect(0,y,S,3); }
      else if(kind==='plate'){ g.fillStyle='#8f969c'; g.fillRect(0,0,S,S); for(let y=0;y<S;y+=16) for(let x=(y/16%2)*8;x<S;x+=16){ g.fillStyle='rgba(255,255,255,.28)'; g.fillRect(x,y,9,3); hg.fillStyle=gv(190); hg.fillRect(x,y,9,3); } speckle(g,0,0,S,S,200,'0,0,0','255,255,255'); }
      else if(kind==='tile'){ g.fillStyle='#e9edf0'; g.fillRect(0,0,S,S); g.fillStyle='rgba(60,70,80,.25)'; for(let k=0;k<=S;k+=32){ g.fillRect(k,0,2,S); g.fillRect(0,k,S,2); hg.fillStyle=gv(110); hg.fillRect(k,0,2,S); hg.fillRect(0,k,S,2); } }
      else if(kind==='plank'){ for(let i=0;i<6;i++) woodGrain(g,hg,0,i*S/6,S,S/6,false,['#9c7148','#8a6440','#a3784d','#93693f','#9a6e45','#86603c'][i]); g.fillStyle='rgba(30,15,5,.6)'; for(let i=0;i<6;i++) g.fillRect(0,i*S/6,S,2); }
      else { g.fillStyle='#a9a6a0'; g.fillRect(0,0,S,S); speckle(g,0,0,S,S,700,'40,40,40','255,255,255'); g.fillStyle='rgba(50,50,50,.35)'; g.fillRect(0,0,S,2); g.fillRect(0,0,2,S); hg.fillStyle=gv(110); hg.fillRect(0,0,S,3); hg.fillRect(0,0,3,S); } // concrete
    },2); t.map.wrapS=t.map.wrapT=THREE.RepeatWrapping; poiFloorTex.set(kind,t); }
  return new THREE.MeshPhongMaterial({map:t.map,normalMap:t.normal,shininess:kind==='plate'?40:kind==='tile'?30:8,specular:0x222222,polygonOffset:true,polygonOffsetFactor:0,polygonOffsetUnits:2}); },'HOUSE_CEIL'); }
function poiTrimMat(hex){ return houseMat('ptrim'+hex,()=>new THREE.MeshPhongMaterial({color:hex,shininess:10,specular:0x111111}),'HOUSE_TRIM'); }
const poiColMats=new Map();
function poiColMat(hex,glow){ const k=hex+(glow?'g':''); let m=poiColMats.get(k); if(!m){ m=glow?new THREE.MeshBasicMaterial({color:hex}):new THREE.MeshLambertMaterial({color:hex}); poiColMats.set(k,m); } return m; }

/* the layout kit: building pieces in a block's own frame. A block is one quarter of the site between the streets; its
   cell (a,b) counts away from the streets (a across the main street, b across the cross street) and its metres (u,v)
   from the block's street edges, so one layout can be mirrored into any quarter. */
function poiFrame(t,qx,qz){ const ci=Math.round(t.x/CELL), cj=Math.round(t.z/CELL), C=CELL;
  return {qx,qz,ci,cj,
    i:a=>qx>0?ci+1+a:ci-2-a, j:b=>qz>0?cj+1+b:cj-2-b,           // the world cell of block cell a (or b)
    I:a=>qx>0?ci+1+a:ci-1-a, J:b=>qz>0?cj+1+b:cj-1-b,           // the world wall line before block cell a (between a-1 and a)
    x:u=>qx>0?(ci+1)*C+u:(ci-1)*C-u, z:v=>qz>0?(cj+1)*C+v:(cj-1)*C-v, // block metres to world
    dir:d=>[qx>0?0:2,qz>0?1:3,qx>0?2:0,qz>0?3:1][d],            // a stair rising along +a (0), +b (1), -a (2), -b (3)
    yaw:y=>{ const dx=Math.sin(y)*qx, dz=Math.cos(y)*qz; return Math.atan2(dx,dz); } }; }
function poiKit(t){ const P=[], keys=new Set(), L=Math.round(t.h/LVL);
  const add=q=>{ const key=q.type==='wall'?`w${q.axis}${q.i}_${q.j}_${q.l}`:q.type==='floor'?`f${q.i}_${q.j}_${q.l}`:`m${q.i}_${q.j}_${q.l}`; if(keys.has(key)) return null; keys.add(key); q.key=key; q.dir=q.dir||0; q.axis=q.axis||'x'; P.push(q); return q; };
  const K={P,L,
    floor:(i,j,l,skin,o)=>add(Object.assign({type:'floor',i,j,l,mat:skin.mat,skin:skin.s},o||{})),
    wallX:(I,j,l,mask,skin,o)=>add(Object.assign({type:'wall',axis:'x',i:I,j,l,mask,mat:skin.mat,skin:skin.s,out:0},o||{})), // a wall on the line x=I*CELL across cell row j
    wallZ:(i,J,l,mask,skin,o)=>add(Object.assign({type:'wall',axis:'z',i,j:J,l,mask,mat:skin.mat,skin:skin.s,out:0},o||{})),
    ramp:(i,j,l,dir,skin)=>add({type:'ramp',i,j,l,dir,mat:skin.mat,skin:skin.s}),
    // a room in world cells i0..i0+w-1, j0..j0+d-1: walls round it from level l0 up, mask(face,k,lvl) picks each panel ('w','e','n','s'; k counts along the face)
    shell(i0,j0,w,d,l0,n,skin,mask){ for(let s=0;s<n;s++){ const l=l0+s;
      for(let k=0;k<d;k++){ const mw=mask('w',k,s,d), me=mask('e',k,s,d); if(mw!=null) K.wallX(i0,j0+k,l,mw,skin); if(me!=null) K.wallX(i0+w,j0+k,l,me,skin); }
      for(let k=0;k<w;k++){ const mn=mask('n',k,s,w), ms=mask('s',k,s,w); if(mn!=null) K.wallZ(i0+k,j0,l,mn,skin); if(ms!=null) K.wallZ(i0+k,j0+d,l,ms,skin); } } },
    slab(i0,j0,w,d,l,skin,skip,o){ for(let a=0;a<w;a++) for(let b=0;b<d;b++) if(!(skip&&skip(i0+a,j0+b))) K.floor(i0+a,j0+b,l,skin,o); },
    // a pitched roof of roof pieces over a rectangle at level l, ridge along the longer side, with closed gables
    roof(i0,j0,w,d,l,skin){ for(let a=0;a<w;a++) for(let b=0;b<d;b++){ let mask=0; const along=w>=d;
        if(along){ mask=d===1?0:b<d/2-0.01?12:b>d/2-0.99&&d%2&&b===(d-1)/2?0:3; if(d===2) mask=b===0?12:3; }
        else { mask=w===1?0:a<w/2-0.01?10:5; if(w===2) mask=a===0?10:5; }
        const gable=[]; if(a===0) gable.push(['w',-1]); if(a===w-1) gable.push(['e',1]); if(b===0) gable.push(['n',-1]); if(b===d-1) gable.push(['s',1]);
        add({type:'cone',i:i0+a,j:j0+b,l,mask,mat:skin.roof||'wood',skin:skin.s,gable}); } } };
  // in a block's frame: cells and wall lines counted from the streets
  K.in=F=>({
    floor:(a,b,l,sk,o)=>K.floor(F.i(a),F.j(b),l,sk,o),
    wallA:(a,b,l,mask,sk,o)=>K.wallX(F.I(a),F.j(b),l,mask,sk,o),   // the wall line before cell a, across cell b
    wallB:(a,b,l,mask,sk,o)=>K.wallZ(F.i(a),F.J(b),l,mask,sk,o),
    ramp:(a,b,l,d,sk)=>K.ramp(F.i(a),F.j(b),l,F.dir(d),sk),
    // a room over block cells a0..a0+w-1, b0..b0+d-1; mask(face,k,lvl,n): faces 'a0' (toward the main street), 'a1' (far side), 'b0' (toward the cross street), 'b1'
    room(a0,b0,w,d,l0,n,sk,mask){ for(let s=0;s<n;s++){ const l=l0+s;
      for(let k=0;k<d;k++){ const m0=mask('a0',k,s,d), m1=mask('a1',k,s,d); if(m0!=null) K.wallX(F.I(a0),F.j(b0+k),l,m0,sk); if(m1!=null) K.wallX(F.I(a0+w),F.j(b0+k),l,m1,sk); }
      for(let k=0;k<w;k++){ const m0=mask('b0',k,s,w), m1=mask('b1',k,s,w); if(m0!=null) K.wallZ(F.i(a0+k),F.J(b0),l,m0,sk); if(m1!=null) K.wallZ(F.i(a0+k),F.J(b0+d),l,m1,sk); } } },
    slab(a0,b0,w,d,l,sk,skip,o){ for(let a=0;a<w;a++) for(let b=0;b<d;b++) if(!(skip&&skip(a0+a,b0+b))) K.floor(F.i(a0+a),F.j(b0+b),l,sk,o); },
    // the world rectangle of block cells (for roofs, which are laid out in world cells)
    rect(a0,b0,w,d){ const ia=F.i(a0), ib=F.i(a0+w-1), ja=F.j(b0), jb=F.j(b0+d-1); return [Math.min(ia,ib),Math.min(ja,jb),w,d]; } });
  return K; }
// a fixture on one floor piece: boxes in the piece's own metres (from its north-west corner, y up from the floor top), solid and drawn
function poiFix(p,list){ const o=new THREE.Vector3((p.i+.5)*CELL,p.l*LVL-FT/2,(p.j+.5)*CELL), byMat=new Map(), boxes=[];
  for(const [w,h,d,x,y,z,col,solid,glow] of list){ const g=new THREE.BoxGeometry(w,h,d); g.translate(p.i*CELL+x-o.x,p.l*LVL+y+h/2-o.y,p.j*CELL+z-o.z); const m=poiColMat(col,glow); let a=byMat.get(m); if(!a){ a=[]; byMat.set(m,a); } a.push(g);
    if(solid!==false) boxes.push([p.i*CELL+x-w/2,p.l*LVL+y,p.j*CELL+z-d/2,p.i*CELL+x+w/2,p.l*LVL+y+h,p.j*CELL+z+d/2]); }
  const parts=[]; byMat.forEach((gs,m)=>{ const g=mergeGeos(gs); g.computeVertexNormals(); g.computeBoundingSphere(); parts.push([g,m]); });
  p.fix={boxes,parts}; }

/* decoration: merged meshes in vertex colours (one per 64 m patch, so they cull), with solid boxes for standing on */
function poiDecor(){ const patches=new Map(), glows=new Map(), col=new THREE.Color();
  const bucket=(map,x,z)=>{ const k=Math.floor(x/64)+','+Math.floor(z/64); let a=map.get(k); if(!a){ a=[]; map.set(k,a); } return a; };
  const put=(g,c,x,y,z,rot,glow)=>{ if(rot){ if(rot[0]) g.rotateX(rot[0]); if(rot[2]) g.rotateZ(rot[2]); if(rot[1]) g.rotateY(rot[1]); } g.translate(x,y,z); if(g.index) g=g.toNonIndexed(); g.computeVertexNormals(); col.setHex(c);
    const n=g.attributes.position.count, ca=new Float32Array(n*3); for(let q=0;q<n;q++){ ca[q*3]=col.r; ca[q*3+1]=col.g; ca[q*3+2]=col.b; } g.setAttribute('color',new THREE.BufferAttribute(ca,3)); if(g.attributes.uv) g.deleteAttribute('uv'); bucket(glow?glows:patches,x,z).push(g); return g; };
  const D={
    box:(w,h,d,x,y,z,c,rot,glow)=>put(new THREE.BoxGeometry(w,h,d),c,x,y+h/2,z,rot,glow),            // y is the bottom
    cyl:(rt,rb,h,x,y,z,c,seg,rot,glow)=>put(new THREE.CylinderGeometry(rt,rb,h,seg||14),c,x,y+h/2,z,rot,glow),
    tube:(r,h,x,y,z,c,rot,seg)=>put(new THREE.CylinderGeometry(r,r,h,seg||10),c,x,y,z,rot),             // centred
    sph:(r,x,y,z,c,sc,glow)=>{ const g=new THREE.SphereGeometry(r,16,10); if(sc) g.scale(sc[0],sc[1],sc[2]); return put(g,c,x,y,z,null,glow); },
    geo:(g,c,x,y,z,rot,glow)=>put(g,c,x,y,z,rot,glow),
    // a solid box in world metres (split into patches no wider than 2.4 m so the collision lookup always finds it)
    solid(x0,y0,z0,x1,y1,z1){ const nx=Math.max(1,Math.ceil((x1-x0)/2.4)), nz=Math.max(1,Math.ceil((z1-z0)/2.4));
      for(let a=0;a<nx;a++) for(let b=0;b<nz;b++){ const xa=x0+(x1-x0)*a/nx, xb=x0+(x1-x0)*(a+1)/nx, za=z0+(z1-z0)*b/nz, zb=z0+(z1-z0)*(b+1)/nz;
        STATICS.push({x:(xa+xb)/2,z:(za+zb)/2,solid:{boxes:[[xa,y0,za,xb,y1,zb]],key:'poi'+STATICS.length,mat:'metal',deco:1}}); } },
    sbox(w,h,d,x,y,z,c,glow){ D.box(w,h,d,x,y,z,c,null,glow); D.solid(x-w/2,y,z-d/2,x+w/2,y+h,z+d/2); },          // drawn and solid
    scyl(r,h,x,y,z,c,seg){ D.cyl(r,r,h,x,y,z,c,seg); const n=Math.max(2,Math.ceil(r*2/1.2)); for(let q=0;q<n;q++){ const xa=-r+2*r*q/n, xb=-r+2*r*(q+1)/n, xm=(xa+xb)/2, hd=Math.sqrt(Math.max(0.01,r*r-xm*xm)); D.solid(x+xa,y,z-hd,x+xb,y+h,z+hd); } },
    flush(){ const out=[]; const merge=list=>{ let n=0; for(const g of list) n+=g.attributes.position.count; const P=new Float32Array(n*3), N=new Float32Array(n*3), Cc=new Float32Array(n*3); let o=0;
        for(const g of list){ P.set(g.attributes.position.array,o*3); N.set(g.attributes.normal.array,o*3); Cc.set(g.attributes.color.array,o*3); o+=g.attributes.position.count; }
        const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(P,3)); g.setAttribute('normal',new THREE.BufferAttribute(N,3)); g.setAttribute('color',new THREE.BufferAttribute(Cc,3)); return g; };
      const mk=(map,glow)=>map.forEach(list=>{ if(!list.length) return; const g=merge(list); g.computeBoundingSphere();
        const m=new THREE.Mesh(g,glow?new THREE.MeshBasicMaterial({vertexColors:true}):new THREE.MeshLambertMaterial({vertexColors:true})); m.castShadow=!glow; m.receiveShadow=!glow; m.userData.kind='poiDecor'; m.matrixAutoUpdate=false; m.updateMatrix(); scene.add(m); out.push(m); });
      mk(patches,false); mk(glows,true); patches.clear(); glows.clear(); return out; } };
  return D; }
// ground for a whole site: a flat textured pad over the levelled ground (streets stay on top of it)
const poiGroundTex=new Map();
let poiGroundN=0;
function poiGround(t,kind,shape,margin,clip){ let tex=poiGroundTex.get(kind); if(!tex){ const N=256, c=document.createElement('canvas'); c.width=c.height=N; const g=c.getContext('2d');
    if(kind==='cobble'){ g.fillStyle='#8f897d'; g.fillRect(0,0,N,N); for(let y=0;y<N;y+=16) for(let x=-(y/16%2)*10;x<N;x+=20){ const v=120+Math.random()*60; g.fillStyle=`rgb(${v},${v-4},${v-12})`; g.beginPath(); g.ellipse(x+10,y+8,9,7,0,0,7); g.fill(); } }
    else if(kind==='asphalt'){ g.fillStyle='#55575a'; g.fillRect(0,0,N,N); speckle(g,0,0,N,N,2400,'20,20,20','190,190,190'); for(let k=0;k<6;k++){ g.strokeStyle='rgba(20,20,20,.35)'; g.lineWidth=1.5; g.beginPath(); let x=Math.random()*N, y=Math.random()*N; g.moveTo(x,y); for(let s=0;s<6;s++){ x+=(Math.random()-.5)*40; y+=(Math.random()-.5)*40; g.lineTo(x,y); } g.stroke(); } }
    else if(kind==='concrete'){ g.fillStyle='#8f8e8a'; g.fillRect(0,0,N,N); speckle(g,0,0,N,N,1600,'60,60,60','255,255,255'); g.fillStyle='rgba(60,60,60,.4)'; g.fillRect(0,0,N,2); g.fillRect(0,0,2,N); }
    else { g.fillStyle='#6e5a43'; g.fillRect(0,0,N,N); speckle(g,0,0,N,N,2600,'50,36,20','170,150,115'); for(let k=0;k<40;k++){ g.fillStyle='rgba(230,200,140,.25)'; g.fillRect(Math.random()*N,Math.random()*N,3+Math.random()*10,1.5); } } // dirt and sawdust
    tex=new THREE.CanvasTexture(c); tex.wrapS=tex.wrapT=THREE.RepeatWrapping; tex.anisotropy=MAXANI; poiGroundTex.set(kind,tex); }
  const rep=kind==='cobble'?3:kind==='concrete'?5:8, ox=Math.round(t.x/CELL)*CELL, oz=Math.round(t.z/CELL)*CELL;
  // the outline: rays out from the middle of the shape until they leave it, plus a margin that wanders, so the edge is ragged and lopsided
  const rr=seeded(t.seed+kind.length*977), ph=[rr()*6.28,rr()*6.28,rr()*6.28,rr()*6.28], amp=[2.2+rr()*1.5,1.2+rr()*1,0.8+rr()*0.6,0.5];
  let cx=0, cz=0, n=0; for(let x=-45;x<=45;x+=3) for(let z=-45;z<=45;z+=3) if(shape(x,z)){ cx+=x; cz+=z; n++; } cx/=n||1; cz/=n||1;
  const N=96, ring=[]; for(let k=0;k<N;k++){ const a=k/N*Math.PI*2, dx=Math.cos(a), dz=Math.sin(a); let r=0; for(let s=0;s<70;s+=0.5) if(shape(cx+dx*s,cz+dz*s)) r=s;
    let m=margin+amp[0]*Math.sin(a*2+ph[0])+amp[1]*Math.sin(a*5+ph[1])+amp[2]*Math.sin(a*9+ph[2])+amp[3]*Math.sin(a*17+ph[3]); r+=Math.max(0.8,m);
    for(;r>2;r-=0.25){ const x=cx+dx*r, z=cz+dz*r; if(Math.hypot(ox+x-t.x,oz+z-t.z)<t.R-1.2&&(!clip||clip(x,z))) break; } ring.push([cx+dx*r,cz+dz*r]); }
  // a fan of triangles from the middle; the edge is softened by a narrow band that fades to the ground (vertex alpha)
  const pos=[cx,0,cz], uv=[(ox+cx)/rep,(oz+cz)/rep], al=[1]; for(const [x,z] of ring){ pos.push(x,0,z); uv.push((ox+x)/rep,(oz+z)/rep); al.push(1); }
  for(const [x,z] of ring){ const dx=x-cx, dz=z-cz, l=Math.hypot(dx,dz)||1, f=Math.min(1.6,l*0.06); pos.push(x+dx/l*f,0,z+dz/l*f); uv.push((ox+x+dx/l*f)/rep,(oz+z+dz/l*f)/rep); al.push(0); }
  const idx=[]; for(let k=0;k<N;k++){ const a=1+k, b=1+(k+1)%N, a2=1+N+k, b2=1+N+(k+1)%N; idx.push(0,b,a, a,b,b2, a,b2,a2); }
  const geo=new THREE.BufferGeometry(); geo.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));
  const cols=[]; for(const a of al) cols.push(1,1,1,a); geo.setAttribute('color',new THREE.Float32BufferAttribute(cols,4)); geo.setIndex(idx); geo.computeVertexNormals();
  const m=new THREE.Mesh(geo,new THREE.MeshLambertMaterial({map:tex,vertexColors:true,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-1,polygonOffsetUnits:-2}));
  m.position.set(ox,t.h+0.025,oz); m.receiveShadow=true; m.renderOrder=-10+(poiGroundN++%8); m.matrixAutoUpdate=false; m.updateMatrix(); scene.add(m);
  // no grass through it
  const inPoly=(x,z)=>{ let c=false; for(let a=0,b=N-1;a<N;b=a++){ const [xa,za]=ring[a], [xb,zb]=ring[b]; if((za>z)!==(zb>z)&&x<(xb-xa)*(z-za)/(zb-za)+xa) c=!c; } return c; };
  for(let x=-46;x<=46;x+=0.8) for(let z=-46;z<=46;z+=0.8) if(inPoly(x,z)){ const c=worldCell(ox+x,oz+z); if(c>=0) WORLD.GRASS[c]=0; }
  return m; }

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
    D.sbox(10,0.3,2.4,X(20),y0,Z(-13.8),0x8a5a32); for(const x of [15.4,24.6]) D.box(0.2,2.6,0.2,X(x),y0+0.3,Z(-12.8),0x6b4a2e); D.box(10.2,0.15,2.8,X(20),y0+2.9,Z(-13.8),0x4a2e16,[0.12,0,0]);
    D.sbox(1.2,0.5,0.5,X(22),y0+0.3,Z(-13.4),0x6b4a2e); D.box(0.6,2.2,0.6,X(23.4),y0,Z(-21.6),0x6e6458); D.box(0.9,6.6,0.9,X(24.6),y0,Z(-20),0x8f877a); D.solid(X(24.15),y0,Z(-20.45),X(25.05),y0+6.6,Z(-19.55)); // bench, stove, chimney
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
        const ex=Math.abs(co)*n*0.48+Math.abs(s)*3.6, ez=Math.abs(s)*n*0.48+Math.abs(co)*3.6; D.solid(X(x)-ex*0.85,y0,Z(z)-ez*0.85,X(x)+ex*0.85,y0+h*0.75,Z(z)+ez*0.85); };
    pile(-25,-12,0.3,5); pile(12,9,1.3,4); pile(24,22,-0.4,5); pile(-8,24,2.0,3); pile(-27,-25,0.9,3);
    for(const [x,z,yw,n] of [[10,-6,0.1,4],[16,-4,0.2,3],[6,16,-0.5,5]]){ for(let q=0;q<n;q++){ const g=new THREE.BoxGeometry(2.4,0.38,4.8); D.geo(g,q%2?0xd9b077:0xc89a62,X(x),y0+0.12+q*0.4+0.19,Z(z),[0,yw+(q%2?0.03:0),0]); }
      D.solid(X(x)-1.6,y0,Z(z)-2.6,X(x)+1.6,y0+0.12+n*0.4,Z(z)+2.6); D.box(2.6,0.12,5,X(x),y0,Z(z),0x8c6a3f,[0,yw,0]); }
    { const lx=X(-18), lz=Z(-3); D.sbox(2.6,1.4,4.4,lx,y0+0.5,lz,0xe0a326); D.sbox(2.0,1.4,1.8,lx,y0+1.9,lz+1.1,0xe0a326); D.box(1.8,1.0,0.05,lx,y0+2.2,lz+0.18,0x5ec8ff); for(const dz of [-1.4,1.4]) for(const dx of [-1.4,1.4]){ const w=new THREE.CylinderGeometry(0.55,0.55,0.4,12); w.rotateZ(Math.PI/2); D.geo(w,0x1d1f22,lx+dx,y0+0.55,lz+dz); }
      const arm=new THREE.BoxGeometry(0.4,0.4,7); arm.translate(0,0,-3.2); D.geo(arm,0xd4991c,lx,y0+3.2,lz-1,[-0.5,0,0]); const cl=new THREE.TorusGeometry(0.7,0.12,6,12,Math.PI); D.geo(cl,0x3a3d42,lx,y0+3.6,lz-7.4,[Math.PI/2,0,0]); }
    { const tx=X(-3), tz=Z(9), yw=0.6, g=new THREE.BoxGeometry(2.4,0.5,9); D.geo(g,0x3a3d42,tx,y0+1.05,tz,[0,yw,0]); const cab=new THREE.BoxGeometry(2.4,1.9,2.2); cab.translate(0,0,5.4); D.geo(cab,0x2e86c1,tx,y0+2.15,tz,[0,yw,0]);
      for(const s of [-3.2,-1.8,4.6]){ const w=new THREE.CylinderGeometry(0.55,0.55,2.5,12); w.rotateZ(Math.PI/2); w.translate(0,0,s); D.geo(w,0x1d1f22,tx,y0+0.55,tz,[0,yw,0]); }
      for(let k=0;k<5;k++){ const lg=new THREE.CylinderGeometry(0.38,0.4,8.4,10); lg.rotateX(Math.PI/2); lg.translate((k%3-1)*0.75,k<3?0:0.7,-0.2); D.geo(lg,0x8a5a32,tx,y0+1.7,tz,[0,yw,0]); }
      D.solid(tx-3.5,y0+0.6,tz-3.5,tx+3.5,y0+2.7,tz+3.5); }
    { const wx=X(22), wz=Z(12); for(const [dx,dz] of [[-2,-2],[2,-2],[-2,2],[2,2]]){ D.box(0.35,8,0.35,wx+dx,y0,wz+dz,0x6b4a2e); D.solid(wx+dx-0.18,y0,wz+dz-0.18,wx+dx+0.18,y0+8,wz+dz+0.18); }
      for(const h of [2.6,5.2]){ D.box(4.4,0.15,0.15,wx,y0+h,wz-2,0x5a3d26); D.box(4.4,0.15,0.15,wx,y0+h,wz+2,0x5a3d26); D.box(0.15,0.15,4.4,wx-2,y0+h,wz,0x5a3d26); D.box(0.15,0.15,4.4,wx+2,y0+h,wz,0x5a3d26); }
      D.sbox(5.4,0.3,5.4,wx,y0+8,wz,0x5a3d26); D.scyl(2.5,3.6,wx,y0+8.3,wz,0x9a6a3d,18); for(const h of [0.6,1.8,3]) D.cyl(2.55,2.55,0.12,wx,y0+8.3+h,wz,0x2a2a2e,18); D.cyl(0.2,2.8,1.4,wx,y0+11.9,wz,0x4a2e16,18); }
    for(let k=0;k<14;k++){ const x=-38+r()*76, z=-38+r()*76; if(!X_.inR(x,z,1)) continue; if(Math.abs(x+6)<14&&z<-12&&z>-32) continue; if(Math.hypot(x-22,z-12)<5||Math.hypot(x+19,z-15)<4||Math.hypot(x+3,z-9)<6) continue;
      const rr=0.35+r()*0.3; D.cyl(rr,rr*1.15,0.5+r()*0.4,X(x),y0,Z(z),0x8a5a32,10); D.cyl(rr*0.95,rr*0.95,0.03,X(x),y0+0.52,Z(z),0xd9b077,10); if(k%4===0){ D.box(0.06,0.7,0.06,X(x)+0.1,y0+0.6,Z(z),0x6b4a2e,[0,0,0.3]); D.box(0.04,0.2,0.32,X(x)+0.28,y0+0.95,Z(z),0x9aa3ab,[0,0,0.3]); } }
    pad.push(rectIn(-30,-15,30,26,1),rectIn(-40,-5,-28,5,2),rectIn(28,-5,40,5,2),rectIn(-4,26,4,40,2)); }
  poiGround(t,'dirt',anyIn(pad),2.8);
  return blds; };
// build a site once: its pieces (put up by buildWorld like the houses) and its decoration
function planPOI(t){ if(t.blds) return t.blds; const D=poiDecor(); t.blds=POI_BUILD[t.kind](t,D); t.decor=D.flush(); return t.blds; }
// shots stop on solid decoration (containers, machines, the rocket...): a stand-in piece takes the hit
const POI_SOLID={key:'_deco',mat:'metal',type:'wall',deco:1,group:{position:new THREE.Vector3()}};
function decoShot(o,d,range,nearT){ let best=null; const ps=new Set(), n=Math.min(90,Math.ceil(range/4)); for(let k=0;k<=n;k++){ const t=k*4; staticsInto(ps,o.x+d.x*t,o.z+d.z*t,2.5); }
  ps.forEach(s=>{ if(!s.deco) return; for(const b of s.boxes){ const tb=rayBox(o,d,b); if(tb>=nearT&&tb<=range&&(!best||tb<best)) best=tb; } }); return best; }

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
    solid(x0,y0,z0,x1,y1,z1,kp){ const nx=Math.max(1,Math.ceil((x1-x0)/2.4)), nz=Math.max(1,Math.ceil((z1-z0)/2.4));
      for(let a=0;a<nx;a++) for(let b=0;b<nz;b++){ const xa=x0+(x1-x0)*a/nx, xb=x0+(x1-x0)*(a+1)/nx, za=z0+(z1-z0)*b/nz, zb=z0+(z1-z0)*(b+1)/nz;
        STATICS.push({x:(xa+xb)/2,z:(za+zb)/2,solid:{boxes:[[xa,y0,za,xb,y1,zb]],key:(kp||'poi')+STATICS.length,mat:'metal',deco:1}}); } },
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


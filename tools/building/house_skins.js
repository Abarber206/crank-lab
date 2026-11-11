/* ---------- house skins ----------
   Town houses are real build pieces underneath: they keep wood, brick or metal for their health, their cracks and what
   the pickaxe farms from them. But they're dressed as houses: painted lap siding, stucco or modern board panels
   outside, with window and door trim and shutters; painted walls with a baseboard inside; hardwood floors under white
   ceilings; and asphalt shingle or clay tile roofs. Wall textures carry a paint mask in their alpha (paint 1, trim 0.5),
   so one texture serves every paint colour. */
const HOUSE_STYLE={wood:'siding',brick:'stucco',metal:'panel'};
const HOUSE_PAINT={siding:[0xf3ead6,0xb7d0e2,0xc4d6b0,0xf1db96,0xeceae5,0xb9645a],stucco:[0xf2e4cc,0xf0cba8,0xe7e1d3,0xdcc59e],panel:[0x97a0a8,0x56606b,0x35506a,0xbdb5a6]};
const ROOF_COL={wood:[0x55595f,0x6b5444,0x4c5a6b,0x4f6150],brick:[0xc0644a,0xa9583f,0x8f6a52,0xb98a6a]};
function houseTex(S,paint,bump){
  const a=document.createElement('canvas'), h=document.createElement('canvas'), k=document.createElement('canvas'); a.width=a.height=h.width=h.height=k.width=k.height=S;
  const g=a.getContext('2d'), hg=h.getContext('2d'), mg=k.getContext('2d'); hg.fillStyle=gv(128); hg.fillRect(0,0,S,S); mg.fillStyle='#fff'; mg.fillRect(0,0,S,S);
  paint(g,hg,mg,S);
  const id=g.getImageData(0,0,S,S), md=mg.getImageData(0,0,S,S).data; for(let i=0;i<S*S;i++) id.data[i*4+3]=128+Math.round(md[i*4]/255*127);
  g.putImageData(id,0,0);
  const map=new THREE.CanvasTexture(a); map.anisotropy=MAXANI; return {map,normal:normalFromHeight(hg,S,bump||3,1)};
}
// a trim board: its own colour (never painted over), raised a little
function trimRect(g,hg,mg,x,y,w,h,col,ht){ g.fillStyle=col; g.fillRect(x,y,w,h); hg.fillStyle=gv(ht||200); hg.fillRect(x,y,w,h); mg.fillStyle='#000'; mg.fillRect(x,y,w,h);
  g.fillStyle='rgba(255,255,255,.18)'; g.fillRect(x,y,w,2); g.fillStyle='rgba(0,0,0,.16)'; g.fillRect(x,y+h-2,w,2); }
// the wall faces: plain, with a window (the middle tile is open) or a door (middle and bottom-middle open)
function sidingField(g,hg,S){ const row=21; g.fillStyle='#f0efea'; g.fillRect(0,0,S,S);
  for(let y=0;y<S;y+=row){ g.fillStyle='rgba(30,30,30,.32)'; g.fillRect(0,y,S,3); g.fillStyle='rgba(255,255,255,.12)'; g.fillRect(0,y+3,S,3);
    const hr=hg.createLinearGradient(0,y,0,y+row); hr.addColorStop(0,gv(105)); hr.addColorStop(1,gv(175)); hg.fillStyle=hr; hg.fillRect(0,y,S,row);
    for(let x=Math.random()*200;x<S;x+=180+Math.random()*160){ g.fillStyle='rgba(30,30,30,.22)'; g.fillRect(x,y,2,row); hg.fillStyle=gv(100); hg.fillRect(x,y,2,row); } } // butt joints
  speckle(g,0,0,S,S,500,'60,60,60','255,255,255'); }
function stuccoField(g,hg,S){ g.fillStyle='#ecebe6'; g.fillRect(0,0,S,S);
  for(let i=0;i<2600;i++){ const x=Math.random()*S, y=Math.random()*S, r=1+Math.random()*3, v=Math.random(); g.fillStyle=v<.5?'rgba(80,70,60,.07)':'rgba(255,255,255,.12)'; g.beginPath(); g.arc(x,y,r,0,7); g.fill(); hg.fillStyle=gv(v<.5?110:150); hg.beginPath(); hg.arc(x,y,r,0,7); hg.fill(); }
  for(let i=0;i<10;i++){ const x=Math.random()*S, y=Math.random()*S, r=30+Math.random()*60, gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0,'rgba(120,100,80,.06)'); gr.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=gr; g.fillRect(x-r,y-r,r*2,r*2); } }
function panelField(g,hg,S){ const w=S/10; g.fillStyle='#e9eaeb'; g.fillRect(0,0,S,S);
  for(let i=0;i<10;i++){ const x=i*w; g.fillStyle=i%2?'rgba(0,0,0,.03)':'rgba(255,255,255,.04)'; g.fillRect(x,0,w,S);
    g.fillStyle='rgba(255,255,255,.35)'; g.fillRect(x+w-9,0,3,S); g.fillStyle='rgba(20,20,20,.35)'; g.fillRect(x+w-3,0,3,S); hg.fillStyle=gv(190); hg.fillRect(x+w-9,0,9,S); } // battens
  speckle(g,0,0,S,S,300,'60,60,60','255,255,255'); }
const T3=1/3;
function houseWallTex(style,kind){
  return houseTex(512,(g,hg,mg,S)=>{
    const a=S*T3, b=S*2*T3, white=style==='panel'?'#2a2d31':'#f6f4ee', trimH=style==='panel'?150:205;
    (style==='siding'?sidingField:style==='stucco'?stuccoField:panelField)(g,hg,S);
    // top band and base
    if(style==='siding'){ trimRect(g,hg,mg,0,0,S,16,white,210); trimRect(g,hg,mg,0,S-20,S,20,'#e9e6de',215); }
    else if(style==='stucco'){ trimRect(g,hg,mg,0,0,S,14,'#efe9dc',205);
      trimRect(g,hg,mg,0,S-58,S,58,'#8f8a82',185); g.strokeStyle='rgba(40,36,32,.55)'; g.lineWidth=2; hg.strokeStyle=gv(110); hg.lineWidth=3; // a stone plinth
      for(let r=0;r<2;r++){ const y=S-58+r*29; g.beginPath(); g.moveTo(0,y); g.lineTo(S,y); g.stroke(); hg.beginPath(); hg.moveTo(0,y); hg.lineTo(S,y); hg.stroke();
        for(let x=(r?40:0);x<S;x+=80){ g.beginPath(); g.moveTo(x,y); g.lineTo(x,y+29); g.stroke(); hg.beginPath(); hg.moveTo(x,y); hg.lineTo(x,y+29); hg.stroke(); } }
      speckle(g,0,S-58,S,58,220,'30,30,30','255,255,255'); }
    else { trimRect(g,hg,mg,0,0,S,10,white,150); trimRect(g,hg,mg,0,S-24,S,24,'#5d6066',170); }
    if(kind==='win'){ const c=style==='panel'?10:17;
      trimRect(g,hg,mg,a-c,a-c,b-a+2*c,c,white,trimH); trimRect(g,hg,mg,a-c,b,b-a+2*c,c,white,trimH); trimRect(g,hg,mg,a-c,a,c,b-a,white,trimH); trimRect(g,hg,mg,b,a,c,b-a,white,trimH);
      if(style==='siding'){ trimRect(g,hg,mg,a-c-8,a-c-12,b-a+2*c+16,12,white,225); // head cap
        trimRect(g,hg,mg,a-c-10,b+c,b-a+2*c+20,10,'#e8e4da',225);  // sill
        for(const x of [a-c-62,b+c+8]){ trimRect(g,hg,mg,x,a-4,54,b-a+8,'#2f4b3c',185); // shutters with louvres
          for(let y=a+6;y<b-4;y+=9){ g.fillStyle='rgba(0,0,0,.35)'; g.fillRect(x+6,y,42,2); g.fillStyle='rgba(255,255,255,.12)'; g.fillRect(x+6,y+2,42,2); hg.fillStyle=gv(160); hg.fillRect(x+6,y,42,3); } } }
      else if(style==='stucco'){ trimRect(g,hg,mg,a-c-6,b+c,b-a+2*c+12,14,'#b9b2a6',225); // stone sill
        for(const x of [a-c-50,b+c+6]){ trimRect(g,hg,mg,x,a-2,44,b-a+4,'#6b4a33',180); for(let y=a+8;y<b;y+=12){ g.fillStyle='rgba(0,0,0,.3)'; g.fillRect(x+5,y,34,2); } } } }
    if(kind==='door'){ const c=style==='panel'?12:20;
      trimRect(g,hg,mg,a-c,a-c,b-a+2*c,c,white,trimH); trimRect(g,hg,mg,a-c,a,c,S-a,white,trimH); trimRect(g,hg,mg,b,a,c,S-a,white,trimH);
      if(style!=='panel'){ trimRect(g,hg,mg,a-c-10,a-c-14,b-a+2*c+20,14,white,225); } // a little cornice over the door
      const lx=b+c+18, ly=a+40; trimRect(g,hg,mg,lx,ly,16,26,'#2b2b2b',215); g.fillStyle='#ffe7a3'; g.fillRect(lx+4,ly+5,8,14); mg.fillStyle='#000'; mg.fillRect(lx+4,ly+5,8,14); } // porch lamp
  },3);
}
const houseTexCache=new Map();
function houseWallSet(style,kind){ const k=style+kind; let t=houseTexCache.get(k); if(!t){ t=houseWallTex(style,kind); houseTexCache.set(k,t); } return t; }
const hardwood=texSet(512,(g,hg,S)=>{ const n=8, h=S/n, tones=['#b9844f','#a87444','#c18d58','#9f6c3f','#b47f4b','#ad7a48','#c69460','#a3713f'];
  for(let i=0;i<n;i++){ woodGrain(g,hg,0,i*h,S,h,false,tones[i]); g.fillStyle='rgba(40,20,6,.7)'; g.fillRect(0,i*h,S,2); hg.fillStyle=gv(70); hg.fillRect(0,i*h,S,2);
    const j=(i*197)%S; g.fillRect(j,i*h,2,h); hg.fillRect(j,i*h,2,h); }
  g.fillStyle='rgba(255,230,190,.08)'; g.fillRect(0,0,S,S); },2);
function roofTex(kind){ const t=houseTex(512,(g,hg,mg,S)=>{
    if(kind==='wood'){ const row=26, tab=S/8; g.fillStyle='#d8d8d8'; g.fillRect(0,0,S,S); // asphalt shingles: tabs offset every other row
      for(let r=0;r*row<S;r++){ const y=r*row, off=(r%2)*tab/2;
        for(let x=-tab;x<S+tab;x+=tab){ const v=200+Math.random()*45; g.fillStyle=gv(v); g.fillRect(x+off,y,tab-3,row); speckle(g,x+off,y,tab,row,30,'0,0,0','255,255,255'); }
        g.fillStyle='rgba(0,0,0,.5)'; g.fillRect(0,y,S,4); hg.fillStyle=gv(90); hg.fillRect(0,y,S,4);
        for(let x=off;x<S;x+=tab){ g.fillStyle='rgba(0,0,0,.4)'; g.fillRect(x-3,y,3,row); } } }
    else { const row=32, w=S/10; g.fillStyle='#e8e2dc'; g.fillRect(0,0,S,S); // clay barrel tiles
      for(let r=0;r*row<S;r++){ const y=r*row;
        for(let i=0;i<10;i++){ const x=i*w+(r%2)*w/2, gr=g.createLinearGradient(x,0,x+w,0); gr.addColorStop(0,'rgba(0,0,0,.28)'); gr.addColorStop(.45,'rgba(255,255,255,.22)'); gr.addColorStop(1,'rgba(0,0,0,.3)');
          g.fillStyle=gr; g.fillRect(x,y,w,row); g.fillRect(x-S,y,w,row); }
        g.fillStyle='rgba(40,20,10,.45)'; g.fillRect(0,y,S,4); hg.fillStyle=gv(80); hg.fillRect(0,y,S,4); } }
  },2); t.map.wrapS=t.map.wrapT=THREE.RepeatWrapping; return t; }
const roofTexs={wood:roofTex('wood'),brick:roofTex('brick')};
// one shader tweak for every house material: paint colour through the mask, painted walls inside, white ceilings, roofs
// that follow the slope (rows run along the eaves) with bare boards underneath
function houseOBC(sh){
  // only wall geometry carries the 'inside' flag, so only the wall shader reads it (a missing attribute breaks the draw)
  sh.vertexShader='#ifdef HOUSE_PAINT\nattribute float inside;\n#endif\n#ifdef HOUSE_VPAINT\nattribute vec3 paint;\nvarying vec3 vPaint;\n#endif\nvarying float vIn;\nvarying vec3 vON;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\n  vON=objectNormal;\n#ifdef HOUSE_VPAINT\n  vPaint=paint;\n#endif\n#ifdef HOUSE_PAINT\n  vIn=inside;\n#else\n  vIn=0.0;\n#endif');
  sh.fragmentShader='#ifdef HOUSE_VPAINT\nvarying vec3 vPaint;\n#define PCOL vPaint\n#else\n#define PCOL diffuse\n#endif\nvarying float vIn;\nvarying vec3 vON;\n'+sh.fragmentShader
    .replace('#include <map_fragment>',`#ifdef HOUSE_ROOF
  vec2 ruv=abs(vON.x)>abs(vON.z)?vec2(vUv.y,vUv.x*sign(vON.x)):vec2(vUv.x,vUv.y*sign(vON.z));
  vec4 texelColor=mapTexelToLinear(texture2D(map,ruv*1.5)); diffuseColor*=texelColor;\n#ifdef HOUSE_VPAINT\n  diffuseColor.rgb*=vPaint;\n#endif
  if(!gl_FrontFacing) diffuseColor.rgb=vec3(0.56,0.45,0.33);
#else
#include <map_fragment>
#endif
#ifdef HOUSE_PAINT
  { float pa=clamp((texelColor.a-0.5)*2.0,0.0,1.0); diffuseColor=vec4(texelColor.rgb*mix(vec3(1.0),PCOL,pa),opacity);
    if(vIn>0.5) diffuseColor.rgb=mix(vec3(0.85,0.81,0.73)*(0.96+0.06*texelColor.g),vec3(0.95,0.94,0.9),step(vUv.y,0.045)); }
#endif
#ifdef HOUSE_CEIL
  if(vON.y<-0.5) diffuseColor.rgb=vec3(0.93,0.92,0.88);
#endif`)
    .replace('#include <normal_fragment_maps>','if(vIn<0.5){\n#include <normal_fragment_maps>\n}')
    // rooms aren't caves: painted walls and ceilings inside give back a little light of their own
    .replace('#include <emissivemap_fragment>','#include <emissivemap_fragment>\n#ifdef HOUSE_PAINT\n  if(vIn>0.5) totalEmissiveRadiance+=diffuseColor.rgb*0.32;\n#endif\n#ifdef HOUSE_CEIL\n  totalEmissiveRadiance+=diffuseColor.rgb*(vON.y<-0.5?0.4:0.08);\n#endif\n#ifdef HOUSE_ROOF\n  if(!gl_FrontFacing) totalEmissiveRadiance+=diffuseColor.rgb*0.45;\n#endif');
}
const houseMatCache=new Map();
function houseMat(key,make,def,batchKey){ let m=houseMatCache.get(key); if(!m){ m=make(); m.defines=Object.assign({},m.defines||{},{[def]:''}); m.onBeforeCompile=houseOBC; houseMatCache.set(key,m);
    if(batchKey){ let b=houseMatCache.get('batch:'+batchKey); if(!b){ b=m.clone(); b.color.setRGB(1,1,1); b.defines=Object.assign({},m.defines,{HOUSE_VPAINT:''}); b.onBeforeCompile=houseOBC; houseMatCache.set('batch:'+batchKey,b); } m.userData.batch=b; } }
  return m; }
const wallKind=mask=>!(mask&2)?'door':!(mask&16)?'win':'plain';
function houseSkin(p){
  const s=p.skin;
  return {
    wall:houseMat('w'+s.style+wallKind(p.mask==null?511:p.mask)+s.paint,()=>{ const t=houseWallSet(s.style,wallKind(p.mask==null?511:p.mask)); return new THREE.MeshPhongMaterial({map:t.map,normalMap:t.normal,color:HOUSE_PAINT[s.style][s.paint],shininess:s.style==='panel'?18:6,specular:0x111111}); },'HOUSE_PAINT','w'+s.style+wallKind(p.mask==null?511:p.mask)),
    floor:houseMat('floor',()=>new THREE.MeshPhongMaterial({map:hardwood.map,normalMap:hardwood.normal,shininess:22,specular:0x2a2016,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1}),'HOUSE_CEIL'),
    tread:houseMat('tread',()=>new THREE.MeshPhongMaterial({map:hardwood.map,normalMap:hardwood.normal,shininess:22,specular:0x2a2016}),'HOUSE_CEIL'),
    beam:houseMat('trim'+(s.style==='panel'?'d':'w'),()=>new THREE.MeshPhongMaterial({color:s.style==='panel'?0x2c2f34:0xf2efe8,shininess:10,specular:0x111111}),'HOUSE_TRIM'),
    cone:houseMat('roof'+p.mat+s.roof,()=>{ const t=roofTexs[p.mat==='brick'?'brick':'wood']; return new THREE.MeshPhongMaterial({map:t.map,color:ROOF_COL[p.mat==='brick'?'brick':'wood'][s.roof],shininess:4,specular:0x080808,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:1,polygonOffsetUnits:1}); },'HOUSE_ROOF','roof'+(p.mat==='brick'?'brick':'wood'))
  };
}
// wall geometry with an 'inside' flag on the faces that look into the house
const houseGeoCache=new Map();
function houseWallGeo(axis,mask,out){ const key=axis+mask+'_'+out; let g=houseGeoCache.get(key); if(g) return g;
  g=wallGeo(axis,mask).clone(); const n=g.attributes.normal, a=new Float32Array(n.count);
  for(let i=0;i<n.count;i++){ const c=axis==='x'?n.getX(i):n.getZ(i); a[i]=c*out<-0.5?1:0; }
  g.setAttribute('inside',new THREE.BufferAttribute(a,1)); houseGeoCache.set(key,g); return g; }
// closed gable ends: a triangle of siding under each end of the roof (decoration on the roof piece, which owns it)
const gableCache=new Map();
function gableGeo(mask,side,out){ const key=mask+side+out; let g=gableCache.get(key); if(g) return g;
  const C=CELL/2, bit=b=>(mask>>b&1)?LVL:0;
  // the two corners along this edge (bits from the cone corner layout) and where the edge runs
  const ed={w:[0,2,'z',-C],e:[1,3,'z',C],n:[0,1,'x',-C],s:[2,3,'x',C]}[side], h0=bit(ed[0]), h1=bit(ed[1]);
  if(h0===h1) return null;
  const sh=new THREE.Shape([new THREE.Vector2(-C,0),new THREE.Vector2(C,0),new THREE.Vector2(h0?-C:C,LVL)]);
  g=new THREE.ExtrudeGeometry(sh,{depth:WT,bevelEnabled:false}); g.translate(0,0,-WT/2); // shape in the x/y plane, WT thick along z
  if(ed[2]==='z') g.rotateY(-Math.PI/2); // the edge runs along z: local x becomes world z
  g.translate(ed[2]==='z'?ed[3]:0,0,ed[2]==='z'?0:ed[3]);
  g=g.toNonIndexed(); const pa=g.attributes.position, na=g.attributes.normal, uv=g.attributes.uv, ins=new Float32Array(pa.count);
  for(let i=0;i<pa.count;i++){ const along=ed[2]==='z'?pa.getZ(i):pa.getX(i), nn=ed[2]==='z'?na.getX(i):na.getZ(i);
    uv.setXY(i,(along+C)/CELL,pa.getY(i)/LVL); ins[i]=nn*out<-0.5?1:0; }
  g.setAttribute('inside',new THREE.BufferAttribute(ins,1)); gableCache.set(key,g); return g; }

# ---------- 36. house stair handrails are solid; doors fill their frames ----------
# the handrail up the open side of the stairs is a real barrier now (stepped boxes following the slope, no gaps)
rep("  // handrail up the open side of the steps\n","  // the handrail is solid: stepped boxes up the open side, overlapping so there's never a gap\n  for(let k=0;k<N;k++){ const s0=S1-(k+1)*TR-0.02, s1=S1-k*TR+0.02, top=(k+1)*RISE; stairs.boxes.push(box(Math.max(LAND-0.05,s0),Math.min(S1,s1),SW-0.02,SW+0.08,top,top+1.0)); }\n  // handrail up the open side of the steps\n")
# doors: the panel fills the opening (no see-through gaps) and a frame is fitted round it
rep("function doorGeo(X){ const key=X?'x':'z'; if(doorGeo[key]) return doorGeo[key]; const tw=CELL/3-0.08, h=2*LVL/3-0.06, th=0.09;\n  const panel=X?new THREE.BoxGeometry(th,h,tw):new THREE.BoxGeometry(tw,h,th); X?panel.translate(0,h/2+0.02,tw/2+0.04):panel.translate(tw/2+0.04,h/2+0.02,0);",
    "function doorGeo(X){ const key=X?'x':'z'; if(doorGeo[key]) return doorGeo[key]; const tw=CELL/3-0.02, h=2*LVL/3-0.015, th=0.09;\n  const panel=X?new THREE.BoxGeometry(th,h,tw):new THREE.BoxGeometry(tw,h,th); X?panel.translate(0,h/2+0.005,tw/2+0.01):panel.translate(tw/2+0.01,h/2+0.005,0);")
rep("    p.doors[c]={open:false,ang:0,to:0,pv}; }\n  doorPieces.add(p); }","""    p.doors[c]={open:false,ang:0,to:0,pv};
    // a frame round the opening: two jambs and a head, standing a little proud of the wall on both faces
    const fm=p.skin?houseSkin(p).beam:doorFrameMat(), dh=2*LVL/3, d0=-CELL/2+c*tw, fd=WT+0.07, fw=0.09;
    for(const e of [d0,d0+tw]){ const jb=new THREE.Mesh(X?new THREE.BoxGeometry(fd,dh+fw,fw):new THREE.BoxGeometry(fw,dh+fw,fd),fm); X?jb.position.set(0,-LVL/2+(dh+fw)/2,e):jb.position.set(e,-LVL/2+(dh+fw)/2,0); jb.castShadow=jb.receiveShadow=true; g.add(jb); }
    const hd=new THREE.Mesh(X?new THREE.BoxGeometry(fd,fw,tw+fw):new THREE.BoxGeometry(tw+fw,fw,fd),fm); X?hd.position.set(0,-LVL/2+dh+fw/2-0.01,d0+tw/2):hd.position.set(d0+tw/2,-LVL/2+dh+fw/2-0.01,0); hd.castShadow=hd.receiveShadow=true; g.add(hd); }
  doorPieces.add(p); }
let _dfm=null; function doorFrameMat(){ return _dfm||(_dfm=new THREE.MeshPhongMaterial({color:0x5a3d26,shininess:12})); }""")

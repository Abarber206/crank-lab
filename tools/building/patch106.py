# ---------- 106. rarer top loot (epics and legendaries are a find now) and a road sign at each way into a town instead
# of the name popping up on screen ----------
rep("const LOOT_RW={common:30,uncommon:28,rare:22,epic:13,legendary:7}","const LOOT_RW={common:46,uncommon:30,rare:16,epic:6,legendary:2}")
rep("  const id=lootWeapon(1.25), out=[[id,WEAPONS[id].mag],ammoFor(id)], r=Math.random();","  const id=lootWeapon(1.15), out=[[id,WEAPONS[id].mag],ammoFor(id)], r=Math.random();")
rep("const id=lootWeapon(brute?1.6:1); return [id,WEAPONS[id].mag]; };","const id=lootWeapon(brute?1.4:1); return [id,WEAPONS[id].mag]; };")
rep("if(t!==P.town){ P.town=t; if(t&&playing) toast(t.name); }","if(t!==P.town){ P.town=t; }")
rep("function buildRails(){","""/* Roadside furniture: a direction sign a little way out on each road into a town, speed limits along the open road,
   warnings before sharp bends, stop signs at the town crossroads and street lamps. A handful of merged meshes. */
var SIGNS=[];
function buildSigns(){ const grey=[], dark=[], pale=[], faces=new Map(), placed=[], roads=WORLD.roads;
  const face=(key,w,h,draw)=>{ let f=faces.get(key); if(!f){ const c=document.createElement('canvas'); c.width=w; c.height=h; draw(c.getContext('2d'),w,h); const tex=new THREE.CanvasTexture(c); tex.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy()); f={tex,geos:[],key}; faces.set(key,f); } return f; };
  const solid=(x,y,z,h)=>STATICS.push({x,z,solid:{boxes:[[x-0.1,y-0.3,z-0.1,x+0.1,y+h,z+0.1]],key:'sign'+STATICS.length}});
  const post=(list,x,y,z,h,yaw,w)=>{ const g=new THREE.BoxGeometry(w||0.09,h,w||0.09); g.rotateY(yaw); g.translate(x,y+h/2,z); list.push(g); solid(x,y,z,h); };
  const board=(f,geo,x,y,z,yaw)=>{ SIGNS.push([f.key,x,z,yaw]); const back=geo.clone(); back.rotateY(Math.PI); const sx=Math.sin(yaw), sz=Math.cos(yaw);
    geo.rotateY(yaw); geo.translate(x+sx*0.062,y,z+sz*0.062); f.geos.push(geo); back.rotateY(yaw); back.translate(x+sx*0.056,y,z+sz*0.056); grey.push(back); };
  // a spot on the right-hand verge for traffic heading along the road in direction dir, facing that traffic
  const spot=(k,q,dir,off,gap)=>{ const rd=roads[k], p=rd.pts, n=p.length; if(q<2||q>n-3||rd.skip[q]) return null; let hx=(p[q+1][0]-p[q-1][0])*dir, hz=(p[q+1][1]-p[q-1][1])*dir; const hl=Math.hypot(hx,hz)||1; hx/=hl; hz/=hl;
    const x=SPAWN[0]+p[q][0]-hz*off, z=SPAWN[2]+p[q][1]+hx*off, y=terrainH(x,z); if(Math.abs(y-p[q][2])>1||nearOther(k,SPAWN[0]+p[q][0],SPAWN[2]+p[q][1])<14) return null;
    if(placed.some(s=>Math.hypot(s[0]-x,s[1]-z)<gap)||propsNear(x,z,[],1).some(o=>Math.hypot(o.x-x,o.z-z)<3.2)) return null; placed.push([x,z]); return {x,y,z,yaw:Math.atan2(-hx,-hz),hx,hz}; };
  const rrect=(g,x,y,w,h,r)=>{ g.beginPath(); g.moveTo(x+r,y); g.arcTo(x+w,y,x+w,y+h,r); g.arcTo(x+w,y+h,x,y+h,r); g.arcTo(x,y+h,x,y,r); g.arcTo(x,y,x+w,y,r); g.closePath(); };
  const F='system-ui,-apple-system,Segoe UI,sans-serif';
  // ---- towns: one sign per road in, some 80 m before the first houses, with the distance to go
  roads.forEach((rd,k)=>{ if(rd.street) return; const p=rd.pts, n=p.length;
    for(const end of [0,1]){ const e=p[end?n-1:0], ex=SPAWN[0]+e[0], ez=SPAWN[2]+e[1], t=TOWNS.find(t=>t.ends.some(a=>Math.hypot(a[0]-ex,a[1]-ez)<3)); if(!t) continue;
      let arc=0, q=end?n-1:0; const st=end?-1:1, want=Math.min(82,n*0.6); while(q+st>=0&&q+st<n&&arc<want){ arc+=Math.hypot(p[q+st][0]-p[q][0],p[q+st][1]-p[q][1]); q+=st; }
      for(let tr=0;tr<10;tr++,q+=st*3,arc+=6){ const s=spot(k,q,-st,ROAD_HW+2.7,20); if(!s) continue;
        const dist=Math.round((arc+t.streetL)/10)*10, f=face('town'+t.name+dist,720,260,(g,w,h)=>{ g.fillStyle='#f4f4f0'; g.fillRect(0,0,w,h); g.fillStyle='#1d6a44'; rrect(g,10,10,w-20,h-20,24); g.fill();
          g.fillStyle='#f4f4f0'; g.textAlign='center'; g.textBaseline='middle'; let fs=104; g.font='800 '+fs+'px '+F; while(g.measureText(t.name).width>w-90&&fs>40){ fs-=4; g.font='800 '+fs+'px '+F; } g.fillText(t.name,w/2,94);
          g.font='700 58px '+F; g.fillText(dist+' m',w/2+36,190); g.lineWidth=13; g.strokeStyle='#f4f4f0'; g.lineCap='round'; g.lineJoin='round'; const ax=w/2-g.measureText(dist+' m').width/2-26; g.beginPath(); g.moveTo(ax,214); g.lineTo(ax,166); g.moveTo(ax-22,186); g.lineTo(ax,162); g.lineTo(ax+22,186); g.stroke(); });
        board(f,new THREE.PlaneGeometry(3.5,1.26),s.x,s.y+2.85,s.z,s.yaw); const cx=Math.cos(s.yaw), cz=-Math.sin(s.yaw); for(const u of [-1.25,1.25]) post(grey,s.x+cx*u,Math.min(s.y,terrainH(s.x+cx*u,s.z+cz*u)),s.z+cz*u,3.55,s.yaw,0.1); break; } } });
  // ---- warnings before sharp bends, both ways
  const bendF=d=>face('bend'+d,256,256,(g)=>{ g.fillStyle='#f6c61a'; g.fillRect(0,0,256,256); g.strokeStyle='#15171a'; g.lineWidth=9; g.strokeRect(13,13,230,230); g.translate(128,128); g.rotate(Math.PI/4); if(d<0) g.scale(-1,1);
    g.lineWidth=20; g.lineCap='butt'; g.lineJoin='round'; g.beginPath(); g.moveTo(-14,70); g.lineTo(-14,6); g.quadraticCurveTo(-14,-30,24,-40); g.stroke(); g.fillStyle='#15171a'; g.beginPath(); g.moveTo(58,-50); g.lineTo(14,-74); g.lineTo(22,-10); g.closePath(); g.fill(); });
  roads.forEach((rd,k)=>{ if(rd.street) return; const p=rd.pts, n=p.length, tan=(q,dir)=>{ const a=p[Math.max(0,q-1)], b=p[Math.min(n-1,q+1)], l=Math.hypot(b[0]-a[0],b[1]-a[1])||1; return [(b[0]-a[0])/l*dir,(b[1]-a[1])/l*dir]; };
    for(const dir of [1,-1]){ let last=-999; for(let i=16;i<n-28;i++){ const q=dir>0?i:n-1-i, h1=tan(q,dir), h2=tan(q+12*dir,dir), cr=h1[0]*h2[1]-h1[1]*h2[0], dt=h1[0]*h2[0]+h1[1]*h2[1], ang=Math.atan2(cr,dt);
      if(Math.abs(ang)<0.72||i-last<45) continue; const x=SPAWN[0]+p[q][0], z=SPAWN[2]+p[q][1]; if(townAt(x,z,30)) continue;
      const s=spot(k,q-12*dir,dir,ROAD_HW+1.9,24); if(!s) continue; last=i; const g=new THREE.PlaneGeometry(0.86,0.86); g.rotateZ(Math.PI/4); board(bendF(ang>0?1:-1),g,s.x,s.y+2.2,s.z,s.yaw); post(grey,s.x,s.y,s.z,2.2,s.yaw); } } });
  // ---- speed limits along the open road
  const spdF=face('speed',256,320,(g)=>{ g.fillStyle='#f6f6f2'; g.fillRect(0,0,256,320); g.strokeStyle='#15171a'; g.lineWidth=10; rrect(g,12,12,232,296,18); g.stroke(); g.fillStyle='#15171a'; g.textAlign='center'; g.textBaseline='middle';
    g.font='800 46px '+F; g.fillText('SPEED',128,62); g.fillText('LIMIT',128,112); g.font='800 150px '+F; g.fillText('40',128,220); });
  roads.forEach((rd,k)=>{ if(rd.street) return; const p=rd.pts, n=p.length; let arc=0, next=130, dir=k%2?1:-1;
    for(let q=1;q<n-3;q++){ arc+=Math.hypot(p[q][0]-p[q-1][0],p[q][1]-p[q-1][1]); if(arc<next) continue; const x=SPAWN[0]+p[q][0], z=SPAWN[2]+p[q][1]; if(townAt(x,z,55)){ next=arc+20; continue; }
      const s=spot(k,q,dir,ROAD_HW+1.9,30); if(!s){ next=arc+8; continue; } board(spdF,new THREE.PlaneGeometry(0.74,0.92),s.x,s.y+2.3,s.z,s.yaw); post(grey,s.x,s.y,s.z,2.75,s.yaw); next=arc+270; dir=-dir; } });
  // ---- towns: a stop sign on each way into the crossroads, and street lamps
  const stopF=face('stop',256,256,(g)=>{ g.fillStyle='#c4262b'; g.fillRect(0,0,256,256); g.strokeStyle='#f6f6f2'; g.lineWidth=10; g.beginPath(); for(let a=0;a<8;a++){ const x=128+Math.cos(a*Math.PI/4)*108, y=128+Math.sin(a*Math.PI/4)*108; a?g.lineTo(x,y):g.moveTo(x,y); } g.closePath(); g.stroke();
    g.translate(128,128); g.rotate(Math.PI/8); g.fillStyle='#f6f6f2'; g.textAlign='center'; g.textBaseline='middle'; g.font='800 74px '+F; g.fillText('STOP',0,4); });
  for(const t of TOWNS){ townBulbs(t);
    for(const [ox,oz] of [[1,0],[-1,0],[0,1],[0,-1]]){ const hx=-ox, hz=-oz, x=t.x+ox*(ROAD_HW+2.3)-hz*(ROAD_HW+0.6), z=t.z+oz*(ROAD_HW+2.3)+hx*(ROAD_HW+0.6), yaw=Math.atan2(ox,oz);
      const g=new THREE.CircleGeometry(0.42,8); g.rotateZ(Math.PI/8); board(stopF,g,x,t.h+2.35,z,yaw); post(grey,x,t.h,z,2.5,yaw); }
    for(const X of [true,false]) for(const s0 of [-29,-15,15,29]){ const sd=(s0>0)!==(Math.abs(s0)>20)?1:-1, ac=sd*(ROAD_HW+WALK_W+0.4); let s=s0, ok=false;
      for(let tr=0;tr<5&&!ok;tr++,s+=Math.sign(s0)*-2.3){ const x=X?t.x+s:t.x+ac, z=X?t.z+ac:t.z+s; ok=!SIDEWALKS.some(([a,b])=>X?(Math.abs(a[0]-b[0])<0.2&&Math.abs(a[0]-x)<2.2&&z>Math.min(a[1],b[1])-0.6&&z<Math.max(a[1],b[1])+0.6):(Math.abs(a[1]-b[1])<0.2&&Math.abs(a[1]-z)<2.2&&x>Math.min(a[0],b[0])-0.6&&x<Math.max(a[0],b[0])+0.6));
        if(!ok) continue; const ix=X?0:-sd, iz=X?-sd:0; // toward the street
        post(dark,x,t.h,z,4.9,0,0.13); const b0=new THREE.BoxGeometry(0.3,0.5,0.3); b0.translate(x,t.h+0.25,z); dark.push(b0);
        const arm=new THREE.BoxGeometry(X?0.08:1.5,0.08,X?1.5:0.08); arm.translate(x+ix*0.7,t.h+4.85,z+iz*0.7); dark.push(arm);
        const hd=new THREE.BoxGeometry(X?0.3:0.62,0.13,X?0.62:0.3); hd.translate(x+ix*1.5,t.h+4.8,z+iz*1.5); dark.push(hd); const gl=new THREE.BoxGeometry(X?0.22:0.5,0.05,X?0.5:0.22); gl.translate(x+ix*1.5,t.h+4.715,z+iz*1.5); pale.push(gl); } } }
  const add=(list,mat)=>{ if(!list.length) return; const g=mergeGeos(list); g.computeBoundingSphere(); const m=new THREE.Mesh(g,mat); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; scene.add(m); };
  add(grey,new THREE.MeshLambertMaterial({color:0x8d939a})); add(dark,new THREE.MeshLambertMaterial({color:0x2b3036})); add(pale,new THREE.MeshBasicMaterial({color:0xfff3cf}));
  faces.forEach(f=>add(f.geos,new THREE.MeshLambertMaterial({map:f.tex})));
}
function buildRails(){""")
rep("syncMats(); buildRails(); buildLandmarks();","syncMats(); buildRails(); buildLandmarks(); buildSigns();")

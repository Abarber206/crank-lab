// build a site once: its pieces (put up by buildWorld like the houses) and its decoration
function planPOI(t){ if(t.blds) return t.blds; const D=poiDecor(); t.blds=POI_BUILD[t.kind](t,D); poiPosts(t.blds,D); t.decor=D.flush(); return t.blds; }
// an open side (only the lintel of the wall left) stands on posts: one at each end of the opening that no full wall
// holds up, in the building's beam colour, so a shed or a loading bay never looks like a roof floating on nothing
function poiPosts(blds,D){ const W=[], full=new Set(), done=new Set(), K=(a,b,l)=>a+','+b+','+l, ends=p=>p.axis==='x'?[[p.i,p.j],[p.i,p.j+1]]:[[p.i,p.j],[p.i+1,p.j]];
  for(const b of blds) for(const p of b.pieces) if(p.type==='wall') W.push(p);
  const OP=new Set(W.filter(p=>p.mask===POI_OPEN).map(p=>p.axis+','+p.i+','+p.j+','+p.l));
  for(const p of W){ const m=p.mask==null?511:p.mask; if(m===POI_OPEN||m===POI_LOW||m===POI_MERLON) continue; for(const [a,b] of ends(p)) full.add(K(a,b,p.l)); }
  for(const p of W){ if(p.mask!==POI_OPEN) continue; for(const [a,b] of ends(p)){ const k=K(a,b,p.l); if(full.has(k)||done.has(k)) continue; done.add(k);
      const x=a*CELL, z=b*CELL, y=p.l*LVL+FT/2, h=LVL*2/3-FT/2+0.04, c=(p.skin&&p.skin.beam!=null)?p.skin.beam:0x5a3a1e, cap=new THREE.Color(c).multiplyScalar(0.8).getHex();
      D.obj(p.mat==='metal'?'metal':p.mat==='brick'?'brick':'wood',p.mat==='metal'?320:240);
      D.box(0.3,h,0.3,x,y,z,c); D.box(0.42,0.12,0.42,x,y,z,cap); D.box(0.38,0.1,0.38,x,y+h-0.1,z,cap);
      if(p.mat!=='metal') for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]) if(dx?OP.has('z,'+(dx>0?a:a-1)+','+b+','+p.l):OP.has('x,'+a+','+(dz>0?b:b-1)+','+p.l)){ const g=new THREE.BoxGeometry(0.12,0.9,0.12); g.rotateZ(dx?-dx*0.7:0); g.rotateX(dz?dz*0.7:0); D.geo(g,c,x+dx*0.3,y+h-0.38,z+dz*0.3); } // knee braces up to the lintel
      D.solid(x-0.15,y,z-0.15,x+0.15,y+h,z+0.15); D.end(); } } }
// shots stop on solid decoration (containers, machines, the rocket...): a stand-in piece takes the hit
const POI_SOLID={key:'_deco',mat:'metal',type:'wall',deco:1,group:{position:new THREE.Vector3()}};
function decoShot(o,d,range,nearT){ let best=null, bs=null; const ps=new Set(), n=Math.min(90,Math.ceil(range/4)); for(let k=0;k<=n;k++){ const t=k*4; staticsInto(ps,o.x+d.x*t,o.z+d.z*t,2.5); }
  ps.forEach(s=>{ if(!s.deco) return; for(const b of s.boxes){ const tb=rayBox(o,d,b); if(tb>=nearT&&tb<=range&&(best==null||tb<best)){ best=tb; bs=s; } } }); return best==null?null:{t:best,s:bs}; } // (where, and what it hit)

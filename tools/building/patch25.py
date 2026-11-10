# ---------- 25. the edit update: geometry, collision and structural support as three systems that follow every edit ----------
# ===== 1. GEOMETRY: which selections are real edits, and what they turn a piece into =====
rep("""const WALL_SHAPES={'':'No change','4':'Window','3':'Side window','5':'Side window','3,5':'Side windows','1,4':'Door','0,3':'Side door','2,5':'Side door',
  '6,7,8':'Lower wall','3,4,5,6,7,8':'Half wall','1,2,4,5,7,8':'Side wall','0,1,3,4,6,7':'Side wall',
  '1,2,5':'Half-sliced wall','0,1,3':'Half-sliced wall','5,7,8':'Half-sliced wall','3,6,7':'Half-sliced wall'};
const SLICED=new Set(['1,2,5','0,1,3','5,7,8','3,6,7']);
const WALL_OK=new Set(Object.keys(WALL_SHAPES).filter(k=>k));""",
"""/* Wall edits (tiles removed; idx = row*3 + col, row 0 is the bottom). Only the edits Fortnite really has (from the
   reference sheets) and their mirror images; any other selection is refused, even if it would hold together. */
const WALL_SHAPES={'':'No change','4':'Window','3':'Side window','5':'Side window','3,5':'Double window','1,4':'Door','0,3':'Side door','2,5':'Side door',
  '0,1,2,4':'Arch','0,1,3,4':'Side arch','1,2,4,5':'Side arch','2,3,5':'Window door','0,3,5':'Window door',
  '6,7,8':'Half wall','3,4,5,6,7,8':'Low wall','2,5,6,7,8':'Half wall door','0,3,6,7,8':'Half wall door','1,2,4,5,7,8':'Column','0,1,3,4,6,7':'Column',
  '1,2,5':'45° cut','0,1,3':'45° cut','5,7,8':'Triangle','3,6,7':'Triangle',
  '0,3,4,5,6,7,8':'Partial low wall','2,3,4,5,6,7,8':'Partial low wall','0,1,3,4,6,7,8':'Partial half wall','1,2,4,5,6,7,8':'Partial half wall'};
const SLICED=new Set(['1,2,5','0,1,3','5,7,8','3,6,7']);
const WALL_OK=new Set(Object.keys(WALL_SHAPES).filter(k=>k));
function wallMaskValid(m){ if(!(m>0&&m<512)) return false; const r=[]; for(let i=0;i<9;i++) if(!(m>>i&1)) r.push(i); return r.length===0||WALL_OK.has(r.join(',')); }
const selMask=(sel,full)=>{ let m=full; sel.forEach(i=>{ if(i<9) m&=~(1<<i); }); return m; };
/* Stair edits: 2x2 big squares (idx = row*2 + col, row along +z, col along +x) and, as in Fortnite, a thin centre
   strip between them (4: between 0 and 1, 5: between 2 and 3, 6: between 0 and 2, 7: between 1 and 3).
   Two side-by-side squares make a half stair, three in an L an L stair, all four dragged in a U a spiral stair;
   each rises the way you dragged. Dragging straight across the centre strip turns the whole stair to rise that way. */
const STAIR_FLIP=[[4,5,1],[5,4,3],[6,7,0],[7,6,2]];
function stairPathOk(t){ if(!Array.isArray(t)||(t.length!==3&&t.length!==4)) return false; if(new Set(t).size!==t.length||t.some(i=>!(i>=0&&i<4&&(i|0)===i))) return false;
  for(let k=1;k<t.length;k++) if(!stairStep(t[k-1],t[k])) return false; return true; }
function stairEditResult(sel,order){
  const ord=(order||[]).filter(i=>sel.has(i)); sel.forEach(i=>{ if(!ord.includes(i)) ord.push(i); });
  const big=ord.filter(i=>i<4), sm=ord.filter(i=>i>=4), n=big.length;
  if(n===2){ const st=stairStep(big[0],big[1]); if(st) return {dir:st.dir,half:st.half,path:null}; }
  if(n===3||n===4){ let path=stairPathOk(big)?big:null;
    if(!path&&n===3){ const mid=big.find(t=>big.every(u=>u===t||stairStep(t,u))); if(mid!=null){ const e=big.filter(t=>t!==mid); path=[e[0],mid,e[1]]; } }
    if(path) return {dir:stairStep(path[0],path[1]).dir,half:-1,path}; }
  for(const [a,b,dir] of STAIR_FLIP){ const ia=sm.indexOf(a), ib=sm.indexOf(b); if(ia>=0&&ib>ia) return {dir,half:-1,path:null}; }
  return n===0?'none':null; }
// the squares of an L or spiral stair: the first climbs to half height, turning squares are landings, the last climbs to the top
function stairSegs(path){ const n=path.length, out=[];
  for(let k=0;k<n;k++){ const t=path[k];
    if(k===0) out.push({t,dir:stairStep(t,path[1]).dir,h0:0,h1:LVL/2});
    else if(k===n-1) out.push({t,dir:stairStep(path[k-1],t).dir,h0:LVL/2,h1:LVL});
    else out.push({t,dir:null,h0:LVL/2,h1:LVL/2}); }
  return out; }
// is this a shape the piece could really have? (checked on the host for every edit from a player)
function shapeValid(p,o){
  if(p.type==='wall') return wallMaskValid(o.mask);
  if(p.type==='floor') return o.mask>=1&&o.mask<=15&&(o.mask|0)===o.mask;
  if(p.type==='cone') return o.mask>=0&&o.mask<=14&&(o.mask|0)===o.mask;
  if(!(o.dir>=0&&o.dir<4&&(o.dir|0)===o.dir)) return false;
  if(o.path!=null) return stairPathOk(o.path)&&(o.half==null||o.half<0);
  return o.half==null||o.half===-1||o.half===0||o.half===1; }""")
rep("""  if(!editValid()) return p.type==='ramp'?'Pick 2 side-by-side tiles or all 4':p.type==='wall'?'Not a valid edit':'Keep at least one tile';
  if(p.type==='wall') return WALL_SHAPES[key]||'Not a valid edit';""",
"""  if(!editValid()) return p.type==='ramp'?'Drag 2 side-by-side squares, an L, a U, or across the centre':p.type==='wall'?'Not a valid edit':'Keep at least one tile';
  if(p.type==='wall') return WALL_SHAPES[key]||'Not a valid edit';""")
rep("""  return n===0?'No change':n===2?'Half stairs':'Full stairs';
}""","""  const r=stairEditResult(edit.sel,edit.order); if(r==='none') return 'No change';
  return r.path?(r.path.length===3?'L stairs':'Spiral stairs'):r.half>=0?'Half stairs':r.dir===p.dir&&(p.half==null||p.half<0)&&!p.path?'Full stairs':'Turned stairs';
}""")
rep("""  if(p.type==='wall') return edit.sel.size===0||WALL_OK.has([...edit.sel].sort((a,b)=>a-b).join(','));
  if(p.type==='cone') return edit.sel.size<4;
  const n=edit.sel.size; if(n===0||n===4) return true;
  if(n!==2) return false; const [a,b]=[...edit.sel]; return stairStep(a,b)!==null;
}""","""  if(p.type==='wall') return edit.sel.size===0||wallMaskValid(selMask(edit.sel,511));
  if(p.type==='cone') return edit.sel.size<4;
  return stairEditResult(edit.sel,edit.order)!==null;
}""")
rep("""    } else {
      // 2 side-by-side tiles: half stair over those tiles, rising from the first one you touched.
      // All 4: full stair aimed from your first tile toward your second.
      const ord=(edit.order||[]).filter(i=>edit.sel.has(i)), n=edit.sel.size;
      if(n===2){ const st=stairStep(ord[0]??[...edit.sel][0],ord[1]??[...edit.sel][1]); if(st){ p.dir=st.dir; p.half=st.half; } }
      else if(n===4){ const st=ord.length>=2?stairStep(ord[0],ord[1]):null; if(st) p.dir=st.dir; p.half=-1; }
    }
  }""","""    } else { const r=stairEditResult(edit.sel,edit.order); if(r&&r!=='none'){ p.dir=r.dir; p.half=r.half; p.path=r.path; } }
  }""")
# confirming, cancelling or resetting: geometry, then collision, then support (only what lost every path to the ground falls)
rep("""  if(pieces.has(p.key)){ buildPiece(p); startAnim(p,80); phaseCheck(p); popPlayerOut(); netOp({op:'shape',key:p.key,mask:p.mask,dir:p.dir,half:p.half}); }
  sfx(apply?'confirm':'edit'); syncMode();""",
"""  if(pieces.has(p.key)){ const nb0=[...(conn.get(p)||[])]; buildPiece(p); startAnim(p,80); phaseCheck(p); popPlayerOut(); netOp({op:'shape',key:p.key,mask:p.mask,dir:p.dir,half:p.half,path:p.path||null}); reshaped(p,nb0); }
  sfx(apply?'confirm':'edit'); syncMode();""")
rep("else { p.half=-1; p.dir=p.sdir??p.dir; }\n  edit.sel.clear(); exitEdit(false);","else { p.half=-1; p.path=null; } // a stair resets to a full stair facing the way it faces now\n  edit.sel.clear(); exitEdit(false);")
# stair edit grid: the four big squares plus the thin centre strip
rep("""      mk(G.tFloor,idx,new THREE.Vector3(cx,p.l*LVL+0.06,cz),m=>{m.rotation.x=-Math.PI/2;}); // flat at the stair's base, same as a floor edit
    }
  }""","""      mk(G.tFloor,idx,new THREE.Vector3(cx,p.l*LVL+0.06,cz),m=>{m.rotation.x=-Math.PI/2;}); // flat at the stair's base, same as a floor edit
    }
    for(const [idx,x,z,w,d] of [[4,.5,.25,.7,2.3],[5,.5,.75,.7,2.3],[6,.25,.5,2.3,.7],[7,.75,.5,2.3,.7]]) // the centre strip
      mk(new THREE.PlaneGeometry(w,d),idx,new THREE.Vector3(p.i*CELL+x*CELL,p.l*LVL+0.09,p.j*CELL+z*CELL),m=>{m.rotation.x=-Math.PI/2;});
  }""")
rep("  if(mask!==511&&!WALL_OK.has(removed.join(','))) return; // bots only make real edits (window, door, ...)",
    "  if(!wallMaskValid(mask)) return; // bots only make real edits (window, door, ...)\n  const nb0=[...(conn.get(p)||[])];")
rep("  if(net.role==='host') netOp({op:'shape',key:p.key,mask:p.mask,dir:p.dir,half:p.half});\n}",
    "  if(net.role==='host') netOp({op:'shape',key:p.key,mask:p.mask,dir:p.dir,half:p.half,path:p.path||null}); reshaped(p,nb0);\n}")
# L and spiral stairs: each square its own little flight of steps (or a landing), with a solid underside
rep("/* ---------- pieces ---------- */","""const stairPathCache=new Map();
function stairPathGeo(path){ const key=path.join(''); let g=stairPathCache.get(key); if(g) return g;
  const treads=[], under=[], h=CELL/2, K=4, w=h-0.12;
  for(const s of stairSegs(path)){ const r=s.t>>1, c=s.t&1, cx=-CELL/2+(c+.5)*h, cz=-CELL/2+(r+.5)*h;
    const put=(b,list)=>{ if(s.dir!=null) b.rotateY([0,-Math.PI/2,Math.PI,Math.PI/2][s.dir]); b.translate(cx,0,cz); list.push(b); };
    if(s.dir==null){ const b=new THREE.BoxGeometry(h-0.02,0.2,h-0.02); b.translate(0,s.h0-LVL/2-0.1,0); put(b,treads);
      const u=new THREE.BoxGeometry(h-0.3,s.h0-0.2,0.18); u.translate(0,(s.h0-0.2)/2-LVL/2,0); put(u,under); continue; } // landing on a post
    const run=h/K, rise=(s.h1-s.h0)/K;
    for(let k=0;k<K;k++){ const t=new THREE.BoxGeometry(run+0.02,0.14,w); t.translate(-h/2+(k+.5)*run,s.h0+(k+1)*rise-0.083-LVL/2,0); put(t,treads);
      const rs=new THREE.BoxGeometry(0.06,rise,w); rs.translate(-h/2+k*run+0.03,s.h0+(k+.5)*rise-LVL/2,0); put(rs,treads); }
    const L=Math.hypot(h,s.h1-s.h0), ang=Math.atan2(s.h1-s.h0,h), u=new THREE.BoxGeometry(L,0.16,w); u.rotateZ(ang); u.translate(0,(s.h0+s.h1)/2-LVL/2-0.32,0); put(u,under); }
  const t=mergeGeos(treads), s=mergeGeos(under); t.computeVertexNormals(); s.computeVertexNormals(); g={t,s}; stairPathCache.set(key,g); return g; }
/* ---------- pieces ---------- */""")
rep("""    const sg=stairGeoFor(p.dir,p.half==null?-1:p.half); add(sg.t,0,0,0,0,0,M.tread); add(sg.s,0,0,0,0,0,M.beam);""",
    """    const sg=p.path?stairPathGeo(p.path):stairGeoFor(p.dir,p.half==null?-1:p.half); add(sg.t,0,0,0,0,0,M.tread); add(sg.s,0,0,0,0,0,M.beam);""")

# ===== 2. COLLISION: built from the same shape, never from the look =====
# the player's footprint is round (an upright capsule), so corners don't catch you diagonally
rep("const SAMP=[[0,0],[-R,-R],[R,-R],[-R,R],[R,R]];\nconst ovl=(b,x,z)=>x+R>b[0]&&x-R<b[3]&&z+R>b[2]&&z-R<b[5];",
    "const SAMP=[[0,0],[R,0],[-R,0],[0,R],[0,-R],[R*.7,R*.7],[-R*.7,R*.7],[R*.7,-R*.7],[-R*.7,-R*.7]];\nfunction circBox(b,x,z,r){ const dx=Math.max(b[0]-x,0,x-b[3]), dz=Math.max(b[2]-z,0,z-b[5]); return dx*dx+dz*dz<r*r; }\nconst ovl=(b,x,z)=>circBox(b,x,z,R);")
rep("  for(const b of p.boxes) if(x+r>b[0]&&x-r<b[3]&&z+r>b[2]&&z-r<b[5]&&b[4]>f+0.62&&b[1]<f+h-0.05) return true;",
    "  for(const b of p.boxes) if(circBox(b,x,z,r)&&b[4]>f+0.62&&b[1]<f+h-0.05) return true;")
# a wall's 45-degree cut collides along the diagonal (thin upright slices that never stick out past the cut)
rep("""      else { // full-height half on the kept side, plus a half-height block under/over the slant
        const keepL=cut[0]>0; push(keepL?off:off+tw/2,tw/2,yy,th);
        push(keepL?off+tw/2:off,tw/2,cut[1]<0?yy+th/2:yy,th/2); }""",
"""      else { const N=8; // slices across the tile; each keeps only what's solid all the way across it
        for(let k=0;k<N;k++){ const a=k/N, b=(k+1)/N, fromCut=cut[0]>0?1-b:a; // 0 at the cut corner's side, 1 at the far side
          const keep=th*fromCut; if(keep<0.02) continue; push(off+a*tw,tw/N,cut[1]<0?yy+th-keep:yy,keep); } }""")
# stairs: every square of an L or spiral stair has its own walking surface; open squares have none
rep("""  if(p.type==='ramp'){
    if(p.half!=null&&p.half>=0){""","""  if(p.type==='ramp'){
    if(p.path){ const h=CELL/2, c=Math.min(1,Math.floor(lx/h)), r=Math.min(1,Math.floor(lz/h)), s=stairSegs(p.path).find(q=>q.t===r*2+c); if(!s) return null;
      if(s.dir==null) return p.l*LVL+s.h0; const ux=(lx-c*h)/h, uz=(lz-r*h)/h, u=s.dir===0?ux:s.dir===1?uz:s.dir===2?1-ux:1-uz; return p.l*LVL+s.h0+(s.h1-s.h0)*u; }
    if(p.half!=null&&p.half>=0){""")

# ===== 3. STRUCTURAL SUPPORT: attachments come from what's left after the edit =====
rep("""  if(p.type==='wall') return [p.axis==='x'?[x0,y,z0,x0,y+LVL,z1]:[x0,y,z0,x1,y+LVL,z0]];
  if(p.type==='floor'||p.type==='cone') return [[x0,y,z0,x1,y,z1]];
  const sd=p.sdir??p.dir; // approx: a rotated stair keeps the attachment it was placed with, so an edit never drops anything
  const lo=[[x0,y,z0,x0,y,z1],[x0,y,z0,x1,y,z0],[x1,y,z0,x1,y,z1],[x0,y,z1,x1,y,z1]][sd];
  const hi=[[x1,y+LVL,z0,x1,y+LVL,z1],[x0,y+LVL,z1,x1,y+LVL,z1],[x0,y+LVL,z0,x0,y+LVL,z1],[x0,y+LVL,z0,x1,y+LVL,z0]][sd];""",
"""  // walls: each tile that's still there; floors: each quarter that's still there
  if(p.type==='wall'){ const m=p.mask==null?511:p.mask, tw=CELL/3, th=LVL/3, out=[];
    for(let r=0;r<3;r++) for(let c=0;c<3;c++) if(m>>(r*3+c)&1){ const ya=y+r*th, a=c*tw; out.push(p.axis==='x'?[x0,ya,z0+a,x0,ya+th,z0+a+tw]:[x0+a,ya,z0,x0+a+tw,ya+th,z0]); }
    return out; }
  if(p.type==='floor'){ const m=p.mask==null?15:p.mask, h=CELL/2, out=[];
    for(let r=0;r<2;r++) for(let c=0;c<2;c++) if(m>>(r*2+c)&1) out.push([x0+c*h,y,z0+r*h,x0+(c+1)*h,y,z0+(r+1)*h]);
    return out; }
  // cones: their four edges where they really are (a raised corner lifts its edges)
  if(p.type==='cone'){ const k=coneCorners(p.mask||0); return [[k.A,k.B],[k.B,k.C],[k.C,k.D],[k.D,k.A]].map(([a,b])=>[x0+Math.min(a[0],b[0]),y+Math.min(a[2],b[2]),z0+Math.min(a[1],b[1]),x0+Math.max(a[0],b[0]),y+Math.max(a[2],b[2]),z0+Math.max(a[1],b[1])]); }
  // stairs: the edge they start from and the edge they reach, as the stair is now (turned, halved, L or spiral)
  const edge=(qx0,qz0,qx1,qz1,d,yy)=>d===0?[qx1,yy,qz0,qx1,yy,qz1]:d===1?[qx0,yy,qz1,qx1,yy,qz1]:d===2?[qx0,yy,qz0,qx0,yy,qz1]:[qx0,yy,qz0,qx1,yy,qz0];
  if(p.path){ const s=stairSegs(p.path), a=s[0], b=s[s.length-1], h=CELL/2, q=t=>[x0+(t&1)*h,z0+(t>>1)*h,x0+((t&1)+1)*h,z0+((t>>1)+1)*h];
    return [edge(...q(a.t),(a.dir+2)%4,y),edge(...q(b.t),b.dir,y+LVL)]; }
  const sd=p.dir, hs=p.half!=null&&p.half>=0, hh=CELL/2;
  const qx0=hs&&(sd===1||sd===3)?x0+p.half*hh:x0, qx1=hs&&(sd===1||sd===3)?qx0+hh:x1, qz0=hs&&(sd===0||sd===2)?z0+p.half*hh:z0, qz1=hs&&(sd===0||sd===2)?qz0+hh:z1;
  const lo=edge(qx0,qz0,qx1,qz1,(sd+2)%4,y), hi=edge(qx0,qz0,qx1,qz1,sd,y+LVL);
  if(hs) return [lo,hi];""")
rep("""   face (>= BUILD_CFG.minContact), so floors touching corner-to-corner don't hold each other up. Edits don't change
   connections (approx: an edited wall still supports what's above it, as in Fortnite). */""",
"""   face (>= BUILD_CFG.minContact), so floors touching corner-to-corner don't hold each other up. Attachments come from
   the piece as it is now: an edit that takes away the tiles along a shared edge takes that connection away too. */""")
rep("/* After something is removed: search outward only from the pieces it touched.",
"""/* After an edit (or a reset): the piece's attachments were rebuilt from its new shape. Re-check only what it touched
   before and after; a group that still has a path to the ground stays, anything left with none falls (the edited
   piece included). Only the host (or a solo game) decides; everyone else is told. */
function reshaped(p,nb0){
  if(net.role==='client'||!pieces.has(p.key)) return;
  const doomed=findUnsupported([p,...(nb0||[])].filter(q=>pieces.has(q.key))); if(!doomed.length) return;
  const oc=pieceCenter(p); doomed.sort((a,b)=>pieceCenter(a).distanceTo(oc)-pieceCenter(b).distanceTo(oc));
  collapsePieces(doomed,oc); if(net.role==='host') netOp({op:'collapse',keys:doomed.map(q=>q.key),c:[+oc.x.toFixed(2),+oc.y.toFixed(2),+oc.z.toFixed(2)]}); }
/* After something is removed: search outward only from the pieces it touched.""")

# ===== 4. MULTIPLAYER: the stair's shape travels with it; the host refuses impossible shapes =====
rep("const pick=t=>({type:t.type,axis:t.axis,i:t.i,j:t.j,l:t.l,dir:t.dir,sdir:t.sdir,key:t.key,mat:t.mat,owner:t.owner});",
    "const pick=t=>({type:t.type,axis:t.axis,i:t.i,j:t.j,l:t.l,dir:t.dir,sdir:t.sdir,key:t.key,mat:t.mat,owner:t.owner,path:t.path||null});")
rep("else if(o.op==='shape'){ const p=pieces.get(o.key); if(p){ if(edit&&edit.piece===p) exitEdit(false); p.mask=o.mask; p.dir=o.dir; p.half=o.half; buildPiece(p); startAnim(p,140); popPlayerOut(); } }",
    "else if(o.op==='shape'){ const p=pieces.get(o.key); if(p){ if(edit&&edit.piece===p) exitEdit(false); const nb0=[...(conn.get(p)||[])]; p.mask=o.mask; p.dir=o.dir; p.half=o.half; p.path=o.path||null; buildPiece(p); startAnim(p,140); popPlayerOut(); reshaped(p,nb0); } }")
s=s.replace("c.send({type:'fix',key:p.key,mask:p.mask,dir:p.dir,half:p.half})","c.send({type:'fix',key:p.key,mask:p.mask,dir:p.dir,half:p.half,path:p.path||null})")
rep("const p=pieces.get(o.key); if(!p||!canEdit(p,from)){","const p=pieces.get(o.key); if(!p||!canEdit(p,from)||!shapeValid(p,o)){")
rep("m.pieces.forEach(t=>{ const p=addPiece(t); p.mask=t.mask??p.mask; p.half=t.half;","m.pieces.forEach(t=>{ const p=addPiece(t); p.mask=t.mask??p.mask; p.half=t.half; p.path=t.path||null;")
rep("else if(m.type==='fix'){ const p=pieces.get(m.key); if(p&&!(p.mask===m.mask&&(p.dir??0)===(m.dir??0)&&(p.half??-1)===(m.half??-1))){ if(edit&&edit.piece===p) exitEdit(false); p.mask=m.mask; p.dir=m.dir; p.half=m.half; buildPiece(p); } }",
    "else if(m.type==='fix'){ const p=pieces.get(m.key); if(p&&!(p.mask===m.mask&&(p.dir??0)===(m.dir??0)&&(p.half??-1)===(m.half??-1)&&String(p.path||'')===String(m.path||''))){ if(edit&&edit.piece===p) exitEdit(false); p.mask=m.mask; p.dir=m.dir; p.half=m.half; p.path=m.path||null; buildPiece(p); } }")
# the build cap counts players' builds only (the towns' houses are thousands of pieces on their own)
rep("  if(order.length>MAX_BUILDS){ const old=order.find(q=>q.owner!=='world'); if(old&&old!==p) removePiece(old); }",
    "  if(p.owner!=='world'){ let n=0, old=null; for(const q of order) if(q.owner!=='world'){ n++; if(!old) old=q; } if(n>MAX_BUILDS&&old&&old!==p) removePiece(old); }")
# a muzzle flash is removed from the gun it was put on (switching weapons right after a shot used to leave it stuck)
rep("H.rig.muzzle.add(f); setTimeout(()=>H.rig.muzzle.remove(f),45); }","H.rig.muzzle.add(f); setTimeout(()=>{ if(f.parent) f.parent.remove(f); },45); }")

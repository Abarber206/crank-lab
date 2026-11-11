# patch134: upstairs is split into real rooms. The stairwell and the landing at its top are the hallway; every other
# room opens off it through its own door: a bathroom across from the landing, a bedroom, and in bigger houses a second
# bedroom or a study. Rooms are divided from each other by solid walls. (The old dividing wall upstairs was clipped
# around the stairwell to less than one 5 m wall panel, so most houses ended up with no wall at all: one open room
# holding the bed, the toilet and the bath.)
rep("""function houseRooms(h,l){ if(h._rooms&&h._rooms[l]) return h._rooms[l]; h._rooms=h._rooms||{};""",
"""function upstairsRooms(h,l){ const C=CELL, DOOR=511&~18, st=houseStair(h).cells, key=(i,j)=>i+','+j, hall=new Set(st.map(c=>key(c[0],c[1])));
  const others=[]; for(let a=0;a<h.w;a++) for(let b=0;b<h.d;b++){ const i=h.i0+a, j=h.j0+b; if(!hall.has(key(i,j))) others.push([i,j]); }
  const nb=(c,d)=>Math.abs(c[0]-d[0])+Math.abs(c[1]-d[1])===1, onHall=c=>st.some(s=>nb(c,s)), land=st[0];
  // a room for each cell beside the hallway (the one across from the landing is the bathroom); the rest join a bedroom next to them
  const seeds=others.filter(onHall).sort((p,q)=>(nb(q,land)-nb(p,land))||(p[0]-q[0])||(p[1]-q[1])), rooms=seeds.map((c,k)=>({type:k===0&&seeds.length>1?'bath':'',cells:[c]}));
  const roomOf=c=>rooms.find(r=>r.cells.some(e=>e[0]===c[0]&&e[1]===c[1]));
  let left=others.filter(c=>!roomOf(c)), guard=0;
  while(left.length&&guard++<20){ for(const c of left.slice()){ const opts=rooms.filter(r=>r.type!=='bath'&&r.cells.some(e=>nb(e,c))); if(!opts.length) continue; opts[h.id%opts.length].cells.push(c); left=left.filter(e=>e!==c); } }
  if(left.length){ const r=rooms.find(r=>r.cells.some(e=>left.some(c=>nb(e,c))))||rooms[0]; if(r) r.cells.push(...left); }
  const beds=rooms.filter(r=>!r.type).sort((p,q)=>q.cells.length-p.cells.length); beds.forEach((r,k)=>{ r.type=k===0?'bed':k===1?(h.id%3===0?'study':'bed2'):'study'; });
  if(!beds.length&&rooms.length) rooms[0].type='bed';
  // walls on every edge between different rooms (and the hallway); each room gets one door, onto the hallway
  const walls=[], doors=[], all=[...st.map(c=>({c,r:null})),...others.map(c=>({c,r:roomOf(c)}))], doorDone=new Set();
  const wall=(axis,i,j,mask)=>{ walls.push({type:'wall',axis,i,j,l,mask,mat:h.mat,inner:1}); if(mask!==511) doors.push(axis==='x'?[i*C-1.0,(j+.5)*C-0.95,i*C+1.0,(j+.5)*C+0.95]:[(i+.5)*C-0.95,j*C-1.0,(i+.5)*C+0.95,j*C+1.0]); };
  // a room's door: onto the hallway cell nearest the landing, from the room cell that touches it
  for(const r of rooms){ let best=null; for(const c of r.cells) for(const s of st) if(nb(c,s)){ const sc=(s===land?0:10)+(Math.abs(c[0]-s[0])?1:0); if(!best||sc<best.sc) best={c,s,sc}; } r.door=best; }
  for(let x=0;x<all.length;x++) for(let y=x+1;y<all.length;y++){ const A=all[x], B=all[y]; if(!nb(A.c,B.c)||A.r===B.r) continue;
    const r=A.r||B.r, rc=A.r?A.c:B.c, hc=A.r?B.c:A.c, isDoor=!(A.r&&B.r)&&r.door&&r.door.c===rc&&r.door.s===hc;
    const axis=A.c[0]!==B.c[0]?'x':'z', i=Math.max(A.c[0],B.c[0]), j=Math.max(A.c[1],B.c[1]); wall(axis,axis==='x'?i:A.c[0],axis==='z'?j:A.c[1],isDoor?DOOR:511); }
  rooms.unshift({type:'hall',cells:st.map(c=>[c[0],c[1]])});
  return {rooms:rooms.map(r=>({type:r.type,cells:r.cells})),walls,doors}; }
function houseRooms(h,l){ if(h._rooms&&h._rooms[l]) return h._rooms[l]; h._rooms=h._rooms||{};
  if(h.floors>1&&l>h.L) return h._rooms[l]=upstairsRooms(h,l);""")
rep("LISTS={living:[0,5,6,2,6],kitchen:[3,10,1],bed:[4,8,7,9],bed2:[4,8,7],bath:[11,13,12],study:[9,2,6]};",
    "LISTS={living:[0,5,6,2,6],kitchen:[3,10,1],bed:[4,8,7,9],bed2:[4,8,7],bath:[11,13,12],study:[9,2,6],hall:[]};")
# a one-room study upstairs gets a desk and a bookcase (a chair as well left no way in to the bookcase in some houses)
rep("const got={}; let made=0; const most=rm.cells.length*2+1;","const got={}; let made=0; const most=rm.type==='study'&&rm.cells.length===1?2:rm.cells.length*2+1;")

function planHouses(t){
  /* The town is a grid: a main street and a cross street through the middle make four blocks. Houses stand in rows
     along both streets, facing them, each with a front yard and a path to the sidewalk and a gap to its neighbours.
     Lots in the way of a road coming into town are skipped. */
  const r=seeded(t.seed), L=Math.round(t.h/LVL), ci=Math.round(t.x/CELL), cj=Math.round(t.z/CELL), used=new Set(), out=[];
  const key=(i,j)=>i+','+j;
  for(let a=-12;a<=12;a++) for(let b=-12;b<=12;b++) if(a===-1||a===0||b===-1||b===0) used.add(key(ci+a,cj+b)); // the two streets
  for(const rd of WORLD.roads){ if(rd.street) continue; // roads coming in
    for(const p of rd.pts){ const x=SPAWN[0]+p[0], z=SPAWN[2]+p[1]; if(Math.hypot(x-t.x,z-t.z)>t.R+12) continue;
      for(let a=-2;a<=2;a++) for(let b=-2;b<=2;b++){ const i=Math.floor(x/CELL)+a, j=Math.floor(z/CELL)+b; if(Math.hypot((i+.5)*CELL-x,(j+.5)*CELL-z)<7.5) used.add(key(i,j)); } } }
  const free=(i0,j0,w,d)=>{ for(let a=-1;a<=w;a++) for(let b=-1;b<=d;b++) if(used.has(key(i0+a,j0+b))) return false; return true; };
  const inTown=(i0,j0,w,d)=>[[i0,j0],[i0+w,j0],[i0,j0+d],[i0+w,j0+d]].every(([i,j])=>Math.hypot(i*CELL-t.x,j*CELL-t.z)<t.R-1);
  const shapes=[[2,2],[3,2],[2,3]]; let k=0;
  const order=t.axis==='z'?[false,true]:[true,false];
  for(const X of order) for(const sd of [1,-1]){ let s=-11;
    while(s<11){ const [along,deep]=shapes[Math.floor(r()*shapes.length)], front=sd>0?2:-2-deep; // a front-yard row between the street and the house
      const i0=X?ci+s:ci+front, j0=X?cj+front:cj+s, w=X?along:deep, d=X?deep:along;
      if(!free(i0,j0,w,d)||!inTown(i0,j0,w,d)){ s++; continue; }
      for(let p=0;p<w;p++) for(let q=0;q<d;q++) used.add(key(i0+p,j0+q));
      const side=X?(sd>0?'n':'s'):(sd>0?'w':'e'); // the door faces its street
      const m=r(), mat=m<0.5?'wood':m<0.85?'brick':'metal', roof=r()<0.6?'brick':'wood', floors=r()<0.55?2:1;
      const rs=seeded(t.seed+977*(k+1)), style=HOUSE_STYLE[mat]; k++;
      out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length,skin:{style,paint:Math.floor(rs()*HOUSE_PAINT[style].length),roof:Math.floor(rs()*4)}});
      s+=along+1; } }
  t.houses=out; return out;
}

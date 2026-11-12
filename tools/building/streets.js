/* ---------- town streets: a main street and side streets ----------
   The main street runs through town along the first road in, out to the edge both ways. Side streets branch off it
   here and there, to one side or both, staggered rather than a neat crossroads: some run out to the edge (where a
   road can come in), some stop short with a turning circle. Now and then a back lane joins two side streets into a
   loop. Every street runs along the build grid, so the houses still sit square to their street. The town's ground is
   a lumpy outline, not a circle (townRadAt). */
function townIn(t,x,z,pad){ const dx=x-t.x, dz=z-t.z; return Math.hypot(dx,dz)<townRadAt(t,dx,dz)-(pad||0); }
function planStreets(t,arrivals){ const C=CELL, ci=Math.round(t.x/C), cj=Math.round(t.z/C);
  if(t.kind){ const Ls=Math.floor((t.R-4)/C)*C; t.streetL=Ls; t.ends=[[t.x-Ls,t.z],[t.x+Ls,t.z],[t.x,t.z-Ls],[t.x,t.z+Ls]]; t.endDir=[[-1,0],[1,0],[0,-1],[0,1]]; t.endEdge=[1,1,1,1]; t.endKind=['edge','edge','edge','edge']; t.segs=[]; t.junc=[]; return; }
  const r=seeded(t.seed+4242), X0=t.axis==='x', inC=(i,j,pad)=>townIn(t,i*C,j*C,pad);
  const reach=(i,j,di,dj)=>{ let n=0; while(n<26&&inC(i+di*(n+1),j+dj*(n+1),5)) n++; return n; };
  // cell space: a street runs along x (X) or along z, on grid line c across it, from grid line a to b along it
  const P0=X0?ci:cj, Q0=X0?cj:ci, ij=(p,q)=>X0?[p,q]:[q,p]; // (along main, across main) -> (i,j)
  const main={X:X0,c:Q0,a:P0-reach(ci,cj,X0?-1:0,X0?0:-1),b:P0+reach(ci,cj,X0?1:0,X0?0:1),edgeA:1,edgeB:1}, segs=[main], sides=[];
  const side=(p,s,want)=>{ const [i,j]=ij(p,Q0), full=reach(i,j,X0?0:s,X0?s:0); if(full<5) return null;
    const len=want==='edge'?full:Math.min(full,want), edge=len===full?1:0;
    const S={X:!X0,c:p,a:s>0?Q0:Q0-len,b:s>0?Q0+len:Q0,side:s,edgeA:s<0?edge:0,edgeB:s>0?edge:0,len}; segs.push(S); sides.push(S); return S; };
  const okAt=(p,s)=>p>=main.a+3&&p<=main.b-3&&sides.every(S=>S.side===s?Math.abs(S.c-p)>=6:(S.c===p||Math.abs(S.c-p)>=3));
  // first a street out toward every road that comes in from the side (the main street's ends take the rest)
  for(const [ax,az] of arrivals||[]){ const dx=ax-t.x, dz=az-t.z, dl=Math.hypot(dx,dz)||1, ua=(X0?dx:dz)/dl, ub=(X0?dz:dx)/dl; if(Math.abs(ua)>0.64) continue;
    const s=ub>0?1:-1; if(sides.some(S=>S.side===s&&(S.edgeA||S.edgeB))) continue;
    const p0=Math.max(main.a+3,Math.min(main.b-3,Math.round((X0?ax:az)/C)));
    for(const dp of [0,1,-1,2,-2,3,-3,4,-4,5,-5]){ const p=p0+dp; if(okAt(p,s)&&side(p,s,'edge')) break; } }
  // then a few more, out to the edge or a short way with a turning circle
  const want=4+(r()<0.5?1:0);
  for(let tr=0;tr<60&&sides.length<want;tr++){ const p=main.a+3+Math.floor(r()*Math.max(1,main.b-main.a-5)), s=r()<0.5?1:-1; if(!okAt(p,s)) continue;
    side(p,s,r()<0.6?'edge':6+Math.floor(r()*4)); }
  // back lanes: two neighbouring side streets on the same side joined into a loop (a short dead end is pulled in to meet it)
  for(const s of [1,-1]){ const L=sides.filter(S=>S.side===s).sort((A,B)=>A.c-B.c), inLoop=new Set();
    for(let q=0;q<L.length-1;q++){ const A=L[q], B=L[q+1]; if(inLoop.has(A)||r()>0.85||B.c-A.c<6||B.c-A.c>16) continue; const o=Math.min(10,A.len,B.len); if(o<7) continue;
      let ok=true; for(let p=A.c;p<=B.c&&ok;p++){ const [i,j]=ij(p,Q0+s*o); if(!inC(i,j,3)) ok=false; } if(!ok) continue;
      if([A,B].some(S=>S.len-o>0&&S.len-o<4&&(S.edgeA||S.edgeB))) continue; // (no stub just past the lane)
      for(const S of [A,B]) if(S.len-o>0&&S.len-o<4){ S.len=o; if(s>0) S.b=Q0+o; else S.a=Q0-o; }
      segs.push({X:X0,c:Q0+s*o,a:A.c,b:B.c,lane:1}); inLoop.add(A); inLoop.add(B); } }
  // the ends left inside town: one turning circle at most (on the longest), the rest a hammerhead where it fits, or a fence
  const onSeg=(S,i,j)=>S.X?(j===S.c&&i>=S.a&&i<=S.b):(i===S.c&&j>=S.a&&j<=S.b);
  { const dead=[]; segs.forEach((S,k)=>{ for(const E of ['A','B']){ if(S['edge'+E]) continue; const g=E==='B'?S.b:S.a, [i,j]=S.X?[g,S.c]:[S.c,g]; if(!segs.some((O,m)=>m!==k&&onSeg(O,i,j))) dead.push([S,E,g]); } });
    dead.sort((x,y)=>(y[0].b-y[0].a)-(x[0].b-x[0].a)); let circle=r()<0.75;
    for(const [S,E,g] of dead){ if(circle){ S['kind'+E]='circle'; circle=false; continue; }
      const H={X:!S.X,c:g,a:S.c-2,b:S.c+2,hammer:1}; let fits=true;
      for(let p=H.a;p<=H.b&&fits;p++){ const [i,j]=H.X?[p,H.c]:[H.c,p]; if(!inC(i,j,3)) fits=false; }
      if(fits&&segs.some(O=>O!==S&&(O.X===H.X?Math.abs(O.c-H.c)<5&&O.a<H.b+3&&O.b>H.a-3:O.c>=H.a-3&&O.c<=H.b+3&&H.c>=O.a-3&&H.c<=O.b+3))) fits=false;
      if(fits&&r()<0.7){ segs.push(H); S['kind'+E]='hammer'; } else S['kind'+E]='fence'; } }
  // in world space, with the open ends (a road comes in, a turning circle, a stub or a fence) and the junctions
  t.segs=segs.map(S=>({X:S.X,ci:S.c,ai:S.a,bi:S.b,c:S.c*C,a:S.a*C,b:S.b*C,main:S===main,lane:!!S.lane,hammer:!!S.hammer}));
  t.ends=[]; t.endDir=[]; t.endEdge=[]; t.endKind=[]; t.junc=[]; const jk=new Set();
  segs.forEach((S,k)=>{ for(const e of [0,1]){ const g=e?S.b:S.a, [i,j]=S.X?[g,S.c]:[S.c,g], d=e?1:-1, E=e?'B':'A';
    const m=segs.findIndex((O,mm)=>mm!==k&&onSeg(O,i,j));
    if(m>=0){ t.segs[k]['j'+E]=m; const key=i+','+j; if(!jk.has(key)){ jk.add(key); t.junc.push([i*C,j*C]); } }
    else { t.segs[k]['end'+E]=t.ends.length; t.ends.push([i*C,j*C]); t.endDir.push(S.X?[d,0]:[0,d]); t.endEdge.push(S['edge'+E]?1:0); t.endKind.push(S['edge'+E]?'edge':S.hammer?'stub':S['kind'+E]||'fence'); } } });
  t.streetL=Math.max(...t.segs.map(S=>S.b-S.a))/2; }
// which open end a road coming in joins: the nearest one at the edge of town (or the one facing a preferred way)
function pickEnd(t,at,pref){ let ids=t.ends.map((e,k)=>k).filter(k=>t.endEdge[k]); if(!ids.length) ids=t.ends.map((e,k)=>k);
  if(pref!=null){ const D=[[-1,0],[1,0],[0,-1],[0,1]][pref]; ids.sort((a,b)=>(t.endDir[b][0]*D[0]+t.endDir[b][1]*D[1])-(t.endDir[a][0]*D[0]+t.endDir[a][1]*D[1])); return t.ends[ids[0]]; }
  return t.ends[ids.reduce((a,b)=>Math.hypot(t.ends[b][0]-at[0],t.ends[b][1]-at[1])<Math.hypot(t.ends[a][0]-at[0],t.ends[a][1]-at[1])?b:a)]; }
// how far (x,z) is from the nearest street centreline of a town; and is it on a street, its sidewalk or a turning circle
function streetDist(t,x,z){ let best=1e9; for(const S of t.segs||[]){ const al=S.X?x:z, ac=S.X?z:x, f=al<S.a?S.a:al>S.b?S.b:al, d=Math.hypot(al-f,ac-S.c); if(d<best) best=d; } return best; }
function streetNear(t,x,z,d){ if(streetDist(t,x,z)<d) return true; for(const b of townBulbs(t)) if(Math.hypot(x-b[0],z-b[1])<BULB_R+d-ROAD_HW) return true; return false; }
// a stretch of street well away from its ends and any junction (for parking)
function streetMid(t,S,x,z,m){ if(!S) return false; const al=S.X?x:z; if(al<S.a+m||al>S.b-m) return false; return !(t.junc||[]).some(J=>Math.hypot(J[0]-x,J[1]-z)<m); }

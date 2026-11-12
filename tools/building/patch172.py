# patch172: bigger towns with a lumpy outline instead of a circle, and streets that aren't a perfect crossroads: a main
# street along the first road in, side streets branching off it staggered (some to the edge, some ending in a turning
# circle), now and then a back lane making a loop. Houses line every street; sidewalks, front paths, stop signs, street
# lights, parked cars and the map all follow the new streets. Points of interest keep their old size and plain ends.
STREETS_JS=open('/home/claude/mg/streets.js').read()
POI_IDX='[3,4,6,8]'
# ---- the outline
rep("""function bakeWorld(o){""","""// the outline of a town: a lumpy, lopsided ring, never wider than t.R (points of interest stay round)
function townRadAt(t,dx,dz){ const sh=t.sh; if(!sh) return t.R; const a=Math.atan2(dz,dx); let s=0;
  for(let k=0;k<sh.length;k+=2) s+=sh[k]*Math.cos((k/2+1)*a+sh[k+1]); return t.R*(0.86+0.14*s); }
function bakeWorld(o){""")
rep("""t.h=Math.max(o.LVL,Math.round(t.avg/o.LVL)*o.LVL); t.R=o.townR; }""",
    """t.h=Math.max(o.LVL,Math.round(t.avg/o.LVL)*o.LVL); const k_=towns.indexOf(t); t.R=typeof o.townR==='function'?o.townR(k_):o.townR; t.sh=o.townShape?o.townShape(k_):null; }""")
rep("""      const k=d<=t.R?1:1-(d-t.R)/26, s=k*k*(3-2*k), q=j*N+i; H0[q]+=(t.h-H0[q])*s; } }""",
    """      const rr=townRadAt(t,du,dv), k=d<=rr?1:Math.max(0,1-(d-rr)/26), s=k*k*(3-2*k), q=j*N+i; H0[q]+=(t.h-H0[q])*s; } }""")
rep("""      for(const t of towns){ const du=u-t.u, dv=v-t.v; if(du*du+dv*dv<(t.R-2)*(t.R-2)){ pin[q]=1; pv[q]=t.h; } }""",
    """      for(const t of towns){ const du=u-t.u, dv=v-t.v; if(Math.sqrt(du*du+dv*dv)<townRadAt(t,du,dv)-2){ pin[q]=1; pv[q]=t.h; } }""")
rep("""for(const t of [A.t,B.t]) if(t&&Math.hypot(u-t.u,v-t.v)<t.R-2){ pin[q]=1; pv[q]=t.h; } }""",
    """for(const t of [A.t,B.t]) if(t&&Math.hypot(u-t.u,v-t.v)<townRadAt(t,u-t.u,v-t.v)-2){ pin[q]=1; pv[q]=t.h; } }""")
rep("""LVL,townR:46,loops:3""","""LVL,townR:k=>%s.includes(k)?46:82,townShape:k=>{ if(%s.includes(k)) return null; const r=seeded(5150+k), a=[0.3+r()*0.25,0.35+r()*0.3,0.18+r()*0.2,0.08+r()*0.12], s=a.reduce((x,y)=>x+y), o=[]; a.forEach(v=>o.push(v/s,r()*6.2832)); return o; },loops:3""" % (POI_IDX,POI_IDX))
rep("""return {x:SPAWN[0]+t.u,z:SPAWN[2]+t.v,R:t.R,h:t.h,""","""return {x:SPAWN[0]+t.u,z:SPAWN[2]+t.v,R:t.R,sh:t.sh,h:t.h,""")
rep("""function townAt(x,z,pad){ for(const t of TOWNS) if(Math.hypot(x-t.x,z-t.z)<t.R+(pad||0)) return t; return null; }""",
    """function townAt(x,z,pad){ for(const t of TOWNS){ const dx=x-t.x, dz=z-t.z; if(Math.abs(dx)<t.R+(pad||0)+1&&Math.abs(dz)<t.R+(pad||0)+1&&Math.hypot(dx,dz)<townRadAt(t,dx,dz)+(pad||0)) return t; } return null; }""")
# ---- the streets, and roads coming in joined to their ends
rep("""{ const rdPts=[];
  for(const t of TOWNS){""",STREETS_JS+"""{ const rdPts=[];
  for(const t of TOWNS){""")
rep("""    t.axis=ax; t.streetL=Math.floor((t.R-4)/CELL)*CELL; const Ls=t.streetL;
    t.ends=[[t.x-Ls,t.z],[t.x+Ls,t.z],[t.x,t.z-Ls],[t.x,t.z+Ls]];""",
    """    t.axis=ax; const tOut=q=>{ const dx=SPAWN[0]+q[0]-t.x, dz=SPAWN[2]+q[1]-t.z; return Math.hypot(dx,dz)>=townRadAt(t,dx,dz)+12; };
    { const arr=[]; for(const rd of WORLD.roads){ if(rd.street) continue; for(const end of [0,1]){ const P=end?rd.pts.slice().reverse():rd.pts; if(Math.hypot(SPAWN[0]+P[0][0]-t.x,SPAWN[2]+P[0][1]-t.z)>4) continue;
        let k=0; while(k<P.length-8&&!tOut(P[k])) k++; arr.push([SPAWN[0]+P[k][0],SPAWN[2]+P[k][1]]); } }
      planStreets(t,arr); }
    const Ls=t.streetL;""")
rep("""        let k=0; while(k<P.length-8&&Math.hypot(SPAWN[0]+P[k][0]-t.x,SPAWN[2]+P[k][1]-t.z)<cut) k++;""",
    """        let k=0; while(k<P.length-8&&!tOut(P[k])) k++;""")
rep("""e=rd.prefEnd&&rd.prefEnd[TOWNS.indexOf(t)]!=null?t.ends[rd.prefEnd[TOWNS.indexOf(t)]]:t.ends.reduce((a,b)=>Math.hypot(b[0]-at[0],b[1]-at[1])<Math.hypot(a[0]-at[0],a[1]-at[1])?b:a);""",
    """e=pickEnd(t,at,rd.prefEnd?rd.prefEnd[TOWNS.indexOf(t)]:null);""")
rep("""ax_=[(e[0]-t.x)/Ls,(e[1]-t.z)/Ls];""","""ax_=t.endDir[t.ends.indexOf(e)];""")
rep("""rr=Math.hypot(cx-t.x,cz-t.z), fr=Math.max(0,Math.min(1,(rr-t.R-1)/Math.max(1,cut-t.R-1))),""",
    """rr=Math.hypot(cx-t.x,cz-t.z), RL=townRadAt(t,cx-t.x,cz-t.z), fr=Math.max(0,Math.min(1,(rr-RL-1)/11)),""")
rep("""      const x=t.x+i*WHS, z=t.z+j*WHS; if((x-t.x)*(x-t.x)+(z-t.z)*(z-t.z)>r2) continue; const c=worldCell(x,z); if(c>=0){ WRD[c]=1e4; WORLD.GRASS[c]=255; } }""",
    """      const x=t.x+i*WHS, z=t.z+j*WHS; if(!townIn(t,x,z,1)) continue; const c=worldCell(x,z); if(c>=0){ WRD[c]=1e4; WORLD.GRASS[c]=255; } }""")
rep("""    if(!t.kind) for(const X of [true,false]){ const pts=[];
      for(let s=-Ls;s<=Ls+0.01;s+=2) pts.push(X?[t.x+s-SPAWN[0],t.z-SPAWN[2],t.h]:[t.x-SPAWN[0],t.z+s-SPAWN[2],t.h]);
      WORLD.roads.push({pts,skip:new Uint8Array(pts.length),street:true,town:t}); }""",
    """    if(!t.kind) for(const S of t.segs){ const pts=[], a=S.a-(S.jA!=null?ROAD_HW_:0), b=S.b+(S.jB!=null?ROAD_HW_:0), n=Math.max(2,Math.ceil((b-a)/2)); // (past a junction by half a road, so corners are closed)
      for(let q=0;q<=n;q++){ const s=a+(b-a)*q/n; pts.push(S.X?[s-SPAWN[0],S.c-SPAWN[2],t.h]:[S.c-SPAWN[0],s-SPAWN[2],t.h]); }
      WORLD.roads.push({pts,skip:new Uint8Array(pts.length),street:true,town:t,seg:S}); }""")
rep("""const WN=WORLD.N, WH=WORLD.H, WRD=WORLD.RD, PLAZA_R=3.6;""","""const WN=WORLD.N, WH=WORLD.H, WRD=WORLD.RD, PLAZA_R=3.6, ROAD_HW_=3.6;""")
rep("""    for(let j=-Math.ceil(t.R/WHS);j<=Math.ceil(t.R/WHS);j++) for(let i=-Math.ceil(t.R/WHS);i<=Math.ceil(t.R/WHS);i++){ const x=t.x+i*WHS, z=t.z+j*WHS; if((x-t.x)*(x-t.x)+(z-t.z)*(z-t.z)>r2) continue; const c=worldCell(x,z); if(c<0) continue; WH[c]=WORLD.H0[c];""",
    """    for(let j=-Math.ceil(t.R/WHS);j<=Math.ceil(t.R/WHS);j++) for(let i=-Math.ceil(t.R/WHS);i<=Math.ceil(t.R/WHS);i++){ const x=t.x+i*WHS, z=t.z+j*WHS; if(!townIn(t,x,z,1)) continue; const c=worldCell(x,z); if(c<0) continue; WH[c]=WORLD.H0[c];""")
rep("""  for(const t of TOWNS) if(!t.kind) for(const X of [true,false]) for(let s=-t.streetL;s<=t.streetL;s+=1) for(let c=-6;c<=6;c+=1){ const cc=worldCell(X?t.x+s:t.x+c,X?t.z+c:t.z+s); if(cc>=0) WORLD.GRASS[cc]=0; } // sidewalks too""",
    """  for(const t of TOWNS) if(!t.kind) for(const S of t.segs) for(let s=S.a-6;s<=S.b+6;s+=1) for(let c=-6;c<=6;c+=1){ if((s<S.a&&S.jA==null)||(s>S.b&&S.jB==null)) continue; const cc=worldCell(S.X?s:S.c+c,S.X?S.c+c:s); if(cc>=0) WORLD.GRASS[cc]=0; } // sidewalks too
  // a street end at the edge of town that no road comes in to runs on as a dirt track, wandering a little and fading into the grass
  for(const t of TOWNS) if(!t.kind) t.ends.forEach((e,k)=>{ if(!t.endEdge[k]||WORLD.roads.some(r=>!r.street&&[r.pts[0],r.pts[r.pts.length-1]].some(p=>Math.hypot(SPAWN[0]+p[0]-e[0],SPAWN[2]+p[1]-e[1])<3))) return;
    const r=seeded(t.seed+k*31+7), L=30+r()*34; let x=e[0], z=e[1], a=Math.atan2(t.endDir[k][1],t.endDir[k][0]), da=(r()-0.5)*0.05; (t.tracks=t.tracks||[]).push([[x,z]]);
    for(let s=0;s<L;s+=0.8){ a+=da; da+=(r()-0.5)*0.016; da*=0.97; x+=Math.cos(a)*0.8; z+=Math.sin(a)*0.8; if(s%4<0.8) t.tracks[t.tracks.length-1].push([x,z]); const f=s<L*0.5?1:1-(s-L*0.5)/(L*0.5);
      for(let w=-2.6;w<=2.6;w+=0.65){ const px=x-Math.sin(a)*w, pz=z+Math.cos(a)*w, c=worldCell(px,pz); if(c<0) continue; const aw=Math.abs(w), rut=Math.abs(aw-0.95)<0.45?1:0.7, v=Math.round(255*f*Math.min(1,(2.7-aw)/1.2)*rut);
        if(v>WORLD.TRACK[c]) WORLD.TRACK[c]=v; const gv=Math.round(255*(1-0.85*f*Math.min(1,(2.7-aw)/1.4))); if(gv<WORLD.GRASS[c]) WORLD.GRASS[c]=gv; } } });""")
# ---- turning circles at any open end with no road
rep("""function townBulbs(t){ if(t.bulbs) return t.bulbs; const Ls=t.streetL;""","""function townBulbs(t){ if(t.bulbs) return t.bulbs;""")
rep("""  return t.bulbs=t.ends.map((e,k)=>{ const ox=(e[0]-t.x)/Ls, oz=(e[1]-t.z)/Ls; return t.dead[k]?""","""  if(t.kind) return t.bulbs=[]; // (a point of interest has no streets: its roads just stop)
  return t.bulbs=t.ends.map((e,k)=>{ const [ox,oz]=t.endDir[k]; return t.dead[k]&&t.endKind[k]==='circle'?""")
# ---- sidewalks: each side of each street, cut where it meets another street; corners go to the earlier street
rep("""  for(const t of TOWNS){ if(t.kind) continue; const Ls=t.streetL, y=t.h+0.045;
    // a sidewalk down each side of both streets
    const bulbs=townBulbs(t), dd=t.dead, cutB=Math.sqrt(BULB_R*BULB_R-ROAD_HW*ROAD_HW)+BULB_IN-0.25; // the sidewalks stop where the turnaround's ring takes over
    for(const X of [true,false]) for(const sd of [-1,1]){ const off=sd*(ROAD_HW+WALK_W/2), c0=dd[X?0:2]?cutB:0, c1=dd[X?1:3]?cutB:0, a=X?[t.x-Ls+c0,t.z+off]:[t.x+off,t.z-Ls+c0], b=X?[t.x+Ls-c1,t.z+off]:[t.x+off,t.z+Ls-c1]; quad(a,b,y,0); SIDEWALKS.push([a,b]); }""",
    """  for(const t of TOWNS){ if(t.kind) continue; const y=t.h+0.045, H=ROAD_HW, Wk=WALK_W;
    // a sidewalk down each side of every street, stopping at the streets it meets (the earlier street keeps the corner)
    const bulbs=townBulbs(t), dd=t.dead, cutB=Math.sqrt(BULB_R*BULB_R-ROAD_HW*ROAD_HW)+BULB_IN-0.25; // the sidewalks stop where the turnaround's ring takes over
    const roadR=S=>{ const a=S.a-(S.jA!=null?H:0), b=S.b+(S.jB!=null?H:0); return S.X?[a,S.c-H,b,S.c+H]:[S.c-H,a,S.c+H,b]; }, got=[];
    t.segs.forEach((S,k)=>{ for(const sd of [-1,1]){
      const ext=E=>S['j'+E]!=null?H+Wk:(S['end'+E]!=null&&t.endKind[S['end'+E]]==='circle')?-cutB:0, c0=S.c+sd*H, c1=S.c+sd*(H+Wk), lo=Math.min(c0,c1), hi=Math.max(c0,c1);
      let iv=[[S.a-ext('A'),S.b+ext('B')]];
      const cutBy=R=>{ const al0=S.X?R[0]:R[1], al1=S.X?R[2]:R[3], ac0=S.X?R[1]:R[0], ac1=S.X?R[3]:R[2]; if(Math.min(hi,ac1)-Math.max(lo,ac0)<0.05) return;
        const nx=[]; for(const [u0,u1] of iv){ if(al1<=u0||al0>=u1){ nx.push([u0,u1]); continue; } if(al0>u0) nx.push([u0,al0]); if(al1<u1) nx.push([al1,u1]); } iv=nx; };
      t.segs.forEach((O,m)=>{ if(m!==k) cutBy(roadR(O)); }); got.forEach(cutBy);
      for(const [u0,u1] of iv){ if(u1-u0<0.4) continue; const m=(c0+c1)/2, a=S.X?[u0,m]:[m,u0], b=S.X?[u1,m]:[m,u1]; quad(a,b,y,0); SIDEWALKS.push([a,b]); got.push(S.X?[u0,lo,u1,hi]:[lo,u0,hi,u1]); } } });
    t.ends.forEach((e,k)=>{ if(t.endKind[k]!=='stub'&&t.endKind[k]!=='fence') return; const [ox,oz]=t.endDir[k], m=[e[0]+ox*Wk/2,e[1]+oz*Wk/2], h=H+Wk, a=[m[0]-oz*h,m[1]-ox*h], b=[m[0]+oz*h,m[1]+ox*h]; quad(a,b,y,0); SIDEWALKS.push([a,b]); }); // the kerb across the end""")
rep("""    for(const h of t.houses){ const D=doorOf(h), a=[D.x+D.nx*0.14,D.z+D.nz*0.14], X=h.side==='n'||h.side==='s', across=X?a[1]-t.z:a[0]-t.x, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
      const b=X?[a[0],t.z+edge]:[t.x+edge,a[1]];""","""    for(const h of t.houses){ const D=doorOf(h), a=[D.x+D.nx*0.14,D.z+D.nz*0.14], X=h.side==='n'||h.side==='s', across=a[X?1:0]-h.sc, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
      const b=X?[a[0],h.sc+edge]:[h.sc+edge,a[1]];""")
rep("""const f=garageFrame(h), m=f.p(2.5,0.02), X=f.X, across=X?m[1]-t.z:m[0]-t.x, edge=Math.sign(across)*(ROAD_HW+0.05);
      const a=[m[0],m[1]], b=X?[m[0],t.z+edge]:[t.x+edge,m[1]];""","""const f=garageFrame(h), m=f.p(2.5,0.02), X=f.X, across=m[X?1:0]-h.sc, edge=Math.sign(across)*(ROAD_HW+0.05);
      const a=[m[0],m[1]], b=X?[m[0],h.sc+edge]:[h.sc+edge,m[1]];""")
# ---- houses along every street
rep("""  for(let a=-12;a<=12;a++) for(let b=-12;b<=12;b++) if(a===-1||a===0||b===-1||b===0) used.add(key(ci+a,cj+b)); // the two streets""",
    """  for(const S of t.segs) for(let a=S.ai-1;a<=S.bi;a++) for(const b of [S.ci-1,S.ci]) used.add(S.X?key(a,b):key(b,a)); // the streets""")
rep("""  const inTown=(i0,j0,w,d)=>[[i0,j0],[i0+w,j0],[i0,j0+d],[i0+w,j0+d]].every(([i,j])=>Math.hypot(i*CELL-t.x,j*CELL-t.z)<t.R-1);""",
    """  const inTown=(i0,j0,w,d)=>[[i0,j0],[i0+w,j0],[i0,j0+d],[i0+w,j0+d]].every(([i,j])=>townIn(t,i*CELL,j*CELL,1));""")
rep("""  const order=t.axis==='z'?[false,true]:[true,false];
  for(const X of order) for(const sd of [1,-1]){ let s=-11;
    while(s<11){ const [along,deep]=shapes[Math.floor(r()*shapes.length)], front=sd>0?TH.set:-TH.set-deep; // a front-yard row between the street and the house
      const i0=X?ci+s:ci+front, j0=X?cj+front:cj+s, w=X?along:deep, d=X?deep:along;
      if(!free(i0,j0,w,d)||!inTown(i0,j0,w,d)){ s++; continue; }""",
    """  for(const S of t.segs) if(!S.hammer) for(const sd of (r()<0.5?[1,-1]:[-1,1])){ let s=S.ai+1; const X=S.X;
    while(s<S.bi){ const [along,deep]=shapes[Math.floor(r()*shapes.length)], set=TH.set+(r()<0.22?1:0), front=sd>0?set:-set-deep; // a front-yard row between the street and the house (some set further back)
      const i0=X?s:S.ci+front, j0=X?S.ci+front:s, w=X?along:deep, d=X?deep:along;
      if(s+along>S.bi||!free(i0,j0,w,d)||!inTown(i0,j0,w,d)){ s++; continue; }""")
rep("""      out.push({i0,j0,w,d,L,side,mat,roof,floors,id:t.houses.length+out.length,""","""      out.push({i0,j0,w,d,L,side,mat,roof,floors,sc:S.c,id:t.houses.length+out.length,""")
rep("""      s+=along+TH.gap; } }
  t.houses=out; return out;""","""      s+=along+TH.gap+(r()<0.25?1:0); } }
  t.houses=out; return out;""")
# ---- yards and gardens keep off the streets they now front
rep("""  for(const h of t.houses){ const D=doorOf(h), X=h.side==='n'||h.side==='s', across=X?D.z-t.z:D.x-t.x, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
    if(seg(D.x,D.z,X?D.x:t.x+edge,X?t.z+edge:D.z,WALK_W)) return true;
    if(h.garage){ const f=garageFrame(h), m=f.p(2.5,0.02), a2=f.X?m[1]-t.z:m[0]-t.x, e2=Math.sign(a2)*(ROAD_HW+0.05); if(seg(m[0],m[1],f.X?m[0]:t.x+e2,f.X?t.z+e2:m[1],3.4)) return true; } }
  return Math.abs(x-t.x)<ROAD_HW+WALK_W+pad||Math.abs(z-t.z)<ROAD_HW+WALK_W+pad; }""",
    """  for(const h of t.houses){ const D=doorOf(h), X=h.side==='n'||h.side==='s', across=(X?D.z:D.x)-h.sc, edge=Math.sign(across)*(ROAD_HW+WALK_W-0.1);
    if(seg(D.x,D.z,X?D.x:h.sc+edge,X?h.sc+edge:D.z,WALK_W)) return true;
    if(h.garage){ const f=garageFrame(h), m=f.p(2.5,0.02), a2=(f.X?m[1]:m[0])-h.sc, e2=Math.sign(a2)*(ROAD_HW+0.05); if(seg(m[0],m[1],f.X?m[0]:h.sc+e2,f.X?h.sc+e2:m[1],3.4)) return true; } }
  return streetNear(t,x,z,ROAD_HW+WALK_W+pad); }""")
rep("""  const free=(t,x,z,pad)=>{ if(Math.hypot(x-t.x,z-t.z)>t.R+6) return false; if(Math.abs(x-t.x)<ROAD_HW+WALK_W+1.4||Math.abs(z-t.z)<ROAD_HW+WALK_W+1.4) return false;""",
    """  const free=(t,x,z,pad)=>{ if(!townIn(t,x,z,-6)) return false; if(streetNear(t,x,z,ROAD_HW+WALK_W+1.4)) return false;""")
rep("""(X?Math.abs((h.side==='n'?h.j0*CELL:(h.j0+h.d)*CELL)-t.z):Math.abs((h.side==='w'?h.i0*CELL:(h.i0+h.w)*CELL)-t.x))-(ROAD_HW+WALK_W)-0.45);""",
    """(X?Math.abs((h.side==='n'?h.j0*CELL:(h.j0+h.d)*CELL)-h.sc):Math.abs((h.side==='w'?h.i0*CELL:(h.i0+h.w)*CELL)-h.sc))-(ROAD_HW+WALK_W)-0.45);""")
# ---- parked cars: along a street, clear of its ends and junctions
rep("""const tw=rd.town, dc=Math.hypot(x-tw.x,z-tw.z); if(kerb>=16||(perTown.get(tw)||0)>=2||dc<11||dc>tw.streetL-12||!roomy(x,z,'car')) continue;""",
    """const tw=rd.town; if(kerb>=16||(perTown.get(tw)||0)>=2||!streetMid(tw,rd.seg,x,z,12)||!roomy(x,z,'car')) continue;""")
# ---- town signs: distance to the middle of town
rep("""const dist=Math.round((arc+t.streetL)/10)*10,""","""const dist=Math.round((arc+Math.hypot(ex-t.x,ez-t.z))/10)*10,""")
# ---- stop signs where a side street meets a through street; street lights along every street
rep("""    for(const [ox,oz] of [[1,0],[-1,0],[0,1],[0,-1]]){ const hx=-ox, hz=-oz, x=t.x+ox*(ROAD_HW+2.3)-hz*(ROAD_HW+0.6), z=t.z+oz*(ROAD_HW+2.3)+hx*(ROAD_HW+0.6), yaw=Math.atan2(ox,oz);""",
    """    const arms=[]; t.segs.forEach(S=>{ for(const E of ['A','B']){ const m=S['j'+E]; if(m==null) continue; const O=t.segs[m]; if(O.hammer||!(S.c>O.a+0.1&&S.c<O.b-0.1)) continue; // a through street: the side street stops
        const g=E==='A'?S.a:S.b, d=E==='A'?1:-1; arms.push([S.X?g:S.c,S.X?S.c:g,S.X?d:0,S.X?0:d]); } });
    for(const [jx,jz,ox,oz] of arms){ const hx=-ox, hz=-oz, x=jx+ox*(ROAD_HW+2.3)-hz*(ROAD_HW+0.6), z=jz+oz*(ROAD_HW+2.3)+hx*(ROAD_HW+0.6), yaw=Math.atan2(ox,oz);""")
rep("""    for(const X of [true,false]) for(const s0 of [-29,-15,15,29]){ const sd=(s0>0)!==(Math.abs(s0)>20)?1:-1, ac=sd*(ROAD_HW+WALK_W+0.4); let s=s0, ok=false;
      for(let tr=0;tr<5&&!ok;tr++,s+=Math.sign(s0)*-2.3){ const x=X?t.x+s:t.x+ac, z=X?t.z+ac:t.z+s;""",
    """    for(const S of t.segs){ if(S.hammer) continue; const X=S.X, n0=Math.floor((S.b-S.a-14)/14); if(n0<1) continue; const step=(S.b-S.a-14)/n0;
     for(let q=0;q<=n0;q++){ const s0=S.a+7+q*step, sd=q%2?1:-1, ac=S.c+sd*(ROAD_HW+WALK_W+0.4); let s=s0, ok=false;
      for(let tr=0;tr<5&&!ok;tr++,s+=(tr%2?1:-1)*tr*2.3){ const x=X?s:ac, z=X?ac:s; if((t.junc||[]).some(J=>Math.hypot(J[0]-x,J[1]-z)<9)||townBulbs(t).some(b=>Math.hypot(b[0]-x,b[1]-z)<BULB_R+WALK_W+1.2)) continue;""")
rep("""const hd=new THREE.BoxGeometry(X?0.3:0.62,0.13,X?0.62:0.3); hd.translate(x+ix*1.5,t.h+4.8,z+iz*1.5); dark.push(hd); const gl=new THREE.BoxGeometry(X?0.22:0.5,0.05,X?0.5:0.22); gl.translate(x+ix*1.5,t.h+4.715,z+iz*1.5); pale.push(gl); } } }""",
    """const hd=new THREE.BoxGeometry(X?0.3:0.62,0.13,X?0.62:0.3); hd.translate(x+ix*1.5,t.h+4.8,z+iz*1.5); dark.push(hd); const gl=new THREE.BoxGeometry(X?0.22:0.5,0.05,X?0.5:0.22); gl.translate(x+ix*1.5,t.h+4.715,z+iz*1.5); pale.push(gl);
        STATICS.push({x,z,solid:{boxes:[[x-0.15,t.h,z-0.15,x+0.15,t.h+4.9,z+0.15]],key:'lamp'+STATICS.length}}); } } } }""")
# ---- the maps: fill the junctions, not a disc at the middle of town
rep("""g.beginPath(); g.arc(tx(t.x),tz(t.z),(PLAZA_R+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); for(const b of townBulbs(t))""",
    """for(const J of t.junc||[]){ g.beginPath(); g.arc(tx(J[0]),tz(J[1]),(ROAD_HW+(w-ROAD_HW*2)/2)*sc,0,7); g.fill(); } for(const b of townBulbs(t))""")
rep("""    g.fillStyle=col; WORLD.towns.forEach(t=>{ g.beginPath(); g.arc(X(t.u),X(t.v),(PLAZA_R/mpp)+w/2+1,0,7); g.fill(); });""",
    """    g.fillStyle=col; TOWNS.forEach(t=>(t.junc||[]).forEach(J=>{ g.beginPath(); g.arc(X(J[0]-SPAWN[0]),X(J[1]-SPAWN[2]),w/2,0,7); g.fill(); }));""")
# ---- a fenced end: a wooden rail fence across the end of the street, with a striped road-ends board on it
rep("""  for(const t of TOWNS){ townBulbs(t); if(t.kind) continue;
    const arms=[];""","""  const fenceW=[];
  for(const t of TOWNS){ townBulbs(t); if(t.kind) continue;
    t.ends.forEach((e,k)=>{ if(t.endKind[k]!=='fence') return; const [ox,oz]=t.endDir[k], px=-oz, pz=ox, L=ROAD_HW+WALK_W+0.3, fx=e[0]+ox*(WALK_W+0.7), fz=e[1]+oz*(WALK_W+0.7), yaw=Math.atan2(ox,oz), y=t.h;
      const n=Math.ceil(2*L/1.5); for(let q=0;q<=n;q++){ const u=-L+2*L*q/n; post(fenceW,fx+px*u,y,fz+pz*u,1.25,yaw,0.15); }
      for(const h of [0.55,1.05]){ const g=new THREE.BoxGeometry(2*L+0.2,0.13,0.06); g.rotateY(yaw+Math.PI/2); g.translate(fx,y+h,fz); fenceW.push(g); }
      for(let u=-L;u<L-0.01;u+=2*L/Math.ceil(2*L/2.2)){ const u1=Math.min(L,u+2*L/Math.ceil(2*L/2.2)), ax=fx+px*u, az=fz+pz*u, bx=fx+px*u1, bz=fz+pz*u1;
        STATICS.push({x:(ax+bx)/2,z:(az+bz)/2,solid:{boxes:[[Math.min(ax,bx)-0.12,y,Math.min(az,bz)-0.12,Math.max(ax,bx)+0.12,y+1.25,Math.max(az,bz)+0.12]],key:'fence'+STATICS.length}}); }
      const f=face('roadend',512,128,(g,w,h)=>{ g.fillStyle='#f2c418'; g.fillRect(0,0,w,h); g.fillStyle='#17181b'; for(let x=-h;x<w+h;x+=64){ g.beginPath(); g.moveTo(x,h); g.lineTo(x+32,h); g.lineTo(x+32+h,0); g.lineTo(x+h,0); g.closePath(); g.fill(); } });
      board(f,new THREE.PlaneGeometry(2.4,0.6),fx-ox*0.06,y+0.8,fz-oz*0.06,Math.atan2(-ox,-oz)); });
    const arms=[];""")
rep("""  add(grey,new THREE.MeshLambertMaterial({color:0x8d939a}));""","""  add(fenceW,new THREE.MeshLambertMaterial({color:0x7a5a3c})); add(grey,new THREE.MeshLambertMaterial({color:0x8d939a}));""")

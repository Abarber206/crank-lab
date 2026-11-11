/* ---------- world generation: deterministic everywhere ----------
   Only integer hashing (Math.imul), + - * / and Math.sqrt/floor, which every browser computes bit-for-bit the same,
   so every player in a party builds exactly the same mountains, towns and roads. */
const GR16=[1,0,0.92388,0.382683,0.707107,0.707107,0.382683,0.92388,0,1,-0.382683,0.92388,-0.707107,0.707107,-0.92388,0.382683,
  -1,0,-0.92388,-0.382683,-0.707107,-0.707107,-0.382683,-0.92388,0,-1,0.382683,-0.92388,0.707107,-0.707107,0.92388,-0.382683];
function ihash(x,z,s){ let h=(Math.imul(x,374761393)+Math.imul(z,668265263)+Math.imul(s,1442695041))|0; h=Math.imul(h^(h>>>13),1274126177); return (h^(h>>>16))&15; }
// 2D gradient noise, roughly -1..1
function gnoise(x,z,s){
  const ix=Math.floor(x), iz=Math.floor(z), fx=x-ix, fz=z-iz;
  let k=ihash(ix,iz,s)*2; const n00=GR16[k]*fx+GR16[k+1]*fz;
  k=ihash(ix+1,iz,s)*2; const n10=GR16[k]*(fx-1)+GR16[k+1]*fz;
  k=ihash(ix,iz+1,s)*2; const n01=GR16[k]*fx+GR16[k+1]*(fz-1);
  k=ihash(ix+1,iz+1,s)*2; const n11=GR16[k]*(fx-1)+GR16[k+1]*(fz-1);
  const ux=fx*fx*fx*(fx*(fx*6-15)+10), uz=fz*fz*fz*(fz*(fz*6-15)+10);
  const a=n00+(n10-n00)*ux, b=n01+(n11-n01)*ux; return (a+(b-a)*uz)*1.42; }
// fractal sum; each octave is rotated so the grid never lines up
function fbm(x,z,oct,s){ let t=0, a=0.5, sum=0;
  for(let i=0;i<oct;i++){ t+=a*gnoise(x,z,s+i*131); sum+=a; const nx=x*1.6-z*1.2, nz=x*1.2+z*1.6; x=nx+17.31; z=nz-9.17; a*=0.5; } return t/sum; }
// ridged multifractal: sharp crests, with detail that only builds up high on the ridges (smooth valleys, like erosion)
function ridged(x,z,oct,s,gain=0.52){ let t=0, a=0.5, w=1, sum=0;
  for(let i=0;i<oct;i++){ let n=gnoise(x,z,s+i*131); n=1-(n<0?-n:n); n*=n; n*=w; w=n*1.8; if(w>1) w=1; t+=n*a; sum+=a;
    const nx=x*1.66-z*1.18, nz=x*1.18+z*1.66; x=nx+5.13; z=nz+11.7; a*=gain; } return t/sum; }
const sstep=(e0,e1,x)=>{ let t=(x-e0)/(e1-e0); t=t<0?0:t>1?1:t; return t*t*(3-2*t); };

function makeWorldGen(o){
  const {FLAT_R,MAP_R}=o;
  // mountain ranges inside the map: seeded ridgelines (a segment each), away from spawn and from each other
  const MASSIFS=[]; { const r=o.rng(31337); let tries=0;
    while(MASSIFS.length<o.massifs&&tries<600){ tries++;
      const u=(r()*2-1)*(MAP_R-220), v=(r()*2-1)*(MAP_R-220), d=Math.sqrt(u*u+v*v); if(d<310||d>MAP_R-200) continue;
      // the ridgeline runs roughly around the island (tangent), tilted a little
      let tx=-v/d, tz=u/d; const tw=(r()-0.5)*1.2; const ax=tx+tz*tw, az=tz-tx*tw, al=Math.sqrt(ax*ax+az*az); tx=ax/al; tz=az/al;
      const L=110+r()*150, R=95+r()*55;
      const m={u,v,ax:u-tx*L,az:v-tz*L,bx:u+tx*L,bz:v+tz*L,R,P:95+r()*75,ox:r()*100,oz:r()*100};
      if(MASSIFS.some(q=>{ const dx=q.u-u, dz=q.v-v; return Math.sqrt(dx*dx+dz*dz)<L+R+q.R+150; })) continue;
      const pad=R*2.25+40; m.minx=Math.min(m.ax,m.bx)-pad; m.maxx=Math.max(m.ax,m.bx)+pad; m.minz=Math.min(m.az,m.bz)-pad; m.maxz=Math.max(m.az,m.bz)+pad;
      MASSIFS.push(m); } }
  function genH(u,v){
    const d=Math.sqrt(u*u+v*v);
    if(d<=FLAT_R) return 0;
    const s=sstep(FLAT_R,FLAT_R+55,d), far=sstep(60,260,d);
    // rolling hills (gentle near the middle) and broad valleys
    let h=10+(8+16*far)*fbm(u*0.0034+11.3,v*0.0034-4.7,4,1)+(2.5+3*far)*fbm(u*0.012,v*0.012,3,2)+12*far*fbm(u*0.0013,v*0.0013,2,3);
    // ranges: a ridged crest along a warped ridgeline, with foothills spreading out from it
    for(let i=0;i<MASSIFS.length;i++){ const M=MASSIFS[i];
      if(u<M.minx||u>M.maxx||v<M.minz||v>M.maxz) continue;
      const wu=u+35*fbm(u*0.006,v*0.006,2,40+i), wv=v+35*fbm(u*0.006+7.7,v*0.006,2,50+i);
      const ex=M.bx-M.ax, ez=M.bz-M.az; let t=((wu-M.ax)*ex+(wv-M.az)*ez)/(ex*ex+ez*ez); t=t<0?0:t>1?1:t;
      const qx=wu-(M.ax+ex*t), qz=wv-(M.az+ez*t), dd=Math.sqrt(qx*qx+qz*qz)/(M.R*(1+0.35*(t*(1-t)*4)));
      if(dd<1.6){ const k1=dd<1?1-dd:0, core=k1*k1*(3-2*k1), foot=sstep(1.6,0.2,dd), along=0.55+0.45*(4*t*(1-t));
        h+=M.P*along*(core*core*(0.25+1.1*ridged(u/210+M.ox,v/210+M.oz,6,60+i*7,0.47))+0.22*foot); } }
    // the outer range: big ridged mountains (long crests, deep valleys) that close the island in
    const de=d+70*fbm(u*0.002,v*0.002,2,20), oR=sstep(MAP_R-130,MAP_R+300,de);
    if(oR>0){ const wu=u+90*fbm(u*0.0012,v*0.0012,2,22), wv=v+90*fbm(u*0.0012+3.3,v*0.0012,2,23);
      h+=oR*(50+(170+230*oR)*ridged(wu*0.0016,wv*0.0016,6,21,0.44)); }
    h*=s; return h<0?0:h; }
  return {genH,MASSIFS};
}

/* ---------- baking the playable area into a heightfield, with towns and roads ----------
   One 2 m grid over the whole island: the ground mesh, physics, grass and props all read the same numbers. */
function bakeWorld(o){
  const {genH,MASSIFS}=o.gen, HS=o.HS, HALF=o.HALF, N=Math.round(2*HALF/HS)+1, FLAT_R=o.FLAT_R, MAP_R=o.MAP_R;
  const H0=new Float32Array(N*N);
  for(let j=0;j<N;j++){ const v=-HALF+j*HS; for(let i=0;i<N;i++) H0[j*N+i]=genH(-HALF+i*HS,v); }
  const at=(A,u,v)=>{ let fx=(u+HALF)/HS, fz=(v+HALF)/HS; fx=fx<0?0:fx>N-1.001?N-1.001:fx; fz=fz<0?0:fz>N-1.001?N-1.001:fz;
    const i=Math.floor(fx), j=Math.floor(fz), tx=fx-i, tz=fz-j, k=j*N+i; return (A[k]*(1-tx)+A[k+1]*tx)*(1-tz)+(A[k+N]*(1-tx)+A[k+N+1]*tx)*tz; };
  // ---- towns: the flattest lowland spots, well spread out
  const towns=[]; { const r=o.rng(4711), cands=[];
    for(let k=0;k<1400;k++){ const u=(r()*2-1)*(MAP_R-170), v=(r()*2-1)*(MAP_R-170), d=Math.sqrt(u*u+v*v); if(d<170||d>MAP_R-170) continue;
      let lo=1e9, hi=-1e9, sum=0, n=0;
      for(let s=0;s<17;s++){ const rr=s===0?0:s<9?22:40, k8=s%8, ox=[1,0.7071,0,-0.7071,-1,-0.7071,0,0.7071][k8], oz=[0,0.7071,1,0.7071,0,-0.7071,-1,-0.7071][k8];
        const h=at(H0,u+ox*rr,v+oz*rr); lo=Math.min(lo,h); hi=Math.max(hi,h); sum+=h; n++; }
      if(hi-lo>10||sum/n>55) continue;
      if(MASSIFS.some(M=>{ const ex=M.bx-M.ax, ez=M.bz-M.az; let t2=((u-M.ax)*ex+(v-M.az)*ez)/(ex*ex+ez*ez); t2=t2<0?0:t2>1?1:t2; const qx=u-(M.ax+ex*t2), qz=v-(M.az+ez*t2); return Math.sqrt(qx*qx+qz*qz)<M.R*1.7; })) continue;
      cands.push({u,v,score:(hi-lo)+r()*3,avg:sum/n}); }
    cands.sort((A,B)=>A.score-B.score||A.u-B.u);
    for(const c of cands){ if(towns.length>=o.towns) break; if(towns.some(t=>{ const dx=t.u-c.u, dz=t.v-c.v; return Math.sqrt(dx*dx+dz*dz)<o.townGap; })) continue; towns.push(c); } }
  // ---- level the towns
  for(const t of towns){ if(o.snap){ const q=o.snap(t.u,t.v); t.u=q[0]; t.v=q[1]; } t.h=Math.max(o.LVL,Math.round(t.avg/o.LVL)*o.LVL); t.R=o.townR; }
  for(const t of towns){ const E=t.R+26, i0=Math.max(0,Math.floor((t.u-E+HALF)/HS)), i1=Math.min(N-1,Math.ceil((t.u+E+HALF)/HS)), j0=Math.max(0,Math.floor((t.v-E+HALF)/HS)), j1=Math.min(N-1,Math.ceil((t.v+E+HALF)/HS));
    for(let j=j0;j<=j1;j++) for(let i=i0;i<=i1;i++){ const du=-HALF+i*HS-t.u, dv=-HALF+j*HS-t.v, d=Math.sqrt(du*du+dv*dv); if(d>=E) continue;
      const k=d<=t.R?1:1-(d-t.R)/26, s=k*k*(3-2*k), q=j*N+i; H0[q]+=(t.h-H0[q])*s; } }
  // ---- roads: towns (and the build field in the middle) joined by a minimum spanning tree plus a couple of loops
  const nodes=towns.map((t,i)=>({u:t.u,v:t.v,town:t}));
  const dist=(a,b)=>{ const dx=a.u-b.u, dz=a.v-b.v; return Math.sqrt(dx*dx+dz*dz); };
  const edges=[]; { const inT=[0], out=new Set(nodes.map((n,i)=>i)); out.delete(0);
    while(out.size){ let best=null; for(const a of inT) for(const b of out){ const d=dist(nodes[a],nodes[b]); if(!best||d<best[2]-1e-9) best=[a,b,d]; } edges.push(best); inT.push(best[1]); out.delete(best[1]); }
    const extra=[]; for(let a=0;a<nodes.length;a++) for(let b=a+1;b<nodes.length;b++){ if(edges.some(e=>e[0]===a&&e[1]===b||e[0]===b&&e[1]===a)) continue; const d=dist(nodes[a],nodes[b]); if(d<o.loopMax) extra.push([a,b,d]); }
    extra.sort((x,y)=>x[2]-y[2]); edges.push(...extra.slice(0,o.loops));
    // and one road from the build field in the middle to the nearest town
    const F={u:0,v:0,field:true}; nodes.push(F); let nb=0; for(let k=1;k<towns.length;k++) if(dist(F,nodes[k])<dist(F,nodes[nb])) nb=k; edges.unshift([nodes.length-1,nb,dist(F,nodes[nb])]); }
  // A* over an 8 m grid: climbing is expensive, steep is very expensive, other towns are avoided, existing roads are cheap
  const AG=4, M=Math.floor((N-1)/AG)+1, gh=new Float32Array(M*M), onRoad=new Uint8Array(M*M), avoid=new Float32Array(M*M);
  for(let j=0;j<M;j++) for(let i=0;i<M;i++){ gh[j*M+i]=H0[(j*AG)*N+i*AG]; const u=-HALF+i*AG*HS, v=-HALF+j*AG*HS, d=Math.sqrt(u*u+v*v); avoid[j*M+i]=d>MAP_R-40?-1:d<FLAT_R+2?300:0; }
  const RD=new Float32Array(N*N).fill(1e4), RY=new Float32Array(N*N);
  const roads=[];
  function astar(si,sj,ei,ej,ownT){
    const G=new Float64Array(M*M).fill(Infinity), from=new Int32Array(M*M).fill(-1), closed=new Uint8Array(M*M);
    const heap=[], push=(f,k)=>{ heap.push([f,k]); let c=heap.length-1; while(c>0){ const p=(c-1)>>1; if(heap[p][0]<heap[c][0]||heap[p][0]===heap[c][0]&&heap[p][1]<heap[c][1]) break; [heap[p],heap[c]]=[heap[c],heap[p]]; c=p; } },
      pop=()=>{ const top=heap[0], last=heap.pop(); if(heap.length){ heap[0]=last; let c=0; for(;;){ const l=c*2+1, r2=l+1; let m=c; for(const q of [l,r2]) if(q<heap.length&&(heap[q][0]<heap[m][0]||heap[q][0]===heap[m][0]&&heap[q][1]<heap[m][1])) m=q; if(m===c) break; [heap[m],heap[c]]=[heap[c],heap[m]]; c=m; } } return top; };
    const s=sj*M+si, e=ej*M+ei, hd=(i,j)=>{ const dx=(i-ei)*AG*HS, dz=(j-ej)*AG*HS; return Math.sqrt(dx*dx+dz*dz)*0.6; };
    G[s]=0; push(hd(si,sj),s);
    const D8=[[1,0,8],[-1,0,8],[0,1,8],[0,-1,8],[1,1,11.3137],[1,-1,11.3137],[-1,1,11.3137],[-1,-1,11.3137]];
    while(heap.length){ const [,k]=pop(); if(closed[k]) continue; closed[k]=1; if(k===e) break; const i=k%M, j=(k-i)/M;
      for(const [di,dj,L] of D8){ const ni=i+di, nj=j+dj; if(ni<0||nj<0||ni>=M||nj>=M) continue; const nk=nj*M+ni; if(closed[nk]||avoid[nk]<0) continue;
        const g=Math.abs(gh[nk]-gh[k])/L; let c=L*(1+70*g*g)+(g>0.13?L*400*(g-0.13):0)+(nk!==e?avoid[nk]:0);
        const tw=townCell[nk]; if(tw&&tw!==ownT[0]&&tw!==ownT[1]) c+=2500;
        if(onRoad[nk]) c*=0.55;
        const ng=G[k]+c; if(ng<G[nk]){ G[nk]=ng; from[nk]=k; push(ng+hd(ni,nj),nk); } } }
    const path=[]; for(let k=e;k>=0;k=from[k]){ path.push(k); if(k===s) break; } return path.reverse(); }
  const townCell=new Array(M*M).fill(null);
  for(const t of towns){ for(let j=0;j<M;j++) for(let i=0;i<M;i++){ const du=-HALF+i*AG*HS-t.u, dv=-HALF+j*AG*HS-t.v; if(du*du+dv*dv<(t.R+10)*(t.R+10)) townCell[j*M+i]=t; } }
  const gi=u=>Math.round((u+HALF)/(AG*HS));
  for(const [a,b] of edges){ const A=nodes[a], B=nodes[b];
    let au=A.u, av=A.v; if(A.field){ const d=dist(A,B); au=B.u/d*(FLAT_R+6); av=B.v/d*(FLAT_R+6); }
    let bu=B.u, bv=B.v; if(B.field){ const d=dist(A,B); bu=A.u/d*(FLAT_R+6); bv=A.v/d*(FLAT_R+6); }
    const path=astar(gi(au),gi(av),gi(bu),gi(bv),[A.town||null,B.town||null]); if(path.length<2) continue;
    // grid path -> smooth centreline every 2 m: thin, Chaikin-round, resample
    let pts=path.map(k=>{ const i=k%M, j=(k-i)/M; return [-HALF+i*AG*HS,-HALF+j*AG*HS]; });
    pts[0]=[au,av]; pts[pts.length-1]=[bu,bv];
    const thin=[pts[0]]; for(let q=2;q<pts.length-1;q+=2) thin.push(pts[q]); thin.push(pts[pts.length-1]); pts=thin;
    for(let it=0;it<4;it++){ const nx=[pts[0]]; for(let q=0;q<pts.length-1;q++){ const p=pts[q], n=pts[q+1]; nx.push([p[0]*0.75+n[0]*0.25,p[1]*0.75+n[1]*0.25],[p[0]*0.25+n[0]*0.75,p[1]*0.25+n[1]*0.75]); } nx.push(pts[pts.length-1]); pts=nx; }
    const rs=[pts[0]]; let acc=0; for(let q=1;q<pts.length;q++){ let [x0,z0]=rs[rs.length-1]; const [x1,z1]=pts[q]; let dx=x1-x0, dz=z1-z0, L=Math.sqrt(dx*dx+dz*dz);
      while(L>=2){ x0+=dx/L*2; z0+=dz/L*2; rs.push([x0,z0]); dx=x1-x0; dz=z1-z0; L=Math.sqrt(dx*dx+dz*dz); } }
    if(rs.length<3) continue;
    // height profile: follow the ground, smoothed and graded; pinned flat in towns and where it meets an earlier road
    const n=rs.length, y=new Float32Array(n), pin=new Int8Array(n), pv=new Float32Array(n);
    for(let q=0;q<n;q++){ const [u,v]=rs[q]; y[q]=at(H0,u,v);
      for(const t of towns){ const du=u-t.u, dv=v-t.v; if(du*du+dv*dv<(t.R-2)*(t.R-2)){ pin[q]=1; pv[q]=t.h; } }
      if(!pin[q]&&at(RD,u,v)<3){ pin[q]=1; pv[q]=at(RY,u,v); }
      if(Math.sqrt(u*u+v*v)<FLAT_R+1){ pin[q]=1; pv[q]=0; } }
    const repin=()=>{ for(let q=0;q<n;q++) if(pin[q]) y[q]=pv[q]; }; repin();
    const tmp=new Float32Array(n);
    for(let pass=0;pass<8;pass++){ for(let q=0;q<n;q++){ let s2=0, c2=0; for(let w=-10;w<=10;w++){ const z=q+w; if(z<0||z>=n) continue; s2+=y[z]; c2++; } tmp[q]=s2/c2; } y.set(tmp); repin(); }
    for(let pass=0;pass<4;pass++){ const g=o.maxGrade*2; for(let q=1;q<n;q++){ if(y[q]>y[q-1]+g) y[q]=y[q-1]+g; if(y[q]<y[q-1]-g) y[q]=y[q-1]-g; } for(let q=n-2;q>=0;q--){ if(y[q]>y[q+1]+g) y[q]=y[q+1]+g; if(y[q]<y[q+1]-g) y[q]=y[q+1]-g; } repin(); }
    const road={pts:rs.map((p,q)=>[p[0],p[1],y[q]]),skip:new Uint8Array(n)};
    for(let q=0;q<n;q++) if(at(RD,rs[q][0],rs[q][1])<2.2) road.skip[q]=1; // already paved by an earlier road
    // carve: nearest distance to this road's segments (and the road height there) for every cell around it
    const R2=o.roadW+o.blendMax;
    for(let q=0;q<n-1;q++){ const [x0,z0]=rs[q], [x1,z1]=rs[q+1], ex=x1-x0, ez=z1-z0, el=ex*ex+ez*ez;
      const i0=Math.max(0,Math.floor((Math.min(x0,x1)-R2+HALF)/HS)), i1=Math.min(N-1,Math.ceil((Math.max(x0,x1)+R2+HALF)/HS)), j0=Math.max(0,Math.floor((Math.min(z0,z1)-R2+HALF)/HS)), j1=Math.min(N-1,Math.ceil((Math.max(z0,z1)+R2+HALF)/HS));
      for(let j=j0;j<=j1;j++){ const pz=-HALF+j*HS; for(let i=i0;i<=i1;i++){ const px=-HALF+i*HS; let t2=((px-x0)*ex+(pz-z0)*ez)/el; t2=t2<0?0:t2>1?1:t2;
        const qx=px-(x0+ex*t2), qz=pz-(z0+ez*t2), dd=Math.sqrt(qx*qx+qz*qz), c=j*N+i; if(dd<RD[c]){ RD[c]=dd; RY[c]=y[q]+(y[q+1]-y[q])*t2; } } } }
    for(let q=0;q<n;q+=2){ const i=gi(rs[q][0]), j=gi(rs[q][1]); if(i>=0&&j>=0&&i<M&&j<M) onRoad[j*M+i]=1; }
    roads.push(road); }
  // final heights: flat across the road, then cut or fill back to the ground (longer where the drop is bigger)
  const H=new Float32Array(H0);
  for(let c=0;c<N*N;c++){ const dd=RD[c]; if(dd>=o.roadW+o.blendMax) continue; const y=RY[c], h0=H0[c], diff=h0>y?h0-y:y-h0;
    if(dd<=o.roadW){ H[c]=y; continue; } let B=diff*1.6; B=B<6?6:B>o.blendMax?o.blendMax:B; if(dd>=o.roadW+B) continue;
    let t=(dd-o.roadW)/B; t=t*t*(3-2*t); H[c]=y+(h0-y)*t; }
  // ground cover per cell: bare rock on steep faces and high up, snow above a wavy snowline, grass elsewhere (not on roads)
  const ROCK=new Uint8Array(N*N), SNOW=new Uint8Array(N*N), GRASS=new Uint8Array(N*N);
  for(let j=0;j<N;j++) for(let i=0;i<N;i++){ const c=j*N+i, h=H[c], gx=(H[j*N+(i<N-1?i+1:i)]-H[j*N+(i>0?i-1:i)])/(2*HS), gz=(H[(j<N-1?j+1:j)*N+i]-H[(j>0?j-1:j)*N+i])/(2*HS), ny=1/Math.sqrt(1+gx*gx+gz*gz);
    const rock=Math.min(1,sstep(0.87,0.7,ny)+0.7*sstep(175,240,h)), line=168+26*gnoise((-HALF+i*HS)*0.011,(-HALF+j*HS)*0.011,77), snow=sstep(line,line+24,h)*sstep(0.58,0.78,ny);
    ROCK[c]=Math.round(rock*255); SNOW[c]=Math.round(snow*255); GRASS[c]=RD[c]<4.8?0:Math.round((1-rock)*(1-snow)*255); }
  return {N,H0,H,RD,ROCK,SNOW,GRASS,at,towns,roads,edges:edges.length};

}

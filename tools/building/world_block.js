/* ---------- world: a 1.6 km island of rolling hills and mountain ranges, with ten towns joined by roads ---------- */
@@GEN@@
const FLAT_R=42, MAP_R=800, WHALF=832, WHS=2; // you can walk up to the foot of the outer range, no further
const WGEN=makeWorldGen({FLAT_R,MAP_R,massifs:4,rng:seeded}), genH=WGEN.genH;
const WORLD=bakeWorld({gen:WGEN,HS:WHS,HALF:WHALF,FLAT_R,MAP_R,rng:seeded,towns:10,townGap:210,LVL,townR:46,loops:3,loopMax:520,maxGrade:0.1,roadW:6,blendMax:34,
  snap:(u,v)=>[Math.round((SPAWN[0]+u)/CELL)*CELL-SPAWN[0],Math.round((SPAWN[2]+v)/CELL)*CELL-SPAWN[2]]});
const WN=WORLD.N, WH=WORLD.H, WRD=WORLD.RD, PLAZA_R=3.6;
// height anywhere: the baked 2 m grid inside the island, the generator itself out beyond it
function terrainH(x,z){ const fx=(x-SPAWN[0]+WHALF)/WHS, fz=(z-SPAWN[2]+WHALF)/WHS;
  if(!(fx>=0&&fz>=0&&fx<WN-1&&fz<WN-1)) return genH(x-SPAWN[0],z-SPAWN[2]);
  const i=fx|0, j=fz|0, tx=fx-i, tz=fz-j, k=j*WN+i; return (WH[k]*(1-tx)+WH[k+1]*tx)*(1-tz)+(WH[k+WN]*(1-tx)+WH[k+WN+1]*tx)*tz; }
// distance to the nearest road centreline (large away from roads)
function roadDistAt(x,z){ const fx=(x-SPAWN[0]+WHALF)/WHS, fz=(z-SPAWN[2]+WHALF)/WHS;
  if(!(fx>=0&&fz>=0&&fx<WN-1&&fz<WN-1)) return 1e4;
  const i=fx|0, j=fz|0, tx=fx-i, tz=fz-j, k=j*WN+i; return (WRD[k]*(1-tx)+WRD[k+1]*tx)*(1-tz)+(WRD[k+WN]*(1-tx)+WRD[k+WN+1]*tx)*tz; }
// the nearest grid cell (for ground cover), or -1 outside the baked area
function worldCell(x,z){ const i=Math.round((x-SPAWN[0]+WHALF)/WHS), j=Math.round((z-SPAWN[2]+WHALF)/WHS); return i<0||j<0||i>=WN||j>=WN?-1:j*WN+i; }
/* ---------- towns: little settlements of houses on levelled ground ----------
   The generator picks the flattest lowland spots and levels each to a whole build level, so the houses (real build
   pieces: you can shoot, break and collapse them) sit flush on it. Same for every player. */
const TOWN_NAMES=['Rustwood','Pebble Point','Kettle Creek','Lantern Row','Mossy Mill','Hollow Hill','Cinder Flats','Brambleford','Copper Ridge','Willow Bend'];
var TOWNS=WORLD.towns.map((t,k)=>{ const r=seeded(9000+k); return {x:SPAWN[0]+t.u,z:SPAWN[2]+t.v,R:t.R,h:t.h,name:TOWN_NAMES[k]||('Town '+(k+1)),seed:1+Math.floor(r()*1e9),houses:[]}; });
// no grass pokes through the town squares
for(const t of TOWNS){ for(let dj=-5;dj<=5;dj++) for(let di=-5;di<=5;di++){ const c=worldCell(t.x+di*WHS,t.z+dj*WHS); if(c>=0&&Math.hypot(di*WHS,dj*WHS)<PLAZA_R+1) WORLD.GRASS[c]=0; } }
/* ---------- town streets: each town on a grid ----------
   A main street and a cross street through the middle of town make four blocks; the houses stand in rows along
   them. The main street lines up with the first road coming in. Roads from outside no longer cut through town to
   its centre: each one now stops at the edge of the flat town ground and joins the end of the nearest street.
   Old road traces inside towns (dirt, bare ground) are cleared. */
/* Two more roads: Kettle Creek to Copper Ridge, and Hollow Hill south round the outside of the south-west mountain, along the southern edge, to Brambleford (through waypoints). Each is
   routed over the ground by a path search on an 8 m grid that prefers gentle grades and keeps off the steep mountain
   sides and other towns, then smoothed, given a graded height profile, and joined to the towns like every road. */
{ const AG=8, M=Math.floor(2*WHALF/AG), H0=WORLD.H0, hAt=(u,v)=>{ const i=Math.round((u+WHALF)/WHS), j=Math.round((v+WHALF)/WHS); return H0[Math.max(0,Math.min(WN-1,j))*WN+Math.max(0,Math.min(WN-1,i))]; };
  const g2u=i=>-WHALF+i*AG, u2g=u=>Math.round((u+WHALF)/AG);
  const leg=(A,B)=>{ const s0=u2g(A.u)+u2g(A.v)*M, e0=u2g(B.u)+u2g(B.v)*M, G=new Float64Array(M*M).fill(Infinity), from=new Int32Array(M*M).fill(-1), done=new Uint8Array(M*M), heap=[];
    const push=(f,k)=>{ heap.push([f,k]); let c=heap.length-1; while(c>0){ const q=(c-1)>>1; if(heap[q][0]<=heap[c][0]) break; [heap[q],heap[c]]=[heap[c],heap[q]]; c=q; } };
    const pop=()=>{ const top=heap[0], last=heap.pop(); if(heap.length){ heap[0]=last; let c=0; for(;;){ const l=2*c+1, r2=l+1; let m=c; if(l<heap.length&&heap[l][0]<heap[m][0]) m=l; if(r2<heap.length&&heap[r2][0]<heap[m][0]) m=r2; if(m===c) break; [heap[m],heap[c]]=[heap[c],heap[m]]; c=m; } } return top; };
    const ex=e0%M, ez=(e0-ex)/M, hd=(i,j)=>Math.hypot(i-ex,j-ez)*AG*0.9; G[s0]=0; push(0,s0);
    while(heap.length){ const [,k]=pop(); if(done[k]) continue; done[k]=1; if(k===e0) break; const i=k%M, j=(k-i)/M, hk=hAt(g2u(i),g2u(j));
      for(let dj=-1;dj<=1;dj++) for(let di=-1;di<=1;di++){ if(!di&&!dj) continue; const ni=i+di, nj=j+dj; if(ni<0||nj<0||ni>=M||nj>=M) continue; const nk=nj*M+ni; if(done[nk]) continue;
        const u=g2u(ni), v=g2u(nj), d=Math.hypot(u,v); if(d>MAP_R-45) continue; const L=AG*Math.hypot(di,dj), gr=Math.abs(hAt(u,v)-hk)/L;
        let c=L*(1+60*gr*gr)+(gr>0.12?L*300*(gr-0.12):0)+(d<FLAT_R+20?400:0);
        for(const t of WORLD.towns){ if(t===A.t||t===B.t||EX.includes(t)) continue; if(Math.hypot(u-t.u,v-t.v)<t.R+20) c+=2000; }
        for(const rd of WORLD.roads){ /* sharing an existing road is fine but not preferred */ }
        const ng=G[k]+c; if(ng<G[nk]){ G[nk]=ng; from[nk]=k; push(ng+hd(ni,nj),nk); } } }
    let pts=[]; for(let k=e0;k>=0;k=from[k]){ const i=k%M, j=(k-i)/M; pts.push([g2u(i),g2u(j)]); if(k===s0) break; } pts.reverse(); pts[0]=[A.u,A.v]; pts[pts.length-1]=[B.u,B.v]; return pts; };
  // a road through a list of stops (towns at the ends, waypoints between): each leg found by the search, then all smoothed
  let EX=[];
  const route=(stops)=>{ EX=[stops[0].t,stops[stops.length-1].t]; let pts=[]; for(let q=0;q<stops.length-1;q++){ const l=stops[q].straight?[[stops[q].u,stops[q].v],[(stops[q].u+stops[q+1].u)/2,(stops[q].v+stops[q+1].v)/2],[stops[q+1].u,stops[q+1].v]]:leg(stops[q],stops[q+1]); if(q&&!stops[q].t){ const W=stops[q], far=p=>Math.hypot(p[0]-W.u,p[1]-W.v)>30; while(pts.length>2&&!far(pts[pts.length-1])) pts.pop(); let i=0; while(i<l.length-2&&!far(l[i])) i++; pts=pts.concat(l.slice(i)); } else pts=pts.concat(q?l.slice(1):l); } // a waypoint is passed near, not hit exactly: no hairpins if(pts.length<3) return null;
    const A=stops[0], B=stops[stops.length-1];
    { const th=[pts[0]]; for(let q=3;q<pts.length-2;q+=3) th.push(pts[q]); th.push(pts[pts.length-1]); pts=th; } // thin the grid steps before smoothing
    for(let it=0;it<5;it++){ const nx=[pts[0]]; for(let q=0;q<pts.length-1;q++){ const a=pts[q], b=pts[q+1]; nx.push([a[0]*.75+b[0]*.25,a[1]*.75+b[1]*.25],[a[0]*.25+b[0]*.75,a[1]*.25+b[1]*.75]); } nx.push(pts[pts.length-1]); pts=nx; }
    const rs=[pts[0]]; for(let q=1;q<pts.length;q++){ let [x0,z0]=rs[rs.length-1]; const [x1,z1]=pts[q]; let dx=x1-x0, dz=z1-z0, L=Math.hypot(dx,dz); while(L>=2){ x0+=dx/L*2; z0+=dz/L*2; rs.push([x0,z0]); dx=x1-x0; dz=z1-z0; L=Math.hypot(dx,dz); } }
    const n=rs.length, y=new Float32Array(n), pin=new Int8Array(n), pv=new Float32Array(n);
    for(let q=0;q<n;q++){ const [u,v]=rs[q]; y[q]=hAt(u,v); for(const t of [A.t,B.t]) if(t&&Math.hypot(u-t.u,v-t.v)<t.R-2){ pin[q]=1; pv[q]=t.h; } }
    const repin=()=>{ for(let q=0;q<n;q++) if(pin[q]) y[q]=pv[q]; }; repin(); const tmp=new Float32Array(n);
    for(let pass=0;pass<8;pass++){ for(let q=0;q<n;q++){ let a=0,c=0; for(let w=-10;w<=10;w++){ const z=q+w; if(z<0||z>=n) continue; a+=y[z]; c++; } tmp[q]=a/c; } y.set(tmp); repin(); }
    for(let pass=0;pass<4;pass++){ const g=0.2; for(let q=1;q<n;q++){ if(y[q]>y[q-1]+g) y[q]=y[q-1]+g; if(y[q]<y[q-1]-g) y[q]=y[q-1]-g; } for(let q=n-2;q>=0;q--){ if(y[q]>y[q+1]+g) y[q]=y[q+1]+g; if(y[q]<y[q+1]-g) y[q]=y[q+1]-g; } repin(); }
    return {pts:rs.map((p,q)=>[p[0],p[1],y[q]]),skip:new Uint8Array(n)}; };
  const T_=k=>({u:WORLD.towns[k].u,v:WORLD.towns[k].v,t:WORLD.towns[k]});
  const W_=(u,v)=>({u,v,t:null});
  for(const stops of [[2,8],[5,W_(-638,283),W_(-486,557),W_(-300,632),'bw',7]]){ const st=stops.map(x=>x==='bw'?Object.assign(W_(WORLD.towns[7].u-90,WORLD.towns[7].v),{straight:true}):typeof x==='number'?WORLD.towns[x]&&T_(x):x); if(st.some(x=>!x)) continue; const rd=route(st); if(rd){ if(stops.length>2) rd.prefEnd={7:0}; WORLD.roads.push(rd); } } } // the south road comes into Brambleford's west end
{ const rdPts=[];
  for(const t of TOWNS){
    let ax='x', best=1e9;
    for(const rd of WORLD.roads) for(const end of [0,1]){ const p=end?rd.pts[rd.pts.length-1]:rd.pts[0], q=end?rd.pts[Math.max(0,rd.pts.length-12)]:rd.pts[Math.min(rd.pts.length-1,11)];
      const d=Math.hypot(SPAWN[0]+p[0]-t.x,SPAWN[2]+p[1]-t.z); if(d<best&&d<4){ best=d; ax=Math.abs(q[0]-p[0])>=Math.abs(q[1]-p[1])?'x':'z'; } }
    t.axis=ax; t.streetL=Math.floor((t.R-4)/CELL)*CELL; const Ls=t.streetL;
    t.ends=[[t.x-Ls,t.z],[t.x+Ls,t.z],[t.x,t.z-Ls],[t.x,t.z+Ls]];
    // reroute: each road coming in is cut some way outside town and joined to the nearest street end by a smooth curve.
    // The curve leaves the street end straight along the street and meets the road along its own direction, and its
    // height eases from the town's level to the road's, so the road keeps its hills and still meets the street cleanly.
    const cut=t.R+12;
    for(const rd of WORLD.roads){ if(rd.street) continue;
      for(const end of [0,1]){ const P=end?rd.pts.slice().reverse():rd.pts.slice();
        if(Math.hypot(SPAWN[0]+P[0][0]-t.x,SPAWN[2]+P[0][1]-t.z)>4) continue; // this end isn't at this town
        let k=0; while(k<P.length-8&&Math.hypot(SPAWN[0]+P[k][0]-t.x,SPAWN[2]+P[k][1]-t.z)<cut) k++;
        const at=[SPAWN[0]+P[k][0],SPAWN[2]+P[k][1]], e=rd.prefEnd&&rd.prefEnd[TOWNS.indexOf(t)]!=null?t.ends[rd.prefEnd[TOWNS.indexOf(t)]]:t.ends.reduce((a,b)=>Math.hypot(b[0]-at[0],b[1]-at[1])<Math.hypot(a[0]-at[0],a[1]-at[1])?b:a);
        const L=Math.hypot(at[0]-e[0],at[1]-e[1]), ax_=[(e[0]-t.x)/Ls,(e[1]-t.z)/Ls];
        const q2=P[Math.min(P.length-1,k+3)], dx=SPAWN[0]+q2[0]-at[0], dz=SPAWN[2]+q2[1]-at[1], dl=Math.hypot(dx,dz)||1, dout=[dx/dl,dz/dl];
        const C1=[e[0]+ax_[0]*L*0.42,e[1]+ax_[1]*L*0.42], C2=[at[0]-dout[0]*L*0.42,at[1]-dout[1]*L*0.42], y0=t.h, y1=P[k][2];
        const n=Math.max(3,Math.round(L/1.8)), conn=[];
        for(let q=0;q<n;q++){ const f=q/n, g=1-f, w0=g*g*g, w1=3*g*g*f, w2=3*g*f*f, w3=f*f*f;
          const cx=w0*e[0]+w1*C1[0]+w2*C2[0]+w3*at[0], cz=w0*e[1]+w1*C1[1]+w2*C2[1]+w3*at[1], rr=Math.hypot(cx-t.x,cz-t.z), fr=Math.max(0,Math.min(1,(rr-t.R-1)/Math.max(1,cut-t.R-1))), ey=fr*fr*(3-2*fr);
          conn.push([cx-SPAWN[0],cz-SPAWN[2],y0+(y1-y0)*ey]); } // level through town, easing to the road's height outside it
        let NP=conn.concat(P.slice(k)); if(end) NP=NP.reverse();
        rd.pts=NP; rd.skip=new Uint8Array(NP.length); } }
    // clear the old road traces inside town: no dirt, grass back
    const r2=(t.R-1)*(t.R-1);
    for(let j=-Math.ceil(t.R/WHS);j<=Math.ceil(t.R/WHS);j++) for(let i=-Math.ceil(t.R/WHS);i<=Math.ceil(t.R/WHS);i++){
      const x=t.x+i*WHS, z=t.z+j*WHS; if((x-t.x)*(x-t.x)+(z-t.z)*(z-t.z)>r2) continue; const c=worldCell(x,z); if(c>=0){ WRD[c]=1e4; WORLD.GRASS[c]=255; } }
    // the two streets
    for(const X of [true,false]){ const pts=[];
      for(let s=-Ls;s<=Ls+0.01;s+=2) pts.push(X?[t.x+s-SPAWN[0],t.z-SPAWN[2],t.h]:[t.x-SPAWN[0],t.z+s-SPAWN[2],t.h]);
      WORLD.roads.push({pts,skip:new Uint8Array(pts.length),street:true,town:t}); }
  }
  // the ground under and beside the roads, cut again for the roads as they now are. Where two roads come close (a
  // junction or a fork), the ground blends smoothly between their heights instead of stepping at the halfway line,
  // so roads at different heights still meet in one smooth surface. Road distance and bare ground follow too.
  { const N=WN, RW=6, BM=34, R2=RW+BM, H0=WORLD.H0, sumW=new Float32Array(N*N), sumY=new Float32Array(N*N), minD=new Float32Array(N*N).fill(1e4), minD2=new Float32Array(N*N).fill(1e4);
    const dk=new Float32Array(N*N).fill(1e4), yk=new Float32Array(N*N), touched=[];
    for(const rd of WORLD.roads){ const p=rd.pts; touched.length=0;
      for(let q=0;q<p.length-1;q++){ const x0=SPAWN[0]+p[q][0], z0=SPAWN[2]+p[q][1], x1=SPAWN[0]+p[q+1][0], z1=SPAWN[2]+p[q+1][1], y0=p[q][2], y1=p[q+1][2], ex=x1-x0, ez=z1-z0, el=ex*ex+ez*ez||1e-6;
        const i0=Math.max(0,Math.floor((Math.min(x0,x1)-R2-SPAWN[0]+WHALF)/WHS)), i1=Math.min(N-1,Math.ceil((Math.max(x0,x1)+R2-SPAWN[0]+WHALF)/WHS));
        const j0=Math.max(0,Math.floor((Math.min(z0,z1)-R2-SPAWN[2]+WHALF)/WHS)), j1=Math.min(N-1,Math.ceil((Math.max(z0,z1)+R2-SPAWN[2]+WHALF)/WHS));
        for(let j=j0;j<=j1;j++){ const pz=SPAWN[2]-WHALF+j*WHS; for(let i=i0;i<=i1;i++){ const px=SPAWN[0]-WHALF+i*WHS; let f=((px-x0)*ex+(pz-z0)*ez)/el; f=f<0?0:f>1?1:f;
          const qx=px-(x0+ex*f), qz=pz-(z0+ez*f), d=Math.sqrt(qx*qx+qz*qz); if(d>=R2) continue; const c=j*N+i; if(dk[c]>=1e4) touched.push(c); if(d<dk[c]){ dk[c]=d; yk[c]=y0+(y1-y0)*f; } } } }
      for(const c of touched){ const d=dk[c], u=d/2.5, w=1/(1+u*u*u*u); sumW[c]+=w; sumY[c]+=w*yk[c]; if(d<minD[c]){ minD2[c]=minD[c]; minD[c]=d; } else if(d<minD2[c]) minD2[c]=d; dk[c]=1e4; } }
    const {ROCK,SNOW,GRASS}=WORLD, DIRT=WORLD.DIRT=new Uint8Array(N*N);
    for(let c=0;c<N*N;c++){ const dd=minD[c], h0=H0[c]; let h=h0;
      if(dd<R2){ const y=sumY[c]/sumW[c], diff=Math.abs(h0-y);
        if(dd<=RW) h=y; else { const B=Math.max(6,Math.min(BM,diff*1.6)); if(dd<RW+B){ let t=(dd-RW)/B; t=t*t*(3-2*t); h=y+(h0-y)*t; } } }
      WH[c]=h; const was=WRD[c]; WRD[c]=dd;
      // a worn dirt edge beside the asphalt, but not in the strip between two roads at a fork: that stays grass
      const gore=minD2[c]<dd+6, edge=gore?(dd<3.9?0:1e4):dd; DIRT[c]=gore&&dd>=3.9?0:dd<5?Math.round(255*(1-sstep(3.8,5.0,dd))):0;
      if(edge<4.8) GRASS[c]=0; else if(was<4.8||gore) GRASS[c]=Math.round((1-ROCK[c]/255)*(1-SNOW[c]/255)*255); } } // grass back where a road used to run
  for(const t of TOWNS){ const r2=(t.R-1)*(t.R-1); // the town ground stays level; no road shoulders inside town (the streets have sidewalks)
    for(let j=-Math.ceil(t.R/WHS);j<=Math.ceil(t.R/WHS);j++) for(let i=-Math.ceil(t.R/WHS);i<=Math.ceil(t.R/WHS);i++){ const x=t.x+i*WHS, z=t.z+j*WHS; if((x-t.x)*(x-t.x)+(z-t.z)*(z-t.z)>r2) continue; const c=worldCell(x,z); if(c<0) continue; WH[c]=WORLD.H0[c]; if(WRD[c]>3.6){ WRD[c]=1e4; WORLD.DIRT[c]=0; } } }
  for(const t of TOWNS) for(const X of [true,false]) for(let s=-t.streetL;s<=t.streetL;s+=1) for(let c=-6;c<=6;c+=1){ const cc=worldCell(X?t.x+s:t.x+c,X?t.z+c:t.z+s); if(cc>=0) WORLD.GRASS[cc]=0; } // sidewalks too
}
function townAt(x,z,pad){ for(const t of TOWNS) if(Math.hypot(x-t.x,z-t.z)<t.R+(pad||0)) return t; return null; }
// highest ground under a body (centre and the four corners), so you never sink into a slope
function terrainUnder(x,z){ let m=terrainH(x,z); for(const s of SAMP){ const t=terrainH(x+s[0],z+s[1]); if(t>m) m=t; } return m; }

/* ---------- terrain rendering ----------
   13×13 chunks of 128 m, each with three levels of detail (2, 4 and 8 m steps) picked by distance from the camera and
   built when first needed. Skirts along the chunk edges hide the cracks where two levels meet. Grass, bare rock, snow
   and dirt shoulders along the roads are blended per vertex. Out past the island the outer range goes on to 2.4 km. */
const rockTex=(()=>{ const N=256, c=document.createElement('canvas'); c.width=c.height=N; const g=c.getContext('2d');
  g.fillStyle='#8b8a86'; g.fillRect(0,0,N,N);
  for(let i=0;i<40;i++){ const y=Math.random()*N, h=3+Math.random()*14, v=Math.random(); g.fillStyle=v<.5?'rgba(60,58,54,.16)':'rgba(190,186,176,.14)';
    for(const oy of [-N,0,N]){ g.beginPath(); g.moveTo(0,y+oy); for(let x=0;x<=N;x+=16) g.lineTo(x,y+oy+Math.sin(x/N*Math.PI*2*(1+i%3))*4); g.lineTo(N,y+oy+h); g.lineTo(0,y+oy+h); g.fill(); } } // wavy strata
  for(let i=0;i<7000;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(40,40,38,.28)':'rgba(220,218,210,.22)'; g.fillRect(Math.random()*N,Math.random()*N,1+Math.random()*2,1+Math.random()*2); }
  g.strokeStyle='rgba(35,33,30,.45)'; g.lineWidth=1.2;
  for(let i=0;i<26;i++){ let x=Math.random()*N, y=Math.random()*N; g.beginPath(); g.moveTo(x,y); for(let k=0;k<6;k++){ x+=(Math.random()-.5)*26; y+=Math.random()*14; g.lineTo(x,y); } g.stroke(); } // cracks
  const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy()); return t; })();
const terrainMat=new THREE.MeshLambertMaterial({map:groundTexture(14),vertexColors:true,color:0xb6cfb0});
hemi.groundColor.setHex(0x56683f); // a deeper, less neon green
// push the ground back in depth so floors built on it never sink into it at a distance
terrainMat.polygonOffset=true; terrainMat.polygonOffsetFactor=4; terrainMat.polygonOffsetUnits=16;
terrainMat.onBeforeCompile=sh=>{ sh.uniforms.rockMap={value:rockTex};
  sh.vertexShader='attribute vec3 cover;\nvarying vec3 vCover;\nvarying vec3 vWP;\nvarying vec3 vWN;\n'+sh.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\n  vCover=cover; vWP=(modelMatrix*vec4(transformed,1.0)).xyz; vWN=objectNormal;');
  sh.fragmentShader='uniform sampler2D rockMap;\nvarying vec3 vCover;\nvarying vec3 vWP;\nvarying vec3 vWN;\n'+sh.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
  { vec3 bw=abs(normalize(vWN)); bw*=bw; bw*=bw; bw/=(bw.x+bw.y+bw.z); // rock is projected from three sides, so cliffs don't smear
    vec3 rk=texture2D(rockMap,vWP.zy*0.085).rgb*bw.x+texture2D(rockMap,vWP.xz*0.085).rgb*bw.y+texture2D(rockMap,vWP.xy*0.085).rgb*bw.z;
    vec3 dirt=vec3(0.52,0.43,0.31)*(0.7+0.55*rk.g);
    diffuseColor.rgb=mix(diffuseColor.rgb,dirt,clamp(vCover.z,0.0,1.0));
    diffuseColor.rgb=mix(diffuseColor.rgb,rk*vec3(0.93,0.92,0.9),clamp(vCover.x,0.0,1.0));
    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.9,0.93,0.97)*(0.9+0.12*rk.r),clamp(vCover.y,0.0,1.0)); }`); };
const T_LUSH=new THREE.Color(0.8,0.94,0.8), T_DRY=new THREE.Color(1.06,1.0,0.74), T_DIRT=new THREE.Color(0.94,0.82,0.66), _tc=new THREE.Color();
// grass tint: lush in the valleys, sun-dried higher up, a little earthy on steep slopes, and gentle random patches
function terrainTint(x,z,h,ny){ const patch=0.5+0.5*Math.sin(x*0.05+Math.sin(z*0.033)*2)*Math.cos(z*0.041-x*0.017);
  return _tc.setRGB(.92,.92,.9).lerp(T_LUSH,0.5*(1-Math.min(1,h/30))*patch).lerp(T_DRY,Math.min(1,Math.max(0,(h-28)/70))*0.75).lerp(T_DIRT,Math.min(1,(1-ny)*4)*0.6); }
const TCH=64, TNC=Math.round((WN-1)/TCH), TERR={chunks:[],outer:[]};
// one mesh: a grid of VA×VB vertices (from a height function) plus a skirt hanging from each of the four edges
function gridMesh(VA,VB,vert,skirt){
  const nv=VA*VB+2*VA+2*VB, pos=new Float32Array(nv*3), nor=new Float32Array(nv*3), uv=new Float32Array(nv*2), col=new Float32Array(nv*3), cov=new Float32Array(nv*3);
  const V=VA, na=VA-1, nb=VB-1, idx=[];
  for(let b=0;b<VB;b++) for(let a=0;a<VA;a++) vert(b*V+a,a,b,0,pos,nor,uv,col,cov);
  for(let b=0;b<nb;b++) for(let a=0;a<na;a++){ const k=b*V+a; idx.push(k,k+V,k+1, k+1,k+V,k+V+1); }
  // skirts: each edge walked so its strip faces outward
  let base=VA*VB;
  [[na,t=>[t,nb]],[nb,t=>[na,nb-t]],[na,t=>[na-t,0]],[nb,t=>[0,t]]].forEach(([n,f])=>{
    for(let t=0;t<=n;t++){ const [a,b]=f(t); vert(base+t,a,b,skirt,pos,nor,uv,col,cov); }
    for(let t=0;t<n;t++){ const [a0,b0]=f(t), [a1,b1]=f(t+1), T0=b0*V+a0, T1=b1*V+a1, B0=base+t, B1=base+t+1; idx.push(T0,B0,T1, T1,B0,B1); }
    base+=n+1; });
  const g=new THREE.BufferGeometry();
  g.setAttribute('position',new THREE.BufferAttribute(pos,3)); g.setAttribute('normal',new THREE.BufferAttribute(nor,3)); g.setAttribute('uv',new THREE.BufferAttribute(uv,2));
  g.setAttribute('color',new THREE.BufferAttribute(col,3)); g.setAttribute('cover',new THREE.BufferAttribute(cov,3));
  g.setIndex(nv<65536?new THREE.Uint16BufferAttribute(idx,1):new THREE.Uint32BufferAttribute(idx,1)); g.computeBoundingSphere();
  const m=new THREE.Mesh(g,terrainMat); m.position.y=-0.03; m.matrixAutoUpdate=false; m.updateMatrix(); scene.add(m); return m; }
// a patch of the baked grid: na×nb cells from (i0,j0), every st cells
function terrainPatch(i0,j0,na,nb,st){
  const {ROCK,SNOW}=WORLD;
  const m=gridMesh(na/st+1,nb/st+1,(k,a,b,dy,pos,nor,uv,col,cov)=>{ const i=i0+a*st, j=j0+b*st, q=j*WN+i, x=SPAWN[0]-WHALF+i*WHS, z=SPAWN[2]-WHALF+j*WHS; let h=WH[q];
    if(st>1&&WRD[q]<12+2*st*WHS){ for(let jj=Math.max(0,j-st);jj<=Math.min(WN-1,j+st);jj++) for(let ii=Math.max(0,i-st);ii<=Math.min(WN-1,i+st);ii++){ const v=WH[jj*WN+ii]; if(v<h) h=v; } } // coarse ground near a road sits at the lowest point it spans
    const ia=Math.max(0,i-st), ib=Math.min(WN-1,i+st), ja=Math.max(0,j-st), jb=Math.min(WN-1,j+st);
    const gx=(WH[j*WN+ib]-WH[j*WN+ia])/((ib-ia)*WHS), gz=(WH[jb*WN+i]-WH[ja*WN+i])/((jb-ja)*WHS), ny=1/Math.sqrt(1+gx*gx+gz*gz);
    pos[k*3]=x; pos[k*3+1]=h-dy; pos[k*3+2]=z; nor[k*3]=-gx*ny; nor[k*3+1]=ny; nor[k*3+2]=-gz*ny;
    uv[k*2]=(i-i0)*WHS/16; uv[k*2+1]=(j-j0)*WHS/16; // the grass texture tiles every 16 m, seamlessly across chunks
    const t=terrainTint(x,z,h,ny); col[k*3]=t.r; col[k*3+1]=t.g; col[k*3+2]=t.b;
    cov[k*3]=ROCK[q]/255; cov[k*3+1]=SNOW[q]/255; cov[k*3+2]=st===1?WORLD.DIRT[q]/255:0; },4*st+2); // a narrow worn edge beside the asphalt, up close only
  m.receiveShadow=true; return m; }
const chunkMesh=(c,lod)=>terrainPatch(c.ci*TCH,c.cj*TCH,TCH,TCH,1<<lod);
for(let cj=0;cj<TNC;cj++) for(let ci=0;ci<TNC;ci++){ const x0=SPAWN[0]-WHALF+ci*TCH*WHS, z0=SPAWN[2]-WHALF+cj*TCH*WHS;
  TERR.chunks.push({ci,cj,x0,z0,x1:x0+TCH*WHS,z1:z0+TCH*WHS,m:[null,null,null],lod:-1}); }
// far away, 2×2 chunks that are all at the coarsest level are drawn as one mesh (fewer draw calls)
TERR.blocks=[]; for(let bj=0;bj<TNC;bj+=2) for(let bi=0;bi<TNC;bi+=2){ const cs=TERR.chunks.filter(c=>c.ci>=bi&&c.ci<bi+2&&c.cj>=bj&&c.cj<bj+2);
  TERR.blocks.push({cs,i0:bi*TCH,j0:bj*TCH,na:(Math.min(TNC,bi+2)-bi)*TCH,nb:(Math.min(TNC,bj+2)-bj)*TCH,m:null}); }
const TLOD=[170,480];
function stepTerrain(cx,cz,force){
  let budget=force?1e9:2; // a couple of new meshes a frame at most, so walking never hitches
  for(const c of TERR.chunks){
    const dx=Math.max(c.x0-cx,0,cx-c.x1), dz=Math.max(c.z0-cz,0,cz-c.z1), d=Math.sqrt(dx*dx+dz*dz);
    let want=d<TLOD[0]?0:d<TLOD[1]?1:2;
    if(c.lod>=0&&want!==c.lod&&Math.abs(d-TLOD[Math.min(want,c.lod)])<12) want=c.lod; // a little hysteresis at the boundaries
    if(!c.m[want]){ if(budget>0){ budget--; c.m[want]=chunkMesh(c,want); c.m[want].visible=false; } else want=c.lod; }
    if(want!==c.lod){ if(c.lod>=0) c.m[c.lod].visible=false; c.m[want].visible=true; c.lod=want; }
    for(let l=0;l<2;l++) if(c.m[l]&&l!==c.lod&&d>TLOD[l]+150){ scene.remove(c.m[l]); c.m[l].geometry.dispose(); c.m[l]=null; } // drop detail that's far away now
  }
  for(const b of TERR.blocks){ let far=b.cs.every(c=>c.lod===2);
    if(far&&!b.m){ if(budget>0){ budget--; b.m=terrainPatch(b.i0,b.j0,b.na,b.nb,4); } else far=false; }
    if(b.m) b.m.visible=far; for(const c of b.cs) c.m[c.lod].visible=!far; }
}
TERR.chunks.forEach(c=>{ c.m[2]=chunkMesh(c,2); c.m[2].visible=false; });
stepTerrain(SPAWN[0],SPAWN[2],true);
// the outer range: 16 tiles out to ±2.4 km at 16 m steps, straight from the generator
(function outerRange(){
  const E=2400, S=16, xs=[-E,-WHALF,WHALF,E], tiles=[];
  for(let b=0;b<3;b++) for(let a=0;a<3;a++){ if(a===1&&b===1) continue; const u0=xs[a], u1=xs[a+1], v0=xs[b], v1=xs[b+1];
    if(u1-u0>=v1-v0){ const um=u0+Math.round((u1-u0)/2/S)*S; tiles.push([u0,um,v0,v1],[um,u1,v0,v1]); } else { const vm=v0+Math.round((v1-v0)/2/S)*S; tiles.push([u0,u1,v0,vm],[u0,u1,vm,v1]); } }
  for(const [u0,u1,v0,v1] of tiles){ const nu=(u1-u0)/S, nvv=(v1-v0)/S, W=nu+3, hg=new Float32Array(W*(nvv+3));
    for(let j=-1;j<=nvv+1;j++) for(let i=-1;i<=nu+1;i++) hg[(j+1)*W+i+1]=genH(u0+i*S,v0+j*S);
    const m=gridMesh(nu+1,nvv+1,(k,a,b,dy,pos,nor,uv,col,cov)=>{ const i=a, j=b, h=hg[(j+1)*W+i+1], u=u0+i*S, v=v0+j*S;
      const gx=(hg[(j+1)*W+i+2]-hg[(j+1)*W+i])/(2*S), gz=(hg[(j+2)*W+i+1]-hg[j*W+i+1])/(2*S), ny=1/Math.sqrt(1+gx*gx+gz*gz);
      pos[k*3]=SPAWN[0]+u; pos[k*3+1]=h-dy; pos[k*3+2]=SPAWN[2]+v; nor[k*3]=-gx*ny; nor[k*3+1]=ny; nor[k*3+2]=-gz*ny;
      uv[k*2]=(u-u0)/16; uv[k*2+1]=(v-v0)/16;
      const t=terrainTint(SPAWN[0]+u,SPAWN[2]+v,h,ny); col[k*3]=t.r; col[k*3+1]=t.g; col[k*3+2]=t.b;
      const line=168+26*gnoise(u*0.011,v*0.011,77); cov[k*3]=Math.min(1,sstep(0.87,0.7,ny)+0.7*sstep(175,240,h)); cov[k*3+1]=sstep(line,line+24,h)*sstep(0.58,0.78,ny); cov[k*3+2]=0; },30);
    TERR.outer.push(m); }
})();

/* ---------- roads: asphalt with white edge lines and a dashed yellow centre, plus a paved square in each town ---------- */
let roadPlainTex=null;
const roadTex=(()=>{ const W=128, Hh=512, c=document.createElement('canvas'); c.width=W; c.height=Hh; const g=c.getContext('2d');
  g.fillStyle='#4b4e53'; g.fillRect(0,0,W,Hh);
  for(let i=0;i<9000;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(22,24,28,.35)':v<.9?'rgba(140,140,138,.22)':'rgba(200,196,186,.3)'; g.fillRect(Math.random()*W,Math.random()*Hh,1+Math.random(),1+Math.random()); }
  for(let i=0;i<14;i++){ const x=Math.random()*W, y=Math.random()*Hh, r=8+Math.random()*24, gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0,'rgba(30,30,32,.18)'); gr.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=gr; g.fillRect(x-r,y-r,r*2,r*2); }
  const pc=document.createElement('canvas'); pc.width=W; pc.height=Hh; pc.getContext('2d').drawImage(c,0,0); // the same asphalt without markings, for junctions
  roadPlainTex=new THREE.CanvasTexture(pc); roadPlainTex.wrapS=roadPlainTex.wrapT=THREE.RepeatWrapping; roadPlainTex.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  g.fillStyle='rgba(236,236,230,.92)'; g.fillRect(6,0,3,Hh); g.fillRect(W-9,0,3,Hh);   // edge lines
  g.fillStyle='#e6c23c'; g.fillRect(W/2-2,0,4,Hh*0.5);                                // centre dash: half of every 12 m
  const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy()); return t; })();
const ROAD_HW=3.6, roadMeshes=[];
// how close a point is to any other road's centreline (for leaving markings out of junctions)
const roadHash=new Map(); WORLD.roads.forEach((rd,k)=>rd.pts.forEach(p=>{ const x=SPAWN[0]+p[0], z=SPAWN[2]+p[1], key=Math.floor(x/8)+','+Math.floor(z/8); let l=roadHash.get(key); if(!l){ l=[]; roadHash.set(key,l); } l.push([x,z,k]); }));
function nearOther(k,x,z){ let best=1e9; const cx=Math.floor(x/8), cz=Math.floor(z/8);
  for(let a=-2;a<=2;a++) for(let b=-2;b<=2;b++){ const l=roadHash.get((cx+a)+','+(cz+b)); if(l) for(const [px,pz,kk] of l) if(kk!==k){ const d=Math.hypot(px-x,pz-z); if(d<best) best=d; } } return best; }
// near a junction the lane markings fade out into plain asphalt (same texture, no lines), so crossings stay clean
function roadOBC(sh){ sh.uniforms.plainMap={value:roadPlainTex};
  sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\nattribute float lines; varying float vLines;').replace('#include <begin_vertex>','#include <begin_vertex>\nvLines=lines;');
  sh.fragmentShader=sh.fragmentShader.replace('#include <common>','#include <common>\nuniform sampler2D plainMap; varying float vLines;')
    .replace('#include <map_fragment>','vec4 texelColor=mix(texture2D(plainMap,vUv),texture2D(map,vUv),vLines); texelColor=mapTexelToLinear(texelColor); diffuseColor*=texelColor;'); }
WORLD.roads.forEach((rd,k)=>{ const p=rd.pts, n=p.length, pos=[], nor=[], uv=[], idx=[], lines=[], AC=[-1,-0.5,0,0.5,1], NC=AC.length; let s=0;
  let bx0=1e9, bz0=1e9, bx1=-1e9, bz1=-1e9;
  for(let q=0;q<n;q++){ const a=p[Math.max(0,q-2)], b=p[Math.min(n-1,q+2)]; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1, sx=-tz/tl, sz=tx/tl;
    if(q>0) s+=Math.hypot(p[q][0]-p[q-1][0],p[q][1]-p[q-1][1]);
    const x=SPAWN[0]+p[q][0], z=SPAWN[2]+p[q][1];
    const ln=Math.min(1,Math.max(0,(nearOther(k,x,z)-8)/8)); // 0 at a junction, fading back to full markings 16 m out
    // every point across the road sits on the ground under it, so the road follows the cut ground exactly: no
    // floating, no sinking, and where two roads at different heights meet the asphalt runs smoothly from one to the other
    for(const c of AC){ const px=x+sx*ROAD_HW*c, pz=z+sz*ROAD_HW*c, h=terrainH(px,pz), e=0.6, gx=(terrainH(px+e,pz)-terrainH(px-e,pz))/(2*e), gz=(terrainH(px,pz+e)-terrainH(px,pz-e))/(2*e), nl=Math.hypot(gx,1,gz);
      pos.push(px,h+0.07,pz); nor.push(-gx/nl,1/nl,-gz/nl); uv.push((c+1)/2,s/12); lines.push(ln); }
    bx0=Math.min(bx0,x); bx1=Math.max(bx1,x); bz0=Math.min(bz0,z); bz1=Math.max(bz1,z); }
  const up=(A,B,C)=>{ const ax=pos[B*3]-pos[A*3], az=pos[B*3+2]-pos[A*3+2], cx=pos[C*3]-pos[A*3], cz=pos[C*3+2]-pos[A*3+2]; return az*cx-ax*cz>0; };
  for(let q=0;q<n-1;q++) for(let c=0;c<NC-1;c++){
    const L0=q*NC+c, R0=L0+1, L1=L0+NC, R1=L1+1;
    if(up(L0,L1,R0)) idx.push(L0,L1,R0); else idx.push(L0,R0,L1);
    if(up(R0,L1,R1)) idx.push(R0,L1,R1); else idx.push(R0,R1,L1); }
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(nor,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2)); g.setAttribute('lines',new THREE.Float32BufferAttribute(lines,1)); g.setIndex(idx); g.computeBoundingSphere();
  const rm=new THREE.MeshLambertMaterial({map:roadTex,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-4*(4+k)}); rm.onBeforeCompile=roadOBC;
  const m=new THREE.Mesh(g,rm);
  m.receiveShadow=true; m.matrixAutoUpdate=false; scene.add(m); roadMeshes.push(m);
  rd.box=[bx0-6,bz0-6,bx1+6,bz1+6]; });
// (no round town squares: each town has a main street instead)
/* Where two roads run close (a fork, or one road meeting another at a shallow angle) the ground between them is paved
   too, up to where they are about 8 m apart, so a fork is one stretch of asphalt that splits, ending in a blunt
   grass nose, not two strips with a sliver of dirt between them. The paving lies on the ground like the roads. */
{ const pos=[], uv=[], idx=[], AC=[0,0.25,0.5,0.75,1], NC=AC.length, S=SPAWN, FILL=8.4;
  const nearestLower=(k,x,z)=>{ let best=null, bd=FILL; const cx=Math.floor(x/8), cz=Math.floor(z/8);
    for(let a=-2;a<=2;a++) for(let b=-2;b<=2;b++){ const l=roadHash.get((cx+a)+','+(cz+b)); if(l) for(const e of l){ const kk=e[2]; if(kk>=k||WORLD.roads[kk].street) continue; const d=Math.hypot(e[0]-x,e[1]-z); if(d<bd){ bd=d; best=e; } } } return best; };
  WORLD.roads.forEach((rd,k)=>{ if(rd.street) return; const p=rd.pts; let run=[];
    const flush=()=>{ if(run.length>=2){ for(let r=0;r<run.length;r++){ const [x,z,o]=run[r]; for(const c of AC){ const px=x+(o[0]-x)*c, pz=z+(o[1]-z)*c; pos.push(px,terrainH(px,pz)+0.06,pz); uv.push(px/7.2,pz/12); } }
        const base=pos.length/3-run.length*NC; for(let r=0;r<run.length-1;r++) for(let c=0;c<NC-1;c++){ const a=base+r*NC+c, b=a+1, a1=a+NC, b1=a1+1;
          const up=(A,B,C)=>{ const ax=pos[B*3]-pos[A*3], az=pos[B*3+2]-pos[A*3+2], cx=pos[C*3]-pos[A*3], cz=pos[C*3+2]-pos[A*3+2]; return az*cx-ax*cz>0; };
          if(up(a,a1,b)) idx.push(a,a1,b); else idx.push(a,b,a1); if(up(b,a1,b1)) idx.push(b,a1,b1); else idx.push(b,b1,a1); } } run=[]; };
    for(let q=0;q<p.length;q++){ const x=S[0]+p[q][0], z=S[2]+p[q][1]; if(townAt(x,z,-2)){ flush(); continue; }
      const o=nearestLower(k,x,z); if(o&&Math.hypot(o[0]-x,o[1]-z)>0.4) run.push([x,z,o]); else flush(); }
    flush(); });
  if(idx.length){ const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2)); g.setIndex(idx); g.computeVertexNormals();
    const fm=new THREE.Mesh(g,new THREE.MeshLambertMaterial({map:roadPlainTex,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-8}));
    fm.receiveShadow=true; fm.matrixAutoUpdate=false; scene.add(fm); roadMeshes.push(fm); } }

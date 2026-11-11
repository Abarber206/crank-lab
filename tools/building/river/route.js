// River routing, written as it will go into the game. X carries the game's own values.
function routeRivers(X){
  const {WORLD,TOWNS,SPAWN,WGEN,MAP_R,FLAT_R,WHALF,WHS,WN,sstep,fbm,OPT}=X, S=WGEN.sea(), RV=[]; if(!S) return RV;
  const G=4, GM=Math.floor((WN-1)/G)+1, NG=GM*GM, gh=new Float32Array(NG), pen=new Float32Array(NG), H0=WORLD.H0;
  const cu=i=>-WHALF+i*G*WHS, ci=u=>Math.max(0,Math.min(GM-1,Math.round((u+WHALF)/(G*WHS)))), cellOf=(u,v)=>ci(v)*GM+ci(u);
  for(let j=0;j<GM;j++) for(let i=0;i<GM;i++){ const k=j*GM+i, u=cu(i), v=cu(j), d=Math.hypot(u,v); gh[k]=H0[(j*G)*WN+i*G];
    let p=(d>MAP_R-36&&!(WGEN.seaW(u,v)>0.5))||d<FLAT_R+78?-1:0; // not past the rim (the bay itself lies past it), not across the build field
    if(p>=0) for(const t of TOWNS){ const dt=Math.hypot(SPAWN[0]+u-t.x,SPAWN[2]+v-t.z); if(dt<t.R+38){ p=-1; break; } if(dt<t.R+70) p+=60; } // nor through a town
    pen[k]=p; }
  for(const rd of WORLD.roads) for(const q of rd.pts){ const i0=ci(q[0]), j0=ci(q[1]); for(let b=-2;b<=2;b++) for(let a=-2;a<=2;a++){ const i=i0+a, j=j0+b; if(i<0||j<0||i>=GM||j>=GM) continue; const k=j*GM+i; if(pen[k]>=0&&pen[k]<1000) pen[k]+=1000; } } // (1000 and up: on or beside a road. A river may cross one, at a price, but not run along it)
  const D8=[[1,0,8],[-1,0,8],[0,1,8],[0,-1,8],[1,1,11.3137],[1,-1,11.3137],[-1,1,11.3137],[-1,-1,11.3137]];
  /* Lowest-pass search, upstream from water that is already there. Each cell gets the lowest "highest ground on the way
     down" (then the shortest way), and a step upstream may never dip more than CUT below the highest ground already
     passed: so a river that follows `prev` back down never has to cut deeper than CUT + 0.9 m into the land. */
  function drain(seeds,CUT){
    const Mx=new Float32Array(NG).fill(1e9), Ln=new Float32Array(NG).fill(1e9), prev=new Int32Array(NG).fill(-1), done=new Uint8Array(NG), heap=[];
    const less=(a,b)=>a[0]<b[0]-1e-4||(a[0]<b[0]+1e-4&&a[1]<b[1]);
    const push=(m,l,k)=>{ heap.push([m,l,k]); let c=heap.length-1; while(c>0){ const p=(c-1)>>1; if(!less(heap[c],heap[p])) break; [heap[p],heap[c]]=[heap[c],heap[p]]; c=p; } };
    const pop=()=>{ const top=heap[0], last=heap.pop(); if(heap.length){ heap[0]=last; let c=0; for(;;){ const l=c*2+1, r=l+1; let m=c; if(l<heap.length&&less(heap[l],heap[m])) m=l; if(r<heap.length&&less(heap[r],heap[m])) m=r; if(m===c) break; [heap[m],heap[c]]=[heap[c],heap[m]]; c=m; } } return top; };
    for(const [k,m] of seeds){ Mx[k]=m; Ln[k]=0; push(m,0,k); }
    while(heap.length){ const [m,l,k]=pop(); if(done[k]) continue; done[k]=1; const i=k%GM, j=(k-i)/GM;
      for(const [di,dj,L] of D8){ const ni=i+di, nj=j+dj; if(ni<0||nj<0||ni>=GM||nj>=GM) continue; const nk=nj*GM+ni; if(done[nk]||pen[nk]<0||gh[nk]<m-CUT) continue;
        const nm=Math.max(m,gh[nk]), nl=l+L+(pen[nk]>=1000?OPT.road+pen[nk]-1000:pen[nk]); if(nm<Mx[nk]-1e-4||(nm<Mx[nk]+1e-4&&nl<Ln[nk])){ Mx[nk]=nm; Ln[nk]=nl; prev[nk]=k; push(nm,nl,nk); } } }
    return {prev,done,Ln}; }
  const trace=(D,k,stop)=>{ const path=[]; for(;k>=0;k=D.prev[k]){ path.push(k); if(stop&&stop(k)&&path.length>1) break; } return path; };
  // grid path -> a smooth centreline every 2 m, wandering a little, with its water surface: never rising, and at least 0.9 m under the ground it passes
  function shape(path,amp,seed,endY){
    let pts=path.map(k=>[cu(k%GM),cu((k-k%GM)/GM)]);
    { const th=[pts[0]]; for(let q=2;q<pts.length-1;q+=2) th.push(pts[q]); th.push(pts[pts.length-1]); pts=th; }
    { let s=0; const out=[pts[0]]; for(let q=1;q<pts.length-1;q++){ const a=pts[q-1], b=pts[q+1], p=pts[q]; s+=Math.hypot(p[0]-a[0],p[1]-a[1]); let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl;
        const w=Math.min(1,q/4,(pts.length-1-q)/4), o=amp*w*fbm(s*0.011+seed,seed*1.7,2,97), nx=p[0]-tz*o, nz=p[1]+tx*o, pk=pen[cellOf(nx,nz)]; out.push(pk<0||(pk>0&&pk<1000)?p:[nx,nz]); } out.push(pts[pts.length-1]); pts=out; }
    for(let it=0;it<4;it++){ const nx=[pts[0]]; for(let q=0;q<pts.length-1;q++){ const p=pts[q], n=pts[q+1]; nx.push([p[0]*0.75+n[0]*0.25,p[1]*0.75+n[1]*0.25],[p[0]*0.25+n[0]*0.75,p[1]*0.25+n[1]*0.75]); } nx.push(pts[pts.length-1]); pts=nx; }
    const rs=[pts[0]]; for(let q=1;q<pts.length;q++){ let [x0,z0]=rs[rs.length-1]; const [x1,z1]=pts[q]; let dx=x1-x0, dz=z1-z0, L=Math.hypot(dx,dz); while(L>=2){ x0+=dx/L*2; z0+=dz/L*2; rs.push([x0,z0]); dx=x1-x0; dz=z1-z0; L=Math.hypot(dx,dz); } }
    const n=rs.length, t=new Float32Array(n), tmp=new Float32Array(n), y=new Float32Array(n);
    for(let q=0;q<n;q++) t[q]=WORLD.at(H0,rs[q][0],rs[q][1]);
    for(let pass=0;pass<3;pass++){ for(let q=0;q<n;q++){ let s2=0, c2=0; for(let w=-5;w<=5;w++){ const z=q+w; if(z<0||z>=n) continue; s2+=t[z]; c2++; } tmp[q]=s2/c2; } t.set(tmp); }
    y[0]=t[0]-0.8; for(let q=1;q<n;q++) y[q]=Math.min(y[q-1],t[q]-0.9);
    const m=Math.min(n-1,30), y0=y[n-1-m]; for(let q=n-1-m;q<n;q++){ const f=(q-(n-1-m))/m; y[q]=Math.min(y[q],y0+(endY-y0)*f*f*(3-2*f)); } // down to the level it runs into over its last 60 m
    for(let q=0;q<n;q++) if(y[q]<endY) y[q]=endY;
    for(let pass=0;pass<2;pass++){ for(let q=0;q<n;q++){ let s2=0, c2=0; for(let w=-4;w<=4;w++){ const z=q+w; if(z<0||z>=n) continue; s2+=y[z]; c2++; } tmp[q]=s2/c2; } for(let q=0;q<n;q++){ y[q]=Math.min(tmp[q],q?y[q-1]:tmp[q],t[q]-0.6); if(y[q]<endY) y[q]=endY; } }
    let cut=0, sum=0; for(let q=0;q<n;q++){ const c=t[q]-y[q]; if(c>cut) cut=c; sum+=c; }
    return {pts:rs.map((p,q)=>[p[0],p[1],y[q]]),cut,mean:sum/n,len:n*2}; }
  // the main river: from the rim across from the bay down to the beach beside the town
  const a0=Math.atan2(-S.nz,-S.nx), seeds=[];
  for(let k=0;k<NG;k++){ if(pen[k]<0||gh[k]>=S.Y-0.2) continue; const u=cu(k%GM), v=cu((k-k%GM)/GM), al=u*S.nx+v*S.nz, lat=v*S.nx-u*S.nz; if(al<S.C0+70&&Math.abs(lat)<OPT.mouthMax&&Math.abs(lat)>OPT.mouthMin) seeds.push([k,S.Y]); }
  const D=drain(seeds,OPT.cut); let src=-1;
  for(const da of OPT.srcAng){ const k=cellOf(Math.cos(a0+da)*(MAP_R-OPT.srcIn),Math.sin(a0+da)*(MAP_R-OPT.srcIn)); if(D.done[k]&&gh[k]>=OPT.srcMinH){ src=k; break; } }
  RV.info={seeds:seeds.length,src:src>=0?[cu(src%GM),cu((src-src%GM)/GM),+gh[src].toFixed(1)]:null}; if(src<0) return RV;
  const mainPath=trace(D,src), sh=shape(mainPath,OPT.amp,3.3,S.Y);
  { let runs=0, longest=0, run=0; for(const k of mainPath){ if(pen[k]>=1000){ if(!run) runs++; run++; if(run>longest) longest=run; } else run=0; } RV.info.mainRoads=[runs,longest]; }
  RV.push({pts:sh.pts,hw0:OPT.hw0,hw1:OPT.hw1,depth:OPT.depth,cut:sh.cut,mean:sh.mean,main:true});
  // streams: from the foot of each range (and from the rim to either side) down into whatever water is nearest
  const wet=new Int32Array(NG).fill(-1), mark=(rv,idx)=>rv.pts.forEach((p,q)=>{ const k=cellOf(p[0],p[1]); if(wet[k]<0) wet[k]=idx*100000+q; }); mark(RV[0],0);
  const cands=[], flank=[]; for(const M of WGEN.MASSIFS){ let bd=1e9, bp=null; for(const p of RV[0].pts){ const d=Math.hypot(p[0]-M.u,p[1]-M.v); if(d<bd){ bd=d; bp=p; } } const dx=(bp[0]-M.u)/bd, dz=(bp[1]-M.v)/bd; for(const r of [0,1.9,-1.9]){ const c=Math.cos(r), sn=Math.sin(r); (r?flank:cands).push([M.u+(dx*c-dz*sn)*M.R*OPT.foot,M.v+(dz*c+dx*sn)*M.R*OPT.foot]); } } // the side of each range facing the river first, then round their flanks
  cands.push(...flank);
  for(const da of OPT.rimAng) cands.push([Math.cos(a0+da)*(MAP_R-OPT.srcIn),Math.sin(a0+da)*(MAP_R-OPT.srcIn)]);
  const made=[], ws=[]; for(let k=0;k<NG;k++) if(wet[k]>=0){ const jy=RV[0].pts[wet[k]%100000][2]; ws.push([k,Math.max(gh[k],jy+0.6+OPT.cut)]); } // (a stream may not run lower than the water it joins)
  for(let k=0;k<NG;k++) if(wet[k]<0&&pen[k]>=0&&gh[k]<S.Y-0.2) ws.push([k,S.Y]); // ...or it runs straight into the bay
  const D2=drain(ws,OPT.cut);
  for(const [u,v] of cands){ if(RV.length>OPT.maxStreams) break; const sk=cellOf(u,v); if(pen[sk]<0||wet[sk]>=0||!D2.done[sk]){ made.push({u:Math.round(u),v:Math.round(v),why:'unreachable'}); continue; }
    const path=trace(D2,sk,k=>wet[k]>=0), tag=wet[path[path.length-1]]; let runs=0, longest=0, run=0; for(const k of path){ if(pen[k]>=1000){ if(!run) runs++; run++; if(run>longest) longest=run; } else run=0; }
    if(runs>OPT.maxCross||longest>OPT.maxRun){ made.push({u:Math.round(u),v:Math.round(v),why:'roads',runs,longest,n:path.length}); continue; } // it would cross too many roads, or run along one
    if(path.length<OPT.minCells||path.length>OPT.maxCells){ made.push({u:Math.round(u),v:Math.round(v),why:'length',n:path.length}); continue; }
    const into=tag>=0?RV[Math.floor(tag/100000)]:null, jq=tag%100000, jy=into?into.pts[jq][2]:S.Y, st=shape(path,OPT.amp*0.6,7.1+made.length*2.3,jy); if(into) st.pts[st.pts.length-1]=[into.pts[jq][0],into.pts[jq][1],jy];
    made.push({u:Math.round(u),v:Math.round(v),len:st.len,cut:+st.cut.toFixed(1),mean:+st.mean.toFixed(1)});
    if(st.len<OPT.minLen||st.mean<0.3) continue; const rv={pts:st.pts,hw0:OPT.shw,hw1:OPT.shw*1.25,depth:OPT.sdepth,cut:st.cut,mean:st.mean,into:into?Math.floor(tag/100000):-1,jq}; RV.push(rv); mark(rv,RV.length-1); }
  RV.made=made; return RV; }
if(typeof module!=='undefined') module.exports=routeRivers;

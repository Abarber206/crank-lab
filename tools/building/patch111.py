# ---------- 111. rivers: a main river from the far rim down to the bay and streams running into it from the hills,
# cut into the land along the lowest passes (never deeper than about 3 m), with flowing water you can wade through,
# and real bridges where roads cross: a concrete deck on piers that you can drive over and wade under ----------
ROUTE = r'''
/* ---------- rivers ----------
   The main river starts at the rim across the map from the bay and follows the lowest passes down to the beach beside
   the coastal town; streams come down from the foot of each mountain range into it (or straight into the bay). The
   search runs upstream from water that is already there and never lets the ground dip more than a couple of metres
   below the highest ground already passed, so no river has to cut a gorge. Each river is a centreline every 2 m:
   [u, v, water level, half width, bank width, depth]. */
function routeRivers(){
  const S=WGEN.sea(), RV=[]; if(!S) return RV;
  const O={cut:2.6,road:60,amp:10,hw0:3.6,hw1:6.5,depth:1.15,shw:2.2,sdepth:0.45,foot:1.3,maxStreams:6};
  const G=4, GM=Math.floor((WN-1)/G)+1, NG=GM*GM, gh=new Float32Array(NG), pen=new Float32Array(NG), H0=WORLD.H0;
  const cu=i=>-WHALF+i*G*WHS, ci=u=>Math.max(0,Math.min(GM-1,Math.round((u+WHALF)/(G*WHS)))), cellOf=(u,v)=>ci(v)*GM+ci(u);
  for(let j=0;j<GM;j++) for(let i=0;i<GM;i++){ const k=j*GM+i, u=cu(i), v=cu(j), d=Math.hypot(u,v); gh[k]=H0[(j*G)*WN+i*G];
    let p=(d>MAP_R-36&&!(WGEN.seaW(u,v)>0.5))||d<FLAT_R+78?-1:0; // not past the rim (the bay itself lies past it), not across the build field
    if(p>=0) for(const t of TOWNS){ const dt=Math.hypot(SPAWN[0]+u-t.x,SPAWN[2]+v-t.z); if(dt<t.R+38){ p=-1; break; } if(dt<t.R+70) p+=60; } // nor through a town
    pen[k]=p; }
  for(const rd of WORLD.roads) for(const q of rd.pts){ const i0=ci(q[0]), j0=ci(q[1]); for(let b=-2;b<=2;b++) for(let a=-2;a<=2;a++){ const i=i0+a, j=j0+b; if(i<0||j<0||i>=GM||j>=GM) continue; const k=j*GM+i; if(pen[k]>=0&&pen[k]<1000) pen[k]+=1000; } } // (1000 and up: on or beside a road. A river may cross one, at a price, but not run along it)
  const D8=[[1,0,8],[-1,0,8],[0,1,8],[0,-1,8],[1,1,11.3137],[1,-1,11.3137],[-1,1,11.3137],[-1,-1,11.3137]];
  function drain(seeds,CUT){
    const Mx=new Float32Array(NG).fill(1e9), Ln=new Float32Array(NG).fill(1e9), prev=new Int32Array(NG).fill(-1), done=new Uint8Array(NG), heap=[];
    const less=(a,b)=>a[0]<b[0]-1e-4||(a[0]<b[0]+1e-4&&a[1]<b[1]);
    const push=(m,l,k)=>{ heap.push([m,l,k]); let c=heap.length-1; while(c>0){ const p=(c-1)>>1; if(!less(heap[c],heap[p])) break; [heap[p],heap[c]]=[heap[c],heap[p]]; c=p; } };
    const pop=()=>{ const top=heap[0], last=heap.pop(); if(heap.length){ heap[0]=last; let c=0; for(;;){ const l=c*2+1, r=l+1; let m=c; if(l<heap.length&&less(heap[l],heap[m])) m=l; if(r<heap.length&&less(heap[r],heap[m])) m=r; if(m===c) break; [heap[m],heap[c]]=[heap[c],heap[m]]; c=m; } } return top; };
    for(const [k,m] of seeds){ Mx[k]=m; Ln[k]=0; push(m,0,k); }
    while(heap.length){ const [m,l,k]=pop(); if(done[k]) continue; done[k]=1; const i=k%GM, j=(k-i)/GM;
      for(const [di,dj,L] of D8){ const ni=i+di, nj=j+dj; if(ni<0||nj<0||ni>=GM||nj>=GM) continue; const nk=nj*GM+ni; if(done[nk]||pen[nk]<0||gh[nk]<m-CUT) continue;
        const nm=Math.max(m,gh[nk]), nl=l+L+(pen[nk]>=1000?O.road+pen[nk]-1000:pen[nk]); if(nm<Mx[nk]-1e-4||(nm<Mx[nk]+1e-4&&nl<Ln[nk])){ Mx[nk]=nm; Ln[nk]=nl; prev[nk]=k; push(nm,nl,nk); } } }
    return {prev,done}; }
  const trace=(D,k,stop)=>{ const path=[]; for(;k>=0;k=D.prev[k]){ path.push(k); if(stop&&stop(k)&&path.length>1) break; } return path; };
  const roadRuns=path=>{ let runs=0, longest=0, run=0; for(const k of path){ if(pen[k]>=1000){ if(!run) runs++; run++; if(run>longest) longest=run; } else run=0; } return [runs,longest]; };
  // grid path -> a smooth centreline every 2 m, wandering a little, with its water surface: never rising, and at least 0.9 m under the ground it passes
  function shape(path,amp,seed,endY,hw0,hw1,depth){
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
    const m=Math.min(n-1,30), ym=y[n-1-m]; for(let q=n-1-m;q<n;q++){ const f=(q-(n-1-m))/m; y[q]=Math.min(y[q],ym+(endY-ym)*f*f*(3-2*f)); } // down to the level it runs into over its last 60 m
    for(let q=0;q<n;q++) if(y[q]<endY) y[q]=endY;
    for(let pass=0;pass<2;pass++){ for(let q=0;q<n;q++){ let s2=0, c2=0; for(let w=-4;w<=4;w++){ const z=q+w; if(z<0||z>=n) continue; s2+=y[z]; c2++; } tmp[q]=s2/c2; } for(let q=0;q<n;q++){ y[q]=Math.min(tmp[q],q?y[q-1]:tmp[q],t[q]-0.6); if(y[q]<endY) y[q]=endY; } }
    let q0=0; for(let q=n-1;q>=10;q--) if(y[q-10]-y[q]>4.4){ q0=q; break; } // it starts where the fall eases to about 1 in 5: above that it would be a waterfall, not a stream
    let sum=0; const out=[]; for(let q=q0;q<n;q++){ const cut=t[q]-y[q]; sum+=cut; const hw=(hw0+(hw1-hw0)*(q-q0)/Math.max(1,n-1-q0))*(0.7+0.3*Math.min(1,(q-q0)/30)); // a little narrower at the top, widening as it goes
      out.push([rs[q][0],rs[q][1],y[q],hw,Math.max(4,Math.min(12,cut*2.2+3)),depth*Math.min(1,hw/hw0)]); }
    return {pts:out,mean:sum/Math.max(1,n-q0)}; }
  // the main river
  const a0=Math.atan2(-S.nz,-S.nx), seeds=[];
  for(let k=0;k<NG;k++){ if(pen[k]<0||gh[k]>=S.Y-0.2) continue; const u=cu(k%GM), v=cu((k-k%GM)/GM), al=u*S.nx+v*S.nz, lat=Math.abs(v*S.nx-u*S.nz); if(al<S.C0+70&&lat<230&&lat>110) seeds.push([k,S.Y]); } // it comes out on the beach to one side of the town
  const D=drain(seeds,O.cut); let src=-1;
  for(const da of [0,0.15,-0.15,0.3,-0.3,0.45,-0.45]){ const k=cellOf(Math.cos(a0+da)*(MAP_R-60),Math.sin(a0+da)*(MAP_R-60)); if(D.done[k]&&gh[k]>=18){ src=k; break; } }
  if(src<0) return RV;
  RV.push(Object.assign(shape(trace(D,src),O.amp,3.3,S.Y,O.hw0,O.hw1,O.depth),{main:true,into:-1}));
  // streams
  const wet=new Int32Array(NG).fill(-1), mark=(rv,idx)=>rv.pts.forEach((p,q)=>{ const k=cellOf(p[0],p[1]); if(wet[k]<0) wet[k]=idx*100000+q; }); mark(RV[0],0);
  const cands=[], flank=[]; for(const M of WGEN.MASSIFS){ let bd=1e9, bp=null; for(const p of RV[0].pts){ const d=Math.hypot(p[0]-M.u,p[1]-M.v); if(d<bd){ bd=d; bp=p; } }
    const dx=(bp[0]-M.u)/bd, dz=(bp[1]-M.v)/bd; for(const r of [0,1.9,-1.9]){ const c=Math.cos(r), sn=Math.sin(r); (r?flank:cands).push([M.u+(dx*c-dz*sn)*M.R*O.foot,M.v+(dz*c+dx*sn)*M.R*O.foot]); } } // the side of each range facing the river first, then round their flanks
  { const mp=RV[0].pts, mn=mp.length; for(const [f,sd] of [[0.3,1],[0.55,-1],[0.75,1],[0.15,-1],[0.45,1],[0.65,-1],[0.88,1],[0.3,-1]]){ const q=Math.round(f*(mn-1)), a=mp[Math.max(0,q-5)], b=mp[Math.min(mn-1,q+5)], tl=Math.hypot(b[0]-a[0],b[1]-a[1])||1; cands.push([mp[q][0]-(b[1]-a[1])/tl*sd*330,mp[q][1]+(b[0]-a[0])/tl*sd*330]); } } // then from the open country to either side of the river
  cands.push(...flank); for(const da of [1.5,-1.5,0.8,-0.8]) cands.push([Math.cos(a0+da)*(MAP_R-60),Math.sin(a0+da)*(MAP_R-60)]);
  const ws=[]; for(let k=0;k<NG;k++){ if(wet[k]>=0) ws.push([k,Math.max(gh[k],RV[0].pts[wet[k]%100000][2]+0.6+O.cut)]); else if(pen[k]>=0&&gh[k]<S.Y-0.2) ws.push([k,S.Y]); } // (a stream may not run lower than the water it joins; or it runs straight into the bay)
  const D2=drain(ws,O.cut);
  RV.rej=[]; for(const [u,v] of cands){ if(RV.length>O.maxStreams) break; const sk=cellOf(u,v); if(pen[sk]<0||wet[sk]>=0||!D2.done[sk]){ RV.rej.push([Math.round(u),Math.round(v),'cell',pen[sk],D2.done[sk]]); continue; }
    const path=trace(D2,sk,k=>wet[k]>=0), tag=wet[path[path.length-1]], [runs,longest]=roadRuns(path); if(runs>3||longest>13||path.length<14||path.length>300){ RV.rej.push([Math.round(u),Math.round(v),'path',runs,longest,path.length]); continue; } // not along a road, not across many, not tiny, not endless
    const into=tag>=0?RV[Math.floor(tag/100000)]:null, jq=tag%100000, jy=into?into.pts[jq][2]:S.Y, st=shape(path,O.amp*0.6,7.1+RV.length*2.3,jy,O.shw,O.shw*1.25,O.sdepth);
    if(into){ const e=st.pts[st.pts.length-1]; e[0]=into.pts[jq][0]; e[1]=into.pts[jq][1]; e[2]=jy; }
    if(st.pts.length<55||st.mean<0.3){ RV.rej.push([Math.round(u),Math.round(v),'shape',st.pts.length,+st.mean.toFixed(2)]); continue; }
    { let worst=0; for(const rd of WORLD.roads){ if(rd.street) continue; let run=0; for(const rp of rd.pts){ let nearIt=false; for(let q=0;q<st.pts.length;q+=2){ const sp=st.pts[q]; if(Math.abs(sp[0]-rp[0])<12&&Math.abs(sp[1]-rp[1])<12&&Math.hypot(sp[0]-rp[0],sp[1]-rp[1])<sp[3]+9.5){ nearIt=true; break; } } run=nearIt?run+1:0; if(run>worst) worst=run; } }
      if(worst>15){ RV.rej.push([Math.round(u),Math.round(v),'alongroad',worst]); continue; } } /* (it would run beside a road for 30 m or more: no place for a bridge) */ RV.push(Object.assign(st,{main:false,into:into?Math.floor(tag/100000):-1,jq})); mark(RV[RV.length-1],RV.length-1); }
  return RV; }
'''
rep("function townAt(x,z,pad){", ROUTE.strip('\n') + r'''
/* The rivers, cut into the land as it now stands (roads and towns done): a rounded bed under the water, a low bank
   at each side, and the ground sloping back up to where it was (farther where the cut is deeper). Roads keep their
   own ground, except where a river runs under them: there the land is cut away and the road is a bridge. */
{ const {RVD,RVY,RVW,RVB,RVP,WS,SAND,GRASS,ROCK}=WORLD, NN=WN*WN;
  for(let c=0;c<NN;c++){ const dd=RVD[c]; if(dd>=1e4) continue; const hw=RVW[c]; if(WRD[c]<5&&dd>=hw+3) continue;
    const ys=RVY[c], h0=WH[c]; let h;
    if(dd<=hw){ const a=dd/hw; h=ys-RVP[c]*(1-a*a); }
    else { const t=(dd-hw)/RVB[c]; if(t>=1) continue; const lip=ys+0.3*Math.min(1,(dd-hw)/1.2); h=lip+(h0-lip)*t*t*(3-2*t); }
    WH[c]=h; if(dd<hw-0.15&&h<ys-0.04&&WS[c]<-999) WS[c]=ys;
    if(dd<hw+1.5) GRASS[c]=0; const sd=Math.round(215*(1-sstep(hw*0.55,hw+1.8,dd))); if(sd>SAND[c]) SAND[c]=sd; if(dd<hw) ROCK[c]=Math.round(ROCK[c]*0.3); } }
function townAt(x,z,pad){''')
rep("  // the ground under and beside the roads, cut again for the roads as they now are. Where two roads come close (a", r'''  // ---- rivers: where they run, and which stretches of road cross them (those become bridges, humped up to clear the water)
  { const NN=WN*WN, RVD=WORLD.RVD=new Float32Array(NN).fill(1e4), RVY=WORLD.RVY=new Float32Array(NN), RVW=WORLD.RVW=new Float32Array(NN), RVB=WORLD.RVB=new Float32Array(NN), RVP=WORLD.RVP=new Float32Array(NN);
    const RV=WORLD.rivers=routeRivers(); WORLD.bridges=[];
    for(const rv of RV){ const p=rv.pts, n=p.length; // every cell near a river remembers the nearest stretch of it
      for(let q=0;q<n-1;q++){ const [x0,z0,y0,w0,b0,d0]=p[q], [x1,z1,y1,w1,b1,d1]=p[q+1], ex=x1-x0, ez=z1-z0, el=ex*ex+ez*ez||1e-6, R2=Math.max(w0,w1)+Math.max(b0,b1)+0.5;
        const i0=Math.max(0,Math.floor((Math.min(x0,x1)-R2+WHALF)/WHS)), i1=Math.min(WN-1,Math.ceil((Math.max(x0,x1)+R2+WHALF)/WHS)), j0=Math.max(0,Math.floor((Math.min(z0,z1)-R2+WHALF)/WHS)), j1=Math.min(WN-1,Math.ceil((Math.max(z0,z1)+R2+WHALF)/WHS));
        for(let j=j0;j<=j1;j++){ const pz=-WHALF+j*WHS; for(let i=i0;i<=i1;i++){ const px=-WHALF+i*WHS; let f=((px-x0)*ex+(pz-z0)*ez)/el; f=f<0?0:f>1?1:f;
          const dd=Math.hypot(px-(x0+ex*f),pz-(z0+ez*f)), hw=w0+(w1-w0)*f, bb=b0+(b1-b0)*f, c=j*WN+i; if(dd<hw+bb&&dd-hw<RVD[c]-RVW[c]){ RVD[c]=dd; RVW[c]=hw; RVY[c]=y0+(y1-y0)*f; RVB[c]=bb; RVP[c]=d0+(d1-d0)*f; } } } } }
    if(RV.length) for(const rd of WORLD.roads){ if(rd.street) continue; const p=rd.pts, n=p.length, dk=new Uint8Array(n); let any=false;
      const cellAt=(u,v)=>{ const i=Math.round((u+WHALF)/WHS), j=Math.round((v+WHALF)/WHS); return i<0||j<0||i>=WN||j>=WN?-1:j*WN+i; };
      for(let q=0;q<n;q++){ const a=p[Math.max(0,q-1)], b=p[Math.min(n-1,q+1)]; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1, sx=-tz/tl, sz=tx/tl;
        for(const o of [-4.6,-2.3,0,2.3,4.6]){ const c=cellAt(p[q][0]+sx*o,p[q][1]+sz*o); if(c>=0&&RVD[c]<RVW[c]+4.5){ dk[q]=1; any=true; break; } } }
      if(!any) continue; const deck=rd.deck=new Uint8Array(n), raise=new Float32Array(n); for(let q=0;q<n;q++) if(dk[q]||(q>0&&dk[q-1])||(q<n-1&&dk[q+1])) deck[q]=1;
      for(let q=0;q<n;q++){ if(!deck[q]) continue; let e=q; while(e+1<n&&deck[e+1]) e++; let need=0;
        for(let k=q;k<=e;k++){ const c=cellAt(p[k][0],p[k][1]); if(c>=0&&RVD[c]<1e4) need=Math.max(need,RVY[c]+2.2-p[k][2]); } // the deck stands at least 2.2 m over the water
        WORLD.bridges.push({rd,q0:q,q1:e});
        if(need>0) for(let k=Math.max(0,q-16);k<=Math.min(n-1,e+16);k++){ const d=k<q?q-k:k>e?k-e:0, w=d?0.5+0.5*Math.cos(Math.PI*d/16):1; raise[k]=Math.max(raise[k],need*w); }
        q=e; }
      for(let q=0;q<n;q++) p[q][2]+=raise[q]; } }
  // the ground under and beside the roads, cut again for the roads as they now are. Where two roads come close (a''')
# the road surface: across a bridge the asphalt gives way to the deck
rep("    for(const c of AC){ const px=x+sx*ROAD_HW*c, pz=z+sz*ROAD_HW*c, h=terrainH(px,pz), e=0.6, gx=(terrainH(px+e,pz)-terrainH(px-e,pz))/(2*e), gz=(terrainH(px,pz+e)-terrainH(px,pz-e))/(2*e), nl=Math.hypot(gx,1,gz);",
    "    const dk=rd.deck&&rd.deck[q];\n    for(const c of AC){ const px=x+sx*ROAD_HW*c, pz=z+sz*ROAD_HW*c, h=dk?p[q][2]:terrainH(px,pz), e=0.6, gx=dk?0:(terrainH(px+e,pz)-terrainH(px-e,pz))/(2*e), gz=dk?0:(terrainH(px,pz+e)-terrainH(px,pz-e))/(2*e), nl=Math.hypot(gx,1,gz);")
rep("  for(let q=0;q<n-1;q++) for(let c=0;c<NC-1;c++){\n    const L0=q*NC+c, R0=L0+1, L1=L0+NC, R1=L1+1;\n    if(up(L0,L1,R0)) idx.push(L0,L1,R0); else idx.push(L0,R0,L1);",
    "  for(let q=0;q<n-1;q++) for(let c=0;c<NC-1;c++){ if(rd.deck&&rd.deck[q]&&rd.deck[q+1]) continue; // (a bridge deck takes over here)\n    const L0=q*NC+c, R0=L0+1, L1=L0+NC, R1=L1+1;\n    if(up(L0,L1,R0)) idx.push(L0,L1,R0); else idx.push(L0,R0,L1);")
# solids that stand still are looked up through a grid now (there are many more of them with the bridges)
rep("var STATICS=[];", r'''var STATICS=[];
function staticsInto(ps,x,z,r){ if(STATICS._n!==STATICS.length){ const g=STATICS._g=new Map(); for(const q of STATICS){ const k=(Math.floor(q.x/8)+4096)*8192+Math.floor(q.z/8)+4096; let l=g.get(k); if(!l){ l=[]; g.set(k,l); } l.push(q); } STATICS._n=STATICS.length; }
  const g=STATICS._g, R=r+5, i0=Math.floor((x-R)/8), i1=Math.floor((x+R)/8), j0=Math.floor((z-R)/8), j1=Math.floor((z+R)/8);
  for(let i=i0;i<=i1;i++) for(let j=j0;j<=j1;j++){ const l=g.get((i+4096)*8192+j+4096); if(l) for(const q of l){ const rr=r+(q.r||0); if(Math.abs(q.x-x)<rr&&Math.abs(q.z-z)<rr) ps.add(q.solid); } } return ps; }''')
rep("for(const q of STATICS) if(Math.abs(q.x-E.pos.x)<3&&Math.abs(q.z-E.pos.z)<3) ps.add(q.solid);","staticsInto(ps,E.pos.x,E.pos.z,3);")
rep("for(const q of STATICS) if(Math.abs(q.x-x)<4&&Math.abs(q.z-z)<4) ps.add(q.solid);","staticsInto(ps,x,z,4);")
rep("  const ps=near(k.x,k.z,1), w=kartGround(k,ps), gC=(w[0]+w[1]+w[2]+w[3])/4;","  const ps=staticsInto(near(k.x,k.z,1),k.x,k.z,4), w=kartGround(k,ps), gC=(w[0]+w[1]+w[2]+w[3])/4;")
rep("  const w=kartGround(k,near(k.x,k.z,1)), gC=(w[0]+w[1]+w[2]+w[3])/4;","  const w=kartGround(k,staticsInto(near(k.x,k.z,1),k.x,k.z,4)), gC=(w[0]+w[1]+w[2]+w[3])/4;")
rep("  const ps=dCam<40&&!k.air?near(k.x,k.z,1):null; if(ps) kartGround(k,ps);","  const ps=dCam<40&&!k.air?staticsInto(near(k.x,k.z,1),k.x,k.z,4):null; if(ps) kartGround(k,ps);")
rep("      const [g]=groundAt(nx,nz,d.pos.y+0.3,near(nx,nz));","      const [g]=groundAt(nx,nz,d.pos.y+0.3,staticsInto(near(nx,nz),nx,nz,1));")
rep("    else { const [g]=groundAt(d.pos.x,d.pos.z,d.pos.y+0.3,near(d.pos.x,d.pos.z));","    else { const [g]=groundAt(d.pos.x,d.pos.z,d.pos.y+0.3,staticsInto(near(d.pos.x,d.pos.z),d.pos.x,d.pos.z,1));")
rep("    if(c<0||townAt(x,z,8)||roadDistAt(x,z)<7||WORLD.SNOW[c]>30||WORLD.ROCK[c]>150||chests.some(q=>Math.hypot(q.x-x,q.z-z)<70)","    if(c<0||shoreAt(x,z)||townAt(x,z,8)||roadDistAt(x,z)<7||WORLD.SNOW[c]>30||WORLD.ROCK[c]>150||chests.some(q=>Math.hypot(q.x-x,q.z-z)<70)")
# the bridges themselves
rep("function buildRails(){", r'''/* Bridges: where a road crosses a river the land under it is cut away and the road runs on a concrete deck with a
   parapet each side, on piers standing in the water. The deck and parapets are solid (you walk and drive on them
   like any floor); under the deck is open, and the river runs through. */
function buildBridges(){ if(!WORLD.bridges||!WORLD.bridges.length) return; const parts=[], col=new THREE.Color();
  const put=(g,c)=>{ if(g.index) g=g.toNonIndexed(); g.computeVertexNormals(); col.setHex(c); const n=g.attributes.position.count, ca=new Float32Array(n*3); for(let q=0;q<n;q++){ ca[q*3]=col.r; ca[q*3+1]=col.g; ca[q*3+2]=col.b; } g.setAttribute('color',new THREE.BufferAttribute(ca,3)); parts.push(g); };
  for(const B of WORLD.bridges){ const p=B.rd.pts, n=p.length, F=[];
    for(let q=B.q0;q<=B.q1;q++){ const a=p[Math.max(0,q-1)], b=p[Math.min(n-1,q+1)]; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; F.push([SPAWN[0]+p[q][0],SPAWN[2]+p[q][1],p[q][2]+0.07,-tz/tl,tx/tl]); }
    // a ribbon along the bridge between two offsets across it, each at its own height over the deck line
    const strip=(o0,y0,o1,y1,c)=>{ const pos=[]; for(let q=0;q<F.length-1;q++){ const A=F[q], Bq=F[q+1];
        const a0=[A[0]+A[3]*o0,A[2]+y0,A[1]+A[4]*o0], a1=[A[0]+A[3]*o1,A[2]+y1,A[1]+A[4]*o1], b0=[Bq[0]+Bq[3]*o0,Bq[2]+y0,Bq[1]+Bq[4]*o0], b1=[Bq[0]+Bq[3]*o1,Bq[2]+y1,Bq[1]+Bq[4]*o1]; pos.push(...a0,...a1,...b0, ...a1,...b1,...b0); }
      const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); put(g,c); };
    const DECK=0x83878d, WALL=0xc8c3b6, UNDER=0x7a766e, PIER=0xa29e94;
    strip(-4.1,0.02,4.1,0.02,DECK); strip(-4.45,-0.6,4.45,-0.6,UNDER);
    for(const sd of [-1,1]){ strip(sd*4.45,-0.6,sd*4.45,0.95,WALL); strip(sd*4.1,0.02,sd*4.1,0.95,WALL); strip(sd*4.1,0.95,sd*4.45,0.95,WALL); strip(sd*0.08,0.03,sd*0.2,0.03,0xe6c23c); } // the parapets; a double yellow line down the middle
    // piers every 8 m where the deck is well clear of the ground, and a block of stone under each end
    const block=(A,w,h,d,yTop,c)=>{ const g=new THREE.BoxGeometry(w,h,d); g.rotateY(Math.atan2(-A[4],A[3])); g.translate(A[0],yTop-h/2,A[1]); put(g,c); };
    const inCh=F.map(A=>{ const c=worldCell(A[0],A[1]); return c>=0&&WORLD.RVD[c]<WORLD.RVW[c]+0.9; }), at=[]; // piers at the water's edge each side (and one more mid-span if that leaves more than 16 m)
    for(let q=1;q<F.length-1;q++) if(inCh[q]!==inCh[q-1]) at.push(inCh[q]?q-1:q);
    for(let k=0;k+1<at.length;k+=2) if(at[k+1]-at[k]>8) at.push(Math.round((at[k]+at[k+1])/2));
    for(const q of at){ const A=F[q], gy=terrainH(A[0],A[1]); if(A[2]-gy<1.2) continue; const top=A[2]-0.6, h=top-(gy-0.9); block(A,7.6,h,1.0,top,PIER); block(A,8.2,0.3,1.4,top,WALL);
      for(let o=-3.3;o<=3.31;o+=1.1){ const x=A[0]+A[3]*o, z=A[1]+A[4]*o; STATICS.push({x,z,solid:{boxes:[[x-0.55,gy-0.9,z-0.55,x+0.55,top,z+0.55]],key:'pier'+STATICS.length}}); } }
    for(const A of [F[0],F[F.length-1]]) block(A,9.4,3.4,2.2,A[2]-0.03,PIER);
    // what you stand on: the deck and its parapets as rows of small flat boxes (a slice across the bridge every metre)
    for(let q=0;q<F.length-1;q++) for(const f of [0,0.5]){ const A=F[q], Bq=F[q+1], x=A[0]+(Bq[0]-A[0])*f, z=A[1]+(Bq[1]-A[1])*f, y=A[2]+(Bq[2]-A[2])*f+0.02, sx=A[3], sz=A[4], boxes=[];
        for(let o=-3.6;o<=3.61;o+=0.9){ const bx=x+sx*o, bz=z+sz*o; boxes.push([bx-0.56,y-0.6,bz-0.56,bx+0.56,y,bz+0.56]); }
        for(const o of [-4.58,4.58]){ const bx=x+sx*o, bz=z+sz*o; boxes.push([bx-0.5,y-0.6,bz-0.5,bx+0.5,y+0.95,bz+0.5]); }
        STATICS.push({x,z,r:5.2,solid:{boxes,key:'deck'+STATICS.length}}); } }
  const pos=[],nor=[],cc=[]; parts.forEach(g=>{ pos.push(...g.attributes.position.array); nor.push(...g.attributes.normal.array); cc.push(...g.attributes.color.array); });
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos,3)); g.setAttribute('normal',new THREE.Float32BufferAttribute(nor,3)); g.setAttribute('color',new THREE.Float32BufferAttribute(cc,3)); g.computeBoundingSphere();
  const m=new THREE.Mesh(g,new THREE.MeshLambertMaterial({vertexColors:true,side:THREE.DoubleSide})); m.castShadow=m.receiveShadow=true; m.matrixAutoUpdate=false; scene.add(m); }
function buildRails(){''')
rep("syncMats(); buildRails(); buildLandmarks(); buildSigns();","syncMats(); buildBridges(); buildRails(); buildLandmarks(); buildSigns();")

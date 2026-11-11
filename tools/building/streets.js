/* ---------- town streets: each town on a grid ----------
   A main street and a cross street through the middle of town make four blocks; the houses stand in rows along
   them. The main street lines up with the first road coming in. Roads from outside no longer cut through town to
   its centre: each one now stops at the edge of the flat town ground and joins the end of the nearest street.
   Old road traces inside towns (dirt, bare ground) are cleared. */
{ const rdPts=[];
  for(const t of TOWNS){
    let ax='x', best=1e9;
    for(const rd of WORLD.roads) for(const end of [0,1]){ const p=end?rd.pts[rd.pts.length-1]:rd.pts[0], q=end?rd.pts[Math.max(0,rd.pts.length-12)]:rd.pts[Math.min(rd.pts.length-1,11)];
      const d=Math.hypot(SPAWN[0]+p[0]-t.x,SPAWN[2]+p[1]-t.z); if(d<best&&d<4){ best=d; ax=Math.abs(q[0]-p[0])>=Math.abs(q[1]-p[1])?'x':'z'; } }
    t.axis=ax; t.streetL=Math.floor((t.R-4)/CELL)*CELL; const Ls=t.streetL;
    t.ends=[[t.x-Ls,t.z],[t.x+Ls,t.z],[t.x,t.z-Ls],[t.x,t.z+Ls]];
    // reroute: cut each road where it enters the flat town ground, then run straight to the nearest street end
    const cut=t.R-2;
    for(const rd of WORLD.roads){ if(rd.street) continue;
      for(const end of [0,1]){ const P=end?rd.pts.slice().reverse():rd.pts.slice();
        if(Math.hypot(SPAWN[0]+P[0][0]-t.x,SPAWN[2]+P[0][1]-t.z)>4) continue; // this end isn't at this town
        let k=0; while(k<P.length-1&&Math.hypot(SPAWN[0]+P[k][0]-t.x,SPAWN[2]+P[k][1]-t.z)<cut) k++;
        const at=[SPAWN[0]+P[k][0],SPAWN[2]+P[k][1]], e=t.ends.reduce((a,b)=>Math.hypot(b[0]-at[0],b[1]-at[1])<Math.hypot(a[0]-at[0],a[1]-at[1])?b:a);
        // a smooth curve: it leaves the street end straight out along the street, and bends to meet the road the way it comes in
        const L=Math.hypot(at[0]-e[0],at[1]-e[1]), ax_=[(e[0]-t.x)/Ls,(e[1]-t.z)/Ls];
        const pin=k>0?[SPAWN[0]+P[k-1][0]-at[0],SPAWN[2]+P[k-1][1]-at[1]]:[t.x-at[0],t.z-at[1]], pl=Math.hypot(pin[0],pin[1])||1, din=[pin[0]/pl,pin[1]/pl];
        const k1=Math.min(L*0.45,Math.max(2,t.R-3-Ls)), k2=L*0.45, C1=[e[0]+ax_[0]*k1,e[1]+ax_[1]*k1], C2=[at[0]+din[0]*k2,at[1]+din[1]*k2];
        const n=Math.max(2,Math.round(L/1.5)), conn=[];
        for(let q=0;q<n;q++){ const f=q/n, g=1-f, w0=g*g*g, w1=3*g*g*f, w2=3*g*f*f, w3=f*f*f;
          conn.push([w0*e[0]+w1*C1[0]+w2*C2[0]+w3*at[0]-SPAWN[0],w0*e[1]+w1*C1[1]+w2*C2[1]+w3*at[1]-SPAWN[2],t.h]); }
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
  // put the remaining road traces back into the road-distance grid near towns, and keep grass off every road
  for(const rd of WORLD.roads){ for(const p of rd.pts){ const x=SPAWN[0]+p[0], z=SPAWN[2]+p[1];
      for(let dj=-4;dj<=4;dj++) for(let di=-4;di<=4;di++){ const c=worldCell(x+di*WHS,z+dj*WHS); if(c<0) continue; const d=Math.hypot(di*WHS,dj*WHS); if(d<WRD[c]) WRD[c]=d; if(d<4.8) WORLD.GRASS[c]=0; } } }
  for(const t of TOWNS) for(const X of [true,false]) for(let s=-t.streetL;s<=t.streetL;s+=1) for(let c=-6;c<=6;c+=1){ const cc=worldCell(X?t.x+s:t.x+c,X?t.z+c:t.z+s); if(cc>=0) WORLD.GRASS[cc]=0; } // sidewalks too
}

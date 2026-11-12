const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,TOWNS,WORLD,SIDEWALKS,streetDist,townIn,SPAWN,CELL,ROAD_HW,WALK_W,townBulbs'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.props&&T.props.length>1000,null,{timeout:180000}); await sleep(3000);
 const r=await pg.evaluate(()=>{ const out=[]; let bad=[];
  for(const t of T.TOWNS){ const o={n:t.name,k:t.kind||'',R:t.R,segs:(t.segs||[]).map(S=>(S.X?'x':'z')+S.ci+':'+S.ai+'..'+S.bi+(S.lane?'L':'')).join(' '),ends:t.ends.length,edge:t.endEdge.join(''),dead:(t.dead||[]).map(d=>d?1:0).join(''),junc:(t.junc||[]).length,houses:t.houses.length};
    out.push(o);
    if(t.kind) continue;
    for(const h of t.houses){ const C=T.CELL; for(let a=0;a<=h.w;a+=0.5) for(let c=0;c<=h.d;c+=0.5){ const x=(h.i0+a)*C, z=(h.j0+c)*C; if(T.streetDist(t,x,z)<T.ROAD_HW+T.WALK_W+0.2){ bad.push('house on street '+t.name+' '+h.i0+','+h.j0); a=1e9; break; } } if(!T.townIn(t,(h.i0+h.w/2)*C,(h.j0+h.d/2)*C,0)) bad.push('house out '+t.name); }
    // every road in joins an edge end
    for(const rd of T.WORLD.roads){ if(rd.street) continue; for(const p of [rd.pts[0],rd.pts[rd.pts.length-1]]){ const x=T.SPAWN[0]+p[0], z=T.SPAWN[2]+p[1]; const k=t.ends.findIndex(e=>Math.hypot(e[0]-x,e[1]-z)<3); if(k>=0&&!t.endEdge[k]) bad.push('road at inner end '+t.name); } }
  }
  // sidewalks shouldn't lie on any street road
  let sw=0; for(const [a,b2] of T.SIDEWALKS){ const mx=(a[0]+b2[0])/2, mz=(a[1]+b2[1])/2; for(const t of T.TOWNS){ if(t.kind||!t.segs) continue; if(Math.hypot(mx-t.x,mz-t.z)>t.R+20) continue; if((t.segs||[]).some(S=>{ const al=S.X?mx:mz, ac=S.X?mz:mx; return al>S.a&&al<S.b&&Math.abs(ac-S.c)<T.ROAD_HW-0.3; })){ sw++; if(bad.length<40) bad.push("walk "+t.name+" "+a.map(v=>v.toFixed(1))+" "+b2.map(v=>v.toFixed(1))); } } }
  return {out,bad:bad.slice(0,20),nbad:bad.length,sw,roads:T.WORLD.roads.length}; });
 console.log(JSON.stringify(r,null,0).replace(/\},\{/g,'},\n{')); console.log('errs',errs.slice(0,5)); await b.close(); })();

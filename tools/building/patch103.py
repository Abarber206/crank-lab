# ---------- 103. more cars (some left standing in a lane, some parked at the kerb in town) and steel guard rails where
# the ground falls away beside a road, plus a few stretches here and there ----------
rep("    add('car',x,z,1,Math.atan2(-tz,tx)+(r()<0.5?Math.PI:0)); parked++; }\n}",
"""    add('car',x,z,1,Math.atan2(-tz,tx)+(r()<0.5?Math.PI:0)); parked++; }
  { const r2=seeded(77120311); let lane=0, kerb=0; const perTown=new Map();
    for(let t=0;t<1500&&(lane<9||kerb<16)&&roads.length;t++){ const rd=roads[Math.floor(r2()*roads.length)], n=rd.pts.length; if(n<9) continue;
      const q=4+Math.floor(r2()*(n-8)), a=rd.pts[q-3], b=rd.pts[q+3], side=r2()<0.5?-1:1, flip=r2()<0.5?Math.PI:0; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl;
      const off=rd.street?2.45:1.9, x=SPAWN[0]+rd.pts[q][0]-tz*off*side, z=SPAWN[2]+rd.pts[q][1]+tx*off*side;
      if(rd.street){ const tw=rd.town, dc=Math.hypot(x-tw.x,z-tw.z); if(kerb>=16||(perTown.get(tw)||0)>=2||dc<11||dc>tw.streetL-12||!roomy(x,z,'car')) continue;
        const p=add('car',x,z,1,Math.atan2(-tz,tx)+(side>0?Math.PI:0)); p.yard=true; perTown.set(tw,(perTown.get(tw)||0)+1); kerb++; }
      else { if(lane>=9||rd.skip[q]||townAt(x,z,14)||Math.abs(terrainH(x,z)-rd.pts[q][2])>0.5||!roomy(x,z,'car')) continue; if(typeof nearOther==='function'&&nearOther(roads.indexOf(rd),x,z)<30) continue;
        add('car',x,z,1,Math.atan2(-tz,tx)+flip+(r2()-0.5)*0.5); lane++; } } }
}
/* Guard rails: posts and a steel beam along the side of a road where the ground drops away, and a few more at random. */
function buildRails(){ const parts=[], roads=WORLD.roads, OFF=ROAD_HW+1.15;
  roads.forEach((rd,k)=>{ if(rd.street) return; const p=rd.pts, n=p.length;
    for(const side of [-1,1]){ const want=new Uint8Array(n), at=[];
      for(let q=0;q<n;q++){ const a=p[Math.max(0,q-1)], b=p[Math.min(n-1,q+1)]; let tx=b[0]-a[0], tz=b[1]-a[1]; const tl=Math.hypot(tx,tz)||1; tx/=tl; tz/=tl;
        const nx=-tz*side, nz=tx*side, x=SPAWN[0]+p[q][0], z=SPAWN[2]+p[q][1]; at.push([x+nx*OFF,z+nz*OFF]);
        if(rd.skip[q]||q<3||q>n-4||townAt(x,z,10)||nearOther(k,x,z)<16) continue;
        const drop=p[q][2]-terrainH(x+nx*10,z+nz*10), here=Math.abs(terrainH(x+nx*OFF,z+nz*OFF)-p[q][2]);
        if(here<0.7&&(drop>1.7||gnoise(q*0.045+k*7.3,side*3.1+k,9127)>0.52)) want[q]=1; }
      for(let q=1;q<n-1;q++) if(!want[q]&&want[q-1]&&want[q+1]&&!rd.skip[q]) want[q]=1; // close single gaps
      let q=0; while(q<n){ if(!want[q]){ q++; continue; } let e=q; while(e+1<n&&want[e+1]) e++;
        if(e-q>=5) for(let j=q;j<=e;j++){ const [x,z]=at[j], y=terrainH(x,z);
          const post=new THREE.BoxGeometry(0.13,0.82,0.13); post.translate(x,y+0.41,z); parts.push(post);
          if(j<e){ const [x2,z2]=at[j+1], y2=terrainH(x2,z2), dx=x2-x, dz=z2-z, dy=y2-y, L=Math.hypot(dx,dz), L3=Math.hypot(L,dy);
            for(const [th,hh,yy] of [[0.07,0.3,0.6],[0.11,0.07,0.6]]){ const beam=new THREE.BoxGeometry(th,hh,L3+0.02); beam.rotateX(-Math.asin(dy/L3)); beam.rotateY(Math.atan2(dx,dz)); beam.translate((x+x2)/2,(y+y2)/2+yy,(z+z2)/2); parts.push(beam); }
            const boxes=[]; for(let s=0;s<3;s++){ const f0=s/3, f1=(s+1)/3, xa=x+dx*f0, xb=x+dx*f1, za=z+dz*f0, zb=z+dz*f1, yb=Math.min(y,y2); boxes.push([Math.min(xa,xb)-0.08,yb-0.3,Math.min(za,zb)-0.08,Math.max(xa,xb)+0.08,Math.max(y,y2)+0.82,Math.max(za,zb)+0.08]); }
            STATICS.push({x:(x+x2)/2,z:(z+z2)/2,solid:{boxes,key:'rail'+STATICS.length}}); } }
        q=e+1; } } });
  if(!parts.length) return; const g=mergeGeos(parts); g.computeBoundingSphere();
  const m=new THREE.Mesh(g,new THREE.MeshPhongMaterial({color:0xb4bac2,shininess:55,specular:0x555a60})); m.castShadow=true; m.receiveShadow=true; m.matrixAutoUpdate=false; m.frustumCulled=false; scene.add(m); }""")
rep("initProps(); props.forEach(p=>{ if(!p.yard&&townAt(p.x,p.z,6)){ p.gone=true; p.alive=false; p.g.visible=false; } }); syncMats();","initProps(); props.forEach(p=>{ if(!p.yard&&townAt(p.x,p.z,6)){ p.gone=true; p.alive=false; p.g.visible=false; } }); syncMats(); buildRails();")

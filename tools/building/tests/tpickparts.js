// pickaxes in one piece: for every pickaxe, every part touches the rest (bounding boxes, 4 mm slack), and in the
// Locker shoulder pose the hand is on the handle.  node tpickparts.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,heroFor,animateRig,OUTFITS,PICKAXES'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.heroFor,null,{timeout:180000}); await sleep(1000);
 const r=await pg.evaluate(()=>{ const out=[];
   for(const P of T.PICKAXES){ const H=T.heroFor(T.OUTFITS[0],P.id); T.scene.add(H.group); const S={showPick:true,bare:false,pos:new THREE.Vector3(),vel:new THREE.Vector3(),yaw:0,pitch:-0.05,onGround:true,gun:false};
     for(let i=0;i<12;i++) T.animateRig(H,S,1/30); H.group.updateMatrixWorld(true);
     const ms=[]; H.rig.pick.traverse(m=>{ if(m.isMesh&&m.visible&&!(m.material&&m.material.side===THREE.BackSide)) ms.push(m); });
     // the merged meshes split back into their separate pieces (connected triangles), each piece's box in world space
     const bx=[]; for(const m of ms){ const g=m.geometry, pa=g.attributes.position, n=pa.count, par=new Int32Array(n).map((_,i)=>i), f=i=>{ while(par[i]!==i){ par[i]=par[par[i]]; i=par[i]; } return i; }, u=(a,b)=>{ a=f(a); b=f(b); if(a!==b) par[a]=b; };
       const key=new Map(); for(let i=0;i<n;i++){ const k=Math.round(pa.getX(i)*2e4)+','+Math.round(pa.getY(i)*2e4)+','+Math.round(pa.getZ(i)*2e4); if(key.has(k)) u(i,key.get(k)); else key.set(k,i); }
       const ix=g.index; const tri=ix?ix.count:n; for(let t=0;t<tri;t+=3){ const a=ix?ix.getX(t):t, b2=ix?ix.getX(t+1):t+1, c=ix?ix.getX(t+2):t+2; u(a,b2); u(b2,c); }
       const comp=new Map(), v=new THREE.Vector3(); for(let i=0;i<n;i++){ const r=f(i); let B=comp.get(r); if(!B){ B=new THREE.Box3(); comp.set(r,B); } B.expandByPoint(v.fromBufferAttribute(pa,i).applyMatrix4(m.matrixWorld)); }
       for(const B of comp.values()) bx.push(B.expandByScalar(0.004)); }
     const seen=new Set([0]), q=[0];
     while(q.length){ const i=q.pop(); for(let j=0;j<bx.length;j++) if(!seen.has(j)&&bx[i].intersectsBox(bx[j])){ seen.add(j); q.push(j); } }
     const loose=bx.map((m,i)=>seen.has(i)?null:i).filter(x=>x!==null);
     // the hand on the handle: the hand's position against the handle line (pick's local y axis)
     const hp=H.rig.armR.hand.getWorldPosition(new THREE.Vector3()), lp=H.rig.pick.worldToLocal(hp.clone()); let top=-9; ms.forEach(m=>{ const bb=new THREE.Box3().setFromObject(m); const c=H.rig.pick.worldToLocal(bb.max.clone()); });
     const pb=new THREE.Box3(); ms.forEach(m=>{ m.geometry.computeBoundingBox(); const g=m.geometry.boundingBox.clone(); m.updateMatrixWorld(); const mm=new THREE.Matrix4().copy(H.rig.pick.matrixWorld).invert().multiply(m.matrixWorld); g.applyMatrix4(mm); if(Math.abs((g.min.x+g.max.x)/2)<0.03&&Math.abs((g.min.z+g.max.z)/2)<0.03) pb.union(g); });
     out.push({id:P.id,parts:bx.length,looseAt:loose.slice(0,3).map(i=>{ const c=bx[i].getCenter(new THREE.Vector3()); const l=H.rig.pick.worldToLocal(c); return [+l.x.toFixed(2),+l.y.toFixed(2),+l.z.toFixed(2)]; }),loose:loose.length,handAt:+lp.y.toFixed(3),handleTop:+(H.rig.pickTop||0).toFixed(3),off:+Math.hypot(lp.x,lp.z).toFixed(3)}); T.scene.remove(H.group); }
   return out; });
 r.forEach(x=>console.log(JSON.stringify(x)));
 const ok=r.every(x=>x.loose===0&&x.handAt<=x.handleTop-0.02&&x.off<0.05); console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

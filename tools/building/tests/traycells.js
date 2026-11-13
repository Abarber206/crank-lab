// shots look only at the pieces in the grid cells along the ray: the first piece hit is the same as testing every piece
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,order,piecesNearRay,TOWNS,terrainH'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.order.length>1000,null,{timeout:180000}); await sleep(1500);
 const r=await pg.evaluate(()=>{ const ray=new THREE.Raycaster(), all=[]; for(const p of T.order){ if(!p.group) continue; for(const m of p.group.children) if(!m.userData.decor) all.push(m); if(p.doorMeshes) all.push(...p.doorMeshes); }
   let same=0, diff=0, hitN=0, tNew=0, tOld=0; const R=(a,b)=>a+Math.random()*(b-a);
   for(let k=0;k<600;k++){ const t=T.TOWNS[k%T.TOWNS.length], o=new THREE.Vector3(t.x+R(-60,60),0,t.z+R(-60,60)); o.y=T.terrainH(o.x,o.z)+R(0.5,9); const d=new THREE.Vector3(R(-1,1),R(-0.3,0.3),R(-1,1)).normalize(), range=R(5,150);
     ray.set(o,d); ray.far=range; let s=performance.now(); const a=ray.intersectObjects(T.piecesNearRay(o,d,range),false)[0]; tNew+=performance.now()-s; s=performance.now(); const c=ray.intersectObjects(all,false)[0]; tOld+=performance.now()-s;
     const da=a?a.distance:-1, dc=c?c.distance:-1; if(Math.abs(da-dc)<1e-4) same++; else diff++; if(c) hitN++; }
   return {same,diff,hitN,tNew:+tNew.toFixed(1),tOld:+tOld.toFixed(1),pieces:T.order.length}; });
 console.log(JSON.stringify(r)); console.log(r.diff===0&&r.hitN>50?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

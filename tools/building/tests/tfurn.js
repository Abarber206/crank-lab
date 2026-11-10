const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,chests,TOWNS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.chests&&T.chests.length,null,{timeout:120000}); await sleep(500);
 const r=await pg.evaluate(()=>{ const F=T.props.filter(p=>p.kind==='furn'&&!p.gone); let inF=0, ov=0; const geos=new Set(F.map(p=>p.g.children[0].geometry.uuid));
   T.chests.forEach(c=>{ if(F.some(p=>Math.abs(p.base-c.y)<1&&p.boxes.some(b=>c.x+0.45>b[0]&&c.x-0.45<b[3]&&c.z+0.45>b[2]&&c.z-0.45<b[5]))) inF++; });
   for(let i=0;i<F.length;i++) for(let j=i+1;j<F.length;j++){ const a=F[i], c=F[j]; if(Math.abs(a.base-c.base)>1||Math.abs(a.x-c.x)>4||Math.abs(a.z-c.z)>4) continue; if(a.boxes.some(p=>c.boxes.some(q=>p[0]<q[3]-0.02&&q[0]<p[3]-0.02&&p[2]<q[5]-0.02&&q[2]<p[5]-0.02))) ov++; }
   return {furniture:F.length,looks:geos.size,chestInFurniture:inF,overlapping:ov}; });
 console.log(JSON.stringify(r), r.chestInFurniture===0&&r.overlapping===0&&r.looks>20?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

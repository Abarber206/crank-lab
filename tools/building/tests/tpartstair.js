// no inside wall touches a staircase: every partition's solid boxes stay clear of the stair cells
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,TOWNS,houseStair,partitionFix,housePartition'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS,null,{timeout:120000}); await sleep(500);
 const r=await pg.evaluate(()=>{ let bad=0, parts=0, two=0; T.TOWNS.forEach(t=>t.houses.forEach(h=>{ if(h.floors<2) return; two++; const S=T.houseStair(h);
   for(let l=h.L;l<h.L+h.floors;l++){ const f=T.partitionFix(h,l); if(!f) continue; parts++; f.boxes.forEach(bx=>{ S.cells.forEach(([i,j])=>{ if(bx[3]>i*5-0.05&&bx[0]<(i+1)*5+0.05&&bx[5]>j*5-0.05&&bx[2]<(j+1)*5+0.05) bad++; }); }); } }));
   return {twoStorey:two,partitions:parts,touching:bad}; });
 console.log(JSON.stringify(r), r.touching===0&&r.partitions>0?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

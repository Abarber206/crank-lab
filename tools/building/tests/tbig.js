// every town with a landmark has a strongbox beside it, standing clear of anything solid, and it always pays out well
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,chests,TOWNS,rollBigLoot,WEAPONS,RARITIES,STATICS,terrainH,props'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.chests&&T.chests.length,null,{timeout:120000}); await sleep(3000);
 const r=await pg.evaluate(()=>{ const big=T.chests.filter(c=>c.big), want=T.TOWNS.filter(t=>t.poi).length; let blocked=0, worst=9, low=0, n5=0;
   for(const c of big){ for(const s of T.STATICS){ if(!s.solid) continue; for(const bx of s.solid.boxes){ const dx=Math.max(bx[0]-c.x,0,c.x-bx[3]), dz=Math.max(bx[2]-c.z,0,c.z-bx[5]), d=Math.hypot(dx,dz); if(bx[4]>c.y+0.2&&bx[1]<c.y+1.5){ worst=Math.min(worst,d); if(d<0.9) blocked++; } } }
     for(const p of T.props){ if(p.gone||!p.boxes) continue; if(Math.hypot(p.x-c.x,p.z-c.z)<1.2) blocked++; } }
   for(let q=0;q<300;q++){ const L=T.rollBigLoot(); if(L.length===5) n5++; if(T.RARITIES.indexOf(T.WEAPONS[L[0][0]].rarity)<2) low++; }
   return {big:big.length,want,blocked,worst:+worst.toFixed(2),low,n5,beams:big.filter(c=>c.beam).length}; });
 console.log(JSON.stringify(r), r.big===r.want&&r.big>=8&&r.blocked===0&&r.low===0&&r.n5===300&&r.beams===r.big?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

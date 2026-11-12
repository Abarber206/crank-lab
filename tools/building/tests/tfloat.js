// nothing hangs in the air: every decoration's solid box and every chest out of doors rests on (or a little into) the
// ground at its lowest corner; and the loot odds follow each item's rarity
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,STATICS,DECOR,terrainH,chests,townAt,WEAPONS,lootWeapon,rollChestLoot,karts,TOWNS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.props&&T.props.length>1000&&T.chests.length>50,null,{timeout:180000}); await sleep(2000);
 const r=await pg.evaluate(()=>{ const H=T.terrainH, bad=[]; let n=0;
   for(let i=T.DECOR.s0;i<T.DECOR.s1;i++){ const s=T.STATICS[i]; if(/^(dock|fencerail|log|moored)/.test(s.solid.key)) continue; for(const b of s.solid.boxes){ n++; const cx=(b[0]+b[3])/2, cz=(b[2]+b[5])/2, ix=(b[3]-b[0])*0.2, iz=(b[5]-b[2])*0.2, lo=Math.min(H(cx,cz),H(cx-ix,cz-iz),H(cx+ix,cz-iz),H(cx-ix,cz+iz),H(cx+ix,cz+iz)); // (under the thing itself, not out at the corners of its box)
       if(b[1]-lo>0.12) bad.push(s.solid.key+" "+(b[3]-b[0]).toFixed(1)+"x"+(b[4]-b[1]).toFixed(1)+"x"+(b[5]-b[2]).toFixed(1)+' gap '+(b[1]-lo).toFixed(2)+' at '+b[0].toFixed(0)+','+b[2].toFixed(0)); } }
   let outdoor=0; const cbad=[]; for(const c of T.chests){ if(T.townAt(c.x,c.z,0)) continue; const g=Math.min(H(c.x+0.5,c.z),H(c.x-0.5,c.z),H(c.x,c.z+0.5),H(c.x,c.z-0.5),H(c.x,c.z)); if(Math.abs(c.y-H(c.x,c.z))>3) continue; outdoor++; if(c.y-g>0.1) cbad.push((c.y-g).toFixed(2)); }
   const big=T.chests.filter(c=>c.big).length, boats=T.karts.filter(k=>k.boat).length;
   const f={}, N=40000; for(let i=0;i<N;i++){ const W=T.WEAPONS[T.lootWeapon(1)]; f[W.rarity]=(f[W.rarity]||0)+1; } const per={}; Object.values(T.WEAPONS).forEach(W=>{ if(!W.throw) per[W.rarity]=(per[W.rarity]||0)+1; });
   const each={}; for(const k in f) each[k]=+(100*f[k]/N/per[k]).toFixed(2);
   const ex={}; for(let i=0;i<20000;i++){ const o=T.rollChestLoot(); if(o[2]) { const k=['light','medium','shells','heavy'].includes(o[2][0])?'ammo':o[2][0]; ex[k]=(ex[k]||0)+1; } }
   return {decorBoxes:n,floating:bad.length,sample:bad.slice(0,8),outdoorChests:outdoor,chestGaps:cbad.length,big,boats,rarityPct:Object.fromEntries(Object.entries(f).map(([k,v])=>[k,+(100*v/N).toFixed(1)])),eachItemPct:each,extras:ex}; });
 console.log(JSON.stringify(r,null,1));
 const ord=['common','uncommon','rare','epic','legendary'], e=r.eachItemPct; let mono=true; for(let i=1;i<5;i++) if(!(e[ord[i]]<e[ord[i-1]])) mono=false;
 const ok=r.floating===0&&r.chestGaps===0&&r.big===0&&r.boats<=6&&mono&&r.extras.mini<r.extras.nade&&r.extras.nade<r.extras.bandage;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

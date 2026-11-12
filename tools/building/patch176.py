# patch176: loot by each item's own rarity; no strongbox at the landmarks; fewer motorboats.
#  - Guns: every gun (and every rarity of it) has a weight set by its rarity alone, so a legendary turns up less often
#    than an epic, an epic less than a rare, and so on, however many guns there happen to be in each rarity. Over all
#    guns that comes to about 45% common, 30% uncommon, 17% rare, 6% epic, 2% legendary (chests lean a little rarer).
#  - The extra item in a chest (bandages, ammo, grenades, shield potions) is picked the same way, by its rarity.
#  - The glowing strongbox at the foot of each town's landmark is gone.
#  - Motorboats: one by every third town and two out at sea, instead of one by every town and four at sea.
rep("""const LOOT_RW={common:46,uncommon:30,rare:16,epic:6,legendary:2},""","""const LOOT_RW={common:46,uncommon:30,rare:16,epic:6,legendary:2}, LOOT_IW={common:5,uncommon:3,rare:1.05,epic:0.32,legendary:0.15},""")
i=s.index("function lootWeapon(luck){"); j=s.index("function ammoFor(id)",i)
s=s[:i]+"""function lootWeapon(luck){ // each gun weighted by its own rarity (`luck` above 1 leans the draw toward the rarer ones)
  const L=luck||1, pool=Object.values(WEAPONS).filter(W=>!W.throw&&LOOT_IW[W.rarity]), w=pool.map(W=>LOOT_IW[W.rarity]*Math.pow(L,RARITIES.indexOf(W.rarity)));
  let x=Math.random()*w.reduce((a,b)=>a+b); for(let i=0;i<pool.length;i++){ x-=w[i]; if(x<=0) return pool[i].id; } return pool[pool.length-1].id; }
"""+s[j:]
rep("""  if(r<0.3) out.push(Math.random()<0.6?['bandage',3]:['mini',2]); else if(r<0.5) out.push(['nade',2]); else if(r<0.75){ const k=['light','medium','shells','heavy'][Math.floor(Math.random()*4)]; out.push([k,AMMO_PACK[k]]); }""",
    """  if(r<0.75){ const pool=[['bandage',3],['ammo',0],['nade',2],['mini',2]], w=pool.map(p=>LOOT_IW[p[0]==='ammo'?'common':lootRarity(p[0])]||1); let x=Math.random()*w.reduce((a,b)=>a+b), pick=pool[0];
    for(let i=0;i<pool.length;i++){ x-=w[i]; if(x<=0){ pick=pool[i]; break; } }
    if(pick[0]==='ammo'){ const k=['light','medium','shells','heavy'][Math.floor(Math.random()*4)]; out.push([k,AMMO_PACK[k]]); } else out.push(pick); } // one more thing, by its rarity""")
i=s.index("  // one strongbox at the foot of each town's landmark, on the side facing the town\n"); j=s.index("  // a few in the wild, under trees and on hilltops",i)
s=s[:i]+"  buildLandmarks();\n"+s[j:]
rep("""  for(const t of TOWNS){ const s=tryNear(t.x,t.z,t.R+10,t.R+220); if(s){ spots.push(s); } }
  const S=WGEN.sea&&WGEN.sea(); if(S) for(let n=0;n<4;n++){ const lat=(n-1.5)*220,""","""  TOWNS.forEach((t,k)=>{ if(k%3) return; const s=tryNear(t.x,t.z,t.R+10,t.R+220); if(s){ spots.push(s); } });
  const S=WGEN.sea&&WGEN.sea(); if(S) for(let n=0;n<2;n++){ const lat=(n-0.5)*260,""")
# chests out in the wild sit at the lowest corner of their spot, so none hangs over a slope
rep("""    addChest(x,terrainH(x,z),z,r()*6.28); made++; }""","""    addChest(x,Math.min(terrainH(x,z),terrainH(x+0.55,z),terrainH(x-0.55,z),terrainH(x,z+0.55),terrainH(x,z-0.55))-0.02,z,r()*6.28); made++; }""")

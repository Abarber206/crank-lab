# ---------- 113. the paved ground beside and between roads carries the road's own asphalt (it was a flat grey, so a
# junction looked like a bare patch the road didn't reach) ----------
rep("terrainMat.onBeforeCompile=sh=>{ sh.uniforms.rockMap={value:rockTex};","terrainMat.onBeforeCompile=sh=>{ sh.uniforms.rockMap={value:rockTex}; sh.uniforms.roadMap={value:roadPlainTex};")
rep("sh.fragmentShader='uniform sampler2D rockMap;\\nvarying vec3 vCover;","sh.fragmentShader='uniform sampler2D rockMap;\\nuniform sampler2D roadMap;\\nvarying vec3 vCover;")
rep("    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.255,0.262,0.278),smoothstep(0.5,0.9,vCover.z));","    diffuseColor.rgb=mix(diffuseColor.rgb,texture2D(roadMap,vWP.xz*vec2(0.1389,0.04167)).rgb,smoothstep(0.5,0.9,vCover.z));")
# you drop in with no shield (as with no guns); Buddy too
rep("function emptyLoadout(){ defaultLoadout(); P.inv=[null,null,null,null,null];","function emptyLoadout(){ defaultLoadout(); P.sh=0; P.inv=[null,null,null,null,null];")
rep("AB.wpn=null; AB.loot=null; AB.hp=100; AB.sh=50; AB.down=null;","AB.wpn=null; AB.loot=null; AB.hp=100; AB.sh=0; AB.down=null;")
# what the horde leaves behind: the ordinary ones mostly nothing or ammo, now and then a plain gun, rarely something to heal with;
# a brute always leaves a gun (usually a good one), ammo for it and more, and often a shield potion or bandages
rep("""  if(brute){ out.push(randAmmo()); if(Math.random()<0.75) out.push(randGun()); if(Math.random()<0.35) out.push(['mini',1]); return out; }
  if(r<0.30) out.push(randAmmo());
  else if(r<0.38) out.push(randGun());
  else if(r<0.44) out.push(Math.random()<0.7?['bandage',2]:['mini',1]);
  else if(r<0.48) out.push(['nade',2]);
  return out; // ~52% drop nothing""","""  if(brute){ const id=lootWeapon(2.2); out.push([id,WEAPONS[id].mag],ammoFor(id),randAmmo()); if(Math.random()<0.6) out.push(['mini',2]); if(Math.random()<0.4) out.push(['bandage',3]); if(Math.random()<0.25) out.push(['nade',2]); return out; }
  if(r<0.30) out.push(randAmmo());
  else if(r<0.35){ const id=lootWeapon(0.55); out.push([id,WEAPONS[id].mag]); }
  else if(r<0.38) out.push(Math.random()<0.8?['bandage',2]:['mini',1]);
  else if(r<0.40) out.push(['nade',1]);
  return out; // 60% drop nothing""")

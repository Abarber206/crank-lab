# ---------- 51. monsters are obliterated when killed: a flash, a burst of glowing shards and gore, and they're gone ----------
s=s.replace("burst(z.pos.clone().setY(z.pos.y+1.1*z.sc),10,4,0.09,goreMat); zsfx('zdie',z.pos);","zObliterate(z); zsfx('zdie',z.pos);")
rep("  if(!z.alive){ if(R.lump) R.lump.visible=false; const k=Math.min(1,z.deadT/0.6); g.rotation.x=-k*1.45; g.position.y=z.pos.y-0.1*k; if(z.deadT>1.1) g.scale.setScalar(z.sc*Math.max(0.01,1-(z.deadT-1.1)*2)); return; }",
    "  if(!z.alive){ if(R.lump) R.lump.visible=false; const d=z.deadT; g.scale.setScalar(z.sc*(d<0.06?1+d*3:Math.max(0.001,1.18-(d-0.06)*9))); if(d>0.2) g.visible=false; return; }")
rep("function zombieHurt(z,dmg,by){","""const zFlashes=[]; let zShardMat=null;
function zObliterate(z){ const c=z.pos.clone().setY(z.pos.y+1.1*z.sc), far=c.distanceTo(P.pos)>70;
  if(!zShardMat) zShardMat=new THREE.MeshBasicMaterial({color:0xd06bff});
  burst(c,far?8:22,7.5,0.11,goreMat); burst(c,far?4:14,9,0.06,zShardMat); burst(c.clone().setY(z.pos.y+0.3),far?3:8,3,0.08,goreMat);
  if(far) return; const m=new THREE.Mesh(new THREE.SphereGeometry(0.5,16,10),new THREE.MeshBasicMaterial({color:0xe8a8ff,transparent:true,opacity:0.85,blending:THREE.AdditiveBlending,depthWrite:false}));
  m.position.copy(c); m.scale.setScalar(z.sc*0.6); scene.add(m); zFlashes.push({m,t:0,s:z.sc}); }
function stepZFlash(dt){ for(let i=zFlashes.length-1;i>=0;i--){ const f=zFlashes[i]; f.t+=dt; const k=f.t/0.28; if(k>=1){ scene.remove(f.m); f.m.geometry.dispose(); f.m.material.dispose(); zFlashes.splice(i,1); continue; }
    f.m.scale.setScalar(f.s*(0.6+2.4*Math.sqrt(k))); f.m.material.opacity=0.85*(1-k)*(1-k); } }
function zombieHurt(z,dmg,by){""")
rep("stepShakes(dt); stepLootGlow(dt);","stepShakes(dt); stepLootGlow(dt); stepZFlash(dt);")

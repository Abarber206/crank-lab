# patch133: no depth fighting high in the air. With the near clipping plane at 8 cm the depth buffer can only tell
# surfaces about 15 cm apart at 450 m, so roofs, roads and the ground under them flickered while skydiving and gliding.
# Up there nothing is close to the camera but you, so the near plane moves out (up to 2.5 m, never past 40% of the
# way to your character, and back to 8 cm as you come down): ~25x the depth precision, at no cost.
rep("""  camDist=dist; hero.visible=dist>0.85&&!scopeOn; // through a scope you see what the scope sees""",
"""  camDist=dist; hero.visible=dist>0.85&&!scopeOn; // through a scope you see what the scope sees
  { let nr=0.08; if(P.sky){ const clr=camera.position.y-Math.max(skyGround(P),terrainH(camera.position.x,camera.position.z)); nr=Math.max(0.08,Math.min(camDist*0.4,clr*0.15,2.5)); }
    if(Math.abs(nr-camera.near)>0.004){ camera.near=nr; camera.updateProjectionMatrix(); } } // high up, the near plane moves out for depth precision far away""")

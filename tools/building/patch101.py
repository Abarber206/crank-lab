# ---------- 101. roofs have real thickness (an underside and edges, so a broken roof isn't a paper sheet);
# the build-field ring is gone from the big map ----------
rep("""  tris.forEach(t=>t.forEach(v=>{ pos.push(v[0]-CELL/2,v[2],v[1]-CELL/2); uv.push(v[0]/CELL,v[1]/CELL); }));
  const g=new THREE.BufferGeometry();""","""  tris.forEach(t=>t.forEach(v=>{ pos.push(v[0]-CELL/2,v[2],v[1]-CELL/2); uv.push(v[0]/CELL,v[1]/CELL); }));
  const RT=0.24, put=(v,d)=>{ pos.push(v[0]-CELL/2,d?Math.max(v[2]-d,-0.12):v[2],v[1]-CELL/2); uv.push(v[0]/CELL,v[1]/CELL+(d?0.06:0)); };
  tris.forEach(t=>{ put(t[2],RT); put(t[1],RT); put(t[0],RT); });                       // the underside
  [[k.A,k.B],[k.B,k.C],[k.C,k.D],[k.D,k.A]].forEach(([a,b])=>{ put(a,0); put(b,0); put(b,RT); put(a,0); put(b,RT); put(a,RT); }); // the four cut edges
  const g=new THREE.BufferGeometry();""")
rep("  g.setLineDash([]); g.strokeStyle='rgba(255,236,190,.8)'; g.lineWidth=3; g.beginPath(); g.arc(X(0),X(0),FLAT_R/mpp,0,7); g.stroke(); // the build field\n","  g.setLineDash([]);\n")

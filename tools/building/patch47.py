# ---------- 47. teammates have a name tag over their head (seen through walls, always the same size on screen) ----------
rep("  const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:col,depthTest:false,transparent:true,opacity:.95})); m.renderOrder=20; m.position.y=2.35; pl.h.group.add(m); pl.mark=m;\n}",
"""  const m=new THREE.Mesh(g,new THREE.MeshBasicMaterial({color:col,depthTest:false,transparent:true,opacity:.95})); m.renderOrder=20; m.position.y=2.35; pl.h.group.add(m); pl.mark=m;
  // the name, in a rounded pill in the team colour
  const c=document.createElement('canvas'), x=c.getContext('2d'), nm=(pl.name||'Player').slice(0,16); c.width=256; c.height=64;
  x.font='800 italic 30px "Arial Black", Arial, sans-serif'; const w=Math.min(244,x.measureText(nm).width+28);
  x.fillStyle='rgba(12,18,28,.72)'; x.beginPath(); x.roundRect?x.roundRect(128-w/2,8,w,46,23):x.rect(128-w/2,8,w,46); x.fill();
  x.strokeStyle='#'+col.toString(16).padStart(6,'0'); x.lineWidth=4; x.stroke(); x.fillStyle='#fff'; x.textAlign='center'; x.textBaseline='middle'; x.fillText(nm,128,32);
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(c),depthTest:false,transparent:true,sizeAttenuation:false})); sp.scale.set(0.16,0.04,1); sp.position.y=2.62; sp.renderOrder=21; m.add(sp); sp.position.set(0,0.27,0);
}""")
rep("nm=(pl.name||'Player').slice(0,16); c.width=256;","nm=(pl.name||'Player').slice(0,16); pl.tagName=pl.name; c.width=256;")
rep("  kartFromState(pl,m);\n}","  kartFromState(pl,m);\n  if(pl.mark&&pl.tagName!==pl.name) teamMarker(pl); // the name arrived or changed\n}")

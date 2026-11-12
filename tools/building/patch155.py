# patch155: pickaxes in the Locker preview are held by the handle. The handle only runs about 12 cm past the hand,
# so the shoulder pose now grips each pickaxe just below the end of its own handle (it was holding the air beyond it).
# The Neon Axe's glowing end cap sat 40 cm above the end of its handle; it now caps the handle.
rep("""    part(sph(.025),glow(0x00e5ff),rig.pick,0,.5,0,null,null,0);
  } else if(pk==='crystal'){""","""    part(sph(.025),glow(0x00e5ff),rig.pick,0,.14,0,null,null,0);
  } else if(pk==='crystal'){""")
rep("""  // hammer + blueprint (build mode)
  rig.hammer=grp(rig.armR.hand,0,0,0);""","""  { let top=0.1; rig.pick.updateMatrixWorld(true); const im=new THREE.Matrix4().copy(rig.pick.matrixWorld).invert(), bb=new THREE.Box3();
    rig.pick.traverse(m=>{ if(!m.isMesh||!m.geometry||m.material===inkMat) return; m.geometry.computeBoundingBox(); bb.copy(m.geometry.boundingBox).applyMatrix4(new THREE.Matrix4().multiplyMatrices(im,m.matrixWorld));
      if(Math.abs(bb.min.x+bb.max.x)<0.05&&Math.abs(bb.min.z+bb.max.z)<0.05&&bb.max.y<0.4) top=Math.max(top,bb.max.y); });
    rig.pickTop=top; } // how far the handle runs past the hand
  // hammer + blueprint (build mode)
  rig.hammer=grp(rig.armR.hand,0,0,0);""")
rep("""  r.pick.position.set(0,-PICK_SHOW.grip,0).applyQuaternion(r.pick.quaternion);""","""  r.pick.position.set(0,-Math.min(PICK_SHOW.grip,(r.pickTop||0.12)-0.05),0).applyQuaternion(r.pick.quaternion);""")
rep("""var PICK_SHOW={hand:[0.19,1.13,-0.32],dir:[-0.2,-0.6,-0.75],grip:0.36};""","""var PICK_SHOW={hand:[0.19,1.13,-0.32],dir:[-0.2,-0.6,-0.75],grip:0.14};""")
# the Summit Axe's tooth and the ice scythe's blade were rows of separate blocks stepping apart from each other (they
# looked like pieces floating off the head); each is now one continuous curved blade
rep("""// a flat strap following points on the body""","""// a blade swept along points in the y-z plane: width w (across, x) and a height that runs from h0 at the root to h1 at the tip
function bladeGeo(pts,w,h0,h1){ const C=new THREE.CatmullRomCurve3(pts), n=24, P=[], I=[], X=new THREE.Vector3(1,0,0), T=new THREE.Vector3(), N=new THREE.Vector3();
  for(let i=0;i<=n;i++){ const t=i/n, p=C.getPoint(t); C.getTangent(t,T); N.crossVectors(X,T).normalize(); const h=(h0+(h1-h0)*t)/2, ww=w/2*(1-0.5*t*t);
    for(const [u,v] of [[-1,-1],[1,-1],[1,1],[-1,1]]){ P.push(p.x+u*ww,p.y+N.y*v*h,p.z+N.z*v*h); } }
  for(let i=0;i<n;i++) for(let k=0;k<4;k++){ const a=i*4+k, b=i*4+(k+1)%4; I.push(a,a+4,b, b,a+4,b+4); }
  I.push(0,2,1, 0,3,2); const e=n*4; I.push(e,e+1,e+2, e,e+2,e+3);
  const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(P,3)); g.setIndex(I); g.computeVertexNormals(); return g; }
// a flat strap following points on the body""")
rep("""    for(let q=0;q<5;q++) part(rbox(.016,.035-q*.003,.07,.006),0xc9d2dc,ph,0,.015*q*q-.005,-.06-.06*q,[-.12-q*.17,0,0]);""",
"""    part(bladeGeo([0,1,2,3,4,4.6].map(q=>new THREE.Vector3(0,.015*q*q-.005,-.03-.06*q)),.016,.04,.01),0xc9d2dc,ph); // the tooth, one curved piece""")
rep("""    for(let q=0;q<5;q++){ const a=-.12-q*.2; part(rbox(.02,.07-q*.008,.1,.01),0x9fe3ff,ph,0,.02+.012*q*q,-.07-.085*q,[a,0,0],null,0.005);
      part(rbox(.022,.012,.1,.004),glow(0xeaffff),ph,0,-.012-q*.006+.012*q*q,-.07-.085*q,[a,0,0],null,0); }""",
"""    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,.02+.012*q*q,-.07-.085*q)),.02,.075,.02),0x9fe3ff,ph); // the blade, one curved piece
    part(bladeGeo([-.3,0,1,2,3,4,4.7].map(q=>new THREE.Vector3(0,-.016-q*.006+.012*q*q,-.07-.085*q)),.022,.012,.006),glow(0xeaffff),ph,0,0,0,null,null,0); // its glowing edge""")

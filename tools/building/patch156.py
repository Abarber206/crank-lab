# patch156: the long coat's tails hang open at the front (over the back and sides, both faces drawn) and sit closer to
# the legs, instead of a closed skirt standing off the trousers all the way round.
rep("""    part(bodyLathe([[.176,.0],[.186,-.12],[.198,-.3]],.72),C.jacket,rig.hips,0,.04,0,null,null,0); // tails (open lathe)""",
"""    part(coatTails(),C.jacket,rig.hips,0,.04,0,null,null,0); // tails, open at the front""")
rep("""// a flat strap following points on the body""","""// a long coat's tails: round the back and sides from the waist to mid-thigh, open in front, drawn on both faces
let _coatTails=null;
function coatTails(){ if(_coatTails) return _coatTails; const prof=[[.17,.0],[.178,-.1],[.188,-.2],[.198,-.31]].map(([r,y])=>new THREE.Vector2(r,y));
  const o=new THREE.LatheGeometry(prof,20,-0.78*Math.PI,1.56*Math.PI); o.scale(1,1,.8); o.computeVertexNormals();
  const i=o.clone(); i.scale(0.985,1,0.985); const ix=i.index.array; for(let k=0;k<ix.length;k+=3){ const t=ix[k]; ix[k]=ix[k+1]; ix[k+1]=t; } i.computeVertexNormals();
  return _coatTails=mergeGeos([o,i]); }
// a flat strap following points on the body""")
# the boat's floor follows the inside of the hull (it was a flat 1.5 m wide board that stuck out through the sides
# near the keel and through the bow)
rep("""  return {outer:mk(outer.concat(tr)),inner:mk(inner),top:mk(top),half,sheer,keel,zOf}; }""","""  return {outer:mk(outer.concat(tr)),inner:mk(inner),top:mk(top),half,sheer,keel,zOf,sec}; }""")
rep("""  put('deck',new THREE.BoxGeometry(1.5,0.05,3.7),0,0.06,0.45);""","""  { const Yd=0.085, rows=[]; for(let n=0;n<=40;n++){ const t=0.07+0.93*n/40, S=h.sec(t,0.055).filter(p=>p[0]>=0).sort((a,b)=>a[1]-b[1]); if(S[0][1]>Yd-0.005) continue;
      let w=0; for(let i=0;i<S.length-1;i++){ const a=S[i], b=S[i+1]; if(a[1]<=Yd&&b[1]>=Yd){ w=a[0]+(b[0]-a[0])*(Yd-a[1])/Math.max(1e-6,b[1]-a[1]); break; } }
      if(w>0.02) rows.push([w-0.004,S[0][2]]); }
    const pos=[]; for(let i=0;i<rows.length-1;i++){ const [w0,z0]=rows[i], [w1,z1]=rows[i+1]; pos.push([-w0,Yd,z0],[-w1,Yd,z1],[w0,Yd,z0], [w0,Yd,z0],[-w1,Yd,z1],[w1,Yd,z1]); }
    const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.Float32BufferAttribute(pos.flat(),3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(new Array(pos.length*2).fill(0),2)); g.computeVertexNormals(); (bins.deck||(bins.deck=[])).push(g); } // the floor, as wide as the hull is inside""")
# the dark boot-top line stops where the bow's keel rises above it (forward of that it hung below the hull as a loose black rod)
rep("""      const a=p(t0,y0), b=p(t1,y0), c=p(t0,y1), d=p(t1,y1); if(s>0) pos.push(a,c,b, b,c,d); else pos.push(a,b,c, b,d,c); }""",
"""      if(h.keel(t0)>y0-0.015) continue; const a=p(t0,y0), b=p(t1,y0), c=p(t0,y1), d=p(t1,y1); if(s>0) pos.push(a,c,b, b,c,d); else pos.push(a,b,c, b,d,c); }""")
# the bow: from inside the boat the tip of the hull (forward of where the inner lining starts) was see-through; the hull
# shell now draws on both sides
rep("""hull:kMat('hull',()=>new THREE.MeshPhongMaterial({color:0xf3f1ec,shininess:80,specular:0x6a6a6a})),""","""hull:kMat('hull',()=>new THREE.MeshPhongMaterial({color:0xf3f1ec,shininess:80,specular:0x6a6a6a,side:THREE.DoubleSide})),""")

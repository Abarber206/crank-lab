# ---------- 98. more detailed trees up close: broadleaf trees get a ring of smaller leaf sprays round the canopy, sunlit
# tufts on top, roots spreading at the base, a third limb and knots in the bark; pines get drooping branch tips on every
# tier and bare lower branches. (The far-away versions are unchanged, so the frame rate is too.) ----------
rep("    blobs.forEach(([x,y,z,rr,tone])=>{ if(rr<1&&q()<.25) return; propPart(lumpGeo(rr*s*(0.9+q()*0.2),q),greens[Math.min(3,tone+(q()<.3?1:0))],g,x*s,y*s,z*s,q(),q(),0,0.05); });",
r"""    blobs.forEach(([x,y,z,rr,tone])=>{ if(rr<1&&q()<.25) return; propPart(lumpGeo(rr*s*(0.9+q()*0.2),q),greens[Math.min(3,tone+(q()<.3?1:0))],g,x*s,y*s,z*s,q(),q(),0,0.05); });
    const spray=(rad)=>{ const gg=new THREE.IcosahedronGeometry(rad,1), pa=gg.attributes.position, k1=q()*6; for(let i=0;i<pa.count;i++){ const f=0.9+0.12*Math.sin(pa.getX(i)/rad*5+k1)*Math.cos(pa.getZ(i)/rad*4); pa.setXYZ(i,pa.getX(i)*f,pa.getY(i)*f*0.8,pa.getZ(i)*f); } const na=gg.attributes.normal, v=new THREE.Vector3(); for(let i=0;i<pa.count;i++){ v.set(pa.getX(i),pa.getY(i),pa.getZ(i)).normalize(); na.setXYZ(i,v.x,v.y,v.z); } return gg; }; // soft, round shading like the big clusters
    for(let k=0;k<13;k++){ const a=k/13*6.283+q()*0.5, rr=1.75+q()*0.55, y=3.45+q()*2.1, up=(y-3.45)/2.1; propPart(spray((0.42+q()*0.3)*s),greens[Math.min(3,1+Math.round(up*2)+(q()<.3?1:0))],g,Math.cos(a)*rr*(1-up*0.45)*s,y*s,Math.sin(a)*rr*(1-up*0.45)*s,q()*3,q()*3,0,0); }
    for(let k=0;k<4;k++){ const a=q()*6.283, rr=q()*0.9; propPart(spray((0.3+q()*0.2)*s),0x7cc95a,g,Math.cos(a)*rr*s,(5.75+q()*0.5)*s,Math.sin(a)*rr*s,q()*3,q()*3,0,0); } // sunlit tufts on top
    for(let k=0;k<4;k++){ const a=k*1.57+q()*0.9; propPart(new THREE.ConeGeometry(.15*s,1.0*s,6).rotateZ(-Math.PI/2).translate(.42*s,0,0),0x6c4829,g,0,.16*s,0,0,a,-0.18,0); } // roots
    propPart(limbGeo(.1*s,.14*s,1.05*s),0x77502f,g,.05*s,2.95*s,-.4*s,-0.95,0,0);
    for(let k=0;k<3;k++){ const a=q()*6.283, y=0.8+q()*1.7; propPart(new THREE.SphereGeometry(.09*s,6,5),0x5a3c22,g,Math.cos(a)*.33*s,y*s,Math.sin(a)*.33*s,0,0,0,0).scale.set(1,1.5,0.6); }""")
rep("      propPart(cg,c,g,0,y*s,0,0,ti*.5+q(),0,0.05); });",
r"""      propPart(cg,c,g,0,y*s,0,0,ti*.5+q(),0,0.05);
      const nt=ti<4?6:4, dc=new THREE.Color(c).multiplyScalar(0.82).getHex(); for(let k=0;k<nt;k++){ const a=k/nt*6.283+q()*0.6+ti; propPart(new THREE.ConeGeometry(.2*s*(1-ti*0.08),.8*s,5).rotateZ(-1.95).translate(.25*s,0,0),dc,g,Math.cos(a)*rr*0.86*s,(y-h*0.62)*s,Math.sin(a)*rr*0.86*s,0,-a,0,0); } }); // drooping tips
    for(let k=0;k<3;k++){ const a=q()*6.283; propPart(limbGeo(.035*s,.05*s,.75*s),0x4f3520,g,Math.cos(a)*.2*s,(1.2+k*0.35)*s,Math.sin(a)*.2*s,Math.sin(a)*-1.25,0,Math.cos(a)*-1.25,0); } // bare lower branches""")

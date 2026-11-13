# patch191: river banks blend into the grass: a band of wet earth at the waterline (under the shallows too), patches of
# sand and gravel, grass blades thinning out over a few metres instead of stopping at a line, and the grass darker and
# lusher where the ground is damp
rep("""    if(dd<hw+1.5) GRASS[c]=0; const sd=Math.round(215*(1-sstep(hw*0.55,hw+1.8,dd))); if(sd>SAND[c]) SAND[c]=sd; if(dd<hw) ROCK[c]=Math.round(ROCK[c]*0.3); } }""",
"""    { const i_=c%WN, j_=(c-i_)/WN, n_=0.5*Math.sin(i_*0.37+Math.sin(j_*0.21)*2.1)+0.5*Math.sin(j_*0.29-i_*0.13); // (-1..1: patchy, not a ribbon)
      const gv=Math.round(255*sstep(hw+1.6,hw+6+1.6*n_,dd)); if(gv<GRASS[c]) GRASS[c]=gv;
      const mud=Math.round(175*(1-sstep(hw+0.8,hw+3.0+1.2*n_,dd))*(dd>hw-0.9?1:0.45)); if(mud>WORLD.TRACK[c]) WORLD.TRACK[c]=mud;
      const sd=Math.round(185*(1-sstep(hw*0.3,hw+1.6+2.4*Math.max(0,n_),dd))*(0.5+0.5*Math.max(0,n_))); if(sd>SAND[c]) SAND[c]=sd; }
    if(dd<hw) ROCK[c]=Math.round(ROCK[c]*0.3); } }""")
rep("""function terrainTint(x,z,h,ny){ const patch=0.5+0.5*Math.sin(x*0.05+Math.sin(z*0.033)*2)*Math.cos(z*0.041-x*0.017);
  return _tc.setRGB(.92,.92,.9)""","""const T_DAMP=new THREE.Color(0.66,0.84,0.6);
function terrainTint(x,z,h,ny){ const patch=0.5+0.5*Math.sin(x*0.05+Math.sin(z*0.033)*2)*Math.cos(z*0.041-x*0.017);
  let damp=0; if(WORLD.RVD){ const c=worldCell(x,z); if(c>=0&&WORLD.RVD[c]<1e4) damp=1-sstep(WORLD.RVW[c]+0.5,WORLD.RVW[c]+7+3*patch,WORLD.RVD[c]); } // damp ground by the water: darker, lusher
  return _tc.setRGB(.92,.92,.9).lerp(T_DAMP,damp*0.75)""")

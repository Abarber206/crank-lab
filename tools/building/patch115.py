# ---------- 115. from a distance the ground still dips where a river or the shore is (the coarse far-off ground used to
# bury the water in places, or leave it lying on the grass) ----------
rep("    if(st>1&&WRD[q]<12+2*st*WHS){ for(let jj=Math.max(0,j-st);jj<=Math.min(WN-1,j+st);jj++)","    if(st>1&&(WRD[q]<12+2*st*WHS||WORLD.RVD[q]<1e4||WORLD.WS[q]>-999)){ for(let jj=Math.max(0,j-st);jj<=Math.min(WN-1,j+st);jj++)")

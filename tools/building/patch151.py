# patch151: where a river runs out into the sea, cutting its channel no longer builds the sea floor up: the bed and
# banks only ever lower the ground there, so no ridges or shoals stick up along the river mouths (which grounded
# boats and felt like an invisible wall).
rep("""    if(dd<=hw){ const a=dd/hw; h=ys-RVP[c]*(1-a*a); }
    else { const t=(dd-hw)/RVB[c]; if(t>=1) continue; const lip=ys+0.3*Math.min(1,(dd-hw)/1.2); h=lip+(h0-lip)*t*t*(3-2*t); }""",
"""    if(dd<=hw){ const a=dd/hw; h=ys-RVP[c]*(1-a*a); }
    else { const t=(dd-hw)/RVB[c]; if(t>=1) continue; const lip=ys+0.3*Math.min(1,(dd-hw)/1.2); h=lip+(h0-lip)*t*t*(3-2*t); }
    if(h0<_rvSeaY+0.6||dd<=hw) h=Math.min(h,h0); // (never raised: not under the river, and not on the sea floor)""")
rep("""{ const {RVD,RVY,RVW,RVB,RVP,WS,SAND,GRASS,ROCK}=WORLD, NN=WN*WN;""","""{ const {RVD,RVY,RVW,RVB,RVP,WS,SAND,GRASS,ROCK}=WORLD, NN=WN*WN, _rvS=WGEN.sea(), _rvSeaY=_rvS?_rvS.Y:-1e4;""")

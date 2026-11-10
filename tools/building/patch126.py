# ---------- 126. reloads you can see: the magazine comes out of the gun in the off hand, goes to the pouch, and a fresh one
# comes back and is seated; shotguns are fed a shell at a time from the fingers ----------
rep("      if(r.arMag) r.arMag.visible=!(mdl==='ar'&&p>0.3&&p<0.62);\n    } else if(r.arMag) r.arMag.visible=true;",
    "      { const mg=mdl==='ar'?r.arMag:r['magG_'+mdl], sh=!!(GW&&GW.shell); if(mg) mg.visible=sh||!(p>0.25&&p<0.8); // out with the hand at a quarter, the new one home at four fifths\n        if(r.heldMag) r.heldMag.visible=!!mg&&!sh&&((p>0.25&&p<0.5)||(p>0.58&&p<0.8)); if(r.heldShell) r.heldShell.visible=sh&&p>0.5&&p<0.97; }\n    } else magBack(r,mdl);")
rep("    ikArm(r.armL,tgt,_pole,_hq2);\n  } else if(r.arMag) r.arMag.visible=true;","    ikArm(r.armL,tgt,_pole,_hq2);\n  } else magBack(r,null);")
rep("function ikArm(arm,targetW,poleW,handQ){","function magBack(r,mdl){ const mg=mdl==='ar'?r.arMag:mdl?r['magG_'+mdl]:null; if(mg) mg.visible=true; if(r.arMag) r.arMag.visible=true; if(r.heldMag) r.heldMag.visible=false; if(r.heldShell) r.heldShell.visible=false; }\nfunction ikArm(arm,targetW,poleW,handQ){")
# the off hand closes round the magazine or shell while it is away from the fore-end
rep("const und=sp===undefined||sp===3, nL=A_.handL||(held?(sp===0?'relax':sp===3?'fist':sp?'wrap':'cradle'):two?'fist':S.editing?'flat':'relax'); set(r.armL,nL,held?(und?0.6:sp?-0.97:0):rest(nL,r.armL,A_.turnL),held&&und?1.35:0);",
    "const und=sp===undefined||sp===3, rlp=held&&S.reload?S.reload.p:-1, busy=rlp>0.12&&rlp<0.9, nL=A_.handL||(held?(busy?'fist':sp===0?'relax':sp===3?'fist':sp?'wrap':'cradle'):two?'fist':S.editing?'flat':'relax'); set(r.armL,nL,held?(busy?0:und?0.6:sp?-0.97:0):rest(nL,r.armL,A_.turnL),held&&und&&!busy?1.35:0);")

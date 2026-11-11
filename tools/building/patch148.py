# patch148: smoother swimming. Going into and out of the water no longer flickers between walking and swimming (the
# swim pose comes in over a third of a second and goes out the same way, and wading in and out at the edge of deep water
# doesn't flip it back and forth); treading water, the arms scull low in front of the chest under the water instead
# of being held up and out like a surrender; and the limbs ease between treading and the stroke instead of snapping.
rep("""  S.swimW=!S.seat&&!S.sky&&S.pos&&!H.anim.dead?swimSurface(S.pos):null;""",
"""  { const A=H.anim, raw=!S.seat&&!S.sky&&S.pos&&!A.dead?swimSurface(S.pos):null;
    if(raw!==null){ A.swIn=(A.swIn||0)+dt; A.swOut=0; A.swLast=raw; } else { A.swOut=(A.swOut||0)+dt; A.swIn=0; }
    S.swimRaw=raw!==null; S.swimW=raw!==null&&((A.swimT||0)>0||A.swIn>0.12)?raw:(raw===null&&(A.swimT||0)>0&&!S.seat&&!S.sky&&!A.dead?A.swLast:null); }""")
rep("""  if(S.swimW!=null){ A.swimT=Math.min(1,(A.swimT||0)+dt*3); A.downT=0; const e=A.swimT*A.swimT*(3-2*A.swimT), set=(o,ax,v)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,sm); }, W=S.swimW;""",
"""  if(S.swimW!=null){ A.swimT=S.swimRaw?Math.min(1,(A.swimT||0)+dt*3):Math.max(0,(A.swimT||0)-dt*3); A.downT=0; const e=A.swimT*A.swimT*(3-2*A.swimT), smS=1-Math.exp(-dt*9), set=(o,ax,v)=>{ o.rotation[ax]=lerp(o.rotation[ax],v,smS); }, W=S.swimW;""")
rep("""    for(const [a,sx] of [[r.armL,-1],[r.armR,1]]){ set(a.sh,'x',lerp(0.45+0.08*sc,1.75+1.15*reach,mvK)); set(a.sh,'z',sx*lerp(1.05+0.18*sc,0.22+0.95*out,mvK)); set(a.sh,'y',sx*lerp(0.25*sc,-0.2*out,mvK));
      set(a.el,'x',lerp(0.55,0.2+1.35*(1-reach),mvK)); set(a.wr,'x',lerp(0.1,0.25,mvK)); }""",
"""    for(const [a,sx] of [[r.armL,-1],[r.armR,1]]){ set(a.sh,'x',lerp(0.78+0.06*sc,1.75+1.15*reach,mvK)); set(a.sh,'z',sx*lerp(0.42+0.16*sc,0.22+0.95*out,mvK)); set(a.sh,'y',sx*lerp(0.35*sc,-0.2*out,mvK));
      set(a.el,'x',lerp(1.0-0.12*sc,0.2+1.35*(1-reach),mvK)); set(a.wr,'x',lerp(0.15,0.25,mvK)); set(a.wr,'z',sx*lerp(0.45*sc,0,mvK)); }""")
# the off hand takes the pickaxe handle over a fifth of a second (after swimming, an emote, building...) instead of
# snapping onto it in one frame
rep("""else if(S.showPick) showPickPose(H,S); else pickTwoHands(H,S);""","""else if(S.showPick) showPickPose(H,S); else pickTwoHands(H,S,dt);""")
rep("""function pickTwoHands(H,S){ const r=H.rig; if(!r.pick) return;""","""const _pgq=[new THREE.Quaternion(),new THREE.Quaternion(),new THREE.Quaternion()];
function pickTwoHands(H,S,dt){ const r=H.rig, A=H.anim; if(!r.pick) return; const was=A.gripW||0; A.gripW=0;""")
rep("""  ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; } // the wrist sits back from the handle so the fist closes on it""",
"""  const L=r.armL, w=A.gripW=Math.min(1,was+(dt||0.016)*5.5); if(w<1){ _pgq[0].copy(L.sh.quaternion); _pgq[1].copy(L.el.quaternion); _pgq[2].copy(L.wr.quaternion); }
  ikArm(L,t,pole,_p2q); L.fing.rotation.x=1.25; // the wrist sits back from the handle so the fist closes on it
  if(w<1){ const e=w*w*(3-2*w); L.sh.quaternion.copy(_pgq[0].slerp(L.sh.quaternion,e)); L.el.quaternion.copy(_pgq[1].slerp(L.el.quaternion,e)); L.wr.quaternion.copy(_pgq[2].slerp(L.wr.quaternion,e)); } }""")
# coming out of the water: the stroke settles to treading as you stand up, and the walk takes over gently for a moment
rep("""  const sm=1-Math.exp(-dt*18), smF=1-Math.exp(-dt*30);""","""  const sm=1-Math.exp(-dt*((A.swEx||0)>0?7:18)), smF=1-Math.exp(-dt*30);""")
rep("""const mvK=A.swimMv=lerp(A.swimMv||0,Math.min(1,sp/(S.down?0.8:1.6)),Math.min(1,dt*4))""","""if(!S.swimRaw) A.swEx=0.5; const mvK=A.swimMv=lerp(A.swimMv||0,S.swimRaw?Math.min(1,sp/(S.down?0.8:1.6)):0,Math.min(1,dt*(S.swimRaw?4:9)))""")
rep("""  A.swimT=0;
""","""  A.swimT=0; if(A.swEx>0) A.swEx=Math.max(0,A.swEx-dt);
""")

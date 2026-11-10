# ---------- 95. the pickaxe sits in a closed fist: the hand turns so the palm faces in and the fingers wrap the handle
# (it used to pass through a flat, forward-facing hand) ----------
rep("function pickTwoHands(H,S){ const r=H.rig; if(!r.pick||!r.pick.visible||S.gun||S.building||S.editing||(S.emote&&EMOTES[S.emote.id])||S.sky||S.down||S.item) return;",
"""const _pkY=new THREE.Vector3(0,1,0);
function pickTwoHands(H,S){ const r=H.rig; if(!r.pick) return;
  if(!r.pickQ0){ r.pickQ0=r.pick.quaternion.clone(); r.pickQ1=new THREE.Quaternion().setFromAxisAngle(_pkY,-Math.PI/2).multiply(r.pickQ0); }
  const grip=r.pick.visible&&!S.gun&&!S.building&&!S.editing&&!(S.emote&&EMOTES[S.emote.id])&&!S.sky&&!S.down&&!S.item;
  r.pick.quaternion.copy(grip?r.pickQ1:r.pickQ0); if(!grip) return;
  r.armR.wr.rotation.y=Math.PI/2; r.armR.fing.rotation.x=1.25;""")
rep("r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=0.95; }","r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; }")

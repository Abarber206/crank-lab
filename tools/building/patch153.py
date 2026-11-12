# patch153: showing off a pickaxe in the Locker or the Item Shop, the hero rests it over the right shoulder (held low
# on the handle in front of the chest, the head of it behind the shoulder) instead of letting it hang down to the floor.
rep("""function showPickPose(H,S){ const r=H.rig; if(!r.pick) return; r.pick.visible=true; H.group.updateMatrixWorld(true);
  const tgt=bodyPt(H,0.27,0.9,-0.12,_slB), pole=bodyPt(H,0.6,0.7,0.2,_slF);
  const hf=bodyDir(H,0,-1,-0.3,_slU), hu=bodyDir(H,0,0,-1,_slA);
  handQuat(_slW,hf,hu); ikArm(r.armR,tgt,pole,_slW); r.armR.fing.rotation.x=1.25;
  // the pick itself: the handle angled down and forward from the hand
  r.armR.hand.updateMatrixWorld(true); const hy=bodyDir(H,-0.12,0.62,0.78,_slA), hx=bodyDir(H,1,0,0,_slU.clone()); hx.addScaledVector(hy,-hx.dot(hy)).normalize(); const hz=_slF.crossVectors(hx,hy).normalize();
  _slM.makeBasis(hx,hy,hz); _slQ.setFromRotationMatrix(_slM); r.armR.hand.getWorldQuaternion(_slQ2); r.pick.quaternion.copy(_slQ2.invert().multiply(_slQ));""",
"""var PICK_SHOW={hand:[0.19,1.13,-0.32],dir:[-0.2,-0.6,-0.75],grip:0.36}; // the hand in front of the chest; the handle's way down from the shoulder; how far up the handle the hand holds it
function showPickPose(H,S){ const r=H.rig; if(!r.pick) return; r.pick.visible=true; H.group.updateMatrixWorld(true);
  const tgt=bodyPt(H,PICK_SHOW.hand[0],PICK_SHOW.hand[1],PICK_SHOW.hand[2],_slB), pole=bodyPt(H,0.65,0.85,0.3,_slF);
  const hf=bodyDir(H,-0.35,-0.25,-1,_slU), hu=bodyDir(H,0,1,-0.2,_slA);
  handQuat(_slW,hf,hu); ikArm(r.armR,tgt,pole,_slW); r.armR.fing.rotation.x=1.25;
  // the pick itself: the handle runs up from the fist and back over the shoulder, the head resting behind it
  r.armR.hand.updateMatrixWorld(true); const hy=bodyDir(H,PICK_SHOW.dir[0],PICK_SHOW.dir[1],PICK_SHOW.dir[2],_slA), hx=bodyDir(H,1,0,0,_slU.clone()); hx.addScaledVector(hy,-hx.dot(hy)).normalize(); const hz=_slF.crossVectors(hx,hy).normalize();
  _slM.makeBasis(hx,hy,hz); _slQ.setFromRotationMatrix(_slM); r.armR.hand.getWorldQuaternion(_slQ2); r.pick.quaternion.copy(_slQ2.invert().multiply(_slQ));
  r.pick.position.set(0,-PICK_SHOW.grip,0).applyQuaternion(r.pick.quaternion);""")
rep("""else if(S.showPick) showPickPose(H,S); else pickTwoHands(H,S,dt);""","""else if(S.showPick) showPickPose(H,S); else pickTwoHands(H,S,dt); if(!S.showPick&&H.rig.pick&&H.rig.pick.position.lengthSq()>0) H.rig.pick.position.set(0,0,0);""")

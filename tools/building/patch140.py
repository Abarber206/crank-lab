# patch140: locker poses. The salute puts the flat hand at the right brow (placed by reaching for it, so it never goes
# into the head on any outfit), the other arm hangs clear of the hip; the groove's arms swing in front of the body
# instead of through it; and a pickaxe picked in the Locker is shown held low at the side, instead of held up in front
# of the face.
rep("""  footRestore(H); animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); poseHands(H,S,dt); footPlant(H,S); }""",
"""  footRestore(H); animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else if(S.showPick) showPickPose(H,S); else pickTwoHands(H,S); if(S.emote&&S.emote.id==='salute'&&EMOTES.salute) saluteHand(H,S); poseHands(H,S,dt); footPlant(H,S); }
const _slA=new THREE.Vector3(), _slB=new THREE.Vector3(), _slQ=new THREE.Quaternion(), _slQ2=new THREE.Quaternion(), _slQ3=new THREE.Quaternion(), _slF=new THREE.Vector3(), _slU=new THREE.Vector3(), _slS=new THREE.Quaternion(), _slW=new THREE.Quaternion(), _slM=new THREE.Matrix4();
// a point in the body's own frame (x right, y up, z back), from its group
const bodyPt=(H,x,y,z,out)=>out.set(x,y,z).applyQuaternion(H.group.quaternion).add(H.group.position);
const bodyDir=(H,x,y,z,out)=>out.set(x,y,z).applyQuaternion(H.group.quaternion).normalize();
function saluteHand(H,S){ const r=H.rig, E=EMOTES.salute, t=S.emote.t, cl=x=>Math.max(0,Math.min(1,x)), ez=x=>x*x*(3-2*x), up=ez(cl(t*4))*ez(cl((E.dur-t)*5)); if(up<0.01) return;
  H.group.updateMatrixWorld(true); r.head.getWorldPosition(_slA); const hq=r.head.getWorldQuaternion(_slQ3);
  const tgt=_slB.set(0.17,0.12,-0.05).applyQuaternion(hq).add(_slA);           // the wrist, out beside the right brow
  const pole=bodyPt(H,0.75,1.25,-0.35,_slF);                                                                           // the elbow out to the side
  const fwd=_slU.set(-0.8,0.35,-0.3).applyQuaternion(hq).normalize(), upv=bodyDir(H,0,0.2,-1,_slA.clone());
  handQuat(_slW,fwd,upv); const s0=r.armR.sh.quaternion.clone(), e0=r.armR.el.quaternion.clone(), w0=r.armR.wr.quaternion.clone();
  ikArm(r.armR,tgt,pole,_slW); if(up<0.999){ r.armR.sh.quaternion.copy(s0.slerp(r.armR.sh.quaternion,up)); r.armR.el.quaternion.copy(e0.slerp(r.armR.el.quaternion,up)); r.armR.wr.quaternion.copy(w0.slerp(r.armR.wr.quaternion,up)); } }
// the Locker's pickaxe preview: held low at the side, the head forward by the shins
function showPickPose(H,S){ const r=H.rig; if(!r.pick) return; r.pick.visible=true; H.group.updateMatrixWorld(true);
  const tgt=bodyPt(H,0.27,0.9,-0.12,_slB), pole=bodyPt(H,0.6,0.7,0.2,_slF);
  const hf=bodyDir(H,0,-1,-0.3,_slU), hu=bodyDir(H,0,0,-1,_slA);
  handQuat(_slW,hf,hu); ikArm(r.armR,tgt,pole,_slW); r.armR.fing.rotation.x=1.25;
  // the pick itself: the handle angled down and forward from the hand
  r.armR.hand.updateMatrixWorld(true); const hy=bodyDir(H,-0.12,0.62,0.78,_slA), hx=bodyDir(H,1,0,0,_slU.clone()); hx.addScaledVector(hy,-hx.dot(hy)).normalize(); const hz=_slF.crossVectors(hx,hy).normalize();
  _slM.makeBasis(hx,hy,hz); _slQ.setFromRotationMatrix(_slM); r.armR.hand.getWorldQuaternion(_slQ2); r.pick.quaternion.copy(_slQ2.invert().multiply(_slQ));
  r.armL.sh.rotation.set(0.05,0,-0.12); r.armL.el.rotation.set(0.15,0,0); }""")
# the stage: show the pickaxe that way while previewing it
rep("const st={bare:!(i===0&&(window._stagePickT||0)>now),","const st={showPick:i===0&&(window._stagePickT||0)>now,bare:!(i===0&&(window._stagePickT||0)>now),")
# the salute's other arm clear of the hip
rep("T.shL=lerp(T.shL,0,up); T.shLz=lerp(T.shLz,-0.04,up); T.elL=lerp(T.elL,0.06,up);","T.shL=lerp(T.shL,0.02,up); T.shLz=lerp(T.shLz,-0.14,up); T.elL=lerp(T.elL,0.1,up);")
# the groove: the arms swing in front of the body, not into it
rep("shL:0.35+0.45*W,shR:0.35-0.45*W,shLz:-0.28,shRz:0.28,shLy:-0.35,shRy:0.35,elL:1.3+0.3*dip,elR:1.3+0.3*dip}","shL:0.55+0.38*W,shR:0.55-0.38*W,shLz:-0.36,shRz:0.36,shLy:-0.2,shRy:0.2,elL:1.1+0.25*dip,elR:1.1+0.25*dip}")

# ---------- 78. the pickaxe is held two-handed: the left hand grips the handle just below the right, carrying and swinging ----------
rep("  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); }","  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); }")
rep("function handQuat(out,fwd,up){",r"""const _p2a=new THREE.Vector3(), _p2b=new THREE.Vector3(), _p2q=new THREE.Quaternion();
function pickTwoHands(H,S){ const r=H.rig; if(!r.pick||!r.pick.visible||S.gun||S.building||S.editing||(S.emote&&EMOTES[S.emote.id])||S.sky||S.down||S.item) return;
  H.group.updateMatrixWorld(true); const t=r.pick.localToWorld(_p2a.set(0,0.11,0)), pole=H.group.localToWorld(_p2b.set(-0.7,0.6,0.3));
  r.armR.wr.getWorldQuaternion(_p2q); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=0.95; }
function handQuat(out,fwd,up){""")

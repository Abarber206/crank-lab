# tools sit in a closed fist: the hand turns so its knuckles run along the handle, the off hand takes the other side, and the shovel's D-grip is joined on
rep("""  set(r.armR,nR,held?Math.PI/2:rest(nR,r.armR,A_.turnR),0);""",
    """  const tg=tool&&!A_.handR&&!S.editing, hm=tg&&r.hammer&&r.hammer.visible, TA=hm?HAMMER_AT:TOOL_AT; set(r.armR,tg?'tool':nR,held||hm?Math.PI/2:tg?0:rest(nR,r.armR,A_.turnR),hm?-Math.PI/2:tg?TOOL_ROLL:0);""")
rep("""two?'fist':S.editing?'flat':'relax'); set(r.armL,nL,held?(busy?0:und?0.6:sp?-0.97:0):rest(nL,r.armL,A_.turnL),held&&und&&!busy?1.35:0);""",
    """two?'tool':S.editing?'flat':'relax'); set(r.armL,nL,held?(busy?0:und?0.6:sp?-0.97:0):two?Math.PI:rest(nL,r.armL,A_.turnL),held&&und&&!busy?1.35:two?-TOOL_ROLL:0);""")
rep("""mx=held?-.032+gh[0]:0, my=held?-.092+gh[1]:-.098, mz=held?-.06+gh[2]:-.032;""",
    """mx=held?-.032+gh[0]:tg?TA[0]:0, my=held?-.092+gh[1]:tg?TA[1]:-.098, mz=held?-.06+gh[2]:tg?TA[2]:-.032;""")
rep("""const _gv1=new THREE.Vector3(), _gv2=new THREE.Vector3(), _gv3=new THREE.Vector3();""",
    """const _gv1=new THREE.Vector3(), _gv2=new THREE.Vector3(), _gv3=new THREE.Vector3();
const TOOL_ROLL=-0.62, TOOL_AT=[-.049,-.069,-.037], HAMMER_AT=[-.037,0,.085]; // a tool handle lies across the palm, tipped the way the pickaxe sits in the hand""")
rep("""  H.group.updateMatrixWorld(true); const t=r.pick.localToWorld(_p2a.set(0,0.11,0)), pole=H.group.localToWorld(_p2b.set(-0.7,0.6,0.3));
  if(S.bare) return; r.armR.wr.getWorldQuaternion(_p2q); t.sub(_p2c.set(0,-.098,-.032).applyQuaternion(_p2q)); ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; }""",
"""  H.group.updateMatrixWorld(true); if(S.bare) return; r.armR.wr.getWorldQuaternion(_p2q); const pole=H.group.localToWorld(_p2b.set(-0.7,0.6,0.3)), shW=r.armL.sh.getWorldPosition(_p2d), reach=(r.armL.a+r.armL.b)*0.985;
  // the off hand takes the handle below the firing hand, or above it when that is the only place it can reach; out of reach altogether, it lets go
  const at=sd=>r.pick.localToWorld(_p2a.set(0,sd>0?0.105:-0.125,0)).sub(_p2c.set(TOOL_AT[0],TOOL_AT[1],-TOOL_AT[2]).applyQuaternion(_p2q));
  let sd=r.pickSd||1, t=at(sd); if(t.distanceTo(shW)>reach){ const o=at(-sd); if(o.distanceTo(shW)<=reach){ sd=-sd; t=o; } else { t=at(sd); if(t.distanceTo(shW)>reach+0.05) return; } } r.pickSd=sd;
  ikArm(r.armL,t,pole,_p2q); r.armL.fing.rotation.x=1.25; }""")
rep("""const _pkY=new THREE.Vector3(0,1,0), _p2c=new THREE.Vector3();""","""const _pkY=new THREE.Vector3(0,1,0), _p2c=new THREE.Vector3(), _p2d=new THREE.Vector3();""")
# the D-grip: a fork off the end of the shaft carrying a cross bar
rep("""    part(new THREE.TorusGeometry(.045,.01,8,16,Math.PI),0x2a2f38,rig.pick,0,.17,0,[0,Math.PI/2,0],null,0); part(limbGeo(.01,.01,.09),0x2a2f38,rig.pick,0,.17,0,[0,0,Math.PI/2],null,0);
    part(limbGeo(.02,.022,.66),0xb98a52,rig.pick,0,.13,0,null,null,0.006);""",
    """    part(new THREE.TorusGeometry(.045,.011,8,16,Math.PI),0x2a2f38,rig.pick,0,.215,0,[Math.PI,Math.PI/2,0],null,0); part(limbGeo(.012,.012,.112),0x2a2f38,rig.pick,0,.215,.056,[Math.PI/2,0,0],null,0);
    part(limbGeo(.02,.022,.7),0xb98a52,rig.pick,0,.17,0,null,null,0.006); part(limbGeo(.024,.024,.03),0x2a2f38,rig.pick,0,.185,0,null,null,0);""")
rep("""const HAND_POSE={relax:""","""const HAND_POSE={tool:[[1.12,1.25,.6],[1.15,1.28,.62],[.75,.3,.4,.45]],relax:""")

# ---------- 49. buggy suspension: it rides on springs (not glued to the ground), flies off crests and jumps, lands with a squash;
#               the driver's hands hold the steering wheel ----------
a=s.index("  if(k.air){ k.vy-=GRAV*dt; k.y+=k.vy*dt; k.pitch+=(Math.max(-0.4,Math.min(0.35,k.vy*0.025))"); b=s.index("  // body sway: squat under power, dive under braking")
s=s[:a]+r"""  { // springs: the body is pushed up toward its ride height over the ground under the wheels, damped; it keeps its own
    // vertical speed, so over a crest or off a ramp it carries on up and flies
    const REST=GRAV/340, comp=gC+REST-k.y, wasAir=k.air;
    if(comp>-0.14){ k.vy+=(340*comp-20*k.vy)*dt; if(wasAir&&k.vy<-3.5){ sfxAt('kart_land',_kz.set(k.x,k.y,k.z)); k.sqV-=Math.min(3,-k.vy*0.25); if(P.kart&&P.kart.k===k){ shake=Math.max(shake,Math.min(0.3,-k.vy*0.025)); camDip=Math.min(camDip,-0.12); } } }
    k.vy-=GRAV*dt; k.y+=k.vy*dt;
    if(k.y<gC-0.18){ k.y=gC-0.18; if(k.vy<0) k.vy=0; } // bottomed out
    k.air=comp<-0.14;
    const pt=Math.atan2((w[0]+w[1]-w[2]-w[3])/2,KWB), rt=Math.atan2((w[1]+w[3]-w[0]-w[2])/2,KTRACK);
    k.pv=k.pv||0; k.rv=k.rv||0;
    if(!k.air){ k.pv+=(90*(pt-k.pitch)-11*k.pv)*dt; k.rv+=(90*(rt-k.roll)-11*k.rv)*dt; }
    else { k.pv+=(-1.2*k.pitch-0.8*k.pv)*dt+(inp.fw>0.1?-0.6:inp.fw<-0.1?0.6:0)*dt; k.rv*=Math.exp(-dt*1.5); } // in the air: throttle tips the nose down, brake lifts it
    k.pitch+=k.pv*dt; k.roll+=k.rv*dt; }
"""+s[b:]
# hands on the wheel: after the rider is placed, reach both hands to the rim (they turn with it)
rep("  r.pick.visible=false; if(!S.seat.gunP){ r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; for(const m of GUN_MODELS) if(r[m]) r[m].visible=false; } }",
"""  r.pick.visible=false; if(!S.seat.gunP){ r.gun.visible=r.pump.visible=r.hammer.visible=r.plan.visible=false; for(const m of GUN_MODELS) if(r[m]) r[m].visible=false; }
  if(S.seat.s===0&&!S.seat.gunP){ G.updateMatrixWorld(true); k.sw.getWorldPosition(_kc); const ax=_kr.set(1,0,0).applyQuaternion(k.sw.getWorldQuaternion(_kq)), ay=_ku2.set(0,1,0).applyQuaternion(_kq), nz=_kn.set(0,0,1).applyQuaternion(_kq);
    for(const [arm,sd] of [[r.armL,-1],[r.armR,1]]){ const t=_kt.copy(_kc).addScaledVector(ax,sd*0.15).addScaledVector(ay,0.02), pole=_kp.copy(t).addScaledVector(ay,-0.6).addScaledVector(ax,sd*0.5);
      handQuat(_khq,_kf.copy(nz).negate().addScaledVector(ay,0.6).normalize(),ay); ikArm(arm,t,pole,_khq); } } }
const _kc=new THREE.Vector3(), _kr=new THREE.Vector3(), _ku2=new THREE.Vector3(), _kn=new THREE.Vector3(), _kt=new THREE.Vector3(), _kp=new THREE.Vector3(), _kf=new THREE.Vector3(), _kq=new THREE.Quaternion(), _khq=new THREE.Quaternion();""")

# emotes: the feet stay where they stand. The pelvis may sway, roll and turn, and each leg is re-solved to keep its foot on its own spot (a foot the dance lifts is left alone)
rep("""  animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); poseHands(H,S,dt); }""",
"""  footRestore(H); animateRig0(H,S,dt); if(S.seat) seatPlace(H,S); else pickTwoHands(H,S); poseHands(H,S,dt); footPlant(H,S); }
const _fpM0=new THREE.Matrix4(), _fpMi=new THREE.Matrix4(), _fpG=[new THREE.Vector3(),new THREE.Vector3()], _fpT=new THREE.Vector3(), _fpJ=new THREE.Vector3(), _fpQ=[new THREE.Quaternion(),new THREE.Quaternion()], _fpQa=new THREE.Quaternion(), _fpQb=new THREE.Quaternion(), _fpW=[0,0];
// the solved legs are put back to their animated angles before the next frame, so the animation's own smoothing never sees them
function footRestore(H){ const f=H.anim.fk; if(!f||!f.on) return; const r=H.rig, v=f.v; f.on=false; r.hips.position.y=f.hy; let i=0;
  for(const L of [r.legL,r.legR]){ L.hp.rotation.x=v[i++]; L.hp.rotation.z=v[i++]; L.kn.rotation.x=v[i++]; L.an.rotation.set(v[i++],v[i++],v[i++]); } }
function footPlant(H,S){ if(!(S.emote&&EMOTES[S.emote.id])||S.seat||S.down||S.sky||H.anim.dead||S.onGround===false) return;
  const r=H.rig, hips=r.hips, legs=[r.legL,r.legR], f=H.anim.fk||(H.anim.fk={v:[],on:false}), v=f.v, A=0.4, B=0.37, LM=A+B-0.004; if(!legs[0].an) return;
  const em=S.emote, fresh=f.id!==em.id||em.t<(f.t||0); f.id=em.id; f.t=em.t; if(fresh) f.anc=null; const slide=em.id==='shuffle'; // the running man slides its feet on purpose
  f.on=true; f.hy=hips.position.y; let i=0; for(const L of legs){ v[i++]=L.hp.rotation.x; v[i++]=L.hp.rotation.z; v[i++]=L.kn.rotation.x; v[i++]=L.an.rotation.x; v[i++]=L.an.rotation.y; v[i++]=L.an.rotation.z; }
  hips.updateMatrix(); _fpM0.makeRotationX(hips.rotation.x).setPosition(0,hips.position.y,hips.position.z); _fpQa.setFromRotationMatrix(_fpM0); let drop=0;
  for(let q=0;q<2;q++){ const L=legs[q]; L.hp.updateMatrix(); L.kn.updateMatrix(); const a=_fpT.copy(L.an.position).applyMatrix4(L.kn.matrix).applyMatrix4(L.hp.matrix), g=_fpG[q].copy(a).applyMatrix4(_fpM0); // where the foot stands under a level pelvis
    if(!slide){ if(!f.anc) f.anc=[null,null]; if(!f.anc[q]) f.anc[q]=g.clone(); g.x=f.anc[q].x; g.z=f.anc[q].z; } // each foot keeps the spot it stood on when the emote began
    const u=Math.max(0,Math.min(1,(g.y-0.155)/0.08)), w=_fpW[q]=1-u*u*(3-2*u); a.applyMatrix4(hips.matrix); g.lerpVectors(a,g,w);
    _fpQ[q].copy(_fpQa).multiply(L.hp.quaternion).multiply(L.kn.quaternion).multiply(L.an.quaternion);                    // and how it is turned
    drop=Math.max(drop,w*(g.distanceTo(_fpJ.copy(L.hp.position).applyMatrix4(hips.matrix))-LM)); }
  if(drop>0){ hips.position.y-=Math.min(drop,0.08); hips.updateMatrix(); } _fpMi.copy(hips.matrix).invert();
  for(let q=0;q<2;q++){ const L=legs[q], w=_fpW[q]; if(w<0.002) continue; const d=_fpT.copy(_fpG[q]).applyMatrix4(_fpMi).sub(L.hp.position), len=Math.max(0.3,Math.min(LM,d.length())); d.setLength(len);
    const k=-(Math.PI-Math.acos(Math.max(-1,Math.min(1,(A*A+B*B-len*len)/(2*A*B))))), e0z=-B*Math.sin(k), ey=-A-B*Math.cos(k), hy=L.hp.rotation.y, ex=e0z*Math.sin(hy), ez=e0z*Math.cos(hy);
    const rr=Math.hypot(ex,ey), c=Math.max(-1,Math.min(1,d.x/rr)), yy=-rr*Math.sqrt(1-c*c); let ps=-Math.acos(c)-Math.atan2(ey,ex), th=Math.atan2(d.z,d.y)-Math.atan2(ez,yy);
    ps=Math.atan2(Math.sin(ps),Math.cos(ps)); th=Math.atan2(Math.sin(th),Math.cos(th)); L.hp.rotation.x=th; L.hp.rotation.z=ps; L.kn.rotation.x=k;
    _fpQb.copy(hips.quaternion).multiply(L.hp.quaternion).multiply(L.kn.quaternion).invert().multiply(_fpQ[q]); L.an.quaternion.slerp(_fpQb,w); } }""")

# ---------- 40. long guns no longer go through your back: the hand moves forward so the stock ends at the shoulder ----------
rep("    const ad=S.ads||0; _tw.addScaledVector(_aim,0.2-0.07*rec+0.06*ad)","    const ad=S.ads||0; _tw.addScaledVector(_aim,0.2-0.07*rec+0.06*ad+gunStockPush(r,mdl))")
rep("function handQuat(out,fwd,up){",r"""// how far a gun reaches back behind the hand (along the aim line, measured once per gun model): past about 22 cm the
// stock would sink into the shoulder and come out of the back, so the hand is pushed forward by the difference
const _gunBack=new Map();
function gunStockPush(r,mdl){ if(!mdl) return 0; let b=_gunBack.get(mdl);
  if(b==null){ const m=mdl==='ar'?r.gun:mdl==='pump'?r.pump:r[mdl], hand=r.armR.hand; if(!m||!hand) return 0;
    hand.updateMatrixWorld(true); const inv=new THREE.Matrix4().copy(hand.matrixWorld).invert(), v=new THREE.Vector3(), M=new THREE.Matrix4(); b=0;
    m.traverse(o=>{ if(!o.isMesh||!o.geometry||!o.geometry.attributes.position) return; M.multiplyMatrices(inv,o.matrixWorld); const pa=o.geometry.attributes.position;
      for(let i=0;i<pa.count;i+=3){ v.fromBufferAttribute(pa,i).applyMatrix4(M); if(v.y>b) b=v.y; } }); // hand space: +y points back along the gun
    _gunBack.set(mdl,b); }
  return Math.max(0,b-0.22); }
function handQuat(out,fwd,up){""")

# ---------- 73. a flowing pickaxe swing: alternating diagonal forehand / backhand strokes (side to side) on smooth curves
# through wind-up, strike and follow-through, the chest and hips turning with each one ----------
import re
m=re.search(r"function pickSwing\(t,pitch\)\{.*?\n\}\n",s,re.S); assert m
s=s.replace(m.group(0),r"""function pickSwing(t,pitch,side=1){
  // t, shoulder fwd, shoulder out (+ = out to the right), elbow, chest twist (+ = toward the left), spine lean, wrist
  const R=[0,0.6,0.25,1.1,0,0,0.2], F=side>0?[ // forehand: up over the right shoulder, sweep down and across to the left
    [0.22,2.3,0.95,1.2,-0.55,-0.05,0.1],[0.44,1.35+pitch*0.5,-0.35,0.1,0.45,0.18,-0.1],[0.7,0.6+pitch*0.3,-0.75,0.35,0.7,0.14,-0.2]]:[ // backhand: up across the left shoulder, sweep out to the right
    [0.22,2.25,-1.1,1.45,0.65,-0.05,0.3],[0.44,1.35+pitch*0.5,0.45,0.15,-0.35,0.16,0],[0.7,0.65+pitch*0.3,1.0,0.4,-0.65,0.12,-0.1]];
  const K=[R,...F,[1,...R.slice(1)]];
  let i=0; while(i<K.length-2&&t>K[i+1][0]) i++;
  const a=K[i], b=K[i+1], a0=K[Math.max(0,i-1)], b1=K[Math.min(K.length-1,i+2)], h=b[0]-a[0], u=Math.max(0,Math.min(1,(t-a[0])/h));
  // Catmull-Rom through the keys: the arm flows through each pose instead of stopping at it
  const C=j=>{ const p0=a0[j], p1=a[j], p2=b[j], p3=b1[j], m1=(p2-p0)*0.5, m2=(p3-p1)*0.5, u2=u*u, u3=u2*u;
    return (2*u3-3*u2+1)*p1+(u3-2*u2+u)*m1+(-2*u3+3*u2)*p2+(u3-u2)*m2; };
  return {sh:C(1),shz:C(2),el:C(3),ch:C(4),sp:C(5),wr:C(6),k:t>0.3&&t<0.75?Math.sin((t-0.3)/0.45*Math.PI):0};
}
""")
rep("    const t=Math.min(1,1-S.swingT/SWING_T), sw=pickSwing(t,S.pitch);","    if(!A.inSwing||S.swingT>A.prevSwT+1e-3) A.side=-(A.side||-1); A.inSwing=true; A.prevSwT=S.swingT; // each new swing comes from the other side\n    const t=Math.min(1,1-S.swingT/SWING_T), sw=pickSwing(t,S.pitch,A.side);")
rep("  // ----- upper body by activity -----\n","  // ----- upper body by activity -----\n  if(!(S.swingT>0)) A.inSwing=false;\n")

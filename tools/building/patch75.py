# ---------- 75. inside walls keep clear of the staircase: a dividing wall that would run along or into the stairs is cut
# short so it stops before them (it used to run straight through the steps) ----------
rep("  const pick=cands.find(c=>!(c.X?hitsStair(c.a,c.z,c.b,c.z):hitsStair(c.x,c.a,c.x,c.b)))||null;",
r"""  const clip=c=>{ let segs=[[c.a,c.b]]; const at=c.X?c.z:c.x, M=0.45;
    for(const [i,j] of st){ const p0=(c.X?j:i)*C-M, p1=((c.X?j:i)+1)*C+M, q0=(c.X?i:j)*C-M, q1=((c.X?i:j)+1)*C+M; if(at<p0||at>p1) continue;
      segs=segs.flatMap(([s0,s1])=>{ const o=[]; if(q0>s0) o.push([s0,Math.min(s1,q0)]); if(q1<s1) o.push([Math.max(s0,q1),s1]); return o.filter(([u,v])=>v-u>0.01); }); }
    const best=segs.sort((u,v)=>(v[1]-v[0])-(u[1]-u[0]))[0]; return best&&best[1]-best[0]>=2.6?Object.assign({},c,{a:best[0],b:best[1]}):null; };
  const pick=cands.map(clip).filter(Boolean).sort((p,q)=>((q.X===frontX)-(p.X===frontX))||((q.b-q.a)-(p.b-p.a)))[0]||null;""")
rep("  if(pick){ pick.door=pick.a+(pick.b-pick.a)*0.5+(((h.id*7+l)%3)-1)*1.2; }","  if(pick){ pick.door=Math.max(pick.a+0.75,Math.min(pick.b-0.75,pick.a+(pick.b-pick.a)*0.5+(((h.id*7+l)%3)-1)*1.2)); }")

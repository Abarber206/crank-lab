# patch206: no invisible walls. Collision boxes follow what is drawn:
#  - a tree's trunk is round, so its solid is a cross of three boxes the trunk's real thickness (it was a square box
#    up to 0.9 m across round a trunk half that), not a square post you bump into beside the bark
#  - a rock's solid follows its (turned) main boulder: three boxes round its oval, lower at the edges, instead of one
#    unturned box that both stuck out past the rock and let you into it
#  - bridge rails are solid in 0.6 m pieces along their slant (a third of a span's corner-to-corner box stood well off it)
rep('''  if(p.kind==='tree'||p.kind==='pine'){ const t=(p.kind==='tree'?.42:.34)*s+0.05; return [[x-t,0,z-t,x+t,3.2*s*(p.hs||1),z+t]]; }
  if(p.kind==='rock'){ const a=1.05*s, c=.9*s; return [[x-a,0,z-c,x+a,1.35*s,z+c]]; }''',
'''  if(p.kind==='tree'||p.kind==='pine'){ const t=(p.kind==='tree'?.37:.32)*s+0.04, H=3.2*s*(p.hs||1); // the trunk's thickness at body height, as a cross (round, near enough)
    return [[x-t*0.95,0,z-t*0.42,x+t*0.95,H,z+t*0.42],[x-t*0.42,0,z-t*0.95,x+t*0.42,H,z+t*0.95],[x-t*0.72,0,z-t*0.72,x+t*0.72,H,z+t*0.72]]; }
  if(p.kind==='rock'){ const m=p.g&&p.g.children.find(c=>c.isMesh), th=m?m.rotation.y:0, A=1.25*s*0.97, C=1.05*s*0.97, ex=Math.hypot(A*Math.cos(th),C*Math.sin(th)), ez=Math.hypot(A*Math.sin(th),C*Math.cos(th)), H=1.32*s;
    return [[x-ex*0.97,0,z-ez*0.45,x+ex*0.97,H*0.7,z+ez*0.45],[x-ex*0.45,0,z-ez*0.97,x+ex*0.45,H*0.7,z+ez*0.97],[x-ex*0.72,0,z-ez*0.72,x+ex*0.72,H,z+ez*0.72]]; }''')
rep('''const boxes=[]; for(let s=0;s<3;s++){ const f0=s/3, f1=(s+1)/3, xa=x+dx*f0, xb=x+dx*f1, za=z+dz*f0, zb=z+dz*f1, yb=Math.min(y,y2); boxes.push([Math.min(xa,xb)-0.08,yb-0.3,Math.min(za,zb)-0.08,Math.max(xa,xb)+0.08,Math.max(y,y2)+0.82,Math.max(za,zb)+0.08]''',
'''const boxes=[], NS=Math.max(3,Math.ceil(Math.hypot(dx,dz)/0.6)); for(let s=0;s<NS;s++){ const f0=s/NS, f1=(s+1)/NS, xa=x+dx*f0, xb=x+dx*f1, za=z+dz*f0, zb=z+dz*f1, ya=y+(y2-y)*f0, yb2=y+(y2-y)*f1; boxes.push([Math.min(xa,xb)-0.08,Math.min(ya,yb2)-0.3,Math.min(za,zb)-0.08,Math.max(xa,xb)+0.08,Math.max(ya,yb2)+0.82,Math.max(za,zb)+0.08]''')

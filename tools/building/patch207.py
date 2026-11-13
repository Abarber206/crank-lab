# patch207: a house's gable ends (the triangle of wall under each end of a pitched roof) were only drawn: you could walk
# straight through them into the roof. They're solid now, in thin slices that stay inside the triangle.
rep('''  if(p.fix) out.push(...p.fix.boxes); // a house's staircase or stairwell railing''',
'''  if(p.type==='cone'&&p.skin&&p.gable) for(const [side] of p.gable){ const m=p.mask||0, bit=b=>(m>>b&1)?1:0, ed={w:[0,2,'z',0],e:[1,3,'z',CELL],n:[0,1,'x',0],s:[2,3,'x',CELL]}[side], h0=bit(ed[0]), h1=bit(ed[1]); if(h0===h1) continue;
    const x0=p.i*CELL, z0=p.j*CELL, N=10; for(let k=0;k<N;k++){ const a=k/N, b=(k+1)/N, hh=LVL*(h0?1-b:a); if(hh<0.05) continue; // (each slice as tall as the triangle at its lower end)
      if(ed[2]==='z'){ const X=x0+ed[3]; out.push([X-WT/2,y0,z0+a*CELL,X+WT/2,y0+hh,z0+b*CELL]); } else { const Z=z0+ed[3]; out.push([x0+a*CELL,y0,Z-WT/2,x0+b*CELL,y0+hh,Z+WT/2]); } } }
  if(p.fix) out.push(...p.fix.boxes); // a house's staircase or stairwell railing''')

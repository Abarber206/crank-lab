# patch173: roads that look lived-in instead of drawn: worn asphalt (wheel tracks, cracks, patched repairs, faded and
# chipped markings, a dusty edge) over a 24 m repeat, a slightly ragged asphalt edge, and a dirt shoulder that comes
# and goes in width with the grass growing in and out along it.
i=s.index("const roadTex=(()=>{ const W=256, Hh=1024,"); j=s.index("return t; })();",i)+len("return t; })();")
s=s[:i]+r"""const roadTex=(()=>{ const W=256, Hh=2048, c=document.createElement('canvas'); c.width=W; c.height=Hh; const g=c.getContext('2d'), R=seeded(4401);
  g.fillStyle='#4b4e53'; g.fillRect(0,0,W,Hh);
  for(let i=0;i<120000;i++){ const v=R(); g.fillStyle=v<.5?'rgba(22,24,28,.26)':v<.9?'rgba(140,140,138,.16)':'rgba(200,196,186,.22)'; g.fillRect(R()*W,R()*Hh,1+R(),1+R()); }
  const blot=(x,y,r,col)=>{ const gr=g.createRadialGradient(x,y,0,x,y,r); gr.addColorStop(0,col); gr.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=gr; g.fillRect(x-r,y-r,r*2,r*2); };
  for(let i=0;i<44;i++){ const x=R()*W, y=R()*Hh; for(const o of [-Hh,0,Hh]) blot(x,y+o,20+R()*50,'rgba(30,30,32,.18)'); }
  const pc=document.createElement('canvas'); pc.width=W; pc.height=1024; pc.getContext('2d').drawImage(c,0,0); // the same asphalt without markings or wear, for junctions
  roadPlainTex=new THREE.CanvasTexture(pc); roadPlainTex.wrapS=roadPlainTex.wrapT=THREE.RepeatWrapping; roadPlainTex.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
  // wheel tracks: two smoother, darker bands down each lane, and a lighter oil-stained strip between them
  for(const x0 of [64,192]){ for(const o of [-31,31]){ const gr=g.createLinearGradient(x0+o-15,0,x0+o+15,0); gr.addColorStop(0,'rgba(24,24,27,0)'); gr.addColorStop(0.5,'rgba(24,24,27,.2)'); gr.addColorStop(1,'rgba(24,24,27,0)'); g.fillStyle=gr; g.fillRect(x0+o-15,0,30,Hh); }
    for(let i=0;i<14;i++){ const y=R()*Hh; for(const k of [-Hh,0,Hh]) blot(x0+(R()-.5)*16,y+k,8+R()*16,'rgba(16,16,18,.22)'); } }
  // patched repairs: rectangles of newer, darker asphalt with a sealed seam
  for(let i=0;i<6;i++){ const lane=R()<0.5?0:128, w=36+R()*84, x=lane+6+R()*(122-w), h=70+R()*240, y=R()*(Hh-h);
    g.fillStyle=R()<0.7?'rgba(34,35,39,.55)':'rgba(96,96,94,.28)'; g.fillRect(x,y,w,h); for(let k=0;k<900;k++){ g.fillStyle='rgba(120,120,118,.12)'; g.fillRect(x+R()*w,y+R()*h,1,1); }
    g.strokeStyle='rgba(14,14,16,.55)'; g.lineWidth=1.6; g.strokeRect(x,y,w,h); }
  // cracks: thin wandering lines, mostly lengthways, more of them toward the edges where the road breaks up
  const crack=(x,y,a,len)=>{ g.beginPath(); g.moveTo(x,y); for(let l=0;l<len;l+=3){ a+=(R()-.5)*0.7; x+=Math.cos(a)*3; y+=Math.sin(a)*3; g.lineTo(x,y); if(R()<0.04) crack(x,y,a+(R()<.5?1:-1)*(0.8+R()*0.6),len*0.4); } g.stroke(); };
  g.strokeStyle='rgba(16,16,18,.6)'; g.lineCap='round';
  for(let i=0;i<70;i++){ const edge=R()<0.55, x=edge?(R()<.5?4+R()*26:W-30+R()*26):20+R()*(W-40), y=R()*(Hh-120)+60; g.lineWidth=0.8+R()*0.9;
    crack(x,y,R()<0.75?Math.PI/2+(R()-.5)*0.6:(R()-.5)*0.8,edge?30+R()*90:20+R()*70); }
  // a dusty, crumbly margin outside the edge lines
  for(const [x0,x1] of [[0,13],[W-13,W]]){ const gr=g.createLinearGradient(x0===0?0:W,0,x0===0?13:W-13,0); gr.addColorStop(0,'rgba(118,104,80,.42)'); gr.addColorStop(1,'rgba(118,104,80,0)'); g.fillStyle=gr; g.fillRect(x0,0,x1-x0,Hh);
    for(let k=0;k<700;k++){ g.fillStyle=R()<.5?'rgba(150,136,108,.35)':'rgba(20,20,22,.3)'; g.fillRect(x0+R()*(x1-x0),R()*Hh,1+R()*2,1+R()*2); } }
  // markings, faded and chipped: edge lines in short runs of varying strength, the centre dashes worn through in places
  for(const x of [13,W-19]) for(let y=0;y<Hh;y+=16){ if(R()<0.03) continue; g.fillStyle='rgba(236,236,230,'+(0.55+R()*0.35).toFixed(2)+')'; g.fillRect(x+(R()-.5)*0.6,y,6,16); }
  for(const y0 of [0,Hh/2]){ g.fillStyle='rgba(230,194,60,.92)'; g.fillRect(W/2-4,y0,8,Hh/4); }
  for(const [x,w] of [[13,6],[W-19,6],[W/2-4,8]]) for(let k=0;k<1400;k++){ g.fillStyle=R()<.7?'rgba(72,74,78,.75)':'rgba(40,42,46,.6)'; g.fillRect(x+R()*w,R()*Hh,1+R()*1.5,1+R()*2); }
  const t=new THREE.CanvasTexture(c); t.wrapS=t.wrapT=THREE.RepeatWrapping; t.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy()); return t; })();"""+s[j:]
# the texture now repeats every 24 m; and a slightly ragged asphalt edge on the open road (lines stay straight: the uv follows the edge)
rep("""    for(const c of AC){ const px=x+sx*ROAD_HW*c, pz=z+sz*ROAD_HW*c,""","""    for(const c0 of AC){ const c=(c0===-1||c0===1)&&!rd.street&&!dk?c0*(1-0.06*(0.5+0.5*gnoise(s/2.4,k*13.1+c0*3.7,93))):c0, px=x+sx*ROAD_HW*c, pz=z+sz*ROAD_HW*c,""")
rep("""uv.push((c+1)/2,s/12); lines.push(ln); }""","""uv.push((c+1)/2,s/24); lines.push(ln); }""")
# a shoulder that widens and narrows, grass growing in and out along it
rep("""      const gore=minD2[c]<dd+6, edge=gore?(dd<3.9?0:1e4):dd; DIRT[c]=gore&&dd>=3.9?0:dd<5?Math.round(255*(1-sstep(3.8,5.0,dd))):0;
      if(edge<4.8) GRASS[c]=0;""","""      let eo=5.0; if(dd<7.5){ const i_=c%N, u=-WHALF+i_*WHS, v=-WHALF+(c-i_)/N*WHS, nz=gnoise(u/9,v/9,71)+0.5*gnoise(u/3.2,v/3.2,72); eo=Math.max(4.1,Math.min(6.9,5.2+1.6*nz)); }
      const gore=minD2[c]<dd+6, edge=gore?(dd<3.9?0:1e4):dd; DIRT[c]=gore&&dd>=3.9?0:dd<eo?Math.round(255*(1-sstep(3.7,eo,dd))):0;
      if(edge<eo-0.3) GRASS[c]=0;""")
# worn earth (a separate cover from the asphalt fill): along the road shoulders outside town and on the dirt tracks
rep("""DIRT=WORLD.DIRT=new Uint8Array(N*N);""","""DIRT=WORLD.DIRT=new Uint8Array(N*N), TRACK=WORLD.TRACK=new Uint8Array(N*N);""")
rep("""      if(edge<eo-0.3) GRASS[c]=0;""","""      TRACK[c]=gore||dd<3.2||dd>=eo+0.8?0:Math.round(170*(1-sstep(eo-1.0,eo+0.8,dd)));
      if(edge<eo-0.3) GRASS[c]=0;""")
rep("""const c=worldCell(x,z); if(c<0) continue; WH[c]=WORLD.H0[c];""","""const c=worldCell(x,z); if(c<0) continue; WH[c]=WORLD.H0[c]; WORLD.TRACK[c]=0;""")
rep("""cov[k*3+1]=SNOW[q]/255;""","""cov[k*3+1]=SNOW[q]?SNOW[q]/255:-WORLD.TRACK[q]/255;""")
rep("""    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.9,0.93,0.97)*(0.9+0.12*rk.r),clamp(vCover.y,0.0,1.0)); }`); };""",
    """    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.5,0.42,0.3)*(0.78+0.4*rk.g),clamp(-vCover.y,0.0,1.0)*0.9); // worn earth: road shoulders, dirt tracks (a negative second cover value)
    diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.9,0.93,0.97)*(0.9+0.12*rk.r),clamp(vCover.y,0.0,1.0)); }`); };""")
# nothing growing or lying in the middle of a dirt track
rep("""initProps(); props.forEach(p=>{ if((!p.yard&&townAt(p.x,p.z,6))||shoreAt(p.x,p.z)){""","""initProps(); props.forEach(p=>{ const tc=worldCell(p.x,p.z); if((!p.yard&&townAt(p.x,p.z,6))||shoreAt(p.x,p.z)||(!p.yard&&tc>=0&&WORLD.TRACK[tc]>110)){""")

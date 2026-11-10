# ---------- 99. damage cracks redrawn: sharper (twice the resolution) fractures that radiate from impact points, taper and
# branch, with a dark core and a lit edge so they read as depth; chipped-away patches showing raw material underneath.
# Wood splits along the grain with pale splinters; brick cracks step along the mortar and spalls; metal dents, tears and scores.
# Also: the minimap shows the real houses (roofs in their colours, ridge line, garage) instead of build tiles. ----------
import re
a=s.index("(function makeCracks(){"); b=s.index("function damageStage(p){",a)
s=s[:a]+r"""(function makeCracks(){
  const R=()=>Math.random(), N=512;
  MAT_ORDER.forEach(mat=>{
    const c=document.createElement('canvas'); c.width=c.height=N; const g=c.getContext('2d'); g.lineCap='round'; g.lineJoin='round';
    const DARK={wood:'rgba(38,20,8,.95)',brick:'rgba(24,19,17,.95)',metal:'rgba(12,15,20,.95)'}[mat], LIT={wood:'rgba(250,222,170,.8)',brick:'rgba(238,228,214,.7)',metal:'rgba(236,243,250,.85)'}[mat], RAW={wood:['#e2c08a','#cfa870'],brick:['#d9cdbd','#b9aa98'],metal:['#c9d2db','#8f9aa6']}[mat];
    // one fracture: a tapering, wandering line with a lit edge beside it, and the odd branch
    const crack=(x,y,len,ang,w,depth)=>{ for(let i=0;i<len;i++){ const t=i/len, ww=Math.max(0.6,w*(1-t*0.85));
        let da=(R()-.5)*(mat==='wood'?0.5:0.95); if(mat==='brick'&&R()<0.35) ang=Math.round(ang/(Math.PI/2))*(Math.PI/2)+(R()<0.5?0:Math.PI/2*(R()<.5?1:-1)); // steps along the mortar
        if(mat==='wood') ang+=(Math.PI/2*Math.sign(Math.sin(ang)||1)-ang)*0.25; // pulled back onto the grain
        ang+=da; const st=7+R()*7, nx=x+Math.cos(ang)*st, ny=y+Math.sin(ang)*st;
        g.strokeStyle=LIT; g.lineWidth=ww*0.55; g.beginPath(); g.moveTo(x+1.6,y+1.6); g.lineTo(nx+1.6,ny+1.6); g.stroke();
        g.strokeStyle=DARK; g.lineWidth=ww; g.beginPath(); g.moveTo(x,y); g.lineTo(nx,ny); g.stroke();
        if(depth<2&&R()<0.16) crack(nx,ny,Math.round((len-i)*0.55),ang+(R()<.5?1:-1)*(0.5+R()*0.7),ww*0.7,depth+1);
        x=nx; y=ny; if(x<-20||y<-20||x>N+20||y>N+20) break; } };
    // a patch where the surface has come away: a ragged shape of raw material with a shadowed upper edge
    const chip=(x,y,r)=>{ const n=7+Math.floor(R()*4), pts=[]; for(let k=0;k<n;k++){ const a=k/n*6.283, rr=r*(0.55+R()*0.6); pts.push([x+Math.cos(a)*rr*(mat==='wood'?0.55:1),y+Math.sin(a)*rr*(mat==='wood'?1.5:0.8)]); }
      const path=()=>{ g.beginPath(); pts.forEach((p,k)=>k?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1])); g.closePath(); };
      g.fillStyle=RAW[R()<0.5?0:1]; path(); g.fill(); g.save(); path(); g.clip(); g.fillStyle='rgba(0,0,0,.28)'; g.fillRect(x-r*2,y-r*2,r*4,r*1.15); g.restore(); g.strokeStyle=DARK; g.lineWidth=1.3; path(); g.stroke(); };
    const stage=(n)=>{
      for(let q=0;q<n;q++){ const x=N*0.08+R()*N*0.84, y=N*0.08+R()*N*0.84, rays=mat==='wood'?2+Math.floor(R()*2):3+Math.floor(R()*3), a0=R()*6.283;
        if(mat==='metal'){ const r=16+R()*26, gr=g.createRadialGradient(x-r*0.2,y-r*0.2,1,x,y,r); gr.addColorStop(0,'rgba(14,18,24,.9)'); gr.addColorStop(0.55,'rgba(40,48,58,.5)'); gr.addColorStop(0.86,'rgba(236,243,250,.6)'); gr.addColorStop(1,'rgba(0,0,0,0)'); g.fillStyle=gr; g.beginPath(); g.arc(x,y,r,0,7); g.fill(); // a dent with a bright rim
          if(R()<0.6){ g.fillStyle='rgba(6,7,9,.97)'; g.beginPath(); g.ellipse(x,y,2.5+R()*4,2+R()*3,R()*3,0,7); g.fill(); } // punched through
          for(let k=0;k<rays-1;k++) crack(x,y,5+R()*7,a0+k/rays*6.283,2.2,1); // short tears
          g.strokeStyle='rgba(236,243,250,.6)'; g.lineWidth=1.4; g.beginPath(); const sx=R()*N, sy=R()*N, sa=R()*3; g.moveTo(sx,sy); g.lineTo(sx+Math.cos(sa)*(40+R()*90),sy+Math.sin(sa)*(40+R()*90)); g.stroke(); } // scoring
        else { chip(x,y,(mat==='brick'?12:9)+R()*12);
          for(let k=0;k<rays;k++) crack(x,y,(mat==='wood'?12:9)+R()*14,mat==='wood'?(k%2?1:-1)*Math.PI/2+(R()-.5)*0.5:a0+k/rays*6.283+(R()-.5)*0.6,mat==='wood'?4.2:3.6,0);
          if(mat==='wood'){ g.strokeStyle=LIT; g.lineWidth=1.8; for(let k=0;k<5;k++){ const sx=x+(R()-.5)*26, sy=y+(R()-.5)*70; g.beginPath(); g.moveTo(sx,sy); g.lineTo(sx+(R()-.5)*7,sy+10+R()*22); g.stroke(); } } // splinters
          else { g.fillStyle='rgba(40,34,30,.3)'; g.beginPath(); g.arc(x+(R()-.5)*30,y+(R()-.5)*30,10+R()*18,0,7); g.fill(); for(let k=0;k<10;k++){ g.fillStyle=RAW[k%2]; g.fillRect(x+(R()-.5)*70,y+10+R()*50,1.5+R()*2.5,1.5+R()*2.5); } } } // soot and grit
      }
      const cp=document.createElement('canvas'); cp.width=cp.height=N; cp.getContext('2d').drawImage(c,0,0); const tx=new THREE.CanvasTexture(cp); tx.anisotropy=4;
      return new THREE.MeshLambertMaterial({map:tx,transparent:true,depthWrite:false,side:THREE.DoubleSide,polygonOffset:true,polygonOffsetFactor:-2,polygonOffsetUnits:-6});
    };
    crackMats[mat]=[stage(mat==='metal'?3:3),stage(mat==='metal'?4:4),stage(mat==='metal'?6:6)];
  });
})();
"""+s[b:]
# minimap: real houses, not their build pieces
rep("  near(ox,oz,Math.ceil(R/CELL)+1).forEach(p=>{\n    if(p.type==='wall'){","""  for(const t of TOWNS){ if(Math.abs(t.x-ox)>R+t.R+20||Math.abs(t.z-oz)>R+t.R+20) continue;
    for(const h of t.houses){ const C=CELL, x0=tx(h.i0*C), z0=tz(h.j0*C), w=h.w*C*sc, d=h.d*C*sc; if(x0>S||z0>S||x0+w<0||z0+d<0) continue;
      const G=h.garage; if(G){ g.fillStyle='#6b6f75'; g.strokeStyle='rgba(20,14,8,.85)'; g.lineWidth=dpr; g.fillRect(tx(G.i*C),tz(G.j*C),C*sc,C*sc); g.strokeRect(tx(G.i*C),tz(G.j*C),C*sc,C*sc); }
      g.fillStyle=h.roof==='brick'?['#b5583f','#a14b38','#c4694a','#8f4636'][h.skin.roof]:['#5f5a55','#6e655c','#4f4c49','#7a6f63'][h.skin.roof]; g.strokeStyle='rgba(20,14,8,.9)'; g.lineWidth=1.2*dpr; g.fillRect(x0,z0,w,d); g.strokeRect(x0,z0,w,d);
      g.strokeStyle='rgba(255,255,255,.35)'; g.lineWidth=dpr; g.beginPath(); if(h.w>=h.d){ g.moveTo(x0,z0+d/2); g.lineTo(x0+w,z0+d/2); } else { g.moveTo(x0+w/2,z0); g.lineTo(x0+w/2,z0+d); } g.stroke(); } }
  near(ox,oz,Math.ceil(R/CELL)+1).forEach(p=>{ if(p.owner==='world') return;
    if(p.type==='wall'){""")

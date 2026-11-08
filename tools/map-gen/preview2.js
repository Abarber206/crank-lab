const zlib=require('zlib');
const fs=require('fs'); const {W,gen}=require('./bake_test.js');
const src=fs.readFileSync('preview.js','utf8'); const png=eval('('+src.slice(src.indexOf('function png'),src.indexOf('\nconst out=')).replace('function png','function')+')');
const S=1024, E=850, px=2*E/S, rgb=Buffer.alloc(S*S*3), Hs=new Float32Array(S*S);
for(let y=0;y<S;y++) for(let x=0;x<S;x++) Hs[y*S+x]=W.at(W.H,-E+x*px,-E+y*px);
for(let y=0;y<S;y++) for(let x=0;x<S;x++){ const i=y*S+x, h=Hs[i], hx=Hs[y*S+Math.min(S-1,x+1)]-Hs[y*S+Math.max(0,x-1)], hz=Hs[Math.min(S-1,y+1)*S+x]-Hs[Math.max(0,y-1)*S+x];
  let nx=-hx/(2*px), nz=-hz/(2*px), ny=1, l=Math.hypot(nx,ny,nz); nx/=l; ny/=l; nz/=l; const sh=Math.max(0,(nx*-0.6+ny*0.7+nz*-0.4)), k=0.35+0.85*sh;
  const rd=W.at(W.RD,-E+x*px,-E+y*px); let c=h>170&&ny>0.6?[235,235,235]:(1-ny>0.25||h>150)?[125,120,115]:h>45?[140,150,90]:[95,140,70];
  if(rd<3.6) c=[60,60,64]; else if(rd<5.5) c=[150,130,100];
  rgb[i*3]=Math.min(255,c[0]*k); rgb[i*3+1]=Math.min(255,c[1]*k); rgb[i*3+2]=Math.min(255,c[2]*k); }
for(const t of W.towns){ const cx=Math.round((t.u+E)/px), cy=Math.round((t.v+E)/px); for(let a=0;a<360;a+=2){ const x=Math.round(cx+Math.cos(a*Math.PI/180)*t.R/px), y=Math.round(cy+Math.sin(a*Math.PI/180)*t.R/px); if(x>=0&&y>=0&&x<S&&y<S){ const i=y*S+x; rgb[i*3]=255; rgb[i*3+1]=220; rgb[i*3+2]=60; } } }
fs.writeFileSync('roads.png',png(S,S,rgb)); console.log('roads',W.roads.length,'total km',(W.roads.reduce((s,r)=>s+r.pts.length*2,0)/1000).toFixed(1));

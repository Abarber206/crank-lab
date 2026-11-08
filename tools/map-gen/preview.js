// hillshade preview of the generator: node preview.js out.png [extent]
const fs=require('fs'), zlib=require('zlib');
const {makeWorldGen}=require('./gen.js');
function seeded(seed){ return ()=>{ seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function png(w,h,rgb){ const raw=Buffer.alloc((w*3+1)*h); for(let y=0;y<h;y++){ raw[y*(w*3+1)]=0; rgb.copy(raw,y*(w*3+1)+1,y*w*3,(y+1)*w*3); }
  const crc=(b)=>{ let c,crcT=[]; for(let n=0;n<256;n++){ c=n; for(let k=0;k<8;k++) c=c&1?0xedb88320^(c>>>1):c>>>1; crcT[n]=c>>>0; } let x=0xffffffff; for(const v of b) x=crcT[(x^v)&255]^(x>>>8); return (x^0xffffffff)>>>0; };
  const chunk=(t,d)=>{ const l=Buffer.alloc(4); l.writeUInt32BE(d.length); const td=Buffer.concat([Buffer.from(t),d]); const c=Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l,td,c]); };
  const ih=Buffer.alloc(13); ih.writeUInt32BE(w,0); ih.writeUInt32BE(h,4); ih[8]=8; ih[9]=2;
  return Buffer.concat([Buffer.from([137,80,78,71,13,10,26,10]),chunk('IHDR',ih),chunk('IDAT',zlib.deflateSync(raw)),chunk('IEND',Buffer.alloc(0))]); }
const out=process.argv[2]||'prev.png', E=+(process.argv[3]||2048), W=1024;
const G=makeWorldGen({FLAT_R:42,MAP_R:800,massifs:4,rng:seeded});
let t0=Date.now(); let n=0; for(let i=0;i<200000;i++){ G.genH((i%447)*3.7-800,Math.floor(i/447)*3.7-800); n++; } console.log('genH',((Date.now()-t0)/n*1000).toFixed(2),'us/call');
const H=new Float32Array(W*W), px=2*E/W; let mx=0;
for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const h=G.genH(-E+x*px,-E+y*px); H[y*W+x]=h; if(h>mx) mx=h; }
console.log('max height',mx.toFixed(0),'massifs',G.MASSIFS.map(m=>`(${m.u.toFixed(0)},${m.v.toFixed(0)}) R${m.R.toFixed(0)} P${m.P.toFixed(0)}`).join(' '));
const rgb=Buffer.alloc(W*W*3);
for(let y=0;y<W;y++) for(let x=0;x<W;x++){ const i=y*W+x, h=H[i], hx=H[y*W+Math.min(W-1,x+1)]-H[y*W+Math.max(0,x-1)], hz=H[Math.min(W-1,y+1)*W+x]-H[Math.max(0,y-1)*W+x];
  let nx=-hx/(2*px), nz=-hz/(2*px), ny=1, l=Math.hypot(nx,ny,nz); nx/=l; ny/=l; nz/=l; const slope=1-ny;
  const sh=Math.max(0,(nx*-0.6+ny*0.7+nz*-0.4)); let r,g,b;
  if(h>170&&ny>0.6){ r=g=b=235; } else if(slope>0.25||h>150){ r=125; g=120; b=115; } else if(h>45){ r=140; g=150; b=90; } else { r=95; g=140; b=70; }
  const k=0.35+0.85*sh; const dd=Math.hypot(-E+x*px,-E+y*px); const ring=Math.abs(dd-800)<px*1.2;
  rgb[i*3]=ring?255:Math.min(255,r*k); rgb[i*3+1]=ring?40:Math.min(255,g*k); rgb[i*3+2]=ring?40:Math.min(255,b*k); }
fs.writeFileSync(out,png(W,W,rgb)); console.log('wrote',out);

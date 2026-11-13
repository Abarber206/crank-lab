// a house's gable end (the triangle under each end of a pitched roof) is solid: walking at it from outside, at attic
// height where the triangle is tall, is blocked; and the roof slopes and walls still work as before
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.argv[2]||'/home/claude/crank-lab/index.html','scene,P,settings,pieces,blocked,near,CELL,LVL'),{norender:true});
 await pg.evaluate(()=>{ document.getElementById('play').click(); }); await sleep(4000);
 const r=await pg.evaluate(()=>{ const C=5, L=4; let n=0, stop=0, open_=0, bad=[];
   T.pieces.forEach(p=>{ if(p.type!=='cone'||!p.gable||!p.skin||n>=300) return; for(const [side,out] of p.gable){ const m=p.mask||0, bit=k=>(m>>k&1), ed={w:[0,2],e:[1,3],n:[0,1],s:[2,3]}[side]; if(bit(ed[0])===bit(ed[1])) continue; n++;
       const hi0=bit(ed[0]), along=hi0?0.2:0.8, y=p.l*L+0.15, h=1.8; let ox,oz,nx,nz; const x0=p.i*C, z0=p.j*C;
       if(side==='w'||side==='e'){ const X=x0+(side==='e'?C:0), z=z0+along*C; ox=X+out*0.9; nx=X-out*0.6; oz=nz=z; } else { const Z=z0+(side==='s'?C:0), x=x0+along*C; oz=Z+out*0.9; nz=Z-out*0.6; ox=nx=x; }
       const ps=T.near((ox+nx)/2,(oz+nz)/2); let hit=false; for(let s=1;s<=15;s++){ const f=s/15, f0=(s-1)/15; if(T.blocked(ox+(nx-ox)*f,oz+(nz-oz)*f,ox+(nx-ox)*f0,oz+(nz-oz)*f0,y,h,0.3,ps)){ hit=true; break; } }
       if(hit) stop++; else { open_++; if(bad.length<4) bad.push([p.key,side,+ox.toFixed(1),+y.toFixed(1),+oz.toFixed(1)]); } } });
   return {n,stop,open:open_,bad}; });
 console.log(JSON.stringify(r)); console.log(r.n>50&&r.open===0?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

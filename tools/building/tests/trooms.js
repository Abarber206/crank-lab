// every house has real rooms: each room holds only what belongs in it, every house has somewhere to sit, cook and sleep,
// and you can walk from the front door (or the stairs) to every piece of furniture through the doorways
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,TOWNS,houseRooms,houseStair,doorOf'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.props&&T.props.length,null,{timeout:120000}); await sleep(500);
 const r=await pg.evaluate(()=>{ const C=5, OK={living:[0,5,6,2],kitchen:[3,10,1],bed:[4,8,7,9],bed2:[4,8,7],bath:[11,13,12],study:[9,2,6]};
   const F=T.props.filter(p=>p.kind==='furn'&&!p.gone); const out={houses:0,rooms:0,types:{},wrong:0,noSit:0,noCook:0,noSleep:0,noBath:0,unreached:0,emptyRooms:0,sample:[]};
   for(const t of T.TOWNS) for(const h of t.houses){ out.houses++; const have={}; const D=T.doorOf(h), st=h.floors>1?T.houseStair(h).cells:[];
     for(let l=h.L;l<h.L+h.floors;l++){ const R=T.houseRooms(h,l), x0=h.i0*C, z0=h.j0*C, W=h.w*C, Dd=h.d*C, S=0.25, nx=Math.round(W/S), nz=Math.round(Dd/S), blk=new Uint8Array(nx*nz), cell=(x,z)=>Math.floor((x-x0)/S)+nx*Math.floor((z-z0)/S);
       const fill=(a,b,c,d)=>{ for(let i=Math.max(0,Math.floor((a-x0)/S));i<Math.min(nx,Math.ceil((c-x0)/S));i++) for(let j=Math.max(0,Math.floor((b-z0)/S));j<Math.min(nz,Math.ceil((d-z0)/S));j++) blk[i+nx*j]=1; };
       const PAD=0.3; // a body's half width
       for(const w of R.walls){ const th=0.13+PAD; if(w.axis==='x'){ const x=w.i*C, a=w.j*C, e=a+C; if(w.mask===511) fill(x-th,a,x+th,e); else { fill(x-th,a,x+th,a+C/3+PAD); fill(x-th,e-C/3-PAD,x+th,e); } } else { const z=w.j*C, a=w.i*C, e=a+C; if(w.mask===511) fill(a,z-th,e,z+th); else { fill(a,z-th,a+C/3+PAD,z+th); fill(e-C/3-PAD,z-th,e,z+th); } } }
       fill(x0,z0,x0+0.13+PAD,z0+Dd); fill(x0+W-0.13-PAD,z0,x0+W,z0+Dd); fill(x0,z0,x0+W,z0+0.13+PAD); fill(x0,z0+Dd-0.13-PAD,x0+W,z0+Dd);
       const mine=F.filter(p=>Math.abs(p.base-l*4)<0.5&&p.x>x0&&p.x<x0+W&&p.z>z0&&p.z<z0+Dd); for(const p of mine) for(const bx of p.boxes) fill(bx[0]-PAD,bx[2]-PAD,bx[3]+PAD,bx[5]+PAD);
       // flood from just inside the front door (ground floor) or from the stairs (upstairs)
       const seen=new Uint8Array(nx*nz), Q=[]; const start=(x,z)=>{ const c=cell(x,z); if(c>=0&&c<nx*nz&&!seen[c]){ seen[c]=1; Q.push(c); } };
       if(l===h.L) start(D.x-D.nx*0.8,D.z-D.nz*0.8); else for(const [i,j] of st) start((i+.5)*C,(j+.5)*C);
       while(Q.length){ const c=Q.pop(), i=c%nx, j=(c-i)/nx; for(const [a,b2] of [[1,0],[-1,0],[0,1],[0,-1]]){ const u=i+a, v=j+b2; if(u<0||v<0||u>=nx||v>=nz) continue; const k=u+nx*v; if(seen[k]||blk[k]) continue; seen[k]=1; Q.push(k); } }
       for(const rm of R.rooms){ out.rooms++; out.types[rm.type]=(out.types[rm.type]||0)+1; have[rm.type]=1;
         const inRoom=p=>rm.cells.some(([i,j])=>p.x>i*C&&p.x<(i+1)*C&&p.z>j*C&&p.z<(j+1)*C); const ps=mine.filter(inRoom); if(!ps.length) out.emptyRooms++;
         for(const p of ps){ if(!OK[rm.type].includes(p.ft)){ out.wrong++; if(out.sample.length<6) out.sample.push([rm.type,p.ft]); }
           // somewhere free and reached within a step of the piece
           const bx=p.boxes[0]; let near=false; for(let x=bx[0]-0.9;x<=bx[3]+0.9&&!near;x+=S) for(let z=bx[2]-0.9;z<=bx[5]+0.9;z+=S){ if(x<=x0||z<=z0||x>=x0+W||z>=z0+Dd) continue; if(seen[cell(x,z)]){ near=true; break; } }
           if(!near){ out.unreached++; if(out.sample.length<6) out.sample.push(['unreached',rm.type,p.ft,h.w,h.d,h.floors,l-h.L]); } }
         if(rm.type==='kitchen'&&!ps.some(p=>p.ft===3)) out.noCook++; if((rm.type==='bed'||rm.type==='bed2')&&!ps.some(p=>p.ft===4)) out.noSleep++; if(rm.type==='bath'&&!ps.some(p=>p.ft===11)) out.noBath++; if(rm.type==='living'&&!ps.some(p=>p.ft===0||p.ft===6)) out.noSit++; } }
     if(!have.living) out.noSit++; if(!have.kitchen) out.noCook++; if(!have.bed&&!have.bed2) out.noSleep++; }
   return out; });
 const ok=r.wrong===0&&r.unreached===0&&r.noSit===0&&r.noCook===0&&r.noSleep===0&&r.noBath===0&&r.emptyRooms===0&&r.types.bath>10;
 console.log(JSON.stringify(r), ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

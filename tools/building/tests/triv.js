// rivers and bridges: water runs downhill and is wet all the way; you walk and drive across every bridge on its deck,
// wade under the main river's bridges, wade slower than you run, and nothing grows in the water
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,WORLD,SPAWN,TOWNS,terrainH,waterAt,physStep,moveBody,karts,simKart,props,STATICS,settings,RUN'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(()=>{ const out={}, W=T.WORLD, S=T.SPAWN, P=T.P, dt=1/60; P.sky=null; P.kart=null;
   out.rivers=W.rivers.length; out.mainLen=W.rivers[0].pts.length*2; out.bridges=W.bridges.length;
   // downhill, and wet along the middle
   let rises=0, dry=0, n=0, maxDepth=0; for(const rv of W.rivers){ rv.pts.forEach((p,q)=>{ if(q&&p[2]>rv.pts[q-1][2]+1e-4) rises++; if(q%5||q<30||q>rv.pts.length-4) return; n++; const x=S[0]+p[0], z=S[2]+p[1], w=T.waterAt(x,z), d=w-T.terrainH(x,z); if(!(w>-999)||d<0.12) dry++; if(d>maxDepth) maxDepth=d; }); }
   out.rises=rises; out.dry=dry; out.samples=n; out.maxDepth=+maxDepth.toFixed(2);
   const place=(x,y,z,yaw)=>{ P.pos.set(x,y,z); P.vel.set(0,0,0); P.yaw=yaw; P.onGround=false; P.groundSlab=null; P.crouch=false; if(P.phase) P.phase.clear(); };
   const walk=(n,fn)=>{ for(let i=0;i<n;i++){ T.moveBody(P,1,0,false,dt); T.physStep(dt,P); if(fn&&fn()) return i; } return n; };
   // every bridge: on foot and by buggy, from one end to the other on the deck
   out.walk=[]; out.drive=[]; out.under=[];
   for(const B of W.bridges){ const p=B.rd.pts, a=p[Math.max(0,B.q0-5)], e=p[Math.min(p.length-1,B.q1+5)], mid=p[Math.round((B.q0+B.q1)/2)], wl=W.RVY[Math.round((mid[1]+832)/2)*W.N+Math.round((mid[0]+832)/2)];
     const ax=S[0]+a[0], az=S[2]+a[1], ex=S[0]+e[0], ez=S[2]+e[1], yaw=Math.atan2(-(ex-ax),-(ez-az));
     const qa=Math.max(0,B.q0-5), qe=Math.min(p.length-1,B.q1+5); let tq=qa+1; const aim=(x,z)=>{ while(tq<qe&&Math.hypot(S[0]+p[tq][0]-x,S[2]+p[tq][1]-z)<2.5) tq++; return Math.atan2(-(S[0]+p[tq][0]-x),-(S[2]+p[tq][1]-z)); };
     place(ax,a[2]+0.2,az,yaw); let minY=1e9; const steps=walk(900,()=>{ if(Math.hypot(P.pos.x-(S[0]+mid[0]),P.pos.z-(S[2]+mid[1]))<8&&P.pos.y<minY) minY=P.pos.y; P.yaw=aim(P.pos.x,P.pos.z); return Math.hypot(P.pos.x-ex,P.pos.z-ez)<1.5; });
     out.walk.push({ok:steps<900&&minY>wl+1.5,steps,over:+(minY-wl).toFixed(2),deck:+(mid[2]-wl).toFixed(2)});
     const k=T.karts[0]; Object.assign(k,{x:ax,z:az,y:a[2]+0.1,yaw,vx:0,vz:0,vf:0,air:false}); let kMin=1e9, got=false;
     tq=qa+1; for(let i=0;i<600&&!got;i++){ const want=aim(k.x,k.z); let dy=((want-k.yaw+Math.PI*3)%(Math.PI*2))-Math.PI; T.simKart(k,{fw:Math.abs(k.vf)>7?0.2:1,st:Math.max(-1,Math.min(1,-dy*2)),hb:false},dt); if(Math.hypot(k.x-(S[0]+mid[0]),k.z-(S[2]+mid[1]))<8&&k.y<kMin) kMin=k.y; got=Math.hypot(k.x-ex,k.z-ez)<3; }
     out.drive.push({ok:got&&kMin>wl+1.4,over:+(kMin-wl).toFixed(2)});
     // and under it, along the river (the main river only: the streams are too shallow to stand in under a deck)
     const rv=W.rivers[0]; let bi=-1, bd=1e9; rv.pts.forEach((q,i)=>{ const d=Math.hypot(q[0]-mid[0],q[1]-mid[1]); if(d<bd){ bd=d; bi=i; } });
     if(bd<6&&bi>10&&bi<rv.pts.length-10){ const u0=rv.pts[bi-7], u1=rv.pts[bi+7], x0=S[0]+u0[0], z0=S[2]+u0[1], x1=S[0]+u1[0], z1=S[2]+u1[1]; place(x0,T.terrainH(x0,z0)+0.05,z0,Math.atan2(-(x1-x0),-(z1-z0)));
       let top=-1e9, st=700, lx=P.pos.x, lz=P.pos.z, side=0; for(let i=0;i<700;i++){ P.yaw=Math.atan2(-(x1-P.pos.x),-(z1-P.pos.z)); T.moveBody(P,1,side,false,dt); T.physStep(dt,P); if(P.pos.y>top) top=P.pos.y;
         if(i%30===29){ side=Math.hypot(P.pos.x-lx,P.pos.z-lz)<0.5?(side>0?-1:1):0; lx=P.pos.x; lz=P.pos.z; } if(Math.hypot(P.pos.x-x1,P.pos.z-z1)<1.5){ st=i; break; } }
       out.under.push({ok:st<700&&top<wl+0.6,steps:st,top:+(top-wl).toFixed(2)}); } }
   // wading is slower than running
   { const rv=W.rivers[0], q=rv.pts[400], q2=rv.pts[430], x=S[0]+q[0], z=S[2]+q[1]; place(x,T.terrainH(x,z)+0.02,z,Math.atan2(-(q2[0]-q[0]),-(q2[1]-q[1]))); walk(30); const x0=P.pos.x, z0=P.pos.z; walk(60); out.wade=+(Math.hypot(P.pos.x-x0,P.pos.z-z0)).toFixed(2); out.run=T.RUN; out.depth=+(T.waterAt(x,z)-T.terrainH(x,z)).toFixed(2); }
   out.wetProps=T.props.filter(p=>p.alive&&!p.gone&&T.waterAt(p.x,p.z)>-999).length;
   out.decks=T.STATICS.filter(s=>s.solid.key.startsWith('deck')).length;
   return out; });
 const ok=r.rivers>=3&&r.mainLen>1500&&r.bridges>=2&&r.rises===0&&r.dry===0&&r.maxDepth<1.31&&r.walk.every(w=>w.ok)&&r.drive.every(w=>w.ok)&&r.under.length>=1&&r.under.every(w=>w.ok)&&r.wade<r.run*0.85&&r.wade>1&&r.wetProps===0&&r.decks>20;
 console.log(JSON.stringify(r)); console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

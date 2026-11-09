// house stairs: you can't step off the open side through the handrail
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,TOWNS,houseStair,physStep,moveBody,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.getElementById('play').click(); }); await sleep(2000);
 const r=await pg.evaluate(()=>{ const out=[]; let n=0;
   for(const t of T.TOWNS) for(const h of t.houses){ if(h.floors<2||n>=4) continue; n++; const S=T.houseStair(h), bx=S.stairs.boxes; // steps are boxes 1..20 (0 is the landing)
     const st=bx[10], cx=(st[0]+st[3])/2, cz=(st[2]+st[5])/2; // a middle step
     // which way is the open side? the handrail boxes are the last ones: step from the stair toward the nearest rail box
     const rail=bx[bx.length-10], rx=(rail[0]+rail[3])/2-cx, rz=(rail[2]+rail[5])/2-cz, X=Math.abs(rx)>Math.abs(rz);
     const dir=X?[Math.sign(rx),0]:[0,Math.sign(rz)];
     T.P.pos.set(cx,st[4],cz); T.P.vel.set(0,0,0); T.P.onGround=true; T.P.sky=null; const y0=st[4];
     T.P.yaw=Math.atan2(-dir[0],-dir[1]); for(let i=0;i<90;i++){ T.moveBody(T.P,1,0,false,1/60); T.physStep(1/60); }
     out.push({drop:+(y0-T.P.pos.y).toFixed(2),moved:+Math.hypot(T.P.pos.x-cx,T.P.pos.z-cz).toFixed(2)}); }
   return out; });
 console.log(JSON.stringify(r)); console.log(r.length&&r.every(o=>o.drop<0.5&&o.moved<1.6)?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

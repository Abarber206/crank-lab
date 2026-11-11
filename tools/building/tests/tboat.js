// boats: moored on the sea and rivers; you get in and drive (top speed, turning), it never goes up onto land (it runs
// aground and stops), and getting out in deep water leaves you swimming. node tboat.js [shots-prefix]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const shots=process.argv[2]; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,waterAt,waterDepth,boatDepth,camera,karts,enterKart,exitKart,SPAWN,RUN,BOAT_MIN'),shots?{vp:{width:900,height:560}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const info=await pg.evaluate(()=>{ const bs=T.karts.filter(k=>k.boat); return {n:bs.length,boats:bs.map(k=>({id:k.id,x:+k.x.toFixed(1),z:+k.z.toFixed(1),dep:+T.boatDepth(k.x,k.z,k.yaw).toFixed(2),wd:+T.waterDepth(k.x,k.z).toFixed(2),fromSpawn:Math.round(Math.hypot(k.x-T.SPAWN[0],k.z-T.SPAWN[2]))}))}; });
 console.log(JSON.stringify(info));
 // the deepest-water boat for the drive
 const opens=await pg.evaluate(()=>T.karts.filter(k=>k.boat).map(k=>{ let best=0; for(let q=0;q<24;q++){ const a=q/24*Math.PI*2; let d=0; for(let s=2;s<160;s+=2){ const x=k.x-Math.sin(a)*s, z=k.z-Math.cos(a)*s; if(T.boatDepth(x,z,a)<0.5||Math.hypot(x-T.SPAWN[0],z-T.SPAWN[2])>800) break; d=s; } best=Math.max(best,d); } return [k.id,best]; }));
 console.log('open water',JSON.stringify(opens)); const pick={id:opens.sort((a,b)=>b[1]-a[1])[0][0]};
 if(shots){ await pg.evaluate(id=>{ const k=T.karts[id]; T.P.pos.set(k.x+Math.cos(k.yaw)*4,T.terrainH(k.x,k.z)+40,k.z-Math.sin(k.yaw)*4); window.__hold=1; const R=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera&&window.__hold){ const k=T.karts[id]; c.position.set(k.x+Math.cos(k.yaw+0.6)*6.5,k.y+2.6,k.z-Math.sin(k.yaw+0.6)*6.5); c.lookAt(k.x,k.y+0.4,k.z); c.updateMatrixWorld(); } R(s,c); }; },pick.id); await sleep(2500); await pg.screenshot({path:shots+'_moored.png',timeout:200000}); await pg.evaluate(()=>{ window.__hold=0; }); }
 const r=await pg.evaluate(async(id)=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms)), o={}, k=T.karts[id];
   T.P.pos.set(k.x,k.y,k.z); T.P.vel.set(0,0,0); T.enterKart(k,0); o.inBoat=!!(T.P.kart&&T.P.kart.k===k); o.y0=+(k.y-T.waterAt(k.x,k.z)).toFixed(2); return o; },pick.id);
 // drive: full throttle out, then a turn, then straight at the shore
 await pg.evaluate(id=>{ const k=T.karts[id]; let best=null; for(let q=0;q<24;q++){ const a=q/24*Math.PI*2; let d=0; for(let s=2;s<160;s+=2){ const x=k.x-Math.sin(a)*s, z=k.z-Math.cos(a)*s; if(T.boatDepth(x,z,a)<0.5||Math.hypot(x-T.SPAWN[0],z-T.SPAWN[2])>800) break; d=s; } if(!best||d>best.d) best={a,d}; } k.yaw=best.a; T.P.yaw=best.a; window.__open=best.d; },pick.id);
 await pg.keyboard.down('KeyW'); let top=0; for(let i=0;i<14;i++){ await sleep(500); const v=await pg.evaluate(id=>Math.hypot(T.karts[id].vx,T.karts[id].vz),pick.id); top=Math.max(top,v); }
 if(shots){ await pg.screenshot({path:shots+'_drive.png',timeout:200000}); }
 const y0=await pg.evaluate(id=>T.karts[id].yaw,pick.id); await pg.keyboard.down('KeyA'); await sleep(1500); await pg.keyboard.up('KeyA'); const y1=await pg.evaluate(id=>T.karts[id].yaw,pick.id);
 // aim at the nearest shore and hold full throttle for a while: it must stay afloat
 await pg.evaluate(id=>{ const k=T.karts[id]; let best=null; for(let q=0;q<36;q++){ const a=q/36*Math.PI*2; for(let s=2;s<200;s+=2){ if(T.waterDepth(k.x-Math.sin(a)*s,k.z-Math.cos(a)*s)<0.05){ if(!best||s<best.s) best={a,s}; break; } } } k.yaw=best.a; window.__shore=best.s; },pick.id);
 let minDep=99, landed=false; for(let i=0;i<24;i++){ await sleep(500); const s=await pg.evaluate(id=>{ const k=T.karts[id]; return [T.boatDepth(k.x,k.z,k.yaw),T.waterAt(k.x,k.z)<-999||T.waterDepth(k.x,k.z)<0.05]; },pick.id); minDep=Math.min(minDep,s[0]); if(s[1]) landed=true; }
 await pg.keyboard.up('KeyW');
 // back out into deep water and get out: swimming
 await pg.evaluate(id=>{ const k=T.karts[id]; let best=null; for(let s=0;s<400000&&!best;s++){ const a=s*2.399, d=(s%3000)*0.1, x=k.x+Math.cos(a)*d, z=k.z+Math.sin(a)*d; if(T.boatDepth(x,z,k.yaw)>2.2) best=[x,z]; } if(best){ k.x=best[0]; k.z=best[1]; k.vx=k.vz=0; } },pick.id);
 await sleep(800); await pg.evaluate(()=>T.exitKart(true)); await sleep(1500); const after=await pg.evaluate(()=>({kart:!!T.P.kart,swim:!!T.P.swim}));
 const res={...r,top:+top.toFixed(1),turned:+Math.abs(y1-y0).toFixed(2),shore:await pg.evaluate(()=>window.__shore),minDep:+minDep.toFixed(2),landed,...after}; console.log(JSON.stringify(res));
 const ok=info.n>=4&&info.boats.every(b=>b.dep>=0.3)&&res.inBoat&&res.top>9&&res.turned>0.4&&!landed&&minDep>0.2&&!res.kart&&res.swim;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

// walking into each town's landmark from four sides: you are stopped at its wall (or step up on to its platform), never inside it
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,TOWNS,physStep,settings,terrainH'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS,null,{timeout:120000});
 const r=await pg.evaluate(()=>{ const out=[]; T.TOWNS.forEach((t,k)=>{ const L=t.poi; if(!L) return; const row=[k]; for(let q=0;q<4;q++){ const a=q*Math.PI/2+0.2, sx=Math.cos(a), sz=Math.sin(a); T.P.pos.set(L.x+sx*10,T.terrainH(L.x+sx*10,L.z+sz*10)+0.05,L.z+sz*10); T.P.sky=null; T.P.vel.set(0,0,0); T.P.onGround=true;
     for(let n=0;n<500;n++){ T.P.vel.x=-sx*5; T.P.vel.z=-sz*5; T.physStep(1/120,T.P); } row.push(+Math.hypot(T.P.pos.x-L.x,T.P.pos.z-L.z).toFixed(1),+(T.P.pos.y-(L.y!=null?L.y:t.h)).toFixed(1)); } out.push(row); }); return out; });
 console.log(JSON.stringify(r)); console.log(errs.join('\n')||'no errors'); await b.close(); })();

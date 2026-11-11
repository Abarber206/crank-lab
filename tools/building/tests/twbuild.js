// building in water: aimed from the water, walls, floors and stairs start on the bed (below level 0) and rise out of
// the water; on land nothing changes (level 0 is still the lowest)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,settings,waterAt,waterDepth,terrainH,SPAWN,computeTargetRaw,buildFloor,LVL'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const S=T.SPAWN, out={}; let sp=null;
   for(let k=0;k<400000&&!sp;k++){ const a=k*2.399, d=600+(k%4000)*0.055, x=S[0]+Math.cos(a)*d, z=S[2]+Math.sin(a)*d; if(T.waterDepth(x,z)>2&&T.waterDepth(x,z)<4&&T.waterDepth(x+6,z)>1.5&&T.waterDepth(x-6,z)>1.5&&T.waterDepth(x,z+6)>1.5&&T.waterDepth(x,z-6)>1.5) sp={x,z}; }
   const w=T.waterAt(sp.x,sp.z); T.P.pos.set(sp.x,w-1.3,sp.z); T.P.vel.set(0,0,0); T.P.onGround=true; await new Promise(r=>setTimeout(r,600)); T.P.pitch=-0.1;
   for(const ty of ['wall','floor','ramp']){ const t=T.computeTargetRaw(ty,T.P); const cx=(t.i+.5)*5, cz=(t.j+.5)*5; out[ty]={l:t.l,base:t.l*T.LVL,top:(t.l+1)*T.LVL,bed:+T.terrainH(cx,cz).toFixed(2),water:w}; }
   T.P.pos.set(S[0],T.terrainH(S[0],S[2]),S[2]); T.P.onGround=true; await new Promise(r=>setTimeout(r,400)); out.land=T.computeTargetRaw('wall',T.P).l; return out; });
 console.log(JSON.stringify(r)); const w=r.wall; const ok=w.l<0&&w.base<=w.bed+0.3&&w.top>w.water&&r.ramp.l<0&&r.floor.base>=r.floor.bed-0.2&&r.land>=0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

// the island's edge: walkers are held at the cliff top; a swimmer near the lagoon's mouth is carried over the falls and eliminated
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,WGEN,SPAWN,terrainH,waterAt'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.P&&T.WGEN,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); }); await sleep(5000);
 const S=await pg.evaluate(()=>{ const S=T.WGEN.sea(); return Math.atan2(S.nz,S.nx); });
 for(const [name,a] of [['land',S+2.2],['land2',S-1.6]]){
   await pg.evaluate(a=>{ const C=T.SPAWN, e=T.WGEN.edgeR(Math.cos(a)*800,Math.sin(a)*800)-12, x=C[0]+Math.cos(a)*e, z=C[2]+Math.sin(a)*e; T.P.pos.set(x,Math.max(T.terrainH(x,z),T.waterAt(x,z))+0.2,z); T.P.vel&&T.P.vel.set(0,0,0); T.P.yaw=-Math.atan2(Math.cos(a),-Math.sin(a)); window._a=a; },a);
   // push outward every frame for 6 s
   const t0=Date.now(); let mx=0, y=0;
   while(Date.now()-t0<6000){ const r=await pg.evaluate(()=>{ const a=window._a, C=T.SPAWN; T.P.pos.x+=Math.cos(a)*0.6; T.P.pos.z+=Math.sin(a)*0.6; const u=T.P.pos.x-C[0], v=T.P.pos.z-C[2]; return [Math.hypot(u,v)-T.WGEN.edgeR(u,v),T.P.pos.y]; }); mx=Math.max(mx,r[0]); y=r[1]; await sleep(50); }
   const fin=await pg.evaluate(()=>{ const C=T.SPAWN, u=T.P.pos.x-C[0], v=T.P.pos.z-C[2]; return [Math.hypot(u,v)-T.WGEN.edgeR(u,v),T.P.pos.y,T.P.hp]; });
   console.log(name,'max past edge (before clamp)',mx.toFixed(2),'final',fin.map(x=>+(+x).toFixed(2)).join(' '), fin[0]<0.5&&fin[1]>-20?'OK':'FAIL'); }
 for(const off of [0.05,-0.1]){ await pg.evaluate(a=>{ const C=T.SPAWN, e=T.WGEN.edgeR(Math.cos(a)*800,Math.sin(a)*800)-22, x=C[0]+Math.cos(a)*e, z=C[2]+Math.sin(a)*e; T.P.pos.set(x,T.waterAt(x,z)-0.6,z); T.P.vel.set(0,0,0); T.P.hp=100; T.P.overFalls=false; },S+off);
   const tr=[]; for(let i=0;i<40;i++){ await sleep(500); const r=await pg.evaluate(()=>{ const C=T.SPAWN, u=T.P.pos.x-C[0], v=T.P.pos.z-C[2]; return [+(Math.hypot(u,v)-T.WGEN.edgeR(u,v)).toFixed(1),+T.P.pos.y.toFixed(1),T.P.hp,!!T.P.swim,!!T.P.overFalls]; }); tr.push(r.join('/')); if(r[2]<=0) break; }
   console.log('lagoon',off,tr.filter((x,i)=>i%3==0||i==tr.length-1).join('  ')); const hp=+tr[tr.length-1].split('/')[2]; console.log(hp<=0?'swimmer went over and was eliminated OK':'FAIL swimmer survived'); await sleep(4000); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

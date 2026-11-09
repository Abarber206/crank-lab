const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,karts,simKart,enterKart,stepKarts,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.karts,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(()=>{ const k=T.karts[0]; T.P.pos.set(k.x+1.5,k.y,k.z); T.enterKart(k,0); const out={hp0:k.hp};
   // ram the garage's back wall over and over
   for(let n=0;n<14&&!k.dead;n++){ Object.assign(k,{x:k.home.x,z:k.home.z,y:k.home.y,yaw:k.home.yaw,vx:Math.sin(k.home.yaw)*16,vz:Math.cos(k.home.yaw)*16}); for(let i=0;i<40;i++) T.simKart(k,{fw:0,st:0,hb:false},1/60); }
   out.hp=k.hp; out.dead=k.dead>0; out.thrown=!T.P.kart; return out; });
 console.log(JSON.stringify(r), r.dead&&r.thrown?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

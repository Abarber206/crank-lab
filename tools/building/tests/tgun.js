const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,gunTakes,renderGun,GUN_SND,audioInit,sfx'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.GUN_SND,null,{timeout:120000});
 const r=await pg.evaluate(async()=>{ T.audioInit(); const out={}; await new Promise(r=>setTimeout(r,3500)); out.warm={n:Object.values(T.gunTakes).reduce((a,t)=>a+t.length,0)}; for(const k in T.GUN_SND){ const t0=performance.now(); const bf=T.renderGun(T.GUN_SND[k]); const ms=performance.now()-t0; const d=bf.getChannelData(0); let nan=0,pk=0; for(const v of d){ if(!isFinite(v)) nan++; pk=Math.max(pk,Math.abs(v)); }
   const step=4; out[k]={ms:+ms.toFixed(1),dur:bf.duration,nan,pk:+pk.toFixed(2),sr:bf.sampleRate,data:Array.from(d.filter((_,i)=>i%step===0)).map(v=>Math.round(v*32767))}; T.sfx(k); } return out; });
 for(const k in r){ const {data,...m}=r[k]; console.log(k,JSON.stringify(m)); fs.writeFileSync('gun_'+k+'.json',JSON.stringify({sr:r[k].sr/4,data})); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

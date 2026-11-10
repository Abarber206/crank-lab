// every dance song plays all four bars without an error, and a beat is cheap to schedule
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,audioInit,emoteBeat,SONGS,EMOTES'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.SONGS,null,{timeout:120000});
 const r=await pg.evaluate(async()=>{ T.audioInit(); await new Promise(r=>setTimeout(r,300)); const out={}; for(const id in T.SONGS){ const S=T.SONGS[id]; let bad=0; for(const k of ['k','s','h']) for(const p of S[k]) if(p.length!==16) bad++; for(const k of ['bass','lead']) for(const p of S[k].n) if(p.length!==16) bad++; for(const p of S.chord.r) if(p.length!==16) bad++; if(S.chord.c.length!==4) bad++;
     const t0=performance.now(); for(let q=0;q<16;q++) T.emoteBeat(id,q); out[id]={bad,ms:+((performance.now()-t0)/16).toFixed(2),dance:!!T.EMOTES[id].beat}; await new Promise(r=>setTimeout(r,150)); } return out; });
 const ok=Object.values(r).every(v=>v.bad===0&&v.ms<8&&v.dance)&&Object.keys(r).length===6;
 console.log(JSON.stringify(r), ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

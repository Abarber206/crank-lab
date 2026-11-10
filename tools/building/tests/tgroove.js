const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,emoteBeat,audioInit,GROOVE,EMOTES'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.GROOVE,null,{timeout:120000});
 const n=await pg.evaluate(()=>{ T.audioInit(); let c=0; for(const id in T.GROOVE){ if(!T.EMOTES[id]) throw new Error('no emote '+id); for(let b=0;b<16;b++){ T.emoteBeat(id,b); c++; } } return c; });
 console.log(n, errs.join('\n')||'no errors'); await b.close(); })();

// the frame-rate guard: slow frames first lower the resolution; only when that is spent are the extras shed, one at a time
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,stepDynRes,dynRes,PERF,settings'),{fast:false,norender:true});
 await pg.waitForFunction(()=>window.T&&T.PERF,null,{timeout:120000});
 const r=await pg.evaluate(()=>{ const out=[], feed=(ms,n)=>{ for(let q=0;q<n;q++) T.stepDynRes(ms,performance.now()); }; T.settings.autoRes=true; T.settings.reflect=true; T.settings.ao=true;
   Object.assign(T.PERF,{reflect:true,ao:true,far:true,slow:0}); T.dynRes.acc=0; T.dynRes.n=0;
   feed(15,400); out.push([T.PERF.reflect,T.PERF.ao,T.PERF.far]);                 // smooth: nothing happens
   for(let w=0;w<12&&T.dynRes.cur>T.dynRes.min+1e-3;w++) feed(40,51); out.push([T.PERF.reflect,T.PERF.ao,T.PERF.far,T.dynRes.cur<=T.dynRes.min+1e-3]); // slow: resolution goes first
   feed(40,102); out.push([T.PERF.reflect,T.PERF.ao,T.PERF.far]); feed(40,102); out.push([T.PERF.reflect,T.PERF.ao,T.PERF.far]); feed(40,102); out.push([T.PERF.reflect,T.PERF.ao,T.PERF.far]);
   out.push([T.settings.reflect,T.settings.ao]); return out; });
 const j=JSON.stringify(r), ok=r[0].every(v=>v)&&r[1][0]&&r[1][3]&&!r[2][0]&&r[4].filter(v=>!v).length>=2&&r[5][0]===true&&r[5][1]===true;
 console.log(j, ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

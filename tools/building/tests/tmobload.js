// phone start-up: where the time goes while the page loads to the lobby (touch device, 390x844 @3x), how many WebGL
// contexts get made, and the GPU memory (textures) in use
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); let html=page('/home/claude/crank-lab/index.html','scene,renderer,INDOOR');
 html=html.replace('<script>\n','<script>\nwindow.__ctx=0; window.__t0=performance.now(); { const gc=HTMLCanvasElement.prototype.getContext; HTMLCanvasElement.prototype.getContext=function(t,a){ if(/webgl/.test(t)&&!this.__c){ this.__c=1; window.__ctx++; (window.__ctxLog=window.__ctxLog||[]).push([Math.round(performance.now()-window.__t0),this.width+"x"+this.height,new Error().stack.split("\\n")[2].trim().slice(0,90)]); } return gc.call(this,t,a); }; }\n');
 let cdp; const {pg,errs}=await open(b,html,{vp:{width:390,height:844},ctx:{hasTouch:true,isMobile:true,deviceScaleFactor:3},before:async pg=>{ cdp=await pg.context().newCDPSession(pg); await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval',{interval:1000}); await cdp.send('Profiler.start'); }});
 const t0=Date.now(); await pg.waitForFunction(()=>window.T&&T.renderer&&T.INDOOR&&T.INDOOR.tex,null,{timeout:300000}); const tReady=Date.now()-t0; await sleep(6000);
 const {profile}=await cdp.send('Profiler.stop');
 // self time by function, top 25
 const self=new Map(), byId=new Map(profile.nodes.map(n=>[n.id,n])); const dt=profile.timeDeltas; profile.samples.forEach((id,i)=>{ const n=byId.get(id), k=n.callFrame.functionName||'(anon)'; self.set(k,(self.get(k)||0)+(dt[i]||0)/1000); });
 // inclusive time for named functions
 const parent=new Map(); profile.nodes.forEach(n=>(n.children||[]).forEach(c=>parent.set(c,n.id))); const incl=new Map(); profile.samples.forEach((id,i)=>{ const seen=new Set(); let x=id; while(x!=null){ const k=byId.get(x).callFrame.functionName; if(k&&!seen.has(k)){ seen.add(k); incl.set(k,(incl.get(k)||0)+(dt[i]||0)/1000); } x=parent.get(x); } });
 const info=await pg.evaluate(()=>({ctx:window.__ctx,log:window.__ctxLog,mem:T.renderer.info.memory,prog:T.renderer.info.programs.length,isTouch:matchMedia('(pointer: coarse)').matches}));
 console.log('ready',tReady,'ms',JSON.stringify(info,null,0));
 console.log('INCLUSIVE'); [...incl].sort((a,b)=>b[1]-a[1]).slice(0,40).forEach(([k,v])=>console.log(v.toFixed(0).padStart(7),k));
 console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

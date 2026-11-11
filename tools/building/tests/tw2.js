const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,TOWNS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 const r=await pg.evaluate(process.argv[2]); console.log(JSON.stringify(r)); console.log(errs.join('\n')||'no errors'); await b.close(); })();

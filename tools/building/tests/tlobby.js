const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const tag=process.argv[2]||'a';
 for(const [nm,vp] of [['desk',{width:1280,height:760}],['phone',{width:390,height:780}],['land',{width:844,height:390}]]){
  const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer'),{vp});
  await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(5000);
  await pg.screenshot({path:`lb_${tag}_${nm}.png`});
  if(nm==='desk'){ await pg.click('[data-tab=shop]'); await sleep(800); await pg.screenshot({path:`lb_${tag}_shop.png`}); await pg.click('[data-tab=play]'); await sleep(500);
    const st=await pg.evaluate(()=>({lobby:document.getElementById('menu').className, canvasW:document.getElementById('stageC').width})); console.log(JSON.stringify(st)); }
  console.log(nm,errs.join('\n')||'no errors'); await pg.context().close(); }
 await b.close(); })();

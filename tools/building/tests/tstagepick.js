// the Locker/Item Shop pickaxe preview: the hero on the stage rests the pickaxe over the shoulder.  node tstagepick.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/sp'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,settings'),{vp:{width:1100,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(2500);
 await pg.evaluate(()=>document.querySelector('button[data-tab=locker]').click()); await sleep(500);
 for(const id of ['steel','bone']){ await pg.evaluate(id=>{ window._stageLook={pk:id}; window._stagePrev=null; window._stagePickT=performance.now()+60000; },id); await sleep(2500); await pg.screenshot({path:pre+'_'+id+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

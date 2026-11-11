// locker preview pictures: node tlocker.js out-prefix  (Drift outfit; pickaxe just picked and 1 s later; salute; groove)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/lk'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,settings'),{vp:{width:1200,height:760}});
 await pg.waitForFunction(()=>window.T&&T.scene,null,{timeout:180000}); await sleep(2000);
 await pg.evaluate(()=>document.querySelector('.mtabs button[data-tab=locker]').click()); await sleep(1500);
 const cards=await pg.evaluate(()=>({o:[...document.querySelectorAll('#outfits > *')].map(e=>e.textContent.trim().slice(0,20)),p:[...document.querySelectorAll('#picks > *')].map(e=>e.textContent.trim().slice(0,20)),e:[...document.querySelectorAll('#emotesBox > *')].map(e=>e.textContent.trim().slice(0,20))}));
 console.log(JSON.stringify(cards));
 const oi=cards.o.findIndex(t=>/drift/i.test(t)); if(oi>=0) await pg.evaluate(i=>document.querySelectorAll('#outfits > *')[i].click(),oi); await sleep(800);
 const bb=await pg.evaluate(()=>{ const r=document.getElementById('stage').getBoundingClientRect(); return {x:Math.max(0,r.x),y:Math.max(0,r.y),width:Math.min(r.width,1200-r.x),height:Math.min(r.height,760-Math.max(0,r.y))}; }); const stage={screenshot:o=>pg.screenshot({path:o.path,clip:bb,timeout:120000})};
 await pg.evaluate(()=>document.querySelectorAll('#picks > *')[0].click()); await sleep(250); await stage.screenshot({path:pre+'_pick0.png'}); await sleep(900); await stage.screenshot({path:pre+'_pick1.png'});
 for(const nm of (process.env.EMOTES||'salute,groove,wave,cheer,hype').split(',')){ const ei=cards.e.findIndex(t=>t.toLowerCase().includes(nm)); if(ei<0) continue; await sleep(3500); await pg.evaluate(i=>document.querySelectorAll('#emotesBox > *')[i].click(),ei); for(const t of (process.env.TS||'0.8,1.6').split(',')){ await sleep(+t*1000-(t==='0.8'?0:800)); await stage.screenshot({path:pre+'_'+nm+'_'+t+'.png'}); } }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

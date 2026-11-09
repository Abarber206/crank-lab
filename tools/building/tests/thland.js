// solo horde: you drop in with no guns, and the first countdown holds until you land
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,horde,settings,renderer'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(4000);
 const a=await pg.evaluate(()=>({sky:!!T.P.sky,t:T.horde.t,land:T.horde.land,guns:T.P.inv.filter(Boolean),wave:T.horde.wave}));
 await pg.waitForFunction(()=>!T.P.sky,null,{timeout:120000}); await sleep(3000);
 const c=await pg.evaluate(()=>({sky:!!T.P.sky,t:T.horde.t,land:T.horde.land,guns:T.P.inv.filter(Boolean)}));
 console.log(JSON.stringify(a),JSON.stringify(c));
 console.log(a.sky&&a.t>=19.9&&a.land&&!a.guns.length&&!c.land&&c.t<19.5&&!c.guns.length?'PASS':'FAIL');
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

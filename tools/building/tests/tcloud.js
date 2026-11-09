// the cloud intro on the first drop: white, then the clouds rush up and part to show the island; drops land at different spots
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,randomDropSpot,SPAWN'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(100); console.log(await pg.evaluate(()=>{ const e=document.getElementById('cloudFx'); const cs=getComputedStyle(e); return JSON.stringify({hidden:e.hidden,cls:e.className,op:cs.opacity,disp:cs.display,z:cs.zIndex,kids:e.children.length,ever:T.P.everPlayed}); }));
 for(const [n,t] of [['1',150],['2',800],['3',1400],['4',1900]]){ await pg.evaluate(t=>{ const el=document.getElementById('cloudFx'); clearTimeout(0); el.hidden=false; el.classList.add('go'); document.getAnimations().forEach(a=>{ a.pause(); a.currentTime=t; }); },t); await pg.screenshot({path:'cl_'+n+'.png'}); }
 const r=await pg.evaluate(()=>{ const s=[]; for(let i=0;i<30;i++) s.push(T.randomDropSpot()); const far=s.filter(p=>Math.hypot(p[0]-T.SPAWN[0],p[1]-T.SPAWN[2])>100).length;
   return {sky:!!T.P.sky,pos:[Math.round(T.P.pos.x),Math.round(T.P.pos.z)],far,uniq:new Set(s.map(p=>Math.round(p[0]/50)+','+Math.round(p[1]/50))).size,overlay:document.getElementById('cloudFx').hidden}; });
 console.log(JSON.stringify(r), r.sky&&r.far>15&&r.uniq>20?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

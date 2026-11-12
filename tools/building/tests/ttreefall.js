// a chopped tree tips over, lands, and sinks away (never shrinks), then grows back normally.  node ttreefall.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,P,camera,settings,TOD,props,terrainH,propBreak,propRevive,stepForest'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.props,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode=fight]').click(); document.querySelector('#play').click(); }); await sleep(8000);
 const id=await pg.evaluate(()=>{ const t=T.props.find(p=>p.kind==='tree'&&p.alive&&!T.props.some(q=>q!==p&&q.alive&&Math.hypot(q.x-p.x,q.z-p.z)<9)); T.P.pos.set(t.x-9,T.terrainH(t.x-9,t.z)+0.1,t.z); window.__t=t; return t.id; });
 await sleep(3000); await pg.evaluate(()=>{ window.__s=[]; T.propBreak(window.__t,true); const t0=performance.now(); const iv=setInterval(()=>{ const t=window.__t; window.__s.push([performance.now()-t0,t.g.scale.x,t.g.position.y-t.base,t.g.quaternion.x,t.g.quaternion.z,t.g.visible]); if(performance.now()-t0>2700) clearInterval(iv); },30); });
 await sleep(2900);
 await sleep(1500); const r=await pg.evaluate(()=>{ const s=window.__s, t=window.__t; const minScale=Math.min(...s.map(x=>x[1])); T.propRevive(t); return {frames:s.length,minScale:+minScale.toFixed(3),s:t.s,maxTilt:+Math.max(...s.map(x=>Math.hypot(x[3],x[4]))).toFixed(2),sank:+Math.min(...s.map(x=>x[2])).toFixed(2),hidden:!s[s.length-1][5],alive:t.alive,rot:[t.g.rotation.x,t.g.rotation.z].map(v=>+v.toFixed(3)),y:+(t.g.position.y-t.base).toFixed(3)}; });
 console.log(JSON.stringify(r)); const ok=Math.abs(r.minScale-r.s)<0.01&&r.maxTilt>0.6&&r.sank<-0.5&&r.alive&&r.rot.every(v=>v===0)&&r.y===0; console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

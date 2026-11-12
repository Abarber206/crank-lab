// close-up pictures of the Locker stage hero (front, three-quarter, side, back, face) for judging the body and lighting.
// OUTFIT=id to pick one.  FILE=... node thero.js out-prefix
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/hr'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,settings,saveSettings,get _stage(){return _stage}'),{vp:{width:1500,height:1100}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(2500);
 if(process.env.OUTFIT) await pg.evaluate(o=>{ T.settings.outfit=o; }, process.env.OUTFIT);
 await pg.evaluate(()=>document.querySelector('button[data-tab=locker]').click()); await sleep(1500);
 await pg.evaluate(()=>{ window._stagePickT=0; const S=T._stage, R=S.r.render.bind(S.r); window.__v=null; S.r.render=(sc,cam)=>{ const v=window.__v; if(v&&S.heroes[0]){ const p=S.heroes[0].pos, y=(S.heroes[0].yaw||0)+v.a; cam.position.set(p.x-Math.sin(y)*v.d,p.y+v.h,p.z-Math.cos(y)*v.d); cam.lookAt(p.x,p.y+v.t,p.z); cam.fov=v.f||30; cam.updateProjectionMatrix(); } R(sc,cam); }; });
 const V={front:{a:0,d:4.6,h:1.0,t:0.95},tq:{a:Math.PI*0.25,d:2.4,h:1.35,t:1.25},side:{a:Math.PI*0.5,d:4.6,h:1.0,t:0.95},back:{a:Math.PI,d:4.6,h:1.0,t:0.95},face:{a:Math.PI*0.12,d:1.1,h:1.62,t:1.58}};
 for(const k of (process.env.VIEWS||'front,tq,side,back,face').split(',')){ await pg.evaluate(v=>{ window.__v=v; },V[k]); await sleep(1500); const el=await pg.$('#stageC'); await el.screenshot({path:pre+'_'+k+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

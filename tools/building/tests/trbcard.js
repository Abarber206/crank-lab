const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,RB,onRb,renderer,settings,camera'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 await pg.evaluate(()=>{ const p=T.P.pos; T.onRb({op:'card',id:'x1',n:'Buddy',t:0,o:2,p:[p.x+6,p.y,p.z-6],ttl:100}); const c=T.RB.cards.get('x1');
   window.cam=new THREE.PerspectiveCamera(45,900/520,0.05,3000); const Rr=T.renderer.render.bind(T.renderer); T.renderer.render=(s,cc)=>Rr(s,cc===T.camera?cam:cc);
   cam.position.set(c.x+0.4,c.y+1.5,c.z+2.4); cam.lookAt(c.x,c.y+1.3,c.z); });
 for(const [n,t] of [['a',600],['b',1400]]){ await sleep(t); await pg.screenshot({path:'rbc_'+n+'.png'}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

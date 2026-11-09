const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,horde,newZombie'),{vp:{width:1000,height:580}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.settings.hordeBot=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.querySelector('.mode[data-mode=horde]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 await pg.evaluate(()=>{ T.P.yaw=0.5; T.P.pitch=0; T.P.hp=1e6; const p=T.P.pos, f=[-Math.sin(T.P.yaw),-Math.cos(T.P.yaw)]; ['husk','runner','brute','hurler'].forEach((t,i)=>T.newZombie(t,p.x+f[0]*9+(i-1.5)*2.2*f[1],p.z+f[1]*9-(i-1.5)*2.2*f[0])); });
 for(const [n,t] of [['rise',700],['near',6000],['close',5000]]){ await sleep(t); await pg.evaluate(()=>{ T.P.hp=1e6; T.P.sh=100; }); await pg.screenshot({path:'zv_'+n+'.png'}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

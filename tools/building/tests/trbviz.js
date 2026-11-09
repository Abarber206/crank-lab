// screenshots: a reboot card, a reboot van, and the knocked crawl pose
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,RB,VANS,onRb,renderer,settings,localHero,net,camera'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.VANS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 const shot=async(nm,fn)=>{ await pg.evaluate(fn); await sleep(2500); await pg.screenshot({path:nm}); };
 await pg.evaluate(()=>{ const p=T.P.pos; T.onRb({op:'card',id:'x1',n:'Buddy',t:0,o:2,p:[p.x,p.y,p.z-3.2],ttl:100}); T.P.yaw=0; T.P.pitch=0.05; });
 await shot('rbv_card.png',()=>{ T.P.yaw=0; });
 //await shot('rbv_beam.png',()=>{ const c=T.RB.cards.get('x1'); T.P.pos.set(c.x,c.y,c.z+18); T.P.yaw=0; T.P.pitch=0.35; });
 //await shot('rbv_van.png',()=>{ const v=T.VANS[0]; T.P.pos.set(v.tx+(v.tx-v.x)*2.2,v.y+0.1,v.tz+(v.tz-v.z)*2.2); T.P.yaw=Math.atan2(-(v.x-T.P.pos.x),-(v.z-T.P.pos.z))+0.35; T.P.pitch=-0.05; });
 await shot('rbv_down.png',()=>{ const v=T.VANS[0]; T.P.pos.set(v.tx+(v.tx-v.x)*3,v.y+0.1,v.tz+(v.tz-v.z)*3); T.P.down={hp:10,t0:performance.now(),noMate:-999}; T.P.hp=10; T.P.yaw+=1.2; T.P.pitch=-0.25; });
await pg.evaluate(()=>{ window.cam=new THREE.PerspectiveCamera(50,900/520,0.05,3000); const Rr=T.renderer.render.bind(T.renderer); T.renderer.render=(s,cc)=>Rr(s,cc===T.camera?cam:cc); const p=T.P.pos, y=T.P.yaw, rx=Math.cos(y), rz=-Math.sin(y); cam.position.set(p.x+rx*3.2-Math.sin(y)*0.6,p.y+1.3,p.z+rz*3.2-Math.cos(y)*0.6); cam.lookAt(p.x-Math.sin(y)*0.8,p.y+0.3,p.z-Math.cos(y)*0.8); }); await sleep(1500); await pg.screenshot({path:'rbv_down_side.png'});
 console.log(await pg.evaluate(()=>JSON.stringify({rx:T.localHero.group.rotation.x,down:!!T.P.down,hp:T.P.hp,dead:T.net.dead})));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

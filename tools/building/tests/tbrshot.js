// Battle royale pictures: the storm wall close by with the HUD, a few bots around, and the big map with the circles.
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/brs'; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,terrainH,TOD'),{vp:{width:1000,height:620}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.BR.on,null,{timeout:120000});
 await pg.evaluate(()=>{ const p=T.P.pos, S=T.BR.storm; T.P.sky=null; T.P.hp=1e6; S.cx=p.x-60; S.cz=p.z-30; S.r=90; S.tx=S.cx-10; S.tz=S.cz; S.tr=50; S.t=40; S.state='wait'; T.BR.over=true; T.BR.overT=1e9;
   T.BR.bots.forEach((b,i)=>{ b.sky=null; const a=i*0.7, r=12+i*3; b.pos.set(p.x+Math.cos(a)*r,0,p.z-Math.abs(Math.sin(a))*r-6); b.pos.y=T.terrainH(b.pos.x,b.pos.z)+0.1; b.wpn=i%3?'ar':'pump'; b.ammo=30; }); T.P.yaw=0.9; T.P.pitch=-0.05; });
 await sleep(4000); await pg.screenshot({path:pre+'_hud.png',timeout:200000});
 await pg.keyboard.press('KeyM'); await sleep(1500); await pg.screenshot({path:pre+'_map.png',timeout:200000});
 console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

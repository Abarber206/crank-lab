// the battle bus: a Battle royale match starts with you and every bot aboard the bus high over the island; you jump out
// when you press Jump and skydive; the bots jump along the way, your teammates right after you; nobody's left aboard at
// the end; the first storm countdown waits for the bus.  node tbus.js [shots-prefix]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const shots=process.argv[2]; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,BRBUS,brJumpOut,terrainH,TOD'),shots?{vp:{width:1000,height:620}}:{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; T.TOD.fix=0.3; document.querySelector('.mode[data-mode=br]').click(); const s=document.getElementById('brTeamSel'); s.value='2'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.BR.on&&T.BRBUS.on,null,{timeout:120000}); await sleep(1500);
 const s0=await pg.evaluate(()=>({bus:T.BRBUS.on,pBus:!!T.P.bus,botsBus:T.BR.bots.filter(b=>b.bus).length,above:Math.round(T.P.pos.y-T.terrainH(T.P.pos.x,T.P.pos.z)),T:Math.round(T.BRBUS.T),stormT:Math.round(T.BR.storm.t),tip:!document.getElementById('busTip').hidden,vis:T.BRBUS.g.visible}));
 if(shots){ await sleep(2500); await pg.screenshot({path:shots+'_ride.png',timeout:200000}); }
 await sleep(6000); await pg.evaluate(()=>T.brJumpOut(T.P)); await sleep(3000);
 const s1=await pg.evaluate(()=>({pBus:!!T.P.bus,pSky:!!T.P.sky,mate:T.BR.bots.filter(b=>b.team===0).map(b=>!b.bus&&!!b.sky),botsBus:T.BR.bots.filter(b=>b.bus).length,tip:!document.getElementById('busTip').hidden}));
 if(shots){ await pg.screenshot({path:shots+'_jump.png',timeout:200000}); }
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T-0.5; }); await sleep(2500);
 const s2=await pg.evaluate(()=>({botsBus:T.BR.bots.filter(b=>b.bus).length,sky:T.BR.bots.filter(b=>b.sky).length}));
 console.log(JSON.stringify({s0,s1,s2}));
 const ok=s0.bus&&s0.pBus&&s0.botsBus===19&&s0.above>150&&s0.stormT>s0.T&&s0.tip&&!s1.pBus&&s1.pSky&&s1.mate.every(x=>x)&&!s1.tip&&s2.botsBus===0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

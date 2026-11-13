// rain: streaks around you outdoors (none indoors), grey light; the sound plays; no errors
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,TOD,TOWNS,terrainH,CELL,WEATHER,weatherRoll,renderMain,localHero,audioInit'),{vp:{width:1000,height:600}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); T.audioInit(); }); await sleep(2500);
 await pg.evaluate(()=>{ T.WEATHER.fixed=1; T.weatherRoll(); T.WEATHER.k=0.98; T.TOD.fix=0.3; const t=T.TOWNS.find(t=>!t.kind), x=t.x+30, z=t.z+30; T.P.pos.set(x,T.terrainH(x,z)+0.1,z); }); await sleep(3000);
 const shot=async n=>{ const u=await pg.evaluate(()=>{ T.renderMain(); return T.renderer.domElement.toDataURL('image/jpeg',0.85); }); require('fs').writeFileSync('/home/claude/work/rain_'+n+'.jpg',Buffer.from(u.split(',')[1],'base64')); };
 await shot('out');
 const st=await pg.evaluate(()=>({k:+T.WEATHER.k.toFixed(2),vis:T.WEATHER.mesh&&T.WEATHER.mesh.visible,snd:T.WEATHER.snd?+T.WEATHER.snd.g.gain.value.toFixed(3):null}));
 // indoors
 await pg.evaluate(()=>{ const t=T.TOWNS.find(t=>!t.kind&&t.houses.length), h=t.houses[0], x=(h.i0+h.w/2)*T.CELL, z=(h.j0+h.d/2)*T.CELL; T.P.pos.set(x,t.h+0.05,z); }); await sleep(2500);
 await shot('in');
 console.log(JSON.stringify(st)); console.log(st.vis&&st.k>0.9?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

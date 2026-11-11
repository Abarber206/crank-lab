// the 3D lobby: pictures of the lobby (desktop and phone landscape) and of the Friends and Profile tabs
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const pre=process.argv[2]||'/home/claude/work/lob';
 for(const [nm,vp] of [['desk',{width:1280,height:720}],['phone',{width:844,height:390}]]){ if(process.env.ONLY&&process.env.ONLY!==nm) continue;
  const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,settings,LOBBY,camera'),{vp});
  await pg.waitForFunction(()=>window.T&&T.scene&&T.LOBBY,null,{timeout:180000}); await sleep(9000);
  const st=await pg.evaluate(()=>({on:T.LOBBY.on,heroes:T.LOBBY.heroes.length,cam:T.camera.position.toArray().map(v=>+v.toFixed(1))})); console.log(nm,JSON.stringify(st));
  await pg.screenshot({path:pre+'_'+nm+'.png',timeout:200000});
  if(nm==='desk'){ for(const tab of ['friends','profile','locker']){ await pg.evaluate(t=>document.querySelector('.mtabs button[data-tab='+t+']').click(),tab); await sleep(2500); await pg.screenshot({path:pre+'_'+tab+'.png',timeout:200000}); }
    await pg.evaluate(()=>document.querySelector('.mtabs button[data-tab=play]').click()); await sleep(1500); await pg.evaluate(()=>document.getElementById('modeBtn').click()); await sleep(2500); await pg.screenshot({path:pre+'_mode.png',timeout:200000}); }
  console.log(errs.join('\n')||'no errors'); await pg.context().close(); }
 await b.close(); })();

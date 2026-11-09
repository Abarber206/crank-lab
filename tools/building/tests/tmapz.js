const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,toggleMap,settings,TOWNS,SPAWN,mapView'),{fast:true,vp:{width:800,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.getElementById('play').click(); }); await sleep(2000);
 await pg.evaluate(()=>T.toggleMap(true)); await sleep(1500);
 // zoom in on Cinder Flats with the wheel
 const box=await pg.evaluate(()=>{ const r=document.getElementById('bigmapC').getBoundingClientRect(), t=T.TOWNS[6], W=832; return {x:r.left+(t.x-T.SPAWN[0]+W)/(2*W)*r.width,y:r.top+(t.z-T.SPAWN[2]+W)/(2*W)*r.height}; });
 for(let i=0;i<10;i++){ await pg.evaluate(b=>document.getElementById('bigmapC').dispatchEvent(new WheelEvent('wheel',{deltaY:-300,clientX:b.x,clientY:b.y,bubbles:true,cancelable:true})),box); await sleep(100); }
 console.log(await pg.evaluate(()=>JSON.stringify({z:T.mapView.zoom,cx:T.mapView.cx,el:document.elementFromPoint(400,400).id}))); await sleep(800); await pg.screenshot({path:'mapzoom.png'});
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

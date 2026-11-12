// the full map eases smoothly when you scroll, draws quickly, and a click drops a pin (shown on the map, minimap,
// compass and in the world); clicking it again takes it away
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,settings,TOD,terrainH,TOWNS,mapView,MARKS,drawBigMap'),{vp:{width:1280,height:760}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.renderer.info.render.frame>5,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(8000); await pg.evaluate(()=>{ T.TOD.fix=0.3; const t=T.TOWNS[2]; T.P.pos.set(t.x,T.terrainH(t.x,t.z)+0.1,t.z); }); await pg.keyboard.press('KeyM'); await sleep(2500);
 const box=await pg.evaluate(()=>{ const r=document.getElementById('bigmapC').getBoundingClientRect(); return [r.left,r.top,r.width,r.height]; });
 const cx=box[0]+box[2]*0.62, cy=box[1]+box[3]*0.4; await pg.mouse.move(cx,cy);
 // a few scroll notches, then watch the zoom move toward its target frame by frame
 for(let k=0;k<3;k++){ await pg.mouse.wheel(0,-240); await sleep(30); }
 const tr=[]; for(let i=0;i<25;i++){ tr.push(await pg.evaluate(()=>+T.mapView.zoom.toFixed(3))); await sleep(40); }
 const mono=tr.every((v,i)=>i===0||v>=tr[i-1]-1e-6), steps=tr.slice(1).map((v,i)=>v-tr[i]), maxJump=Math.max(...steps)/Math.max(0.01,tr[tr.length-1]-tr[0]);
 const ms=await pg.evaluate(()=>{ const t0=performance.now(); for(let i=0;i<20;i++) T.drawBigMap(); return (performance.now()-t0)/20; });
 await pg.mouse.click(cx+60,cy+40); await sleep(600); const m1=await pg.evaluate(()=>({n:T.MARKS.size,beam:[...T.MARKS.values()].map(M=>!!M.beam.parent)}));
 await pg.screenshot({path:'/home/claude/work/map_pin.png'});
 await pg.keyboard.press('KeyM'); await sleep(1500); await pg.screenshot({path:'/home/claude/work/map_pin_world.png'}); const tag=await pg.evaluate(()=>{ const M=[...T.MARKS.values()][0]; return M?{hidden:M.tag.hidden,txt:M.tag.textContent}:null; });
 await pg.keyboard.press('KeyM'); await sleep(1500); await pg.mouse.click(cx+60,cy+40); await sleep(400); const m2=await pg.evaluate(()=>T.MARKS.size);
 console.log(JSON.stringify({zoom:tr.filter((_,i)=>i%4===0),mono,maxJump:+maxJump.toFixed(2),drawMs:+ms.toFixed(1),m1,tag,m2}));
 const ok=mono&&tr[tr.length-1]>2&&m1.n===1&&m1.beam[0]&&tag&&!tag.hidden&&m2===0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

// upstairs pictures: standing at the top of the stairs in a few two-storey houses, looking down the hallway and across it
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,houseStair,houseRooms,camera'),{vp:{width:1000,height:620}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(800);
 const picks=(process.argv[3]||'0:0,0:1,5:0').split(',').map(s=>s.split(':').map(Number));
 for(const [k,view] of picks){ const r=await pg.evaluate(([k,view])=>{ const hs=[]; for(const t of T.TOWNS) for(const h of t.houses) if(h.floors>1) hs.push(h); const h=hs[k%hs.length], st=T.houseStair(h).cells, C=5, a=st[0], b=st[1];
     const R=T.houseRooms(h,h.L+1); const cx=(a[0]+.5)*C, cz=(a[1]+.5)*C, dx=b[0]-a[0], dz=b[1]-a[1];
     // stand on the landing cell, on the open side of the stairwell; view 0 looks along the hallway, view 1 across it at the doors
     const ox=dz?1:0, oz=dx?1:0; let sx=cx, sz=cz; const mid=[(h.i0+h.w/2)*C,(h.j0+h.d/2)*C]; const sg=ox?Math.sign(mid[0]-cx)||1:Math.sign(mid[1]-cz)||1; sx+=ox*sg*1.4; sz+=oz*sg*1.4;
     T.P.pos.set(sx-dx*1.6,(h.L+1)*4+0.05,sz-dz*1.6); T.P.vel.set(0,0,0); const fx=view?ox*sg:dx, fz=view?oz*sg:dz; T.P.yaw=Math.atan2(-fx,-fz); T.P.pitch=view?0.0:-0.05; window.__hold=[T.P.pos.clone(),T.P.yaw,T.P.pitch];
     if(!window.__hk){ window.__hk=1; const Rr=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera&&window.__hold){ T.P.pos.copy(window.__hold[0]); T.P.vel.set(0,0,0); T.P.yaw=window.__hold[1]; T.P.pitch=window.__hold[2]; } Rr(s,c); }; }
     return {k,w:h.w,d:h.d,rooms:R.rooms.map(r=>r.type).join('/')}; },[k,view]);
   console.log(JSON.stringify(r)); await sleep(3500); await pg.screenshot({path:(process.argv[2]||'/home/claude/work/up')+'_'+k+'_'+view+'.png',timeout:200000}); }
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

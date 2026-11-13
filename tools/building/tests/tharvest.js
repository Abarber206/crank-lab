// harvesting: pickaxe a house wall - a weak point appears on it, a health bar shows the wall's health going down;
// aiming at the weak point and swinging does double damage and moves it
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,pieces,CELL,LVL,TOWNS,terrainH,HARV,startSwing,selectPick,localHero'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(3000);
 const w=await pg.evaluate(()=>{ let best=null; T.pieces.forEach(p=>{ if(best||p.owner!=='world'||p.type!=='wall'||p.axis!=='x'||p.mask!==511||!p.town||p.town.kind) return; const x=p.i*T.CELL+2.4, z=(p.j+.5)*T.CELL; if(Math.abs(T.terrainH(x,z)-p.l*T.LVL)>0.3) return; if(T.pieces.get(`wx${p.i+1}_${p.j}_${p.l}`)||T.pieces.get(`f${p.i}_${p.j}_${p.l}`)) return; best=p; }); // an outside wall, open ground east of it
   const p=best; T.P.pos.set(p.i*T.CELL+2.4,p.l*T.LVL,(p.j+.5)*T.CELL); T.P.yaw=Math.PI/2; T.P.pitch=0.05; T.selectPick(); return {key:p.key,hp:p.hp,max:p.maxHp}; });
 await sleep(1500); const log=[];
 for(let k=0;k<6;k++){ await pg.evaluate(()=>T.startSwing()); await sleep(1600);
   const s=await pg.evaluate(k=>{ const p=T.pieces.get(k), el=document.getElementById('harvBar'); return {hp:p?Math.round(p.hp):0,bar:!el.hidden,txt:el.textContent.slice(0,40),wp:!!(T.HARV.wp&&T.HARV.wp.visible),key:T.HARV.key&&T.HARV.key.key}; },w.key); log.push(s);
   if(k===2&&s.wp){ // aim right at the weak point
     await pg.evaluate(()=>{ for(let q=0;q<3;q++){ T.camera.updateMatrixWorld(); const c=T.camera.position, p=T.HARV.wp.position, d=p.clone().sub(c).normalize(); T.P.yaw=Math.atan2(-d.x,-d.z); T.P.pitch=Math.asin(d.y); } }); await sleep(800);
     await pg.evaluate(()=>{ T.camera.updateMatrixWorld(); const c=T.camera.position, p=T.HARV.wp.position, d=p.clone().sub(c).normalize(); T.P.yaw=Math.atan2(-d.x,-d.z); T.P.pitch=Math.asin(d.y); }); await sleep(400); } }
 const u=await pg.evaluate(()=>{ T.renderer.render(T.scene,T.camera); return T.renderer.domElement.toDataURL('image/jpeg',0.85); }); require('fs').writeFileSync('/home/claude/work/harvest.jpg',Buffer.from(u.split(',')[1],'base64'));
 await pg.screenshot({path:'/home/claude/work/harvest_hud.png',timeout:150000}).catch(()=>{});
 console.log(JSON.stringify(w)); log.forEach(s=>console.log(JSON.stringify(s)));
 const drops=log.map((s,i)=>(i?log[i-1].hp:w.hp)-s.hp), crit=drops.some(d=>d>=90);
 console.log('drops',drops.join(','),'crit',crit); console.log(log.slice(1).every(s=>s.bar)&&crit?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

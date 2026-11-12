// ground views of street ends (kind: edge/fence/stub/circle) and the open road.  node tendview.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,TOWNS,P,settings,TOD,townBatch,WORLD,SPAWN,terrainH'),{vp:{width:1280,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; T.TOD.fix=0.32; document.querySelector('.mode[data-mode=fight]').click(); const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.querySelector('#play').click(); });
 await sleep(9000); await pg.evaluate(()=>{ T.TOD.fix=0.3; });
 const wants=['edge','fence','stub','circle'], shots=[];
 for(const w of wants){ const at=await pg.evaluate(w=>{ for(const t of T.TOWNS){ if(t.kind) continue; const k=t.endKind.findIndex((q,i)=>q===w&&(w!=='edge'||t.dead[i])); if(k>=0) return [t.ends[k][0],t.ends[k][1],t.endDir[k][0],t.endDir[k][1],t.h,t.name]; } return null; },w); if(at) shots.push([w,at]); }
 // and a stretch of open road
 shots.push(['road',await pg.evaluate(()=>{ const rd=T.WORLD.roads.find(r=>!r.street&&r.pts.length>200), p=rd.pts[120], q=rd.pts[124]; const x=T.SPAWN[0]+p[0], z=T.SPAWN[2]+p[1], dx=q[0]-p[0], dz=q[1]-p[1], l=Math.hypot(dx,dz); return [x,z,dx/l,dz/l,T.terrainH(x,z),'road']; })]);
 for(const [w,a] of shots){ await pg.evaluate(a=>{ T.P.pos.set(a[0]-a[2]*20,a[4]+0.1,a[1]-a[3]*20); },a); await pg.evaluate(()=>{ T.TOD.fix=0.3; }); await sleep(4500);
   const url=await pg.evaluate(([w,a])=>{ const THREE=window.THREE, cam=new THREE.PerspectiveCamera(60,1280/800,0.3,2000), back=w==='road'?14:24, side=w==='road'?3:5;
     cam.position.set(a[0]-a[2]*back-a[3]*side,a[4]+(w==='road'?2.2:6),a[1]-a[3]*back+a[2]*side); cam.lookAt(a[0]+a[2]*(w==='road'?20:10),a[4]+0.5,a[1]+a[3]*(w==='road'?20:10));
     T.townBatch.forEach(bb=>bb.meshes.forEach(m=>{ m.visible=true; })); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/png'); },[w,a]);
   require('fs').writeFileSync('/home/claude/work/end_'+w+'.png',Buffer.from(url.split(',')[1],'base64')); console.log(w,a[5]); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

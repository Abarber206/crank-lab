// the named places at eye height: eight spots round each one, looking across it, in a sheet per place
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.argv[4]||'/home/claude/crank-lab/index.html','P,renderer,camera,scene,settings,TOD,terrainH,TOWNS,localHero'),{vp:{width:560,height:340}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const tag=process.argv[2]||'now', only=process.argv[3]&&process.argv[3]!=='all'?process.argv[3]:null; const pois=await pg.evaluate(()=>T.TOWNS.filter(t=>t.kind).map(t=>({n:t.name,x:t.x,z:t.z,R:t.R,h:t.h})));
 for(const p of pois){ if(only&&!p.n.startsWith(only)) continue; const shots=[];
   for(let k=0;k<8;k++){ const a=k/8*Math.PI*2+0.3, rr=p.R*(k%2?0.62:0.38), c=[p.x+Math.cos(a)*rr,p.z+Math.sin(a)*rr], la=a+Math.PI+(k%2?0.35:-0.35), l=[c[0]+Math.cos(la)*20,c[1]+Math.sin(la)*20];
     await pg.evaluate(c=>{ T.TOD.fix=0.3; T.P.pos.set(c[0],T.terrainH(c[0],c[1]),c[1]); },c); await sleep(1500);
     const u=await pg.evaluate(([c,l,h])=>{ const cam=new THREE.PerspectiveCamera(70,560/340,0.1,3000); const y=Math.max(h,T.terrainH(c[0],c[1]))+1.7; cam.position.set(c[0],y,c[1]); cam.lookAt(l[0],y-0.6,l[1]); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.8); },[c,l,p.h]);
     const f=`/home/claude/work/eye_${p.n.replace(/\s/g,'')}_${k}_${tag}.jpg`; require('fs').writeFileSync(f,Buffer.from(u.split(',')[1],'base64')); shots.push(f); }
   console.log(p.n,shots.length); }
 console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

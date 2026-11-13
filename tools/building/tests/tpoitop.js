// the named places straight down from above (a map of what stands where), with a 5 m grid drawn over in the sheet
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.argv[4]||'/home/claude/crank-lab/index.html','P,renderer,camera,scene,settings,TOD,terrainH,TOWNS,localHero'),{vp:{width:700,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const tag=process.argv[2]||'now', only=process.argv[3]&&process.argv[3]!=='all'?process.argv[3]:null; const pois=await pg.evaluate(()=>T.TOWNS.filter(t=>t.kind).map(t=>({n:t.name,x:t.x,z:t.z,R:t.R,h:t.h,ci:Math.round(t.x/5),cj:Math.round(t.z/5)})));
 for(const p of pois){ if(only&&!p.n.startsWith(only)) continue;
   await pg.evaluate(p=>{ T.TOD.fix=0.3; T.P.pos.set(p.ci*5,T.terrainH(p.x,p.z),p.cj*5); },p); await sleep(2500);
   const u=await pg.evaluate(p=>{ const S=50, cam=new THREE.OrthographicCamera(-S,S,S,-S,1,400); cam.position.set(p.ci*5,p.h+120,p.cj*5); cam.up.set(0,0,-1); cam.lookAt(p.ci*5,p.h,p.cj*5); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },p);
   require('fs').writeFileSync(`/home/claude/work/top_${p.n.replace(/\s/g,'')}_${tag}.jpg`,Buffer.from(u.split(',')[1],'base64')); }
 console.log(JSON.stringify(pois)); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

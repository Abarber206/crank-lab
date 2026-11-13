// the named places: each one from above at an angle and from the ground at two corners, at midday
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,camera,scene,settings,TOD,terrainH,TOWNS,localHero'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const tag=process.argv[2]||'now', only=process.argv[3]; const pois=await pg.evaluate(()=>T.TOWNS.filter(t=>t.kind).map(t=>({n:t.name,x:t.x,z:t.z,R:t.R,h:t.h})));
 for(const p of pois){ if(only&&!p.n.startsWith(only)) continue; const views=[['top',[p.x+p.R*1.1,p.h+38,p.z+p.R*1.1],[p.x,p.h,p.z]],['top2',[p.x-p.R*1.1,p.h+30,p.z-p.R*0.6],[p.x,p.h,p.z]],['g1',[p.x+p.R*0.55,p.h+1.7,p.z+p.R*0.45],[p.x-p.R*0.3,p.h+1.2,p.z-p.R*0.2]],['g2',[p.x-p.R*0.5,p.h+1.7,p.z+p.R*0.5],[p.x+p.R*0.3,p.h+1.2,p.z-p.R*0.3]]];
   for(const [n,c,l] of views){ await pg.evaluate(c=>{ T.TOD.fix=0.3; T.P.pos.set(c[0],T.terrainH(c[0],c[2]),c[2]); },c); await sleep(2500);
     const u=await pg.evaluate(([c,l])=>{ const cam=new THREE.PerspectiveCamera(65,1100/640,0.1,3000); const y=Math.max(c[1],T.terrainH(c[0],c[2])+1.6); cam.position.set(c[0],y,c[2]); cam.lookAt(l[0],l[1],l[2]); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.82); },[c,l]);
     require('fs').writeFileSync(`/home/claude/work/poi_${p.n.replace(/\s/g,'')}_${n}_${tag}.jpg`,Buffer.from(u.split(',')[1],'base64')); } }
 console.log(JSON.stringify(pois)); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

// pictures of a place from given spots: node tpoishot.js <tag> <name prefix> "x,y,z,lx,ly,lz;..." (metres from the site's middle cell, y above its ground)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,scene,settings,TOD,terrainH,TOWNS,localHero'),{vp:{width:800,height:500}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const [tag,name,list]=process.argv.slice(2); const p=await pg.evaluate(n=>{ const t=T.TOWNS.find(t=>t.name.startsWith(n)); return {ox:Math.round(t.x/5)*5,oz:Math.round(t.z/5)*5,h:t.h}; },name);
 let k=0; for(const v of list.split(';')){ const [x,y,z,lx,ly,lz]=v.split(',').map(Number); await pg.evaluate(([p,x,z])=>{ T.TOD.fix=0.3; T.P.pos.set(p.ox+x,T.terrainH(p.ox+x,p.oz+z),p.oz+z); },[p,x,z]); await sleep(2500);
   const u=await pg.evaluate(([p,a])=>{ const cam=new THREE.PerspectiveCamera(60,800/500,0.1,3000); cam.position.set(p.ox+a[0],p.h+a[1],p.oz+a[2]); cam.lookAt(p.ox+a[3],p.h+a[4],p.oz+a[5]); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },[p,[x,y,z,lx,ly,lz]]);
   require('fs').writeFileSync(`/home/claude/work/shot_${name.replace(/\s/g,'')}_${k++}_${tag}.jpg`,Buffer.from(u.split(',')[1],'base64')); }
 console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

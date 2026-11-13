// house interiors: for a few houses, the ground floor from two corners and (two-storey) the upstairs, at midday
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,TOD,TOWNS,terrainH,CELL,LVL,localHero'),{vp:{width:960,height:560}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(3000);
 const tag=process.argv[2]||'now';
 const H=await pg.evaluate(()=>{ const out=[]; for(const t of T.TOWNS){ if(t.kind||!t.houses) continue; for(const h of t.houses){ if(out.length<4&&(out.length%2===0?h.floors>1:h.floors===1)&&!out.some(o=>o.t===t.name)) out.push({t:t.name,ty:t.h,i0:h.i0,j0:h.j0,w:h.w,d:h.d,f:h.floors}); } } return out; });
 console.log(JSON.stringify(H)); const shots=[];
 for(let k=0;k<H.length;k++){ const h=H[k], C=0, x0=h.i0*5, z0=h.j0*5, x1=(h.i0+h.w)*5, z1=(h.j0+h.d)*5;
   const views=[[x0+0.9,h.ty+1.65,z0+0.9,x1-2,h.ty+1.2,z1-2],[x1-0.9,h.ty+1.65,z1-0.9,x0+2,h.ty+1.2,z0+2]]; if(h.f>1) views.push([x0+0.9,h.ty+4+1.65,z1-0.9,x1-2,h.ty+4+1.0,z0+2]);
   for(let v=0;v<views.length;v++){ const V=views[v]; await pg.evaluate(V=>{ T.TOD.fix=0.3; T.P.pos.set(V[0],V[1]-1.6,V[2]); },V); await sleep(2200);
     const u=await pg.evaluate(V=>{ const cam=new THREE.PerspectiveCamera(75,960/560,0.05,2000); cam.position.set(V[0],V[1],V[2]); cam.lookAt(V[3],V[4],V[5]); T.localHero.group.visible=false; T.camera.position.copy(cam.position); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },V);
     const f='/home/claude/work/int_'+k+'_'+v+'_'+tag+'.jpg'; require('fs').writeFileSync(f,Buffer.from(u.split(',')[1],'base64')); shots.push(f); } }
 console.log(shots.join(' ')); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

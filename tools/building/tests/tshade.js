// lighting check: inside a town house (ground floor, looking across the room), and in the woods under trees, at midday
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,TOD,TOWNS,terrainH,FOREST,CELL,LVL,SPAWN,hero,INDOOR,terrainMat,grassMat'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(3000);
 const tag=process.argv[2]||'now';
 const views=await pg.evaluate(()=>{ const t=T.TOWNS.find(t=>!t.kind&&t.houses&&t.houses.length), h=t.houses.find(h=>h.w>=3&&h.d>=3)||t.houses[0];
   const cx=(h.i0+h.w/2)*T.CELL, cz=(h.j0+h.d/2)*T.CELL; // a tree with others around it
   let best=null, bn=0; for(let i=0;i<T.FOREST.trees.length;i+=7){ const p=T.FOREST.trees[i]; let n=0; for(let j=0;j<T.FOREST.trees.length;j+=3){ const q=T.FOREST.trees[j]; if(Math.abs(q.x-p.x)<14&&Math.abs(q.z-p.z)<14) n++; } if(n>bn){ bn=n; best=p; } }
   return {house:[cx,cz,h.i0*T.CELL+0.8,h.j0*T.CELL+0.8,t.h],tree:[best.x,best.z]}; });
 for(const [n,f] of [['in',v=>({p:[v.house[2],v.house[4]+1.6,v.house[3]],l:[v.house[0]+3,v.house[4]+1.0,v.house[1]+3]})],['woods',v=>({p:[v.tree[0]+5,null,v.tree[1]+5],l:[v.tree[0]-8,null,v.tree[1]-8]})]]){
   const u=await pg.evaluate(([fs,v])=>{ const f=eval(fs)(v); T.TOD.fix=0.3; if(f.p[1]==null) f.p[1]=T.terrainH(f.p[0],f.p[2])+1.7; if(f.l[1]==null) f.l[1]=T.terrainH(f.l[0],f.l[2])+0.6;
     T.P.pos.set(f.p[0],f.p[1]-1.6,f.p[2]); return 1; },[f.toString(),views]); await sleep(3500);
   const img=await pg.evaluate(([fs,v])=>{ const f=eval(fs)(v); if(f.p[1]==null) f.p[1]=T.terrainH(f.p[0],f.p[2])+1.7; if(f.l[1]==null) f.l[1]=T.terrainH(f.l[0],f.l[2])+0.6; const cam=new THREE.PerspectiveCamera(70,1100/640,0.1,3000); cam.position.set(...f.p); cam.lookAt(...f.l);
     T.camera.position.copy(cam.position); T.camera.quaternion.copy(cam.quaternion); T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.88); },[f.toString(),views]);
   require('fs').writeFileSync('/home/claude/work/shade_'+n+'_'+tag+'.jpg',Buffer.from(img.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

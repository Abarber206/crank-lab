// invisible barriers: from each face of every solid box (decoration, trees, rocks, cars, furniture) at body height, look
// inward for what is drawn there; a face standing well off anything drawn is a wall you'd bump into in thin air
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.argv[2]||'/home/claude/crank-lab/index.html','scene,P,settings,props,STATICS,treeMesh,TOWNS,terrainH'),{norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(4000);
 const out=await pg.evaluate(()=>{ const ray=new THREE.Raycaster(); ray.layers.enableAll(); const o=new THREE.Vector3(), d=new THREE.Vector3();
   T.scene.updateMatrixWorld(true);
   const deco=[]; T.scene.traverse(m=>{ if(m.isMesh&&m.geometry&&m.visible!==false&&!m.isInstancedMesh){ m.geometry.computeBoundingSphere&&m.geometry.computeBoundingSphere(); if(m.geometry.boundingSphere&&m.geometry.boundingSphere.radius<150) deco.push(m); } }); deco.forEach(m=>m.updateMatrixWorld(true)); const _c=new THREE.Vector3();
   const nearDeco=(x,z)=>deco.filter(m=>{ const s=m.geometry.boundingSphere; _c.copy(s.center).applyMatrix4(m.matrixWorld); return Math.hypot(_c.x-x,_c.z-z)<s.radius*Math.max(m.scale.x,m.scale.y,m.scale.z,1)+6; });
   const gaps=(b,meshes)=>{ const cx=(b[0]+b[3])/2, cz=(b[2]+b[5])/2, b1=Math.max(b[1],T.terrainH(cx,cz)), top=Math.min(b[4],b1+1.8); if(top-b1<0.3) return {worst:0,at:null}; let worst=0, at=null;
     const hs=[0.25,0.8,1.4].map(h=>b1+h).filter(y=>y<top-0.05); if(!hs.length) hs.push((b1+top)/2);
     for(const [nx,nz] of [[1,0],[-1,0],[0,1],[0,-1]]) for(const f of [-0.3,0,0.3]){ const half=nx?(b[3]-b[0])/2:(b[5]-b[2])/2, along=nx?(b[5]-b[2]):(b[3]-b[0]);
         const px=nx?(nx>0?b[3]:b[0]):cx+f*along, pz=nz?(nz>0?b[5]:b[2]):cz+f*along; let best=1e9, inner=false;
         for(const y of hs){ if(inAny(px+nx*0.05,y,pz+nz*0.05,b)){ inner=true; break; } o.set(px+nx*7,y,pz+nz*7); d.set(-nx,0,-nz); ray.set(o,d); ray.far=half*2+7; const hit=ray.intersectObjects(meshes,true)[0]; const g=hit?hit.distance-7:half*2; if(g<best) best=g; }  // (felt only if nothing is there at any body height)
         if(inner) continue; if(best>worst){ worst=best; at=[+px.toFixed(1),+hs[0].toFixed(1),+pz.toFixed(1)]; } }
     return {worst:+worst.toFixed(2),at}; };
   const grid=new Map();
   for(const st of T.STATICS){ if(!st.solid) continue; for(const bb of st.solid.boxes){ for(let gx=Math.floor(bb[0]/4);gx<=Math.floor(bb[3]/4);gx++) for(let gz=Math.floor(bb[2]/4);gz<=Math.floor(bb[5]/4);gz++){ const k=gx+','+gz; let l=grid.get(k); if(!l) grid.set(k,l=[]); l.push(bb); } } }
   const inAny=(x,y,z,self)=>{ const l=grid.get(Math.floor(x/4)+','+Math.floor(z/4)); return !!l&&l.some(bb=>bb!==self&&x>bb[0]&&x<bb[3]&&z>bb[2]&&z<bb[5]&&y>bb[1]&&y<bb[4]); };
   const res={deco:[],prop:{}};
   // decoration: every solid box out in the world
   for(const st of T.STATICS){ if(!st.solid||!st.solid.boxes.length) continue; const b=st.solid.boxes[0]; if(b[4]-b[1]<0.4) continue; const ms=nearDeco(st.x,st.z); if(!ms.length) continue; const g=gaps(b,ms);
     const site=T.TOWNS.find(t=>t.kind&&Math.hypot(t.x-st.x,t.z-st.z)<t.R+4); if(g.worst>0.3) res.deco.push({k:(site?site.name.replace(/\s/g,'')+':':'')+st.solid.key.replace(/\d+$/,''),o:st.solid.dobj?st.solid.dobj.id:null,gap:g.worst,size:[+(b[3]-b[0]).toFixed(1),+(b[4]-b[1]).toFixed(1),+(b[5]-b[2]).toFixed(1)],at:g.at,rel:site?[+(st.x-Math.round(site.x/5)*5).toFixed(1),+(st.z-Math.round(site.z/5)*5).toFixed(1)]:null}); }
   // props: all rocks, cars and furniture, a sample of trees
   let nt=0; for(const p of T.props){ if(!p.alive||!p.boxes) continue; if((p.kind==='tree'||p.kind==='pine')&&(nt++%25)) continue; if(p.kind==='rock'){ const H0=T.terrainH(p.x,p.z); if([[2.5,0],[-2.5,0],[0,2.5],[0,-2.5]].some(([a,c])=>Math.abs(T.terrainH(p.x+a,p.z+c)-H0)>0.6)) continue; } if(p.lazy||(p.kind==='tree'||p.kind==='pine')) T.treeMesh(p); p.g.updateMatrixWorld(true);
     const ms=[]; p.g.traverse(m=>{ if(m.isMesh) ms.push(m); }); const e=res.prop[p.kind]||(res.prop[p.kind]={n:0,bad:0,worst:[]}); e.n++; let w=0, at=null; for(const b of p.boxes){ const g=gaps(b,ms); if(g.worst>w){ w=g.worst; at=g.at; } }
     if(w>0.3){ e.bad++; e.worst.push({id:p.id,s:+p.s.toFixed(2),gap:w,at}); } }
   for(const k in res.prop) res.prop[k].worst=res.prop[k].worst.sort((a,b)=>b.gap-a.gap).slice(0,6);
   const by={}; for(const r of res.deco){ (by[r.k]=by[r.k]||[]).push(r); } res.decoBy=Object.fromEntries(Object.entries(by).map(([k,l])=>[k,{n:l.length,worst:l.sort((a,b)=>b.gap-a.gap).slice(0,5)}])); res.nDeco=res.deco.length; delete res.deco;
   res.total=T.STATICS.length; return res; });
 for(const [k,v] of Object.entries(out.decoBy)) console.log('deco',k.padEnd(10),v.n,'bad; worst',v.worst.slice(0,/:/.test(k)?5:3).map(w=>w.gap+'@'+(w.rel?'rel '+w.rel.join(','):w.at.join(','))+' size '+w.size.join('x')).join(' | '));
 for(const [k,v] of Object.entries(out.prop)) console.log('prop',k.padEnd(10),v.bad+'/'+v.n,'bad; worst',v.worst.slice(0,3).map(w=>w.gap+'@'+w.at.join(',')+' s'+w.s).join(' | '));
 console.log('deco bad',out.nDeco,'of',out.total); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

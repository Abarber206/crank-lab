// what the draw calls are: one frame's calls grouped by pass (main, mirror, shadow) and by what's drawn.  node tcalls.js [town|river|br]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const sc=process.argv[2]||'town'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,P,renderer,settings,TOWNS,terrainH,SPAWN,camera,BR,BRBUS,WORLD,TOD,pieces,props,chests,drops,karts,townBatch,STATICS,localHero,VANS'),{vp:{width:320,height:200}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(sc=>{ T.settings.skyDrop=false; T.TOD.fix=0.3; document.querySelector('.mode[data-mode='+(sc==='br'?'br':'fight')+']').click(); const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); },sc);
 if(sc==='br') await pg.waitForFunction(()=>T.BR.on,null,{timeout:120000}); await sleep(2000);
 await pg.evaluate(sc=>{ const t=T.TOWNS[0]; T.P.pos.set(t.x+6,T.terrainH(t.x+6,t.z+4)+0.05,t.z+4); T.P.yaw=0.6; T.P.pitch=-0.05; T.P.vel.set(0,0,0);
   if(sc==='river'){ const rv=T.WORLD.rivers.find(r=>r.main)||T.WORLD.rivers[0], p=rv.pts[Math.floor(rv.pts.length*0.45)], n=rv.pts[Math.floor(rv.pts.length*0.45)+6], S=T.SPAWN, x=S[0]+p[0]+p[3]+3, z=S[2]+p[1]; T.P.pos.set(x,T.terrainH(x,z)+0.05,z); T.P.yaw=Math.atan2(-(n[0]-p[0]),-(n[1]-p[1])); }
   if(sc==='br'){ T.BRBUS.t=T.BRBUS.T; T.P.bus=false; T.P.sky=null; T.P.hp=1e6; T.BR.over=true; T.BR.overT=1e9; T.BR.bots.forEach((b,i)=>{ b.bus=false; b.sky=null; const a=i*0.33, r=15+i*5, x=t.x+Math.cos(a)*r, z=t.z+Math.sin(a)*r; b.pos.set(x,T.terrainH(x,z)+0.1,z); b.vel.set(0,0,0); b.hp=1e6; }); } },sc);
 await sleep(6000);
 await pg.evaluate(()=>{ const tag=(o,k)=>{ if(o&&!o.userData.kind) o.userData.kind=k; }; T.pieces.forEach(p=>tag(p.group,p.owner==='world'?'piece:world':'piece:build')); T.props.forEach(p=>tag(p.g,'prop:'+p.kind)); T.chests.forEach(c=>tag(c.g,'chest')); T.drops.forEach(d=>tag(d.g,'drop')); T.karts.forEach(k=>tag(k.g,k.boat?'boat':'kart'));
   T.townBatch.forEach(b=>b.meshes.forEach(m=>tag(m,'townBatch'))); (T.STATICS||[]).forEach(s=>{ tag(s.g,'static'); tag(s.mesh,'static'); }); tag(T.localHero.group,'hero:you'); T.BR.bots.forEach(b=>tag(b.h.group,'hero:bot')); (T.VANS||[]).forEach(v=>tag(v.g,'van')); });
 const r=await pg.evaluate(()=>new Promise(res=>{ const R=T.renderer, orig=R.renderBufferDirect.bind(R), cnt=new Map(); let pass='main', on=false, total=0;
   const top=o=>{ let x=o; while(x.parent&&x.parent!==T.scene) x=x.parent; return x; };
   R.renderBufferDirect=function(cam,scene,geo,mat,obj,grp){ if(on){ total++; const t=top(obj), p=mat.type==='MeshDepthMaterial'||mat.type==='MeshDistanceMaterial'?'shadow':cam===T.camera?'main':'other';
       const kk=t.userData&&t.userData.kind; const k=p+' | '+(kk||t.name||t.type+'['+geo.type+(geo.attributes.position?':'+geo.attributes.position.count:'')+(mat.color?' #'+mat.color.getHexString():'')+']')+' | '+(obj.isInstancedMesh?'inst ':'')+mat.type; cnt.set(k,(cnt.get(k)||0)+1); } return orig(cam,scene,geo,mat,obj,grp); };
   requestAnimationFrame(()=>{ on=true; requestAnimationFrame(()=>{ on=false; R.renderBufferDirect=orig; res({total,top:[...cnt.entries()].sort((a,b)=>b[1]-a[1]).slice(0,30)}); }); }); }));
 console.log(sc,'total calls in one frame:',r.total); r.top.forEach(([k,n])=>console.log(String(n).padStart(6),k));
 console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

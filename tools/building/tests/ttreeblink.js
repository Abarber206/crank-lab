// hit a tree: on every rendered frame it is drawn exactly once (its own mesh or its forest instance, never neither)
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,props,propHit,FOREST'),{fast:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(1500);
 const r=await pg.evaluate(async()=>{ let tree=null, bd=1e9; T.props.forEach(p=>{ if(p.lazy&&p.alive&&!p.gone){ const d=Math.hypot(p.x-T.P.pos.x,p.z-T.P.pos.z); if(d<bd){ bd=d; tree=p; } } });
   T.P.pos.set(tree.x+2,T.P.pos.y,tree.z); await new Promise(r=>setTimeout(r,800));
   const m=new THREE.Matrix4(), v=new THREE.Vector3(), inInst=()=>{ for(const set of [T.FOREST.near,T.FOREST.far]) for(const im of set[tree.kind]){ for(let i=0;i<im.count;i++){ im.getMatrixAt(i,m); v.setFromMatrixPosition(m); if(Math.abs(v.x-tree.x)<0.01&&Math.abs(v.z-tree.z)<0.01) return true; } } return false; };
   const R0=T.renderer.render.bind(T.renderer); let none=0, both=0, n=0, own=0; T.renderer.render=(s,c)=>{ const a=!!tree.g.parent, i=inInst(); if(!a&&!i) none++; if(a&&i) both++; if(a) own++; n++; R0(s,c); };
   T.propHit(tree,10,new THREE.Vector3(tree.x,tree.base+1,tree.z),true);
   const t0=performance.now(); while(tree.g.parent||performance.now()-t0<2000){ await new Promise(r=>setTimeout(r,250)); if(performance.now()-t0>60000) break; } await new Promise(r=>setTimeout(r,1500)); T.renderer.render=R0; return {frames:n,none,both,ownFrames:own}; });
 console.log(JSON.stringify(r), r.frames>4&&r.none===0&&r.ownFrames>0?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

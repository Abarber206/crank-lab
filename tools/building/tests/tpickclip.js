// does the shoulder-rest pickaxe pass through the body? Builds every outfit's hero (two pickaxes) in the preview pose and
// checks points along the pick against the body's meshes (inside = rays out cross it an odd number of times); the
// gripping hand doesn't count. SEARCH=1 tries a grid of poses and prints the best.  node tpickclip.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,heroFor,animateRig,OUTFITS,PICK_SHOW'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.heroFor,null,{timeout:180000}); await sleep(1000);
 const r=await pg.evaluate((search)=>{ const rc=new THREE.Raycaster(), dirs=[new THREE.Vector3(1,0.013,0.021).normalize(),new THREE.Vector3(-0.017,1,0.011).normalize(),new THREE.Vector3(0.019,-0.012,1).normalize()];
   const HS=[]; for(const o of T.OUTFITS) for(const pk of ['steel','bone']){ const H=T.heroFor(o,pk); T.scene.add(H.group); HS.push({H,nm:o.id+'/'+pk}); }
   const under=(m,g)=>{ for(let x=m;x;x=x.parent) if(x===g) return true; return false; };
   const run=(detail)=>{ let tot=0; const rep=[]; for(const {H,nm} of HS){ const S={showPick:true,bare:false,pos:new THREE.Vector3(0,0,0),vel:new THREE.Vector3(),yaw:0,pitch:-0.05,onGround:true,gun:false};
       for(let i=0;i<12;i++) T.animateRig(H,S,1/30); H.group.updateMatrixWorld(true); const P=H.rig.pick, hand=H.rig.armR.wr||H.rig.armR.hand;
       const body=[]; H.group.traverse(m=>{ if(m.isMesh&&m.visible&&!under(m,P)&&!under(m,hand)&&m.material&&m.material.side!==THREE.BackSide) body.push(m); });
       const bad=[]; for(let y=-0.95;y<=0.5;y+=0.03){ const p=P.localToWorld(new THREE.Vector3(0,y,0)); for(const m of body){ let inside=0; for(const d of dirs){ rc.set(p,d); rc.far=3; if(rc.intersectObject(m,false).length%2===1) inside++; } if(inside>=2){ bad.push(y.toFixed(2)); break; } } }
       { const sh=H.rig.armR.sh.getWorldPosition(new THREE.Vector3()), a=P.localToWorld(new THREE.Vector3(0,0,0)), c=P.localToWorld(new THREE.Vector3(0,-0.9,0)), ab=c.clone().sub(a), t=Math.max(0,Math.min(1,sh.clone().sub(a).dot(ab)/ab.lengthSq())); const d=a.clone().addScaledVector(ab,t).distanceTo(sh); run.dist=(run.dist||0)+d; } tot+=bad.length; if(detail&&bad.length) rep.push(nm+' '+bad.join(',')); }
     return detail?rep:tot; };
   if(!search) return run(true);
   const all=[]; for(const hx of [0.15,0.19,0.23]) for(const hz of [-0.18,-0.25,-0.32]) for(const dx of [-0.04,-0.12,-0.2]) for(const dz of [-0.75,-0.92,-1.1]){ T.PICK_SHOW.hand=[hx,1.13,hz]; T.PICK_SHOW.dir=[dx,-0.6,dz]; run.dist=0; const n=run(false), dd=run.dist/HS.length; all.push({score:n+200*Math.max(0,dd-0.12),n,dd:+dd.toFixed(3),hx,hz,dx,dz}); }
   all.sort((a,b)=>a.score-b.score); return all.slice(0,6).map(x=>JSON.stringify(x)); },!!process.env.SEARCH);
 console.log(r.length?r.join('\n'):'no clipping'); if(!process.env.SEARCH) console.log(r.length?'FAIL':'PASS'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,camera,karts,enterKart,heroFor,OUTFITS,animateRig,settings'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.karts,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); T.settings.skyDrop=false; });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 console.log(await pg.evaluate(()=>{ const K=T.karts[1]; const h=T.heroFor(T.OUTFITS[2],'steel'); T.scene.add(h.group); const out={};
  for(const s of [0,1]){ for(let j=0;j<20;j++) T.animateRig(h,{pos:T.P.pos,vel:new THREE.Vector3(),yaw:K.yaw,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:null,seat:{k:K,s,look:K.yaw}},0.06);
   h.group.updateMatrixWorld(true); K.g.updateMatrixWorld(true); const inv=new THREE.Matrix4().copy(K.body.matrixWorld).invert(); const L=o=>{ const v=new THREE.Vector3(); o.getWorldPosition(v); v.applyMatrix4(inv); return v.toArray().map(x=>+x.toFixed(3)); };
   const r=h.rig; out['s'+s]={hp:L(r.legL.hp),kn:L(r.legL.kn),foot:L(r.legL.foot), footKids:r.legL.foot.children.length};
   const bb=new THREE.Box3(); r.legL.foot.traverse(o=>{ if(o.isMesh){ o.geometry.computeBoundingBox(); const b2=o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld).applyMatrix4(inv); bb.union(b2);} }); out['s'+s].footBox=[bb.min.toArray().map(x=>+x.toFixed(2)),bb.max.toArray().map(x=>+x.toFixed(2))]; }
  return JSON.stringify(out); }));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

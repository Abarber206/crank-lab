const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,heroFor,OUTFITS,animateRig'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.OUTFITS,null,{timeout:120000});
 console.log(await pg.evaluate(()=>{ const out=[]; const h=T.heroFor(T.OUTFITS[0]); const v=new THREE.Vector3(), p=new THREE.Vector3();
   const st=sw=>({pos:new THREE.Vector3(),vel:new THREE.Vector3(),yaw:0,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:sw,emote:null});
   for(let k=0;k<60;k++) T.animateRig(h,st(0),1/60);
   for(const side of ['fore','back']){ let line=side+': '; const N=34; for(let i=0;i<=N;i++){ const t=i/N; T.animateRig(h,st(t<1?0.34*(1-t)+1e-4:0),0.01); if(i%3===0){ h.group.updateMatrixWorld(true); h.rig.pick.getWorldPosition(v); line+=`[${t.toFixed(2)} x${v.x.toFixed(2)} y${v.y.toFixed(2)}] `; } } for(let k=0;k<20;k++) T.animateRig(h,st(0),1/60); out.push(line); }
   return out.join('\n'); }));
 await b.close(); })();

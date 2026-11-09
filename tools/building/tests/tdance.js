// hero close-ups: several outfits, front / side / back / face, plus a run pose, on a neutral backdrop
const {sleep,page,launch,open}=require('./h.js'); const tag=process.argv[2]||'a';
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,RUN'),{vp:{width:1200,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 await pg.evaluate(()=>{ document.getElementById('menu').hidden=true;
   const cv=document.createElement('canvas'); cv.width=1200; cv.height=700; cv.style.cssText='position:fixed;inset:0;z-index:99;background:#7c93ad'; document.body.appendChild(cv);
   const r=new THREE.WebGLRenderer({canvas:cv,antialias:true}); r.setClearColor(0x8aa0b8); r.shadowMap.enabled=true; const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xeaf2ff,0x4a5a40,0.8)); const k=new THREE.DirectionalLight(0xfff2e0,0.9); k.position.set(3,6,-4); k.castShadow=true; sc.add(k); const f=new THREE.DirectionalLight(0xbfd8ff,0.35); f.position.set(-4,3,3); sc.add(f);
   const gnd=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({color:0x6f8a5a})); gnd.rotation.x=-Math.PI/2; gnd.receiveShadow=true; sc.add(gnd);
   window.H=[]; const ids=[0,1,2,5,9]; ids.forEach((i,n)=>{ const h=T.heroFor(T.OUTFITS[i]); h.group.traverse(o=>{ if(o.isMesh){ o.castShadow=o.receiveShadow=true; } }); sc.add(h.group); H.push({h,x:(n-2)*1.3}); });
   window.R={r,sc}; window.dpose=(t0)=>{ const ids=['floss','robot','hype','disco','shuffle']; H.forEach((e,n)=>{ for(let k=0;k<50;k++){ const st={pos:new THREE.Vector3(e.x,0,0),vel:new THREE.Vector3(),yaw:0.15,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:{id:ids[n],t:t0+k/60}}; T.animateRig(e.h,st,1/60); } e.h.rig.pick.visible=false; }); };
   window.pose=(yaw,run,t,gun)=>{ H.forEach((e,n)=>{ const st={pos:new THREE.Vector3(e.x,0,0),vel:new THREE.Vector3(run?-Math.sin(yaw)*T.RUN:0,0,run?-Math.cos(yaw)*T.RUN:0),yaw,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:gun||false,ads:0,swingT:0,emote:null};
     for(let k=0;k<(t||40);k++) T.animateRig(e.h,st,1/60); e.h.rig.pick.visible=!run; }); };
   window.shoot=(cx,cy,cz,lx,ly,lz,fov)=>{ const cam=new THREE.PerspectiveCamera(fov||30,1200/700,0.05,100); cam.position.set(cx,cy,cz); cam.lookAt(lx,ly,lz); r.render(sc,cam); }; });
 const snap=async(nm,js)=>{ await pg.evaluate(js); await sleep(150); await pg.screenshot({path:`hero_${tag}_${nm}.png`}); };
 await snap('d1',()=>{ dpose(1.0); shoot(0,1.2,-8.5,0,0.95,0); });
 await snap('d2',()=>{ dpose(1.6); shoot(0,1.2,-8.5,0,0.95,0); });
console.log(await pg.evaluate(()=>JSON.stringify(H.map(e=>[e.h.rig.armL.el.rotation.x.toFixed(2),e.h.rig.armL.sh.rotation.x.toFixed(2),e.h.rig.armL.sh.rotation.z.toFixed(2)]))));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

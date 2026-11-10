// guns in the hands: node tholds.js tag id,id,id,id  -> hold_<tag>_right.png, _left.png, _back.png
const {sleep,page,launch,open}=require('./h.js'); const tag=process.argv[2]||'a', ids=(process.argv[3]||'ar,pump,smg,sniper').split(',');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,RUN'),{fast:true,norender:true,vp:{width:1300,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 await pg.evaluate((ids)=>{ document.getElementById('menu').hidden=true;
   const cv=document.createElement('canvas'); cv.width=1300; cv.height=640; cv.style.cssText='position:fixed;inset:0;z-index:99;background:#7c93ad'; document.body.appendChild(cv);
   const r=new THREE.WebGLRenderer({canvas:cv,antialias:true,preserveDrawingBuffer:true}); r.setClearColor(0x8aa0b8); r.shadowMap.enabled=true; const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xeaf2ff,0x4a5a40,0.75)); const k=new THREE.DirectionalLight(0xfff2e0,1.0); k.position.set(3,6,-4); k.castShadow=true; sc.add(k); const f=new THREE.DirectionalLight(0xbfd8ff,0.3); f.position.set(-4,3,3); sc.add(f);
   const gnd=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({color:0x6f8a5a})); gnd.rotation.x=-Math.PI/2; gnd.receiveShadow=true; sc.add(gnd);
   window.H=[]; ids.forEach((id,n)=>{ const h=T.heroFor(T.OUTFITS[[0,1,2,5,9][n%5]]); h.group.traverse(o=>{ if(o.isMesh){ o.castShadow=o.receiveShadow=true; } }); sc.add(h.group); H.push({h,z:(n-(ids.length-1)/2)*1.5,id}); });
   H.forEach(e=>{ const st={pos:new THREE.Vector3(0,0,e.z),vel:new THREE.Vector3(0,0,0),yaw:0,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:e.id,wpn:e.id,ads:0,swingT:0,emote:null}; for(let k=0;k<60;k++) T.animateRig(e.h,st,1/60); });
   window.shoot=(cx,cy,cz,lx,ly,lz,fov)=>{ const cam=new THREE.PerspectiveCamera(fov||30,1300/640,0.05,100); cam.position.set(cx,cy,cz); cam.lookAt(lx,ly,lz); r.render(sc,cam); return cv.toDataURL('image/png'); }; },ids);
 const snap=async(nm,js)=>{ const u=await pg.evaluate(js); require('fs').writeFileSync(`hold_${tag}_${nm}.png`,Buffer.from(u.split(',')[1],'base64')); };
 const span=ids.length*1.5;
 await snap('right',`shoot(${span*0.95+0.6},1.35,-0.35,0,1.2,-0.35,34)`);
 await snap('left',`shoot(${-span*0.95-0.6},1.35,-0.35,0,1.2,-0.35,34)`);
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

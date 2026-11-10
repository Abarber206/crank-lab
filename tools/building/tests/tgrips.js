// every gun in the hands, close up from both sides:  node tgrips.js out.png id,id,...
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,BASE_WEAPONS'),{fast:true,norender:true,vp:{width:1300,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 const url=await pg.evaluate((ids)=>{ ids=ids?ids.split(','):Object.keys(T.BASE_WEAPONS); const CW=300, CH=210, cols=4, rows=Math.ceil(ids.length*2/cols);
   const cv=document.createElement('canvas'); cv.width=cols*CW; cv.height=rows*CH; const cx=cv.getContext('2d');
   const R=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); R.setPixelRatio(1); R.setSize(CW,CH); R.setClearColor(0x8aa0b8);
   const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xeaf2ff,0x4a5a40,0.9)); const k=new THREE.DirectionalLight(0xfff2e0,0.8); k.position.set(3,6,-4); sc.add(k); const k2=new THREE.DirectionalLight(0xfff2e0,0.5); k2.position.set(-3,2,-4); sc.add(k2);
   const h=T.heroFor(T.OUTFITS[8]); sc.add(h.group); const cam=new THREE.PerspectiveCamera(20,CW/CH,0.05,100);
   ids.forEach((id,n)=>{ const st={pos:new THREE.Vector3(0,0,0),vel:new THREE.Vector3(0,0,0),yaw:0,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:id,wpn:id,ads:0,swingT:0,emote:null};
     h.anim.equip=0; for(let q=0;q<70;q++){ h.anim.equip=0; h.anim.idleT=0; T.animateRig(h,st,1/60); }
     [[1.9,1.42,-0.45],[-1.9,1.2,-0.6]].forEach((c,v)=>{ cam.position.set(c[0],c[1],c[2]); cam.lookAt(0.02*Math.sign(c[0]),1.32,v?-0.55:-0.45); R.render(sc,cam); const i=n*2+v; cx.drawImage(R.domElement,(i%cols)*CW,Math.floor(i/cols)*CH); cx.fillStyle='#10151c'; cx.font='bold 13px sans-serif'; cx.fillText(id+(v?' (left)':' (right)'),(i%cols)*CW+6,Math.floor(i/cols)*CH+15); }); });
   return cv.toDataURL('image/png'); },process.argv[3]||'');
 fs.writeFileSync(process.argv[2]||'grips.png',Buffer.from(url.split(',')[1],'base64')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

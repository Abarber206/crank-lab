// a contact sheet of every gun model, side-on:  node tguns.js out.png [id,id,...] [cols] [cellW] [cellH]
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,iconModel,WEAPONS,BASE_WEAPONS'),{fast:true,norender:true,vp:{width:1300,height:900}});
 await pg.waitForFunction(()=>window.T&&T.iconModel&&T.BASE_WEAPONS,null,{timeout:120000}); await sleep(300);
 const url=await pg.evaluate(([ids,cols,CW,CH])=>{ ids=ids?ids.split(','):Object.keys(T.BASE_WEAPONS); const rows=Math.ceil(ids.length/cols);
   const cv=document.createElement('canvas'); cv.width=cols*CW; cv.height=rows*CH; const cx=cv.getContext('2d'); cx.fillStyle='#8fa3b8'; cx.fillRect(0,0,cv.width,cv.height);
   const R=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true}); R.setPixelRatio(1); R.setSize(CW,CH); R.setClearColor(0,0);
   const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff,0x4a5568,0.9)); const k=new THREE.DirectionalLight(0xffffff,0.9); k.position.set(-2,3,5); sc.add(k); const rim=new THREE.DirectionalLight(0xbfe4ff,0.55); rim.position.set(3,2,-4); sc.add(rim);
   const cam=new THREE.OrthographicCamera(-1,1,1,-1,0.01,50); cam.position.set(0,0,10); cam.lookAt(0,0,0);
   ids.forEach((id,n)=>{ const m=T.iconModel(id); sc.add(m); m.updateMatrixWorld(true); const bb=new THREE.Box3().setFromObject(m), c=bb.getCenter(new THREE.Vector3()), sz=bb.getSize(new THREE.Vector3()); const half=Math.max(sz.x/2*1.06,sz.y/2*1.06*CW/CH,0.32);
     m.position.sub(c); cam.left=-half; cam.right=half; cam.top=half*CH/CW; cam.bottom=-half*CH/CW; cam.updateProjectionMatrix(); R.render(sc,cam); cx.drawImage(R.domElement,(n%cols)*CW,Math.floor(n/cols)*CH); sc.remove(m);
     cx.fillStyle='#10151c'; cx.font='bold 15px sans-serif'; cx.fillText(id+' — '+T.WEAPONS[id].name,(n%cols)*CW+8,Math.floor(n/cols)*CH+18); });
   return cv.toDataURL('image/png'); },[process.argv[3]||'',+(process.argv[4]||4),+(process.argv[5]||320),+(process.argv[6]||150)]);
 fs.writeFileSync(process.argv[2]||'guns.png',Buffer.from(url.split(',')[1],'base64')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

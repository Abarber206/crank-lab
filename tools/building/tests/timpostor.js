const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,IMP,impostorGeo,FOREST'),{vp:{width:1280,height:800}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.FOREST&&T.IMP.rt,null,{timeout:180000});
 const url=await pg.evaluate(()=>{ const rt=T.IMP.rt, W=rt.width, H=rt.height, px=new Uint8Array(W*H*4); T.renderer.readRenderTargetPixels(rt,0,0,W,H,px); const c=document.createElement('canvas'); c.width=W; c.height=H; const g=c.getContext('2d'), im=g.createImageData(W,H);
   for(let y=0;y<H;y++) for(let x=0;x<W;x++){ const s=((H-1-y)*W+x)*4, d=(y*W+x)*4; im.data[d]=px[s]; im.data[d+1]=px[s+1]; im.data[d+2]=px[s+2]; im.data[d+3]=255; } g.putImageData(im,0,0); return c.toDataURL('image/png')+'|'+W+'x'+H+' tile '+T.IMP.tile+' cols '+T.IMP.cols; });
 const [u,info]=url.split('|'); console.log(info); require('fs').writeFileSync('/home/claude/work/imp_atlas.png',Buffer.from(u.split(',')[1],'base64'));
 // a row of impostors, close
 const u2=await pg.evaluate(()=>{ const THREE=window.THREE, sc=new THREE.Scene(); sc.background=new THREE.Color(0x88aacc); sc.add(new THREE.AmbientLight(0xffffff,0.6)); const dl=new THREE.DirectionalLight(0xffffff,0.6); dl.position.set(3,5,2); sc.add(dl);
   for(let v=0;v<8;v++){ const m=new THREE.InstancedMesh(T.impostorGeo('tree',v,3),T.IMP.mat,1); m.setMatrixAt(0,new THREE.Matrix4().makeTranslation((v-3.5)*9,0,0)); sc.add(m); }
   const cam=new THREE.PerspectiveCamera(50,1280/800,0.5,500); cam.position.set(0,6,45); cam.lookAt(0,5,0); T.renderer.setRenderTarget(null); T.renderer.render(sc,cam); return T.renderer.domElement.toDataURL('image/png'); });
 require('fs').writeFileSync('/home/claude/work/imp_row.png',Buffer.from(u2.split(',')[1],'base64')); console.log(errs.slice(0,3)); await b.close(); })();

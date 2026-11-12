// all pickaxes side by side (head up, handle down), big enough to judge the shapes.  node tpickrow.js out.png
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const out=process.argv[2]||'/home/claude/work/picks.png'; const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,OUTFITS,PICKAXES,heroFor'),{vp:{width:1600,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.PICKAXES,null,{timeout:180000}); await sleep(1500);
 const url=await pg.evaluate(()=>{ const THREE=window.THREE, L=T.PICKAXES, cols=9, rows=Math.ceil(L.length/cols), W=170*cols, H=300*rows, cv=document.createElement('canvas'); cv.width=W; cv.height=H;
   const r=new THREE.WebGLRenderer({canvas:cv,antialias:true}); r.setSize(W,H,false); r.outputEncoding=T.renderer.outputEncoding; r.toneMapping=T.renderer.toneMapping; r.toneMappingExposure=T.renderer.toneMappingExposure;
   const sc=new THREE.Scene(); sc.background=new THREE.Color(0x3a4a66); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x40384a,0.8)); const k=new THREE.DirectionalLight(0xfff1dc,1.1); k.position.set(-3,5,-6); sc.add(k); const f=new THREE.DirectionalLight(0xbfd6ff,0.5); f.position.set(5,3,-4); sc.add(f);
   L.forEach((p,i)=>{ const h=T.heroFor(T.OUTFITS[0],p.id), pg=h.rig.pick; pg.parent.remove(pg); pg.position.set(0,0,0); pg.rotation.set(0,0,0); pg.updateMatrixWorld(true); const bb=new THREE.Box3().setFromObject(pg), c=bb.getCenter(new THREE.Vector3());
     const g=new THREE.Group(); g.add(pg); pg.position.sub(c); g.rotation.y=Math.PI/2; g.position.set(-(i%cols)*1.1,-Math.floor(i/cols)*2.0,0); sc.add(g); });
   const cam=new THREE.OrthographicCamera(-0.55,cols*1.1-0.55,1.0,1.0-rows*2.0,0.1,50); cam.position.set(0,0,-8); cam.lookAt(0,0,0); r.render(sc,cam); return cv.toDataURL('image/png'); });
 require('fs').writeFileSync(out,Buffer.from(url.split(',')[1],'base64')); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

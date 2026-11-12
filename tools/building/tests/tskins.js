// every outfit standing in a row (front and back), lit like the Locker, for judging the skins.  node tskins.js out.png [ids]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const out=process.argv[2]||'/home/claude/work/skins.png'; const {pg,errs}=await open(b,page(process.env.FILE||'/home/claude/crank-lab/index.html','scene,renderer,OUTFITS,heroFor'),{vp:{width:1600,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000}); await sleep(1500);
 const ids=process.argv[3]?process.argv[3].split(','):null; const back=!!process.env.BACK, side=!!process.env.SIDE;
 const url=await pg.evaluate(([ids,back,side])=>{ const THREE=window.THREE; const L=T.OUTFITS.filter(o=>!ids||ids.includes(o.id)); const cols=Math.min(L.length,10), rows=Math.ceil(L.length/cols);
   const W=160*cols, H=330*rows, cv=document.createElement('canvas'); cv.width=W; cv.height=H; const r=new THREE.WebGLRenderer({canvas:cv,antialias:true}); r.setSize(W,H,false); r.outputEncoding=T.renderer.outputEncoding; r.toneMapping=T.renderer.toneMapping; r.toneMappingExposure=T.renderer.toneMappingExposure;
   const sc=new THREE.Scene(); sc.background=new THREE.Color(0x3a4a66); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x40384a,0.75)); const k=new THREE.DirectionalLight(0xfff1dc,1.1); k.position.set(-3,5,-6); sc.add(k); const f=new THREE.DirectionalLight(0xbfd6ff,0.45); f.position.set(5,3,-4); sc.add(f); const rim=new THREE.DirectionalLight(0xffffff,0.5); rim.position.set(0,4,6); sc.add(rim);
   L.forEach((o,i)=>{ const h=T.heroFor(o,'steel'); h.group.position.set((back?1:-1)*(i%cols)*1.1,-Math.floor(i/cols)*2.25,0); if(side) h.group.rotation.y=Math.PI/2; sc.add(h.group); });
   const cam=new THREE.OrthographicCamera(-0.55,cols*1.1-0.55,1.95,1.95-rows*2.25,0.1,50); cam.position.set(0,0,back?8:-8); cam.lookAt(0,0,0);
   r.render(sc,cam); return cv.toDataURL('image/png'); },[ids,back,side]);
 require('fs').writeFileSync(out,Buffer.from(url.split(',')[1],'base64')); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

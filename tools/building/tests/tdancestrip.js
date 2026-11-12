// a dance as a strip of frames, front row and side row, for judging the poses.  node tdancestrip.js id out.png [frames] [outfit]
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const id=process.argv[2]||'dance', out=process.argv[3]||'/home/claude/work/ds.png', N=+(process.argv[4]||8), oid=process.argv[5]||'rook';
 const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,OUTFITS,heroFor,animateRig,EMOTES'),{vp:{width:1600,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000}); await sleep(1000);
 const url=await pg.evaluate(([id,N,oid,OFF,SPAN])=>{ const THREE=window.THREE, E=T.EMOTES[id], W=150*N, H=600, cv=document.createElement('canvas'); cv.width=W; cv.height=H;
   const r=new THREE.WebGLRenderer({canvas:cv,antialias:true}); r.setSize(W,H,false); r.outputEncoding=T.renderer.outputEncoding; r.toneMapping=T.renderer.toneMapping;
   const sc=new THREE.Scene(); sc.background=new THREE.Color(0x3a4a66); sc.add(new THREE.HemisphereLight(0xdfe9ff,0x40384a,0.8)); const k=new THREE.DirectionalLight(0xfff1dc,1.0); k.position.set(-3,5,-6); sc.add(k); const k2=new THREE.DirectionalLight(0xfff1dc,0.5); k2.position.set(6,4,2); sc.add(k2);
   const o=T.OUTFITS.find(x=>x.id===oid)||T.OUTFITS[0]; const span=SPAN||Math.min(E.dur-0.6,(E.beat?8/E.beat:E.dur-0.6));
   for(let row=0;row<2;row++) for(let i=0;i<N;i++){ const h=T.heroFor(o,'steel'), z=new THREE.Vector3(), t=0.5+span*i/(N-1)+OFF;
     const S={bare:true,pos:z,vel:new THREE.Vector3(),yaw:0,pitch:-0.05,onGround:true,crouch:false,building:false,editing:false,gun:false,ads:0,swingT:0,emote:{id,t:0}};
     for(let q=0;q<=40;q++){ S.emote.t=t-(40-q)/60; if(S.emote.t<0) S.emote.t=0; T.animateRig(h,S,1/60); }
     h.group.position.set(-i*1.5,-row*3,0); h.group.rotation.y=row?Math.PI/2:0; sc.add(h.group); }
   const cam=new THREE.OrthographicCamera(0.75,-(N-1)*1.5-0.75,2.2,2.2-6,0.1,50); cam.position.set(0,0,-8); cam.lookAt(0,0,0); cam.left=-0.75; cam.right=(N-1)*1.5+0.75; cam.updateProjectionMatrix();
   cam.position.set(-(N-1)*0.75,0,-8); cam.left=-(N*0.75); cam.right=N*0.75; cam.top=2.2; cam.bottom=-3.8; cam.updateProjectionMatrix(); cam.lookAt(-(N-1)*0.75,0,0);
   r.render(sc,cam); return cv.toDataURL('image/png'); },[id,N,oid,+(process.env.OFF||0),+(process.env.SPAN||0)]);
 require('fs').writeFileSync(out,Buffer.from(url.split(',')[1],'base64')); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

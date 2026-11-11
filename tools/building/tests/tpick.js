// close-ups of the pickaxe hold: node tpick.js out.png pickId [outfit]
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,EMOTES,RUN,SWING_T'),{fast:true,norender:true,vp:{width:1300,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 await pg.evaluate(v=>{window.__sw=v;},+(process.env.SW||0)); const url=await pg.evaluate(([pk,of])=>{ const CW=420, CH=420; const views=[[0.3,1.0,5,0.95,5],[-1.2,1.3,5,0.95,5],[1.6,1.2,5,0.95,5],[0,1.1,26,.98,5.2]];
   const cv=document.createElement('canvas'); cv.width=views.length*CW; cv.height=CH; const cx=cv.getContext('2d');
   const R=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); R.setPixelRatio(1); R.setSize(CW,CH); R.setClearColor(0x2244cc);
   const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xeaf2ff,0x4a5a40,0.85)); const k=new THREE.DirectionalLight(0xfff2e0,0.9); k.position.set(3,6,-4); sc.add(k);
   const h=T.heroFor(T.OUTFITS[of],pk); sc.add(h.group);
   const st={pos:new THREE.Vector3(0,0,0),vel:new THREE.Vector3(0,0,0),yaw:0,pitch:0,onGround:true,crouch:false,building:false,editing:false,gun:false,down:null,ads:0,swingT:0,emote:null};
   if(window.__sw===2){ st.building='wall'; } for(let q=0;q<90;q++) T.animateRig(h,st,1/60);
   h.group.updateMatrixWorld(true); const hw=h.rig.armR.hand.getWorldPosition(new THREE.Vector3());
   if(window.__sw===1){ let i=0; for(const side of [0,1]){ const N=Math.round(T.SWING_T*60); for(let f=0;f<=N;f++){ st.swingT=T.SWING_T*(1-f/N)+0.001; T.animateRig(h,st,1/60); const u=f/N; if([0.22,0.44,0.7].some(x=>Math.abs(u-x)<0.5/N)){ const cam=new THREE.PerspectiveCamera(22,1,0.05,100); cam.position.set(1.6,1.5,-5); cam.lookAt(0,1.05,0); R.render(sc,cam); cx.drawImage(R.domElement,70,0,280,420,i*280,0,280,420); i++; } } st.swingT=0; for(let q=0;q<20;q++) T.animateRig(h,st,1/60); } } else views.forEach((v,i)=>{ const cam=new THREE.PerspectiveCamera(v[2],1,0.05,100); cam.position.set(Math.sin(v[0])*v[4],v[1],-Math.cos(v[0])*v[4]); if(i<3) cam.lookAt(hw.x,hw.y,hw.z); else cam.lookAt(0,v[3],0); R.render(sc,cam); cx.drawImage(R.domElement,i*CW,0); });
   return cv.toDataURL('image/png'); },[process.argv[3]||'shovel',+(process.argv[4]||0)]);
 fs.writeFileSync(process.argv[2]||'pick.png',Buffer.from(url.split(',')[1],'base64')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

// a film strip of an emote (or any state):  node tposes.js out.png emoteId t0 t1 n [outfit] [camYaw]
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,heroFor,OUTFITS,animateRig,EMOTES,RUN'),{fast:true,norender:true,vp:{width:1300,height:700}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.OUTFITS,null,{timeout:180000});
 await pg.evaluate(([r,c,g,rl,f,ly])=>{ window.__run=r; window.__crouch=c; window.__gun=g; window.__rl=rl; window.__fov=f; window.__ly=ly; },[+(process.env.RUN||0),+(process.env.CROUCH||0),process.env.GUN||'',+(process.env.RELOAD||0),+(process.env.FOV||0),+(process.env.LY||0)]);
 const url=await pg.evaluate(([id,t0,t1,n,of,cy])=>{ const CW=200, CH=330, cols=Math.min(n,8), rows=Math.ceil(n/cols);
   const cv=document.createElement('canvas'); cv.width=cols*CW; cv.height=rows*CH; const cx=cv.getContext('2d');
   const R=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}); R.setPixelRatio(1); R.setSize(CW,CH); R.setClearColor(0x8aa0b8);
   const sc=new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xeaf2ff,0x4a5a40,0.85)); const k=new THREE.DirectionalLight(0xfff2e0,0.9); k.position.set(3,6,-4); sc.add(k);
   const gnd=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshLambertMaterial({color:0x6f8a5a})); gnd.rotation.x=-Math.PI/2; sc.add(gnd);
   const h=T.heroFor(T.OUTFITS[of]); sc.add(h.group); const cam=new THREE.PerspectiveCamera(26,CW/CH,0.05,100); if(window.__gun){ cam.fov=window.__fov||16; cam.updateProjectionMatrix(); cam.position.set(Math.sin(cy)*3.4,1.3,-Math.cos(cy)*3.4-0.3); cam.lookAt(0,window.__ly||1.22,-0.3); } else { cam.position.set(Math.sin(cy)*5.2,1.25,-Math.cos(cy)*5.2); cam.lookAt(0,0.98,0); }
   const st={pos:new THREE.Vector3(0,0,0),vel:new THREE.Vector3(0,0,-(+(window.__run||0))*T.RUN),yaw:0,pitch:0,onGround:true,crouch:!!window.__crouch,building:false,editing:false,gun:window.__gun||false,wpn:window.__gun||undefined,ads:0,swingT:0,emote:id==='none'?null:{id,t:0}};
   let t=0; for(let q=0;q<30;q++) T.animateRig(h,Object.assign({},st,{emote:null}),1/60);
   for(let f=0;f<n;f++){ const tt=t0+(t1-t0)*f/Math.max(1,n-1); while(t<tt-1e-6){ t+=1/60; if(st.emote) st.emote.t=t; if(window.__rl) st.reload={w:window.__gun,p:Math.min(1,t/t1)}; h.anim.equip=0; T.animateRig(h,st,1/60); } if(!window.__gun) h.rig.pick.visible=false; R.render(sc,cam); cx.drawImage(R.domElement,(f%cols)*CW,Math.floor(f/cols)*CH); cx.fillStyle='#10151c'; cx.font='12px sans-serif'; cx.fillText(tt.toFixed(2)+'s',(f%cols)*CW+4,Math.floor(f/cols)*CH+12); }
   return cv.toDataURL('image/png'); },[process.argv[3]||'dance',+(process.argv[4]||0),+(process.argv[5]||2),+(process.argv[6]||8),+(process.argv[7]||0),+(process.argv[8]||0)]);
 fs.writeFileSync(process.argv[2]||'poses.png',Buffer.from(url.split(',')[1],'base64')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

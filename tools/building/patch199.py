# patch199: phones. The page used to make up to four WebGL contexts (the game, the item pictures, the locker portraits,
# the lobby stage) and photograph the whole island while the lobby was up; on a phone that's a lot of memory, the lobby
# was slow and turning the phone could tip it over. Now:
#  - item pictures and locker portraits are drawn by the game's own renderer into an offscreen target (2x, scaled down
#    smoothly), so there's no extra context; the locker portraits wait until you open the Locker on a phone
#  - the island photo for the map is taken when a match loads (not in the lobby) on a phone
#  - phones keep the shorter draw distances and a smaller indoor-light map, and the lobby stage draws at a lower resolution
#  - if the browser drops the graphics context anyway (memory), the game puts up a note and reloads instead of dying
rep("function renderIcon(id){","""// a renderer-shaped stand-in that draws with the game's own renderer into an offscreen target (no extra WebGL context)
function offRenderer(){ const o={w:128,h:128,ss:2,rt:null,clr:new THREE.Color(0),ca:0,cv:document.createElement('canvas'),big:document.createElement('canvas')};
  o.setPixelRatio=()=>{}; o.setClearColor=(c,a)=>{ o.clr.set(c); o.ca=a==null?1:a; }; o.setSize=(w,h)=>{ o.w=w; o.h=h; o.cv.width=w; o.cv.height=h; }; o.setSize(128,128);
  o.render=(sc,cam)=>{ const W=o.w*o.ss, H=o.h*o.ss; if(!o.rt||o.rt.width!==W||o.rt.height!==H){ if(o.rt) o.rt.dispose(); o.rt=new THREE.WebGLRenderTarget(W,H,{format:THREE.RGBAFormat}); }
    const pr=renderer.getRenderTarget(), pc=renderer.getClearColor(new THREE.Color()), pa=renderer.getClearAlpha(), sa=renderer.shadowMap.autoUpdate, sn=renderer.shadowMap.needsUpdate, tm=renderer.toneMapping;
    try{ renderer.setRenderTarget(o.rt); renderer.setClearColor(o.clr,o.ca); renderer.clear(); renderer.shadowMap.autoUpdate=false; renderer.toneMapping=THREE.NoToneMapping; renderer.render(sc,cam);
      const buf=new Uint8Array(W*H*4); renderer.readRenderTargetPixels(o.rt,0,0,W,H,buf); o.big.width=W; o.big.height=H; const g=o.big.getContext('2d'), id=g.createImageData(W,H);
      for(let y=0;y<H;y++) id.data.set(buf.subarray((H-1-y)*W*4,(H-y)*W*4),y*W*4); g.putImageData(id,0,0);
      const c=o.cv.getContext('2d'); c.clearRect(0,0,o.w,o.h); c.imageSmoothingEnabled=true; c.imageSmoothingQuality='high'; c.drawImage(o.big,0,0,o.w,o.h); }
    finally{ renderer.setRenderTarget(pr); renderer.setClearColor(pc,pa); renderer.shadowMap.autoUpdate=sa; renderer.shadowMap.needsUpdate=sn; renderer.toneMapping=tm; } };
  o.domElement=o.cv; o.dispose=()=>{ if(o.rt){ o.rt.dispose(); o.rt=null; } }; return o; }
function renderIcon(id){""")
rep("iconR=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});","iconR=offRenderer();")
rep("""  setTimeout(()=>{ try{
    const W=168, Hh=224, r=new THREE.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});""","""  window._lockerPics=()=>{ if(window._lockerPicsDone) return; window._lockerPicsDone=1;
  setTimeout(()=>{ try{
    const W=168, Hh=224, r=offRenderer();""")
rep("""    r.dispose(); if(r.forceContextLoss) r.forceContextLoss();
  }catch(e){} },60);""","""    r.dispose();
  }catch(e){} },60); }; if(!isTouch) setTimeout(()=>window._lockerPics(),1500); // (on a phone: when you open the Locker)""")
rep("""function showTab(name){""","""function showTab(name){ if(name==='locker'&&window._lockerPics) setTimeout(()=>window._lockerPics(),30);""")
# the map photo: not in the lobby on a phone
rep("""  if(!bigMapImg) try{ bigMapImg=renderBigMapImage(); }catch(e){}
  if(bigMapImg){ const k=bigMapImg.width""","""  if(!bigMapImg&&!(isTouch&&(LOBBY.on||!playing))) try{ bigMapImg=renderBigMapImage(); }catch(e){}
  if(bigMapImg){ const k=bigMapImg.width""")
# phones keep the old draw distances
rep("const TLOD=[230,640];","const TLOD=isTouch?[170,480]:[230,640];")
rep("const NEAR_TREE=150, MID_TREE=390, FAR_TREE=1500;","const NEAR_TREE=isTouch?115:150, MID_TREE=isTouch?290:390, FAR_TREE=1500;")
rep("const INDOOR={tex:null,dummy:null,N:2048,","const INDOOR={tex:null,dummy:null,N:isTouch?1024:2048,")
rep("""function stageInit(){ const c=$('stageC'), r=new THREE.WebGLRenderer({canvas:c,antialias:true,alpha:true}); r.setClearColor(0,0); r.setPixelRatio(Math.min(devicePixelRatio,2));""","""function stageInit(){ const c=$('stageC'), r=new THREE.WebGLRenderer({canvas:c,antialias:!isTouch,alpha:true,powerPreference:'default'}); r.setClearColor(0,0); r.setPixelRatio(Math.min(devicePixelRatio,isTouch?1.25:2));""")
# the graphics context lost (out of memory): say so and reload, rather than freeze
rep("""addEventListener('resize',fitView);""","""addEventListener('resize',fitView);
canvas.addEventListener('webglcontextlost',e=>{ e.preventDefault(); try{ const d=document.createElement('div'); d.textContent='Reloading graphics…'; d.style.cssText='position:fixed;inset:0;z-index:99;display:flex;align-items:center;justify-content:center;background:#0b1430;color:#fff;font:800 20px sans-serif'; document.body.appendChild(d); }catch(_){} setTimeout(()=>location.reload(),900); },false);""")

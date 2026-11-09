// the glider noses down in a dive and up in a climb: side-view shots plus its world pitch
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,skyDrop,deployGlider,settings,renderer,camera,localHero'),{vp:{width:900,height:520}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000});
 await pg.evaluate(()=>{ T.skyDrop(T.P.pos.x,T.P.pos.z,700); T.P.sky.t=5; T.deployGlider(T.P); window._pt=0; setInterval(()=>{ T.P.pitch=window._pt; },16);
   window.cam=new THREE.PerspectiveCamera(40,900/520,0.1,3000); const R0=T.renderer.render.bind(T.renderer); T.renderer.render=(s,c)=>{ if(c===T.camera){ const p=T.P.pos, y=T.P.yaw, rx=Math.cos(y), rz=-Math.sin(y); cam.position.set(p.x+rx*7,p.y+1.6,p.z+rz*7); cam.lookAt(p.x,p.y+1.2,p.z); R0(s,cam); } else R0(s,c); }; });
 const pitchOf=()=>pg.evaluate(()=>{ const g=T.localHero.glider; if(!g) return null; const q=new THREE.Quaternion(); g.getWorldQuaternion(q); const n=new THREE.Vector3(0,0,-1).applyQuaternion(q); return +Math.asin(n.y).toFixed(2); });
 const out={};
 for(const [nm,p,cond] of [['level',0,'Math.abs((T.localHero.anim.glP||0)+0.11)<0.06'],['dive',-0.8,'(T.localHero.anim.glP||0)<-0.85']]){ await pg.evaluate(p=>{ window._pt=p; },p); await pg.waitForFunction(cond,null,{timeout:120000}).catch(()=>{}); out[nm]=await pitchOf(); await pg.screenshot({path:'gt_'+nm+'.png'}); }
 console.log(JSON.stringify(out), out.dive<out.level-0.3?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

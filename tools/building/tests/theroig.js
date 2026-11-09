// the hero in the real game lighting: close front and back, and the normal third-person view
const {sleep,page,launch,open}=require('./h.js'); const tag=process.argv[2]||'a';
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,localHero'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); });
 await pg.waitForFunction(()=>T.renderer.info.render.frame>5,null,{timeout:120000}); await sleep(2500);
 await pg.screenshot({path:`hig_${tag}_tp.png`});
 await pg.evaluate(()=>{ window.cam=new THREE.PerspectiveCamera(32,1100/640,0.05,3000); const Rr=T.renderer.render.bind(T.renderer); T.renderer.render=(s,cc)=>Rr(s,cc===T.camera?cam:cc); });
 const at=async(nm,fx,fy,fz,ly)=>{ await pg.evaluate(([fx,fy,fz,ly])=>{ const p=T.P.pos, y=T.P.yaw, f=[-Math.sin(y),-Math.cos(y)], r=[Math.cos(y),-Math.sin(y)]; cam.position.set(p.x+f[0]*fz+r[0]*fx,p.y+fy,p.z+f[1]*fz+r[1]*fx); cam.lookAt(p.x,p.y+ly,p.z); },[fx,fy,fz,ly]); await sleep(1200); await pg.screenshot({path:`hig_${tag}_${nm}.png`}); };
 await at('front',0.5,1.3,2.6,1.05); await at('back',-0.4,1.4,-2.4,1.1); await at('face',0.15,1.62,1.1,1.5);
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

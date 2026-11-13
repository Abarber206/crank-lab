// river banks: a few views of where the river meets the grass
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,camera,TOD,terrainH,WORLD,SPAWN,localHero'),{vp:{width:1100,height:640}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.WORLD&&T.WORLD.rivers,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(3000);
 const tag=process.argv[2]||'now';
 for(const [n,fr,side,h] of [['a',0.35,1,2.2],['b',0.6,-1,6],['c',0.45,1,1.6]]){
   const sp=await pg.evaluate(([fr,side,h])=>{ const rv=T.WORLD.rivers.find(r=>r.main)||T.WORLD.rivers[0], p=rv.pts, q=Math.floor(p.length*fr), a=p[q], c=p[Math.min(p.length-1,q+6)], tx=c[0]-a[0], tz=c[1]-a[1], tl=Math.hypot(tx,tz)||1, nx=-tz/tl, nz=tx/tl, w=a[3];
     const x=T.SPAWN[0]+a[0]+nx*side*(w+7), z=T.SPAWN[2]+a[1]+nz*side*(w+7); T.P.pos.set(x,T.terrainH(x,z),z); T.TOD.fix=0.3; return {x,z,lx:T.SPAWN[0]+a[0]+tx/tl*20-nx*side*w*0.3,lz:T.SPAWN[2]+a[1]+tz/tl*20-nz*side*w*0.3,h}; },[fr,side,h]); await sleep(3500);
   const u=await pg.evaluate(sp=>{ const cam=new THREE.PerspectiveCamera(60,1100/640,0.1,3000); cam.position.set(sp.x,T.terrainH(sp.x,sp.z)+sp.h,sp.z); cam.lookAt(sp.lx,T.terrainH(sp.lx,sp.lz),sp.lz); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.88); },sp);
   require('fs').writeFileSync('/home/claude/work/river_'+n+'_'+tag+'.jpg',Buffer.from(u.split(',')[1],'base64')); }
 console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

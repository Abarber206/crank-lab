// one oak (and one pine) on its own, from four sides, so the shape of the crown can be checked
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,propVariant'),{vp:{width:1200,height:600}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.propVariant,null,{timeout:180000}); await sleep(1500);
 const u=await pg.evaluate(()=>{ const sc=new THREE.Scene(); sc.background=new THREE.Color(0x9cc8ee); sc.add(new THREE.HemisphereLight(0xffffff,0x557744,0.7)); const sun=new THREE.DirectionalLight(0xfff2d8,0.9); sun.position.set(3,6,2); sc.add(sun);
   const W=1200,H=600, c=document.createElement('canvas'); c.width=W; c.height=H; const g=c.getContext('2d');
   const cell=(kind,v,a,ix,iy)=>{ const V=T.propVariant(kind,v), m=new THREE.Mesh(V.geo,V.mat); sc.add(m); const cam=new THREE.PerspectiveCamera(45,300/300,0.1,100), D=kind==='tree'?12:13; cam.position.set(Math.cos(a)*D,4,Math.sin(a)*D); cam.lookAt(0,kind==='tree'?4.2:3.6,0);
     T.renderer.setSize(300,300,false); T.renderer.render(sc,cam); g.drawImage(T.renderer.domElement,ix*300,iy*300,300,300); sc.remove(m); };
   for(let k=0;k<4;k++) cell('tree',k*2,k*1.6,k,0); for(let k=0;k<4;k++) cell('pine',k*2+1,k*1.6,k,1);
   return c.toDataURL('image/jpeg',0.85); });
 require('fs').writeFileSync('/home/claude/work/oak_iso.jpg',Buffer.from(u.split(',')[1],'base64')); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

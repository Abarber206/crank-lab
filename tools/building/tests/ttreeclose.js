// close-ups: a few oaks and pines as you'd see them standing next to them, at midday
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,renderer,camera,scene,settings,TOD,terrainH,FOREST,localHero'),{vp:{width:1280,height:720}});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.FOREST&&T.FOREST.trees,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); if(s){ s.value='off'; s.dispatchEvent(new Event('change')); } document.getElementById('play').click(); }); await sleep(2500);
 const tag=process.argv[2]||'now', out=[];
 for(const kind of ['tree','pine']) for(let v=0;v<3;v++){
   const sp=await pg.evaluate(([kind,v])=>{ const ts=T.FOREST.trees.filter(p=>p.kind===kind&&p.alive&&!p.gone); const p=ts[Math.floor(ts.length*(0.2+v*0.27))]; const a=v*2.1+0.4, D=kind==='tree'?9+3*(p.s||1):7+3*(p.s||1);
     const x=p.x+Math.cos(a)*D, z=p.z+Math.sin(a)*D; T.P.pos.set(x,T.terrainH(x,z),z); T.TOD.fix=0.3; return {x,z,px:p.x,pz:p.z,s:p.s||1}; },[kind,v]); await sleep(2500);
   const u=await pg.evaluate(sp=>{ const cam=new THREE.PerspectiveCamera(60,1280/720,0.1,3000), y=T.terrainH(sp.x,sp.z)+1.7; cam.position.set(sp.x,y,sp.z); cam.lookAt(sp.px,T.terrainH(sp.px,sp.pz)+3.2*sp.s,sp.pz); T.localHero.group.visible=false; T.renderer.render(T.scene,cam); return T.renderer.domElement.toDataURL('image/jpeg',0.85); },sp);
   const f='/home/claude/work/tc_'+kind+v+'_'+tag+'.jpg'; require('fs').writeFileSync(f,Buffer.from(u.split(',')[1],'base64')); out.push(f); }
 console.log(out.join(' ')); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

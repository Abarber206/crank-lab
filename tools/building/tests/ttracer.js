// tracers and bullet streaks always leave from the gun's muzzle: standing or moving at a run, rifle, smg, sniper and shotgun, near and far.
// The game loop is paused and stepped by hand at 60 fps so the first frames of each streak are seen.
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,TOWNS,terrainH,camera,bullets,tracers,WEAPONS,selectGun,playerShoot,aimDir,settings,renderer,localHero,stepBullets,stepTracers'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.renderer,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const res=await pg.evaluate(async()=>{ const wait=ms=>new Promise(r=>setTimeout(r,ms)), out=[];
  for(const [w,sp,pitch] of [['ar',0,0.02],['ar',7,0.02],['ar',-7,0.02],['ar',7,-0.12],['pump',7,0],['smg',7,0.03],['sniper',7,0.05],['ar',30,0.02]]){
   const t=T.TOWNS[2]; T.P.pos.set(t.x+40,T.terrainH(t.x+40,t.z+40)+0.1,t.z+40); T.P.vel.set(0,0,0); T.P.yaw=2.2; T.P.pitch=pitch;
   T.P.inv[0]=w; T.P.ammo[w]=T.WEAPONS[w].mag; T.selectGun(w); T.P.equipT=0; T.P.gunT=0; T.P.reloadT=0; T.WEAPONS[w].spread=0; T.P.bloom=0;
   await wait(500); T.P.pitch=pitch; T.bullets.length=0; await wait(50);
   const d0=T.aimDir(), fwd=new THREE.Vector3(-Math.sin(T.P.yaw),0,-Math.cos(T.P.yaw)), m=new THREE.Vector3(), S=[];
   T.camera.updateMatrixWorld(); T.localHero.group.updateMatrixWorld(true); T.P.gunT=0; T.playerShoot();
   for(let f=0;f<8;f++){ // the shooter keeps moving at sp m/s along the aim; the world is stepped by hand
     T.localHero.group.position.addScaledVector(fwd,sp/60); T.localHero.group.updateMatrixWorld(true); T.stepBullets(1/60); T.stepTracers(1/60);
     T.localHero.rig.muzzle.getWorldPosition(m);
     for(const l of [...T.bullets.map(b=>b.l),...T.tracers.map(t=>t.l)]){ const pa=l.geometry.attributes.position; const a=new THREE.Vector3().fromBufferAttribute(pa,0), b=new THREE.Vector3().fromBufferAttribute(pa,1);
       if(a.distanceTo(b)<0.01) continue; S.push([f,Math.min(a.clone().sub(m).dot(d0),b.clone().sub(m).dot(d0)),Math.min(a.distanceTo(m),b.distanceTo(m))]); } }
   T.stepBullets(0.05); T.bullets.slice().forEach((b,i)=>{}); 
   const first=S.filter(s=>s[0]===S[0][0]); out.push({w,sp,pitch,n:S.length,worstBack:+Math.min(...S.map(s=>s[1])).toFixed(2),firstNear:+Math.min(...first.map(s=>s[2])).toFixed(2)}); }
  return out; });
 res.forEach(r=>console.log(JSON.stringify(r))); const ok=res.every(r=>r.n>0&&r.worstBack>-0.06&&r.firstNear<0.06); console.log(ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

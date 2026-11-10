// bullets fly: they take time, drop as the table says (true at the zero, low beyond it), stop at the ground; point blank is
// instant; shotguns stay instant; recoil climbs and settles back
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,TOWNS,terrainH,camera,bullets,BALL,bulletRise,WEAPONS,selectGun,playerShoot,aimDir,settings,castShot,pieces,get B(){return B}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS&&T.BALL,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const out={}, wait=ms=>new Promise(r=>setTimeout(r,ms)), t=T.TOWNS[2];
   const give=(w)=>{ T.P.inv[0]=w; T.P.ammo[w]=T.WEAPONS[w].mag; T.selectGun(w); T.P.equipT=0; T.P.gunT=0; T.P.reloadT=0; };
   // 1. a sniper round fired up over the town
   T.P.pos.set(t.x+3,t.h+0.1,t.z+3); T.P.vel.set(0,0,0); T.P.yaw=0.4; T.P.pitch=0.4; give('sniper'); await wait(500); T.P.pitch=0.4; T.P.kick=0; T.P.rcl=0; await wait(120);
   T.WEAPONS.sniper.spread=0; T.P.bloom=0; const d=T.aimDir(); T.playerShoot(); out.flying=T.bullets.length; const bl=T.bullets[0], S=[]; let n=0;
   const V=T.BALL.sniper[0], v0=bl.v.clone(), y0=bl.p.y, tilt=Math.asin(v0.y/v0.length())-Math.asin(d.y); out.tilt=+(tilt/(0.5*Math.asin(9.8*100/(V*V)))).toFixed(2);
   while(bl&&T.bullets.includes(bl)&&n++<400){ S.push([bl.t,bl.dist,bl.p.y-(y0+v0.y*bl.t-0.5*9.8*bl.t*bl.t)]); await wait(16); }
   const at=D=>S.reduce((a,c)=>Math.abs(c[1]-D)<Math.abs(a[1]-D)?c:a,S[0]), a100=at(100), a300=at(300);
   out.t100=+(a100[0]*100/a100[1]).toFixed(3); out.err=+Math.max(...S.map(q=>Math.abs(q[2]))).toFixed(3); out.speed=+(a300[1]/a300[0]/V).toFixed(2); out.flat300=+T.bulletRise('sniper',300).toFixed(2); out.flat100=+T.bulletRise('sniper',100).toFixed(3); out.far=+S[S.length-1][1].toFixed(0);
   // 2. fired at the ground: it lands and is gone
   T.P.pitch=-0.12; give('ar'); await wait(300); T.P.pitch=-0.12; T.playerShoot(); const had=T.bullets.length; await wait(700); out.ground=[had,T.bullets.length];
   // 3. a shotgun is still instant
   give('pump'); await wait(300); T.playerShoot(); out.pump=T.bullets.length;
   // 4. recoil climbs while firing and settles most of the way back
   T.P.pitch=0.2; give('ar'); await wait(400); T.P.pitch=0.2; T.P.rcl=0; T.P.kick=0; await wait(100); const p0=T.P.pitch; for(let q=0;q<6;q++){ T.P.gunT=0; T.playerShoot(); await wait(150); } const p1=T.P.pitch; await wait(1500); const p2=T.P.pitch;
   out.climb=+(p1-p0).toFixed(3); out.left=+(p2-p0).toFixed(3);
   // 5. a round that flies 45 m to the opponent hurts it when it lands, not before
   { const sel=document.querySelector('#botSel'); sel.value='easy'; sel.dispatchEvent(new Event('change')); await wait(1500); const Bt=T.B; out.bot=!!(Bt&&Bt.active);
     if(out.bot){ give('sniper'); T.P.bloom=0; let done=false; for(let q=0;q<10&&!done;q++){ const a=q*0.63, bx=T.P.pos.x-Math.sin(a)*45, bz=T.P.pos.z-Math.cos(a)*45; Bt.pos.set(bx,T.terrainH(bx,bz)+0.05,bz); Bt.vel.set(0,0,0);
         for(let it=0;it<3;it++){ const to=Bt.pos.clone().setY(Bt.pos.y+1.15).sub(it?T.camera.position:new THREE.Vector3(T.P.pos.x,T.P.pos.y+1.6,T.P.pos.z)); T.P.yaw=Math.atan2(-to.x,-to.z); T.P.pitch=Math.asin(to.y/to.length()); await wait(200); Bt.pos.set(bx,T.terrainH(bx,bz)+0.05,bz); Bt.vel.set(0,0,0); }
         Bt.pos.set(bx,T.terrainH(bx,bz)+0.05,bz); Bt.vel.set(0,0,0); const h=T.castShot(T.camera.position.clone(),T.aimDir(),200,4,[Bt]); if(h.kind!=='body') continue;
         const before=Bt.hp+Bt.sh; T.P.gunT=0; T.P.equipT=0; T.P.ammo.sniper=1; T.P.reloadT=0; T.playerShoot(); out.botAtOnce=before-(Bt.hp+Bt.sh); out.botFly=T.bullets.length; await wait(600); out.botAfter=+(before-(Bt.hp+Bt.sh)).toFixed(0); done=true; } out.botTried=done; } }
   return out; });
 const ok=r.flying===1&&Math.abs(r.t100-100/300)<0.03&&r.err<0.05&&Math.abs(r.tilt-1)<0.2&&r.flat300<-1.2&&Math.abs(r.flat100)<0.01&&Math.abs(r.speed-1)<0.06&&r.far>300&&r.ground[0]===1&&r.ground[1]===0&&r.pump===0&&r.climb>0.03&&r.left<r.climb*0.35&&r.bot&&r.botTried&&r.botAtOnce===0&&r.botFly===1&&r.botAfter>30;
 console.log(JSON.stringify(r), ok?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

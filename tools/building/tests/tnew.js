// interact key: chests open only when you hold it; guns wait for it, ammo doesn't; inventory keeps you moving; slot labels match; no spinning when dead; house doors
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,chests,drops,spawnDrop,useDown,useUp,openInv,closeInv,inputDown,inputUp,net,slotKeyLabel,pieces,toggleDoor,makeBoxes,settings,renderSlots,get useTgt(){return useTgt},get invOpen(){return invOpen}'),{fast:true,vp:{width:640,height:400}});
 const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+JSON.stringify(d));
 await pg.waitForFunction(()=>window.T&&T.scene,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); });
 await pg.evaluate(()=>document.getElementById('play').click()); await pg.waitForFunction(()=>window.T&&T.P,null,{timeout:120000}); await sleep(3000);
 await pg.evaluate(()=>{ T.scene.visible=false; }); // logic only, fast frames
 const frames=n=>pg.evaluate(n=>new Promise(r=>{ let k=0; const f=()=>{ if(++k>=n) r(); else requestAnimationFrame(f); }; requestAnimationFrame(f); }),n);
 const hold=(fn,n)=>pg.evaluate(async([fs,n])=>{ const f=eval(fs); for(let k=0;k<n;k++){ f(); await new Promise(r=>requestAnimationFrame(r)); } },[fn.toString(),n]);
 // chest: standing at it does nothing; holding Interact opens it
 await pg.evaluate(()=>{ const c=T.chests.find(c=>!c.open); window.CH=c; T.P.pos.set(c.x-Math.sin(c.yaw)*1.4,c.y,c.z-Math.cos(c.yaw)*1.4); T.P.yaw=Math.atan2(-(c.x-T.P.pos.x),-(c.z-T.P.pos.z)); T.P.vel.set(0,0,0); });
 await hold(()=>{ T.P.vel.set(0,0,0); },60);
 const c1=await pg.evaluate(()=>({open:CH.open,tgt:T.useTgt&&T.useTgt.kind,prompt:document.getElementById('useT').textContent,shown:!document.getElementById('chestBar').hidden,key:document.getElementById('useK').textContent}));
 await pg.evaluate(()=>T.useDown()); await hold(()=>{ T.P.vel.set(0,0,0); },80); await pg.evaluate(()=>T.useUp());
 const c2=await pg.evaluate(()=>CH.open);
 ok('a chest doesn\'t open by itself; the prompt shows; holding Interact opens it',!c1.open&&c1.tgt==='chest'&&c1.shown&&c2,{before:c1,openedAfterHold:c2});
 // guns wait for Interact; ammo is picked up by walking over it
 await pg.evaluate(()=>{ T.P.pos.set(2,0,2); T.P.vel.set(0,0,0); T.P.inv=[null,null,null,null,null]; T.renderSlots(); const g=T.spawnDrop('ar',30,new THREE.Vector3(2,0.2,1.2),new THREE.Vector3(),9001); window.GD=g; T.P.res.light=0; T.spawnDrop('light',30,new THREE.Vector3(2.3,0.2,2.1),new THREE.Vector3(),9002); T.P.yaw=0; });
 await hold(()=>{ T.P.vel.set(0,0,0); },60);
 const g1=await pg.evaluate(()=>({gunStill:T.drops.has(9001),inv:T.P.inv.filter(Boolean),ammoGone:!T.drops.has(9002),light:T.P.res.light,tgt:T.useTgt&&T.useTgt.label}));
 await pg.evaluate(()=>T.useDown()); await frames(5); await pg.evaluate(()=>T.useUp());
 const g2=await pg.evaluate(()=>({gunTaken:!T.drops.has(9001),inv:T.P.inv.filter(Boolean)}));
 ok('a gun on the ground waits for Interact; ammo is picked up just by walking over it',g1.gunStill&&g1.inv.length===0&&g1.ammoGone&&g2.gunTaken&&g2.inv.length===1,{before:g1,after:g2});
 // inventory: holding forward and opening it, you keep walking
 const m=await pg.evaluate(async()=>{ T.P.pos.set(0,0,0); T.P.vel.set(0,0,0); T.P.yaw=0; const fwd=T.settings.binds.forward; T.inputDown(fwd); for(let k=0;k<20;k++) await new Promise(r=>requestAnimationFrame(r));
   const z0=T.P.pos.z; T.openInv(); for(let k=0;k<30;k++) await new Promise(r=>requestAnimationFrame(r)); const z1=T.P.pos.z, open=T.invOpen; T.closeInv(); T.inputUp(fwd); return {moved:+(z0-z1).toFixed(2),open}; });
 ok('opening the inventory while walking, you keep walking',m.open&&m.moved>0.5,m);
 // slot labels: the inventory shows the same keys as the hotbar
 const lab=await pg.evaluate(()=>{ T.settings.binds.gun='Digit1'; T.settings.binds.pump='Digit2'; T.settings.binds.bandage='Digit4'; const hud=[...document.querySelectorAll('#wbar .slot .k')].map(e=>e.textContent); return {inv:[0,1,2,3,4].map(i=>T.slotKeyLabel(i)),hud}; });
 ok('the inventory\'s slot numbers are the hotbar\'s keys',lab.inv[0]==='1'&&lab.inv[1]==='2'&&lab.inv[2]==='4',lab);
 // eliminated: the mouse doesn't turn you
 const d=await pg.evaluate(()=>{ T.net.dead=true; const y0=T.P.yaw; dispatchEvent(new MouseEvent('mousemove',{movementX:300,movementY:0})); const y1=T.P.yaw; T.net.dead=false; return {y0,y1}; });
 ok('once eliminated, moving the mouse doesn\'t spin you',d.y0===d.y1,d);
 // a house front door: there, closed (solid), and it opens and closes with Interact
 const hd=await pg.evaluate(()=>{ const p=[...T.pieces.values()].find(p=>p.owner==='world'&&p.doors&&p.doors.some(Boolean)); if(!p) return {none:true}; const c=p.doors.findIndex(Boolean), n0=T.makeBoxes(p).length;
   T.toggleDoor(p,c,true,true,1); const n1=T.makeBoxes(p).length; T.toggleDoor(p,c,true,false,1); const n2=T.makeBoxes(p).length; return {n0,n1,n2,doors:[...T.pieces.values()].filter(q=>q.doors&&q.doors.some(Boolean)).length}; });
 ok('every house front door is a real door: solid when closed, open walks through, closes again',!hd.none&&hd.n0===hd.n1+1&&hd.n2===hd.n0&&hd.doors>=80,hd);
 console.log(R.join('\n')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

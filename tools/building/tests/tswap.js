// full inventory: Interact on a gun swaps it for the one you're holding; map houses can't be edited
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','P,scene,renderer,drops,spawnDrop,findUseTarget,useDown,selectSlot,canEdit,pieces,settings,horde,camera,applyFov,scopeZoom,get adsK(){return adsK},set adsK(v){adsK=v},get scopeOn(){return scopeOn},set scopeOn(v){scopeOn=v},get scopeLvl(){return scopeLvl},get useTgt(){return useTgt},set useTgt(v){useTgt=v}'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:120000});
 await pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); T.settings.skyDrop=false; });
 await pg.evaluate(()=>document.getElementById('play').click()); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const P=T.P, out={}; P.inv=['ar','pump','smg','pistol','sniper']; P.ammo={ar:30,pump:5,smg:20,pistol:10,sniper:1}; T.selectSlot(1);
   out.before=P.inv.slice(); const pos=P.pos.clone(); pos.x-=Math.sin(P.yaw)*1.0; pos.z-=Math.cos(P.yaw)*1.0;
   T.spawnDrop('revolver',6,pos,new THREE.Vector3()); for(const d of T.drops.values()){ d.landed=true; d.t=1; }
   const t=T.findUseTarget(); out.label=t&&t.label; T.useTgt=t; T.useDown();
   out.after=P.inv.slice(); out.held=P.inv[P.slot]; out.dropped=[...T.drops.values()].some(d=>d.item==='pump');
   // houses: not editable with any rule, horde or not
   const house=[...T.pieces.values()].find(p=>p.owner==='world'); const res=[]; for(const rule of ['owner','team','anyone']){ T.settings.editRule=rule; res.push(T.canEdit(house,'me')); } T.horde.on=true; T.settings.editRule='team'; res.push(T.canEdit(house,'me')); T.horde.on=false; T.settings.editRule='owner';
   out.houseEdit=res;
   // scope: the wheel steps the zoom in and out
   P.wpn='sniper'; T.adsK=1; T.scopeOn=true; T.applyFov(); const f0=T.camera.fov; dispatchEvent(new WheelEvent('wheel',{deltaY:-100})); const f1=T.camera.fov; dispatchEvent(new WheelEvent('wheel',{deltaY:-100})); const f2=T.camera.fov; dispatchEvent(new WheelEvent('wheel',{deltaY:-100})); const f3=T.camera.fov; dispatchEvent(new WheelEvent('wheel',{deltaY:100})); const f4=T.camera.fov;
   out.fov=[f0,f1,f2,f3,f4].map(v=>+v.toFixed(2)); return out; });
 console.log(JSON.stringify(r));
 const ok=r.label==='Swap Pump Shotgun for Revolver'||(/^Swap .* for /.test(r.label||''));
 console.log(ok&&r.after[1]==='revolver'&&r.held==='revolver'&&r.dropped&&r.houseEdit.every(v=>v===false)&&r.fov[1]<r.fov[0]&&r.fov[2]<r.fov[1]&&r.fov[3]===r.fov[2]&&r.fov[4]===r.fov[1]?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

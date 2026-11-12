// a match starts with no materials and no shield; the Shield Potion gives 50 (up to 100); eliminated, you spill everything
// and it stays; chest extras include the Shield Potion, rarer than the small one
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,settings,BR,BRBUS,drops,ITEMS,spillLoot,rollChestLoot,stepUse,startUse,selectItem,infMats,SPAWN,brPlayerOut'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; T.settings.infMats=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(800);
 const s0=await pg.evaluate(()=>({mats:JSON.stringify(T.P.mats),sh:T.P.sh,inf:T.infMats(),items:JSON.stringify(T.P.items)}));
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(800); await pg.evaluate(()=>{ T.P.sky=null; T.P.bus=false; T.P.pos.set(T.SPAWN[0],T.P.pos.y,T.SPAWN[2]); });
 // the shield potion
 const pot=await pg.evaluate(()=>{ T.P.items.big=2; T.P.inv[0]='big'; T.P.sh=30; T.selectItem('big'); T.startUse(true); for(let i=0;i<80;i++) T.stepUse(0.1); const a=T.P.sh; T.startUse(true); for(let i=0;i<80;i++) T.stepUse(0.1); return {after1:a,after2:T.P.sh,left:T.P.items.big}; });
 // spill
 const sp=await pg.evaluate(()=>{ T.P.inv=['ar','pump','bandage','big',null]; T.P.items={bandage:5,mini:0,big:1}; T.P.res={light:20,medium:60,shells:10,heavy:0,rockets:0}; T.P.nades=2; const n0=T.drops.size; T.brPlayerOut(null); let keep=0, n=0; T.drops.forEach(d=>{ n++; if(d.keep) keep++; }); return {before:n0,after:n,keep,inv:JSON.stringify(T.P.inv)}; });
 await sleep(3000); const kept=await pg.evaluate(()=>{ T.drops.forEach(d=>{ d.t=500; }); return 0; }); await sleep(2500); const still=await pg.evaluate(()=>T.drops.size);
 const ex={}; await pg.evaluate(()=>0); const extras=await pg.evaluate(()=>{ const c={}; for(let i=0;i<30000;i++){ const o=T.rollChestLoot(); if(o[2]) c[o[2][0]]=(c[o[2][0]]||0)+1; } return c; });
 console.log(JSON.stringify({s0,pot,sp,still,extras}));
 const ok=s0.mats==='{"wood":0,"brick":0,"metal":0}'&&s0.sh===0&&!s0.inf&&pot.after1===80&&pot.after2===100&&sp.after-sp.before>=6&&still>=sp.after-2&&extras.big<extras.mini;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

// BR bots know when they're beaten: one you've nearly finished runs from you (and heals out of sight); a brave one keeps pushing
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,WEAPONS,SPAWN,terrainH,TOWNS'),{fast:true,norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(800);
 const res=[];
 for(const brave of [false,true]){
   await pg.evaluate(brave=>{ const P=T.P, bots=T.BR.bots, gun=Object.keys(T.WEAPONS).find(k=>T.WEAPONS[k].mag&&!(T.WEAPONS[k].pellets>1)&&(T.WEAPONS[k].range||150)>60);
     // an open spot in the middle of the field
     const x=T.SPAWN[0]+30, z=T.SPAWN[2]+60; P.sky=null; P.bus=false; P.pos.set(x,T.terrainH(x,z)+0.1,z); P.vel.set(0,0,0); P.hp=100; P.sh=100;
     bots.forEach((o,i)=>{ if(i>1){ o.alive=false; o.bus=false; o.sky=null; o.pos.set(T.SPAWN[0]-300,-50,T.SPAWN[2]); } });
     const o=bots[0]; o.alive=true; o.bus=false; o.sky=null; const bx=x+14, bz=z; o.pos.set(bx,T.terrainH(bx,bz)+0.1,bz); o.vel.set(0,0,0); o.wpn=gun; o.ammo=30; o.hp=25; o.sh=0; o.brave=brave; o.flee=false; o.heals=0; o.loot=null; o.dest=null;
     o.aw.set(P,1.5); o.tgt=P; o.los=true; o.hurtAt=performance.now(); o.lastSeen={x,z,t:performance.now(),T:P}; o.thinkT=0;
     bots[1].alive=true; bots[1].bus=false; bots[1].sky=null; bots[1].pos.set(T.SPAWN[0]+300,T.terrainH(T.SPAWN[0]+300,T.SPAWN[2])+0.1,T.SPAWN[2]); window._d0=Math.hypot(bx-x,bz-z); },brave);
   const tr=[]; for(let i=0;i<8;i++){ await sleep(400); tr.push(await pg.evaluate(()=>{ const o=T.BR.bots[0]; o.hurtAt=Math.max(o.hurtAt,performance.now()-600); T.P.hp=100; T.P.sh=100; return [+Math.hypot(o.pos.x-T.P.pos.x,o.pos.z-T.P.pos.z).toFixed(1),o.flee,o.alive]; })); }
   console.log(brave?'brave':'normal',tr.map(t=>t.join('/')).join('  '));
   const d0=tr[0][0], d1=tr[tr.length-1][0]; res.push(brave?(d1<d0+1&&!tr.some(t=>t[1])):(tr.some(t=>t[1])&&d1>d0+8)); }
 console.log(res.every(x=>x)?'OK':'FAIL',JSON.stringify(res)); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

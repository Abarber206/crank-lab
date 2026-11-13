// two skilled BR bots with a rifle and a shotgun each and materials meet in the open: they build (walls, ramps), swap
// guns with the range, and one of them wins
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,pieces,WEAPONS,SPAWN,terrainH'),{fast:true,norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(800);
 await pg.evaluate(()=>{ const P=T.P; P.sky=null; P.bus=false; P.pos.set(T.SPAWN[0]-200,T.terrainH(T.SPAWN[0]-200,T.SPAWN[2])+0.2,T.SPAWN[2]); P.hp=1e6;
   const W=T.WEAPONS, ar=Object.keys(W).find(k=>W[k].base==='ar'&&W[k].rarity==='rare'), sg=Object.keys(W).find(k=>W[k].base==='pump'&&W[k].rarity==='rare');
   T.BR.bots.forEach((o,i)=>{ if(i>1){ o.alive=false; o.bus=false; o.sky=null; o.pos.set(T.SPAWN[0]-400,-50,T.SPAWN[2]); } });
   const x0=T.SPAWN[0]+20, z0=T.SPAWN[2]+70; [0,1].forEach(i=>{ const o=T.BR.bots[i], x=x0+i*32, z=z0; o.alive=true; o.bus=false; o.sky=null; o.team=10+i; o.pos.set(x,T.terrainH(x,z)+0.2,z); o.vel.set(0,0,0);
     Object.assign(o,{wpn:ar,ammo:30,wpn2:sg,ammo2:5,mats:300,skill:0.85,brave:i===0,hp:100,sh:50,heals:2,flee:false,loot:null,dest:null}); window['_n'+i]={swaps:0,last:o.wpn}; });
   const a=T.BR.bots[0], c=T.BR.bots[1]; a.aw.set(c,1.5); c.aw.set(a,1.5); });
 let mx=0; const log=[]; for(let t=0;t<40;t++){ await sleep(1000);
   const r=await pg.evaluate(()=>{ let n=0; T.pieces.forEach(p=>{ if(p.owner==='bot') n++; }); const bs=[0,1].map(i=>{ const o=T.BR.bots[i], s=window['_n'+i]; if(o.wpn!==s.last){ s.swaps++; s.last=o.wpn; } return [o.alive?1:0,Math.round(o.hp),Math.round(o.sh),o.wpn&&T.WEAPONS[o.wpn].base,o.mats,s.swaps,Math.round(o.pos.distanceTo(T.BR.bots[1-i].pos))]; }); return {n,bs}; });
   mx=Math.max(mx,r.n); log.push(r); if(t%4===3) console.log(t+1,JSON.stringify(r)); if(!r.bs[0][0]||!r.bs[1][0]) break; }
 const L=log[log.length-1], swaps=L.bs[0][5]+L.bs[1][5], done=!L.bs[0][0]||!L.bs[1][0];
 console.log('built',mx,'swaps',swaps,'winner',done?(L.bs[0][0]?'brave':'other'):'none'); console.log(mx>=2&&done?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

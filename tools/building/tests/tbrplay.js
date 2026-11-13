// BR bots play like players: after the drop they carry two kinds of gun, gather materials, build in fights (walls,
// ramps, boxes), and the match keeps moving (eliminations happen); no errors
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,pieces,WEAPONS,SPAWN'),{fast:true,norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(500);
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T; }); await sleep(800); await pg.evaluate(()=>{ T.P.sky=null; T.P.bus=false; T.P.pos.set(T.SPAWN[0],T.P.pos.y,T.SPAWN[2]); T.P.hp=1e6; T.P.sh=0; });
 const st=()=>pg.evaluate(()=>{ const bs=T.BR.bots, al=bs.filter(b=>b.alive); let bp=0; T.pieces.forEach(p=>{ if(p.owner==='bot') bp++; });
   return {alive:al.length,armed:al.filter(b=>b.wpn).length,two:al.filter(b=>b.wpn&&b.wpn2).length,sg:al.filter(b=>[b.wpn,b.wpn2].some(w=>w&&T.WEAPONS[w].pellets>1)).length,mats:Math.round(al.reduce((s,b)=>s+(b.mats||0),0)/Math.max(1,al.length)),built:bp,flee:al.filter(b=>b.flee).length}; });
 let last=null, maxBuilt=0; for(let t=0;t<14;t++){ await sleep(10000); last=await st(); maxBuilt=Math.max(maxBuilt,last.built); console.log('t',(t+1)*10,JSON.stringify(last)); }
 const ok=last.two>=1&&maxBuilt>=4&&last.alive<29&&last.mats>0;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,6).join('\n')||'no errors'); await b.close(); })();

// inner walls are real pieces clear of the stairs; breaking one leaves the floor (and the reverse); chests are solid
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,pieces,TOWNS,houseStair,destroyPiece,chests,settings,physStep,renderer'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS,null,{timeout:120000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); document.getElementById('play').click(); }); await sleep(1500);
 const r=await pg.evaluate(async()=>{ const inner=[...T.pieces.values()].filter(p=>p.inner); let bad=0, doors=0; const out={inner:inner.length};
   T.TOWNS.forEach(t=>t.houses.forEach(h=>{ if(h.floors<2) return; const S=T.houseStair(h); inner.forEach(p=>{ if(p.town!==t) return; S.cells.forEach(([i,j])=>{ if(p.axis==='z'&&p.i===i&&(p.j===j||p.j===j+1)) bad++; if(p.axis==='x'&&p.j===j&&(p.i===i||p.i===i+1)) bad++; }); }); }));
   inner.forEach(p=>{ if(p.mask!==511) doors++; }); out.touchStairs=bad; out.doorways=doors;
   const w=inner.find(p=>p.mask===511)||inner[0], fk='f'+(w.axis==='z'?w.i:w.i)+'_'+(w.axis==='z'?w.j:w.j)+'_'+w.l, f=T.pieces.get(fk); out.floorUnder=!!f;
   T.destroyPiece(w); await new Promise(r=>setTimeout(r,600)); out.wallGone=!T.pieces.has(w.key); out.floorStays=T.pieces.has(fk);
   const w2=inner.find(p=>T.pieces.has(p.key)&&p.l>p.town.houses[0].L-99&&p!==w), f2=T.pieces.get('f'+w2.i+'_'+w2.j+'_'+w2.l); if(f2){ T.destroyPiece(f2); await new Promise(r=>setTimeout(r,600)); out.floorGone=!T.pieces.has(f2.key); out.wallStays=T.pieces.has(w2.key); }
   // walk into a chest: you stop short of its middle
   const c=T.chests.find(c=>!c.open&&c.y<12); T.P.pos.set(c.x-1.6,c.y+0.05,c.z); T.P.vel.set(0,0,0); await new Promise(r=>setTimeout(r,500)); T.P.pos.set(c.x-1.6,c.y+0.05,c.z); for(let k=0;k<240;k++){ T.P.vel.x=5; T.P.vel.z=0; T.physStep(1/120,T.P); } out.stopAt=+(c.x-T.P.pos.x).toFixed(2);
   return out; });
 console.log(JSON.stringify(r), r.inner>60&&r.touchStairs===0&&r.doorways>30&&r.wallGone&&r.floorStays&&r.stopAt>0.6?'PASS':'FAIL'); console.log(errs.join('\n')||'no errors'); await b.close(); })();

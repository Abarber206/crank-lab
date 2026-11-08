const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,pieces,findUnsupported,clearBuilds,TOWNS'),{fast:true,norender:true});
 const r=await pg.evaluate(()=>{ const w=[...T.pieces.values()].filter(p=>p.owner==='world'); const un=T.findUnsupported(w);
   T.clearBuilds(); const w2=[...T.pieces.values()].filter(p=>p.owner==='world'); return {world:w.length,unsupported:un.length,sample:un.slice(0,5).map(p=>p.key+' '+p.type+' m'+p.mask),afterClear:w2.length,unsupported2:T.findUnsupported(w2).length}; });
 console.log((r.unsupported===0&&r.unsupported2===0?'PASS':'FAIL')+' every town house piece is held up under the new rules — '+JSON.stringify(r));
 console.log(errs.join('\n')||'no errors'); await b.close(); })();

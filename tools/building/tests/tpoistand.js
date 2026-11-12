// the points of interest stand on their own: no piece falls or is removed in the first half minute of a match.  node tpoistand.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,TOWNS,pieces,settings,TOD'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS,null,{timeout:180000});
 await pg.evaluate(()=>{ T.settings.skyDrop=false; document.querySelector('.mode[data-mode=fight]').click(); document.querySelector('#play').click(); });
 const count=()=>pg.evaluate(()=>{ const o={}; for(const t of T.TOWNS){ if(!t.kind) continue; let n=0; T.pieces.forEach(p=>{ if(p.town===t) n++; }); o[t.name]=n; } return o; });
 await sleep(4000); const a=await count(); await sleep(30000); const c=await count();
 console.log(JSON.stringify(a),JSON.stringify(c)); console.log(JSON.stringify(a)===JSON.stringify(c)&&Object.values(a).every(n=>n>100)?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

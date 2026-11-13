// how big the scene graph is, and what in it updates its matrix every frame
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,settings,BR,BRBUS,TOWNS,terrainH,props,pieces'),{norender:true});
 await pg.evaluate(()=>{ T.settings.skyDrop=true; document.querySelector('.mode[data-mode=br]').click(); document.getElementById('play').click(); }); await pg.waitForFunction(()=>T.BR.on,null,{timeout:90000}); await sleep(1500);
 await pg.evaluate(()=>{ T.BRBUS.t=T.BRBUS.T*0.55; }); await sleep(4000);
 const r=await pg.evaluate(()=>{ let n=0, auto=0; const top=[]; const byTop=new Map();
   for(const c of T.scene.children){ let cn=0, ca=0, cv=0; c.traverse(o=>{ cn++; if(o.matrixAutoUpdate) ca++; }); n+=cn; auto+=ca; const k=(c.userData&&c.userData.kind)||c.type+(c.name?':'+c.name:''); const e=byTop.get(k)||{n:0,nodes:0,auto:0,vis:0}; e.n++; e.nodes+=cn; e.auto+=ca; if(c.visible) e.vis++; byTop.set(k,e); }
   const pg=new Set(); T.pieces.forEach(p=>{ if(p.group) pg.add(p.group); }); const prg=new Set(T.props.map(p=>p.g).filter(Boolean)); const bg=new Set(); T.BR.bots.forEach(b=>{ for(const k in b){ const v=b[k]; if(v&&v.isObject3D) bg.add(v); } });
   const cat={}; for(const c of T.scene.children){ if(c.type!=='Group') continue; let cn=0; c.traverse(()=>cn++); const k=pg.has(c)?'piece'+(c.visible?'V':'H'):prg.has(c)?'prop'+(c.visible?'V':'H'):bg.has(c)?'bot'+(c.visible?'V':'H'):'other'+(c.visible?'V':'H')+':'+(c.name||c.children.length); const e=cat[k]||(cat[k]={n:0,nodes:0}); e.n++; e.nodes+=cn; }
   const own=new Map(); const walk=(v,path,d)=>{ if(!v||typeof v!=='object'||d>2) return; if(v.isObject3D){ if(!own.has(v)) own.set(v,path); return; } for(const k in v){ try{ walk(v[k],path+'.'+k,d+1); }catch(e){} } };
   T.BR.bots.forEach((b,i)=>walk(b,'bot',0)); 
   const ex={}; for(const c of T.scene.children){ if(c.type!=='Group'||c.visible) continue; let cn=0; c.traverse(()=>cn++); if(cn<20) continue; const k=c.children.length; if(ex[k]&&ex[k].length>2) continue; (ex[k]=ex[k]||[]).push({own:own.get(c)||null,nm:c.name,ud:JSON.stringify(c.userData).slice(0,80),ch:c.children.map(x=>x.type+':'+x.name+':'+x.children.length).join('|').slice(0,120),pos:c.position.toArray().map(v=>Math.round(v))}); }
   return {ex,cat,n,auto,children:T.scene.children.length,props:T.props.length,pieces:T.pieces.size,top:[...byTop.entries()].sort((a,b)=>b[1].auto-a[1].auto).slice(0,25)}; });
 console.log(JSON.stringify(r,null,0).replace(/\],\[/g,'],\n[')); await b.close(); })();

// every staircase at the points of interest can be walked: open floor at the foot, headroom all the way up, a floor at
// the top; every chest and floor-loot spot sits on a floor with room above it.  node tpoiwalk.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,renderer,TOWNS,near,groundAt,ceilAt,staticsInto,pieces,CELL,LVL,DIRS,chests'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.TOWNS,null,{timeout:180000}); await sleep(3000);
 const r=await pg.evaluate(()=>{ const out={bad:[],ramps:0,spots:0};
   const probe=(x,z,want,tag,up)=>{ const ps=T.staticsInto(T.near(x,z),x,z,1), [g]=T.groundAt(x,z,want+0.7,ps), c=T.ceilAt(x,z,g+0.1,ps,g+0.05);
     if(g<want-0.55||g>want+(up||0.55)) out.bad.push(tag+' ground '+g.toFixed(2)+' want '+want.toFixed(2)); else if(c-g<1.95) out.bad.push(tag+' headroom '+(c-g).toFixed(2)); };
   for(const t of T.TOWNS){ if(!t.kind) continue;
     for(const bl of t.blds) for(const q of bl.pieces){ if(q.type!=='ramp') continue; out.ramps++; const d=T.DIRS[q.dir], C=T.CELL, cx=(q.i+.5)*C, cz=(q.j+.5)*C, y=q.l*T.LVL;
       for(const lat of [-1.2,0,1.2]){ const lx=-d[1]*lat, lz=d[0]*lat;
         probe(cx-d[0]*(C/2+0.7)+lx,cz-d[1]*(C/2+0.7)+lz,y,t.name+' '+q.key+' foot');
         for(let s=-0.4;s<=0.41;s+=0.2) probe(cx+d[0]*s*C+lx,cz+d[1]*s*C+lz,y+(s+0.5)*T.LVL,t.name+' '+q.key+' at '+s.toFixed(1));
         probe(cx+d[0]*(C/2+0.7)+lx,cz+d[1]*(C/2+0.7)+lz,y+T.LVL,t.name+' '+q.key+' top',1.2); } }
     for(const bl of t.blds) for(const k of ['chest','floor']) for(const s of bl.spots[k]){ out.spots++; probe(s.x,s.z,s.y,t.name+' '+bl.kind+' '+k+' spot'); } }
   out.chests=T.chests.length; return out; });
 console.log('ramps',r.ramps,'spots',r.spots); r.bad.forEach(x=>console.log('  ',x)); console.log(r.bad.length?'FAIL':'PASS'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

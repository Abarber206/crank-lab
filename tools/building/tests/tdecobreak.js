// decorations break: a shot finds the object, enough damage breaks it (its shape folds away, it stops being solid),
// and a new round puts it back; counts of objects by material
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,props,DECO,DECOR,castShot,damagePiece,decoReset,STATICS,P,TOWNS'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.props&&T.props.length>1000&&T.DECO&&T.DECO.objs.length,null,{timeout:180000}); await sleep(1500);
 const r=await pg.evaluate(()=>{ const D=T.DECO, by={}; D.objs.forEach(o=>{ by[o.mat]=(by[o.mat]||0)+1; }); const solid=D.objs.filter(o=>o.statics.length).length;
   // one at a campsite (a tent) and one at a point of interest
   const pick=(x,z)=>D.objs.filter(o=>o.statics.length&&!o.gone).sort((a,b)=>Math.hypot(a.c.x-x,a.c.z-z)-Math.hypot(b.c.x-x,b.c.z-z))[0];
   const out=[]; const t=T.TOWNS.find(t=>t.kind==='factory'), c=T.DECOR.camps[0];
   for(const o of [pick(c[0]+4,c[1]),pick(t.x,t.z)]){ const bx=o.statics[0].solid.boxes[0], tc=new THREE.Vector3((bx[0]+bx[3])/2,(bx[1]+bx[4])/2,(bx[2]+bx[5])/2), from=new THREE.Vector3(tc.x+0.05,bx[4]+8,tc.z+0.05), d=tc.clone().sub(from).normalize(); const hit=T.castShot(from,d,20,0,null);
     const got=hit.kind==='piece'&&hit.piece.dobj===o; let n=0; while(!o.gone&&n<40){ T.damagePiece(o.piece,100,o.c.clone()); n++; }
     const [g,off]=o.ranges[0]; const A=g.attributes.position.array, folded=A[off*3]===A[off*3+3]&&A[off*3+1]===A[off*3+4]; const empty=o.statics.every(s=>!s.solid.boxes.length);
     const after=T.castShot(from,d,20,0,null); out.push({hitk:hit.kind,hitp:hit.piece?(hit.piece.key||"")+(hit.piece.dobj?"#"+hit.piece.dobj.id:""):"",oid:o.id,t:+hit.t.toFixed(2),mat:o.mat,hp0:o.hp0,got,hits:n,gone:o.gone,folded,empty,shotThrough:!(after.kind==='piece'&&after.piece.dobj===o)}); }
   T.decoReset(); const back=D.objs.filter(o=>o.gone).length, solidBack=D.objs.filter(o=>o.statics.length&&o.statics[0].solid.boxes.length).length;
   return {objs:D.objs.length,solid,by,out,back,solidBack}; });
 console.log(JSON.stringify(r)); const ok=r.objs>200&&r.out.every(o=>o.got&&o.gone&&o.folded&&o.empty&&o.shotThrough)&&r.back===0&&r.solidBack===r.solid;
 console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,5).join('\n')||'no errors'); await b.close(); })();

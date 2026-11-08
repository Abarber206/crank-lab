// Edit / collision / structural validation suite, following Part 16 of the editing rulebook.
const {sleep,page,launch,open}=require('./h.js');
const EXPOSE='P,pieces,conn,addPiece,removePiece,destroyPiece,clearBuilds,physStep,beginEdit,exitEdit,resetEdit,paintTile,editValid,editShapeName,wallMaskValid,stairEditResult,shapeValid,slabTop,makeBoxes,pbox,findUnsupported,grounded,canEdit,settings,net,WALL_SHAPES,stairSegs,coneHeight,wallTiles,castShot,CELL,LVL,WT,FT,R,get edit(){return edit}';
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html',EXPOSE),{fast:true});
 await pg.waitForFunction(()=>window.T&&T.pieces,null,{timeout:120000});
 // shared helpers inside the page
 await pg.evaluate(()=>{ const H=window.H={}; let n=0;
   H.reset=()=>{ T.clearBuilds(); [...T.pieces.values()].filter(p=>p.owner!=='world').forEach(p=>T.removePiece(p)); };
   H.wall=(axis,i,j,l,o)=>T.addPiece(Object.assign({type:'wall',axis,i,j,l,key:`w${axis}${i}_${j}_${l}`,mat:'wood',instant:true},o||{}));
   H.floor=(i,j,l,o)=>T.addPiece(Object.assign({type:'floor',i,j,l,key:`f${i}_${j}_${l}`,mat:'wood',instant:true},o||{}));
   H.ramp=(i,j,l,dir,o)=>T.addPiece(Object.assign({type:'ramp',i,j,l,dir,key:`m${i}_${j}_${l}`,mat:'wood',instant:true},o||{}));
   H.cone=(i,j,l,o)=>T.addPiece(Object.assign({type:'cone',i,j,l,key:`m${i}_${j}_${l}`,mat:'wood',instant:true},o||{}));
   H.edit=(p,tiles,apply=true)=>{ T.beginEdit(p); if(!T.edit) return {refused:true}; tiles.forEach(i=>T.paintTile(i)); const ok=T.editValid(), name=T.editShapeName(); T.exitEdit(apply); return {ok,name}; };
   H.at=(x,y,z)=>{ T.P.pos.set(x,y,z); T.P.vel.set(0,0,0); T.P.onGround=false; T.P.phase=new Set(); T.P.crouch=false; };
   // run the player's physics: steer at a horizontal velocity, optionally jumping whenever on the ground
   H.sim=(vx,vz,secs,jump)=>{ let maxY=-1e9, minX=1e9, maxX=-1e9; for(let t=0;t<secs;t+=1/120){ T.P.vel.x=vx; T.P.vel.z=vz; if(jump&&T.P.onGround) { T.P.vel.y=8.4; T.P.onGround=false; }
       T.physStep(1/120,T.P); maxY=Math.max(maxY,T.P.pos.y); } return {x:+T.P.pos.x.toFixed(2),y:+T.P.pos.y.toFixed(2),z:+T.P.pos.z.toFixed(2),maxY:+maxY.toFixed(2)}; };
   H.keys=p=>[...(T.conn.get(p)||[])].map(q=>q.key).sort().join(',');
   H.shot=(o,d)=>{ T.pieces.forEach(p=>p.group&&p.group.updateMatrixWorld(true)); return T.castShot(new THREE.Vector3(...o),new THREE.Vector3(...d).normalize(),30,0,null).kind; };
 });
 const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+(d!==undefined?' — '+(typeof d==='string'?d:JSON.stringify(d)):''));
 const ev=f=>pg.evaluate(f).catch(e=>{ console.log(R.join('\n')); console.log('ERROR in the group after the above:',e.message.split('\n')[0]); process.exit(1); });

 // ===== 16.1 every edit configuration =====
 const walls=await ev(()=>{ H.reset(); const out={valid:0,invalid:0,bad:[],named:0,namedBad:[]}; const tw=T.CELL/3, th=T.LVL/3;
   for(let m=1;m<512;m++){ if(!T.wallMaskValid(m)){ out.invalid++; continue; } out.valid++;
     const p=H.wall('x',2,0,0); const removed=[]; for(let i=0;i<9;i++) if(!(m>>i&1)) removed.push(i);
     const r=H.edit(p,removed); const q=T.pieces.get(p.key);
     if(!r.ok||!q||q.mask!==m){ out.bad.push(m+' not applied '+JSON.stringify(r)); T.removePiece(p); continue; }
     const boxes=T.makeBoxes(q), X=10;
     // no collision where tiles were removed
     for(const t of removed){ const r0=(t/3)|0, c0=t%3, za=c0*tw, zb=za+tw, ya=r0*th, yb=ya+th;
       for(const bx of boxes){ const oz=Math.min(bx[5],zb)-Math.max(bx[2],za), oy=Math.min(bx[4],yb)-Math.max(bx[1],ya); if(oz>0.02&&oy>0.02){ out.bad.push(m+' collision in removed tile '+t); break; } } }
     // collision on every remaining tile (for a 45-degree cut, deep inside the part that's left)
     for(const {r:r0,c:c0,cut} of T.wallTiles(m)){ let pz=c0*tw+tw/2, py=r0*th+th/2; if(cut){ pz=c0*tw+tw*(cut[0]>0?0.15:0.85); py=r0*th+th*(cut[1]<0?0.85:0.15); }
       if(!boxes.some(bx=>pz>=bx[2]&&pz<=bx[5]&&py>=bx[1]&&py<=bx[4])) out.bad.push(m+' no collision on kept tile '+(r0*3+c0)); }
     // support: one attachment per remaining tile
     let kept=0; for(let i=0;i<9;i++) kept+=m>>i&1; if(T.pbox(q).length!==kept) out.bad.push(m+' attachments '+T.pbox(q).length+' vs '+kept);
     T.removePiece(q); }
   for(const [k,name] of Object.entries(T.WALL_SHAPES)){ if(!k) continue; let m=511; k.split(',').forEach(i=>m&=~(1<<+i)); if(T.wallMaskValid(m)) out.named++; else out.namedBad.push(name+' '+k); }
   out.bad=out.bad.slice(0,8); return out; });
 ok('walls: every connected selection applies, with collision only on what is left and one attachment per tile',walls.bad.length===0,`${walls.valid} valid, ${walls.invalid} refused`+(walls.bad.length?' '+walls.bad.join(' | '):''));
 ok('walls: every named Fortnite edit (windows, doors, arches, window door, half walls, columns, cuts, triangles) is valid',walls.namedBad.length===0,walls.named+' named'+(walls.namedBad.length?' bad: '+walls.namedBad.join(','):''));
 const wallRules=await ev(()=>{ const v=k=>{ let m=511; k.forEach(i=>m&=~(1<<i)); return T.wallMaskValid(m); };
   return {midRow:v([3,4,5]),all:v([0,1,2,3,4,5,6,7,8]),centreCol:v([1,4,7]),topOnly:v([0,1,2,3,4,5]),diag:v([0,4,8])}; });
 ok('walls: selections that would leave a part hanging loose are refused (middle row, centre column, diagonal, everything)',!wallRules.midRow&&!wallRules.all&&!wallRules.centreCol&&!wallRules.diag&&wallRules.topOnly,wallRules);
 const floors=await ev(()=>{ H.reset(); const bad=[];
   for(let m=1;m<16;m++){ const p=H.floor(2,0,0); const removed=[0,1,2,3].filter(i=>!(m>>i&1)); const r=H.edit(p,removed); const q=T.pieces.get(p.key);
     if(!q||q.mask!==m){ bad.push(m+' not applied'); continue; } const bx=T.makeBoxes(q); let kept=0; for(let i=0;i<4;i++) kept+=m>>i&1;
     if(bx.length!==(m===15?1:kept)) bad.push(m+' boxes '+bx.length); if(T.pbox(q).length!==kept) bad.push(m+' attach'); T.removePiece(q); }
   const p=H.floor(2,0,0); const r=H.edit(p,[0,1,2,3]); const ref=T.pieces.get(p.key).mask; return {bad,allRefused:!r.ok&&ref===15}; });
 ok('floors: all 15 shapes (3/4, half, diagonal bridge, 1/4) apply with matching collision and attachments; removing all 4 is refused',floors.bad.length===0&&floors.allRefused,floors);
 const cones=await ev(()=>{ H.reset(); const bad=[];
   for(let m=0;m<15;m++){ const p=H.cone(2,0,0); const sel=[0,1,2,3].filter(i=>m>>i&1); H.edit(p,sel); const q=T.pieces.get(p.key); if(q.mask!==m){ bad.push(m+' not applied'); continue; }
     for(const [lx,lz] of [[0.6,0.6],[4.4,0.6],[2.5,2.5],[1.2,3.9],[4.1,4.2]]){ const h=T.slabTop(q,10+lx,lz); if(Math.abs(h-T.coneHeight(m,lx,lz))>1e-6) bad.push(m+' surface'); }
     T.removePiece(q); }
   const p=H.cone(2,0,0); const r=H.edit(p,[0,1,2,3]); return {bad,allRefused:!r.ok&&T.pieces.get(p.key).mask===0}; });
 ok('cones: all 15 corner shapes apply and the walking surface matches the shape; raising all 4 corners is refused',cones.bad.length===0&&cones.allRefused,cones);
 const ramps=await ev(()=>{ H.reset(); const bad=[], names={}; const adj=(a,b)=>((a>>1)===(b>>1))!==((a&1)===(b&1));
   const perms=a=>a.length<2?[a]:a.flatMap((x,i)=>perms([...a.slice(0,i),...a.slice(i+1)]).map(r=>[x,...r]));
   const tryEdit=(tiles)=>{ const p=H.ramp(2,0,0,0); const r=H.edit(p,tiles); const q=T.pieces.get(p.key); const out={r,q:{dir:q.dir,half:q.half,path:q.path}}; T.removePiece(q); return out; };
   // half stairs: every side-by-side pair, both ways
   for(let a=0;a<4;a++) for(let c=0;c<4;c++) if(a!==c&&adj(a,c)){ const o=tryEdit([a,c]); if(!(o.r.ok&&o.q.half>=0)) bad.push('half '+a+c); names[o.r.name]=1; }
   // L stairs: every 3-square path; spiral stairs: every 4-square path
   for(const t of perms([0,1,2,3]).filter(t=>t.slice(1).every((x,i)=>adj(t[i],x)))){ const o=tryEdit(t); if(!(o.r.ok&&o.q.path&&o.q.path.join()===t.join())) bad.push('U '+t); names[o.r.name]=1;
     const l=t.slice(0,3); const o3=tryEdit(l); if(!(o3.r.ok&&o3.q.path&&o3.q.path.length===3)) bad.push('L '+l); names[o3.r.name]=1; }
   // turning the whole stair across the centre strip, all four ways
   for(const [a,c,d] of [[4,5,1],[5,4,3],[6,7,0],[7,6,2]]){ const o=tryEdit([a,c]); if(!(o.r.ok&&o.q.dir===d&&o.q.half===-1&&!o.q.path)) bad.push('flip '+a+c); names[o.r.name]=1; }
   // refused: one square, two diagonal squares
   for(const t of [[0],[3],[0,3],[1,2]]){ const o=tryEdit(t); if(o.r.ok) bad.push('should refuse '+t); }
   return {bad:bad.slice(0,8),names:Object.keys(names)}; });
 ok('stairs: half (8 ways), L (24 paths), spiral U (8 paths) and turning via the centre strip (4 ways) all apply; one square or a diagonal pair is refused',ramps.bad.length===0,ramps);
 const stairSurf=await ev(()=>{ H.reset(); const bad=[]; const cases=[[[0,1]],[[0,1,3]],[[0,1,3,2]],[[2,0,1]],[[3,2,0,1]]];
   for(const [t] of cases){ const p=H.ramp(2,0,0,0); H.edit(p,t); const q=T.pieces.get(p.key), segs=q.path?T.stairSegs(q.path):null;
     // walk the path through square centres: heights must climb from 0 to the top, open squares have no surface
     let last=-1; const h=2.5, ctr=i=>[10+(i&1)*h+h/2,(i>>1)*h+h/2];
     for(const i of t){ const [x,z]=ctr(i), y=T.slabTop(q,x,z); if(y==null||y<last-1e-6) bad.push(t+' at '+i+' '+y); last=y; }
     for(let i=0;i<4;i++) if(!t.includes(i)){ const [x,z]=ctr(i); if(T.slabTop(q,x,z)!=null) bad.push(t+' open square '+i+' has a surface'); }
     T.removePiece(q); }
   return bad; });
 ok('stairs: walking surfaces climb along each edited stair, and squares that were removed have no surface',stairSurf.length===0,stairSurf);

 // ===== 16.2 collision =====
 const col=await ev(()=>{ const o={};
   H.reset(); H.wall('x',4,0,0); H.at(18.5,0,2.5); o.solid=H.sim(6,0,1.2);                                   // 1 solid wall
   H.reset(); H.edit(H.wall('x',4,0,0),[1,4]); H.at(18.5,0,2.5); o.door=H.sim(6,0,1.2);                      // 2 doorway
   H.reset(); H.edit(H.wall('x',4,0,0),[3,4,5,6,7,8]); H.at(18.5,0,2.5); o.jumpLow=H.sim(6,0,1.6,true);      // 3 jump over a low wall (an opening open to the top)
   H.reset(); H.edit(H.wall('x',4,0,0),[4]); H.at(18.5,0,2.5); o.window=H.sim(6,0,2.5,true);                 // 4 window: too small for the player
   H.reset(); H.wall('x',4,0,0); H.edit(H.floor(4,0,1),[0]); H.at(22.0,6,3.75); o.standKept=H.sim(0,0,1.2);                     // 5 stand on a remaining quarter
   H.at(21.25,6,1.25); o.fallRemoved=H.sim(0,0,1.6);                                                         // 6 fall through the removed quarter
   H.reset(); H.edit(H.ramp(4,0,0,0),[0,1]); H.at(20.3,0,1.25); o.halfUp=H.sim(6,0,1.4);                     // 7 walk up an edited (half) stair
   H.reset(); H.edit(H.ramp(4,0,0,0),[0,1,3]); H.at(20.4,0,1.25); let a=H.sim(6,0,0.6); o.lUp1=a; o.lUp=H.sim(0,6,1.0); // L stair: along, then turn
   H.reset(); const cn=H.cone(4,0,0); H.edit(cn,[0,1]); H.at(22.5,3,1.0); const c1=H.sim(0,0,1); const cq=T.pieces.get(cn.key), Rr=T.R; let hi=-1; for(const [dx,dz] of [[0,0],[Rr,0],[-Rr,0],[0,Rr],[0,-Rr],[Rr*.7,Rr*.7],[-Rr*.7,Rr*.7],[Rr*.7,-Rr*.7],[-Rr*.7,-Rr*.7]]){ const v=T.slabTop(cq,22.5+dx,1.0+dz); if(v!=null) hi=Math.max(hi,v); } o.cone={stoodAt:c1.y,surface:+hi.toFixed(2)}; // 8 edited cone
   H.reset(); H.ramp(4,0,0,0); H.at(23.4,0,1.25); o.underRamp=H.sim(0,0,1.2,true);                             // 9 jump under a stair: the underside stops your head
   H.reset(); const r2=H.ramp(4,0,0,0); H.edit(r2,[2,3]); H.at(23.4,0,1.25); o.underRemoved=H.sim(0,0,1.2,true); // 10 the same spot after that half is removed
   return o; });
 ok('collision 1: walking into a solid wall stops you',col.solid.x<20-0.3,col.solid);
 ok('collision 2: you walk straight through a doorway',col.door.x>21,col.door);
 ok('collision 3: you can jump through an opening big enough (over a low wall)',col.jumpLow.x>21,col.jumpLow);
 ok('collision 4: a window is too small to get through, even jumping',col.window.x<20,col.window);
 ok('collision 5: you stand on a remaining floor quarter',Math.abs(col.standKept.y-4)<0.05,col.standKept);
 ok('collision 6: you fall through a removed floor quarter',col.fallRemoved.y<0.1,col.fallRemoved);
 ok('collision 7: you walk up an edited (half) stair to the top',col.halfUp.maxY>3.5,col.halfUp);
 ok('collision 7b: you walk up an L stair round its corner',col.lUp.maxY>3.5&&col.lUp1.y>1.5,{first:col.lUp1,then:col.lUp});
 ok('collision 8: you stand on an edited cone at its real surface (the highest point under your feet)',Math.abs(col.cone.stoodAt-col.cone.surface)<0.08,col.cone);
 ok('collision 9: jumping under a stair, the underside stops your head',col.underRamp.maxY<1.0,col.underRamp);
 ok('collision 10: after that half of the stair is removed, nothing stops the jump',col.underRemoved.maxY>1.2,col.underRemoved);
 const chan=await ev(()=>{ H.reset(); H.edit(H.wall('x',4,0,0),[1,4]); const o={};
   o.throughDoor=H.shot([18,1.2,2.5],[1,0,0]); o.intoWall=H.shot([18,1.2,0.6],[1,0,0]); o.overDoor=H.shot([18,3.4,2.5],[1,0,0]); return o; });
 ok('shots and sight: pass through the doorway, hit the wall beside it and above it',chan.throughDoor==='none'&&chan.intoWall==='piece'&&chan.overDoor==='piece',chan);

 // ===== 16.3 reset =====
 const rs=await ev(()=>{ H.reset(); const p=H.wall('x',3,0,0); const f=H.floor(3,0,1); const box0=JSON.stringify(T.makeBoxes(p)), nb0=H.keys(p); p.hp=97; const id0=p.key, n0=T.pieces.size, out={};
   const seq=[[4],[1,4],[0,1,2,4],[1,2,5],[3,6,7]]; let ok=true;
   for(const t of seq){ H.edit(T.pieces.get(id0),t); T.beginEdit(T.pieces.get(id0)); T.resetEdit(); const q=T.pieces.get(id0);
     if(!q||q.mask!==511||JSON.stringify(T.makeBoxes(q))!==box0||H.keys(q)!==nb0||q.hp!==97||q.owner!==p.owner||q.mat!=='wood'||T.pieces.size!==n0) ok=false; }
   out.wall=ok;
   // edited -> different edit -> reset, stairs
   const r=H.ramp(5,0,0,0); H.edit(r,[0,1,3]); H.edit(T.pieces.get(r.key),[6,7]); H.edit(T.pieces.get(r.key),[0,2]); T.beginEdit(T.pieces.get(r.key)); T.resetEdit();
   const q=T.pieces.get(r.key); out.stair=q.dir===0&&q.half===-1&&!q.path&&T.slabTop(q,26,2.5)!=null;
   // reset after moving and after a structural change nearby
   H.edit(T.pieces.get(id0),[4]); H.at(14,0,2.5); H.sim(3,0,0.5); T.destroyPiece(T.pieces.get(f.key)); T.beginEdit(T.pieces.get(id0)); T.resetEdit();
   const w=T.pieces.get(id0); out.afterChanges=!!w&&w.mask===511&&w.hp===97&&!T.pieces.has(f.key);
   return out; });
 ok('reset: walls edited, reset and edited again keep identity, health, owner, material and connections, with no leftover collision',rs.wall,rs);
 ok('reset: a stair edited to an L, turned, halved and reset is back as placed',rs.stair,rs);
 ok('reset: works after moving around and after a neighbour was destroyed, and never brings the neighbour back',rs.afterChanges,rs);

 // ===== 16.4 structural =====
 const st=await ev(()=>{ const o={}, alive=k=>T.pieces.has(k);
   H.reset(); const f0=H.floor(3,0,0); o.t1=T.grounded(f0);                                                                         // 1
   H.reset(); const w=H.wall('x',3,0,0), f=H.floor(3,0,1); o.t2a=T.findUnsupported([f]).length===0; T.destroyPiece(w); o.t2b=!alive(f.key); // 2
   H.reset(); const w3=H.wall('x',3,0,0), fa=H.floor(3,0,1), fb=H.floor(4,0,1), fc=H.floor(5,0,1); o.t3=T.findUnsupported([fc]).length===0;      // 3 platform reaching out
   H.reset(); const tw=[0,1,2,3].map(l=>H.wall('x',3,0,l)); const top=H.floor(3,0,4); o.t4=T.findUnsupported([top]).length===0; T.destroyPiece(tw[0]); o.t4b=![1,2,3].some(l=>alive(tw[l].key))&&!alive(top.key); // 4 tower
   H.reset(); const wl=H.wall('x',3,0,0), wr=H.wall('x',6,0,0), br=[3,4,5].map(i=>H.floor(i,0,1));                                       // 5-8 bridge, two supports
   T.destroyPiece(wl); o.t5=br.every(q=>alive(q.key)); T.destroyPiece(wr); o.t6=br.every(q=>!alive(q.key));
   H.reset(); const s1=H.wall('x',3,0,0), F=H.floor(3,0,1), W2=H.wall('x',4,0,1);                                                        // 9 editing a floor disconnects a wall on it
   o.t9pre=T.findUnsupported([W2]).length===0; H.edit(F,[1,3]); o.t9=!alive(W2.key)&&alive(F.key);
   H.reset(); const s2=H.wall('x',3,0,0), F2=H.floor(3,0,1); H.edit(s2,[6,7,8]); o.t10=!alive(F2.key)&&alive(s2.key);                   // 10 editing a wall drops the platform it held
   H.reset(); const ok10b=H.wall('x',3,0,0), F3=H.floor(3,0,1); H.edit(ok10b,[4]); o.t10b=alive(F3.key);                                // ...but a window keeps it
   H.reset(); const rp=H.ramp(3,0,0,0), F4=H.floor(4,0,1); o.t11pre=T.findUnsupported([F4]).length===0; T.destroyPiece(rp); o.t11=!alive(F4.key); // 11 destroying a supporting stair
   H.reset(); const rp2=H.ramp(3,0,0,0), F5=H.floor(4,0,1); H.edit(rp2,[7,6]); o.t11b=!alive(F5.key)&&T.pieces.get(rp2.key).dir===2;                                  //    turning that stair away drops it too
   H.reset(); const a=H.wall('x',3,0,0), bb=H.wall('x',4,0,0), F6=H.floor(3,0,1); H.edit(a,[4]); T.destroyPiece(bb); T.beginEdit(T.pieces.get(a.key)); T.resetEdit(); // 12
   o.t12=alive(a.key)&&T.pieces.get(a.key).mask===511&&alive(F6.key)&&!alive(bb.key);
   H.reset(); const sA=H.wall('x',3,0,0), sB=H.wall('z',3,1,0), FF=H.floor(3,0,1); H.edit(sA,[6,7,8]); o.multi=alive(FF.key);         // still held by the other wall
   return o; });
 ok('structure 1: a floor on the ground is anchored',st.t1);
 ok('structure 2: a floor on a wall stands, and falls when the wall is destroyed',st.t2a&&st.t2b,st);
 ok('structure 3: a platform reaching out from an anchored piece stands',st.t3);
 ok('structure 4: a tower stands through its connections; destroying the base drops everything above',st.t4&&st.t4b,st);
 ok('structure 5-7: a bridge with two supports survives losing one',st.t5,st);
 ok('structure 8: and falls when the last support goes',st.t6,st);
 ok('structure 9: editing a floor out from under a wall drops that wall (the floor stays)',st.t9pre&&st.t9,st);
 ok('structure 10: editing away a wall\'s top row drops the platform it held; a window keeps it',st.t10&&st.t10b,st);
 ok('structure 11: destroying a supporting stair drops what it held; turning the stair away does too',st.t11pre&&st.t11&&st.t11b,st);
 ok('structure 12: resetting an edited piece after a neighbour was destroyed restores it and nothing else',st.t12,st);
 ok('structure: an edit that removes one of two supports keeps the platform',st.multi,st);

 // ===== 16.5 ownership =====
 const own=await ev(()=>{ H.reset(); const o={}; const mine=H.wall('x',3,0,0); o.owner=!H.edit(mine,[4]).refused&&T.pieces.get(mine.key).mask!==511;
   const theirs=H.wall('x',5,0,0,{owner:'p2'}); T.settings.editRule='owner'; o.blocked=!!H.edit(theirs,[4]).refused&&T.pieces.get(theirs.key).mask===511;
   T.settings.editRule='anyone'; o.allowed=!H.edit(theirs,[4]).refused; T.settings.editRule='owner';
   const gone=H.wall('x',6,0,0); T.removePiece(gone); T.beginEdit(gone); o.destroyed=!T.edit;
   const c=H.wall('x',7,0,0); T.beginEdit(c); [1,4].forEach(i=>T.paintTile(i)); T.exitEdit(false); o.cancel=T.pieces.get(c.key).mask===511;
   const world=H.wall('x',8,0,0,{owner:'world'}); o.world=!!H.edit(world,[4]).refused;
   o.host={badWall:!T.shapeValid(mine,{mask:0b111000111}),badRamp:!T.shapeValid(H.ramp(9,0,0,0),{dir:0,half:-1,path:[0,3,1]}),goodRamp:T.shapeValid(T.pieces.get('m9_0_0'),{dir:0,half:-1,path:[0,1,3,2]})};
   return o; });
 ok('ownership: you can edit your own build',own.owner,own);
 ok('ownership: another player\'s build is refused, unless "anyone can edit" is on',own.blocked&&own.allowed,own);
 ok('ownership: a destroyed piece can\'t enter edit mode; map buildings can\'t be edited',own.destroyed&&own.world,own);
 ok('ownership: cancelling an edit leaves the piece exactly as it was',own.cancel,own);
 ok('host check: impossible shapes sent by a player are refused',own.host.badWall&&own.host.badRamp&&own.host.goodRamp,own.host);
 console.log(R.join('\n')); console.log((R.filter(x=>x.startsWith('FAIL')).length)+' failed of '+R.length); console.log(errs.join('\n')||'no page errors'); await b.close(); })();

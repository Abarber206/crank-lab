// in a party, the Locker stage shows only your hero with no name tag, its pad fits inside the picture, and the room code chip stays hidden behind the menu.  node tstageone.js
const {sleep,page,launch,open}=require('./h.js');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','renderer,net,party,get _stage(){return _stage}'),{vp:{width:1400,height:900}});
 await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await sleep(2000);
 await pg.evaluate(()=>{ T.net.role='client'; T.net.code='K7Q2'; T.net.id='me1'; T.party.list=[{id:'me1',name:'Me',o:0,ready:true},{id:'p2',name:'Pal',o:2,ready:true,lead:true},{id:'p3',name:'Bud',o:3,ready:false}]; document.querySelector('button[data-tab=locker]').click(); });
 await sleep(6000);
 const r=await pg.evaluate(()=>{ const S=T._stage, v=new THREE.Vector3(), c=S.r.domElement; S.cam.updateMatrixWorld(); let minX=1,maxX=-1;
   for(let a=0;a<64;a++){ v.set(Math.cos(a/64*Math.PI*2)*1.25*S.pad.scale.x,0,Math.sin(a/64*Math.PI*2)*1.25*S.pad.scale.z).project(S.cam); minX=Math.min(minX,v.x); maxX=Math.max(maxX,v.x); }
   return {heroes:S.heroes.length,plates:getComputedStyle(document.getElementById('plates')).display,room:document.getElementById('hudRoom').hidden,padScale:+S.pad.scale.x.toFixed(2),minX:+minX.toFixed(2),maxX:+maxX.toFixed(2)}; });
 const el=await pg.$('#stage'); await el.screenshot({path:'/home/claude/work/stage_one.png',timeout:200000});
 console.log(JSON.stringify(r)); const ok=r.heroes===1&&r.plates==='none'&&r.room===true&&r.minX>-1&&r.maxX<1; console.log(ok?'PASS':'FAIL'); console.log(errs.slice(0,4).join('\n')||'no errors'); await b.close(); })();

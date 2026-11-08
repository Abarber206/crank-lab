// two players: edits (arch, L stair) sync exactly; an edit that cuts support collapses on both screens; a forged shape is refused
const {sleep,page,launch,open}=require('./h.js'); const {ExpressPeerServer}=require('peer'); const express=require('express'); const http=require('http');
const app=express(), srv=http.createServer(app); app.use('/',ExpressPeerServer(srv,{path:'/'})); srv.listen(9102,'127.0.0.1');
const html=page('/home/claude/crank-lab/index.html','scene,toggleDoor,P,net,pieces,addPiece,beginEdit,exitEdit,paintTile,netOp,tryPlace,computeTarget,slabTop,makeBoxes,get edit(){return edit}',
  '<script>window.CRANK_PEER_OPTS={host:"127.0.0.1",port:9102,path:"/",secure:false,config:{iceServers:[]}}</script>');
(async()=>{ const b=await launch(); const R=[]; const ok=(n,p,d)=>R.push((p?'PASS ':'FAIL ')+n+' — '+JSON.stringify(d));
 const H=await open(b,html,{name:'H',fast:true,norender:true}), C=await open(b,html,{name:'C',fast:true,norender:true});
 for(const X of [H,C]){ await X.pg.waitForFunction(()=>window.T&&T.pieces,null,{timeout:120000}); await X.pg.evaluate(()=>{ const s=document.querySelector('#botSel'); s.value='off'; s.dispatchEvent(new Event('change')); }); }
 await H.pg.evaluate(()=>document.getElementById('hostBtn').click()); await H.pg.waitForFunction(()=>T.net.code,null,{timeout:30000}); const code=await H.pg.evaluate(()=>T.net.code);
 await C.pg.fill('#jcode',code); await C.pg.evaluate(()=>document.getElementById('joinBtn').click()); await C.pg.waitForFunction(()=>T.net.role==='client'&&T.net.id,null,{timeout:60000});
 await sleep(1500);
 await C.pg.evaluate(()=>{ const d=T.pieces.delete.bind(T.pieces); T.pieces.delete=k=>{ if(k==='wx3_0_0') console.error('DEL '+new Error().stack.split('\n').slice(4,12).join(' <- ')); return d(k); }; });
 // the guest builds through the normal path (placed by the guest, checked by the host)
 const place=(pg,t)=>pg.evaluate(t=>{ t.owner=T.net.id; t.mat='wood'; t.instant=true; const p=T.addPiece(t); T.netOp({op:'place',t:Object.assign({},t)}); return p.key; },t);
 const wk=await place(C.pg,{type:'wall',axis:'x',i:3,j:0,l:0,key:'wx3_0_0'}), fk=await place(C.pg,{type:'floor',i:3,j:0,l:1,key:'f3_0_1'}), rk=await place(C.pg,{type:'ramp',i:5,j:0,l:0,dir:0,sdir:0,key:'m5_0_0'});
 const wait=async(pg,f,arg,ms=15000)=>{ const t0=Date.now(); while(Date.now()-t0<ms){ if(await pg.evaluate(f,arg)) return true; await sleep(500); } return false; };
 ok('the host gets the guest\'s pieces',await wait(H.pg,k=>k.every(x=>T.pieces.has(x)),[wk,fk,rk]),[wk,fk,rk]);
 process.on('unhandledRejection',e=>{ console.log(R.join('\n')); console.log('guest errs:',C.errs.join(' ## ')); console.log('ERROR',String(e).split('\n')[0]); process.exit(1); });
 const tr=async(l)=>console.log('  ',l,'guest',await C.pg.evaluate(k=>{ const p=T.pieces.get(k); return (p?p.mask:'GONE')+' role '+T.net.role+' gap '+Math.round(performance.now()-(T.net.hostSeen||0))+' toast '+document.getElementById('toast').textContent+' banner '+document.getElementById('banTitle').textContent; },wk),'host',await H.pg.evaluate(k=>{ const p=T.pieces.get(k); return p?p.mask+' owner '+p.owner:'GONE'; },wk));
 const edit=(pg,key,tiles)=>pg.evaluate(([key,tiles])=>{ T.beginEdit(T.pieces.get(key)); if(!T.edit) return 'refused'; tiles.forEach(i=>T.paintTile(i)); T.exitEdit(true); const p=T.pieces.get(key); return p?{mask:p.mask,dir:p.dir,half:p.half,path:p.path}:'gone'; },[key,tiles]);
 const shapeOf=(pg,key)=>pg.evaluate(key=>{ const p=T.pieces.get(key); return p?JSON.stringify({mask:p.mask,path:p.path||null,boxes:T.makeBoxes(p)}):'gone'; },key);
 // arch (removes bottom row + centre) keeps the top row, so the floor stays
 const a=await edit(C.pg,wk,[0,1,2,4]); await wait(H.pg,k=>T.pieces.get(k).mask!==511,wk);
 ok('the guest\'s arch looks and collides the same on the host',await shapeOf(H.pg,wk)===await shapeOf(C.pg,wk),{guest:a,host:await shapeOf(H.pg,wk)});
 await tr('before L'); const L=await edit(C.pg,rk,[0,1,3]); await tr('after L'); await wait(H.pg,k=>!!T.pieces.get(k).path,rk);
 const hs=await H.pg.evaluate(k=>{ const p=T.pieces.get(k); return [T.slabTop(p,26.25,1.25),T.slabTop(p,28.75,3.75),T.slabTop(p,26.25,3.75)]; },rk), cs=await C.pg.evaluate(k=>{ const p=T.pieces.get(k); return [T.slabTop(p,26.25,1.25),T.slabTop(p,28.75,3.75),T.slabTop(p,26.25,3.75)]; },rk);
 ok('the guest\'s L stair has the same walking surface on both screens',JSON.stringify(hs)===JSON.stringify(cs)&&hs[2]===null,{host:hs,guest:cs});
 // half wall: removes the top row, so the floor loses its only support: the host decides it falls, and the guest sees it fall
 await tr('before'); const e0=await edit(C.pg,wk,[]); await tr('after reopen '+JSON.stringify(e0)); await sleep(1500); await tr('later');
 await C.pg.evaluate(k=>{ T.beginEdit(T.pieces.get(k)); },wk); await C.pg.evaluate(()=>{ [0,1,2,4].forEach(i=>T.paintTile(i)); }); await C.pg.evaluate(()=>T.exitEdit(true)); // clear back to full
 await tr('after clear'); await sleep(1500); await tr('later2');
 const hw=await edit(C.pg,wk,[6,7,8]);
 const gone=await wait(H.pg,k=>!T.pieces.has(k),fk)&&await wait(C.pg,k=>!T.pieces.has(k),fk);
 ok('a guest\'s edit that cuts the floor\'s support makes it fall on both screens',gone,{edit:hw});
 // doors: a guest's door edit has a door; opening it on the guest opens it for the host too
 const dk=await place(C.pg,{type:'wall',axis:'x',i:8,j:0,l:0,key:'wx8_0_0'}); await wait(H.pg,k=>T.pieces.has(k),dk);
 await edit(C.pg,dk,[1,4]); await wait(H.pg,k=>T.pieces.get(k).doors&&T.pieces.get(k).doors[1],dk);
 await C.pg.evaluate(k=>{ T.P.pos.set(38,0,2.5); T.toggleDoor(T.pieces.get(k),1,false); },dk);
 const dopen=await wait(H.pg,k=>{ const p=T.pieces.get(k); return p&&p.doors&&p.doors[1]&&p.doors[1].open; },dk);
 ok('a guest opens a door and it opens for the host too',dopen,{});
 // a forged impossible shape (top row hanging) is refused by the host and put back on the guest
 await C.pg.evaluate(k=>{ T.netOp({op:'shape',key:k,mask:0b111000111,dir:0,half:-1,path:null}); },wk);
 await sleep(3000);
 const hm=await H.pg.evaluate(k=>T.pieces.get(k).mask,wk), cm=await C.pg.evaluate(k=>T.pieces.get(k).mask,wk);
 ok('a forged impossible shape is refused by the host',hm!==0b111000111&&cm===hm,{host:hm,guest:cm});
 console.log(R.join('\n')); console.log('host:',H.errs.join('\n')||'no errors'); console.log('guest:',C.errs.join('\n')||'no errors'); await b.close(); srv.close(); process.exit(0); })();

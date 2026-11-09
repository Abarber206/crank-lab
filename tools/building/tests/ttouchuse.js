// phone layout: the top-row buttons (menu, inventory, emote) never overlap each other, in landscape and portrait
const {sleep,page,launch}=require('./h.js'); const fs=require('fs'); const path=require('path');
(async()=>{ const b=await launch(); let ok=true;
 for(const [nm,vp] of [['land',{width:844,height:390}],['land2',{width:740,height:360}],['port',{width:390,height:844}]]){
  const ctx=await b.newContext({viewport:vp,hasTouch:true,isMobile:true,deviceScaleFactor:1}); const pg=await ctx.newPage(); const errs=[]; pg.on('pageerror',e=>errs.push(e.message));
  const NM=path.join(__dirname,'node_modules'); for(const [pat,f] of [['**/three.min.js','three/build/three.min.js'],['**/peerjs.min.js','peerjs/dist/peerjs.min.js']]) await pg.route(pat,r=>r.fulfill({body:fs.readFileSync(path.join(NM,f)),contentType:'text/javascript'}));
  await pg.route('https://fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
  const html=page('/home/claude/crank-lab/index.html','scene,renderer,settings').replace('<script>\n','<script>\ntry{ localStorage.setItem("cranklab.settings",JSON.stringify({shadows:false,grassLevel:"off",clouds:"simple",skyDrop:false,bot:"off"})); }catch(e){}\n');
  await pg.route('http://127.0.0.1:9101/',r=>r.fulfill({body:html,contentType:'text/html'})); await pg.goto('http://127.0.0.1:9101/');
  await pg.waitForFunction(()=>window.T&&T.renderer,null,{timeout:180000}); await pg.evaluate(()=>document.getElementById('play').click()); await sleep(2500);
  const r=await pg.evaluate(()=>{ document.getElementById('tUse').hidden=false; const ids=['menuBtn','tBag','emoteBtn','tUse','tFire','tJump'], R=ids.map(id=>{ const e=document.getElementById(id); const b=e.getBoundingClientRect(); return {id,vis:!e.hidden&&getComputedStyle(e).display!=='none',l:b.left,r:b.right,t:b.top,b:b.bottom}; });
    const hit=[]; for(let i=0;i<R.length;i++) for(let j=i+1;j<R.length;j++){ const a=R[i], c=R[j]; if(a.vis&&c.vis&&a.l<c.r-1&&c.l<a.r-1&&a.t<c.b-1&&c.t<a.b-1) hit.push(a.id+'/'+c.id); }
    const mm=document.querySelector('.mapwrap'), mb=mm&&mm.getBoundingClientRect(); R.forEach(a=>{ if(mb&&a.vis&&a.l<mb.right-1&&mb.left<a.r-1&&a.t<mb.bottom-1&&mb.top<a.b-1) hit.push(a.id+'/minimap'); });
    return {hit,R:R.map(a=>a.id+':'+Math.round(a.l)+'-'+Math.round(a.r))}; });
  await pg.screenshot({path:'tu_'+nm+'.png'}); console.log(nm,JSON.stringify(r),errs.join(';')||'no errors'); if(r.hit.length) ok=false; await ctx.close(); }
 console.log(ok?'PASS':'FAIL'); await b.close(); })();

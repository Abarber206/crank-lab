// node tmap.js out.png [cx cz half]  -> the big map image (or a crop of it, in world metres relative to spawn)
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const {pg,errs}=await open(b,page('/home/claude/crank-lab/index.html','scene,P,renderer,TOWNS,WORLD,SPAWN,WGEN,renderBigMapImage'),{fast:true,norender:true});
 await pg.waitForFunction(()=>window.T&&T.renderer&&T.TOWNS,null,{timeout:180000});
 const [cx,cz,half]=process.argv.slice(3).map(Number);
 const url=await pg.evaluate(([cx,cz,half])=>{ const c=T.renderBigMapImage(); if(!half) { const o=document.createElement('canvas'); o.width=o.height=1024; o.getContext('2d').drawImage(c,0,0,1024,1024); return o.toDataURL('image/png'); }
   const S=c.width, mpp=1664/S, o=document.createElement('canvas'); o.width=o.height=900; o.getContext('2d').drawImage(c,(cx-half+832)/mpp,(cz-half+832)/mpp,2*half/mpp,2*half/mpp,0,0,900,900); return o.toDataURL('image/png'); },[cx,cz,half]);
 fs.writeFileSync(process.argv[2],Buffer.from(url.split(',')[1],'base64')); console.log(errs.join('\n')||'no errors'); await b.close(); })();

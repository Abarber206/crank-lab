// shared test harness: load index.html in swiftshader chromium with local three/peerjs, expose internals as window.T
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
const NM=path.join(__dirname,'node_modules');
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
function page(file,expose,extraHead){
  let html=fs.readFileSync(file||'/home/claude/crank-lab/index.html','utf8');
  if(expose){ const n=html.match(/\n\}\)\(\);\n<\/script>/g); if(!n||n.length!==1) throw new Error('expose anchor count '+(n&&n.length));
    html=html.replace(/\n\}\)\(\);\n<\/script>/,"\nwindow.T={"+expose+"};\n})();\n</script>"); }
  if(extraHead) html=html.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',extraHead+'\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>');
  return html; }
async function launch(){ return chromium.launch({executablePath:require('fs').readdirSync('/opt/pw-browsers/chromium-1243').includes('chrome-linux64')?'/opt/pw-browsers/chromium-1243/chrome-linux64/chrome':'/opt/pw-browsers/chromium-1243/chrome-linux/chrome',args:['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--disable-features=WebRtcHideLocalIpsWithMdns,LocalNetworkAccessChecks,BlockInsecurePrivateNetworkRequests']}); }
async function open(b,html,o={}){
  if(o.fast){ html=html.replace('<script>\n','<script>\ntry{ localStorage.setItem("cranklab.settings",JSON.stringify({shadows:false,reflect:false,grassLevel:"off",autoRes:false,clouds:"simple"})); }catch(e){}\n'); o.vp=o.vp||{width:320,height:200}; }
  const ctx=await b.newContext({viewport:o.vp||{width:640,height:400}}); const pg=await ctx.newPage(); const errs=[];
  pg.on('pageerror',e=>errs.push((o.name||'')+' ERR '+e.message+' '+(e.stack||'').split('\n').slice(1,3).join(' | ')));
  pg.on('console',m=>{ if(m.type()==='error') errs.push((o.name||'')+' console: '+m.text()); if(o.log) console.log('  [page]',m.text()); });
  for(const [pat,f] of [['**/three.min.js','three/build/three.min.js'],['**/peerjs.min.js','peerjs/dist/peerjs.min.js']]) await pg.route(pat,r=>r.fulfill({body:fs.readFileSync(path.join(NM,f)),contentType:'text/javascript'}));
  await pg.route('https://fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'}));
  await pg.route('https://fonts.gstatic.com/**',r=>r.abort());
  const url=o.url||'http://127.0.0.1:9101/';
  await pg.route(url,r=>r.fulfill({body:html,contentType:'text/html'}));
  const t0=Date.now(); await pg.goto(url,{timeout:180000});
  if(o.norender){ await pg.waitForFunction(()=>window.T&&T.scene,null,{timeout:180000}); await pg.evaluate(()=>{ T.scene.visible=false; }); } // logic, physics and networking still run; nothing is drawn
  return {pg,errs,ctx,t0}; }
module.exports={sleep,page,launch,open};

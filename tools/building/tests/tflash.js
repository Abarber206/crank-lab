// the very first paint (before any game script runs) is already the lobby look
const {sleep,page,launch,open}=require('./h.js'); const fs=require('fs');
(async()=>{ const b=await launch(); const ctx=await b.newContext({viewport:{width:1000,height:600}}); const pg=await ctx.newPage();
 let html=fs.readFileSync('/home/claude/crank-lab/index.html','utf8'); html=html.replace(/<script[\s\S]*?<\/script>/g,''); // no scripts at all
 await pg.route('https://fonts.googleapis.com/**',r=>r.fulfill({body:'',contentType:'text/css'})); await pg.route('http://127.0.0.1:9101/',r=>r.fulfill({body:html,contentType:'text/html'}));
 await pg.goto('http://127.0.0.1:9101/'); await sleep(300); await pg.screenshot({path:'flash.png'});
 const r=await pg.evaluate(()=>({cls:document.getElementById('menu').className,bg:getComputedStyle(document.getElementById('menu')).backgroundImage.slice(0,30)}));
 console.log(JSON.stringify(r), /lobby/.test(r.cls)&&/gradient/.test(r.bg)?'PASS':'FAIL'); await b.close(); })();

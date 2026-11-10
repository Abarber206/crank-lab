# ---------- 80. polish pass 2 ----------
# (a) asphalt: twice the texture resolution with finer, softer grain (it looked blotchy and smeared up close)
rep("const roadTex=(()=>{ const W=128, Hh=512,","const roadTex=(()=>{ const W=256, Hh=1024,")
rep("  for(let i=0;i<9000;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(22,24,28,.35)':v<.9?'rgba(140,140,138,.22)':'rgba(200,196,186,.3)'; g.fillRect(Math.random()*W,Math.random()*Hh,1+Math.random(),1+Math.random()); }\n  for(let i=0;i<14;i++){ const x=Math.random()*W, y=Math.random()*Hh, r=8+Math.random()*24,",
    "  for(let i=0;i<60000;i++){ const v=Math.random(); g.fillStyle=v<.5?'rgba(22,24,28,.26)':v<.9?'rgba(140,140,138,.16)':'rgba(200,196,186,.22)'; g.fillRect(Math.random()*W,Math.random()*Hh,1+Math.random(),1+Math.random()); }\n  for(let i=0;i<22;i++){ const x=Math.random()*W, y=Math.random()*Hh, r=20+Math.random()*50,")
rep("g.fillRect(6,0,3,Hh); g.fillRect(W-9,0,3,Hh);   // edge lines","g.fillRect(12,0,6,Hh); g.fillRect(W-18,0,6,Hh);   // edge lines")
rep("g.fillRect(W/2-2,0,4,Hh*0.5);","g.fillRect(W/2-4,0,8,Hh*0.5);")
# (b) knocked: the camera lifts up and back a little so you can see yourself crawling
rep("  const side=0.6-0.05*adsK-0.3*skyCamK-0.35*kartCamK, back=2.9-1.35*adsK+3.4*skyCamK+1.4*kartCamK, up=0.18+0.08*adsK+1.0*skyCamK+0.45*kartCamK;",
    "  downCamK+=((P.down?1:0)-downCamK)*Math.min(1,lastDt*3);\n  const side=0.6-0.05*adsK-0.3*skyCamK-0.35*kartCamK-0.4*downCamK, back=2.9-1.35*adsK+3.4*skyCamK+1.4*kartCamK+0.9*downCamK, up=0.18+0.08*adsK+1.0*skyCamK+0.45*kartCamK+0.7*downCamK;")
rep("function updateCamera(){\n","var downCamK=0;\nfunction updateCamera(){\n")
rep('Update: Nov 9 · knocked &amp; revive, reboot cards &amp; vans, new lobby &amp; Item Shop, realistic gun sounds','Update: Nov 9 · polish pass, bot teammate, dances, knocked &amp; revive, reboot vans, new lobby &amp; shop')

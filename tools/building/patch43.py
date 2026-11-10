# ---------- 43. polished loot glow; a gentle filmic tone map (a little deeper and richer, a touch of fantasy) ----------
rep("""  const beam=new THREE.Mesh(new THREE.CylinderGeometry(.05,.18,3.2,10,1,true).translate(0,1.6,0),new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:.28,blending:THREE.AdditiveBlending,depthWrite:false}));
  const ring=new THREE.Mesh(new THREE.RingGeometry(.3,.5,24).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:.5,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide})); ring.position.y=.03;""",
"""  // a soft column of light that fades out as it rises, a round glow pooled on the ground, and a few motes drifting up
  const beam=new THREE.Mesh(new THREE.CylinderGeometry(.07,.2,3.4,16,1,true).translate(0,1.7,0),new THREE.MeshBasicMaterial({color:col,map:lootTex().beam,transparent:true,opacity:.55,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide}));
  const ring=new THREE.Mesh(new THREE.PlaneGeometry(1.5,1.5).rotateX(-Math.PI/2),new THREE.MeshBasicMaterial({color:col,map:lootTex().pool,transparent:true,opacity:.7,blending:THREE.AdditiveBlending,depthWrite:false})); ring.position.y=.04;
  const motes=new THREE.Points(new THREE.BufferGeometry().setAttribute('position',new THREE.Float32BufferAttribute([...Array(7)].flatMap(()=>[(Math.random()-.5)*.35,Math.random()*2.4,(Math.random()-.5)*.35]),3)),new THREE.PointsMaterial({color:col,size:.07,map:lootTex().mote,transparent:true,blending:THREE.AdditiveBlending,depthWrite:false}));
  beam.add(motes); beam.userData.motes=motes;""")
rep("function lootRarity(item){","""let _lootTex=null;
function lootTex(){ if(_lootTex) return _lootTex; const mk=(w,h,draw)=>{ const c=document.createElement('canvas'); c.width=w; c.height=h; draw(c.getContext('2d'),w,h); const t=new THREE.CanvasTexture(c); return t; };
  _lootTex={beam:mk(4,128,(g,w,h)=>{ const gr=g.createLinearGradient(0,h,0,0); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(0.15,'rgba(255,255,255,.75)'); gr.addColorStop(0.6,'rgba(255,255,255,.22)'); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(0,0,w,h); }),
    pool:mk(64,64,(g,w,h)=>{ const gr=g.createRadialGradient(w/2,h/2,0,w/2,h/2,w/2); gr.addColorStop(0,'rgba(255,255,255,.9)'); gr.addColorStop(0.35,'rgba(255,255,255,.45)'); gr.addColorStop(0.7,'rgba(255,255,255,.12)'); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(0,0,w,h); }),
    mote:mk(16,16,(g,w,h)=>{ const gr=g.createRadialGradient(8,8,0,8,8,8); gr.addColorStop(0,'rgba(255,255,255,1)'); gr.addColorStop(1,'rgba(255,255,255,0)'); g.fillStyle=gr; g.fillRect(0,0,w,h); })};
  return _lootTex; }
function lootRarity(item){""")
rep("  const d={id,item,n,pos:pos.clone(),vel:vel?vel.clone():new THREE.Vector3(),g,model,landed:false,t:0,spin:Math.random()*6};","  const d={id,item,n,pos:pos.clone(),vel:vel?vel.clone():new THREE.Vector3(),g,model,landed:false,t:0,spin:Math.random()*6,beam:g.children.includes(beam)?beam:null,pool:ring};")
rep("function removeDrop(id){","""function stepLootGlow(dt){ const t=performance.now()/1000; drops.forEach(d=>{ if(!d.beam) return; const p=0.5+0.5*Math.sin(t*2.2+d.spin);
    d.beam.material.opacity=0.42+0.16*p; d.pool.material.opacity=0.55+0.2*p; d.pool.scale.setScalar(0.92+0.12*p);
    const m=d.beam.userData.motes, a=m.geometry.attributes.position; for(let i=0;i<a.count;i++){ let y=a.getY(i)+dt*0.55; if(y>2.6) y=0.1; a.setY(i,y); } a.needsUpdate=true; }); }
function removeDrop(id){""")
rep("stepShakes(dt); stepKarts(dt);","stepShakes(dt); stepLootGlow(dt); stepKarts(dt);")

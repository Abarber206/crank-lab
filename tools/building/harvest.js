/* ---------- harvesting: the weak point and the health bar ----------
   Swing at something you can break (a tree, a rock, a car, a wall, a crate...) and a glowing circle appears somewhere
   else on it. Hit the circle and that swing does double damage (with a crack and a flash); then it jumps to a new spot.
   Miss it and it stays where it is. While you're breaking something, a bar under the crosshair shows what it is and how
   much of it is left. Both go away a few seconds after you stop. */
const HARV={wp:null,key:null,t:0,barT:0,_v:new THREE.Vector3(),_n:new THREE.Vector3(),_a:new THREE.Vector3(),_b:new THREE.Vector3()};
function harvMesh(){ if(HARV.wp) return HARV.wp; const g=new THREE.Group();
  const ring=new THREE.Mesh(new THREE.RingGeometry(0.15,0.21,40),new THREE.MeshBasicMaterial({color:0xbfeeff,transparent:true,opacity:0.95,depthWrite:false,side:THREE.DoubleSide}));
  const disc=new THREE.Mesh(new THREE.CircleGeometry(0.15,40),new THREE.MeshBasicMaterial({color:0x37a9ff,transparent:true,opacity:0.55,depthWrite:false,side:THREE.DoubleSide}));
  const dot=new THREE.Mesh(new THREE.CircleGeometry(0.05,24),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.9,depthWrite:false,side:THREE.DoubleSide}));
  disc.position.z=-0.002; dot.position.z=0.002; g.add(disc,ring,dot); g.renderOrder=5; g.visible=false; g.userData.noCull=true; scene.add(g); return HARV.wp=g; }
// the normal of a mesh hit, in world space
function harvNormal(hit,d){ if(hit&&hit.face){ const n=HARV._n.copy(hit.face.normal).transformDirection(hit.object.matrixWorld); if(n.dot(d)>0) n.negate(); return n.clone(); } return d.clone().negate(); }
// put the weak point somewhere else on the same thing: try spots around where you hit, keep one the camera can see on it
function harvPlace(info){ const g=harvMesh(), cam=camera.position, n=info.normal, a=HARV._a.set(0,1,0); if(Math.abs(n.y)>0.85) a.set(1,0,0); const t1=HARV._b.copy(a).cross(n).normalize(), t2=new THREE.Vector3().crossVectors(n,t1);
  for(let k=0;k<14;k++){ const ang=Math.random()*Math.PI*2, r=0.45+Math.random()*0.75*(info.big?1.4:1), c=info.point.clone().addScaledVector(t1,Math.cos(ang)*r).addScaledVector(t2,Math.sin(ang)*r*0.8);
    const d=c.clone().sub(cam), L=d.length(); d.normalize(); let p=null, nn=null;
    if(info.mesh){ ray.set(cam,d); ray.near=0; ray.far=L+1.5; const h=ray.intersectObject(info.mesh,false)[0]; if(h&&Math.abs(h.distance-L)<0.7){ p=h.point; nn=harvNormal(h,d); } }
    else if(info.boxes){ let bt=null; for(const b of info.boxes){ const t=rayBox(cam,d,b); if(t>0&&(bt==null||t<bt)) bt=t; } if(bt!=null&&Math.abs(bt-L)<0.7){ p=cam.clone().addScaledVector(d,bt); nn=d.clone().negate(); } }
    if(!p) continue; if(p.y<terrainH(p.x,p.z)+0.25) continue;
    g.position.copy(p).addScaledVector(nn,0.03); g.lookAt(p.clone().add(nn)); g.visible=true; HARV.key=info.key; HARV.t=4; return true; }
  g.visible=false; HARV.key=null; return false; }
// a swing landed: returns the damage multiplier (2 on the weak point) and moves the point on
function harvHit(info){ const g=harvMesh(); let crit=false;
  if(HARV.key===info.key&&g.visible&&g.position.distanceTo(info.point)<0.42){ crit=true; burst(g.position.clone(),10,3.5,0.06,sparkMat); try{ sfx('headhit'); }catch(e){} }
  if(crit||HARV.key!==info.key||!g.visible) harvPlace(info); else HARV.t=4;
  return crit?2:1; }
function harvBar(name,hp,max){ const el=$('harvBar'); if(!el) return; el.hidden=false; HARV.barT=3; const k=Math.max(0,Math.min(1,hp/Math.max(1,max)));
  $('harvName').textContent=name; $('harvFill').style.width=(k*100).toFixed(1)+'%'; $('harvNum').textContent=Math.max(0,Math.ceil(hp))+' / '+Math.round(max); el.classList.toggle('low',k<0.3); }
function stepHarv(dt){ if(HARV.wp&&HARV.wp.visible){ HARV.t-=dt; const K=HARV.key; if(K&&((K.key&&K.type&&!K.dobj&&!pieces.has(K.key))||(K.isProp&&!K.alive)||K.gone)) HARV.t=0; const s=1+0.08*Math.sin(performance.now()/140); HARV.wp.scale.setScalar(s); if(HARV.t<=0||mode!=='pick'){ HARV.wp.visible=false; HARV.key=null; } }
  if(HARV.barT>0){ HARV.barT-=dt; if(HARV.barT<=0){ const el=$('harvBar'); if(el) el.hidden=true; } } }
const PROP_NAME={tree:'Tree',pine:'Pine',rock:'Rock',furn:'Furniture',car:'Car'};
const pieceName=p=>(MATERIALS[p.mat]?MATERIALS[p.mat].name:'')+' '+({wall:'wall',floor:'floor',ramp:'stairs',cone:'roof'}[p.type]||'piece');

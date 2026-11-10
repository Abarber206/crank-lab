# ---------- 109. the water mirrors the world: the scene is drawn again from below the surface (half size, no shadow pass
# of its own, no grass) and the water shows that image by angle, wobbled by its ripples. A setting turns it off. ----------
rep("  WATER.lv=lv; WATER.ld=ld; WATER.LN=LN; WATER.LC=LC;\n})();","""  WATER.lv=lv; WATER.ld=ld; WATER.LN=LN; WATER.LC=LC;
})();
const REFL={rt:null,cam:new THREE.PerspectiveCamera(),m:new THREE.Matrix4(),plane:new THREE.Plane(),clip:new THREE.Vector4(),q:new THREE.Vector4(),sz:new THREE.Vector2(),t:new THREE.Vector3(),hid:[]};
function renderReflection(){ if(!WATER.mat) return; const u=WATER.mat.uniforms; u.reflK.value=0;
  if(settings.reflect===false||!WATER.lv||!scene.visible) return;
  const cp=camera.position, LN=WATER.LN, i=Math.max(0,Math.min(LN-1,Math.floor((cp.x-SPAWN[0]+WHALF)/WATER.LC))), j=Math.max(0,Math.min(LN-1,Math.floor((cp.z-SPAWN[2]+WHALF)/WATER.LC))), lvl=WATER.lv[j*LN+i], off=WATER.ld[j*LN+i], hgt=cp.y-lvl;
  if(lvl<-999||off>300||hgt<0.12||hgt>180) return; // no water near, or too high up for it to matter
  const K=(1-sstep(180,300,off))*(1-sstep(120,180,hgt)); if(K<0.01) return;
  renderer.getDrawingBufferSize(REFL.sz); const w=Math.max(64,Math.round(REFL.sz.x*0.5)), h=Math.max(64,Math.round(REFL.sz.y*0.5));
  if(!REFL.rt){ REFL.rt=new THREE.WebGLRenderTarget(w,h,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat}); u.reflT.value=REFL.rt.texture; } else if(REFL.rt.width!==w||REFL.rt.height!==h) REFL.rt.setSize(w,h);
  // the camera's mirror image below the surface
  const vc=REFL.cam; camera.updateMatrixWorld(); vc.position.set(cp.x,2*lvl-cp.y,cp.z);
  REFL.t.set(0,0,-1).applyQuaternion(camera.quaternion).add(cp); REFL.t.y=2*lvl-REFL.t.y;
  vc.up.set(0,1,0).applyQuaternion(camera.quaternion); vc.up.y=-vc.up.y; vc.lookAt(REFL.t); vc.updateMatrixWorld(); vc.projectionMatrix.copy(camera.projectionMatrix);
  REFL.m.set(0.5,0,0,0.5, 0,0.5,0,0.5, 0,0,0.5,0.5, 0,0,0,1).multiply(vc.projectionMatrix).multiply(vc.matrixWorldInverse);
  // its near plane is tilted onto the water surface, so nothing below the surface is drawn (Lengyel's oblique clipping)
  REFL.plane.normal.set(0,1,0); REFL.plane.constant=-lvl; REFL.plane.applyMatrix4(vc.matrixWorldInverse);
  const cl=REFL.clip.set(REFL.plane.normal.x,REFL.plane.normal.y,REFL.plane.normal.z,REFL.plane.constant), pe=vc.projectionMatrix.elements, q=REFL.q;
  q.set((Math.sign(cl.x)+pe[8])/pe[0],(Math.sign(cl.y)+pe[9])/pe[5],-1,(1+pe[10])/pe[14]); cl.multiplyScalar(2/cl.dot(q));
  pe[2]=cl.x; pe[6]=cl.y; pe[10]=cl.z+1-0.003; pe[14]=cl.w;
  const hid=REFL.hid; hid.length=0; for(const o of [...WATER.meshes,VCLOUD.sky,grassMesh,flowerMesh]) if(o&&o.visible){ o.visible=false; hid.push(o); }
  const prev=renderer.getRenderTarget(), au=renderer.shadowMap.autoUpdate; renderer.shadowMap.autoUpdate=false; // the shadow maps from the last frame serve
  renderer.setRenderTarget(REFL.rt); renderer.clear(); renderer.render(scene,vc); renderer.setRenderTarget(prev); renderer.shadowMap.autoUpdate=au;
  for(const o of hid) o.visible=true;
  u.reflM.value.copy(REFL.m); u.reflK.value=K; u.reflY.value=lvl;
}""")
rep("renderClouds(); renderer.render(scene,camera); }","renderClouds(); renderReflection(); renderer.render(scene,camera); }")
rep("shadows:!isTouch, binds:{}};","shadows:!isTouch, reflect:!isTouch, binds:{}};")
rep('          <label for="shadows">Shadows <input type="checkbox" id="shadows"></label>','          <label for="shadows">Shadows <input type="checkbox" id="shadows"></label>\n          <label for="reflectC">Water reflections <input type="checkbox" id="reflectC"></label>')
rep("  sens.addEventListener('input',()=>{ settings.sens=+sens.value; show(); saveSettings(); });","  { const rf=$('reflectC'); rf.checked=settings.reflect!==false; rf.addEventListener('change',()=>{ settings.reflect=rf.checked; saveSettings(); }); }\n  sens.addEventListener('input',()=>{ settings.sens=+sens.value; show(); saveSettings(); });")
rep("  { const gy=terrainH(camera.position.x,camera.position.z)+0.35; if(camera.position.y<gy) camera.position.y=gy; } // never inside a hill","  { const gy=Math.max(terrainH(camera.position.x,camera.position.z)+0.35,waterAt(camera.position.x,camera.position.z)+0.3); if(camera.position.y<gy) camera.position.y=gy; } // never inside a hill, never under water")

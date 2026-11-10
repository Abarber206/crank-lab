# ---------- 112. ambient occlusion: corners, creases and the places where things meet the ground are shaded a little.
# The picture is drawn into a buffer (still anti-aliased) so its depth can be read; a half-size pass works out how
# hemmed-in each point is; the picture goes to the screen darkened there. WebGL 2 only, and a setting turns it off. ----------
rep("const REFL={rt:null,", r'''/* ---------- ambient occlusion ---------- */
const AO={ok:renderer.capabilities.isWebGL2&&typeof THREE.WebGLMultisampleRenderTarget==='function',rt:null,ao:null,sz:new THREE.Vector2(),n:0};
function aoInit(w,h){ if(AO.rt){ AO.rt.dispose(); AO.ao.dispose(); }
  const rt=AO.rt=new THREE.WebGLMultisampleRenderTarget(w,h,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat});
  rt.depthTexture=new THREE.DepthTexture(w,h,THREE.UnsignedIntType); // 24 bits: the 16 it would get otherwise are far too coarse a few metres out
  const aw=Math.max(8,w>>1), ah=Math.max(8,h>>1), ao=AO.ao=new THREE.WebGLRenderTarget(aw,ah,{minFilter:THREE.LinearFilter,magFilter:THREE.LinearFilter,format:THREE.RGBAFormat,depthBuffer:false});
  if(!AO.cam){ AO.cam=new THREE.Camera(); const g=new THREE.BufferGeometry().setAttribute('position',new THREE.Float32BufferAttribute([-1,-1,0,3,-1,0,-1,3,0],3));
    AO.matA=new THREE.ShaderMaterial({depthTest:false,depthWrite:false,uniforms:{tDepth:{value:null},tColor:{value:null},projInv:{value:new THREE.Matrix4()},res:{value:new THREE.Vector2()},pscale:{value:1}},
      vertexShader:`void main(){ gl_Position=vec4(position.xy,0.0,1.0); }`,
      fragmentShader:`uniform sampler2D tDepth, tColor; uniform mat4 projInv; uniform vec2 res; uniform float pscale;
        vec3 vpos(vec2 uv){ float d=texture2D(tDepth,uv).x; vec4 v=projInv*vec4(uv*2.0-1.0,d*2.0-1.0,1.0); return v.xyz/v.w; }
        void main(){ vec2 uv=gl_FragCoord.xy/res; if(texture2D(tDepth,uv).x>=0.99999||texture2D(tColor,uv).a<0.25){ gl_FragColor=vec4(1.0); return; } // sky, or grass (which marks itself in the picture's alpha)
          vec3 P=vpos(uv); float dist=-P.z, fade=1.0-smoothstep(55.0,120.0,dist), rpx=min(0.8*pscale/dist,40.0), rad=rpx*dist/pscale; // the reach on screen (capped), and what that comes to in metres here
          if(fade<=0.0||rpx<1.5){ gl_FragColor=vec4(1.0); return; }
          vec2 px=1.0/res; vec3 Pr=vpos(uv+vec2(px.x,0.0)), Pl=vpos(uv-vec2(px.x,0.0)), Pu=vpos(uv+vec2(0.0,px.y)), Pd=vpos(uv-vec2(0.0,px.y));
          vec3 dx=abs(Pr.z-P.z)<abs(P.z-Pl.z)?Pr-P:P-Pl, dy=abs(Pu.z-P.z)<abs(P.z-Pd.z)?Pu-P:P-Pd, N=normalize(cross(dx,dy)); // the surface's facing, from its neighbours
          vec2 ip=mod(floor(gl_FragCoord.xy),4.0); float ang=(ip.x+ip.y*4.0)*2.7488936, occ=0.0, cnt=0.0; // sixteen turns of the pattern over each 4x4 pixels: the blur that follows covers exactly that
          for(int i=0;i<10;i++){ float fi=(float(i)+0.5)/10.0, a=ang+float(i)*2.3999632; vec2 suv=uv+vec2(cos(a),sin(a))*sqrt(fi)*rpx*px; if(texture2D(tColor,suv).a<0.25) continue; // ten points on a spiral around it (not grass)
            vec3 v=(vpos(suv)-P)/rad; float vv=dot(v,v), f=max(1.0-vv,0.0); occ+=f*f*f*max((dot(v,N)-0.07)/(vv+0.04),0.0); cnt+=1.0; }                                                                       // how far each one rises above the surface
          float ao=clamp(1.0-occ/max(cnt,1.0)*1.15,0.0,1.0);
          gl_FragColor=vec4(vec3(mix(1.0,ao,fade)),1.0); }`});
    AO.matC=new THREE.ShaderMaterial({depthTest:false,depthWrite:false,uniforms:{tColor:{value:null},tAO:{value:null},res:{value:new THREE.Vector2()},ares:{value:new THREE.Vector2()}},
      vertexShader:`void main(){ gl_Position=vec4(position.xy,0.0,1.0); }`,
      fragmentShader:`uniform sampler2D tColor, tAO; uniform vec2 res, ares;
        void main(){ vec2 uv=gl_FragCoord.xy/res, c=floor(uv*ares+0.5), p=1.0/ares; vec4 col=texture2D(tColor,uv);
          float ao=(texture2D(tAO,(c+vec2(-1.0,-1.0))*p).r+texture2D(tAO,(c+vec2(1.0,-1.0))*p).r+texture2D(tAO,(c+vec2(-1.0,1.0))*p).r+texture2D(tAO,(c+vec2(1.0,1.0))*p).r)*0.25; // a 4x4 average: four samples, each between four pixels
          ao=mix(1.0,ao,step(0.25,col.a));
          gl_FragColor=vec4(col.rgb*(ao+(1.0-ao)*vec3(0.14,0.16,0.24)),1.0); }`}); // laid on with a cool tint rather than as plain black
    AO.sA=new THREE.Scene(); AO.sC=new THREE.Scene(); for(const [s,m] of [[AO.sA,AO.matA],[AO.sC,AO.matC]]){ const q=new THREE.Mesh(g,m); q.frustumCulled=false; s.add(q); } }
  AO.matA.uniforms.tDepth.value=rt.depthTexture; AO.matA.uniforms.tColor.value=rt.texture; AO.matA.uniforms.res.value.set(aw,ah); AO.matC.uniforms.tColor.value=rt.texture; AO.matC.uniforms.tAO.value=ao.texture; AO.matC.uniforms.res.value.set(w,h); AO.matC.uniforms.ares.value.set(aw,ah);
  const gl=renderer.getContext(); for(let i=0;i<8&&gl.getError()!==gl.NO_ERROR;i++); AO.n=0; }
// the picture: straight to the screen, or by way of the buffers above
function renderMain(){ if(!AO.ok||settings.ao===false||!scene.visible){ renderer.render(scene,camera); return; }
  renderer.getDrawingBufferSize(AO.sz); const w=AO.sz.x, h=AO.sz.y;
  if(!AO.rt||AO.rt.width!==w||AO.rt.height!==h){ try{ aoInit(w,h); }catch(e){ console.warn('ambient occlusion unavailable',e); AO.ok=false; renderer.render(scene,camera); return; } }
  renderer.setRenderTarget(AO.rt); renderer.render(scene,camera);
  AO.matA.uniforms.projInv.value.copy(camera.projectionMatrixInverse); AO.matA.uniforms.pscale.value=AO.ao.height*0.5*camera.projectionMatrix.elements[5];
  renderer.setRenderTarget(AO.ao); renderer.render(AO.sA,AO.cam); renderer.setRenderTarget(null); renderer.render(AO.sC,AO.cam);
  if(AO.n<3&&++AO.n===3){ const gl=renderer.getContext(); if(gl.getError()!==gl.NO_ERROR){ console.warn('ambient occlusion switched off: the graphics driver refused it'); AO.ok=false; } } } // (checked once, after the first few frames)
const REFL={rt:null,''')
rep("renderClouds(); renderReflection(); renderer.render(scene,camera); }","renderClouds(); renderReflection(); renderMain(); }")
rep("shadows:!isTouch, reflect:!isTouch, binds:{}};","shadows:!isTouch, reflect:!isTouch, ao:!isTouch, binds:{}};")
rep('          <label for="reflectC">Water reflections <input type="checkbox" id="reflectC"></label>','          <label for="reflectC">Water reflections <input type="checkbox" id="reflectC"></label>\n          <label for="aoC">Ambient occlusion (soft shading in corners and where things meet the ground) <input type="checkbox" id="aoC"></label>')
rep("  { const rf=$('reflectC'); rf.checked=settings.reflect!==false;","  { const ac=$('aoC'); ac.checked=settings.ao!==false&&AO.ok; ac.disabled=!AO.ok; ac.addEventListener('change',()=>{ settings.ao=ac.checked; saveSettings(); }); }\n  { const rf=$('reflectC'); rf.checked=settings.reflect!==false;")
# grass and flowers leave the picture's alpha at 0 where they are drawn: that is how the shading pass knows to leave them alone
rep("  [grassMesh,flowerMesh].forEach(m=>{ m.receiveShadow=true; m.frustumCulled=false;","  grassMat.opacity=0; flowerMat.opacity=0;\n  [grassMesh,flowerMesh].forEach(m=>{ m.receiveShadow=true; m.frustumCulled=false;")

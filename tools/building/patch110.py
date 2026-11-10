# ---------- 110. shadows reach much farther: a second, coarser shadow map takes over beyond the sharp one near you
# (out to about 200 m), with trees in that range casting into it ----------
rep("renderer.shadowMap.enabled=true;\nrenderer.shadowMap.type=THREE.PCFSoftShadowMap;","""renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
// two-step shadows: with two shadow-casting directional lights, the first one's map is used close up and the second
// one's (coarser, far wider) beyond it, blended over the last few metres of the first
THREE.ShaderChunk.shadowmap_pars_fragment+=`
#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 1
float csmShadow() {
	vec3 p = vDirectionalShadowCoord[ 0 ].xyz / vDirectionalShadowCoord[ 0 ].w;
	vec2 e = min( p.xy, 1.0 - p.xy );
	float k = p.z > 1.0 ? 0.0 : clamp( min( e.x, e.y ) / 0.07, 0.0, 1.0 );
	float s0 = k > 0.0 ? getShadow( directionalShadowMap[ 0 ], directionalLightShadows[ 0 ].shadowMapSize, directionalLightShadows[ 0 ].shadowBias, directionalLightShadows[ 0 ].shadowRadius, vDirectionalShadowCoord[ 0 ] ) : 1.0;
	vec3 q = vDirectionalShadowCoord[ 1 ].xyz / vDirectionalShadowCoord[ 1 ].w;
	vec2 e1 = min( q.xy, 1.0 - q.xy );
	float k1 = q.z > 1.0 ? 0.0 : clamp( min( e1.x, e1.y ) / 0.06, 0.0, 1.0 );
	float s1 = ( k < 1.0 && k1 > 0.0 ) ? getShadow( directionalShadowMap[ 1 ], directionalLightShadows[ 1 ].shadowMapSize, directionalLightShadows[ 1 ].shadowBias, directionalLightShadows[ 1 ].shadowRadius, vDirectionalShadowCoord[ 1 ] ) : 1.0;
	return mix( mix( 1.0, s1, k1 ), s0, k );
}
#endif`;
{ const a='\\t#if NUM_DIR_LIGHT_SHADOWS > 0\\n\\tDirectionalLightShadow directionalLight;', c=THREE.ShaderChunk.shadowmask_pars_fragment;
  if(c.indexOf(a)<0) console.warn('shadow mask chunk not as expected'); THREE.ShaderChunk.shadowmask_pars_fragment=c.replace(a,'\\t#if NUM_DIR_LIGHT_SHADOWS > 1\\n\\tshadow *= receiveShadow ? csmShadow() : 1.0;\\n\\t#elif NUM_DIR_LIGHT_SHADOWS > 0\\n\\tDirectionalLightShadow directionalLight;');
  const b='directLight.color *= all( bvec2( directLight.visible, receiveShadow ) ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;', d=THREE.ShaderChunk.lights_fragment_begin;
  if(d.indexOf(b)<0) console.warn('light chunk not as expected'); THREE.ShaderChunk.lights_fragment_begin=d.replace(b,'#if NUM_DIR_LIGHT_SHADOWS > 1\\n\\t\\t#if UNROLLED_LOOP_INDEX == 0\\n\\t\\tdirectLight.color *= all( bvec2( directLight.visible, receiveShadow ) ) ? csmShadow() : 1.0;\\n\\t\\t#endif\\n\\t\\t#else\\n\\t\\t'+b+'\\n\\t\\t#endif'); }""")
rep("scene.add(sun); scene.add(sun.target);","""scene.add(sun); scene.add(sun.target);
// the far shadow map's light: same direction as the sun, no light of its own; redrawn a few times a second, not every frame
const sunFar=new THREE.DirectionalLight(0x000000,0); sunFar.castShadow=settings.shadows&&!isTouch; sunFar.shadow.mapSize.set(2048,2048);
{ const fc=sunFar.shadow.camera, hb=204.8; fc.left=-hb; fc.right=hb; fc.top=hb; fc.bottom=-hb; fc.near=1; fc.far=1100; sunFar.shadow.bias=-0.0009; sunFar.shadow.normalBias=1.1; /* generous: its texels are 20 cm, and a wall seen edge-on by the light would speckle with less */ sunFar.shadow.autoUpdate=false; sunFar.shadow.needsUpdate=true; }
scene.add(sunFar); scene.add(sunFar.target);
const FARS={a:1e9,b:1e9,t:0,dir:new THREE.Vector3()};
function placeFarShadow(pos){ if(!sunFar.castShadow) return; const now=performance.now(), st=8, a=Math.round(pos.dot(_lX)/st)*st, b=Math.round(pos.dot(_lY)/st)*st; // it follows you in 8 m steps (40 of its texels)
  if(a===FARS.a&&b===FARS.b&&now-FARS.t<(FARS.dir.equals(SUN_DIR)?420:300)) return; FARS.a=a; FARS.b=b; FARS.t=now; FARS.dir.copy(SUN_DIR);
  sunFar.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,pos.dot(SUN_DIR)); sunFar.position.copy(sunFar.target.position).addScaledVector(SUN_DIR,520); sunFar.shadow.needsUpdate=true; }""")
rep("    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,c); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); }","    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,c); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); placeFarShadow(P.pos); }")
rep("    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,cc); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); }","    sun.target.position.set(0,0,0).addScaledVector(_lX,a).addScaledVector(_lY,b).addScaledVector(SUN_DIR,cc); sun.position.copy(sun.target.position).addScaledVector(SUN_DIR,65); placeFarShadow(pl.pos); }")
rep("sh.addEventListener('change',()=>{ settings.shadows=sh.checked; sun.castShadow=sh.checked; saveSettings(); });","sh.addEventListener('change',()=>{ settings.shadows=sh.checked; sun.castShadow=sh.checked; sunFar.castShadow=sh.checked&&!isTouch; sunFar.shadow.needsUpdate=true; FARS.t=0; saveSettings(); });")
# trees between the detailed ones and the far ones cast into the far map only
rep("  FOREST.near={}; FOREST.far={};","""  FOREST.near={}; FOREST.far={}; FOREST.mid={};
  const midDepth=new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking}); // drawn into the wide shadow map only: in the sharp one near you they'd be out of range anyway
  midDepth.onBeforeCompile=sh=>{ sh.vertexShader=sh.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\\n\\tif( projectionMatrix[ 0 ][ 0 ] > 0.012 ) gl_Position = vec4( 2.0, 2.0, 2.0, 1.0 );'); };""")
rep("    FOREST.far[kind]=[...Array(4)].map((_,v)=>mk(farTreeGeo(kind,v),propVariant(kind,0).mat,trees.filter(p=>p.kind===kind&&p.id%4===v).length,false)); }",
    "    FOREST.far[kind]=[...Array(4)].map((_,v)=>mk(farTreeGeo(kind,v),propVariant(kind,0).mat,trees.filter(p=>p.kind===kind&&p.id%4===v).length,false));\n    FOREST.mid[kind]=FOREST.far[kind].map(f=>{ const m=mk(f.geometry,f.material,f.instanceMatrix.count,true); m.customDepthMaterial=midDepth; return m; }); }")
rep("    if(d2<N2) push(FOREST.near[p.kind][p.id%8],p); else if(d2<420000||","    if(d2<N2) push(FOREST.near[p.kind][p.id%8],p); else if(d2<46000) push(FOREST.mid[p.kind][p.id%4],p); else if(d2<420000||")
rep("  for(const set of [FOREST.near,FOREST.far]) for(const kind in set)","  for(const set of [FOREST.near,FOREST.mid,FOREST.far]) for(const kind in set)")

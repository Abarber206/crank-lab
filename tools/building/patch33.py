# ---------- 33. soft atmospheric haze; chests are done once opened ----------
# Haze: real air. It thickens with distance and thins with height, so the far valleys soften into the pale horizon
# while peaks stand out above it. (fog.near is the haze density per metre, fog.far its thinning height.)
rep("scene.fog=new THREE.Fog(HAZE,250,2600); // distance fades into a pale horizon haze, like real air",
r"""const HAZE_DENS=0.00095, HAZE_H=210;
scene.fog=new THREE.Fog(HAZE,HAZE_DENS,HAZE_H); // near = density, far = scale height (see the fog chunks below)
THREE.ShaderChunk.fog_pars_vertex='#ifdef USE_FOG\n\tvarying float fogDepth;\n\tvarying float vFogY;\n#endif';
THREE.ShaderChunk.fog_vertex='#ifdef USE_FOG\n\tfogDepth = - mvPosition.z;\n\tvFogY = ( ( mvPosition.xyz - viewMatrix[ 3 ].xyz ) * mat3( viewMatrix ) ).y;\n#endif';
THREE.ShaderChunk.fog_pars_fragment='#ifdef USE_FOG\n\tuniform vec3 fogColor;\n\tvarying float fogDepth;\n\tvarying float vFogY;\n\t#ifdef FOG_EXP2\n\t\tuniform float fogDensity;\n\t#else\n\t\tuniform float fogNear;\n\t\tuniform float fogFar;\n\t#endif\n#endif';
THREE.ShaderChunk.fog_fragment=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * fogDepth * fogDepth );
	#else
		// exponential height haze: the amount of air along the view ray, thinning with height
		float fH = max( fogFar, 1.0 ), fy0 = clamp( cameraPosition.y, -40.0, 4000.0 ), fq = ( vFogY - fy0 ) / fH;
		float fk = abs( fq ) > 1e-3 ? ( 1.0 - exp( - fq ) ) / fq : 1.0;
		float fogFactor = clamp( 1.0 - exp( - fogNear * exp( - fy0 / fH ) * fk * fogDepth ), 0.0, 0.93 );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`;""")
rep("scene.fog.near=250-190*duskK; scene.fog.far=2600-2360*duskK;","scene.fog.near=HAZE_DENS+(0.0042-HAZE_DENS)*duskK; scene.fog.far=HAZE_H-90*duskK;")
# chests: no refills. An opened chest is done: it sinks away a moment after the loot flies out, and only a new match
# (or a new round) brings the chests back
rep("    if(c.open&&net.role!=='client'){ c.respawnT-=dt; if(c.respawnT<=0&&d>12){ closeChest(c); if(net.role==='host') netSend({type:'chestReset',id:c.id}); } }",
    "    if(c.open){ c.goneT=(c.goneT||0)+dt; const f=Math.max(0,Math.min(1,(c.goneT-1.6)/0.6)); if(f>0){ c.g.scale.setScalar(1-0.85*f); c.g.position.y=c.y-0.5*f; if(f>=1) c.g.visible=false; if(!c.poofed){ c.poofed=true; if(d<60) burst(new THREE.Vector3(c.x,c.y+0.4,c.z),8,2.5,0.06,chestMats.gold); } } }")
rep("function closeChest(c){ c.open=false; c.prog=0; c.respawnT=0; }","function closeChest(c){ c.open=false; c.prog=0; c.respawnT=0; c.goneT=0; c.poofed=false; c.g.scale.setScalar(1); c.lidA=0; }")
rep("chests.forEach(c=>{ c.open=(m.co||[]).includes(c.id); c.lidA=c.open?1.95:0; });","chests.forEach(c=>{ closeChest(c); c.open=(m.co||[]).includes(c.id); c.lidA=c.open?1.95:0; if(c.open){ c.goneT=9; c.poofed=true; } });")
rep("function clearBuilds(){ resetKarts();","function clearBuilds(){ resetKarts(); if(typeof chests!=='undefined') chests.forEach(closeChest);")

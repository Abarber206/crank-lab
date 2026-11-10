# ---------- 45. a gentle colour grade: midtones a touch deeper, colours a little richer, cool shadows and warm highlights ----------
rep("const renderer=new THREE.WebGLRenderer({canvas, antialias:!isTouch || devicePixelRatio<2});",r"""const renderer=new THREE.WebGLRenderer({canvas, antialias:!isTouch || devicePixelRatio<2});
THREE.ShaderChunk.tonemapping_pars_fragment=THREE.ShaderChunk.tonemapping_pars_fragment.replace('vec3 CustomToneMapping( vec3 color ) { return color; }',`vec3 CustomToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	float l = dot( color, vec3( 0.2126, 0.7152, 0.0722 ) );
	color = mix( vec3( l ), color, 1.14 );                                           // a little richer
	color = pow( max( color, 0.0 ), vec3( 1.07 ) );                                 // midtones a touch deeper
	color += vec3( -0.012, 0.0, 0.022 ) * ( 1.0 - smoothstep( 0.0, 0.35, l ) );    // cool, slightly magical shadows
	color += vec3( 0.03, 0.016, -0.008 ) * smoothstep( 0.45, 1.0, l );             // warm light
	return clamp( color, 0.0, 1.0 ); }`);
renderer.toneMapping=THREE.CustomToneMapping; renderer.toneMappingExposure=1.0;""")

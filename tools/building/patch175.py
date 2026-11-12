# patch175: things lying about the island (see decor.js): campsites, power lines, hay fields, street furniture, a dock and
# rowboats, boats on the river banks, fallen logs and stumps, picnic tables, and clutter round the points of interest.
DECOR_JS=open('/home/claude/mg/decor.js').read()
rep("""function buildBridges(){""",DECOR_JS+"""
function buildBridges(){""")
rep("""buildBridges(); buildRails(); buildLandmarks(); buildSigns();""","""buildBridges(); buildRails(); buildLandmarks(); buildSigns(); buildWorldDecor();""")
rep("""  // one strongbox at the foot of each town's landmark, on the side facing the town""","""  for(const [x,y,z,a] of DECOR.chests) addChest(x,y,z,a); // one at each campsite
  // one strongbox at the foot of each town's landmark, on the side facing the town""")

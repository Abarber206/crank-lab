# Rebuilding index.html in a fresh session
    mkdir -p /home/claude/mg && cp -r tools/building/* /home/claude/mg/ && chmod +x /home/claude/mg/build.sh
    /home/claude/mg/build.sh        # -> "patched N" / "syntax ok"; writes /home/claude/crank-lab/index.html
Patches live in /home/claude/mg/patchNN.py (driver patch.py execs them in order; rep(a,b,count) asserts the anchor count).
Tests: copy tools/building/tests/* into a scratch dir; h.js page(file, exposeList) exposes internals as T.*; run with `timeout 115 node tX.js`.
After a successful build, copy changed patch files back into tools/building/ before committing.

# patch193: rarity changes a gun's damage only (not its reload): rarer is stronger, otherwise the same gun
rep("const RSTAT={common:{d:0.9,r:1.12},uncommon:{d:0.95,r:1.06},rare:{d:1,r:1},epic:{d:1.05,r:0.94},legendary:{d:1.1,r:0.88}};","const RSTAT={common:{d:0.9,r:1},uncommon:{d:0.95,r:1},rare:{d:1,r:1},epic:{d:1.05,r:1},legendary:{d:1.1,r:1}};")

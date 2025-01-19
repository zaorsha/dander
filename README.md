# dander
Virtual walking app

##### App Version: 0.1

### Ideas
---
- Make this a historical walking app: Walking tours throughout vast historical regions: WW1 (Walk the Western Front, Eastern Front etc)
- Add group of 'Virtual Friends' to walk with, each at different paces, to help push you to win
- Embed your walk within the timeframe, creating a story around it. e.g WW1 walk: "Reach Ghent by Jan 21st to deliver a vital message to Army Command"
- Audio narration would be ideal for each section, but bonus idea / feature if ever possible.

### To-Do
---
- Get main app loop to function as expected: Add distance, map updates, DB saves and restores on reopen. Completion of trail shows 'Finished' screen.

### Known Bugs
---



### Changelog
---
##### Version 0.1
#### Bug Fixes
2. Route colour only changes after first distance addition (Fix: route is being coloured from the start, so green is overlapping green)
1. The maths of adding distance only works the first 2 times. Subsequent additions work unexpectedly.
3. Only the initial distance added is committed to the db

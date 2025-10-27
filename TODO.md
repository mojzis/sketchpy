
## meta stuff
- claude skills 🚧
 - testing ?
- ideas interchange with claude.ai 🚧
- ci/cd
 - (some) tests ?
- tests for javascript features ?
- license ? (not copyright ...)
- use newest pyodide, test the lib on the python it supports

## features
- nicer homepage 🚧
 - add usual stuff like favicon ...
 - add social links
 - colored code !
- link to home ?
- theme switching
  - create lessons per theme though ?
- canvas higher, allow user to move
- save code to github gists ☮️
- lessons 🚧
- safe execution ✅
  - timeout protection (5s limit with worker termination)
  - import blocking (allow stdlib validation modules, block user imports)
  - AST validation (block eval/exec/__import__/dangerous patterns)
  - canvas limits (max size, max shapes)
  - client-side validation (code length, forbidden patterns)
  - comprehensive test coverage with error reporting
- sharing
 - security though ?
- help panel
 - for this lib
 - basic python help ☮️
- palletes
  - add a function to show the current pallete, ✅
  - pick palletes,
  - switch pallets
- add color picker ?
- help
 - canvas - generated from code (meticulously explain each param)
 - python - basic principles, with examples (as links to editor ?)

 - ai
  - document sketch lib
  - llm.txt file

## drawing improvements
- gradients ✅
  - linear gradients with customizable colors and offsets
  - radial gradients with center/radius control
- named groups ✅
  - group context manager for organizing shapes
  - group transformations (move, rotate)
  - group visibility control (hide/show)
  - group removal
- splines
- object manipulation (copy, change color)


## much later
i18n ? :)

## NTH
auto reload in browser for development ?
- drawing lib - make it faster to load ?

## DONE
- canvas: add a posibility to show a grid
- improve editor experience  (- use a better code editor - like we have in streamlit ?)
- when i run uv srv, it should restart if running
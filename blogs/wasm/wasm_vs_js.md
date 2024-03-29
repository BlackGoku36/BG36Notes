# WebAssembly vs Javascript

Table of contents:

- [Introduction](intro.html)
- WASM vs JS
- [Binary Format](binary_format.html)
- [Emscripten](emscripten.html)

---

WebAssembly wasn't designed and created to replace Javascript, but rather complement it and make two of them work together in tandem. As we will see, some part of code should see benefits from using WASM when compared to JS, but some parts rather be in JS itself. We will discuss about what problem Javascript has, how WebAssembly solves it, what are WebAssembly limitations and benefits are over Javascript.

## What problem does Javascript have?

---

The browser has to fetch javascript code from the server, than compile it just like any other language. Depending on how a particular browser implement it, javascript is either compiled to bytecode, machine code or just interpreted in old-school way. The browser has to do this on go, and it might have to compile/interpret same piece of code multiple time.

1. **Download-time and Load-time latency:**
	- Browser has to fetch javascript code from server, and since the size of a text file is lot more than size of binary file, it will take lot more time to download which will leads to load-time latency. This is important on web, the less data you need to download the better it is. That is why there are programs such as js/css minifier which try to shave of as many as bytes possible by removing whitespaces or turning many-words identifiers into few-chars identifiers.
	- Compiler has to parse the text-file first, then convert it to code to another format (intermediate representation), optimize it and finally convert it to end format (such as bytecode or machine code). Parsing + Optimization take lot of time, so we have even more latency.
2. **Execution Speed:**
	- To decrease the above load-time latency, implementation sometimes only compile a certain part of code instead of whole, this might means that compile might have to compile a particular part of code again and again. This redundancy will make the whole code lot more slower.
	- To decrease the load-time even more, the implementation can just skip optimisation passes, which would make the resulting code lot more slower.
	- Javascript language design such as dynamic typing and garbage collection (automatic memory management), would make things even more worse.

## How does it solve those problems?

---

To solve the above problem, WASM was introduced.

1. **Download-time and load-time latency:**
	- Browser would "only" need to fetch binary file(s) that is already compiled. So the amount of bytes to fetch would be lot less, and also we would skip all the compilation steps and just run it directly.
2. **Execution Speed**:
	- Whole code is compile to WASM bytecode, so there no need to re-compile some parts again and again.
	- Since, the bytecode would already be compiled and optimized by compiler, the code would run even more faster.
	- Since, system programming language like C, Rust, Zig, etc is used to compile to binary, and since they are typically static typed with manual memory management, we would have more faster code.

## Additional benefits

---

- **Single Instruction Multiple Data (SIMD)**: WASM supports vector operations that are native to hardware. With this you can run calculations that requires doing same operations but on multiple data, which are typically used in image and signal processing.
- **Multi-Threading**: Although not additional as javascript can do it with WebWorker API, you can enjoy low over-head with WASM.

## Limitations?

---

1. **Performance**: Although many times WASM is faster than JS, there are times browser can compile JS to native code (by using technique called [Just-In-Time Compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation)) and execute it. It wins when compilation overhead is lot less than the execution of the said code. Javascript engines such as JavascriptCore (WebKit, Safari) and V8 (Chromium, Chrome) are capable of doing this. This can change in coming year, as WASM is still relatively new technology and JS have been giving years of head start for optimization.
2. **Javascript can't be eliminated entirely**: It is not possible to manipulate DOM's element directly from WASM, instead it is done through binding between JS and WASM. Also, just manipulating a button color (through WASM) doesn't incur any performance penalty, doing it repeatedly can become overhead.

# Introduction to WebAssembly (WASM)

Table of contents:

- Introduction
- [WASM vs JS](wasm_vs_js.html)
- [Binary Format](binary_format.html)
- [Emscripten](emscripten.html)

---

In short, WebAssembly is a binary instruction format for a stack-based VM. To understand it better, we will talk a little bit more about what a `Binary Instruction Format` means and what a `Stack-based VM` means.

It was design for improving performance of web application and allow it to do computational expensive tasks that was previously not possible with JS. It is portable format, which can work in enviroment outside of browsers such as desktop/mobile apps, client/server application, IoTs, and even embedded devices.

Before WASM, [asm.js](https://en.wikipedia.org/wiki/Asm.js) existed that compiled statically-typed manual memory management language such as C to optimized version of JS. It used source-to-source compiler that targeted specific subset of JS. This subsets consisted of static types and virtually no [garbage collection](https://en.wikipedia.org/wiki/Garbage_collection_%28computer_science%29), which improved performanc by magnitudes. It also optimized size by employing techniques like [dead-code elimination](https://en.wikipedia.org/wiki/Dead-code_elimination), and also remove unnecessary whitespace, newlines, etc and shortening long identifier to few chars identifiers.

<details>
	<summary>What is Garbage Collection?</summary>
	<p>Basically garbage means allocated memory that isn't used anymore, and collection means de-allocating this not-used-anymore memory.\
	In manual memory management languages, you allocate and deallocate memory by yourself. But in Garbage Collected language, the language do it for you. How GC does it and when depends upon implemented technique, you wouldn't want GC to do it work at inconvient time in inconvient ways.</p>
</details>

## Binary Instruction Format

---

Just like humans use languages to understand and communicate with each other, computer need something similar. Human languages consist of atomic symbols such as alphabets, just as machine language consist of 0s and 1s. These symbols randomly stringed together, themselves doesn't means anything. Just like `kdjhsk` doesn't means anything, random 0s and 1s `01010101` doesn't means anything. Language defines rules for these symbols and strings to give a meaning, like `hello` means greeting in `English` languge. Zeros and Ones can be given meaning with language designed particularly for a machine.

For sake of understanding, we can design our own machine language. Let say, our language is based on bit string of length 8-bit (called as byte), which is analogous to a word in english language (although a word can be of arbitarary length). To understand a sentence, we say that string of bytes, start with a verb and than, if any, we have noun. For example, a byte string `"10100000 00100101"`, `10100000` is a verb and `00100101` is a noun. Similarly, `"10010011 00100100 00010000 10000001"` is verb, noun, verb and noun respectively. Then we can go an add rules for what a verb and what a noun is. For example,

Byte     Meaning
-------- --------
00______ Walk
01______ Run
10______ Sprint
11______ Stop
-------- --------

Then we can define next 2-bits for vocal cords, and then next-next 2-bits and so on and on. For verb, it could means human names somehow mapped to a byte. This will effectively give us a way to command any (actually upto 2^8 = 255 here) humans in our machine languge.

There already exist machine language for computer, these language are sometimes called `Instruction Set Architecture (ISA)`, such as `x86_64`, `RISC-V`, `ARM64`, etc. WebAssembly is another one of these language, but for a made-up hardware.

## Stack-based VM

---

Virtual Machine (VM) as the name implies, a machine that is virtual and not a physical hardware. VMs are software that emulates a specific machine, typically they emulates ISAs. These works for decoding the binary files (executables), then it try to make sense of the structure, and then execute appropriate similar instruction that are available natively.

Stack-based means that it uses stack as storage for immediate temporary values instead of registers like ISAs. For example, you want to execute following line of code:
```c
printf(1 + 2);
```
The order of instructions and it execution look something like this:

Instruction  Operation   Stack
-----------  ----------- -----
1            push 1      1
2            push 2      1, 2
3            add         3
4            call printf null
-----------  ----------- -----

## Binary Instruction Format for Stack-based VM

---

So, WebAssembly is just a portable specification developed for a machine that uses stack, which main goal is to be used in Web. But since it is just a format, it can be used anywhere as long as VM is compilant and provides interface for the enviroment (just like how ISAs interface with OS enviroment through function calls and other stuffs).

# Introduction to WASM

Table of contents:

- Introduction (this)
- Binary Format
- Emscripten (emcc)

In short, WebAssembly is a binary instruction format for a stack-based VM. To understand it better, we will talk a little bit more about what a `Binary Instruction Format` means and what a `Stack-based VM` means.

### Binary Instruction Format

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

!WIP!

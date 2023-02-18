# Cache Memory Notes

## What a cache memory?

DRAM performance improve lot slower compared to CPU performance, as a result DRAM and CPU performance gap keep on increasing. Chances are that your CPU is already done it's job and is waiting (idling) for data from DRAM to continue further, here the DRAM speed is bottelnecking CPU speed. To solve this, we put smaller but faster (also more costy) memory on CPU. Chunk(s) of memory (DRAM) is loaded into this, so that CPU can immediately access it. This memory is know as cache memory.

Memory hierarchy looks something like this:

```txt
                          |  DRAM
    Size and              |  L3 (shared between processes)
         latency decrease |  L2
                          v  L1 (Data), L1 (Instruction)
```
*Hierarchy is showen as formality, we don't have to keep levels of cache is mind when programming*

## Associativity

Associativity of cache is how copy of main-memory is mapped to cache.
You can think of cache as an N-Byte 3D array, though the 2D array is laid linearly one after another instead of stack. This is how it look like:

```txt
{ // 3
    { // 2
        { a, b, c, d, e, f, g, h }, // 1
        { i, j, k, l, m, n, o, p }
    },
    {
        { q, r, s, t, u, v, w, x },
        { y, z, !, @, #, $, %, ^ }
    }
}
```
1. This is cache line (aka block), here each bytes are contiguous. It's size can be X-byte long, here it's 8 bytes.
2. A Group of cache lines is called a set. There can be Y number of sets.
3. Cache consists of Y sets * X bytes.

### Fully associative cache

Here the memory of cache's block size is placed anywhere in the cache (This means there 0 set). For example, if you have memory like:
```txt
{ a, b, c, d,  e, f, g, h,  i, j, k, l,  m, n, o, p,  q, r, s, t,  u, v, w, x }
```
1. Each alphabet represent 1-byte, so there are 24 bytes.

If you have fully associative cache memory with 4 cache block and of size 4-bytes, then your cache memory might be like:
```txt
{
    a, b, c, d,
    i, j, k, l,
    , , , ,     // Empty cache block
    u, v, w, x
}
```

That is, the cache block is placed randomly (well not randomly, there are different types of policies for eviction and replacement for these cache block).

- **Pro**:
    1. You can fit large amount of data from anywhere in memory into cache.

- **Con**:
    1. You will have to linearly search the whole cache memory to find the desired block.

### Direct-mapped cache

TBD

### Set-associative cache

TBD

---

Agenda:

- Explain what cache memory is and why does it matter.
- What is direct mapped, associative and set-associative cache memory.
- Simple calculations of things like cache address bits and determine different things of the cache memory that helps with understanding of data in cache.
- Different types of misses and how it can be improved.
- Real-life example of code that hate cache:
    - Multiplication of huge N matrix with sub matrix and how it can be optimised.
    - Why Linked list sucks in this regard.
    - Why Bubble sort is faster than merge sort when data size is small. (Not tested, purely theoritical).
- Why nobody (except those who want high performance design, I don't think cache memory is big brain thing tho) seems to give fuck about cache memory even if it taught in university.
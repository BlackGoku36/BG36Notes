# WebAssembly Binary Format

! WIP !

## Values

How different values such as bytes, ints and floats are encoded in this binary format.

### Bytes

They are encoded as themeselves:
- 0x00..0xFF = 0x00..0xFF

### Integers



> All integers used for sizes and indexes in this binary formats are in unsigned LEB128 format.

## Structure

Structure are divided into different sections, each with a specific id, and are order-dependent. Each of the sections are optional and can be skipped. The module starts with a magic number (0x00, 0x61, 0x73, 0x6D) ('/0asm' string) and a version number (0x01, 0x00, 0x00, 0x00) (current version of wasm binary format is 1).


| ID  | Sections   |
| --- | ---------- |
| 0   | Custom     |
| 1   | Type       |
| 2   | Import     |
| 3   | Function   |
| 4   | Table      |
| 5   | Memory     |
| 6   | Global     |
| 7   | Export     |
| 8   | Start      |
| 9   | Element    |
| 10  | Code       |
| 11  | Data       |
| 12  | Data count |

## Sections

Each sections are divided into 3 parts:

- Id of the section - 1 Byte
- Size of content in bytes - unsigned leb128
- Content of sections (dependent of structure of the section)

> All of the sections can be skipped. WASM file that only consist of 8 bytes (0x00, 0x61, 0x73, 0x6D, 0x01, 0x00, 0x00, 0x00) is a valid binary.

> Size of each section other than custom can be skipped. Size can be used to skip sections while navigating through a binary. Size of custom section are needed to skip the entire section in case implementation doesn't support it.

> Implementation: Errors in custom sections shouldn't prevent it from parsing other sections.

## Custom

!WIP!

## Type

This section is used to define signature of all functions. It contains vector of functype. This section look like:

- Id: byte = 1
- Size: unsigned leb128 = size of contents in bytes
- Content: vec(functype) = array of functype elements

Eg:
```
|  Id  | Size |                                Content                                            |
|      |      | len  |      |    parameter 1     |   result 1  |      | parameter 2 |   result 2  |
|      |      |      |      | len  | i32  | f32  | len  | f32  |      |     len     | len  | f64  |
| 0x01 | 0x09 | 0x02 | 0x60 | 0x02 | 0x7F | 0x7D | 0x01 | 0x7D | 0x60 |     0x0     | 0x01 | 0x7C |
                     |<------------ function sig. 1 ---------->|<--------- function sig. 2 ------>|
```

### Function Type - functype
Function type defines signature of function and is encoded as:

- `0x60`
- parameter: resulttype
- results: resulttype

Eg:
```
|      |      parameter     |    result   |
|      | len  | i32  | f32  | len  | f32  |
| 0x60 | 0x02 | 0x7F | 0x7D | 0x01 | 0x7D |
```
It defines function type with 2 parameters (i32 and f32) and single return/result type of f32

### Result Type - resulttype

- resulttype: vec(valtype) = array of valtype elements

### Value Type - valtype

- valtype: numtype or vectype or reftype

### Number Type - numtype

- i32 = 0x7F
- i64 = 0x7E
- f32 = 0x7D
- f64 = 0x7C

### Vector Type - vectype

- v128 = 0x7B

### Reference Type - reftype

- funcref = 0x70
- externref = 0x6F

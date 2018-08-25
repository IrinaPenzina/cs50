# Questions

## What's `stdint.h`?

It's a standart library in C which allows you work with the specified-width integer types of C99 (i.e. "int32_t", "uint16_t" etc.).

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

**`uint8_t`** - unsinged 8 bit integer, **`uint32_t`** - unsinged 32 bit integer, **`int32_t`** -singed 32 bit integer, and **`uint16_t`** - unsinged 16 bit integer.
These integers will be the same size in any machine you use.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

**`BYTE`** - 8 bits, a **`DWORD`** - (double word) 32 bits or 4 bytes, a **`LONG`** - 4 bytes, and a **`WORD`** - 16 bits or 2 bytes .


## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The first two bytes of any BMP file are 424d e601.

## What's the difference between `bfSize` and `biSize`?

bfSize - the size of the file itself. biSize - the number of bytes required by the structure.

## What does it mean if `biHeight` is negative?

 If biHeight is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

No file.

## Why is the third argument to `fread` always `1` in our code?

It is the total number of elements successfully read.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

Padding = 3.

## What does `fseek` do?

**`fseek`** allows you to change the location of the file pointer.

## What is `SEEK_CUR`?

It's a curent position of the file.

## Whodunit?

It was Professor Plum with the candlestick in the library.

# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?
Pneumonoultramicroscopicsilicovolcanoconiosis is a word invented by the president of the National Puzzlers' League as a synonym for the disease known as silicosis.
It is the longest word in the English language published in a dictionary, the Oxford English Dictionary, which defines it as "an artificial long word said to mean a lung disease
caused by inhaling very fine ash and sand dust.


## According to its man page, what does `getrusage` do?

getrusage - get resource usage.
RUSAGE_SELF - Return resource usage statistics for the calling process, which is the sum of resources used by all threads in the process.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16 variables.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Passing by reference secures that you are passing correct information from its address.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.
Every program in C starts with "main" and returns an integer. It reads file from the beginning to the end. So, all declarations has to be done before they are used.

Function "for" loop - for loop consists of three parts 1.variable 2. condition 3. Incrimination
1. variable. it can be any integer declared within the loop or outside the loop. the integer is executed first and only once.
2. condition. if condition is true it will be executed next, if it false the command after that loop will be executed.
3. Incrimination. the loop will be executed again and again until the condition is true when it becomes false the loop will be terminated.


## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

The problem might be in the return value. This function returns the number of input items successfully matched and assigned,
which can be fewer than provided for, or even zero in the event of an early matching failure.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

The const keyword specifies that a variable's value is constant and tells the compiler to prevent the programmer from modifying it.

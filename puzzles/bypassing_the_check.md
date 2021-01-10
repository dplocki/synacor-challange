# Bypassing the check

From the [previous puzzle](./check_code.ipynb) I know, that function on line `6027` is the check function. Not counting the recursion, the function it is called from just one place. Near the useage of `register7`:

```txt
    5483:     set  register_0   4
    5486:     set  register_1   1
    5489:    call  6027
    5491:      eq  register_1   register_0   6
    5495:      jf  register_1   5579
    5498:    push  register_0
    5500:    push  register_1
    5502:    push  register_2
    5504:     set  register_0   29014
    5507:     set  register_1   1531
    5510:     add  register_2   1425         3171
    5514:    call  1458
    5516:     pop  register_2
    5518:     pop  register_1
    5520:     pop  register_0
    5522:     set  register_0   register_7
    5525:     set  register_1   25866
    5528:     set  register_2   32767
    5531:    push  register_3
    5533:     set  register_3   29241
    5536:    call  1841
    5538:     pop  register_3
    5540:    push  register_0
    5542:    push  register_1
    5544:    push  register_2
```

The easiest will be simply to remove memory cell `5489` and the following `5490`: the optcode and its the only paramater. Removing by replace them by `nope` operation.

Also, after the invoke of the function `6027` program is checking the call result:

```txt
    5491:      eq  register_1   register_0   6
    5495:      jf  register_1   5579
```

The meaning of the code:

```py
register_1 = _6027(register_0, register_1)
if register_1 != 6:
    goto :5579
```

Because we have removed the call to the check function, we have replace optcode `jf` with `jt`.

The final code which I have added into [../main.py], just after loading the invoking `load_dump_file`.

```py
    # Set register 7
    registers[32775] = 25734

    # removing call checking function
    #  5489:    call  6027
    memory[5489] = 21
    memory[5490] = 21

    # Removing check of result checkfunction
    #  5495:      jf  register_1   5579
    memory[5495] = 7
```

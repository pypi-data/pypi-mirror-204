![Tests](https://github.com/jesse-wei/SAPsim/actions/workflows/tests.yml/badge.svg)

# SAPsim

> Simulation of [SAP (Simple As Possible) computer](img/SAP.png) programs from COMP311 (Computer Organization) @ [UNC](https://unc.edu)

## How to program

Write a SAP program in the format given in [`template.csv`](template.csv). Also see [`example.csv`](tests/public_prog/example.csv) ([output full speed](tests/data/public_prog/example_full_speed.txt)) ([output debug mode](tests/data/public_prog/example_debug.txt)).

You may edit the `.csv` files in Microsoft Excel. Pass the path to your SAP program as a CLI argument. It'll then be run in debug mode (default). Alternatively, apply the `-s` option to run at full <ins>s</ins>peed.

## Install

Your Python version needs to be 3.7+. Check with `python --version`. If you normally use `python3`, then use that.

Next, install SAPsim.

```sh
pip install SAPsim
```

If `pip` doesn't work, try `pip3`.

## Usage

Open a Python terminal or file.

```py
from SAPsim import run
run("path/to/your/SAP/program.csv")
```

For additional settings, such as running in debug (step) mode, see the [documentation](https://sapsim.readthedocs.io/en/latest/#usage).

![SAP instruction set](img/SAP_instruction_set.png)

## Rules

- All SAP programs fit in 16 addresses (0 to 15) because the program counter (`PC`) is 4-bit.
- Initial values are `{PC: 0, Register A: 0, Register B: 0, FlagC: 0, FlagZ: 0, num_bits_in_registers: 8, Executing: 1}`.
- `A` and `B` registers are unsigned and 8-bit by default. Number of bits is configurable via the `-b BITS` CLI option.
- Instructions and data are all bytes.
  - An instruction is a Mnemonic representing an Opcode (4-bit) and an Arg (4-bit).
    - For an instruction, the Arg can be represented in base-10 or base-16.
      - For example, `JC 15` can be written as Mnemonic `JC` and Arg `15` or `F`.
  - All data must fit in a byte. Specifically, the Mnemonic is a hexit, and the Arg is a hexit.
    - For example, 254 = `0xFE` is Mnemonic `F`, Arg `E`.
    - 10 = `0x0A` is Mnemonic `0`, Arg `A`. You may not omit the leading 0.
- Programs run until they `HLT` or until an [`Exception`](src/utils/exceptions.py) is raised. Infinite loops are possible, of course.
- These are the same rules a SAP computer implemented by hardware has to follow.
  - > "This is a feature, not a bug"

## Allowed syntax

In the Mnemonic column, these are allowed

- two or three letter Mnemonic (for an instruction)
- single-digit hexit `0` to `F` (for data)

In the Arg column, these are allowed

- single-digit hexit `0` to `F` (for instruction or data)
- double-digit base-10 integer `10` to `15` representing a hexit
  - e.g. `JC 15` and `JC F` are both legal and represent the same instruction

## Disallowed syntax

If you follow the templates and example programs, you won't run into any problems.

But if something goes wrong, an [`Exception`](src/utils/exceptions.py) will occur, and there'll be a descriptive error message.

## Documentation

[https://sapsim.readthedocs.io/en/latest/](https://sapsim.readthedocs.io/en/latest/)

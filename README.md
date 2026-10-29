\# cocotb-constrained-random



!\[ci](https://github.com/madhu-dev-ai/cocotb-constrained-random/actions/workflows/ci.yml/badge.svg)



A constrained-random verification testbench for an 8-bit ALU, written in Python with cocotb and simulated with Icarus Verilog.



\## What this project shows



\- A Python \*\*reference model\*\* that predicts the correct output for every input

\- \*\*Constrained-random stimulus\*\*: random inputs that favour corner values (0, 1, 127, 128, 254, 255) and force `a == b` about 20% of the time

\- \*\*Functional coverage\*\*: 12 bins, with an automatic failure if any bin is never hit

\- A \*\*planted bug\*\* that only the constrained-random test caught

\- \*\*CI\*\*: all tests run on every push with GitHub Actions



\## Design under test



`alu8.v` is a clocked 8-bit ALU with 4 operations (add, subtract, AND, OR) and 3 outputs: `result`, `carry` and `zero`.



\## Testbench structure



```mermaid

flowchart LR

&#x20;   G\[Constrained-random generator] --> D\[ALU8 design]

&#x20;   G --> M\[Python reference model]

&#x20;   D --> C\[Compare]

&#x20;   M --> C

&#x20;   C --> V\[Coverage bins]

```



\## Tests



| Test | What it does |

|------|--------------|

| `test\_fixed\_values` | 5 hand-picked cases, to check the setup works |

| `test\_random` | 500 fully random cases against the reference model |

| `test\_constrained\_random` | 1000 cases biased towards corner values |

| `test\_coverage` | 2000 cases with 12 coverage bins; fails if any bin is empty |



\## Bug found by constrained random



I planted a bug: the ALU returned 255 instead of 254 for `255 + 255`.



| Test | Result |

|------|--------|

| `test\_fixed\_values` | PASS (never tried this case) |

| `test\_random` | PASS (a 1 in 65,536 chance per try) |

| `test\_constrained\_random` | \*\*FAIL\*\* |



```

AssertionError: Mismatch at iteration 260: a=255 b=255 op=0

expected=(254, 1, 0) actual=(255, 1, 0)

```



The bug was fixed afterwards. The design in this repository is the correct version.



\## Coverage results (2000 cycles)



| Bin | Hits |

|-----|------|

| op\_add | 484 |

| op\_sub | 510 |

| op\_and | 498 |

| op\_or | 508 |

| add\_overflow | 249 |

| sub\_borrow | 191 |

| zero\_result | 248 |

| a\_equals\_b | 453 |

| a\_is\_0 | 102 |

| a\_is\_255 | 119 |

| and\_gives\_zero | 105 |

| or\_gives\_255 | 109 |



Result: \*\*12/12 bins hit\*\*.



\## Run it yourself



Requirements: Python, cocotb 2.1.0, Icarus Verilog and make.



```

make

```


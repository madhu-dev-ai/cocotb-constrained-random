# cocotb-constrained-random



[![CI](https://img.shields.io/github/actions/workflow/status/madhu-dev-ai/cocotb-constrained-random/ci.yml?branch=main&label=CI)](https://github.com/madhu-dev-ai/cocotb-constrained-random/actions/workflows/ci.yml)

A constrained-random verification testbench for an 8-bit ALU, written in Python with cocotb and simulated with Icarus Verilog.



## What this project shows



- A Python **reference model** that predicts the correct output for every input

- **Constrained-random stimulus**: random inputs that favour corner values (0, 1, 127, 128, 254, 255) and force `a == b` about 20% of the time

- **Functional coverage**: 12 bins, with an automatic failure if any bin is never hit

- A **planted bug** that only the constrained-random test caught

- **CI**: all tests run on every push with GitHub Actions



## Design under test



`alu8.v` is a clocked 8-bit ALU with 4 operations (add, subtract, AND, OR) and 3 outputs: `result`, `carry` and `zero`.



## Testbench structure



```mermaid

flowchart LR

&#x20;   G[Constrained-random generator] --> D[ALU8 design]

&#x20;   G --> M[Python reference model]

&#x20;   D --> C[Compare]

&#x20;   M --> C

&#x20;   C --> V[Coverage bins]

```



## Tests



| Test | What it does |

|------|--------------|

| `test_fixed_values` | 5 hand-picked cases, to check the setup works |

| `test_random` | 500 fully random cases against the reference model |

| `test_constrained_random` | 1000 cases biased towards corner values |

| `test_coverage` | 2000 cases with 12 coverage bins; fails if any bin is empty |



## Bug found by constrained random



I planted a bug: the ALU returned 255 instead of 254 for `255 + 255`.



| Test | Result |

|------|--------|

| `test_fixed_values` | PASS (never tried this case) |

| `test_random` | PASS (a 1 in 65,536 chance per try) |

| `test_constrained_random` | **FAIL** |



```

AssertionError: Mismatch at iteration 260: a=255 b=255 op=0

expected=(254, 1, 0) actual=(255, 1, 0)

```



The bug was fixed afterwards. The design in this repository is the correct version.



## Coverage results (2000 cycles)



| Bin | Hits |

|-----|------|

| op_add | 484 |

| op_sub | 510 |

| op_and | 498 |

| op_or | 508 |

| add_overflow | 249 |

| sub_borrow | 191 |

| zero_result | 248 |

| a_equals_b | 453 |

| a_is_0 | 102 |

| a_is_255 | 119 |

| and_gives_zero | 105 |

| or_gives_255 | 109 |



Result: **12/12 bins hit**.



## Run it yourself



Requirements: Python, cocotb 2.1.0, Icarus Verilog and make.



```

make

```


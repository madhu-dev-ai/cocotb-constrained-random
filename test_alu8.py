import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def apply(dut, a, b, op):
    """Drive inputs, wait one clock edge, then return (result, carry, zero)."""
    dut.a.value = a
    dut.b.value = b
    dut.op.value = op
    await RisingEdge(dut.clk)
    await Timer(1, "ns")  # let the outputs settle
    return int(dut.result.value), int(dut.carry.value), int(dut.zero.value)


@cocotb.test()
async def test_fixed_values(dut):
    cocotb.start_soon(Clock(dut.clk, 10, "ns").start())

    # add: 5 + 3 = 8
    assert await apply(dut, 5, 3, 0) == (8, 0, 0)
    # add overflow: 255 + 1 = 0, carry 1, zero 1
    assert await apply(dut, 255, 1, 0) == (0, 1, 1)
    # subtract with borrow: 3 - 5 = 254, carry 1
    assert await apply(dut, 3, 5, 1) == (254, 1, 0)
    # and: 0xF0 & 0x3C = 0x30
    assert await apply(dut, 0xF0, 0x3C, 2) == (0x30, 0, 0)
    # or: 0xF0 | 0x0F = 0xFF
    assert await apply(dut, 0xF0, 0x0F, 3) == (0xFF, 0, 0)
def model(a, b, op):
    """Python reference model of the ALU: returns (result, carry, zero)."""
    if op == 0:
        full = a + b
    elif op == 1:
        full = (a - b) & 0x1FF
    elif op == 2:
        full = a & b
    else:
        full = a | b
    result = full & 0xFF
    carry = (full >> 8) & 1
    zero = 1 if result == 0 else 0
    return result, carry, zero


@cocotb.test()
async def test_random(dut):
    cocotb.start_soon(Clock(dut.clk, 10, "ns").start())

    for i in range(500):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        op = random.randint(0, 3)

        expected = model(a, b, op)
        actual = await apply(dut, a, b, op)

        assert actual == expected, (
            f"Mismatch at iteration {i}: a={a} b={b} op={op} "
            f"expected={expected} actual={actual}"
        )

def pick_value():
    """Constrained pick: 40% corner values, 60% fully random."""
    if random.random() < 0.4:
        return random.choice([0, 1, 2, 127, 128, 253, 254, 255])
    return random.randint(0, 255)


def pick_inputs():
    a = pick_value()
    # 20% of the time, force b == a
    b = a if random.random() < 0.2 else pick_value()
    op = random.randint(0, 3)
    return a, b, op


@cocotb.test()
async def test_constrained_random(dut):
    cocotb.start_soon(Clock(dut.clk, 10, "ns").start())

    zero_hits = 0
    carry_hits = 0

    for i in range(1000):
        a, b, op = pick_inputs()

        expected = model(a, b, op)
        actual = await apply(dut, a, b, op)

        assert actual == expected, (
            f"Mismatch at iteration {i}: a={a} b={b} op={op} "
            f"expected={expected} actual={actual}"
        )

        zero_hits += actual[2]
        carry_hits += actual[1]

    dut._log.info(f"zero flag was 1 in {zero_hits} of 1000 cycles")
    dut._log.info(f"carry flag was 1 in {carry_hits} of 1000 cycles")
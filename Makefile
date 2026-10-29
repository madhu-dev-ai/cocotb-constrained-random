SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = alu8.v
COCOTB_TOPLEVEL = alu8
COCOTB_TEST_MODULES = test_alu8

include $(shell cocotb-config --makefiles)/Makefile.sim
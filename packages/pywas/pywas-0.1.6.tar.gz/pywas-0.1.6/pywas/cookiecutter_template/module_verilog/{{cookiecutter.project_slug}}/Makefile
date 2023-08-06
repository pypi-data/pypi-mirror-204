SIM ?= icarus
TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/{{cookiecutter.project_slug}}.v

TOPLEVEL = {{cookiecutter.project_slug}}

MODULE = test_{{cookiecutter.project_slug}}

include $(shell cocotb-config --makefiles)/Makefile.sim

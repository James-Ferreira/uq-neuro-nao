# ARM64 Darwin (macOS Apple Silicon) configuration
SYSTEM = arm64_Darwin
MACHINE_TYPE = arm64
SYSTEM_TYPE = Darwin
CC = clang
CXX = clang++
CFLAGS = -mdynamic-no-pic -arch arm64 -O3
CXXFLAGS = -mdynamic-no-pic -arch arm64 -O3
LDFLAGS = -arch arm64
RANLIB = ranlib
INSTALL = /usr/bin/install -c
AR = ar
ARFLAGS = rcs
INSTALL_PROGRAM = ${INSTALL}
INSTALL_DATA = ${INSTALL} -m 644

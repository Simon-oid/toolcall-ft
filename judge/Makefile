# The judge links cMCP's core library: the same parser and validator the
# servers run. CMCP_DIR defaults to a sibling checkout, built (`make`).
CMCP_DIR ?= ../../cMCP
CC       ?= cc
CFLAGS   ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2 -g
LDLIBS   := $(shell pkg-config --libs libcurl) -lpthread -lm

judge: judge.c $(CMCP_DIR)/build/libcmcp_core.a
	$(CC) $(CFLAGS) -I$(CMCP_DIR)/include -o $@ judge.c $(CMCP_DIR)/build/libcmcp_core.a $(LDLIBS)

clean:
	rm -f judge

.PHONY: clean

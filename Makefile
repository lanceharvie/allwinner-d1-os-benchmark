CC := /opt/homebrew/bin/riscv64-elf-gcc
CFLAGS := -march=rv64gc -mabi=lp64d -msmall-data-limit=0 -O2 -ffreestanding -fno-stack-protector
LDFLAGS := -nostdlib -nostartfiles -Wl,-e,_start -Wl,--build-id=none -Wl,--no-relax

runtime-panel: src/main.c src/font_atlas.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

src/font_atlas.h: tools/generate_font.py
	.fontenv/bin/python tools/generate_font.py

clean:
	rm -f runtime-panel

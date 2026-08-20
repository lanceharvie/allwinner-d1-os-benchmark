#!/usr/bin/env python3
"""Generate a compact 4-bit alpha C atlas from an OpenType/TrueType font."""
from pathlib import Path
from PIL import ImageFont

FONT = Path.home() / "Library/Fonts/PlusJakartaSans-Medium.ttf"
OUT = Path(__file__).resolve().parents[1] / "src/font_atlas.h"
SIZES = (13, 18, 24, 32, 40, 48)
CHARS = range(32, 127)

def generate():
    blob = bytearray()
    tables = []
    for size in SIZES:
        font = ImageFont.truetype(str(FONT), size)
        glyphs = []
        for code in CHARS:
            ch = chr(code)
            bbox = font.getbbox(ch)
            advance = int(round(font.getlength(ch)))
            if bbox is None or bbox[2] <= bbox[0] or bbox[3] <= bbox[1]:
                glyphs.append((len(blob), 0, 0, 0, 0, max(advance, 1)))
                continue
            mask = font.getmask(ch, mode="L")
            raw = bytes(mask)
            offset = len(blob)
            for i in range(0, len(raw), 2):
                hi = (raw[i] + 8) // 17
                lo = (raw[i + 1] + 8) // 17 if i + 1 < len(raw) else 0
                blob.append((min(15, hi) << 4) | min(15, lo))
            glyphs.append((offset, bbox[2]-bbox[0], bbox[3]-bbox[1], bbox[0], bbox[1], max(advance, 1)))
        tables.append(glyphs)

    with OUT.open("w") as f:
        f.write("/* Generated from Plus Jakarta Sans Medium. */\n#include <stdint.h>\n")
        f.write("struct aa_glyph{uint32_t off;uint8_t w,h;int8_t xo,yo;uint8_t adv;};\n")
        f.write(f"static const uint8_t aa_sizes[{len(SIZES)}]={{" + ",".join(map(str,SIZES)) + "};\n")
        f.write(f"static const struct aa_glyph aa_glyphs[{len(SIZES)}][95]={{\n")
        for table in tables:
            f.write("{")
            f.write(",".join("{%d,%d,%d,%d,%d,%d}" % g for g in table))
            f.write("},\n")
        f.write("};\n")
        f.write(f"static const uint8_t aa_bitmap[{len(blob)}]={{\n")
        for i in range(0, len(blob), 32):
            f.write(",".join(str(x) for x in blob[i:i+32]) + ",\n")
        f.write("};\n")
    print(f"generated {OUT} ({len(blob)} packed alpha bytes)")

if __name__ == "__main__":
    generate()

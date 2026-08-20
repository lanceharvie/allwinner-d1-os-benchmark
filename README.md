# Runtime Panel

Lightweight native 720×720 touchscreen UI for the Sipeed Lichee RV86 running Tina/MaixLinux.

![Platform](https://img.shields.io/badge/platform-Allwinner%20D1%20RISC--V-2477f2)
![UI](https://img.shields.io/badge/UI-framebuffer%20%2B%20evdev-27b56f)

## Current dashboard

The application renders directly to the detected Linux framebuffer and discovers the `fts_ts` evdev node through sysfs. It provides instant switching between `RunTime` and `Home`, a RAM back buffer, event-driven redraws, interactive mock-home controls, and live Linux metrics. It has no runtime library dependencies.

Text uses a compact 4-bit anti-aliased glyph atlas generated at build time from Plus Jakarta Sans Medium. The font renderer alpha-blends glyphs directly into the RAM back buffer. No font library or font file is required on Tina.

The navigation controls are drawn at Y=570–669, above the panel's poorly calibrated extreme lower edge. Each target is 360×100 pixels.

## Build on macOS

```sh
make
```

The Makefile uses Homebrew's `riscv64-elf-gcc` and produces the statically linked RISC-V executable `runtime-panel`.

To regenerate the font atlas, create the project-local Python environment and run:

```sh
python3 -m venv .fontenv
.fontenv/bin/pip install Pillow
.fontenv/bin/python tools/generate_font.py
```

The generator currently uses `~/Library/Fonts/PlusJakartaSans-Medium.ttf`. The generated packed atlas is committed under `src/font_atlas.h`, so normal builds do not require Python, Pillow, or the source font.

Plus Jakarta Sans is designed by Gumpita Rahayu/Tokotype and licensed under the SIL Open Font License 1.1. See `FONT-LICENSE.txt`.

## Measured footprint

- Executable: approximately 133 KiB
- Resident memory on Tina: approximately 2.1 MiB
- RunTime screen with 1 Hz metric updates: approximately 4% of one D1 core
- UI/input service rate: 10 Hz; no continuous high-frame-rate rendering

## Manual run on Tina

```sh
cd /root/runtime-panel
./runtime-panel
```

No boot or init configuration is installed. Stop any other framebuffer application before running this prototype, and restart it afterward if required.

## Safety and scope

The application does not modify the kernel, device tree, bootloader, LCD timing/profile, touchscreen driver, or network configuration. Its 60-second idle mode controls only the existing DISP2 backlight interface.

## Controls

- Tap `RunTime` or `Home` in the bottom navigation area.
- Climate `-` and `+` adjust the local target temperature.
- Tap the climate status area to toggle Cooling/Off.
- Tap a light row or switch to toggle the mock light locally.
- RunTime refreshes CPU, thermal, memory, uptime, network, display, and touch information once per second.
- After 60 seconds without touch input, the Allwinner DISP2 backlight is disabled. The first subsequent touch wakes the display and is consumed so it cannot activate a control accidentally.
- Set `RUNTIME_PANEL_DEBUG=1` in a future libc-enabled build for stdout traces; the current freestanding prototype displays coordinates directly on screen.

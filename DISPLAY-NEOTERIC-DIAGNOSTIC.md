# Neoteric Display diagnostic overlay (2026-09-14)

This is an experimental Display-only overlay on the Android 16 vendor
foundation. It is not proof of the cause of the boot failure, and has not
passed a device boot test.

## Reproduction

Use a dump with vendor, odm and system_ext partition directories. The local
prepared dump is `/tmp/xuanyuan-neo-display-dump`. From this device directory:

```sh
./extract-files.py --no-cleanup --section 'Display Neoteric*' /tmp/xuanyuan-neo-display-dump
./setup-makefiles.py
```

The selected sections contain 152 files. Keep a blank line before each section
heading: extract-utils uses blank-line-delimited sections, not every comment.
Do not use `Display*` for this overlay and do not run full extraction from this
partial dump. `Display A16 retained*` contains 19 GPU/firmware files and 57
paths absent in the Neoteric dump, plus the A16 QTI composer3 wrapper; these
must stay on the existing baseline.
The standard tinyxml fixups still apply to composer and libsdmclient.

No libbinder, libc++, bionic, Audio, KeyMint, SPL or device partition changes
are part of this overlay. Since selected files span vendor, odm and system_ext,
a vendor-only flash would not represent the prepared overlay.

## Evidence and rollback material

`D:\xuanyuan-backups-20260914` retains the pre-overlay Display tarball,
Android.bp, xuanyuan-vendor.mk, proprietary-files.txt and extract-files.py.
`displayneo-verified-0914-v3.json` records pre/post SHA256 for all 229 entries.
Source dump identity is recorded
by file hashes; its SDK label alone is not an ABI compatibility guarantee.

`displayneo-audit-0914-v3.json` records a preliminary static check of 103
candidate ELFs against local Android 16 providers. No DT_NEEDED library-name
gaps or unresolved strong symbol names were found for those candidate files.
This is a necessary check only: linker namespaces, symbol versions, dlopen
plugins, retained consumers, VINTF and runtime semantics remain to verify.

The first build failed because Neoteric composer directly needs standard
Composer AIDL V3 while its QTI wrapper needs V4. Keep the existing A16
`vendor.qti.hardware.display.composer3-V1-ndk.so`, which needs standard V3.
The saved baseline SHA is
`d74203762895784143967bc3e6d42a1e57e148aa123ced7b52dfae6320d604d1`.
All five QTI wrapper exports directly required by Neoteric composer exist in
this baseline. No AIDL dependency checks were disabled. Runtime compatibility
still needs a controlled boot test after image validation.

The phone is running Neoteric. No reboot, wipe, flash or device modification
was performed during this overlay preparation.

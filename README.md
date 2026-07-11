# Android device tree for Xiaomi 15 Ultra (xuanyuan)

```
#
# SPDX-FileCopyrightText: The Evolution X Project
# SPDX-License-Identifier: Apache-2.0
#
```

## Device Specifications

| Feature | Specification |
|---|---|
| Codename | xuanyuan |
| Model | Xiaomi 15 Ultra |
| Platform | Snapdragon 8 Elite (SM8750, sun) |
| Architecture | arm64-v8a |
| Screen density | 600 dpi |
| A/B OTA | Yes |
| Boot header | v4 (init_boot) |

## Build instructions

```bash
source build/envsetup.sh
lunch evolution_xuanyuan-userdebug
m evolution_ota_package
```

## Credits

- [The LineageOS Project](https://github.com/LineageOS) — device tree template
- [The Evolution X Project](https://github.com/Evolution-X) — EvoX build system

# Xiaomi 15 Ultra (xuanyuan): stock 303 bring-up

Android 16 Evolution X `bka`, product `lineage_xuanyuan-bp4a-userdebug`.
This is a bring-up snapshot, not a release or a claim that an EvoX build has passed.
Keep OS3.0.303.0.WOAEUXM proprietary inputs and the existing boot images intact.
The xiaomi-8750/android_device_xiaomi_xuanyuan repository is reference-only;
none of its tree is to be copied, cherry-picked or substituted here.

## Verified on the existing device

NFC reading, Wi-Fi boot restoration, fingerprint enrollment/icons, speaker
audio and software A2DP including LDAC were previously tested. Consumer IR
was tested after reboot on 2026-10-15; the user confirmed appliance control.
See `tests/` for evidence and caveats. Camera 200MP saving and palm rejection
are not claimed fixed. These live results do not substitute for testing EvoX.

## Build support

- `build-support/evox-manifest-pinned.xml` records the platform revisions.
- `build-support/platform-patches/` contains preserved compatibility diffs,
  named by project path with `/` replaced by `__`; `.base` records their base.
  Apply each nonempty patch from its corresponding project only after
  `git apply --check` succeeds. Never force-apply to a different revision.
- `build-support/sm8750-common/` snapshots the local common layer expected
  at `device/xiaomi/sm8750-common` (not a replacement from a reference repo).
- `build-support/vendor-config/` snapshots generated vendor build definitions;
  the `.snapshot` suffix prevents them from being discovered as live modules.
  the proprietary vendor tree itself is required separately. This repository
  does not publish all vendor blobs or fully automate their prior fixups.
- The large Camera APK uses Git LFS; run `git lfs pull` after checkout.
- `recovery/adb_keys` is deliberately local-only and optional. Do not publish
  host private keys or bake an unknown host's authorization into a release.

From the ROM root, after preparing the above inputs:

```sh
source build/envsetup.sh
lunch lineage_xuanyuan-bp4a-userdebug
m evolution -j4
```

The saved June 2026 platform security patch override is a retained bring-up
compatibility setting, not a claim of current security coverage. Review it
before any release. Do not flash experimental images without explicit approval.

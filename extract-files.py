#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)
from pathlib import Path

namespace_imports = [
    'device/xiaomi/xuanyuan',
    'hardware/qcom-caf/wlan',
]

vendor_suffix_libs = (
    'android.frameworks.cameraservice.common-V1-ndk',
    'android.frameworks.cameraservice.device-V2-ndk',
    'android.frameworks.cameraservice.service-V2-ndk',
    'audio.bluetooth.default',
    'android.hardware.audio.common-V3-ndk',
    'android.hardware.audio.core-V2-ndk',
    'android.hardware.audio.core.sounddose-V1-ndk',
    'android.hardware.audio.effect-V2-ndk',
    'android.hardware.biometrics.fingerprint-V5-ndk',
    'android.hardware.bluetooth.audio-V4-ndk',
    'android.hardware.bluetooth.audio-impl',
    'android.hardware.bluetooth.audio@2.0-impl',
    'android.hardware.camera.common-V1-ndk',
    'android.hardware.camera.device-V1-ndk',
    'android.hardware.camera.device-V2-ndk',
    'android.hardware.camera.metadata-V1-ndk',
    'android.hardware.camera.metadata-V2-ndk',
    'android.hardware.camera.provider-V2-ndk',
    'android.hardware.drm-service.clearkey',
    'android.hardware.drm-V1-ndk',
    'android.hardware.graphics.allocator-V1-ndk',
    'android.hardware.graphics.allocator-V2-ndk',
    'android.hardware.graphics.common-V5-ndk',
    'android.hardware.health-service.qti',
    'android.hardware.security.sharedsecret-V2-ndk',
    'android.hardware.wifi-service',
    'android.hardware.security.keymint-V3-ndk',
    'android.media.audio.common.types-V2-ndk',
    'android.media.audio.common.types-V3-ndk',
    'android.frameworks.sensorservice-V1-ndk',
    'android.hardware.sensors-V2-ndk',
    'hostapd',
    'libbluetooth_audio_session',
    'libbluetooth_audio_session_aidl',
    'lib_android_keymaster_keymint_utils',
    'libcamera2ndk_vendor',
    'libsensorndkbridge',
    'vendor.xiaomi.hardware.camera.injection-V1-ndk',
    'wpa_supplicant',
)

non_installable_modules = (
    'android.frameworks.cameraservice.common-V1-ndk_vendor',
    'android.frameworks.cameraservice.device-V2-ndk_vendor',
    'android.frameworks.cameraservice.service-V2-ndk_vendor',
    'android.frameworks.sensorservice-V1-ndk_vendor',
    'android.hardware.biometrics.fingerprint-V5-ndk_vendor',
    'android.hardware.bluetooth.audio@2.0-impl_vendor',
    'android.hardware.camera.common-V1-ndk_vendor',
    'android.hardware.camera.device-V1-ndk_vendor',
    'android.hardware.camera.device-V2-ndk_vendor',
    'android.hardware.camera.metadata-V1-ndk_vendor',
    'android.hardware.camera.metadata-V2-ndk_vendor',
    'android.hardware.camera.provider-V2-ndk_vendor',
    'android.hardware.drm-V1-ndk_vendor',
    'android.hardware.drm-service.clearkey_vendor',
    'android.hardware.graphics.allocator-V1-ndk_vendor',
    'android.hardware.graphics.allocator-V2-ndk_vendor',
    'android.hardware.graphics.common-V5-ndk_vendor',
    'android.hardware.health-service.qti_vendor',
    'android.hardware.security.keymint-V3-ndk_vendor',
    'android.hardware.security.sharedsecret-V2-ndk_vendor',
    'android.hardware.sensors-V2-ndk_vendor',
    'android.hardware.wifi-service_vendor',
    'android.hardware.audio.common-V3-ndk_vendor',
    'android.hardware.audio.core-V2-ndk_vendor',
    'android.hardware.audio.core.sounddose-V1-ndk_vendor',
    'android.hardware.audio.effect-V2-ndk_vendor',
    'android.hardware.bluetooth.audio-V4-ndk_vendor',
    'android.hardware.bluetooth.audio-impl_vendor',
    'android.media.audio.common.types-V2-ndk_vendor',
    'android.media.audio.common.types-V3-ndk_vendor',
    'audio.bluetooth.default_vendor',
    'libbluetooth_audio_session_vendor',
    'libbluetooth_audio_session_aidl_vendor',
    'libcamera2ndk_vendor_vendor',
    'libclang_rt.ubsan_standalone-aarch64-android',
    'libprotobuf-cpp-full-21.12',
    'libsensorndkbridge_vendor',
    'vendor.display.config@1.0_vendor',
    'vendor.display.config@1.1_vendor',
    'vendor.display.config@1.2_vendor',
    'vendor.display.config@1.3_vendor',
    'vendor.display.config@1.4_vendor',
    'vendor.display.config@1.5_vendor',
    'vendor.display.config@2.0_vendor',
    'vendor.qti.hardware.perf@2.0_vendor',
    'vendor.qti.hardware.perf@2.1_vendor',
    'vendor.qti.hardware.perf@2.2_vendor',
    'wpa_supplicant_vendor',
)


def move_stock_keymint_utils_to_odm():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    module_marker = '    name: "lib_android_keymaster_keymint_utils_vendor",\n'
    start = contents.find(module_marker)
    if start < 0:
        raise ValueError('Stock KeyMint utils module not found')
    block_start = contents.rfind('cc_prebuilt_library_shared {', 0, start)
    block_end = contents.find('\n}\n', start)
    if block_start < 0 or block_end < 0:
        raise ValueError('Stock KeyMint utils module block is malformed')
    block_end += 3
    block = contents[block_start:block_end]
    marker = '    soc_specific: true,\n'
    if marker not in block:
        raise ValueError('Stock KeyMint utils vendor partition marker not found')
    block = block.replace(marker, '    device_specific: true,\n', 1)
    contents = contents[:block_start] + block + contents[block_end:]
    bp_path.write_text(contents)


def lib_fixup_vendor_suffix(lib: str, partition: str) -> str:
    return f'{lib}_vendor' if partition in ('odm', 'vendor') else lib


def lib_fixup_neoteric_audio_impl(lib: str, partition: str) -> str:
    return 'libaudioserviceexampleimpl-neoteric'


lib_fixups = {
    vendor_suffix_libs: lib_fixup_vendor_suffix,
    ('libaudioserviceexampleimpl',): lib_fixup_neoteric_audio_impl,
}

motion_tuning_xmls = (
    'odm/etc/camera/enhance_motiontuning.xml',
    'odm/etc/camera/motiontuning.xml',
    'odm/etc/camera/snsc_bokeh_motiontuning.xml',
    'odm/etc/camera/snsc_enhance_motiontuning.xml',
    'odm/etc/camera/snsc_motiontuning.xml',
    'odm/etc/camera/snsc_noface_motiontuning.xml',
)

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libtinyxml2.so': blob_fixup()
        .fix_soname(),
    'vendor/lib64/libaudio_aidl_conversion_common_ndk.so': blob_fixup()
        .fix_soname(),
    'vendor/bin/hw/vendor.qti.hardware.display.composer-service': blob_fixup()
        .replace_needed(
            'libtinyxml2.so',
            'libtinyxml2-neoteric.so',
        ),
    'vendor/lib64/libsdmclient.so': blob_fixup()
        .replace_needed(
            'libtinyxml2.so',
            'libtinyxml2-neoteric.so',
        ),
    (
        'vendor/lib64/hw/libaudiocorehal.default.so',
        'vendor/lib64/hw/libaudiocorehal.qti.so',
    ): blob_fixup()
        .replace_needed(
            'libaudioserviceexampleimpl.so',
            'libaudioserviceexampleimpl-neoteric.so',
        ),
    'vendor/lib64/libaudioserviceexampleimpl.so': blob_fixup()
        .fix_soname()
        .add_needed('libaudioutils_shim.so')
        .add_needed('libbluetooth_audio_session_aidl_shim.so'),
    'vendor/lib64/libpowercore.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-neoteric.so'),
    (
        'vendor/bin/poweropt-service',
        'vendor/lib64/hw/libaudioeffecthal.qti.so',
    ): blob_fixup()
        .replace_needed(
            'libtinyxml2.so',
            'libtinyxml2-neoteric.so',
        ),
    (
        'vendor/lib64/soundfx/libdlbvolaidl.so',
        'vendor/lib64/soundfx/libhwdapaidl.so',
        'vendor/lib64/soundfx/libswspatializeraidl.so',
    ): blob_fixup()
        .replace_needed(
            'libstagefright_foundation.so',
            'libstagefright_foundation-v33.so',
        ),
    'vendor/lib64/libar-pal.so': blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-xuanyuan-v34.so')
        .replace_needed('libtinyalsa.so', 'libtinyalsa-v34.so'),
    'vendor/lib64/libaudioroute-v34.so': blob_fixup()
        .replace_needed('libtinyalsa.so', 'libtinyalsa-v34.so')
        .fix_soname(),
    'vendor/lib64/libtinyalsa.so': blob_fixup()
        .fix_soname(),
    'odm/lib64/libaudioroute_ext.so': blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-xuanyuan-v34.so')
        .replace_needed('libtinyalsa.so', 'libtinyalsa-v34.so'),
    'odm/bin/vendor.xiaomi.hardware.mitrustedui-service': blob_fixup()
        .replace_needed(
            'vendor.qti.hardware.systemhelperaidl-V1-ndk.so',
            'vendor.qti.hardware.systemhelperaidl-V1-ndk-xiaomi.so',
        ),
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so': blob_fixup()
        .replace_needed(
            'libprotobuf-cpp-full.so',
            'libprotobuf-cpp-full-21.12.so',
        ),
    'vendor/bin/hw/vendor.xiaomi.hardware.videoservice-service': blob_fixup()
        .add_needed('libgui_consumer_listener_compat.so'),
    'vendor/lib64/vendor.qti.hardware.systemhelperaidl-V1-ndk-xiaomi.so': blob_fixup()
        .fix_soname(),
    motion_tuning_xmls: blob_fixup().regex_replace(
        r'^<\?xml=version=',
        '<?xml version=',
    ),
    'odm/etc/init/vendor.qti.camera.provider-service_64.rc': blob_fixup()
        .regex_replace(
            r'\n    interface vendor\.xiaomi\.hardware\.quickcamera@1\.0::IQuickCameraService default',
            '',
        ),
}

module = ExtractUtilsModule(
    'xuanyuan',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)


def add_system_ext_protobuf_prebuilt():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    module_name = 'libprotobuf-cpp-full-21.12-system_ext'

    if f'name: "{module_name}"' in contents:
        return

    contents += '''

// Stock protobuf ABI required by system_ext vendor HALs.
cc_prebuilt_library_shared {
    name: "libprotobuf-cpp-full-21.12-system_ext",
    stem: "libprotobuf-cpp-full-21.12",
    owner: "xiaomi",
    strip: {
        none: true,
    },
    target: {
        android_arm64: {
            srcs: [
                "proprietary/vendor/lib64/libprotobuf-cpp-full-21.12.so",
            ],
            shared_libs: [
                "libz",
                "liblog",
                "libc++",
                "libc",
                "libm",
                "libdl",
            ],
        },
    },
    compile_multilib: "64",
    prefer: true,
    system_ext_specific: true,
}
'''
    bp_path.write_text(contents)


def add_system_ext_diaghal_prebuilt():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    module_name = 'vendor.qti.diaghal-V1-ndk-system_ext'

    if f'name: "{module_name}"' in contents:
        return

    contents += '''

// Stock diag AIDL runtime required by system_ext diagnostics.
cc_prebuilt_library_shared {
    name: "vendor.qti.diaghal-V1-ndk-system_ext",
    stem: "vendor.qti.diaghal-V1-ndk",
    owner: "xiaomi",
    strip: {
        none: true,
    },
    target: {
        android_arm64: {
            srcs: [
                "proprietary/vendor/lib64/vendor.qti.diaghal-V1-ndk.so",
            ],
            shared_libs: [
                "libbinder_ndk",
                "android.hardware.common-V2-ndk",
                "libc++",
                "libc",
                "libm",
                "libdl",
            ],
        },
    },
    compile_multilib: "64",
    prefer: true,
    system_ext_specific: true,
}
'''
    bp_path.write_text(contents)


def add_stock_audio_effect_overrides():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()

    for module_name in (
        'libdownmixaidl',
        'libdynamicsprocessingaidl',
        'libloudnessenhanceraidl',
        'libreverbaidl',
        'libvisualizeraidl',
    ):
        marker = f'    name: "{module_name}_vendor",\n'
        replacement = f'{marker}    overrides: ["{module_name}"],\n'
        if marker not in contents:
            raise ValueError(f'Module not found in generated Android.bp: {module_name}_vendor')
        contents = contents.replace(marker, replacement, 1)

    bp_path.write_text(contents)


def fix_libpowercore_generated_dependencies():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    module_marker = '    name: "libpowercore",\n'
    start = contents.find(module_marker)
    if start < 0:
        raise ValueError('libpowercore module not found in generated Android.bp')
    block_start = contents.rfind('cc_prebuilt_library_shared {', 0, start)
    block_end = contents.find('\n}\n', start)
    if block_start < 0 or block_end < 0:
        raise ValueError('libpowercore module block is malformed')
    block_end += 3
    block = contents[block_start:block_end]
    old_dep = '                "libtinyxml2",\n'
    new_dep = '                "libtinyxml2-neoteric",\n'
    if new_dep in block:
        return
    if old_dep not in block:
        raise ValueError('libpowercore generated libtinyxml2 dependency not found')
    block = block.replace(old_dep, new_dep, 1)
    contents = contents[:block_start] + block + contents[block_end:]
    bp_path.write_text(contents)


def allow_stock_undefined_symbols():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    for module_name in (
        'libMiVideoFilter',
        'libsigmautils',
        'com.qti.chi.override',
        'libchifeature2',
        'libAncHumanPreviewBokeh',
        'libMiEmojiEffect',
        'libMiPhotoFilter',
        'libTrueSight',
        'libwa_widelens_undistort',
        'libfdmonitor',
    ):
        marker = f'    name: "{module_name}",\n'
        replacement = f'{marker}    allow_undefined_symbols: true,\n'
        if marker not in contents:
            raise ValueError(f'Module not found in generated Android.bp: {module_name}')
        contents = contents.replace(marker, replacement, 1)
    bp_path.write_text(contents)


def disable_stock_elf_checks():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()
    for module_name in (
        'libhta_hexagon_runtime_snpe',
        'libSnpeHtpV79CalculatorStub',
        'libmihapticv1',
        'libvega_common_ecd',
        'libcalculator',
        'libqms_xiaomi',
        'sigma_dut',
    ):
        marker = f'    name: "{module_name}",\n'
        replacement = f'{marker}    check_elf_files: false,\n'
        if marker not in contents:
            raise ValueError(f'Module not found in generated Android.bp: {module_name}')
        contents = contents.replace(marker, replacement, 1)
    bp_path.write_text(contents)


def mark_source_duplicates_non_installable():
    android_root = Path(__file__).resolve().parents[3]
    bp_path = android_root / 'vendor/xiaomi/xuanyuan/Android.bp'
    contents = bp_path.read_text()

    for module_name in non_installable_modules:
        marker = f'    name: "{module_name}",\n'
        replacement = f'{marker}    installable: false,\n'
        if marker not in contents:
            raise ValueError(f'Module not found in generated Android.bp: {module_name}')
        contents = contents.replace(marker, replacement, 1)

    bp_path.write_text(contents)


def remove_non_installable_product_packages():
    android_root = Path(__file__).resolve().parents[3]
    vendor_mk_path = android_root / 'vendor/xiaomi/xuanyuan/xuanyuan-vendor.mk'
    contents = vendor_mk_path.read_text()

    for module_name in non_installable_modules:
        marker = f'    {module_name} \\\n'
        if marker not in contents:
            raise ValueError(
                f'Module not found in generated xuanyuan-vendor.mk: {module_name}'
            )
        contents = contents.replace(marker, '', 1)

    vendor_mk_path.write_text(contents)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
    move_stock_keymint_utils_to_odm()
    add_system_ext_protobuf_prebuilt()
    add_system_ext_diaghal_prebuilt()
    add_stock_audio_effect_overrides()
    fix_libpowercore_generated_dependencies()
    allow_stock_undefined_symbols()
    disable_stock_elf_checks()
    mark_source_duplicates_non_installable()
    remove_non_installable_product_packages()

#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Enable updating of APEXes
$(call inherit-product, $(SRC_TARGET_DIR)/product/updatable_apex.mk)

# A/B
$(call inherit-product, $(SRC_TARGET_DIR)/product/virtual_ab_ota.mk)

PRODUCT_PACKAGES += \
    update_engine \
    update_engine_sideload \
    update_verifier

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_system=true \
    POSTINSTALL_PATH_system=system/bin/otapreopt_script \
    FILESYSTEM_TYPE_system=ext4 \
    POSTINSTALL_OPTIONAL_system=true

AB_OTA_POSTINSTALL_CONFIG += \
    RUN_POSTINSTALL_vendor=true \
    POSTINSTALL_PATH_vendor=bin/checkpoint_gc \
    FILESYSTEM_TYPE_vendor=ext4 \
    POSTINSTALL_OPTIONAL_vendor=true

PRODUCT_PACKAGES += \
    checkpoint_gc \
    otapreopt_script

# API levels
PRODUCT_SHIPPING_API_LEVEL := 35

# Legacy HIDL compatibility
# The stock vendor stack still exposes legacy HIDL HALs even though the
# device launched on API level 35.
PRODUCT_PACKAGES += \
    android.hidl.allocator@1.0-service \
    android.hidl.memory@1.0-impl \
    hwservicemanager

# Core vendor services
# Use the source-built modules here. The similarly named proprietary
# prebuilts are dependency-only variants and are not installable.
PRODUCT_PACKAGES += \
    android.hardware.health-service.qti \
    android.hardware.wifi-service \
    charger \
    wpa_supplicant

# fastbootd
PRODUCT_PACKAGES += \
    android.hardware.fastboot@1.1-impl-mock \
    fastbootd

# Developer GSI AVB keys for first-stage mounts
$(call inherit-product, $(SRC_TARGET_DIR)/product/developer_gsi_keys.mk)

# fastbootd and Qualcomm recovery HALs
PRODUCT_PACKAGES += \
    android.hardware.health-service.qti_recovery \
    fastbootd

# Kernel
PRODUCT_ENABLE_UFFD_GC := true

# Overlays
PRODUCT_ENFORCE_RRO_TARGETS := *

# Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true

# Product characteristics
PRODUCT_CHARACTERISTICS := nosdcard

# VINTF
DEVICE_FRAMEWORK_COMPATIBILITY_MATRIX_FILE += \
    device/xiaomi/xuanyuan/vintf/device_framework_matrix.xml

# Rootdir
PRODUCT_PACKAGES += \
    coresight_reset_source_sink.sh \
    dcc-script-tuna.sh \
    dcc-script.sh \
    dcc_extension.sh \
    flash.sh \
    flash_before.sh \
    init.class_main.sh \
    init.crda.sh \
    init.kernel.extra_free_kbytes.sh \
    init.kernel.init_boot-memory.sh \
    init.kernel.post_boot-kera.sh \
    init.kernel.post_boot-kera_2_3_1.sh \
    init.kernel.post_boot-kera_2_4_0.sh \
    init.kernel.post_boot-kera_3_2_1.sh \
    init.kernel.post_boot-kera_default_3_4_1.sh \
    init.kernel.post_boot-memory.sh \
    init.kernel.post_boot-sun.sh \
    init.kernel.post_boot-sun_5_2.sh \
    init.kernel.post_boot-sun_6_0.sh \
    init.kernel.post_boot-sun_default_6_2.sh \
    init.kernel.post_boot-tuna.sh \
    init.kernel.post_boot-tuna_1_3_2_1.sh \
    init.kernel.post_boot-tuna_2_2_2_1.sh \
    init.kernel.post_boot-tuna_2_3_1_1.sh \
    init.kernel.post_boot-tuna_2_3_2_0.sh \
    init.kernel.post_boot-tuna_default_2_3_2_1.sh \
    init.kernel.post_boot.sh \
    init.mdm.sh \
    init.qcom.class_core.sh \
    init.qcom.coex.sh \
    init.qcom.early_boot.sh \
    init.qcom.efs.sync.sh \
    init.qcom.post_boot.sh \
    init.qcom.sdio.sh \
    init.qcom.sensors.sh \
    init.qcom.sh \
    init.qcom.usb.sh \
    init.qcrild.sh \
    init.qti.display_boot.sh \
    init.qti.kernel.debug-kera.sh \
    init.qti.kernel.debug-sun.sh \
    init.qti.kernel.debug-tuna.sh \
    init.qti.kernel.debug.sh \
    init.qti.kernel.early_debug-kera.sh \
    init.qti.kernel.early_debug-sun.sh \
    init.qti.kernel.early_debug-tuna.sh \
    init.qti.kernel.early_debug.sh \
    init.qti.kernel.sh \
    init.qti.keymaster.sh \
    init.qti.media.sh \
    init.qti.qcv.sh \
    init.qti.write.sh \
    init.qvrd.usb_mtu_set.sh \
    init.xiaomi.modem.sh \
    init.xrcommd.usb_mtu_set.sh \
    qca6234-service.sh \
    system_dlkm_modprobe.sh \
    ufs_ffu.sh \
    vendor.qti.diag.sh \
    vendor_modprobe.sh \

PRODUCT_PACKAGES += \
    fstab.qcom \
    init.batterysecret.rc \
    init.mi_thermald.rc \
    init.qcom.factory.rc \
    init.qcom.rc \
    init.qcom.usb.rc \
    init.qti.kernel.rc \
    init.qti.kernel.target.rc \
    init.qti.ufs.rc \
    init.target.rc \
    init.recovery.hardware.rc \
    init.recovery.qcom.rc \
    miui.factoryreset.rc \

PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/rootdir/etc/fstab.qcom:$(TARGET_COPY_OUT_VENDOR_RAMDISK)/first_stage_ramdisk/fstab.qcom

# Physical firmware partition mount points. These must exist in the read-only
# images before second-stage init runs mount_all.
PRODUCT_PACKAGES += \
    vendor_bt_firmware_mountpoint \
    vendor_dsp_mountpoint \
    vendor_firmware_mnt_mountpoint \
    vendor_modem_firmware_mountpoint \
    product_vm_system_mountpoint

PRODUCT_PACKAGES += \
    libprotobuf-cpp-full-21.12-system_ext

# Soong namespaces
PRODUCT_SOONG_NAMESPACES += \
    $(LOCAL_PATH) \
    hardware/qcom-caf/wlan

# Inherit the proprietary files
$(call inherit-product, vendor/xiaomi/xuanyuan/xuanyuan-vendor.mk)

# Early boot diagnostics
PRODUCT_COPY_FILES += \
    device/xiaomi/xuanyuan/rootdir/system_ext/etc/init/init.xuanyuan.bootdiag.rc:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/init/init.xuanyuan.bootdiag.rc \
    device/xiaomi/xuanyuan/rootdir/system_ext/bin/bootdiag.sh:$(TARGET_COPY_OUT_SYSTEM_EXT)/bin/bootdiag.sh

# Legacy vendor Binder context manager required by stock vendor stack
PRODUCT_PACKAGES += \
    vndservicemanager

# Runtime AIDL library required by the stock KeyMint V3 services.
PRODUCT_PACKAGES += \
    android.hardware.security.keymint-V3-ndk.vendor

# Compatibility libraries required by the stock Android 15 vendor/ODM HALs.
PRODUCT_PACKAGES += \
    android.hardware.camera.provider-V2-ndk.vendor \
    android.hardware.drm-V1-ndk.vendor \
    android.hardware.graphics.allocator-V1-ndk.vendor \
    android.hardware.graphics.common-V5-ndk.vendor \
    android.hardware.sensors-V2-ndk.vendor \
    libcld80211 \
    libprotobuf-cpp-full-21.12-vendorcompat \
    libprotobuf-cpp-lite-21.12-vendorcompat \
    libsensorndkbridge \
    vendor.qti.diaghal-V1-ndk-system_ext \
    vendor.qti.hardware.display.allocator@4.0.vendor

# Stable AIDL compatibility libraries required by the stock Android 15 audio HAL.
PRODUCT_PACKAGES += \
    android.hardware.audio.common-V3-ndk.vendor \
    android.hardware.audio.core-V2-ndk.vendor \
    android.hardware.audio.core.sounddose-V1-ndk.vendor \
    android.hardware.audio.effect-V2-ndk.vendor \
    android.media.audio.common.types-V2-ndk.vendor \
    android.media.audio.common.types-V3-ndk.vendor

# Stock audio service implementation dependencies.
PRODUCT_PACKAGES += \
    android.hardware.bluetooth.audio-V4-ndk.vendor \
    android.hardware.bluetooth.audio-impl \
    libbluetooth_audio_session_aidl \
    libaudioutils_shim \
    libbluetooth_audio_session_aidl_shim \
    libstagefright_foundation-v33

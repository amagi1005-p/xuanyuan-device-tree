#
# SPDX-FileCopyrightText: The Evolution X Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from xuanyuan device
$(call inherit-product, device/xiaomi/xuanyuan/device.mk)

# Evolution X's shared product configuration is installed at vendor/lineage
# by its vendor_evolution manifest project.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

PRODUCT_DEVICE := xuanyuan
PRODUCT_NAME := evolution_xuanyuan
PRODUCT_BRAND := Xiaomi
PRODUCT_MODEL := Xiaomi 15 Ultra
PRODUCT_MANUFACTURER := Xiaomi

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="missi-user 16 BP2A.250605.031.A3 16OS3.1.260423.175212425.QCPEGL.S release-keys" \
    BuildFingerprint=Xiaomi/missi/missi:16/BP2A.250605.031.A3/16OS3.1.260423.175212425.QCPEGL.S:user/release-keys

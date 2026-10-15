"""Check the IR installation contract without changing proprietary binaries."""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DEVICE = ROOT / "device/xiaomi/xuanyuan"


class IrInstallTest(unittest.TestCase):
    def setUp(self):
        text = (DEVICE / "device.mk").read_text()
        self.files = {}
        for src, partition, dst in re.findall(
                r"([^\s:]+):\$\(TARGET_COPY_OUT_(VENDOR|ODM)\)/([^\s\\]+)", text):
            src = src.replace("$(LOCAL_PATH)", "device/xiaomi/xuanyuan")
            self.files[f"{partition.lower()}/{dst}"] = ROOT / src

    def test_feature_is_installed(self):
        src = self.files.get("vendor/etc/permissions/android.hardware.consumerir.xml")
        self.assertIsNotNone(src, "IR feature is not installed")
        self.assertIsNotNone(ET.parse(src).find("./feature[@name='android.hardware.consumerir']"))

    def test_hal_is_declared(self):
        src = self.files.get("vendor/etc/vintf/manifest/android.hardware.ir-service.example.xml")
        self.assertIsNotNone(src, "IR AIDL manifest is not installed")
        hal = ET.parse(src).find("./hal[name='android.hardware.ir']")
        self.assertIsNotNone(hal)
        self.assertEqual(hal.get("format"), "aidl")
        self.assertEqual(hal.findtext("fqname"), "IConsumerIr/default")

    def test_hal_starts_as_system(self):
        src = self.files.get("vendor/etc/init/android.hardware.ir-service.example.rc")
        self.assertIsNotNone(src, "IR init service is not installed")
        lines = [line.strip() for line in src.read_text().splitlines() if line.strip()]
        self.assertIn("service vendor.ir-default /vendor/bin/hw/android.hardware.ir-service.example", lines)
        self.assertIn("class hal", lines)
        self.assertIn("user system", lines)
        self.assertNotIn("disabled", lines)


if __name__ == "__main__":
    unittest.main()

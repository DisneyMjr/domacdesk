import re
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]


class PackagingAssetTests(unittest.TestCase):
    def test_portable_embedded_images_exist(self):
        source = ROOT / "libs/portable/src/ui.rs"
        for asset in re.findall(r'include_bytes!\("([^\"]+)"\)', source.read_text(encoding="utf-8")):
            with self.subTest(asset=asset):
                self.assertTrue((source.parent / asset).is_file())

    def test_appimage_uses_packaged_executable(self):
        for recipe in (ROOT / "appimage").glob("AppImageBuilder-*.yml"):
            with self.subTest(recipe=recipe.name):
                executable = re.search(r'^\s+exec:\s*(\S+)', recipe.read_text(encoding="utf-8"), re.MULTILINE)
                self.assertIsNotNone(executable)
                self.assertEqual(executable.group(1), "usr/share/domacdesk/domacdesk")

    def test_linux_package_icons_exist(self):
        source = (ROOT / "build.py").read_text(encoding="utf-8")
        for name in set(re.findall(r"res/([\w@.-]+\.(?:png|svg))", source)):
            with self.subTest(asset=name):
                self.assertTrue((ROOT / "res" / name).is_file())

    def test_android_adaptive_icons_have_foregrounds(self):
        resources = ROOT / "flutter/android/app/src/main/res"
        for adaptive in (resources / "mipmap-anydpi-v26").glob("*.xml"):
            for layer in ET.parse(adaptive).getroot():
                reference = layer.get("{http://schemas.android.com/apk/res/android}drawable", "")
                if reference.startswith("@mipmap/"):
                    name = reference.split("/", 1)[1]
                    with self.subTest(icon=adaptive.name, layer=layer.tag):
                        self.assertTrue(list(resources.glob(f"mipmap-*/{name}.png")))


if __name__ == "__main__":
    unittest.main()

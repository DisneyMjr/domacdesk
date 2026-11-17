import base64
import hashlib
import json
import re
import unittest
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


ROOT = Path(__file__).resolve().parents[2]


class RustUpdateFixtureTests(unittest.TestCase):
    def test_signed_rust_fixture_matches_domacdesk_release_policy(self):
        source = (ROOT / "src/update_metadata_tests.rs").read_text(encoding="utf-8")
        metadata = re.search(r'let metadata = br#"(.*?)"#;', source).group(1).encode()
        signature = json.loads(re.search(r'let signature = br#"(.*?)"#;', source).group(1))
        key_bytes = re.search(r"public_key: \[\s*(\d.*?)\]", source, re.S).group(1)
        key = Ed25519PublicKey.from_public_bytes(bytes(map(int, re.findall(r"\d+", key_bytes))))
        key.verify(base64.b64decode(signature["signature"], validate=True),
                   b"DomacDesk update metadata v1\n" + metadata)
        document = json.loads(metadata)
        artifact = document["artifacts"][0]
        self.assertEqual(document["app"], "domacdesk")
        self.assertEqual(artifact["size"], len(b"domacdesk"))
        self.assertEqual(artifact["sha256"], hashlib.sha256(b"domacdesk").hexdigest())
        self.assertEqual(artifact["url"],
                         f"https://github.com/DisneyMjr/domacdesk/releases/download/"
                         f"{document['release_id']}/{artifact['file_name']}")

    def test_rust_hash_fixture_matches_payload(self):
        source = (ROOT / "src/update_hash.rs").read_text(encoding="utf-8")
        expected = re.search(r'DOMACDESK_SHA256: &str =\s*"([a-f0-9]+)"', source).group(1)
        self.assertEqual(expected, hashlib.sha256(b"domacdesk").hexdigest())


if __name__ == "__main__":
    unittest.main()

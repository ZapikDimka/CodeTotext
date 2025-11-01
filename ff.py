
import re

HEX = ("7958401743454e1756174552475256435e59501a5c524e176f786517545e475f5245191772195019175e4317445f58425b531743565c521756174443455e595017d5b7ab5f525b5b58174058455b53d5b7aa175659531b17505e41525917435f52175c524e175e4417d5b7ab5c524ed5b7aa1b174f584517435f5217515e454443175b524343524517d5b7ab5fd5b7aa17405e435f17d5b7ab5cd5b7aa1b17435f5259174f584517d5b7ab52d5b7aa17405e435f17d5b7ab52d5b7aa1b17435f525917d5b7ab5bd5b7aa17405e435f17d5b7ab4ed5b7aa1b1756595317435f5259174f58451759524f4317545f564517d5b7ab5bd5b7aa17405e435f17d5b7ab5cd5b7aa175650565e591b17435f525917d5b7ab58d5b7aa17405e435f17d5b7ab52d5b7aa1756595317445817585919176e5842175a564e17424452175659175e5953524f1758511754585e59545e53525954521b177f565a5a5e595017535e4443565954521b177c56445e445c5e17524f565a5e5956435e58591b17444356435e44435e54565b17435244434417584517405f564352415245175a52435f5853174e5842175152525b174058425b5317445f584017435f52175552444317455244425b4319")

ct = bytes.fromhex(HEX)


ALLOWED = set(range(0x20, 0x7F)) | {0x0E}
COMMON  = b" ETAOINSHRDLUetaoinshrdlu"

def english_likeness(bs: bytes) -> int:
    bad = sum(1 for b in bs if b not in ALLOWED)
    spaces = bs.count(0x20)
    letters = sum(bs.count(c) for c in COMMON)
    return letters + spaces*2 - bad*50

best_key, best_score, best_pt = 0, -10**9, None
for k in range(256):
    pt = bytes(b ^ k for b in ct)
    sc = english_likeness(pt)
    if sc > best_score:
        best_key, best_score, best_pt = k, sc, pt


def normalize(bs: bytes) -> bytes:
    out, i = bytearray(), 0
    while i < len(bs):
        b = bs[i]
        if i + 2 < len(bs) and b == 0xC2 and bs[i+1] == 0xA0 and bs[i+2] in (0xBC, 0xBD):
            out.append(0x27); i += 3; continue
        if b == 0x0E: out.append(0x2E)
        elif b in (0x00, 0x0C, 0x0D, 0x19, 0x1A, 0x1B):
            out.append(0x20)
        else:
            out.append(b)
        i += 1
    return bytes(out)

raw = normalize(best_pt)
raw_text = re.sub(r' +', ' ', raw.decode('ascii', errors='ignore')).strip()


print(f"guessed_key = 0x{best_key:02x}  (0x{best_key^0x20:02x} дає те саме, але з іншим регістром)")
print(raw_text)

import re

HEX = ("7958401743454e1756174552475256435e59501a5c524e176f786517545e475f5245191772195019175e4317445f58425b531743565c521756174443455e595017d5b7ab5f525b5b58174058455b53d5b7aa175659531b17505e41525917435f52175c524e175e4417d5b7ab5c524ed5b7aa1b174f584517435f5217515e454443175b524343524517d5b7ab5fd5b7aa17405e435f17d5b7ab5cd5b7aa1b17435f5259174f584517d5b7ab52d5b7aa17405e435f17d5b7ab52d5b7aa1b17435f525917d5b7ab5bd5b7aa17405e435f17d5b7ab4ed5b7aa1b1756595317435f5259174f58451759524f4317545f564517d5b7ab5bd5b7aa17405e435f17d5b7ab5cd5b7aa175650565e591b17435f525917d5b7ab58d5b7aa17405e435f17d5b7ab52d5b7aa1756595317445817585919176e5842175a564e17424452175659175e5953524f1758511754585e59545e53525954521b177f565a5a5e595017535e4443565954521b177c56445e445c5e17524f565a5e5956435e58591b17444356435e44435e54565b17435244434417584517405f564352415245175a52435f5853174e5842175152525b174058425b5317445f584017435f52175552444317455244425b4319")

def decode_hex_xor17_and_normalize(hex_str: str) -> str:
    data = bytes.fromhex(hex_str)
    plain = bytes(b ^ 0x17 for b in data)

    out = bytearray()
    i = 0
    while i < len(plain):
        if i + 2 < len(plain) and plain[i] == 0xC2 and plain[i+1] == 0xA0 and plain[i+2] in (0xBC, 0xBD):
            out.append(0x27)  # '
            i += 3
            continue
        if plain[i] == 0x0E:
            out.append(0x2E)
        elif plain[i] in (0x00, 0x0C, 0x0D, 0x19, 0x1A, 0x1B):
            out.append(0x20)
        else:
            out.append(plain[i])
        i += 1

    text = out.decode('ascii')
    text = re.sub(r' +', ' ', text).strip()
    return text

def postprocess(text: str) -> str:
    return text.swapcase()


if __name__ == "__main__":
    decoded = decode_hex_xor17_and_normalize(HEX)
    final_text = postprocess(decoded)
    print(final_text)

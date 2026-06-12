from __future__ import annotations

import base64
from pathlib import Path
from typing import Dict, Tuple


DMS_MAGIC = bytes([0x80, 0xFE, 0x64, 0x6F, 0x6D, 0x69, 0x73, 0x6F])
DMS_ENC_KEY = bytes([0xAA, 0x55, 0xDE, 0xAD])


def split_published_text(text: str) -> Tuple[str, str]:
    comment_lines = []
    sheet_lines = []
    is_sheet = False
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if "======" in line:
            is_sheet = True
            continue
        if is_sheet:
            sheet_lines.append(line)
        else:
            comment_lines.append(line)
    if not is_sheet:
        return "", text
    return "\r\n".join(comment_lines).strip(), "\r\n".join(sheet_lines).strip()


def is_dms_bytes(data: bytes) -> bool:
    return data.startswith(DMS_MAGIC) and len(data) >= 16


def _decode_utf16le(data: bytes) -> str:
    if len(data) % 2:
        data = data[:-1]
    return data.decode("utf-16le", errors="replace").rstrip("\x00")


def decrypt_dms_bytes(data: bytes) -> Tuple[str, str]:
    if not is_dms_bytes(data):
        raise ValueError("not a Domiso .dms file")
    cipher_key = bytearray(data[8:12])
    plain_len = int.from_bytes(data[12:14], "little")
    cipher_len = int.from_bytes(data[14:16], "little")
    expected = 16 + plain_len + cipher_len
    if len(data) < expected:
        raise ValueError("truncated Domiso .dms file")
    plaintext_bytes = data[16 : 16 + plain_len]
    ciphertext_bytes = bytearray(data[16 + plain_len : expected])
    enc_key = bytearray(DMS_ENC_KEY)
    for index, value in enumerate(plaintext_bytes):
        enc_key[index & 3] ^= value
    for index in range(4):
        cipher_key[index] ^= enc_key[index]
    for index, value in enumerate(ciphertext_bytes):
        ciphertext_bytes[index] = value ^ cipher_key[index & 3]
    return _decode_utf16le(plaintext_bytes), _decode_utf16le(bytes(ciphertext_bytes))


def encrypt_dms_bytes(public_text: str, sheet_text: str, cipher_seed: bytes = b"\x12\x34\x56\x78") -> bytes:
    if len(cipher_seed) != 4:
        raise ValueError("cipher_seed must be exactly 4 bytes")
    plain = public_text.encode("utf-16le")
    cipher = bytearray(sheet_text.encode("utf-16le"))
    if len(plain) > 0xFFFF or len(cipher) > 0xFFFF:
        raise ValueError(".dms sections must be shorter than 65536 bytes")
    enc_key = bytearray(DMS_ENC_KEY)
    for index, value in enumerate(plain):
        enc_key[index & 3] ^= value
    cipher_key = bytearray(cipher_seed)
    for index in range(4):
        cipher_key[index] ^= enc_key[index]
    for index, value in enumerate(cipher):
        cipher[index] = value ^ cipher_key[index & 3]
    header = bytearray(16)
    header[:8] = DMS_MAGIC
    header[8:12] = cipher_seed
    header[12:14] = len(plain).to_bytes(2, "little")
    header[14:16] = len(cipher).to_bytes(2, "little")
    return bytes(header) + plain + bytes(cipher)


def decode_text_bytes(data: bytes, encoding: str = "utf-8") -> str:
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        return data.decode("utf-8-sig", errors="replace")


def sheet_text_from_bytes(data: bytes, encoding: str = "utf-8") -> Tuple[str, Dict[str, object]]:
    if is_dms_bytes(data):
        comment, sheet = decrypt_dms_bytes(data)
        return sheet, {"format": "domiso_dms", "comment": comment}
    text = decode_text_bytes(data, encoding)
    comment, sheet = split_published_text(text)
    source = {"format": "domiso_txt"}
    if comment:
        source["comment"] = comment
        source["publishedSplit"] = True
    return sheet, source


def sheet_text_from_base64(content_base64: str, encoding: str = "utf-8") -> Tuple[str, Dict[str, object]]:
    return sheet_text_from_bytes(base64.b64decode(content_base64), encoding=encoding)


def read_sheet_file(path: str | Path, encoding: str = "utf-8") -> Tuple[str, Dict[str, object]]:
    return sheet_text_from_bytes(Path(path).read_bytes(), encoding=encoding)

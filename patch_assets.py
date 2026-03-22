import sys
import struct

def main():
    if len(sys.argv) != 4:
        print("Usage: patch_assets.py <code.bin> <old_version> <new_version>")
        sys.exit(1)

    code_bin_path = sys.argv[1]
    old_ver_path = sys.argv[2]
    new_ver_path = sys.argv[3]

    with open(code_bin_path, 'rb') as f:
        code_data = f.read()

    # Find the magic string
    magic_str = b'romfs:/game.pbp\x00'
    idx = code_data.find(magic_str)
    if idx == -1:
        magic_str = b'romfs:/game.pbp'
        idx = code_data.find(magic_str)
        if idx == -1:
            print("ERROR: Could not find 'romfs:/game.pbp' in code.bin.")
            sys.exit(1)

    # Calculate memory address
    # Index + 12 = offset of 'p' in 'pbp'
    # Base load address is 0x00100000
    mem_addr = idx + 12 + 0x00100000
    print(f"Patched memory address is 0x{mem_addr:X}")

    with open(old_ver_path, 'rb') as f:
        ver_data = bytearray(f.read())

    if len(ver_data) < 20:
        print("ERROR: version file is too small.")
        sys.exit(1)

    # Patch the memory address at 0x10 (little-endian 32-bit int)
    ver_data[0x10:0x14] = struct.pack('<I', mem_addr)

    with open(new_ver_path, 'wb') as f:
        f.write(ver_data)

    print("Success: Generated patched version file.")

if __name__ == "__main__":
    main()

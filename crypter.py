#!/usr/bin/env pypy3
import base64, sys, random, zlib, argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="program mode, possible values: encrypt, decrypt, enc, dec, e, and d")
parser.add_argument("file", help="file to encrypt/decrypt")
parser.add_argument("cycles", help="encryption complexity", type=int)
parser.add_argument("cipher", help="encryption cipher, or password")
args = parser.parse_args()
e = ["encrypt", "enc", "e"]
d = ["decrypt", "dec", "d"]

methods = {
    "b64": {
        "encode": base64.b64encode,
        "decode": base64.b64decode
    },
    "b32": {
        "encode": base64.b32encode,
        "decode": base64.b32decode
    },
    "b16": {
        "encode": base64.b16encode,
        "decode": base64.b16decode
    },
    "a85": {
        "encode": base64.a85encode,
        "decode": base64.a85decode
    },
    "b85": {
        "encode": base64.b85encode,
        "decode": base64.b85decode
    },
}

random.seed(args.cipher)

if args.mode in e:
    file = open(args.file, "rb")
    file_content = file.read()
    file.close()
    methods_in_use = [random.choice(list(methods)) for _ in range(args.cycles)]
    for method in tqdm(methods_in_use):
        file_content = methods[method]["encode"](file_content)
    sys.stdout.buffer.write(zlib.compress(file_content))

elif args.mode in d:
    file = open(args.file, "rb")
    file_content = file.read()
    file.close()
    file_content = zlib.decompress(file_content)
    methods_in_use = [random.choice(list(methods)) for _ in range(args.cycles)]
    methods_in_use.reverse()
    for method in tqdm(methods_in_use):
        file_content = methods[method]["decode"](file_content)
    sys.stdout.buffer.write(file_content)

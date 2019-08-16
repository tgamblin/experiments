#!/usr/bin/env spack-python

import hashlib
import base64

from llnl.util.tty.colify import colify_table


text = "the quick brown fox jumps over the lazy yellow dog."
algos = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']



def get_hash(algo, text):
    hasher = getattr(hashlib, algo)(text)
    hash_bytes = hasher.digest()

    return (hash_bytes,
            base64.b16encode(hash_bytes).lower(),
            base64.b32encode(hash_bytes).lower(),
            base64.b64encode(hash_bytes))

table = [['', 'BYTES', 'LEN', '16', 'LEN', '32', 'LEN', '64']]

for algo in algos:
    b8, b16, b32, b64 = list(get_hash(algo, text))
    row = [algo, len(b8), len(b16), b16, len(b32), b32, len(b64), b64]
    table.append(row)

colify_table(table)

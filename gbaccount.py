"""
Copyright (c) 2020, John L. Scarfone

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys

def checksum8(name):
   sum = 0

   for c in name.upper():
       sum += ord(c)

   return sum & 0xff

def validation(dollarHigh, dollarLow, iters):
    val = (dollarHigh + dollarLow) & 0xff
    if val == 0:
        val = 1
    if iters == 0:
        iters = 1

    for _ in range(iters):
        tmp = (val << 1) & 0xff
        tmp ^= val
        tmp = (tmp << 1) & 0xff
        tmp ^= val
        tmp = (tmp << 2) & 0xff
        tmp ^= val
        val = (val << 1) & 0xff
        if tmp & 0x80:
            val |= 0x01

    return val

def accountNumber(dollarHigh, val, dollarLow):
    accountBits = dollarHigh << 16 | val << 8 | dollarLow
    account = []
    for _ in range(4):
        second = accountBits & 0x07
        accountBits >>= 3
        first = accountBits & 0x07
        accountBits >>= 3
        account.append(first)
        account.append(second)

    return ''.join(map(str, account))
 
if len(sys.argv) < 3:
    print("Usage: %s <name> <six digit dollar amount>" % sys.argv[0])
    sys.exit(1)

name = sys.argv[1][0:18]
dollarHigh = (int(sys.argv[2][0]) - 0) * 16 + int(sys.argv[2][1]) - 0
dollarLow = (int(sys.argv[2][2]) - 0) * 16 + int(sys.argv[2][3]) - 0

iters = checksum8(name)
val = validation(dollarHigh, dollarLow, iters)
print("account number: " + accountNumber(dollarHigh, val, dollarLow))

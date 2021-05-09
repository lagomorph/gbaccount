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

"""
The account number obfuscation algorithm:
Both the name and the account balance are used to generate the account number.
Account balances are up to six digits. The lowest two digits are not used and
treated as zero. The account number is built from three bytes. Two bytes come
from the four BCD digits of the account balance. The remaining byte is
computed using the account balance and name. Let's call it a check byte.

Computing the check byte:
- Add the high and low byte of the account balance ignoring any overflow. If
the result is zero add one. This will be the initial value of the check byte.
- Perform an eight bit checksum over the (uppercase) name. If the result is
zero add one. This will act as an iteration count for the next step.
- Left shift and xor the current check byte value several times as shown in
validate(). The next value of the check byte will be the current one rotated
left with the low bit rotated in from the high bit of the result of the left
shifts and xors. Repeat this step using the iteration count. The result will
be the final check byte.

The three bytes used to generate the account number are:
<BCD balance high> <check byte> <BCD balance low>

Break these bytes into groups of three bits each. Each group of three bits
will be a digit in the account number. The digits are first grouped into
pairs and then the list of pairs are reversed to give the correct order
in the account number.

An example:
Name: DUCK,DONALD
Account balance: 250700

The eight bit checksum of DUCK,DONALD is 5. This is the iteration count.
The initial check byte is $25 + $07 = $2c
Iterating 5 times we have:
$2c -->
  1: $58
  2: $b0
  3: $61
  4: $c3
  5: $87

So $87 is our check byte

The three bytes used to generate the account number are then:
$25 $87 $07
in binary:                           00100101 10000111 00000111
broken up into groups of three bits: 001 001 011 000 011 100 000 111
as digits:                           1 1 3 0 3 4 0 7
grouped into digit pairs:            11 30 34 07
reversed digit pairs:                07 34 30 11

So the account number is 07343011.
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

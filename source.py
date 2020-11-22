import json

KEY_SPACE = 2**16 - 1

# Open config file containing public signature values
with open('input.json') as f:
    data = json.load(f)

    # Parse all input numbers as long
    g = int(data['g'])
    q = int(data['q'])
    p = int(data['p'])
    s = int(data['s'])
    y = int(data['y'])
    r = int(data['r'])

    # Convert SHA-1 hash to long
    h = int(data['h'], 16)

# Extended Euclidian Algorithm Pseudocode from
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def gcd(a, b):
    s, old_s, r, old_r = 0, 1, b, a
    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q * r)
        (old_s, s) = (s, old_s - q * s)
    return old_r, old_s

def modular_inverse(a, b):
    g, x = gcd(a, b)
    return x % b

# Brute force random nonce k
print("Starting brute force of k...")
for k in range(1, KEY_SPACE):
    if r == pow(g, k, p) % q:
        break
print("Found k")
print("k: " + str(k))

# Using k and modular inverse, find x
x = ((k * s - h) * modular_inverse(r, q)) % q
print("x: " + str(x))

# Verify k and x are valid by replicating s
print("Verifying values...")
s_prime = (modular_inverse(k, q) * (h + x * r)) % q
print("s:  " + str(s))
print("s': " + str(s_prime))
if s == s_prime:
    print("k and x verified")
else:
    print("Verification of k and x failed")

import requests 

""" 
By examining the code, one can see that the keystream value is the same for each block.
In fact, the counter object (ctr) was created with step_up = False and since stup = step_up
it's value is 0. So the increment function will always execute the else statement.
So we can compute the keystream value. indeed, encrypt function return us an encryption of
a png file. Good new, cause the header of a PNG file we can get that and then have the 16 first bytes of the file.
Let's call that bytes X then the first bloc of 16 bytes of the encrypted data is and xor of the keystream and X. Cool
we have keystream now.

Visit the wiki page to know more about PNG files : https://fr.wikipedia.org/wiki/Portable_Network_Graphics
"""
domain = 'https://aes.cryptohack.org/bean_counter/'
url = domain + 'encrypt/'
data = requests.get(url).json()
enc = data['encrypted']

png_head = bytes.fromhex('89504E470D0A1A0A0000000D49484452')

keystream = bytes([a^b for a, b in zip(bytes.fromhex(enc[:32]), png_head)])

# getting the flag
out = []
for i in range(0, len(enc), 32):
    block = enc[i:i+32]
    xored = [a^b for a, b in zip(bytes.fromhex(block), keystream)]
    out.append(bytes(xored).hex())

# write into a png file
with open('bean_counter_flag.png', 'wb') as f:
    f.write(bytes.fromhex(''.join(out)))

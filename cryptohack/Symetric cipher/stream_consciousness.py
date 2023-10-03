import requests
from langdetect import detect

""" 
The remark to make is that the counter value doesn't change.
You can test the function counter.New in your own to notice that.

"""
# we know that the flag starts with crypto{
FLAG_BEGINS = b'crypto{'.hex()

# We are going to get the ciphers of a 100 message and one at least of them (with a great probability)
# is the flag
def collections_of_ciphertext():
    url = 'https://aes.cryptohack.org/stream_consciousness/encrypt/'
    #erase
    tmp = open('stream_consciousness_docs/ciphertext.txt', 'w')
    tmp.close()
    for _ in range(100):
        resp = requests.get(url)
        data = resp.json()
        
        ct = data['ciphertext']
        
        with open('stream_consciousness_docs/ciphertext.txt', 'a') as f:
            f.write(ct)
            f.write('\n')
            f.close()

# @return list of most probable keys and the most probable key to test first !
def getKey():
    with open('stream_consciousness_docs/ciphertext.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    tmp = open('stream_consciousness_docs/plaintext.txt', 'w')
    tmp.close()
    key = ""
    possibles_key = {}
    for line in lines:
        possibly_key = int(FLAG_BEGINS, 16) ^ int(line[:14], 16)
        with open('stream_consciousness_docs/plaintext.txt', 'a') as f:
            f.write("=========== > " + hex(possibly_key)[2:])
            f.write('\n')
            f.close()
        count = 0
        for line in lines:
            pt = hex(possibly_key ^ int(line[:14], 16))[2:]
            try:
                pt = bytes.fromhex(pt)
                if detect(pt.decode()) == 'en':
                    with open('stream_consciousness_docs/plaintext.txt', 'a') as f:
                        f.write("\t" + pt.decode())
                        f.write('\n')
                        f.close()
                    count+=1
            except:
                break
        
        if count >= len(lines)//3:
            possibles_key[count] = hex(possibly_key)

    possibles_key = sorted(possibles_key.items())
    possibles_key.reverse()
    return possibles_key[:5], possibles_key[0][1][2:]

def decrypt(text, key):
    to_dec = text[:len(key)]
    return hex(int(key, 16)^int(to_dec, 16))[2:]

# recovering the whole key. this function will need us to interact.
def get_whole_key():
    # getting the key(s)
    print("Getting the first 7 bytes of the key...")
    keys, key = getKey()
    print("Done !")
    with open('stream_consciousness_docs/ciphertext.txt', 'r') as f:
        lines = f.readlines()
        f.close()
    flag = ''
    msg = "Come on dude let's work as a team to get the flag.\nI have done the most difficult part of the job.\n \
    But now i need some help. I havn't the intelligence to guess the next letter of a phrase or a word but you do.\n \
    HERE IS WHAT YOU CAN DO FOR ME : \n 1. Read the file plaintext.txt\n 2. Find a phrase that you know the nex letter\n \
    3. Tell me which letter you think it is \n 4. There it's cipher just in front of the phrase and you give me that cipher\nEASY NO ! LET'S GO"
    print(msg)
    while '}' not in flag:
        tmp = open('stream_consciousness_docs/plaintext.txt', 'w')
        tmp.close()
        next_letter = ""
        for line in lines:
            phrase = ""
            try:
                phrase = bytes.fromhex(decrypt(line, key)).decode()
            except:
                #print("You may have mess up something dude :-( (IF YOU WANT TO COUNCEL YOUR INPUT CHOSE next letter -2).")
                #print("If sentences are still make sense please continue :) ")
                continue
            if 'crypto{' in phrase:
                    flag = phrase
            with open('stream_consciousness_docs/plaintext.txt', 'a') as f:
                f.write("Phrase : " + phrase + "\t next letter cipher : " + line[len(key):len(key)+2] + "\n")
        
        next_letter = input("Next letter you've guest (guest == -2 to step back | -1 to stop) : ")
        if next_letter != '-1' and next_letter != '-2':
            next_letter_cipher = input("Give it's cipher : ")
            tmp = hex(int(next_letter.encode().hex(), 16)^int(next_letter_cipher, 16))[2:]
            if len(tmp) % 2 == 1:
                tmp = '0'+tmp
            key += tmp
        elif next_letter == '-1':
            break
    
        print("Good : let's continue")
        
        if next_letter =='-2': # step back
            key = key[:len(key)-2]

    return flag
#collections_of_ciphertext()

flag = get_whole_key()
if '}' not in flag:
    print("Flag is not complete : ", flag)
    print("next time we gonna have it, use the characters of the flag that we have recovered at the beginning :)")
else:
    print("flag is : ", flag)

# flag : crypto{???} 
# don't be lazy play with me !
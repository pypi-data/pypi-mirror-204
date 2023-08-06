"In this script you can find all the functions relative to Cryptosystems."
class Ciphers:
    "In this class you can find all the Ciphers."

    def MonoalphabeticCipher():
        "This function generates a cipher using the monoalphabetic encryption"
        import string, random
        elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù"
        cipher = {elements[i]: None for i in range(len(elements))}

        already_sorted = []
        element_sorted = None

        for i in cipher.keys():
            while True:
                sort = random.randint(0, len(elements) -1)
                if sort in already_sorted:
                    continue
                else:
                    break

            already_sorted.append(sort)
            element_sorted = elements[sort]

            cipher[i] = element_sorted

        return cipher


    def CaesarCipher():
        "This functions generate the Caesar Cipher with a random sequence, or if enabled by the user in the script, the original one."
        import string, random
        elements = string.ascii_letters + string.digits + string.punctuation + "àèéìòù"
        cipher = {elements[i]: None for i in range(len(elements))}

        # sequence = 3 # use this for the original Caesar cipher
        sequence = random.randint(0, len(cipher)) # use this for a random Caesar cipher

        modulo = int(len(cipher))
        for i in cipher.keys():
            index = sequence % modulo
            cipher[i] = elements[index]
            sequence += 1

        return cipher
    

class Asymmetric:
    "In this class you can find all the Asymmetric Cryptosystems"
    class RSA:
        "The RSA implementation, including the Creation of the Key, Encryption and Decryption."

        def KeyCreation(p: int, q:int):
            "Given two distinct primes: p and q. Return p,q,N=p*q,e=65537"

            N = p * q

            e = 2**16 + 1

            return p, q, N, e
        
        def Encryption(plaintext:int, e:int, N:int):
            "Given the plaintext converted in an integer, the public encryption exponent (e) and N: product of p and q. Return the plaintext encrypted"

            if not 1 <= plaintext < N:
                return None
            
            ciphertext = pow(plaintext, e, N)

            return ciphertext


        def Decryption(p:int, q:int, e:int, ciphertext:int):
            "Given p and q the prime numbers used for the creation of the key, the public encryption exponent (e) and he ciphertext. Return the ciphertext decrypted."

            from cryptographyComplements.mathFunctions import InverseModuloExtendedEuclideanAlgorithm

            n = (p-1)*(q-1)

            N = p*q

            d = InverseModuloExtendedEuclideanAlgorithm(e, n)

            plaintext = pow(ciphertext, d, N)

            return plaintext
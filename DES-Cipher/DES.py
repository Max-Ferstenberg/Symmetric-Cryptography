
import numpy as np
import os

class DES(object):
    #Split inputs into 64-bit blocks
    def split(self, text):
        return [text[i:i+64] for i in range(0, len(text), 64)]
    
    #Convert text to binary
    def toBinary(self, text):
        return ''.join(format(ord(c), '08b') for c in text)
    
    #Pad text
    def pad(self, text):
        padding_length = 64 - (len(text) % 64)
        padding = [0] * padding_length
        return text + ''.join(map(str, padding))
    
    #Key generation
    def keyGen(self):
        key = np.random.randint(2, size=64)
        key = [key[i] for i in range(len(key)) if (i+1) % 8 != 0]
        return key
    
    #Permutation
    def permute(self, text, table):
        return [text[i-1] for i in table]
    
    #Initial permutation
    def initialPermutation(self, text):
        IPTable = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
        return self.permute(text, IPTable)
    
    #Key expansion
    def keyExpansion(self, key):
        pc1Table = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
        pc2Table = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
        leftKey = key[:len(key)//2]
        rightKey = key[len(key)//2:]
        leftKey = np.roll(leftKey, -1)
        rightKey = np.roll(rightKey, -1)
        key = np.concatenate([leftKey, rightKey])
        return self.permute(key, pc2Table)
    
    #Expansion permutation
    def expansionPermutation(self, rightText):
        EPTable = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
        return self.permute(rightText, EPTable)
    
    #XOR
    def xor(self, text, key):
        return [int(text[i]) ^ int(key[i]) for i in range(len(text))]
    
    #S-Box
    def sbox (self, rightText):
        SBoxTable = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],  
                    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
            
                    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
            
                    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
            
                    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
            
                    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
            
                    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
            
                    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
            
                    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]
        
        sbox = []
        for i in range(8):
            row = int(str(rightText[i*6]) + str(rightText[i*6+5]), 2)
            col = int(''.join([str(rightText[i*6+j]) for j in range(1, 5)]), 2)
            sbox += [int(x) for x in format(SBoxTable[i][row][col], '04b')]
        
        return self.permute(sbox, [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25])
    
    #Feistel
    def feistel(self, rightText, key):
        rightText = self.expansionPermutation(rightText)
        rightText = self.xor(rightText, key)
        rightText = self.sbox(rightText)
        return rightText
    
    #Final permutation
    def finalPermutation(self, text):
        FPTable = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
        return self.permute(text, FPTable)

    #Encryption
    def encrypt(self, text, key):
        text = self.toBinary(text)
        text = self.initialPermutation(text)
        key = self.keyExpansion(key)
        leftText = text[:len(text)//2]
        rightText = text[len(text)//2:]
        for i in range(16):
            temp = rightText
            rightText = self.xor(leftText, self.feistel(rightText, key))
            leftText = temp
            key = np.roll(key, -1)
        text = self.finalPermutation(rightText + leftText)
        return ''.join([str(x) for x in text])
    
def main():
    des = DES()
    filepath = input("Enter the file path: ")
    file = open(filepath, "r")
    plaintext = list(file.read())
    key = des.keyGen()
    print("Key: ", ''.join(map(str, key)))
    binary_plaintext = des.toBinary(''.join(plaintext))
    if len(binary_plaintext) < 64:
        binary_plaintext = des.pad(binary_plaintext)
    ciphertext = des.encrypt(binary_plaintext[:64], key)

    #Write ciphertext to file
    file = open("Symmetric-Cryptography\DES-Cipher\ciphertext.txt", "w")
    file.write(''.join(ciphertext))
    file.close()

if __name__ == "__main__":
    main()
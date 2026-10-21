import pickle
import os
with open("sample.huff", "rb") as f:
    huff_data = pickle.load(f)

ext = huff_data["ext"]
codes = huff_data["codes"]
padding = huff_data["padding"]
data = huff_data["data"]
bits_list = []
for b in data:
    bits_list.append(format(b, '08b'))
bits = "".join(bits_list)
if padding>0:   
    bits = bits[:-padding]
fliped = {}
for i,j in codes.items():
    fliped[j] = i
ok = []
i = 0
j = 0
while j<len(bits):
    if fliped.get(bits[i:j+1]) != None:
        ok.append(fliped[bits[i:j+1]])
        i = j+1
    j+=1
with open("restored" + ext, "wb") as f:
    f.write(bytes(ok))
print(os.path.getsize("sample.txt"), os.path.getsize("restored.txt"))
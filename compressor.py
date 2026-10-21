from collections import Counter
import heapq
import pickle, os
class Node:
    def __init__(self, val, freq, left=None, right=None):
        self.val = val
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq
    

with open("sample.txt", "rb") as f:
    data = f.read()

if not data:
    print("File is empty")
    exit()
a = Counter(data)
b = []
for i,j in a.items():
    c = Node(i,j)
    
    b.append(c)
heapq.heapify(b)
while len(b)>1:
    first = heapq.heappop(b)
    second = heapq.heappop(b)
    new = Node(None,first.freq + second.freq)
    new.left = first
    new.right = second
    heapq.heappush(b,new)
if b:
    root = b[0]
else:
    root = None
ans = {}
def ok(node,abd):
    if node.val != None:
        ans[node.val] = abd
    if node.left:
        ok(node.left,abd+"0")
    if node.right:
        ok(node.right,abd+"1")
    
    return
ok(root,"")
if len(ans) == 1:
    for key in ans:
        ans[key] = "0"
compress = []
for i in data:
    
    t = ans[i]
    compress.append(t)
compressed = "".join(compress)
padding = (8-len(compressed)%8)%8
compressed = compressed + "0"*padding
packed = []
for i in range(0,len(compressed),8):
    r = compressed[i:i+8]
    packed.append(int(r,2))

packed_bytes = bytes(packed)
huff_data = {
    "ext": os.path.splitext("sample.txt")[1],
    "codes": ans,
    "padding": padding,
    "data": packed_bytes
}

with open("sample.huff", "wb") as f:
    pickle.dump(huff_data, f)

original = os.path.getsize("sample.txt")
compressed_size = os.path.getsize("sample.huff")
saved = (1 - compressed_size / original) * 100

print("Original:  ", original, "bytes")
print("Compressed:", compressed_size, "bytes")
print("Saved:     ", round(saved), "%")

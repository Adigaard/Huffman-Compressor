# Huffman Compressor

A lossless file compressor built from scratch in Python using **Huffman coding**.
It shrinks files by giving short bit codes to frequent bytes and longer codes to rare ones, and restores them **byte-for-byte identical**.

## Results

Tested on *Pride and Prejudice* (plain text, from Project Gutenberg):

| File | Size |
|---|---|
| Original (`sample.txt`) | 772,384 bytes (~754 KB) |
| Compressed (`sample.huff`) | 448,353 bytes (~438 KB) |
| Restored (`restored.txt`) | 772,384 bytes, identical to the original ✅ |

That's about **42% smaller**, with no data lost.

## How Huffman coding works

Normally every character takes 8 bits, whether it's common like `e` or rare like `z`.
Huffman coding gives **shorter codes to frequent characters** and **longer codes to rare ones**, so the total number of bits drops.

Example: `aaaabbc`

| Char | Count | Code |
|---|---|---|
| a | 4 | `1` |
| b | 2 | `01` |
| c | 1 | `00` |

- Normal: 7 × 8 = **56 bits**
- Huffman: 4×1 + 2×2 + 1×2 = **10 bits**

**No separators needed:** no code is the start of another code (the *prefix property*), so the decoder always knows where one code ends and the next begins.

## How the compressor works

1. **Read the file in binary mode** (`"rb"`), so it works for any file type: text, PDF, images.
2. **Count byte frequencies** with `collections.Counter`. Every byte is counted, including spaces and newlines.
3. **Build the Huffman tree** with a min-heap (`heapq`):
   - each byte becomes a leaf `Node(val, freq)`
   - repeatedly pop the two smallest nodes, merge them into a parent whose `freq` is their sum, and push the parent back
   - the last node left is the root
   - rare bytes get merged first, so they sit deeper in the tree (long codes); frequent bytes stay near the top (short codes)
4. **Generate codes** by walking the tree recursively: left adds `0`, right adds `1`. The path to each leaf is that byte's code.
5. **Encode** the file by replacing each byte with its code, giving one long bit string.
6. **Pad** the bit string with zeros so its length is a multiple of 8, and remember how many zeros were added.
7. **Pack** every 8 bits into one real byte (`int(chunk, 2)` → `bytes(...)`). This is the step that actually makes the file smaller.
8. **Save** a `.huff` file using `pickle`, containing:
   - the original file extension
   - the codes dictionary
   - the padding count
   - the packed bytes

## How the decompressor works

1. **Load** the `.huff` file with `pickle`.
2. **Unpack** each byte back into 8 bits with `format(b, '08b')`.
3. **Remove the padding** zeros from the end.
4. **Flip the codes dictionary** so codes map back to bytes.
5. **Decode** by reading bits one at a time; as soon as the bits read so far match a code, output that byte and start again.
6. **Write** the restored bytes to `restored` + the original extension.

## Data structures and concepts used

- **Min-heap** (`heapq`) to always pick the two least frequent nodes
- **Binary tree** (custom `Node` class with `__lt__` so nodes compare by frequency)
- **Recursion** to generate codes
- **Hash maps** for frequency counts and code lookup
- **Bit manipulation** to pack bits into bytes and unpack them
- **Binary file handling** and serialization with `pickle`

## Edge cases handled

- **Empty file:** detected up front, nothing to compress
- **Only one unique byte** (e.g. `aaaa`): the tree is a single leaf, so it is given the code `0` manually
- **Zero padding:** handled so no data is cut off when the bits already fit into whole bytes

## Used in my DBMS

This compressor is also used in **my own DBMS, built from scratch**, to compress data before it is stored on disk and decompress it when it is read back.
Since Huffman coding is lossless, stored records come back exactly as they were written, while taking up less storage space.

Check out the DBMS here: 
[NBS-DBMS](https://github.com/Adigaard/NBS-DBMS)

## How to run

1. Put the file you want to compress in the project folder as `sample.txt` (or change the filename in `compressor.py`).
2. Compress:
   ```
   python compressor.py
   ```
   This creates `sample.huff` and prints the original and compressed sizes.
3. Decompress:
   ```
   python decompressor.py
   ```
   This creates `restored.txt`, identical to the original.

No external libraries are needed; everything uses Python's standard library.

## Limitations

- **Already-compressed files** (PDF, JPG, MP3, ZIP) barely shrink and can even grow slightly, because their bytes are already spread out evenly.
- **Very small files** may get bigger, since the codes dictionary is stored alongside the data.
- Only load `.huff` files you created yourself, since `pickle` can run code when loading untrusted files.

## Possible improvements

- Store a compact custom header instead of using `pickle`
- Use canonical Huffman codes (store only code lengths) for a smaller header
- Accept the input filename from the command line
- Combine with LZ77 (like ZIP/gzip's DEFLATE) for much better compression

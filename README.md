# Huffman-Text-Compression-Decompression

## Introduction
* Text files can be compressed and decompressed 
* Implementation of lossless text compression and decompression using Huffman Coding

## Huffman Coding Algorithm
### Compression
* It takes text in the form of string as an input
* Builds frequency map which maps characters present in the text to their number of occurences
* Builds Min Heap based on the frequency of characters
* Generates Huffman Tree by taking top 2 nodes with minimum frequency at a time and add their frequencies and push back into the heap 
* Generate Codes for each characters by traversing huffman tree and taking '0' for left turn and '1' for right turn
* Also a reverse map is created while generating codes
* Writes a binary file by replacing characters of text with their corresponding codes which will be our compressed file
### Decompression
* It considers that reverse map which was generated while making codes for characters
* Replaces valid group of bits which would be present as keys in reverse map
* After replacement a text file will be generated which will be our decompressed file

## Setup
* Operating system should be Ubuntu Linux
* Just download the HuffmanCompressor folder from this repository
* Run an executable file named "HuffmanCompressor" in that folder

## How to use
* Click on "Browse" button to select whichever text file you want to compress
* Click on "Compress" button to compress that file
* One binary file named "file_name.bin" and one pickle file named "file_name.pkl" will be generated
* Sum of sizes of these two files will be smaller than the original file
* Now to decompress put those two files at same location and then select that "file_name.bin" file through browse button
* Finally click on decompress button which will generate "file_name_decompressed.txt"

##Development
* Implemented algorithm in Python
* Build Gui using Tkinter

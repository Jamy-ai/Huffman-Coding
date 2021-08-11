import os
import heapq
import pickle

class HuffmanCoding:
    #constructor
    def __init__(self,path):
        self.path = path
        self.min_heap = []
        self.codes = {}
        self.reverse_mapping = {}

    #heap node class with comparator
    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        #comparators
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq

    #calc frequency of characters in file
    def build_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    #make priority_queue(min heap)
    def build_min_heap(self,frequency):
        for key in frequency:
            node = self.HeapNode(key,frequency[key])
            heapq.heappush(self.min_heap, node)

    #build huffman tree and heap will contain only root node at the end
    def build_huffman_tree(self):
        while(len(self.min_heap)>1):
            node1 = heapq.heappop(self.min_heap)
            node2 = heapq.heappop(self.min_heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.min_heap, merged)

    #traverse tree recursively and generate code
    def make_codes_helper(self,root,current_code):
        if(root==None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    #make codes for characters
    def make_codes(self):
        root = heapq.heappop(self.min_heap)
        self.make_codes_helper(root,"")

    #get encoded string by replacing characters by their codes
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    #pad extra bits if bits-stream is not multiple of 8
    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    #build byte array
    def build_byte_array(self, paded_encoded_text):
        if (len(paded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        byte_array = bytearray()
        for i in range(0, len(paded_encoded_text), 8):
            byte = paded_encoded_text[i:i+8]
            byte_array.append(int(byte, 2))
        return byte_array

    #compress file
    def compress(self):
        file_name, file_extension = os.path.splitext(self.path)
        if (file_extension != ".txt"):
            return f"{file_extension} cannot be compressed...Select '.txt' file to compress"
        output_path = file_name + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.build_frequency_dict(text)

            self.build_min_heap(frequency)
            self.build_huffman_tree()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)

            paded_encoded_text = self.pad_encoded_text(encoded_text)

            byte_array = self.build_byte_array(paded_encoded_text)

            output.write(bytes(byte_array))

        with open(f"{file_name}.pkl","wb") as rev_map_file:
            pickle.dump(self.reverse_mapping, rev_map_file)

        # print("compressed")
        return output_path

    ''' decompression '''

    #remove padding which was given during compression
    def remove_padding(self, bit_string):
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)

        bit_string = bit_string[8:]
        encoded_text = bit_string[:-1*extra_padding]

        return encoded_text

    #decode by replacing codes with original characters
    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    #decompress given file using pickle file which contains reverse mapping
    def decompress(self):
        file_name, file_extension = os.path.splitext(self.path)
        if(file_extension != ".bin"):
            return f"{file_extension} cannot be decompressed...Select '.bin' file to decompress"

        output_path = file_name + "_decompressed" + ".txt"

        with open(f"{file_name}.pkl","rb") as rev_map_file:
            self.reverse_mapping = pickle.load(rev_map_file)

        with open(self.path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while(len(byte)>0):
                byte = ord(byte) #converts byte into integer
                bits = bin(byte)[2:].rjust(8,'0') #converts int to bits...it gives "0b" at starting...append zeroes at starting to round it to 8
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        # print("decompressed")
        return output_path

# if __name__ == '__main__':
#     # path = "/home/jamy/Jamy-ai/huffman/sample.txt"
#     # h = HuffmanCoding(path)
#     # print(h.compress())
#     path = "/home/jamy/Jamy-ai/huffman/sample.bin"
#     h = HuffmanCoding(path)
#     print(h.decompress())
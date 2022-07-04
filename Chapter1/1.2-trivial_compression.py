from sys import getsizeof


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def __str__(self) -> str:
        b = "bytes: {0:b}\n".format(self.bit_string)
        s = "string: {}".format(self.decompress())
        return b + s

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1  # start with sentinel
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # shift left 2 bits
            if nucleotide == "A":
                self.bit_string |= 0b00  # change last 2 bits to 00
            elif nucleotide == "C":
                self.bit_string |= 0b01  # change last 2 bits to 01
            elif nucleotide == "G":
                self.bit_string |= 0b10  # change last 2 bits to 10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError("Invalid Nucleotide: {}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):  # -1 to exclude sentinel
            bits: int = self.bit_string >> i & 0b11  # get just 2 relevant bits
            if bits == 0b00:
                gene += "A"
            elif bits ==  0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError("Invalid bits: {}".format(bits))
        return gene[::-1]  # [::-1] reverses string by slicing backwards


if __name__ == "__main__":
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGAT"
    compressed: CompressedGene = CompressedGene(original)

    print("-> original gene is {} bytes".format(getsizeof(original)))
    print("-> compressed gene is {} bytes".format(getsizeof(compressed.bit_string)))
    print("-> original and decompressed are the same: {}".format(
        original == compressed.decompress()))
    print()
    print(compressed)  # prints decompressed string



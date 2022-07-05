from enum import IntEnum
from typing import Tuple, List


Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]  # type alias for codons
Gene = List[Codon]  # type alias for genes


def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    return gene


def linear_search(gene: Gene, key_codon: Codon):
    for codon in gene:
        if codon == key_codon: return True
    return False


def binary_search(sortedGene: Gene, key_codon: Codon) -> bool:
    low: int = 0
    high: int = len(sortedGene) - 1
    while low <= high:
        mid: int = (low + high) // 2
        if sortedGene[mid] < key_codon:
            low = mid + 1
        elif sortedGene[mid] > key_codon:
            high = mid - 1
        else:
            return True
    return False


if __name__ == "__main__":
    gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"
    my_gene: Gene = string_to_gene(gene_str)
    my_sorted_gene: Gene = sorted(my_gene)

    acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)
    gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)

    print("linear search: {} (should be True)".format(linear_search(my_gene, acg)))
    print("linear search: {} (should be False)".format(linear_search(my_gene, gat)))

    print("binary search: {} (should be True)".format(binary_search(my_sorted_gene, acg)))
    print("binary search: {} (should be False)".format(binary_search(my_sorted_gene, gat)))

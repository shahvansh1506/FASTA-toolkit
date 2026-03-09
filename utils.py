# FASTA Reader
def read_fasta(file):
    sequences = {}
    header = None

    for line in file:
        line = line.decode("utf-8").strip()

        if line.startswith(">"):
            header = line[1:]
            sequences[header] = ""
        else:
            sequences[header] += line.upper()

    return sequences


# GC Content
def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return round((g + c) / len(sequence) * 100, 2)


# DNA → RNA
def transcribe_dna(sequence):
    return sequence.replace("T", "U")


# Reverse Complement
def reverse_complement(sequence):

    complement = {"A":"T","T":"A","G":"C","C":"G"}

    rev = ""
    for base in sequence[::-1]:
        rev += complement.get(base, base)

    return rev


# DNA → Protein
def translate_dna(sequence):

    codon_table = {
        "ATA":"I","ATC":"I","ATT":"I","ATG":"M",
        "ACA":"T","ACC":"T","ACG":"T","ACT":"T",
        "AAC":"N","AAT":"N","AAA":"K","AAG":"K",
        "AGC":"S","AGT":"S","AGA":"R","AGG":"R",

        "CTA":"L","CTC":"L","CTG":"L","CTT":"L",
        "CCA":"P","CCC":"P","CCG":"P","CCT":"P",
        "CAC":"H","CAT":"H","CAA":"Q","CAG":"Q",
        "CGA":"R","CGC":"R","CGG":"R","CGT":"R",

        "GTA":"V","GTC":"V","GTG":"V","GTT":"V",
        "GCA":"A","GCC":"A","GCG":"A","GCT":"A",
        "GAC":"D","GAT":"D","GAA":"E","GAG":"E",
        "GGA":"G","GGC":"G","GGG":"G","GGT":"G",

        "TCA":"S","TCC":"S","TCG":"S","TCT":"S",
        "TTC":"F","TTT":"F","TTA":"L","TTG":"L",
        "TAC":"Y","TAT":"Y","TAA":"*","TAG":"*",
        "TGC":"C","TGT":"C","TGA":"*","TGG":"W"
    }

    protein = ""

    for i in range(0, len(sequence)-2, 3):
        codon = sequence[i:i+3]
        protein += codon_table.get(codon, "X")

    return protein


# Motif Finder
def find_motif(sequence, motif):

    positions = []

    for i in range(len(sequence)-len(motif)+1):
        if sequence[i:i+len(motif)] == motif:
            positions.append(i+1)

    return positions


# ORF Finder
def find_orfs(sequence):

    start = "ATG"
    stop = ["TAA","TAG","TGA"]

    orfs = []

    for i in range(len(sequence)-2):

        if sequence[i:i+3] == start:

            for j in range(i, len(sequence)-2, 3):

                codon = sequence[j:j+3]

                if codon in stop:

                    orfs.append({
                        "start": i+1,
                        "end": j+3,
                        "length": j+3-i
                    })

                    break

    return orfs
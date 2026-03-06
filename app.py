import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Function to read FASTA file
def read_fasta(file):
    sequences = {}
    current_header = None

    for line in file:
        line = line.decode("utf-8").strip()

        if line.startswith(">"):
            current_header = line
            sequences[current_header] = ""
        else:
            if current_header:
                sequences[current_header] += line

    return sequences


# Function to calculate GC content
def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return (g + c) / len(sequence) * 100


# DNA → RNA transcription
def transcribe_dna(sequence):
    return sequence.replace("T", "U")


# Reverse Complement
def reverse_complement(sequence):

    complement = {
        "A":"T",
        "T":"A",
        "G":"C",
        "C":"G"
    }

    rev_comp = ""

    for base in sequence[::-1]:
        rev_comp += complement.get(base, base)

    return rev_comp


# DNA → Protein translation
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


# Streamlit UI
st.title("FASTA Toolkit 🧬")

uploaded_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa"])

if uploaded_file is not None:

    sequences = read_fasta(uploaded_file)

    headers = list(sequences.keys())

    selected_seq = st.selectbox("Choose a sequence", headers)

    seq = sequences[selected_seq]

    st.subheader(selected_seq)

    st.write("Sequence Length:", len(seq))
    st.write("GC Content:", round(gc_content(seq), 2), "%")


    # DNA Tools
    st.subheader("Sequence Tools")


    if st.button("Transcribe DNA → RNA"):
        rna_seq = transcribe_dna(seq)
        st.text(rna_seq)


    if st.button("Translate DNA → Protein"):
        protein = translate_dna(seq)
        st.text(protein)


    if st.button("Reverse Complement"):
        rev = reverse_complement(seq)
        st.text(rev)


    # GC Content Analysis
    st.subheader("GC Content Analysis")

    gc_values = []
    names = []

    for header, sequence in sequences.items():
        gc_values.append(gc_content(sequence))
        names.append(header)


    df = pd.DataFrame({
        "Sequence": names,
        "GC Content": gc_values
    })


    # Histogram
    st.write("### GC Content Distribution")

    fig1 = plt.figure()
    plt.hist(df["GC Content"], bins=10)
    plt.xlabel("GC Content %")
    plt.ylabel("Frequency")

    st.pyplot(fig1)


    # Bar Plot
    st.write("### GC Content per Sequence")

    fig2 = plt.figure()
    plt.bar(names, gc_values)
    plt.xticks(rotation=90)
    plt.ylabel("GC Content %")

    st.pyplot(fig2)


    # Download results
    st.subheader("Download Results")

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download GC Content Data",
        data=csv,
        file_name="gc_content_results.csv",
        mime="text/csv"
    )
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import *

st.title("FASTA Toolkit 🧬")

st.write("Upload a FASTA file or use the example dataset.")

uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta","fa"])

use_example = st.button("Use Example FASTA")

if uploaded_file:

    sequences = read_fasta(uploaded_file)

elif use_example:

    with open("sample.fasta","rb") as f:
        sequences = read_fasta(f)

else:
    st.stop()


headers = list(sequences.keys())

selected = st.selectbox("Select sequence", headers)

seq = sequences[selected]


st.subheader("Sequence Overview")

st.write("Length:", len(seq))
st.write("GC Content:", gc_content(seq), "%")


st.subheader("Sequence Tools")

if st.button("DNA → RNA"):
    st.text(transcribe_dna(seq))

if st.button("Reverse Complement"):
    st.text(reverse_complement(seq))

if st.button("Translate DNA → Protein"):
    st.text(translate_dna(seq))


st.subheader("Motif Finder")

motif = st.text_input("Enter motif (example: ATG)")

if motif:
    pos = find_motif(seq, motif)
    st.write("Positions:", pos)


st.subheader("ORF Finder")

if st.button("Find ORFs"):

    orfs = find_orfs(seq)

    if orfs:
        df = pd.DataFrame(orfs)
        st.dataframe(df)
    else:
        st.write("No ORFs found.")


st.subheader("GC Content Visualization")

names = []
gc_vals = []

for name, sequence in sequences.items():

    names.append(name)
    gc_vals.append(gc_content(sequence))


df = pd.DataFrame({
    "Sequence":names,
    "GC Content":gc_vals
})


fig = plt.figure()

plt.bar(names, gc_vals)

plt.xticks(rotation=90)

plt.ylabel("GC Content %")

st.pyplot(fig)


csv = df.to_csv(index=False)

st.download_button(
    "Download GC Content CSV",
    csv,
    "gc_content.csv"
)


st.subheader("Example FASTA Format")

example = """>Human_gene_example
ATGCGTACGATCGATCGATCGTAGCTAGCTAGCTAGCTAGCTAA

>Mouse_gene_example
ATGCGTATATATCGCGCGCGATATATATCGCGCGCGCTGA
"""

st.code(example)
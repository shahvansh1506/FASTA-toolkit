import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import *

st.set_page_config(page_title="FASTA Toolkit", page_icon="🧬")

st.title("FASTA Toolkit 🧬")
st.write("A simple bioinformatics toolkit for FASTA sequence analysis.")

# SIDEBAR
st.sidebar.header("Input Options")

uploaded_file = st.sidebar.file_uploader("Upload FASTA file", type=["fasta","fa"])

use_example = st.sidebar.button("Use Example FASTA")


# LOAD DATA
if uploaded_file:

    sequences = read_fasta(uploaded_file)

elif use_example:

    with open("sample.fasta","rb") as f:
        sequences = read_fasta(f)

else:
    st.info("Upload a FASTA file or use the example dataset from the sidebar.")
    st.stop()


# SEQUENCE SELECTION
headers = list(sequences.keys())

selected = st.sidebar.selectbox("Select Sequence", headers)

seq = sequences[selected]


# SEQUENCE OVERVIEW
st.header("Sequence Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Sequence Length", len(seq))

with col2:
    st.metric("GC Content (%)", gc_content(seq))


# SEQUENCE TOOLS
st.header("Sequence Tools")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("DNA → RNA"):
        st.code(transcribe_dna(seq))

with col2:
    if st.button("Reverse Complement"):
        st.code(reverse_complement(seq))

with col3:
    if st.button("Translate DNA → Protein"):
        st.code(translate_dna(seq))


# MOTIF FINDER
st.header("Motif Finder 🔎")

motif = st.text_input("Enter motif (example: ATG)")

if motif:

    positions = find_motif(seq, motif)

    if positions:
        st.write("Motif positions:", positions)
    else:
        st.write("Motif not found.")


# ORF FINDER
st.header("ORF Finder 🧬")

if st.button("Find ORFs"):

    orfs = find_orfs(seq)

    if orfs:
        df_orf = pd.DataFrame(orfs)
        st.dataframe(df_orf)
    else:
        st.write("No ORFs found.")


# GC CONTENT VISUALIZATION
st.header("GC Content Visualization")

names = []
gc_vals = []

for name, sequence in sequences.items():

    names.append(name)
    gc_vals.append(gc_content(sequence))

df = pd.DataFrame({
    "Sequence": names,
    "GC Content": gc_vals
})


fig = plt.figure()

plt.bar(names, gc_vals)

plt.xticks(rotation=90)

plt.ylabel("GC Content %")

st.pyplot(fig)


# DOWNLOAD RESULTS
st.header("Download Results")

csv = df.to_csv(index=False)

st.download_button(
    label="Download GC Content CSV",
    data=csv,
    file_name="gc_content.csv"
)


# EXAMPLE FASTA FORMAT
st.header("Example FASTA Format")

example = """>Human_gene_example
ATGCGTACGATCGATCGATCGTAGCTAGCTAGCTAGCTAGCTAA

>Mouse_gene_example
ATGCGTATATATCGCGCGCGATATATATCGCGCGCGCTGA
"""

st.code(example)
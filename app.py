import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils import *

st.title("FASTA Toolkit 🧬")

uploaded_file = st.file_uploader("Upload FASTA file", type=["fasta","fa"])

if uploaded_file:

    sequences = read_fasta(uploaded_file)

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

    motif = st.text_input("Enter motif")

    if motif:
        pos = find_motif(seq, motif)
        st.write("Positions:", pos)


    st.subheader("ORF Finder")

    if st.button("Find ORFs"):

        orfs = find_orfs(seq)

        df = pd.DataFrame(orfs)

        st.dataframe(df)


    st.subheader("GC Content Visualization")

    gc_values = []
    names = []

    for name, sequence in sequences.items():
        names.append(name)
        gc_values.append(gc_content(sequence))

    df = pd.DataFrame({
        "Sequence":names,
        "GC Content":gc_values
    })


    fig = plt.figure()
    plt.bar(names, gc_values)
    plt.xticks(rotation=90)
    plt.ylabel("GC Content %")

    st.pyplot(fig)


    csv = df.to_csv(index=False)

    st.download_button(
        "Download GC Data",
        csv,
        "gc_content.csv"
    )
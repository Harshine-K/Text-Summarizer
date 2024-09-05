import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import streamlit as st

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Streamlit app UI
st.title("Text Summarization App")
st.write("Enter text below to generate a summary:")

# Text input from the user
input_text = st.text_area("Input Text", height=300)

# Text summarization logic
def summarize(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Frequency table
    freqTable = dict()
    for w in words:
        w = w.lower()
        if w in stopWords:
            continue
        if w in freqTable:
            freqTable[w] += 1
        else:
            freqTable[w] = 1

    sentences = sent_tokenize(text)
    svalueTable = dict()

    for s in sentences:
        for word, freq in freqTable.items():
            if word in s.lower():
                if s in svalueTable:
                    svalueTable[s] += freq
                else:
                    svalueTable[s] = freq

    sumValues = 0
    for sentence in svalueTable:
        sumValues += svalueTable[sentence]

    average = int(sumValues / len(svalueTable))
    summary = ''
    for sentence in sentences:
        if (sentence in svalueTable) and (svalueTable[sentence] > (1.2 * average)):
            summary += " " + sentence
    return summary

# Generate summary when the button is clicked
if st.button("Summarize"):
    if input_text:
        summary = summarize(input_text)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.write("Please enter some text for summarization.")
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to summarize text
def summarize_text(text):
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

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
    
    if len(svalueTable) == 0:
        return "No sentences to summarize."
    
    # Calculate the average sentence score
    average = int(sumValues / len(svalueTable))
    
    # Create the summary by selecting sentences with score higher than 1.2 * average
    summary = ''
    for sentence in sentences:
        if (sentence in svalueTable) and (svalueTable[sentence] > (1.2 * average)):
            summary += sentence + " "
    
    return summary if summary else "Summary could not be generated."

# Streamlit app layout
st.title("Text Summarization App")

# Text input
input_text = st.text_area("Enter text to summarize", height=200)

# Button to generate summary
if st.button("Summarize"):
    if input_text.strip() != "":
        summary = summarize_text(input_text)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.error("Please enter some text to summarize.")

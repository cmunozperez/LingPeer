from main import get_peers
import streamlit as st
import subprocess

@st.cache_resource
def download_en_core_web_sm():
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])

# This hides streamlit's info
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# This inserts the link to the github repository
st.markdown('''<div style="text-align: right;">
            <small>
            <a href="https://github.com/cmunozperez/LingPeer">GitHub</a>
            </small>
            ''', unsafe_allow_html=True)
st.write("#")
st.write("#")

# Name of the web app
st.title('LingPeer')

# Description
st.markdown("<i>Get potential reviewers for papers in theoretical linguistics based on data from [Lingbuzz](https://ling.auf.net)</i>", unsafe_allow_html=True)

title = st.text_input("Title")

keywords = st.text_input("Keywords", help='For better results, introduce at least 3 keywords separated by commas or semicolons')

abstract = st.text_area("Abstract", height=50, help='The abstract must have a maximum lenght of 1000 words')

# Button to call the get_peers function
if st.button("Suggest me reviewers!"):
    # Ask to fill the fields if there are no words in them
    if any(char.isalnum() for char in title) == False and any(char.isalnum() for char in keywords) == False and any(char.isalnum() for char in abstract) == False:
        st.write('Please, fill at least one of the fields.')
    # Word limit for the abstract
    elif len(abstract.split()) > 1000:
        st.write('The abstract must have a maximum lenght of 1000 words.')
    else:
        # This runs the function
        peers = get_peers(title, keywords, abstract)
        
        # Message if no results are found
        if len(peers) == 0:
            st.write('The search yielded no results.')
            
        else:
            for name, kw_list, title, ms_id, _ in peers:
                st.divider()
                st.subheader(name)
                if len(kw_list) == 0:
                    st.write('No keywords in common between this author and the info you provided.')  
                else:
                    st.write('This author has employed the following matching keywords.')
                    kw_acum = []
                    for kw in kw_list:
                        kw_bullet = f'- :red[{kw}]'
                        kw_acum.append(kw_bullet)
                    kw_acum = '\n'.join(kw_acum)
                    st.markdown(kw_acum)
    
                url = f'https://ling.auf.net/{ms_id}'
                st.markdown(f'As a reference, you can check their manuscript *[{title}]({url})*.')
                

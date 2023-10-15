from main import get_peers
import streamlit as st

st.title('LingPeer')

st.markdown("<i>Retrieves from [Lingbuzz](https://ling.auf.net) potential reviewers for papers in theoretical linguistics</i>", unsafe_allow_html=True)

title = st.text_input("Title")

keywords = st.text_input("Keywords", help='Introduce between 3 and 12 keywords separated by commas or semicolons')

abstract = st.text_area("Abstract", height=50, help='The abstract must have a length of between 10 and 1000 words')

# Button to call the get_peers function
if st.button("Suggest me reviewers!"):
    if len(abstract.split()) < 10:
        st.write('The abstract should be at least 10 words long.')
    elif len(abstract.split()) > 1000:
        st.write('The abstract should be shorter than 1000 words.')
    else:
        peers = get_peers(title, keywords, abstract)
        for name, kw_list, title, ms_id, _ in peers:
            st.subheader(name)
            if len(kw_list) == 0:
                st.write('No keywords in common between this author and the abstract you provided.')  
            else:
                st.write('The following are keywords in common between this author and the abstract you provided.')
                kw_acum = []
                for kw in kw_list:
                    kw_bullet = f'- :red[{kw}]'
                    kw_acum.append(kw_bullet)
                kw_acum = '\n'.join(kw_acum)
                st.markdown(kw_acum)

            url = f'https://ling.auf.net/{ms_id}'
            st.markdown(f'As a reference, you can check their manuscript [*{title}*]({url}).')
            st.divider()

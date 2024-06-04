import streamlit as st
import pickle
import numpy as np

# Load the necessary data files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Streamlit app
st.title('Book Recommender System')

# Create tabs
tab1, tab2 = st.tabs(["Top 50 Books", "Recommendation Form"])

# Top 50 Books tab
with tab1:
    st.header('Top 50 Books')
    num_cols = 4  # Number of columns per row
    cols = st.columns(num_cols)
    for idx, i in enumerate(range(len(popular_df))):
        col = cols[idx % num_cols]
        with col:
            st.image(popular_df.iloc[i]['Image-URL-M'], width=100)
            st.write(f"**Title**: {popular_df.iloc[i]['Book-Title']}")
            st.write(f"**Author**: {popular_df.iloc[i]['Book-Author']}")
            st.write(f"**Votes**: {popular_df.iloc[i]['num_rating']}")
            st.write(f"**Rating**: {popular_df.iloc[i]['avg_rating']:.1f}")
            st.write("---")

# Recommendation Form tab
with tab2:
    st.header('Recommend Books')
    user_input = st.text_input("Enter a book title:")
    if st.button('Recommend'):
        with st.spinner('Generating recommendations...'):
            if user_input in pt.index:
                index = np.where(pt.index == user_input)[0][0]
                similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

                st.write(f"Books similar to **{user_input}**:")
                cols = st.columns(num_cols)
                for idx, i in enumerate(similar_items):
                    col = cols[idx % num_cols]
                    with col:
                        item = []
                        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

                        st.image(item[2], width=100)
                        st.write(f"**Title**: {item[0]}")
                        st.write(f"**Author**: {item[1]}")
                        st.write("---")
            else:
                st.error("Book not found. Please check the spelling or try another book.")

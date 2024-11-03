import streamlit as st

# Sample product data
products = [
    {
        "name": "Department of Engineering Library",
        "description": "",
        "price": "29.4",
        "image_url": "images/doe.jpg"  # Placeholder image URL
    },
    {
        "name": "University Library",
        "description": "",
        "price": "300",
        "image_url": "images/Main_UL_building.jpg"
    },
    {
        "name": "Squire Law Library",
        "description": "",
        "price": "300",
        "image_url": "images/squirelaw.jpg"
    },
    {
        "name": "CUES Stash",
        "description": "",
        "price": "9999",
        "image_url": "images/cuesstash.png"
    }
]

# Display products in three columns
cols = st.columns(4)

for i, product in enumerate(products):
    with cols[i]:  # Use each column for one product
        st.image(product["image_url"], width=150)
        st.write(f"**{product['name']}**")
        st.write(product["description"])
        st.write(f"Current Share Price: {product['price']}")
        if st.button(f"Purchase {product['name']}"):
            st.write(f"You selected {product['name']} for purchase!")

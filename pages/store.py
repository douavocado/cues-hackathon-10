import streamlit as st

# Sample product data
products = [
    {
        "name": "Product 1",
        "description": "This is the first product.",
        "price": "$10",
        "image_url": "https://via.placeholder.com/150"  # Placeholder image URL
    },
    {
        "name": "Product 2",
        "description": "This is the second product.",
        "price": "$20",
        "image_url": "https://via.placeholder.com/150"
    },
    {
        "name": "Product 3",
        "description": "This is the third product.",
        "price": "$30",
        "image_url": "https://via.placeholder.com/150"
    }
]

# Display products in three columns
cols = st.columns(3)

for i, product in enumerate(products):
    with cols[i]:  # Use each column for one product
        st.image(product["image_url"], width=150)
        st.write(f"**{product['name']}**")
        st.write(product["description"])
        st.write(f"Price: {product['price']}")
        if st.button(f"Purchase {product['name']}"):
            st.write(f"You selected {product['name']} for purchase!")

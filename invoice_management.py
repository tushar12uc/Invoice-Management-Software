import streamlit as st
import pandas as pd
from fpdf import FPDF
import os
import base64

# Streamlit App
st.set_page_config(layout="wide")

# Add custom CSS for background image
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image
set_background_image("background.jpg")

# Add login authentication
def authenticate(username, password):
    return username == "tushar12uc" and password == "mehek2009@#"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''

# Login Page
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("Invoice Management System Login")  # Centered title
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    st.stop()

# Logout Button
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.password = ''

# Rest of the application (only accessible after login)
# Add logout button to sidebar
st.sidebar.title("Menu")
if st.sidebar.button("Logout"):
    logout()
    st.rerun()

# File paths for data storage
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"
INVOICES_FILE = "invoices.csv"

# Load or initialize data
def load_data(file, default_columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=default_columns)

# Save data to CSV
def save_data(df, file):
    df.to_csv(file, index=False)

# Initialize data
customers = load_data(CUSTOMERS_FILE, ["customer_id", "customer_name", "address", "mobile", "email"])
products = load_data(PRODUCTS_FILE, ["product_id", "product_name", "description", "price", "stock"])
invoices = load_data(INVOICES_FILE, ["invoice_id", "customer_id", "product_ids", "quantities", "total_amount", "payment_status"])

# Generate PDF Invoice
def generate_invoice(customer_id, product_ids, quantities, total_amount):
    customer = customers[customers['customer_id'] == customer_id].iloc[0]
    selected_products = products[products['product_id'].isin(product_ids)]

    pdf = FPDF()
    pdf.add_page()

    # Logo
    if os.path.exists("company_logo.png"):
        pdf.image("company_logo.png", x=160, y=8, w=33)

    # Title and Company Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Editors Chamber.", ln=True, align='L')
    pdf.cell(200, 10, txt="Udaipur, India", ln=True, align='L')
    pdf.cell(200, 10, txt="Pincode: 313324", ln=True, align='L')
    pdf.cell(200, 10, txt="Email: tushar@editorschamber.in", ln=True, align='L')
    pdf.ln(10)

    # Customer Details
    pdf.cell(200, 10, txt="Customer Details:-------------", ln=True)
    pdf.cell(200, 10, txt=f"Customer: {customer['customer_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {customer['address']}", ln=True)
    pdf.cell(200, 10, txt=f"Mobile: {customer['mobile']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {customer['email']}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.cell(60, 10, "Product", 1)
    pdf.cell(60, 10, "Description", 1)
    pdf.cell(20, 10, "Qty", 1)
    pdf.cell(30, 10, "Unit Price", 1)
    pdf.cell(30, 10, "Total", 1)
    pdf.ln()

    total = 0
    for i, product in selected_products.iterrows():
        qty = quantities[product_ids.index(product['product_id'])]
        line_total = product['price'] * qty
        total += line_total
        pdf.cell(60, 10, product['product_name'], 1)
        pdf.cell(60, 10, product['description'], 1)
        pdf.cell(20, 10, str(qty), 1)
        pdf.cell(30, 10, f"${product['price']:.2f}", 1)
        pdf.cell(30, 10, f"${line_total:.2f}", 1)
        pdf.ln()

    pdf.cell(170, 10, "", 0)
    pdf.cell(30, 10, f"Total: ${total_amount:.2f}", 1)

    filename = f"invoice_{customer_id}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Sidebar Menu
st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Customer Management", "Product Management", "Invoice Management"]
)

# Home Page
if menu == "Home":
    st.title("Invoice Management System")
    st.write("Welcome to the Invoice Management System!")
    st.write("Use the sidebar to navigate to different sections.")

# Customer Management
elif menu == "Customer Management":
    st.title("Customer Management")
    create_or_manage = st.radio("Choose Action", ["Create", "Manage"])

    if create_or_manage == "Create":
        st.subheader("Add New Customer")
        new_name = st.text_input("Customer Name")
        new_address = st.text_input("Address")
        new_mobile = st.text_input("Mobile")
        new_email = st.text_input("Email")
        add_customer = st.button("Add Customer")

        if add_customer:
            new_id = customers['customer_id'].max() + 1 if not customers.empty else 1
            new_customer = pd.DataFrame([[new_id, new_name, new_address, new_mobile, new_email]],
                                       columns=["customer_id", "customer_name", "address", "mobile", "email"])
            customers = pd.concat([customers, new_customer], ignore_index=True)
            save_data(customers, CUSTOMERS_FILE)
            st.success("Customer added successfully!")

    elif create_or_manage == "Manage":
        st.subheader("Manage Customers")

        # Search Bar
        search_query = st.text_input("Search Customers by Name, Email, or Mobile")
        if search_query:
            filtered_customers = customers[
                (customers['customer_name'].str.contains(search_query, case=False)) |
                (customers['email'].str.contains(search_query, case=False)) |
                (customers['mobile'].str.contains(search_query, case=False))
            ]
            st.dataframe(filtered_customers)
        else:
            st.dataframe(customers)

        # Edit/Delete Customer
        st.subheader("Edit or Delete Customer")
        customer_id_to_edit = st.number_input("Enter Customer ID to Edit/Delete", min_value=1)
        if customer_id_to_edit:
            customer_to_edit = customers[customers['customer_id'] == customer_id_to_edit]
            if not customer_to_edit.empty:
                st.write("Current Details:")
                st.write(customer_to_edit)

                new_name = st.text_input("New Customer Name", value=customer_to_edit.iloc[0]['customer_name'])
                new_address = st.text_input("New Address", value=customer_to_edit.iloc[0]['address'])
                new_mobile = st.text_input("New Mobile", value=customer_to_edit.iloc[0]['mobile'])
                new_email = st.text_input("New Email", value=customer_to_edit.iloc[0]['email'])

                if st.button("Update Customer"):
                    customers.loc[customers['customer_id'] == customer_id_to_edit, 'customer_name'] = new_name
                    customers.loc[customers['customer_id'] == customer_id_to_edit, 'address'] = new_address
                    customers.loc[customers['customer_id'] == customer_id_to_edit, 'mobile'] = new_mobile
                    customers.loc[customers['customer_id'] == customer_id_to_edit, 'email'] = new_email
                    save_data(customers, CUSTOMERS_FILE)
                    st.success("Customer updated successfully!")

                if st.button("Delete Customer"):
                    customers = customers[customers['customer_id'] != customer_id_to_edit]
                    save_data(customers, CUSTOMERS_FILE)
                    st.success("Customer deleted successfully!")
            else:
                st.error("Customer ID not found!")

# Product Management
elif menu == "Product Management":
    st.title("Product Management")
    create_or_manage = st.radio("Choose Action", ["Create", "Manage"])

    if create_or_manage == "Create":
        st.subheader("Add New Product")
        new_product_name = st.text_input("Product Name")
        new_description = st.text_input("Description")
        new_price = st.number_input("Price", min_value=0.0)
        new_stock = st.number_input("Stock Quantity", min_value=0)
        add_product = st.button("Add Product")

        if add_product:
            new_id = products['product_id'].max() + 1 if not products.empty else 101
            new_product = pd.DataFrame([[new_id, new_product_name, new_description, new_price, new_stock]],
                                      columns=["product_id", "product_name", "description", "price", "stock"])
            products = pd.concat([products, new_product], ignore_index=True)
            save_data(products, PRODUCTS_FILE)
            st.success("Product added successfully!")

    elif create_or_manage == "Manage":
        st.subheader("Manage Products")
        st.dataframe(products)

        # Edit/Delete Product
        st.subheader("Edit or Delete Product")
        product_id_to_edit = st.number_input("Enter Product ID to Edit/Delete", min_value=101)
        if product_id_to_edit:
            product_to_edit = products[products['product_id'] == product_id_to_edit]
            if not product_to_edit.empty:
                st.write("Current Details:")
                st.write(product_to_edit)

                new_name = st.text_input("New Product Name", value=product_to_edit.iloc[0]['product_name'])
                new_description = st.text_input("New Description", value=product_to_edit.iloc[0]['description'])
                new_price = st.number_input("New Price", value=product_to_edit.iloc[0]['price'])
                new_stock = st.number_input("New Stock Quantity", value=product_to_edit.iloc[0]['stock'])

                if st.button("Update Product"):
                    products.loc[products['product_id'] == product_id_to_edit, 'product_name'] = new_name
                    products.loc[products['product_id'] == product_id_to_edit, 'description'] = new_description
                    products.loc[products['product_id'] == product_id_to_edit, 'price'] = new_price
                    products.loc[products['product_id'] == product_id_to_edit, 'stock'] = new_stock
                    save_data(products, PRODUCTS_FILE)
                    st.success("Product updated successfully!")

                if st.button("Delete Product"):
                    products = products[products['product_id'] != product_id_to_edit]
                    save_data(products, PRODUCTS_FILE)
                    st.success("Product deleted successfully!")
            else:
                st.error("Product ID not found!")

# Invoice Management
elif menu == "Invoice Management":
    st.title("Invoice Management")
    create_or_manage = st.radio("Choose Action", ["Create", "Manage"])

    if create_or_manage == "Create":
        st.subheader("Create New Invoice")

        # Step 1: Select Customer
        customer_names = customers['customer_name'].tolist()
        selected_customer = st.selectbox("Select Customer", customer_names)
        customer_id = customers[customers['customer_name'] == selected_customer]['customer_id'].values[0]

        # Step 2: Select Products
        product_names = products['product_name'].tolist()
        selected_products = st.multiselect("Select Products", product_names)
        product_ids = products[products['product_name'].isin(selected_products)]['product_id'].tolist()

        # Step 3: Enter Quantities
        quantities = [
            st.number_input(f"Quantity for {product}", min_value=1, value=1)
            for product in selected_products
        ]

        # Step 4: Discounts and Taxes
        discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0)
        tax = st.number_input("Tax (%)", min_value=0.0, max_value=100.0, value=0.0)

        # Step 5: Calculate Total
        subtotal = sum(
            products[products['product_id'] == product_id]['price'].values[0] * qty
            for product_id, qty in zip(product_ids, quantities)
        )
        total_amount = subtotal * (1 - discount / 100) * (1 + tax / 100)

        # Step 6: Payment Status
        payment_status = st.selectbox("Payment Status", ["Paid", "Unpaid", "Partially Paid"])

        # Step 7: Generate Invoice
        if st.button("Generate Invoice"):
            filename = generate_invoice(customer_id, product_ids, quantities, total_amount)
            new_invoice = pd.DataFrame([[len(invoices) + 1, customer_id, product_ids, quantities, total_amount, payment_status]],
                                      columns=["invoice_id", "customer_id", "product_ids", "quantities", "total_amount", "payment_status"])
            invoices = pd.concat([invoices, new_invoice], ignore_index=True)
            save_data(invoices, INVOICES_FILE)
            st.success("Invoice generated successfully!")

            with open(filename, "rb") as f:
                st.download_button(
                    "Download Invoice",
                    data=f,
                    file_name=filename,
                    mime="application/pdf",
                )

    elif create_or_manage == "Manage":
        st.subheader("Manage Invoices")
        st.dataframe(invoices)
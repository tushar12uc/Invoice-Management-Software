import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")


def generate_invoice(customer_id, product_ids, quantities):
	customer = customers[customers['customer_id']==customer_id].iloc[0]
	selected_products =  products[products['product_id'].isin(product_ids)]
	if len(selected_products) != len(quantities):
		st.error("Mismatch between selected products and quantities")
		return None
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font("Arial", 'B', size=30)
	pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
	pdf.image("company_logo.png", x=160, y=25, w=30)
	pdf.set_font("Arial", size=12)
	pdf.cell(200, 10, txt="Editors Chamber.", ln=True)
	pdf.cell(200, 10, txt="Udaipur, India", ln=True)
	pdf.cell(200, 10, txt="Pincode: 313324", ln=True)
	pdf.cell(200, 10, txt="Email: tushar@editorschamber.in", ln=True)
	pdf.cell(200, 10, txt="", ln=True)  # Space
	pdf.set_font("Arial", 'B', size=20)
	pdf.cell(200, 10, txt="Customer Details:-------------", ln=True)
	pdf.cell(200, 10, txt="", ln=True)  # Space
	# Customer Information
	pdf.set_font("Arial", size=12)
	pdf.cell(200, 10, txt=f"Customer: {customer['customer_name']}", ln=True)
	pdf.cell(200, 10, txt=f"Address: {customer['address']}", ln=True)
	pdf.cell(200, 10, txt=f"Mobile: {customer['mobile']}", ln=True)
	pdf.cell(200, 10, txt=f"Email: {customer['email']}", ln=True)
	pdf.cell(200, 10, txt="", ln=True)  # Space
	# Invoice Table Headers:
	pdf.set_font("Arial", 'B', size=12)
	pdf.cell(60, 10, txt="Product", border=1)
	pdf.cell(60, 10, txt="Description", border=1)
	pdf.cell(20, 10, txt="Qty", border=1)
	pdf.cell(30, 10, txt="Unit Price", border=1)
	pdf.cell(30, 10, txt="Total", border=1)
	pdf.ln()
	# Invoice Table Rows:
	total = 0
	pdf.set_font("Arial", size=12)
	for i, product in selected_products.iterrows():
		quantity = quantities[product_ids.index(product['product_id'])]
		line_total = product['price'] * quantity
		total += line_total
		pdf.cell(60, 10, txt=product['product_name'], border=1)
		pdf.cell(60, 10, txt=product['description'], border=1)
		pdf.cell(20, 10, txt=str(quantity), border=1)
		pdf.cell(30, 10, txt=f"${product['price']}", border=1)
		pdf.cell(30, 10, txt=f"${line_total}", border=1)
		pdf.ln()
	pdf.cell(200, 10, txt=" ", ln=True)  # Space
	# Total Amount
	pdf.set_font("Arial", 'B', size=12)
	pdf.cell(170, 10, txt="Total", border=1)
	pdf.cell(30, 10, txt=f"${total}", border=1)
	filename = f"invoice_{customer_id}.pdf"
	pdf.output(filename)
	return filename






st.title("Invoice Management System")
st.sidebar.header("Select Customer and Products")

customer_names = customers["customer_name"].tolist()
selected_customer = st.sidebar.selectbox("Customer", customer_names)
customer_id = customers[customers['customer_name']==selected_customer]['customer_id'].values[0]

product_names = products['product_name'].tolist()
selected_products = st.sidebar.multiselect("Products", product_names)
product_ids = products[products['product_name'].isin(selected_products)]['product_id'].tolist()

quantities = []
for product in selected_products:
	quantity = st.sidebar.number_input(f"Quantity of {product}", min_value=1, max_value=100, value=1)
	quantities.append(quantity)


if st.sidebar.button("Generate Invoice"):
	if len(product_ids) != len(quantities):
		st.error("Mismatch between selected products and quantities")
	else:
		filename = generate_invoice(customer_id, product_ids, quantities)
		if filename:
			with open(filename, 'rb') as f:
				st.download_button(
					label="Download Invoice",
					data=f,
					file_name=filename,
					mime="application/pdf",
                )
			with open(filename, "rb") as f:
				base64_pdf = base64.b64encode(f.read()).decode('utf-8')
			pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
			st.markdown(pdf_display, unsafe_allow_html=True)
st.write(f"*Selected Customer:* {selected_customer}")
st.write("*Selected Products:*")
for i, product in enumerate(selected_products):
	st.write(f"{product} - {quantities[i]} units")
import datetime
from util import generate_hash
from fpdf import FPDF


def generate_pdf(
    property_address: str, property_url: str, image_names: list, requestor: str = "N/A"
):
    """function to generate a pdf file from address and url of the property"""
    pdf_file = f"pdfs/{generate_hash(property_address)}.pdf"

    # create a pdf document
    pdf = FPDF()

    # add a page
    pdf.add_page()

    # set the font and font size
    pdf.set_font("Times", size=24)

    # add a title
    pdf.cell(200, 10, txt="Property Report", ln=1, align="C")
    pdf.set_font("Times", size=12)
    pdf.cell(200, 10, txt="https://t.me/propertyhelperbot", ln=1, align="C")

    # add a line break
    pdf.ln(10)
    pdf.ln(10)

    # body
    # add timestamp
    timestamp = "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now())
    pdf.cell(200, 10, txt="Time: " + timestamp, ln=1, align="L")

    # address
    pdf.cell(200, 10, txt="Address: " + property_address, ln=1, align="L")
    pdf.cell(200, 10, txt="Domain URL: " + property_url, ln=1, align="L")
    pdf.cell(200, 10, txt="Requested By: " + str(requestor), ln=1, align="L")

    # add a line break
    pdf.ln(10)
    pdf.ln(10)

    # add the images, do not let images overlap one another
    for image_name in image_names:
        pdf.image(image_name, x=None, y=None, w=190, h=0, type="", link=property_url)

    # output the pdf file
    pdf.output(pdf_file)

    return pdf_file

from fpdf import FPDF

def generate_summary(memory):
    """
    Generates a PDF summary from stored interactions in memory.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Travel Summary", ln=True, align="C")
    pdf.ln(10)

    # Add memory interactions
    pdf.set_font("Arial", size=12)
    for interaction in memory.get_conversation():
        user_query = interaction["query"]
        ai_response = interaction["response"]
        pdf.multi_cell(0, 10, txt=f"User: {user_query}")
        pdf.ln(1)
        pdf.multi_cell(0, 10, txt=f"STC: {ai_response}")
        pdf.ln(5)

    # Save PDF to bytes
    return pdf.output(dest="S").encode("latin1")
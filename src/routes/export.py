from flask import Blueprint, request, jsonify, Response, render_template, abort
from fpdf import FPDF
from src.models.user import db, Usuario
import os

export_bp = Blueprint("export", __name__)

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

class PDF(FPDF):
    def header(self):
        if os.path.exists(FONT_PATH):
            self.add_font("NotoSansCJK", fname=FONT_PATH)
            self.set_font("NotoSansCJK", size=15)
        else:
            self.set_font("helvetica", "B", 15)
            print(f"AVISO: Fonte NotoSansCJK não encontrada em {FONT_PATH}. Usando Helvetica.")
        self.cell(0, 10, "Resumo Personalizado - Orion Quiz", border=0, ln=1, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        if os.path.exists(FONT_PATH):
            self.set_font("NotoSansCJK", size=8)
        else:
            self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", border=0, align="C")

@export_bp.route("/pdf/<string:access_code>", methods=["GET"])
def export_pdf(access_code):
    if not access_code:
        return jsonify({"error_key": "MISSING_ACCESS_CODE"}), 400

    try:
        user = Usuario.query.filter_by(codigo_acesso=access_code).first()

        if not user or not user.resumo_gerado:
            return jsonify({"error_key": "RESULT_NOT_FOUND"}), 404

        pdf = PDF()
        pdf.add_page()
        
        if os.path.exists(FONT_PATH):
            pdf.add_font("NotoSansCJK", fname=FONT_PATH)
            pdf.set_font("NotoSansCJK", size=12)
        else:
            pdf.set_font("helvetica", size=12)

        pdf.set_font_size(14)
        # Encode nick properly for PDF output if using non-ASCII characters
        # FPDF's default latin-1 might cause issues. Using UTF-8 with add_font is better.
        pdf.cell(0, 10, f"Usuário: {user.nick}", ln=1)
        pdf.set_font_size(12)
        pdf.ln(5)
        
        # Use multi_cell which handles line breaks
        pdf.multi_cell(0, 10, user.resumo_gerado)

        # Output as bytes string, FPDF handles encoding based on font setup
        pdf_output = pdf.output(dest="S") 

        return Response(
            pdf_output,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment;filename=orion_summary_{user.nick}_{access_code}.pdf"}
        )

    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        import traceback
        traceback.print_exc()
        # Return error key
        return jsonify({"error_key": "PDF_GENERATION_FAILED"}), 500

# Removed TODO for share link, will handle in main.py and script.js


from odoo import models, fields, api
import base64
from pdfminer.high_level import extract_text
import io
import logging

logger = logging.getLogger(__name__)


class PdfScreening(models.Model):
    _name = 'pdf.screening'
    _description = 'PDF Screening'

    name = fields.Char(string='Name')
    date = fields.Date(string='Date')
    description = fields.Text(string='Description')
    pdf_file = fields.Binary(string='PDF File')
    extracted_text = fields.Text(string='Extracted Text', readonly=True)
    document_id = fields.Many2one('ir.attachment', string='PDF Document')

    @api.onchange('pdf_file')
    def _onchange_pdf_file(self):
        if self.pdf_file:
            self.extract_text()

    def extract_text(self):
        pdf_data = self.pdf_file
        if pdf_data:
            try:
                # Extract text from PDF data
                pdf_text = extract_text(io.BytesIO(base64.b64decode(pdf_data)))
                # Create a document with extracted text
                self.extracted_text = pdf_text  # Update extracted_text field
            except Exception as e:
                pdf_text = "Error extracting text from PDF: {}".format(str(e))
                self.extracted_text = pdf_text

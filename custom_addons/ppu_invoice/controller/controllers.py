from odoo import http
from odoo.http import request

class PpuInvoiceController(http.Controller):

    @http.route('/ppu_invoice/action_generate', type='http', auth='user')
    def action_generate(self, **kw):
        # Your generate logic here
        # For example, you can perform some actions or generate some data
        # when the "Generate" button is clicked
        pass

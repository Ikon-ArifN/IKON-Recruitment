from odoo import http
from odoo.http import request


class RootTestEndpoint(http.Controller):

    @http.route('/api/test', type='http', auth='public', csrf=False)
    def api_test(self, **kwargs):
        return 'Hello test'

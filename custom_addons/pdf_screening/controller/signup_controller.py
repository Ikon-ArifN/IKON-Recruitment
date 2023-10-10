from odoo import http
from odoo.addons.graphql_base import GraphQLControllerMixin

from ..schema.signup_schema import SignupSchema

class signupController(http.Controller, GraphQLControllerMixin):

    @http.route('/graphiql/signup', auth='public', csrf=False)
    def graphiql_page(self, **kwargs):
        return self._handle_graphiql_request(SignupSchema.grapihql_schema)

    @http.route('/graphql/signup', type='http', auth='public', csrf=False)
    def graphql_endpoint(self, **kwargs):
        return self._handle_graphql_request(SignupSchema.graphql_schema)
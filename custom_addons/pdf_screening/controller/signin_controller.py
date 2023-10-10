

from odoo import http

from odoo.addons.graphql_base import GraphQLControllerMixin
from ..schema.signin_schema import SigninSchema


class signinController(http.Controller, GraphQLControllerMixin):

    @http.route("/graphiql/signin", auth="public")
    def graphiql_page(self, **kwargs):
        return self._handle_graphiql_request(SigninSchema.graphql_schema)

    @http.route("/graphql/signin", type='http', auth='public', methods=['POST'], csrf=False)
    def graphql_endpoint(self, **kwargs):
        return self._handle_graphql_request(SigninSchema.graphql_schema)

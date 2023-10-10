import graphene
from odoo import http
from graphql import GraphQLError
from werkzeug.security import check_password_hash

class Partner(graphene.ObjectType):
    name = graphene.String()
    email = graphene.String()

class Session(graphene.ObjectType):
    session_id = graphene.String()
    user_id = graphene.String()
    username = graphene.String()
    partner_id = graphene.ID()
    partner = graphene.Field(Partner)
    login = graphene.String()

class Signin(graphene.Mutation):
    class Arguments:
        db = graphene.String(required=True)
        login = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = Session

    @staticmethod
    def mutate(self, info, db, login, password):
        print(f"Received login attempt: {login}, Password: {password}")
        with http.request.env.cr.savepoint():
            user = http.request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            if user:
                hashedP = user.password
                print(user)
                print(f"Password dari user: {user.password}")

                # cek = check_password_hash(hashedP, password)
                # if cek:
                uid = http.request.session.authenticate(db, login, password)
                print("UID: ", uid)
                if uid:
                    http.request.session.dbname = db
                    http.request.session.uid = uid
                    http.request.session.login = login
                    user_id = user.id
                    partner_id = user.partner_id.id
                    session = Session(
                        session_id=http.request.session.sid,
                        user_id=user_id,
                        partner_id=partner_id,
                        username=None if user.name == False else user.name,
                        login=user.login,
                    )
                    partner = user.partner_id
                    session.partner = Partner(
                        name=None if partner.name == False else partner.name,
                        email=None if partner.email == False else partner.email,
                    )
                    return session
                # else:
                #     # Incorrect password, raise an error
                #     raise GraphQLError("Invalid password", extensions={"statusCode": 401})
            else:
                raise GraphQLError("Invalid login or password", extensions={"statusCode": 401})

class Query(graphene.ObjectType):
    session = graphene.Field(Session)

    def resolve_session(self, info):
        if http.request.session and http.request.session.sid:
            session_id = http.request.session.sid
            user = http.request.env.user
            partner = user.partner_id
            return Session(
                session_id=session_id,
                username=user.name,
                login=user.login,
                partner=Partner(
                    name=None if partner.name == False else partner.name,
                    email=None if partner.email == False else partner.email,
                )
            )
        else:
            raise GraphQLError("No active session")


class Mutation(graphene.ObjectType):
    signin = Signin.Field()

SigninSchema = graphene.Schema(query=Query, mutation=Mutation)

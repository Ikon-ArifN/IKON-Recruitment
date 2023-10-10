import graphene
from graphene import Mutation, String, Boolean, Int
# from werkzeug.security import check_password_hash, generate_password_hash


class Signup(Mutation):

    class Arguments:
        name = String(required=True)
        login = String(required=True)
        email = String(required=True)
        password = String(required=True)

    success = Boolean()
    message = String()
    # pss = String()

    @staticmethod
    def mutate(root, info, name, email, login, password):
        try:
            env = info.context["env"]
            User = env["res.users"]
            Partner = env["res.partner"]

            partner_vals = {
                "name": name,
                "email": email,
            }

            partner = Partner.create(partner_vals)
            # hashedp = generate_password_hash(password)

            vals = {
                "partner_id": partner.id,
                "name": name,
                "email": email,
                "login": login,
                "password": password,
                "active": True,
            }

            new_user = User.create(vals)
            # print(hashedp)
            # print("From Vals: ", vals[4])
            print("From new_user: ", new_user.password)

            success = True
            message = "Signup successful"
            # pss = password
            new_user

        except Exception as e:
            success = False
            message = str(e)

        return Signup(success=success, message=message)


class Mutation(graphene.ObjectType):
    signup = Signup.Field()


class Query(graphene.ObjectType):
    hello = String()

    @staticmethod
    def resolve_hello(root, info):
        return "Hello, World!"


SignupSchema = graphene.Schema(query=Query, mutation=Mutation)


# src/application/mappers/customer_mapper.py
# For now, our domain Customer and GraphQL CustomerType are very similar.
# If they diverge, this mapper will be crucial.
# We'll define the GraphQL types first, then come back if complex mapping is needed.
# For now, this file can be minimal or skipped if direct mapping is obvious.
# Let's create it with a placeholder or a simple function.

from src.domain.entities import Customer as DomainCustomer
# We will define GQLCustomer in types.py, this is a forward reference.
# from src.interfaces.graphql_resolvers.types import Customer as GQLCustomer

# def to_gql_customer(customer: DomainCustomer) -> GQLCustomer:
#     return GQLCustomer(id=customer.id, name=customer.name, email=customer.email)

# def to_domain_customer_input(name: str, email: str) -> dict: # Or a specific input type
#     return {"name": name, "email": email}
pass # Will define more concretely after GQL types

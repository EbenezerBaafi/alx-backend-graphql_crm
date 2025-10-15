import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    """
    Main Query class that combines all app-level queries.
    Inherits from CRMQuery to include all CRM-related queries.
    """
    # You can add additional project-level queries here if needed
    pass


class Mutation(CRMMutation, graphene.ObjectType):
    """
    Main Mutation class that combines all app-level mutations.
    Inherits from CRMMutation to include all CRM-related mutations.
    """
    # You can add additional project-level mutations here if needed
    pass


# Create the main schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
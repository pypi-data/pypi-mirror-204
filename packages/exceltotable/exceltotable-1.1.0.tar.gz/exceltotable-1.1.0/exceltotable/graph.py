from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from kiota_authentication_azure.azure_identity_authentication_provider import (
    AzureIdentityAuthenticationProvider
)
from msgraph import GraphRequestAdapter, GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    adapter: GraphRequestAdapter
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['4bc98752-e567-4dcc-92e1-734810079c42']
        tenant_id = self.settings['0c5638da-d686-4d6a-8df4-e0552c70cb17']
        client_secret = self.settings['Eky8Q~osWrRPh9On.PltGteQP9pU8Qmsk1NhhaI2']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        auth_provider = AzureIdentityAuthenticationProvider(self.client_credential) # type: ignore
        self.adapter = GraphRequestAdapter(auth_provider)
        self.app_client = GraphServiceClient(self.adapter)


async def get_app_only_token(self):
    graph_scope = 'https://graph.microsoft.com/.default'
    access_token = await self.client_credential.get_token(graph_scope)
    return access_token.token

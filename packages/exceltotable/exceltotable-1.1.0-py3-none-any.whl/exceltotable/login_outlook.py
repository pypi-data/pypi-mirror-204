import asyncio
from azure.identity.aio import ClientSecretCredential
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from msgraph import GraphRequestAdapter
from msgraph import GraphServiceClient
from microsoftgraph.client import Client
client = Client('4bc98752-e567-4dcc-92e1-734810079c42', 'Eky8Q~osWrRPh9On.PltGteQP9pU8Qmsk1NhhaI2', account_type='common') # by default common, thus account_type is optional parameter.
credential = ClientSecretCredential(
  #tenantid
   '0c5638da-d686-4d6a-8df4-e0552c70cb17',
    #'client_id',
     '4bc98752-e567-4dcc-92e1-734810079c42',    
 #'client_secret'
'Eky8Q~osWrRPh9On.PltGteQP9pU8Qmsk1NhhaI2'
)
scopes = ['User.Read', 'Mail.Read']
auth_provider = AzureIdentityAuthenticationProvider(credential, scopes=scopes)
request_adapter = GraphRequestAdapter(auth_provider)
client = GraphServiceClient(request_adapter)

async def me():
    me = await client.me.get()
    print(me.display_name)

asyncio.run(me())

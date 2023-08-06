from azure.storage.blob import  BlobClient
from azure.storage.blob import ContainerClient

class SasTokenBased:
    def __init__(self, account_url, sas_token, blob_container_name):
        self.account_url = account_url
        self.sas_token = sas_token
        self.blob_container_name = blob_container_name
        
        container_client = self.get_container_client()
        self.container_client = container_client

    def get_blob_client_with_sas_url(self,blob_name):
        sas_url = f"{self.account_url}/{self.blob_container_name}/{blob_name}{self.sas_token}"
        blob_client = BlobClient.from_blob_url(sas_url)
        return blob_client

    def read_from_blob_with_sas_url(self,blob_name):
        blob_client = self.get_blob_client_with_sas_url(blob_name)
        xml_string = blob_client.download_blob().readall()
        return xml_string

    def save_to_local(self, byte_data, local_filename):
        with open(f'{local_filename}', 'wb') as f:
            f.write(byte_data)
        print(f"Written to {local_filename}")
    
    def read_from_local(self,local_filename):
        with open(f'{local_filename}', 'rb') as f:
            byte_content = f.read()
        return byte_content
    
    def upload_to_blob_with_sas_url(self,blob_name,byte_data):
        blob_client = self.get_blob_client_with_sas_url(blob_name)
        blob_client.upload_blob(byte_data,overwrite=True)
        print("Uploaded the blob",blob_name)
    
    def get_container_client(self):
        sas_url = f"{self.account_url}/{self.blob_container_name}{self.sas_token}"
        container_client = ContainerClient.from_container_url(sas_url)
        return container_client

    def list_files_in_blob_with_sas_url(self,blob_folder_name):
        file_ls =  [file['name'] for file in list(self.container_client.list_blobs(name_starts_with=blob_folder_name))]
        return file_ls

    def delete_blob(self,blob_name): 
        blob_client = self.get_blob_client_with_sas_url(blob_name)  
        blob_client.delete_blob(delete_snapshots="include")
        print(f"Deleted {blob_name}")


# blob_container_name = "formrecog"
# blob_name = "Acord 125 2016 03 Training Files"
# account_url = "https://bdaildevarchivestorage.blob.core.windows.net"
# sas_token = "?sp=rwl&st=2023-03-07T11:15:52Z&se=2024-03-07T19:15:52Z&spr=https&sv=2021-06-08&sr=c&sig=iihQxNMetGN3P6xPA1EX2nfRvyQ3gRezD0KPCLa8YW0%3D"
# sas_token_based = SasTokenBased(account_url,sas_token,blob_container_name)

# blob_folder_name = "Acord 125 2016 03 Training Files"
# file_ls = sas_token_based.list_files_in_blob_with_sas_url(blob_folder_name)

# blob_name = "Acord 125 2016 03 Training Files/ACORD 0125 2016-03 Acroformsample1_page1.png"
# local_filename = "dummy.png"
# byte_data = sas_token_based.read_from_blob_with_sas_url(blob_name)
# sas_token_based.save_to_local(byte_data, local_filename)

# blob_name = "Acord 125 2016 03 Training Files/dummy.png"
# byte_data = sas_token_based.read_from_local(local_filename)
# sas_token_based.upload_to_blob_with_sas_url(blob_name,byte_data)

# sas_token_based.delete_blob(blob_name)
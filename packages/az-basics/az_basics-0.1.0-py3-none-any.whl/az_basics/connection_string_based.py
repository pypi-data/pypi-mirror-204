from azure.storage.blob import BlobServiceClient, BlobClient
import os

class ConnectionStringBased:
    def __init__(self,connection_string,container_name):
        self.connection_string = connection_string
        self.container_name = container_name
        
        container_client = self.get_clients_with_connection_string()
        self.container_client = container_client
    
    def get_clients_with_connection_string(self):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(self.container_name)
        return container_client

    def read_from_blob(self,file_path):
        blob_client = self.container_client.get_blob_client(file_path)
        byte_data = blob_client.download_blob().readall()
        return byte_data
    
    def save_to_local(self, byte_data, local_filename):
        with open(f'{local_filename}', 'wb') as f:
            f.write(byte_data)
        print(f"Written to {local_filename}")
    
    def read_from_local(self,local_filename):
        with open(f'{local_filename}', 'rb') as f:
            byte_content = f.read()
        return byte_content
    
    def list_files_in_blob(self, blob_folder_name):
        file_ls =  [file['name'] for file in list(self.container_client.list_blobs(name_starts_with=blob_folder_name))]
        return file_ls
    
    def upload_to_blob_with_connection_string(self, local_filename, blob_name):
        blob = BlobClient.from_connection_string(self.connection_string, container_name=self.container_name, blob_name=blob_name)
        with open(local_filename, "rb") as data:
            blob.upload_blob(data,overwrite=True)
        print(f"Uploaded {blob_name}")

    def delete_blob(self,blob_name):
        blob = BlobClient.from_connection_string(self.connection_string, container_name = self.container_name, blob_name=blob_name)
        blob.delete_blob(delete_snapshots="include")
        print(f"Deleted {blob_name}")
    
    def create_recursive_backup(self,blob_folder_name):
        ls = self.list_files_in_blob(blob_folder_name)
        for file in ls:
            if '/'.join(file.split("/")[:len(blob_folder_name.split("/"))]) == blob_folder_name:
                folder_name = '/'.join(file.split("/")[:-1])
                if os.path.exists(folder_name) == False:
                    os.makedirs(folder_name)
                byte_file = self.read_from_blob(file)
                self.save_to_local(byte_file, file)
                print('Saved',file)
    
    def perform_recursive_deletion(self,blob_folder_name):
        for file in self.list_files_in_blob(blob_folder_name):
            self.delete_blob(file)
            

# connection_string = 'DefaultEndpointsProtocol=https;AccountName=bddcsdevstorage;AccountKey=SudkpHTRR930XP4TDxVhjhehDVzY+E/tocDtg7iUIPFoNFdEo7t1TtqVClU9BPvWBPg2CMUtuRzsUeJpwqGgWg=='
# container_name = 'dcs-form-images'
# file_path = "0005a191-e8f6-4b29-bc5c-e5585f8cc054/Loss Run - Aspen - 18-19 (12 28 2022).pdf/image_1.png"
# connection_string_based = ConnectionStringBased(connection_string,container_name)
# byte_data = connection_string_based.read_from_blob(file_path)
# local_filename = "image_1.png"
# connection_string_based.save_to_local(byte_data,local_filename)
# byte_data = connection_string_based.read_from_local(local_filename)
# blob_folder_name = "0005a191-e8f6-4b29-bc5c-e5585f8cc054/Loss Run - Aspen - 18-19 (12 28 2022).pdf"
# file_ls = connection_string_based.list_files_in_blob(blob_folder_name)
# blob_name = "dummy/image_1.png"
# connection_string_based.upload_to_blob_with_connection_string(local_filename, blob_name)
# connection_string_based.delete_blob(blob_name)
# blob_folder_name = "my_dummy"
# connection_string_based.perform_recursive_deletion(blob_folder_name)
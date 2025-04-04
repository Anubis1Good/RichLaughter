import os
import dropbox
from utils.settings import settings

class AgentSmith:
    def __init__(self,local_file):
        """local_file = '1_1_test_MOEX_FUT.json'
        """
        self.dbx = self.get_dropbox_client()
        self.folder_picks = './Screening/strat_picks'
        if not os.path.exists(self.folder_picks):
            os.makedirs(self.folder_picks)
        self.local_path_u = os.path.join(self.folder_picks,local_file)
        prefix_file = 'u'+local_file
        self.local_path_d = os.path.join(self.folder_picks,prefix_file)
        self.remote_file_path = '/MTA_SKYNET/'+prefix_file

    def get_dropbox_client(self):
        try:
            dbx = dropbox.Dropbox(
                oauth2_refresh_token=settings.dropbox_refresh,
                app_key=settings.dropbox_key,
                app_secret=settings.dropbox_secret,
            )
            print("Успешное подключение к Dropbox!")
            return dbx
        except Exception as e:
            print("Ошибка подключения:", e)
            return None
        
    def upload(self):
        try:
            mode = dropbox.files.WriteMode.overwrite
            with open(self.local_path_u, 'rb') as file:
                self.dbx.files_upload(file.read(), self.remote_file_path,mode=mode)
        except dropbox.exceptions.AuthError as e:
            self.get_dropbox_client()
        except dropbox.exceptions.ApiError as e:
            print(f"Произошла ошибка при загрузке файла: {e}")
    
    def upload_all(self):
        mode = dropbox.files.WriteMode.overwrite
        try:
            files = os.listdir('Screening/strat_picks')
            for file in files:
                if not file.startswith('u'):
                    file_path = os.path.join('Screening/strat_picks',file)
                    with open(file_path, 'rb') as f:
                        self.dbx.files_upload(f.read(), '/MTA_SKYNET/u'+file,mode=mode)
        except dropbox.exceptions.AuthError as e:
            self.get_dropbox_client()
        except dropbox.exceptions.ApiError as e:
            print(f"Произошла ошибка при загрузке файла: {e}")  

    def download(self):
        try:
            # Выполняем загрузку файла
            metadata, res = self.dbx.files_download(self.remote_file_path)
            
            # Сохраняем файл на локальном компьютере
            with open(self.local_path_d, 'wb') as file:
                file.write(res.content)
            
            # print(f"Файл '{metadata.name}' успешно скачан!")
        except dropbox.exceptions.AuthError as e:
            self.get_dropbox_client()
        except dropbox.exceptions.ApiError as e:
            print(f"Произошла ошибка при скачивании файла: {e}")
    
    def download_all(self):
        try:
            entries = self.dbx.files_list_folder('/MTA_SKYNET/', recursive=True).entries
            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                # Формируем локальные и удаленные пути к файлам
                    remote_path = entry.path_display
                    relative_path = os.path.relpath(remote_path, '/MTA_SKYNET/')
                    local_path = os.path.join(self.folder_picks, relative_path)
                                # Скачиваем файл с Dropbox
                    try:
                        _, res = self.dbx.files_download(remote_path)
                        with open(local_path, 'wb') as file:
                            file.write(res.content)
                    except Exception as e:
                        print(f"Произошла ошибка при скачивании файла '{entry.name}': {e}")
        except dropbox.exceptions.AuthError as e:
            self.get_dropbox_client()
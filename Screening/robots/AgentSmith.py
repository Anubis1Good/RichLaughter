import os
import dropbox
from utils.settings import settings

class AgentSmith:
    def __init__(self,local_file):
        """local_file = '1_1_test_MOEX_FUT.json'
        """
        access_token = settings.dropbox_token
        self.dbx = dropbox.Dropbox(access_token)
        self.folder_picks = './Screening/strat_picks'
        if not os.path.exists(self.folder_picks):
            os.makedirs(self.folder_picks)
        self.local_path_u = os.path.join(self.folder_picks,local_file)
        prefix_file = 'u'+local_file
        self.local_path_d = os.path.join(self.folder_picks,prefix_file)
        self.remote_file_path = '/MTA_SKYNET/'+prefix_file

    def upload(self):
        try:
            mode = dropbox.files.WriteMode.overwrite
            with open(self.local_path_u, 'rb') as file:
                self.dbx.files_upload(file.read(), self.remote_file_path,mode=mode)
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
        except dropbox.exceptions.ApiError as e:
            print(f"Произошла ошибка при скачивании файла: {e}")
    
    def download_all(self):
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
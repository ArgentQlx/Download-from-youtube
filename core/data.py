import json

class DataManager():
    def __init__(self):
        self.data_path = '.\\core\\data.json'
        self.backup_path = '.\\core\\data_backup.json'
        with open(self.data_path, 'r', encoding='utf-8') as data:
            try:
                self.options = json.load(data)
            except: self.options = {}

    def save_data(self):
        # self.options.pop('progress_hooks', None)
        # for key, value in list(self.options.items()):
        #     if isinstance(value, (set, object)): del self.options[key]
        self.options.pop('progress_hooks', None)
        with open(self.data_path, 'w', encoding='utf-8') as data:
            try:
                json.dump(self.options, data, indent=4, ensure_ascii=False)
            except Exception as e: 
                print(f'Ошибка при сохранении: {e}\nБерем резервную копию')
                with open(self.backup_path, 'r', encoding='utf-8') as backup:
                    self.options = json.load(backup)
                    self.save_data()

    def change_param(self, key: str, value: any):
        if key not in self.options.keys(): return
        self.options[key] = value
        self.save_data()
    
    def get_options(self) -> dict: return self.options
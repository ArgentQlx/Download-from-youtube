from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon
import os
from gui.main_window import Ui_MainWindow
from logic.save_file import DownloadInfo
from core.data import DataManager
from logic.some_events import set_params, correct_params, get_extension

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Скачать видео')
        self.setWindowIcon(QIcon('.\\img\\icon.png'))
        self.init_events()
        self.file = QFileDialog()
        self.data = DataManager()
        self.fold_path = ''
        self.file_name = ''
        # self.subtitles.setDisabled(True)
        self.textBrowser.setOpenExternalLinks(True)
        self.cancel_btn.setDisabled(True)
        self.setFixedHeight(800)
        set_params(self)

    # ---------- НАВЕШИВАЕМ СОБЫТИЯ
    def init_events(self):
        self.save_btn.clicked.connect(self.start_download)
        self.high_quality.toggled.connect(self.check_checkbox)
        self.audio_option.toggled.connect(self.check_checkbox)
        self.quality_list.currentTextChanged.connect(self.check_list)
        self.cancel_btn.clicked.connect(self.cancel_download)

    # ---------- 2 ФУНКЦИИ СЛЕДЯТ ЧТОБЫ 3 ОПЦИИ НЕ БЫЛИ ВЫБРАНЫ ОДНОВРЕМЕННО
    def check_list(self):
        if not self.quality_list.currentText().lower() == 'не выбирать':
            if self.high_quality.isChecked(): self.high_quality.click()
            if self.audio_option.isChecked(): self.video_option.click()
        
    def check_checkbox(self):
        if self.high_quality.isChecked() or self.audio_option.isChecked(): self.quality_list.setCurrentText('Не выбирать')
        if self.audio_option.isChecked() and self.high_quality.isChecked(): self.high_quality.click()

    # ---------- СОЗДАЕТ ОТДЕЛЬНЫЙ ПОТОК И НАЧИНАЕТ ЗАГРУЗКУ
    def start_download(self):
        title = self.title_input.text().strip()
        url = self.url_input.text().strip()

        if not url: return
        elif 'index=' in url: title = ''

        correct_params(self)
        ext = get_extension(self)
        # path = QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения', '')
        path = self.file.getExistingDirectory(self, 'Папка для сохранения')
        if not path: return
        self.url_input.setText('')
        self.title_input.setText('')

        if not title: 
            path += '/%(title)s.' + ext
            self.file_name = '%(title)s'
        else:
            path += f'/{title}.{ext}'
            self.file_name = title
        self.data.change_param('outtmpl', path)

        self.progress_label.setText('Подготовка...')
        self.save_btn.setDisabled(True)
        self.cancel_btn.setDisabled(False)
        self.installer = DownloadInfo(self.data.get_options(), url)
        self.installer.progress_signal.connect(self.update_ui)
        self.installer.finish_signal.connect(self.finish_download)
        self.installer.start()

    # ---------- ПРЕРЫВАЕТ ПРОЦЕСС ЗАГРУЗКИ
    def cancel_download(self):
        if self.installer and self.installer.isRun:
            self.installer.cancel()
        self.finish_download('Успено прервано, удалите огрызки')

    # ---------- ПОКАЗЫВАЕТ ПРОГРЕЕСС ЗАГРУЗКИ
    def update_ui(self, data: dict):
        self.save_btn.setDisabled(True)
        self.cancel_btn.setDisabled(False)
        self.progress_bar.setValue(int(data['percentage']))
        self.progress_label.setText(f"Прогресс: {data['percentage']:.2f}%  |  {data['downloaded'] // 2**20}Мб / {data['total'] // 2**20}Мб  |  {data['speed'] // 2**20}Мб/с")

    # ---------- ОТОБРАЖАЕТ СООБЩЕНИЕ О ЗАВЕРШЕНИИ (ИЛИ ОШИБКЕ) ЗАГРУЗКИ
    def finish_download(self, status: str):
        self.progress_bar.setValue(0)
        self.progress_label.setText(status)
        self.save_btn.setDisabled(False)
        self.cancel_btn.setDisabled(True)

    # ---------- СОХРАНЯЕТ ДАННЫЕ О ПАРАМЕТРАХ ПРИ ЗАКРЫТИИ ОКНА, ПЕРЕОПРЕДЕЛЕНИЕ ФУНКЦИИ
    def closeEvent(self, a0): correct_params(self)
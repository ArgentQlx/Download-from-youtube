import yt_dlp
from PyQt6.QtCore import QThread, pyqtSignal

class DownloadInfo(QThread):
    progress_signal = pyqtSignal(dict)
    finish_signal = pyqtSignal(str)

    def __init__(self, options, url: str):
        super().__init__()
        self.options = options
        self.url = url
        self.process = None
        self.isRun = False

    # ---------- ПЕРЕОПРЕДЕЛЕНИЕ МЕТОДА RUN ДЛЯ НАЧАЛА РАБОТЫ ПОТОКА
    def run(self):
        def my_hook(d):
            # Статусы: 'downloading', 'finished', 'error'
            if d['status'] == 'downloading':
                # Вычисляем процент загрузки
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                speed = d.get('speed')
                if not speed: speed = 0
                if total:
                    percentage = (downloaded / total) * 100
                    self.progress_signal.emit({
                        'downloaded': downloaded,
                        'total': total,
                        'percentage': percentage,
                        'speed': speed
                    })
                    
                    # print(f"Скачано: {percentage:.2f}% | {downloaded // 1024}мб / {total // 1024}мб")
            elif d['status'] == 'finished': self.finish_signal.emit('Скачивание завершено')
            else: self.finish_signal.emit('Ошибка при сохранении')

        self.options['progress_hooks'] = [my_hook]

        try:
            with yt_dlp.YoutubeDL(self.options) as ydl:
                self.isRun = True
                self.process = ydl
                ydl.download([self.url])
        except Exception as e: self.finish_signal.emit(f'Ошибка при сохранении: {e}')

    def cancel(self):
        if self.process: 
            raise SystemExit("Загрузка прервана пользователем")
            # self.process.params['quiet'] = True
            # self.process.__exit__()
            # self.terminate()

    
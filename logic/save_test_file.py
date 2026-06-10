import yt_dlp

def save_video(self, path: str, url):
    def my_hook(d):
        # Статусы: 'downloading', 'finished', 'error'
        if d['status'] == 'downloading':
            # Вычисляем процент загрузки
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            
            if total:
                percentage = (downloaded / total) * 100
                print(f"Скачано: {percentage:.2f}% | {downloaded} / {total}")
        elif d['status'] == 'finished':
            print('Скачано')
        else: print('Ошибка')

    options = {
    'format': 'bestvideo/best', # Скачать лучшее качество
    'merge_output_format': 'mp4',        # Объединить в MP4
    'outtmpl': path,      # Имя файла: Название_видео.расширение
    'noprogress': True,
    'progress_hooks': [my_hook] 
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

# save_video('', 'https://www.youtube.com/watch?v=89BszIJjWyI')

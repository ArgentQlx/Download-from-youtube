# ---------- ВЫСТАВЛЯЕТ ЗНАЧЕНИЯ ЧЕКБОКСОВ ПРИ СОЗДАНИИ ОКНА
def set_params(self):
        options = self.data.get_options()
        if options['format'] == 'bestaudio+bestvideo': self.high_quality.click()
        if options['noplaylist']: self.only_one_option.click()
        if options['merge_output_format'] == 'mp3': self.audio_option.click()
        if options['writesubtitles']: self.subtitles.click()

# ---------- ПРОВЕРЯЕТ ЧЕКБОКСЫ И ФОРМИРУЕТ АКТУАЛЬНЫЕ ОПЦИИ ДЛЯ СКАЧИВАНИЯ
def correct_params(self):
    if self.high_quality.isChecked():
        if self.audio_option.isChecked(): self.data.change_param('format', 'bestaudio')
        else: self.data.change_param('format', 'bestaudio+bestvideo')

    else:
        if self.quality_list.currentText().lower() == 'не выбирать':
            self.data.change_param('format', 'best')
        else:
            quantity = self.quality_list.currentText()[:-1]
            if self.audio_option.isChecked(): self.data.change_param('format', 'best'); return
            self.data.change_param('format', f'bestvideo[height<={quantity}]+bestaudio/best[height<={quantity}]/best')

    if self.subtitles.isChecked():
        self.data.change_param('writesubtitles', True)
        self.data.change_param('writeautomaticsub', True)
    else:
        self.data.change_param('writesubtitles', False)
        self.data.change_param('writeautomaticsub', False)

    if self.only_one_option.isChecked():
        self.data.change_param('noplaylist', True)
    else: self.data.change_param('noplaylist', False)

# ----------ПРОВЕРЯЕТ ФОРМАТ СКАЧИВАНИЯ (АУДИО ИЛИ ВИДЕО) И ВОЗВРАЩАЕТ ФОРМАТ
def get_extension(self) -> str:
        if self.audio_option.isChecked():
            self.data.change_param('merge_output_format', 'mp3')
            return 'mp3'
        else: 
            self.data.change_param('merge_output_format', 'mp4')
            return 'mp4'
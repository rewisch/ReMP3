import os

from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QFileDialog

from src.model.songListModel import SongListModel
from src.audio.mp3 import MP3
from src.db.db import Database

Ui_MainWindow, QtBaseClass = uic.loadUiType('_gui/mainwindow.ui')

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.db = Database()
        self.model = SongListModel(songs=self.db.get_songs())
        self.songView.setModel(self.model)

        self.songLine.installEventFilter(self)
        self.songView.installEventFilter(self)

        self.tbAddSong.pressed.connect(lambda: self.add_song(self.songLine.text()))
        self.tbRemoveSong.pressed.connect(self.remove_song)
        self.tbFileDialog.pressed.connect(self.file_dialog)
        self.tbPlay.pressed.connect(self.play)
        self.tbStop.pressed.connect(self.stop)
        self.tbPause.pressed.connect(self.pause)
        self.songView.doubleClicked.connect(self.play)

        self.mp3 = MP3()
        self.activeWidget = None

    def add_song(self, song):
        if song:
            fullname, ext = song.split('.')
            try:
                songname = fullname.split('/')[-1]
            except:
                songname = fullname

            if ext == 'mp3':
                file_name = self.mp3.mp3_to_wav(song)
            else:
                file_name = song

            with open(file_name, 'rb') as rs:
                self.db.set_song(songname, rs.read())
            os.remove("converted.wav")
            self.model.songs.append(songname)
            self.model.layoutChanged.emit()
            self.songLine.setText('')

    def remove_song(self):
        indexes = self.songView.selectedIndexes()
        if indexes:
            index = indexes[0]
            title = index.data()
            del self.model.songs[index.row()]
            self.db.del_song(title)
            self.model.layoutChanged.emit()
            self.songView.clearSelection()

    def file_dialog(self):
        file_name, filter = QFileDialog.getOpenFileName(self, "Open Song", "/home", "Images (*.mp3 *.pdf)")
        self.songLine.setText(file_name)
        self.songLine.setCursorPosition(0)

    def play(self):
        indexes = self.songView.selectedIndexes()
        title = indexes[0].data()
        blob = self.db.get_song(title)
        self.mp3.play(title, blob)

    def stop(self):
        self.mp3.stop()

    def pause(self):
        self.mp3.pause()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            for url in event.mimeData().urls():
                file_name = str(url.toLocalFile())
                self.add_song(file_name)
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == Qt.Key_Return and self.activeWidget == self.songLine:
            self.add_song()
        elif a0.key() == Qt.Key_Delete:
            self.remove_song()
        else:
            super().keyPressEvent(a0)

    def eventFilter(self, obj, event):
        if obj == self.songLine:
            if event.type() == QEvent.FocusIn:
                self.activeWidget = self.songLine
            elif event.type() == QEvent.FocusOut:
                self.activeWidget = None
        elif obj == self.songView:
            if event.type() == QEvent.FocusIn:
                self.activeWidget = self.songView
            elif event.type() == QEvent.FocusOut:
                self.activeWidget == None
        return super(MainWindow, self).eventFilter(obj, event)

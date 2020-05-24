from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QFileDialog
from pydub import AudioSegment

from src.model.songListModel import SongListModel
from src.audio.mp3 import MP3

Ui_MainWindow, QtBaseClass = uic.loadUiType('_gui/mainwindow.ui')

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = SongListModel(songs=['sound.wav', 'sound.mp3'])
        self.songView.setModel(self.model)

        self.songLine.installEventFilter(self)
        self.songView.installEventFilter(self)
        self.activeWidget = None

        self.tbAddSong.pressed.connect(self.add_song)
        self.tbRemoveSong.pressed.connect(self.remove_song)
        self.tbFileDialog.pressed.connect(self.file_dialog)
        self.tbPlay.pressed.connect(self.play)
        self.tbStop.pressed.connect(self.stop)
        self.tbPause.pressed.connect(self.pause)

        self.mp3 = MP3()

    def add_song(self):
        text = self.songLine.text()
        if text:
            self.model.songs.append(text)
            self.model.layoutChanged.emit()
            self.songLine.setText('')

    def remove_song(self):
        indexes = self.songView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.songs[index.row()]
            self.model.layoutChanged.emit()
            self.songView.clearSelection()

    def file_dialog(self):
        file_name, filter = QFileDialog.getOpenFileName(self, "Open File", "/home", "Images (*.mp3 *.pdf)")
        self.songLine.setText(file_name)

    def play(self):
        indexes = self.songView.selectedIndexes()
        if indexes:
            self.mp3.play(self.model.data(indexes[0], Qt.DisplayRole))

    def stop(self):
        self.mp3.stop()

    def pause(self):
        self.mp3.pause()

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

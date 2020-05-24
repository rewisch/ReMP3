from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class SongListModel(QtCore.QAbstractListModel):
    def __init__(self, *args, songs=None, **kwargs):
        super(SongListModel, self).__init__(*args, **kwargs)
        self.songs = songs or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.songs[index.row()]
            return text

    def rowCount(self, index):
        return len(self.songs)



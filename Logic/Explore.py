from PyQt5 import QtCore, QtWidgets


class Explore(QtWidgets.QFileDialog):
    """class Explore implements functions for returning the directory path of image(s) for loading in viewer"""

    def win_explore_file(self):
        """Implements methods related with file windows explorer"""

        dir = "/home"
        filters = "Images (*.png *.bmp *.jpg)"
        options = QtWidgets.QFileDialog.Options()
        filepath_e, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Explorar archivos", dir, filters, options=options
        )
        if len(filepath_e) <= 1:
            btn_flag = 0
        elif len(filepath_e) > 1:
            btn_flag = 1

        return filepath_e, btn_flag

    def win_explore_folder(self):
        """Implements methods related with folder windows explorer"""

        dir = "/home"
        filters = ["*.png", "*.bmp", "*.jpg"]
        options = QtWidgets.QFileDialog.Options()
        dirpath_e = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Explorar carpeta", dir
        )
        dirpath = QtCore.QDir(dirpath_e)
        filenames_e = dirpath.entryList(filters, QtCore.QDir.Files, QtCore.QDir.Name)
        if len(filenames_e) <= 1:
            btn_flag = 0
        elif len(filenames_e) > 1:
            btn_flag = 1

        filepaths_e = [None] * len(filenames_e)
        for i in range(len(filenames_e)):
            filepaths_e[i] = dirpath_e + "/" + filenames_e[i]

        return filepaths_e, btn_flag

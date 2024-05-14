from tkinter import filedialog


class FileSelect:
    ShortFileLinkLength = 45
    SelectingFileLink = ""

    def OpenFileSelectWindow():
        typ = [(".slnファイル", "*.sln")]
        dir = "C:\\"
        fle = filedialog.askopenfilename(filetypes=typ, initialdir=dir)
        return fle

    def SetSelectingFileLink(string):
        FileSelect.SelectingFileLink = string

    def GetSelectingFileLink():
        return FileSelect.SelectingFileLink

    def ShorteningFileLink(FileLink):
        length = FileSelect.ShortFileLinkLength
        result = FileLink
        if len(FileLink) > length:
            max = len(FileLink)
            min = max - length
            result = f"...{FileLink[min:max]}"
        return result

    def FileSelect():
        this = FileSelect
        FileLink = (
            this.OpenFileSelectWindow()
        )  # ファイル選択ウィンドウを表示・選択させる
        this.SetSelectingFileLink(FileLink)  # 変数にファイルのフルパスを格納
        return this.ShorteningFileLink(FileLink)  # 画面表示用にパス表示を短縮

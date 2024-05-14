import PySimpleGUI as sg
import FileAction
import shutil
import os
import glob
import subprocess

from Module.FileSelect import FileSelect

TMP_PATH: str = f"{FileAction.ConvertFileLink("")}/.swntmp"
RESULT_PATH: str = FileAction.ConvertFileLink("result")
Output_FileName: str = ""


def deleteDir(path: str):
    target: str = f"{TMP_PATH}/{path}"

    if not os.path.isdir(target):
        return

    shutil.rmtree(target)
    return

def deleteFile(path: str):
    target = glob.glob(f"{TMP_PATH}\\{path}")

    for file in target:
        os.remove(file)

def PrepareProject():
    path: str = FileSelect.FileSelect()
    directory: str = os.path.dirname(path)

    if not os.path.isdir(directory):
        return

    # 出力先のフォルダをリセットする
    if os.path.isdir(TMP_PATH):
        shutil.rmtree(TMP_PATH)

    # 内容を丸ごとコピーする
    shutil.copytree(directory, TMP_PATH)

    deleteDirectorys: list[str] = [".vs", "Project/Debug", ".git", ".vscode"]
    deleteFileTypes: list[str] = [".pdb", ".exe", ".docx", ".xlsx", ".pptx", ".zip"]

    for dir in deleteDirectorys:
        deleteDir(dir)

    for type in deleteFileTypes:
        deleteFile(f"*{type}")
    return

def createArchiveFile():
    fileName: str = Output_FileName

    if fileName == "":
        fileName = "Archive"

    # zipファイルを作成する
    shutil.make_archive(
        f"{RESULT_PATH}/{fileName}",
        format="zip",
        root_dir=TMP_PATH,
    )

    tmp = sg.popup_ok_cancel("出力完了\n出力フォルダを開きますか？", title="確認")
    if tmp == "Cancel":
        return

    OpenOutputFolder()
    return

def OpenOutputFolder():
    if not os.path.isdir(RESULT_PATH):
        sg.popup(
            "出力フォルダがありません。\n出力処理を実行後に再度ボタンを押してください。",
            title="エラー",
        )
        return

    subprocess.Popen(["explorer", RESULT_PATH], shell=True)
    return

# 画面構成
layout = [
    [sg.Text("出力ファイル名設定 (Default: Archive.zip)")],
    [sg.HorizontalSeparator()],
    [sg.Input("", key="OutputFileName"), sg.Text(".zip")],
    [sg.Text("")],
    [sg.Text("出力")],
    [sg.HorizontalSeparator()],
    [sg.Button(".sln ファイル選択", key="sln_select"), sg.Button("出力フォルダを開く", key="open_outputFolder")]
]

# ウィンドウの生成
window = sg.Window("Visual Studio Project Ejecter", layout, size=(400, 175))

if os.path.isdir(RESULT_PATH):
    shutil.rmtree(RESULT_PATH)

# イベントループ
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        # ウィンドウが閉じられた時に処理を抜ける
        break
    elif event == "sln_select":
        Output_FileName = values["OutputFileName"]

        # コピーしたプロジェクトを整える
        PrepareProject()

        createArchiveFile()
    elif event == "open_outputFolder":
        OpenOutputFolder()

# 出力先のフォルダをリセットする
if os.path.isdir(TMP_PATH):
    shutil.rmtree(TMP_PATH)

window.close()

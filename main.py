from ui import Ui_MainWindow, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PIL import Image
import pyautogui
import numpy as np
import cv2
import sys
import keyboard


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col
    return None


def pprint(arr):
    for i in range(9):
        print(arr[i])


def play(arr, image):
    pyautogui.click(200, 200)
    c1, c2 = -1, -1
    for i in range(200, 750, 65):
        c1 += 1
        c2 = -1
        for j in range(300, 840, 65):
            c2 += 1
            if image.getpixel((j, i)) == (255, 255, 255):
                pyautogui.click(j, i)
                pyautogui.click((290 + (arr[c1][c2] - 1) * 70), 830)


color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0),
         (0, 0, 128), (0, 128, 0), (128, 0, 0)]
arr = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0], ]
threshold = 0.75


def main():
    pyautogui.screenshot("ScreenShot.png")
    board = cv2.imread("ScreenShot.png")
    for i in range(0, 9):
        n = cv2.imread(rf"imgs\{i + 1}.png")
        w, h = n.shape[:-1]
        res = cv2.matchTemplate(board, n, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(board, (pt[0] + 5, pt[1] + 15), (pt[0] + w - 15, pt[1] + h + 5), color[i], 30)

    cv2.imwrite('result.png', board)
    result_image = Image.open("result.png")
    c1, c2 = -1, -1
    for i in range(200, 750, 65):
        c1 += 1
        c2 = -1
        for j in range(300, 840, 65):
            c2 += 1
            try:
                arr[c1][c2] = color.index(result_image.getpixel((j, i))) + 1
            except:
                arr[c1][c2] = 0

    solve(arr)
    QMessageBox.about(ui.centralwidget, "confirm", "you cant use the mouse for\nthe next 13 seconds")
    temp=f"{arr[0]}\n{arr[1]}\n{arr[2]}\n{arr[3]}\n{arr[4]}\n{arr[5]}\n{arr[6]}\n{arr[7]}\n{arr[8]}"
    ui.textBrowser.setText(temp)
    play(arr, result_image)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
ui.pushButton.clicked.connect(main)
keyboard.press_and_release("Ctrl + shift +t")
sys.exit(app.exec_())
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import random
import sys
import threading
import pickle
import re

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextFormat, QColor, QPalette
import os
from pathlib import Path
import qdarktheme
from PyQt5.QtWidgets import QTextEdit, QToolTip

from source.GUI.BrowseDirectory import New_Project_UI
from source.GUI.DeleteFiles import DeleteFiles_UI
from source.GUI.QCodeEditor import Highlighter
from source.Engine.EngineChecker import *

import time


class OpenFile(QtCore.QThread):
    Editor_text = QtCore.pyqtSignal(str)
    Itsdone = QtCore.pyqtSignal(int)
    design_file = ""
    finish = 0

    def init(self):
        super(OpenFile, self).init()

    def run(self):
        old_file_list = []
        new_file_list = []
        while True:
            if self.finish:
                break
            if os.path.isfile(self.design_file):
                with open(self.design_file) as File_Read:
                    new_file_list = File_Read.readlines()
                    if not (new_file_list == old_file_list):
                        for line in new_file_list:
                            line = re.sub("\n", "", line)
                            self.Editor_text.emit(line)
                        old_file_list = new_file_list
                    else:
                        self.Itsdone.emit(1)
                        return


class MainWindow_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow_UI, self).__init__()
        self.current_index = None
        self.Results = None
        self.files_button = None
        self.path = None
        self.New_Project_ui = New_Project_UI()
        self.Delete_project_ui = DeleteFiles_UI()
        self.directory_path = ""
        self.projectName = ""
        self.design_files = []
        self.simulation_results = []
        self.selections = []
        self.dark = 0
        self.autotexts = None
        self.texts = None
        self.openFileThread = OpenFile()

        uic.loadUi("MainWindow.ui", self)

        # Define the widgets
        self.action_new_project = self.findChild(QtWidgets.QAction, "actionNew_Project")
        self.Project_Description = self.findChild(QtWidgets.QLabel, "PD_LABEL")
        self.actionDark = self.findChild(QtWidgets.QAction, "actionDark")
        self.actionLight = self.findChild(QtWidgets.QAction, "actionLight")
        self.actionStart = self.findChild(QtWidgets.QAction, "actionStart")
        self.svCodeEDitor = self.findChild(QtWidgets.QPlainTextEdit, "SVCodeEditor")
        self.work_space_tree = self.findChild(QtWidgets.QTreeWidget, "Directory_tree")
        self.charts_pie = self.findChild(QtWidgets.QWidget, "charts")

        # connect the functions
        self.action_new_project.triggered.connect(self.new_project)
        self.New_Project_ui.Directory_text.connect(self.Project_Directory)
        self.New_Project_ui.Name_text.connect(self.project_name)
        self.Delete_project_ui.Delete_Signal.connect(self.removeItem)
        self.actionDark.triggered.connect(self.setDarkMode)
        self.actionLight.triggered.connect(self.setLightMode)
        self.actionStart.triggered.connect(self.start_simulation)
        self.openFileThread.Editor_text.connect(self.PrintCode)
        self.openFileThread.Itsdone.connect(self.Highlight_everword)
        self.highlighter = Highlighter(self.svCodeEDitor.document())
        # initialize Widgets
        self.svCodeEDitor.setReadOnly(True)
        font = QFont('Consolas', 12)
        self.svCodeEDitor.setFont(font)
        self.work_space_tree.itemDoubleClicked.connect(self.handle_double_click)
        # y = [100]
        # mylabels = ["All Good"]
        # mycolors = ["green"]
        # _, self.texts, self.autotexts = self.charts_pie.canvas.axes.pie(y, labels=mylabels, colors=mycolors,
        #                                                                 autopct="%.2f")

    def new_project(self):
        self.New_Project_ui.show()

    def show_msg_box(self, msg: str):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(msg)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        x = msg_box.exec_()

    def Highlight_everword(self, signal):
        if signal:
            self.selections = []
            if self.Results:
                results = self.Results[self.current_index]
                self.svCodeEDitor.line_written = self.Arrange_lines_errors(results)
                for lines in results["Error line"]:
                    for lines_2 in lines:
                        if isinstance(lines_2, list):
                            for lines_3 in lines_2:
                                if isinstance(lines_3, list):
                                    for lines_4 in lines_3:
                                        self.highlightLine(lines_4)
                                else:
                                    self.highlightLine(lines_3)
                        else:
                            self.highlightLine(lines_2)

    def handle_double_click(self, item):
        self.svCodeEDitor.clear()
        self.openFileThread.finish = 1
        self.openFileThread.exit()
        self.openFileThread.design_file = self.directory_path + "/" + item.text(0)
        self.openFileThread.finish = 0
        self.openFileThread.start()
        self.current_index = self.design_files.index(item.text(0))

    def start_simulation(self):
        if self.design_files:
            self.Results = []
            for design in self.design_files:
                Checker = Checks(self.directory_path + "/" + design)
                Checker.do_all_checks()
                self.Results.append(Checker.error_panel)
            mylabels = self.Results[0]["Type"]
            mycolors = ["green", "skyblue", "orange", "red", "purple", "brown", "gray"]
            Total_errors = [0, 0, 0, 0, 0, 0, 0]
            self.charts_pie.canvas.axes.clear()
            for result in self.Results:
                for i in range(len(result["Num errors"])):
                    Total_errors[i] += result["Num errors"][i]
            wedges, self.texts, self.autotexts = self.charts_pie.canvas.axes.pie(Total_errors, colors=mycolors,
                                                                                 autopct="%.2f",
                                                                                 textprops={'fontsize': 8})
            self.charts_pie.canvas.axes.legend(wedges, mylabels, loc="center right", bbox_to_anchor=(0.08, 0.6),
                                               prop={'size': 6})
            self.charts_pie.canvas.draw()
            icon_v = QtGui.QIcon("Icons/Ready.png")
            for i in range(self.work_space_tree.topLevelItemCount()):
                item = self.work_space_tree.topLevelItem(i)
                item.setIcon(1, icon_v)
            if self.dark:
                self.setDarkMode()
            else:
                self.setLightMode()
            self.selections = []
            current_file = re.sub(self.directory_path + "/", "", self.openFileThread.design_file)
            if current_file in self.design_files:
                index = self.design_files.index(current_file)
                results = self.Results[index]
                self.svCodeEDitor.line_written = self.Arrange_lines_errors(results)
                for lines in results["Error line"]:
                    for lines_2 in lines:
                        if isinstance(lines_2, list):
                            for lines_3 in lines_2:
                                if isinstance(lines_3, list):
                                    for lines_4 in lines_3:
                                        self.highlightLine(lines_4)
                                else:
                                    self.highlightLine(lines_3)
                        else:
                            self.highlightLine(lines_2)
        else:
            self.show_msg_box("you need to insert your design")

    def removeItem(self, flag):
        Item = self.work_space_tree.currentItem()
        if Item is None:
            self.show_msg_box(msg="there is no file selected")
        else:
            if self.openFileThread.design_file == self.directory_path + "/" + Item.text(0):
                self.svCodeEDitor.clear()
                self.openFileThread.finish = 1
                self.openFileThread.exit()
                self.design_files.remove(Item.text(0))
                self.openFileThread.design_file = ""
            if flag == 1:
                file = self.directory_path + "/" + Item.text(0)
                print(file)
                os.remove(file.replace("/", "\\"))
            self.work_space_tree.topLevelItem(0).removeChild(Item)

    def PrintCode(self, line):
        self.svCodeEDitor.appendPlainText(line)

    def Project_Directory(self, Path: str):
        self.directory_path = Path

    def project_name(self, Name: str):
        self.Project_Description.setText(Name + "-" + str(self.directory_path))

    def Arrange_lines_errors(self, results):
        results_dic = {}
        # arithmetic overflow
        for i in range(len(results["Error line"][0])):
            if results["Error line"][0][i] in results_dic:
                results_dic[results["Error line"][0][i]] += "-- Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
            else:
                results_dic[results["Error line"][0][i]] = "Arithmetic overflow error at line " + str(
                    results["Error line"][0][i]) + " in variable " + str(results["variable Impacted"][0][i])
        for i in range(len(results["Error line"][1])):
            if results["Error line"][1][i] in results_dic:
                results_dic[results["Error line"][1][i]] += "-- unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
            else:
                results_dic[results["Error line"][1][i]] = "unreachable Block error at line " + str(
                    results["Error line"][1][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][1][i])):
                    results_dic[results["Error line"][1][i]] += str(results["variable Impacted"][1][i][j]) + " "
        for i in range(len(results["Error line"][2])):
            if results["Error line"][2][i] in results_dic:
                results_dic[results["Error line"][2][i]] += "-- unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
            else:
                results_dic[results["Error line"][2][i]] = "unreachable finite state machine at line " + str(
                    results["Error line"][2][i]) + " because " + str(
                    results["variable Impacted"][2][i]) + " is unreachable"
        for i in range(len(results["Error line"][3])):
            if results["Error line"][3][i] in results_dic:
                results_dic[results["Error line"][3][i]] += "-- uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
            else:
                results_dic[results["Error line"][3][i]] = "uninitialized register declared at line " + str(
                    results["Error line"][3][i]) + " in reg " + str(results["variable Impacted"][3][i])
        for i in range(len(results["variable Impacted"][4])):
            for line in results["Error line"][4][i]:
                if line in results_dic:
                    results_dic[line] += "-- multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
                else:
                    results_dic[line] = "multidriven block at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][4][i])
        for i in range(len(results["Error line"][5])):
            if results["Error line"][5][i] in results_dic:
                results_dic[results["Error line"][5][i]] += "-- Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
            else:
                results_dic[results["Error line"][5][i]] = "Non Full case statement at line " + str(
                    results["Error line"][5][i]) + " with variables may be the cause "
                for j in range(len(results["variable Impacted"][5][i])):
                    results_dic[results["Error line"][5][i]] += str(results["variable Impacted"][5][i][j]) + " "
        for i in range(len(results["variable Impacted"][6])):
            for line in results["Error line"][6][i]:
                if line in results_dic:
                    results_dic[line] += "-- latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][6][i])
                else:
                    results_dic[line] = "latch infered at line " + str(line) + " in variable " + str(
                        results["variable Impacted"][6][i])
        return results_dic

    def setDarkMode(self):
        qdarktheme.setup_theme()
        self.dark = 1
        if self.autotexts:
            for ins in self.autotexts:
                ins.set_color('white')
        if self.texts:
            for ins in self.texts:
                ins.set_color('white')
        self.charts_pie.canvas.axes.set_facecolor("black")
        self.charts_pie.canvas.figure.set_facecolor("black")
        self.charts_pie.canvas.draw()

    def setLightMode(self):
        qdarktheme.setup_theme("light")
        self.dark = 0
        if self.autotexts:
            for ins in self.autotexts:
                ins.set_color('white')
        if self.texts:
            for ins in self.texts:
                ins.set_color('black')
        self.charts_pie.canvas.axes.set_facecolor("white")
        self.charts_pie.canvas.figure.set_facecolor("white")
        self.charts_pie.canvas.draw()

    def highlightLine(self, lineNumber):
        cursor = self.svCodeEDitor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        for i in range(lineNumber - 1):
            cursor.movePosition(QTextCursor.Down)
        cursor.select(QTextCursor.LineUnderCursor)

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground((QColor(194, 223, 255, 90)))  # Set background color
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = cursor
        self.selections.append(selection)

        self.svCodeEDitor.setExtraSelections(self.selections)

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self.work_space_tree)
        new_action = contextMenu.addAction("Add Files")
        Delete_action = contextMenu.addAction("Delete Files")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == new_action:
            self.add_files()
        elif action == Delete_action:
            self.Delete_project_ui.show()

    def add_files(self):
        if self.directory_path == "":
            self.show_msg_box("You must first Create a Project")
        else:
            self.path = self.directory_path
            self.files_button = QtWidgets.QFileDialog.getOpenFileNames(None)
            if not self.files_button:
                return
            for file in self.files_button[0]:
                extension = re.sub(".+\.", "", file)
                if not (extension == "v" or extension == "sv"):
                    self.show_msg_box("Only Verilog or SystemVerilog files are supported")
                    return
                file_name = Path(file).stem
                a = QtWidgets.QTreeWidgetItem([str(file_name + "." + extension)])
                if extension == "v":
                    icon_v = QtGui.QIcon("Icons/verilog.png")
                    a.setIcon(0, icon_v)
                else:
                    icon_v = QtGui.QIcon("Icons/systemverilog.png")
                    a.setIcon(0, icon_v)
                icon_v = QtGui.QIcon("Icons/notready.png")
                a.setIcon(1, icon_v)
                self.work_space_tree.addTopLevelItem(a)
                self.design_files.append(str(file_name + "." + extension))
                os.system("copy " + file.replace("/", "\\") + " " + self.directory_path.replace("/", "\\"))


if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    UIWindow = MainWindow_UI()
    UIWindow.show()
    app.exec_()

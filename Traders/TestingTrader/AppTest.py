from PyQt5.QtCore import QProcess,Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QProgressDialog,QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AppTest')
        self.main_layout = QVBoxLayout()
        self.resize(700,700)
        self.processes = {}  # Словарь для хранения процессов
        self.setStyleSheet("""
            QWidget {
                background-color: #5CCDC9;
            }
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size:18px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
            QLabel {
                background-color: #009B95;
                qproperty-alignment: 'AlignCenter';
                border-radius: 5px;
                color: white;
                font-size:18px;
            }
        """)
        self.init_btn_style = """
            QPushButton {
                background-color: #006561;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size:18px;
            }
            QPushButton:hover {
                background-color: #6C0AAB;
            }
            QPushButton:pressed {
                background-color: #A6A600;
            }
        """
        line0 = QHBoxLayout()

        self.processes_lbl = QLabel(text='AmountProceses: '+str(len(self.processes)))
        line1 = QVBoxLayout()
        line2 = QVBoxLayout()
        self.moex_fut_btn = QPushButton(text='StartMoexFut')
        self.moex_fut_btn_close = QPushButton(text='CloseMoexFut')
        self.moex_stock_btn = QPushButton(text='StartMoexStock')
        self.moex_stock_btn_close = QPushButton(text='CloseMoexStock')

        self.moexm_fut_btn = QPushButton(text='StartMoexFut2')
        self.moexm_fut_btn_close = QPushButton(text='CloseMoexFut2')
        self.moexm_stock_btn = QPushButton(text='StartMoexMTAStock')
        self.moexm_stock_btn_close = QPushButton(text='CloseMoexMTAStock')

        line1.addWidget(self.moex_fut_btn)
        line1.addWidget(self.moex_fut_btn_close)
        line1.addWidget(self.moex_stock_btn)
        line1.addWidget(self.moex_stock_btn_close)
        line1.addWidget(self.moexm_fut_btn)
        line1.addWidget(self.moexm_fut_btn_close)
        line1.addWidget(self.moexm_stock_btn)
        line1.addWidget(self.moexm_stock_btn_close)


        self.bitget_fut_btn = QPushButton(text='StartBitgetFut')
        self.bitget_fut_btn_close = QPushButton(text='CloseBitgetFut')
        self.bybit_fut_btn = QPushButton(text='StartBybitFut')
        self.bybit_fut_btn_close = QPushButton(text='CloseBybitFut')
        self.bitgetm_fut_btn = QPushButton(text='StartBitgetMTAFut')
        self.bitgetm_fut_btn_close = QPushButton(text='CloseBitgetMTAFut')
        self.bybitm_fut_btn = QPushButton(text='StartBybitMTAFut')
        self.bybitm_fut_btn_close = QPushButton(text='CloseBybitMTAFut')


        line2.addWidget(self.bitget_fut_btn)
        line2.addWidget(self.bitget_fut_btn_close)
        line2.addWidget(self.bybit_fut_btn)
        line2.addWidget(self.bybit_fut_btn_close)
        line2.addWidget(self.bitgetm_fut_btn)
        line2.addWidget(self.bitgetm_fut_btn_close)
        line2.addWidget(self.bybitm_fut_btn)
        line2.addWidget(self.bybitm_fut_btn_close)


        line0.addLayout(line1)
        line0.addLayout(line2)
        self.main_layout.addWidget(self.processes_lbl)
        self.main_layout.addLayout(line0)
        self.setLayout(self.main_layout)
        script = 'universal_test.py'

        self.moex_fut_btn.clicked.connect(
            lambda: self.toggle_script(self.moex_fut_btn,'moex_fut',script,['MOEX','FUT','run'])
        )
        self.moex_fut_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.moex_fut_btn_close,'moex_fut_close',script,['MOEX','FUT','close'])
        )
        # self.moexm_fut_btn.clicked.connect(
        #     lambda: self.toggle_script(self.moexm_fut_btn,'moexM_fut',script,['MOEXM','FUT','run'])
        # )
        # self.moexm_fut_btn_close.clicked.connect(
        #     lambda: self.toggle_close_script(self.moexm_fut_btn_close,'moexM_fut_close',script,['MOEXM','FUT','close'])
        # )
        self.moexm_fut_btn.clicked.connect(
            lambda: self.toggle_script(self.moexm_fut_btn,'moex2_fut',script,['MOEX2','FUT','run'])
        )
        self.moexm_fut_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.moexm_fut_btn_close,'moex2_fut_close',script,['MOEX2','FUT','close'])
        )
        self.moex_stock_btn.clicked.connect(
            lambda: self.toggle_script(self.moex_stock_btn,'moex_stock',script,['MOEX','STOCK','run'])
        )
        self.moex_stock_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.moex_stock_btn_close,'moex_stock_close',script,['MOEX','STOCK','close'])
        )
        self.moexm_stock_btn.clicked.connect(
            lambda: self.toggle_script(self.moexm_stock_btn,'moexM_stock',script,['MOEXM','STOCK','run'])
        )
        self.moexm_stock_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.moexm_stock_btn_close,'moexM_stock_close',script,['MOEXM','STOCK','close'])
        )
        self.bitget_fut_btn.clicked.connect(
            lambda: self.toggle_script(self.bitget_fut_btn,'bitget_fut',script,['Bitget','FUT','run'])
        )
        self.bitget_fut_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.bitget_fut_btn_close,'bitget_fut_close',script,['Bitget','FUT','close'])
        )
        self.bitgetm_fut_btn.clicked.connect(
            lambda: self.toggle_script(self.bitgetm_fut_btn,'bitgetM_fut',script,['BitgetM','FUT','run'])
        )
        self.bitgetm_fut_btn_close.clicked.connect(
            lambda: self.toggle_close_script(self.bitgetm_fut_btn_close,'bitgetM_fut_close',script,['BitgetM','FUT','close'])
        )

    def update_amount_processes(self):
        text = 'AmountProceses: '+str(len(self.processes)) + '\n'
        for p in self.processes:
            text += str(p) + '\n'
        self.processes_lbl.setText(text)

    def cleanup_processes(self):
        """Удаление всех завершенных процессов"""
        del_processes = []
        for process in self.processes:  # Используем копию списка для безопасного удаления
            if self.processes[process].state() == QProcess.NotRunning:
                del_processes.append(process)
        for process in del_processes:
            self.processes[process].deleteLater()
            del self.processes[process]
            print(process,"Удален завершенный процесс")
        self.update_amount_processes()

    def add_process(self,name, script_path, args):
        self.processes[name] = QProcess(self)
        self.processes[name].setProcessChannelMode(QProcess.MergedChannels)  # Объединяем stdout и stderr
        # Подключаем обработчик вывода
        self.processes[name].readyReadStandardOutput.connect(lambda: print(self.processes[name].readAllStandardOutput().data().decode( errors="replace")))
        self.processes[name].start("python", [script_path] + args)
        self.update_amount_processes()

    def toggle_script(self, btn: QPushButton, name, script_path, args):
        if name not in self.processes or self.processes[name].state() == QProcess.NotRunning:
            # Запуск процесса
            self.add_process(name, script_path, args)
            self.processes[name].finished.connect(lambda: self.base_start_btn_styling(btn,name,script_path,args))
            print(f"Скрипт {name} запущен с аргументами: {args}")
            btn.setText(btn.text().replace('Start', 'Stop'))
            btn.setStyleSheet('background-color: #A6A600;')
        else:
            # Остановка процесса
            print(f"Скрипт {name} завершается...")
            self._safe_terminate_process(name, btn)
            print(f"Скрипт {name} завершен!")

    def base_start_btn_styling(self,btn,name, script_path, args):
        # self.add_process(name+'close', script_path, args[:-1] + ['close'])
        # self.processes[name+'close'].finished.connect(self.cleanup_processes)
        btn.setText(btn.text().replace('Stopping', 'Start').replace('...','').replace('Stop','Start'))
        btn.setStyleSheet(self.init_btn_style)
        btn.setEnabled(True)
        self.update_amount_processes()

    def toggle_close_script(self, btn: QPushButton, name, script_path, args):
        if name not in self.processes or self.processes[name].state() == QProcess.NotRunning:
            # Запуск процесса
            self.add_process(name, script_path, args)
            self.processes[name].finished.connect(lambda:self.base_close_btn_styling(btn))
            print(f"Скрипт {name} запущен с аргументами: {args}")
            self.update_amount_processes()
            btn.setText(btn.text().replace('Close', 'Closing...'))
            btn.setStyleSheet('background-color: #A6A600;')
        else:
            # Остановка процесса
            print(f"Скрипт {name} завершается...")
            self._safe_terminate_process(name, btn)
            print(f"Скрипт {name} завершен!")
    

    def base_close_btn_styling(self,btn):
        btn.setText(btn.text().replace('StopClose', 'Close').replace('...','').replace( 'Closing','Close'))
        btn.setStyleSheet(self.init_btn_style)
        btn.setEnabled(True)
        self.cleanup_processes()
        self.update_amount_processes()

    def _safe_terminate_process(self, name, btn):
        self.update_amount_processes()
        process = self.processes.get(name)
        if not process:
            return

        # 1. Пытаемся корректно завершить
        process.terminate()
        
        # 2. Ждём завершения с прогресс-баром
        btn.setEnabled(False)
        if 'Stop' in btn.text():
            btn.setText(btn.text().replace('Stop', 'Stopping')+'...')
        else:
            btn.setText(btn.text().replace('Closing...', 'StopClose'))

        
        if not process.waitForFinished(3000):  # 3 секунды на корректное завершение
            # 3. Принудительное завершение если не ответил
            process.kill()
            process.waitForFinished(1000)
        
        # 4. Финализация
        if name in self.processes:
            del self.processes[name]
        if 'Stopping' in btn.text():
            btn.setText(btn.text().replace('Stopping', 'Start').replace('...',''))
        else:
            btn.setText(btn.text().replace('StopClose', 'Close').replace('...',''))

        btn.setStyleSheet(self.init_btn_style)
        btn.setEnabled(True)
        self.update_amount_processes()

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        if not hasattr(self, 'processes') or not self.processes:
            event.accept()
            return
        
        # Создаем модальное окно с прогрессом
        progress = QProgressDialog("Closing processes...", "Force quit", 0, len(self.processes), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.show()
        
        QApplication.processEvents()  # Обновляем GUI
        
        # Последовательно завершаем все процессы
        for i, name in enumerate(list(self.processes.keys())):
            progress.setValue(i)
            progress.setLabelText(f"Stopping {name}...")
            QApplication.processEvents()
            
            process = self.processes[name]
            process.terminate()
            if not process.waitForFinished(2000):  # 2 секунды на каждый процесс
                process.kill()
                process.waitForFinished(500)
            
            if name in self.processes:
                del self.processes[name]
        
        progress.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QDialog, QFormLayout, QLineEdit, QMessageBox, QComboBox)
from PySide6.QtCore import Qt

import database
from generator import generate_new_demo


class CheckAnswerModal(QDialog):
    """The pop-up form where you enter your calculated final balances."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Submit Your Balances")
        self.setMinimumWidth(320)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        self.inputs = {
            "Cash": QLineEdit(),
            "Accounts Receivable": QLineEdit(),
            "Owner's Equity": QLineEdit(),
            "Sales Revenue": QLineEdit()
        }
        
        for account, line_edit in self.inputs.items():
            line_edit.setPlaceholderText("0.00")
            line_edit.setFixedHeight(28) 
            form_layout.addRow(QLabel(f"{account}:"), line_edit)
            
        layout.addLayout(form_layout)
        
        self.submit_btn = QPushButton("Check Against System")
        self.submit_btn.setFixedHeight(35)
        self.submit_btn.clicked.connect(self.accept)
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)

    def get_user_values(self):
        user_balances = {}
        for account, line_edit in self.inputs.items():
            text = line_edit.text().strip().replace(",", "")
            try:
                user_balances[account] = float(text) if text else 0.0
            except ValueError:
                user_balances[account] = 0.0
        return user_balances


class BalancingActApp(QMainWindow):
    """The main desktop window for BalancingAct."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BalancingAct - QuickBooks Practice Engine")
        self.resize(700, 550) # Bumped size up slightly to accommodate longer lists
        
        database.init_db()
        
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Difficulty Selector Top Bar
        top_bar_layout = QHBoxLayout()
        difficulty_label = QLabel("Select Difficulty Mode:")
        difficulty_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        
        self.difficulty_dropdown = QComboBox()
        self.difficulty_dropdown.addItems(["Easy", "Medium", "Hard", "Hardest"])
        self.difficulty_dropdown.setFixedHeight(30)
        self.difficulty_dropdown.setMinimumWidth(120)
        
        top_bar_layout.addWidget(difficulty_label)
        top_bar_layout.addWidget(self.difficulty_dropdown)
        top_bar_layout.addStretch() # Pushes everything to the left
        layout.addLayout(top_bar_layout)
        
        # Header / Instructions
        self.header_label = QLabel("Choose a level above and click 'New Demo' to generate practice transactions.")
        self.header_label.setStyleSheet("font-size: 13px; font-weight: bold; padding: 4px; margin-top: 5px;")
        self.header_label.setWordWrap(True)
        layout.addWidget(self.header_label)
        
        # Prompt Box Display
        self.prompt_display = QTextEdit()
        self.prompt_display.setReadOnly(True)
        self.prompt_display.setPlaceholderText("Your business scenario prompts will appear here...")
        self.prompt_display.setStyleSheet("font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; padding: 8px;")
        layout.addWidget(self.prompt_display)
        
        btn_layout = QHBoxLayout()
        
        self.new_demo_btn = QPushButton("New Demo")
        self.new_demo_btn.setFixedHeight(42)
        self.new_demo_btn.clicked.connect(self.handle_new_demo)
        btn_layout.addWidget(self.new_demo_btn)
        
        self.check_btn = QPushButton("Check Answer")
        self.check_btn.setFixedHeight(42)
        self.check_btn.setEnabled(False)
        self.check_btn.clicked.connect(self.handle_check_answer)
        btn_layout.addWidget(self.check_btn)
        
        layout.addLayout(btn_layout)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def handle_new_demo(self):
        # Read the currently active selection from our dropdown box
        selected_difficulty = self.difficulty_dropdown.currentText()
        
        prompts = generate_new_demo(selected_difficulty)
        formatted_text = "\n\n".join([f"• {p}" for p in prompts])
        self.prompt_display.setText(formatted_text)
        
        self.header_label.setText(f"[{selected_difficulty} Mode] Log these into QuickBooks, track ending balances, then check your answers:")
        self.check_btn.setEnabled(True)

    def handle_check_answer(self):
        modal = CheckAnswerModal(self)
        
        if modal.exec() == QDialog.Accepted:
            user_data = modal.get_user_values()
            correct_data = database.get_answer_key()
            
            report_lines = []
            all_correct = True
            
            for account in correct_data.keys():
                u_val = user_data[account]
                c_val = correct_data[account]
                
                if abs(u_val - c_val) < 0.01:
                    report_lines.append(f"✓ {account}: ${u_val:,.2f} (Correct!)")
                else:
                    all_correct = False
                    report_lines.append(f"✗ {account}:\n   Your input: ${u_val:,.2f}\n   QuickBooks should say: ${c_val:,.2f}")
            
            report_msg = "\n\n".join(report_lines)
            if all_correct:
                QMessageBox.information(self, "Perfect Score!", f"Excellent! Everything balances perfectly!\n\n{report_msg}")
            else:
                QMessageBox.warning(self, "Discrepancy Found", f"Not quite matching yet. Check your debits/credits:\n\n{report_msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: #1e1e24;
            color: #f5f5f7;
        }
        QLabel {
            color: #f5f5f7;
        }
        QComboBox {
            background-color: #2a2a32;
            color: #ffffff;
            border: 1px solid #4a4a56;
            border-radius: 4px;
            padding: 4px 8px;
        }
        QComboBox QAbstractItemView {
            background-color: #2a2a32;
            color: #ffffff;
            selection-background-color: #007acc;
        }
        QTextEdit {
            background-color: #121214;
            color: #e2e2e6;
            border: 1px solid #3a3a42;
            border-radius: 4px;
        }
        QLineEdit {
            background-color: #2a2a32;
            color: #ffffff;
            border: 1px solid #4a4a56;
            border-radius: 4px;
            padding: 4px;
        }
        QLineEdit:focus {
            border: 1px solid #007acc;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #0098ff;
        }
        QPushButton:disabled {
            background-color: #3a3a42;
            color: #7a7a85;
        }
    """)
    
    window = BalancingActApp()
    window.show()
    sys.argv = [""]
    sys.exit(app.exec())
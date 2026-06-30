import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QDialog, QFormLayout, QLineEdit, QMessageBox)
from PySide6.QtCore import Qt

# Import our engine modules from the previous step
import database
from generator import generate_new_demo


class CheckAnswerModal(QDialog):
    """The pop-up form where you enter your calculated final balances."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Submit Your Balances")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Create input boxes for each of the 4 core accounts
        self.inputs = {
            "Cash": QLineEdit(),
            "Accounts Receivable": QLineEdit(),
            "Owner's Equity": QLineEdit(),
            "Sales Revenue": QLineEdit()
        }
        
        # Format the inputs to look neat and add them to the form layout
        for account, line_edit in self.inputs.items():
            line_edit.setPlaceholderText("0.00")
            form_layout.addRow(QLabel(f"{account}:"), line_edit)
            
        layout.addLayout(form_layout)
        
        # Submit Button
        self.submit_btn = QPushButton("Check Against System")
        self.submit_btn.clicked.connect(self.accept) # Closes modal and returns success code
        layout.addWidget(self.submit_btn)
        
        self.setLayout(layout)

    def get_user_values(self):
        """Helper to convert the text box inputs safely into floats."""
        user_balances = {}
        for account, line_edit in self.inputs.items():
            text = line_edit.text().strip().replace(",", "")
            try:
                user_balances[account] = float(text) if text else 0.0
            except ValueError:
                user_balances[account] = 0.0 # Default to 0 if typing nonsense
        return user_balances


class BalancingActApp(QMainWindow):
    """The main desktop window for BalancingAct."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BalancingAct - QuickBooks Practice Engine")
        self.resize(600, 450)
        
        # Ensure database is set up on launch
        database.init_db()
        
        # Main Layout Setup
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Header / Instructions
        self.header_label = QLabel("Click 'New Demo' to generate QuickBooks practice transactions.")
        self.header_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        self.header_label.setWordWrap(True)
        layout.addWidget(self.header_label)
        
        # Prompt Box Display
        self.prompt_display = QTextEdit()
        self.prompt_display.setReadOnly(True)
        self.prompt_display.setPlaceholderText("Your business scenario prompts will appear here...")
        self.prompt_display.setStyleSheet("font-family: Consolas, Monaco, monospace; font-size: 13px; background-color: #f9f9f9;")
        layout.addWidget(self.prompt_display)
        
        # Control Buttons Panel
        btn_layout = QHBoxLayout()
        
        self.new_demo_btn = QPushButton("New Demo")
        self.new_demo_btn.setFixedHeight(40)
        self.new_demo_btn.clicked.connect(self.handle_new_demo)
        btn_layout.addWidget(self.new_demo_btn)
        
        self.check_btn = QPushButton("Check Answer")
        self.check_btn.setFixedHeight(40)
        self.check_btn.setEnabled(False) # Disabled until a demo is active
        self.check_btn.clicked.connect(self.handle_check_answer)
        btn_layout.addWidget(self.check_btn)
        
        layout.addLayout(btn_layout)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def handle_new_demo(self):
        """Triggers the engine to make new prompts and displays them."""
        prompts = generate_new_demo()
        
        # Format prompts as a clean bulleted list for reading
        formatted_text = "\n\n".join([f"• {p}" for p in prompts])
        self.prompt_display.setText(formatted_text)
        
        self.header_label.setText("Log the following transactions into QuickBooks, determine final balances, then click Check Answer:")
        self.check_btn.setEnabled(True)

    def handle_check_answer(self):
        """Pops open the entry modal and compares results."""
        modal = CheckAnswerModal(self)
        
        # execution pauses here until the user submits the modal
        if modal.exec() == QDialog.Accepted:
            user_data = modal.get_user_values()
            correct_data = database.get_answer_key()
            
            # Construct a clear, line-by-line breakdown report
            report_lines = []
            all_correct = True
            
            for account in correct_data.keys():
                u_val = user_data[account]
                c_val = correct_data[account]
                
                if abs(u_val - c_val) < 0.01: # Account for minor float rounding
                    report_lines.append(f"✓ {account}: ${u_val:,.2f} (Correct!)")
                else:
                    all_correct = False
                    report_lines.append(f"✗ {account}:\n   Your input: ${u_val:,.2f}\n   QuickBooks should say: ${c_val:,.2f}")
            
            # Show final report pop-up box
            report_msg = "\n\n".join(report_lines)
            if all_correct:
                QMessageBox.information(self, "Perfect Score!", f"Excellent! Everything balances perfectly!\n\n{report_msg}")
            else:
                QMessageBox.warning(self, "Discrepancy Found", f"Not quite matching yet. Check your debits/credits:\n\n{report_msg}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BalancingActApp()
    window.show()
    sys.argv = [""] # Safeguard for certain IDE environments
    sys.exit(app.exec())
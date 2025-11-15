from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTabWidget, QMessageBox
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import pyqtSignal

class AuthPage(QWidget):
    
    login_success = pyqtSignal(str)

    def __init__(self):
        super().__init__()


        layout = QVBoxLayout(self)
        
        # Tab system for Sign In / Register
        tab_widget = QTabWidget()
        
        # Sign In tab
        signin_widget = QWidget()
        signin_layout = QVBoxLayout(signin_widget)

        signin_layout.addStretch()
        self.signin_email = QLineEdit()
        self.signin_email.setPlaceholderText("Email")
        self.signin_password = QLineEdit()
        self.signin_password.setPlaceholderText("Password")
        self.signin_password.setEchoMode(QLineEdit.EchoMode.Password)
        signin_btn = QPushButton("Sign In")

        signin_layout.addWidget(self.signin_email)
        signin_layout.addWidget(self.signin_password)
        signin_layout.addWidget(signin_btn)
        signin_layout.addStretch()
        signin_layout.setSpacing(20)
    
        tab_widget.addTab(signin_widget, "Sign In")
        
        # Register tab
        register_widget = QWidget()
        register_layout = QVBoxLayout(register_widget)
        register_layout.addStretch()
        # Name field
        self.register_name = QLineEdit()
        self.register_name.setPlaceholderText("Full Name")
        register_layout.addWidget(self.register_name)
        
        # Email field
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Email")
        register_layout.addWidget(self.register_email)
        
        # Phone field
        self.register_phone = QLineEdit()
        self.register_phone.setPlaceholderText("Phone")
        register_layout.addWidget(self.register_phone)
        
        # Password field
        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Password")
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        register_layout.addWidget(self.register_password)
        
        # Register button
        register_btn = QPushButton("Register")

        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        register_layout.setSpacing(20)
        tab_widget.addTab(register_widget, "Register")
        
        layout.addWidget(tab_widget)
        # layout.addStretch()

        signin_btn.clicked.connect(self.handle_signin)
        register_btn.clicked.connect(self.handle_register)

    def handle_signin(self):
        email = self.signin_email.text()
        password = self.signin_password.text()
        
        query = QSqlQuery()
        query.prepare("SELECT user_id, role FROM Users WHERE email = ? AND password = ? AND is_active = 1")
        query.addBindValue(email)
        query.addBindValue(password)
        query.exec()

          # e.g., emit role or user_id
        
        if query.next():
            self.user_id = query.value(0)
            role = query.value(1)
            # QMessageBox.information(self, "Login Successful", f"Welcome! Role: {self.user_id}")
            self.login_success.emit(role)  # Emit signal with data
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect email or password or inactive account.")

    def handle_register(self):
        name = self.register_name.text()
        email = self.register_email.text()
        phone = self.register_phone.text()
        password = self.register_password.text()
        role = 'user'  # Or allow selection if you added that UI
        
        if not name or not email or not password or not phone:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO Users (name, email, phone, password, max_books, is_active, role) "
            "VALUES (?, ?, ?, ?, 3, 0, ?)"
        )
        query.addBindValue(name)
        query.addBindValue(email)
        query.addBindValue(phone)
        query.addBindValue(password)
        query.addBindValue(role)
        query.exec()
        
        if query.next:
            QMessageBox.information(self, "Request Sent", f"Ask Admin to approve your account\nemail: {email}")
            # You may want to auto log in or switch tab to sign in here
        else:
            QMessageBox.warning(self, "Registration failed: ", query.lastError().text())
            # print("Registration failed: ", query.lastError().text())

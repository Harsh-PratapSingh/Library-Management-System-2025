from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, 
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QDialog,
    QFormLayout, QSpinBox, QDialogButtonBox,
    QListView, QComboBox, QCheckBox
)
from PyQt6.QtCore import QDate
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt

class AdminPage(QWidget):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget(self)
        root_layout = QVBoxLayout(self)
        root_layout.addWidget(self.tab_widget)

        # Dashboard tab with a simple table
        dashboard_tab = QWidget()
        dash_layout = QVBoxLayout(dashboard_tab)

        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.stats_table.verticalHeader().setVisible(False)

        dash_layout.addWidget(self.stats_table)

        self.tab_widget.addTab(dashboard_tab, "Dashboard")
        
        #Books tab
        books_tab = QWidget()
        books_layout = QVBoxLayout(books_tab)

        # Add Book button
        add_book_btn = QPushButton("Add Book")
        add_book_btn.clicked.connect(self.add_book)
        books_layout.addWidget(add_book_btn)

        # Search row
        search_row = QHBoxLayout()
        search_label = QLabel("Search Books:")
        self.books_search_input = QLineEdit()
        self.books_search_input.setPlaceholderText("Search by title, author, or ISBN...")
        books_search_btn = QPushButton("Search")
        books_search_btn.clicked.connect(self.load_books)
        search_row.addWidget(search_label)
        search_row.addWidget(self.books_search_input)
        search_row.addWidget(books_search_btn)
        books_layout.addLayout(search_row)

        # Books table
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(9)
        self.books_table.setHorizontalHeaderLabels([
            "Book ID", "Title", "Author", "ISBN", "Category", 
            "Published Year", "Total Copies", "Available Copies", "Actions"
        ])
        self.books_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.books_table.verticalHeader().setVisible(False)
        books_layout.addWidget(self.books_table)

        self.tab_widget.addTab(books_tab, "Books")

        # Users tab
        users_tab = QWidget()
        users_layout = QVBoxLayout(users_tab)

        # Add User button
        add_user_btn = QPushButton("Add User")
        add_user_btn.clicked.connect(self.add_user)
        users_layout.addWidget(add_user_btn)

        # Search row
        users_search_row = QHBoxLayout()
        users_search_row.addWidget(QLabel("Search Users:"))
        self.users_search_input = QLineEdit()
        self.users_search_input.setPlaceholderText("Search by name, email, or phone...")
        users_search_btn = QPushButton("Search")
        users_search_btn.clicked.connect(self.load_users)
        users_search_row.addWidget(self.users_search_input)
        users_search_row.addWidget(users_search_btn)
        users_layout.addLayout(users_search_row)

        # Users table
        # Users table (single Actions column)
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(8)
        self.users_table.setHorizontalHeaderLabels([
            "User ID", "Name", "Email", "Phone", "Role", "Max Books", "Active", "Actions"
        ])
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.verticalHeader().setVisible(False)
        users_layout.addWidget(self.users_table)

        self.tab_widget.addTab(users_tab, "Users")

        #Issue Book tab
        issue_tab = QWidget()
        issue_layout = QVBoxLayout(issue_tab)

        # User email input
        email_row = QHBoxLayout()
        email_row.addWidget(QLabel("User Email:"))
        self.issue_user_email = QLineEdit()
        email_row.addWidget(self.issue_user_email)
        issue_layout.addLayout(email_row)

        # Book search
        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search Books:"))
        self.issue_book_search = QLineEdit()
        self.issue_book_search.setPlaceholderText("Search by title, author, or ISBN...")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.load_issue_books)
        search_row.addWidget(self.issue_book_search)
        search_row.addWidget(search_btn)
        issue_layout.addLayout(search_row)

        # Books table (no category column)
        self.issue_books_table = QTableWidget()
        self.issue_books_table.setColumnCount(7)
        self.issue_books_table.setHorizontalHeaderLabels([
            "Book ID", "Title", "Author", "ISBN", "Year", "Available", "Actions"
        ])
        self.issue_books_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.issue_books_table.verticalHeader().setVisible(False)
        issue_layout.addWidget(self.issue_books_table)

        self.tab_widget.addTab(issue_tab, "Issue Book")

        # Approve Book Request tab
        approve_tab = QWidget()
        approve_layout = QVBoxLayout(approve_tab)

        # Email search input
        appr_search_row = QHBoxLayout()
        appr_search_row.addWidget(QLabel("Search User:"))
        self.appr_email_input = QLineEdit()
        self.appr_email_input.setPlaceholderText("Search by user email...")
        appr_search_btn = QPushButton("Search")
        appr_search_btn.clicked.connect(self.load_pending_requests)
        appr_search_row.addWidget(self.appr_email_input)
        appr_search_row.addWidget(appr_search_btn)
        approve_layout.addLayout(appr_search_row)

        # Pending Transactions table
        self.pending_table = QTableWidget()
        self.pending_table.setColumnCount(8)
        self.pending_table.setHorizontalHeaderLabels([
            "Txn ID", "User", "Email", "Book", "ISBN", "Requested", "Status", "Actions"
        ])
        self.pending_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.pending_table.verticalHeader().setVisible(False)
        approve_layout.addWidget(self.pending_table)

        self.tab_widget.addTab(approve_tab, "Approve Issue Requests")

        # Return Book
        return_tab = QWidget()
        return_layout = QVBoxLayout(return_tab)

        # Email filter row
        ret_filter_row = QHBoxLayout()
        ret_filter_row.addWidget(QLabel("Search User:"))
        self.return_email_input = QLineEdit()
        self.return_email_input.setPlaceholderText("Search by user email...")
        self.return_only_overdue = QCheckBox("Show only overdue")
        ret_search_btn = QPushButton("Search")
        ret_search_btn.clicked.connect(self.load_return_txns)
        ret_filter_row.addWidget(self.return_email_input)
        ret_filter_row.addWidget(self.return_only_overdue)
        ret_filter_row.addWidget(ret_search_btn)
        return_layout.addLayout(ret_filter_row)

        # Return table
        self.return_table = QTableWidget()
        self.return_table.setColumnCount(10)
        self.return_table.setHorizontalHeaderLabels([
            "Txn ID", "User", "Email", "Book", "ISBN",
            "Issue", "Due", "Fine", "Status", "Actions"
        ])
        self.return_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.return_table.verticalHeader().setVisible(False)
        return_layout.addWidget(self.return_table)

        self.tab_widget.addTab(return_tab, "Return Book")

        tx_tab = QWidget()
        tx_layout = QVBoxLayout(tx_tab)

        # Email filter row
        tx_filter = QHBoxLayout()
        tx_filter.addWidget(QLabel("Search User:"))
        self.tx_email_input = QLineEdit()
        self.tx_email_input.setPlaceholderText("Leave empty to show all...")
        tx_search_btn = QPushButton("Search")
        tx_search_btn.clicked.connect(self.load_transactions)
        tx_filter.addWidget(self.tx_email_input)
        tx_filter.addWidget(tx_search_btn)
        tx_layout.addLayout(tx_filter)

        # Transactions table
        self.tx_table = QTableWidget()
        self.tx_table.setColumnCount(10)
        self.tx_table.setHorizontalHeaderLabels([
            "Txn ID", "User", "Email", "Book", "ISBN",
            "Issue", "Due", "Return", "Fine", "Status"
        ])
        self.tx_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tx_table.verticalHeader().setVisible(False)
        tx_layout.addWidget(self.tx_table)

        self.tab_widget.addTab(tx_tab, "Transactions")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        # Build + populate
        self.setup_dashboard()

        self.load_books()

        self.load_issue_books()

    def setup_dashboard(self):
        # Define rows (added Pending User Requests)
        metrics = [
            "Total Books",
            "Total Users",
            "Active Loans",
            "Overdue Loans",
            "Pending Book Requests",
            "Inactive Users "  # new
        ]
        self.stats_table.setRowCount(len(metrics))
        for r, name in enumerate(metrics):
            self.stats_table.setItem(r, 0, QTableWidgetItem(name))
            self.stats_table.setItem(r, 1, QTableWidgetItem("—"))

        # Inline query runner
        def run_count(sql, params=None):
            q = QSqlQuery()
            q.prepare(sql)
            if params:
                for p in params:
                    q.addBindValue(p)
            if not q.exec():
                return 0
            return int(q.value(0)) if q.next() and q.value(0) is not None else 0

        today = QDate.currentDate().toString("yyyy-MM-dd")

        # Execute counts
        total_books = run_count("SELECT COUNT(*) FROM Books")
        total_users = run_count("SELECT COUNT(*) FROM Users WHERE role = 'user'")
        active_loans = run_count("SELECT COUNT(*) FROM Transactions WHERE status = 'Issued'")
        overdue_loans = run_count(
            "SELECT COUNT(*) FROM Transactions WHERE status = 'Issued' AND due_date < ?", [today]
        )
        pending_txn_requests = run_count("SELECT COUNT(*) FROM Transactions WHERE status = 'Pending'")
        pending_user_requests = run_count("SELECT COUNT(*) FROM Users WHERE is_active = 0")

        values = [
            total_books,
            total_users,
            active_loans,
            overdue_loans,
            pending_txn_requests,
            pending_user_requests  # new value
        ]
        for r, val in enumerate(values):
            self.stats_table.setItem(r, 1, QTableWidgetItem(str(val)))

        self.stats_table.resizeColumnsToContents()

    def add_book(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Book")
        layout = QFormLayout(dialog)

        title_edit = QLineEdit()
        author_edit = QLineEdit()
        isbn_edit = QLineEdit()

        # Replace category_edit with CheckableComboBox
        categories_combo = CheckableComboBox()
        categories = [
            'Fiction', 'Non-Fiction', 'Mystery',
            'Science Fiction', 'Fantasy', 'Romance',
            'Thriller', 'Historical', 'Biography',
            'Children', 'Young Adult', 'Horror',
            'Adventure', 'Classic', 'Graphic Novel',
            'Poetry', 'Self-Help', 'Science',
            'History', 'Travel'
        ]
        for cat in categories:
            categories_combo.addItem(cat)

        year_spin = QSpinBox()
        year_spin.setRange(1000, 2100)
        total_copies_spin = QSpinBox()
        total_copies_spin.setRange(1, 100)

        layout.addRow("Title:", title_edit)
        layout.addRow("Author:", author_edit)
        layout.addRow("ISBN:", isbn_edit)
        layout.addRow("Category:", categories_combo)
        layout.addRow("Published Year:", year_spin)
        layout.addRow("Total Copies:", total_copies_spin)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addRow(button_box)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_categories = categories_combo.checked_items()
            category_value = ",".join(selected_categories)  # store as comma-separated string

            # Basic validation
            title = title_edit.text().strip()
            author = author_edit.text().strip()
            isbn = isbn_edit.text().strip()
            if not title or not author or not isbn or not category_value:
                QMessageBox.warning(self, "Invalid", "All fields including at least one category are required.")
                return

            query = QSqlQuery()
            query.prepare("""
                INSERT INTO Books (title, isbn, author, category, published_year, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """)
            query.addBindValue(title)
            query.addBindValue(isbn)
            query.addBindValue(author)
            query.addBindValue(category_value)
            query.addBindValue(year_spin.value())
            query.addBindValue(total_copies_spin.value())
            query.addBindValue(total_copies_spin.value())  # available = total initially

            if query.exec():
                QMessageBox.information(self, "Success", "Book added successfully!")
                self.load_books()
            else:
                QMessageBox.warning(self, "Error", f"Failed to add book: {query.lastError().text()}")
        
    def load_books(self):
        search_text = self.books_search_input.text().strip()
        sql = "SELECT book_id, title, author, isbn, category, published_year, total_copies, available_copies FROM Books WHERE 1=1"
        params = []

        if search_text:
            like_pattern = f"%{search_text}%"
            sql += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)"
            params.extend([like_pattern] * 3)

        sql += " ORDER BY title"

        query = QSqlQuery()
        query.prepare(sql)
        for p in params:
            query.addBindValue(p)

        if not query.exec():
            print("Failed to load books:", query.lastError().text())
            return

        self.books_table.clearContents()
        self.books_table.setRowCount(0)

        row = 0
        while query.next():
            self.books_table.insertRow(row)
            book_id = query.value(0)
            self.books_table.setItem(row, 0, QTableWidgetItem(str(book_id)))
            self.books_table.setItem(row, 1, QTableWidgetItem(query.value(1)))  # title
            self.books_table.setItem(row, 2, QTableWidgetItem(query.value(2)))  # author
            self.books_table.setItem(row, 3, QTableWidgetItem(query.value(3)))  # isbn
            self.books_table.setItem(row, 4, QTableWidgetItem(query.value(4)))  # category
            self.books_table.setItem(row, 5, QTableWidgetItem(str(query.value(5))))  # year
            self.books_table.setItem(row, 6, QTableWidgetItem(str(query.value(6))))  # total
            self.books_table.setItem(row, 7, QTableWidgetItem(str(query.value(7))))  # available

            # Actions column with Edit and Delete buttons
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, bid=book_id: self.edit_book(bid))
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, bid=book_id: self.delete_book(bid))

            # Simple horizontal layout for buttons (or use QHBoxLayout if needed)
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            self.books_table.setCellWidget(row, 8, action_widget)

            row += 1

        self.books_table.resizeColumnsToContents()

    def edit_book(self, book_id):
        # Locate row by book_id in column 0
        row = None
        for r in range(self.books_table.rowCount()):
            it = self.books_table.item(r, 0)
            if it and it.text() == str(book_id):
                row = r
                break
        if row is None:
            return

        # Fetch the action widget and the first button (Edit/Confirm)
        action_widget: QWidget = self.books_table.cellWidget(row, 8)
        btns = action_widget.findChildren(QPushButton)
        if not btns:
            return
        edit_btn: QPushButton = btns[0]
        is_confirm = edit_btn.text() == "Confirm"

        if not is_confirm:
            # Enter edit mode: make row items editable (cols 1..7)
            for col in range(1, 8):
                item = self.books_table.item(row, col)
                if not item:
                    continue
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.books_table.openPersistentEditor(item)
            edit_btn.setText("Confirm")

            # Optional: disable Delete while editing to avoid conflicts
            if len(btns) > 1:
                btns[1].setEnabled(False)
            # Optionally start editing first editable cell:
            # self.books_table.editItem(self.books_table.item(row, 1))
            return

        # Confirm: read values, validate, update DB
        title = self.books_table.item(row, 1).text().strip()
        author = self.books_table.item(row, 2).text().strip()
        isbn = self.books_table.item(row, 3).text().strip()
        category = self.books_table.item(row, 4).text().strip()
        year_txt = self.books_table.item(row, 5).text().strip()
        total_txt = self.books_table.item(row, 6).text().strip()
        avail_txt = self.books_table.item(row, 7).text().strip()

        # Basic validation
        if not title or not author or not isbn or not category:
            QMessageBox.warning(self, "Invalid", "Title, Author, ISBN, and Category are required.")
            return
        try:
            year_i = int(year_txt)
            total_i = int(total_txt)
            avail_i = int(avail_txt)
        except ValueError:
            QMessageBox.warning(self, "Invalid", "Published Year, Total Copies, and Available Copies must be integers.")
            return
        if year_i < 0 or total_i < 0 or avail_i < 0 or avail_i > total_i:
            QMessageBox.warning(self, "Invalid", "Copies must be non-negative and Available ≤ Total.")
            return

        # Update DB
        q = QSqlQuery()
        q.prepare("""
            UPDATE Books
            SET title=?, author=?, isbn=?, category=?, published_year=?, total_copies=?, available_copies=?
            WHERE book_id=?
        """)
        for v in (title, author, isbn, category, year_i, total_i, avail_i, book_id):
            q.addBindValue(v)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to update: {q.lastError().text()}")
            return

        # Exit edit mode: make row items read-only again, restore buttons
        for col in range(1, 8):
            item = self.books_table.item(row, col)
            if not item:
                continue
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.books_table.closePersistentEditor(item)

        edit_btn.setText("Edit")
        if len(btns) > 1:
            btns[1].setEnabled(True)

        self.load_books()

    def delete_book(self, book_id):
        reply = QMessageBox.question(
            self, "Confirm Delete", f"Delete book ID {book_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM Books WHERE book_id = ?")
            query.addBindValue(book_id)
            if query.exec():
                QMessageBox.information(self, "Success", "Book deleted!")
                self.load_books()  # Refresh
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete: {query.lastError().text()}")

    def load_users(self):
        search = self.users_search_input.text().strip()
        sql = """
            SELECT user_id, name, email, phone, role, max_books, is_active
            FROM Users
            WHERE 1=1 AND role = 'user'
        """
        params = []
        if search:
            like = f"%{search}%"
            sql += " AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)"
            params.extend([like, like, like])
        sql += " ORDER BY name"

        q = QSqlQuery()
        q.prepare(sql)
        for p in params:
            q.addBindValue(p)
        if not q.exec():
            print("Failed to load users:", q.lastError().text())
            return

        self.users_table.clearContents()
        self.users_table.setRowCount(0)

        row = 0
        while q.next():
            self.users_table.insertRow(row)
            user_id = q.value(0)
            name = q.value(1) or ""
            email = q.value(2) or ""
            phone = q.value(3) or ""
            role = q.value(4) or ""
            max_books = int(q.value(5) or 0)
            is_active = int(q.value(6) or 0)

            self.users_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(name))
            self.users_table.setItem(row, 2, QTableWidgetItem(email))
            self.users_table.setItem(row, 3, QTableWidgetItem(phone))
            self.users_table.setItem(row, 4, QTableWidgetItem(role))
            self.users_table.setItem(row, 5, QTableWidgetItem(str(max_books)))
            self.users_table.setItem(row, 6, QTableWidgetItem("Yes" if is_active else "No"))

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(6)

            status_btn = QPushButton("Deactivate" if is_active else "Activate")
            status_btn.setObjectName("btn_status")
            status_btn.clicked.connect(
                lambda _, uid=user_id, new_active=(0 if is_active else 1):
                    self.toggle_user_status(uid, new_active)
            )

            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("btn_edit")
            edit_btn.clicked.connect(lambda _, uid=user_id: self.edit_user(uid))

            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("btn_delete")
            delete_btn.clicked.connect(lambda _, uid=user_id: self.delete_user(uid))

            action_layout.addWidget(status_btn)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            self.users_table.setCellWidget(row, 7, action_widget)

            row += 1

        self.users_table.resizeColumnsToContents()

    def add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New User")
        form = QFormLayout(dialog)

        name_edit = QLineEdit()
        email_edit = QLineEdit()
        phone_edit = QLineEdit()

        role_combo = QComboBox()
        role_combo.addItems(["user", "admin"])

        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.EchoMode.Password)   # mask input
        confirm_edit = QLineEdit()
        confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)    # mask input

        form.addRow("Name:", name_edit)
        form.addRow("Email:", email_edit)
        form.addRow("Phone:", phone_edit)
        form.addRow("Role:", role_combo)
        form.addRow("Password:", password_edit)
        form.addRow("Confirm Password:", confirm_edit)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(dialog.accept)
        btns.rejected.connect(dialog.reject)
        form.addRow(btns)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        name = name_edit.text().strip()
        email = email_edit.text().strip()
        phone = phone_edit.text().strip()
        role = role_combo.currentText()
        pw = password_edit.text()
        pw2 = confirm_edit.text()

        if not name or not email or not phone or not pw:
            QMessageBox.warning(self, "Invalid", "Name, Email, Phone, and Password are required.")
            return
        if pw != pw2:
            QMessageBox.warning(self, "Invalid", "Passwords do not match.")
            return

        q = QSqlQuery()
        q.prepare("""
            INSERT INTO Users (name, email, phone, password, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        for v in (name, email, phone, pw, role, 1):  # is_active always true
            q.addBindValue(v)

        if q.exec():
            QMessageBox.information(self, "Success", "User added successfully!")
            self.load_users()
        else:
            QMessageBox.warning(self, "Error", f"Failed to add user: {q.lastError().text()}")

    def toggle_user_status(self, user_id, new_active):
        q = QSqlQuery()
        q.prepare("UPDATE Users SET is_active=? WHERE user_id=?")
        q.addBindValue(int(new_active))
        q.addBindValue(user_id)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to update status: {q.lastError().text()}")
            return
        self.load_users()

    def delete_user(self, user_id):
        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete user ID {user_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        q = QSqlQuery()
        q.prepare("DELETE FROM Users WHERE user_id=?")
        q.addBindValue(user_id)
        if q.exec():
            QMessageBox.information(self, "Success", "User deleted!")
            self.load_users()
        else:
            QMessageBox.warning(self, "Error", f"Failed to delete: {q.lastError().text()}")

    def edit_user(self, user_id):
        # find row
        row = None
        for r in range(self.users_table.rowCount()):
            it = self.users_table.item(r, 0)
            if it and it.text() == str(user_id):
                row = r
                break
        if row is None:
            return

        # Actions now at col 7
        action_widget = self.users_table.cellWidget(row, 7)
        if not isinstance(action_widget, QWidget):
            return

        edit_btn = action_widget.findChild(QPushButton, "btn_edit")
        del_btn = action_widget.findChild(QPushButton, "btn_delete")
        if not isinstance(edit_btn, QPushButton):
            return

        is_confirm = edit_btn.text() == "Confirm"

        if not is_confirm:
            # enter edit mode for Name, Email, Phone, Max Books
            for c in (1, 2, 3, 5):
                it = self.users_table.item(row, c)
                if it:
                    it.setFlags(it.flags() | Qt.ItemFlag.ItemIsEditable)
                    self.users_table.openPersistentEditor(it)

            edit_btn.setText("Confirm")
            if isinstance(del_btn, QPushButton):
                del_btn.setEnabled(False)
            return

        # confirm: read & validate
        name = self.users_table.item(row, 1).text().strip()
        email = self.users_table.item(row, 2).text().strip()
        phone = self.users_table.item(row, 3).text().strip()
        max_books_txt = self.users_table.item(row, 5).text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Invalid", "Name and Email are required.")
            return
        try:
            max_books_val = int(max_books_txt)
            if max_books_val < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid", "Max Books must be a non-negative integer.")
            return

        q = QSqlQuery()
        q.prepare("""
            UPDATE Users
            SET name=?, email=?, phone=?, max_books=?
            WHERE user_id=?
        """)
        for v in (name, email, phone, max_books_val, user_id):
            q.addBindValue(v)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to update: {q.lastError().text()}")
            return

        # exit edit mode
        for c in (1, 2, 3, 5):
            it = self.users_table.item(row, c)
            if it:
                it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.users_table.closePersistentEditor(it)

        edit_btn.setText("Edit")
        if isinstance(del_btn, QPushButton):
            del_btn.setEnabled(True)

        self.load_users()

    def load_issue_books(self):
        search = self.issue_book_search.text().strip()
        sql = """
            SELECT book_id, title, author, isbn, published_year, available_copies
            FROM Books
            WHERE 1=1
        """
        params = []
        if search:
            like = f"%{search}%"
            sql += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)"
            params.extend([like, like, like])
        sql += " ORDER BY title"

        q = QSqlQuery()
        q.prepare(sql)
        for p in params:
            q.addBindValue(p)
        if not q.exec():
            print("Failed to load books:", q.lastError().text())
            return

        self.issue_books_table.clearContents()
        self.issue_books_table.setRowCount(0)

        row = 0
        while q.next():
            self.issue_books_table.insertRow(row)
            book_id = q.value(0)
            title = q.value(1) or ""
            author = q.value(2) or ""
            isbn = q.value(3) or ""
            year = str(q.value(4) or "")
            avail = int(q.value(5) or 0)

            self.issue_books_table.setItem(row, 0, QTableWidgetItem(str(book_id)))
            self.issue_books_table.setItem(row, 1, QTableWidgetItem(title))
            self.issue_books_table.setItem(row, 2, QTableWidgetItem(author))
            self.issue_books_table.setItem(row, 3, QTableWidgetItem(isbn))
            self.issue_books_table.setItem(row, 4, QTableWidgetItem(year))
            self.issue_books_table.setItem(row, 5, QTableWidgetItem(str(avail)))

            # Actions cell
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(6)

            if avail > 0:
                issue_btn = QPushButton("Issue")
                issue_btn.clicked.connect(lambda _, bid=book_id: self.issue_book(bid))
                action_layout.addWidget(issue_btn)
            else:
                # no button when out of stock; optional label to indicate state
                unavailable = QLabel("Unavailable")
                action_layout.addWidget(unavailable)

            self.issue_books_table.setCellWidget(row, 6, action_widget)  # single composite widget per cell
            row += 1

        self.issue_books_table.resizeColumnsToContents()

    def issue_book(self, book_id: int):
        email = self.issue_user_email.text().strip()
        if not email:
            QMessageBox.warning(self, "Invalid", "Enter a user email first.")
            return

        # 1) Fetch user (id, active, max_books)
        q = QSqlQuery()
        q.prepare("SELECT user_id, is_active, max_books FROM Users WHERE email = ?")
        q.addBindValue(email)
        if not q.exec() or not q.next():
            QMessageBox.warning(self, "Not found", f"No user with email: {email}")
            return

        user_id = int(q.value(0))
        is_active = int(q.value(1) or 0)
        max_books = int(q.value(2) or 0)
        if not is_active:
            QMessageBox.warning(self, "Inactive", "User account is not active.")
            return

        # 2) Count current issued loans for user
        q2 = QSqlQuery()
        q2.prepare("SELECT COUNT(*) FROM Transactions WHERE user_id=? AND status='Issued'")
        q2.addBindValue(user_id)
        if not q2.exec() or not q2.next():
            QMessageBox.warning(self, "Error", "Failed to read user's loan count.")
            return
        active_loans = int(q2.value(0) or 0)
        if active_loans >= max_books:
            QMessageBox.warning(self, "Limit reached", f"User already has {active_loans}/{max_books} active loans.")
            return

        # 3) Check availability
        q3 = QSqlQuery()
        q3.prepare("SELECT available_copies FROM Books WHERE book_id=?")
        q3.addBindValue(book_id)
        if not q3.exec() or not q3.next():
            QMessageBox.warning(self, "Error", "Failed to read book availability.")
            return
        avail = int(q3.value(0) or 0)
        if avail <= 0:
            QMessageBox.warning(self, "Unavailable", "No copies available to issue.")
            return

        # 4) Compute dates
        today = QDate.currentDate()
        due = today.addDays(7)  # 2-week loan
        today_str = today.toString("yyyy-MM-dd")
        due_str = due.toString("yyyy-MM-dd")

        # 5) Insert transaction
        q4 = QSqlQuery()
        q4.prepare("""
            INSERT INTO Transactions (user_id, book_id, issue_date, due_date, status)
            VALUES (?, ?, ?, ?, 'Issued')
        """)
        for v in (user_id, book_id, today_str, due_str):
            q4.addBindValue(v)
        if not q4.exec():
            QMessageBox.warning(self, "Error", f"Failed to create transaction: {q4.lastError().text()}")
            return

        # 6) Decrement availability
        q5 = QSqlQuery()
        q5.prepare("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id=?")
        q5.addBindValue(book_id)
        if not q5.exec():
            QMessageBox.warning(self, "Warning", f"Issued, but failed to update inventory: {q5.lastError().text()}")

        QMessageBox.information(self, "Issued", f"Issued to {email} until {due_str}.")
        # Refresh table
        self.load_issue_books()

    def load_pending_requests(self):
        email = self.appr_email_input.text().strip()
        sql = """
            SELECT t.transaction_id, u.user_id, b.book_id,
                u.name, u.email, b.title, b.isbn,
                t.issue_date, t.status
            FROM Transactions t
            JOIN Users u ON t.user_id = u.user_id
            JOIN Books b ON t.book_id = b.book_id
            WHERE t.status = 'Pending'
        """
        params = []
        if email:
            sql += " AND u.email LIKE ?"
            params.append(f"%{email}%")
        sql += " ORDER BY t.transaction_id DESC"

        q = QSqlQuery()
        q.prepare(sql)
        for p in params:
            q.addBindValue(p)

        if not q.exec():
            print("Failed to load pending requests:", q.lastError().text())
            return

        self.pending_table.clearContents()
        self.pending_table.setRowCount(0)

        row = 0
        while q.next():
            self.pending_table.insertRow(row)
            txn_id = q.value(0)
            user_id = q.value(1)
            book_id = q.value(2)
            name = q.value(3) or ""
            em = q.value(4) or ""
            title = q.value(5) or ""
            isbn = q.value(6) or ""
            req_date = q.value(7) or "-"
            status = q.value(8) or "Pending"

            self.pending_table.setItem(row, 0, QTableWidgetItem(str(txn_id)))
            self.pending_table.setItem(row, 1, QTableWidgetItem(name))
            self.pending_table.setItem(row, 2, QTableWidgetItem(em))
            self.pending_table.setItem(row, 3, QTableWidgetItem(title))
            self.pending_table.setItem(row, 4, QTableWidgetItem(isbn))
            self.pending_table.setItem(row, 5, QTableWidgetItem(str(req_date)))
            self.pending_table.setItem(row, 6, QTableWidgetItem(status))

            actions = QWidget()
            h = QHBoxLayout(actions)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(6)

            issue_btn = QPushButton("Issue")
            issue_btn.clicked.connect(lambda _, tx=txn_id, uid=user_id, bid=book_id:
                                    self.approve_issue_request(tx, uid, bid))
            h.addWidget(issue_btn)

            reject_btn = QPushButton("Reject")  # <- new
            reject_btn.clicked.connect(lambda _, tx=txn_id: self.reject_issue_request(tx))  # <- new
            h.addWidget(reject_btn)  # <- new

            self.pending_table.setCellWidget(row, 7, actions)
            row += 1

        self.pending_table.resizeColumnsToContents()

    def approve_issue_request(self, txn_id: int, user_id: int, book_id: int):
        # 1) Check user is active and max_books not exceeded
        q1 = QSqlQuery()
        q1.prepare("SELECT is_active, max_books FROM Users WHERE user_id=?")
        q1.addBindValue(user_id)
        if not q1.exec() or not q1.next():
            QMessageBox.warning(self, "Error", "Failed to read user.")
            return
        is_active = int(q1.value(0) or 0)
        max_books = int(q1.value(1) or 0)
        if not is_active:
            QMessageBox.warning(self, "Inactive", "User account is not active.")
            return

        q2 = QSqlQuery()
        q2.prepare("SELECT COUNT(*) FROM Transactions WHERE user_id=? AND status='Issued'")
        q2.addBindValue(user_id)
        if not q2.exec() or not q2.next():
            QMessageBox.warning(self, "Error", "Failed to read user's active loans.")
            return
        active_loans = int(q2.value(0) or 0)
        if active_loans >= max_books:
            QMessageBox.warning(self, "Limit reached",
                                f"User already has {active_loans}/{max_books} active loans.")
            return

        # 2) Check availability
        q3 = QSqlQuery()
        q3.prepare("SELECT available_copies FROM Books WHERE book_id=?")
        q3.addBindValue(book_id)
        if not q3.exec() or not q3.next():
            QMessageBox.warning(self, "Error", "Failed to read book availability.")
            return
        avail = int(q3.value(0) or 0)
        if avail <= 0:
            QMessageBox.warning(self, "Unavailable", "No copies available to issue.")
            return

        # 3) Compute dates
        today = QDate.currentDate()
        due = today.addDays(7)
        today_s = today.toString("yyyy-MM-dd")
        due_s = due.toString("yyyy-MM-dd")

        # 4) Approve: update transaction and inventory
        q4 = QSqlQuery()
        q4.prepare("""
            UPDATE Transactions
            SET status='Issued', issue_date=?, due_date=?
            WHERE transaction_id=? AND status='Pending'
        """)
        q4.addBindValue(today_s)
        q4.addBindValue(due_s)
        q4.addBindValue(txn_id)
        if not q4.exec():
            QMessageBox.warning(self, "Error", f"Failed to approve: {q4.lastError().text()}")
            return

        q5 = QSqlQuery()
        q5.prepare("UPDATE Books SET available_copies = available_copies - 1 WHERE book_id=?")
        q5.addBindValue(book_id)
        if not q5.exec():
            QMessageBox.warning(self, "Warning", f"Approved, but failed to update inventory: {q5.lastError().text()}")

        QMessageBox.information(self, "Approved", f"Issue approved; due on {due_s}.")
        self.load_pending_requests()

    def reject_issue_request(self, txn_id: int):
        ans = QMessageBox.question(
            self,
            "Confirm Rejection",
            f"Reject and remove request #{txn_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if ans != QMessageBox.StandardButton.Yes:
            return

        q = QSqlQuery()
        q.prepare("""
            DELETE FROM Transactions
            WHERE transaction_id=? AND status='Pending'
        """)
        q.addBindValue(txn_id)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to remove request: {q.lastError().text()}")
            return

        QMessageBox.information(self, "Removed", f"Request #{txn_id} deleted.")
        self.load_pending_requests()

    def _update_overdues(self):
        FINE_PER_DAY = 10.00  # change as needed
        today = QDate.currentDate()
        today_s = today.toString("yyyy-MM-dd")

        # Select overdue candidates (Issued and due date < today)
        q = QSqlQuery()
        q.prepare("""
            SELECT transaction_id, due_date
            FROM Transactions
            WHERE status='Issued' AND due_date < ?
        """)
        q.addBindValue(today_s)
        if not q.exec():
            print("Failed to scan overdues:", q.lastError().text())
            return

        # Update each overdue with fine and status
        while q.next():
            txn_id = int(q.value(0))
            due_txt = q.value(1)
            due = QDate.fromString(due_txt, "yyyy-MM-dd")
            if not due.isValid():
                continue
            days_over = due.daysTo(today)
            if days_over <= 0:
                continue
            fine_val = round(days_over * FINE_PER_DAY, 2)

            q2 = QSqlQuery()
            q2.prepare("""
                UPDATE Transactions
                SET status='Overdue', fine=?
                WHERE transaction_id=? AND status='Issued'
            """)
            q2.addBindValue(fine_val)
            q2.addBindValue(txn_id)
            if not q2.exec():
                print("Failed to mark overdue:", q2.lastError().text())

    def load_return_txns(self):
        # First mark new overdues and compute fines
        self._update_overdues()

        email = self.return_email_input.text().strip()
        only_overdue = self.return_only_overdue.isChecked()

        # Base query for active loans
        sql = """
            SELECT t.transaction_id, u.name, u.email, b.title, b.isbn,
                t.issue_date, t.due_date, t.fine, t.status, b.book_id
            FROM Transactions t
            JOIN Users u ON t.user_id = u.user_id
            JOIN Books b ON t.book_id = b.book_id
            WHERE t.status IN ('Issued', 'Overdue')
        """
        params = []
        if email:
            sql += " AND u.email LIKE ?"
            params.append(f"%{email}%")
        if only_overdue:
            sql += " AND t.status = 'Overdue'"
        sql += " ORDER BY t.due_date ASC, t.transaction_id DESC"

        q = QSqlQuery()
        q.prepare(sql)
        for p in params:
            q.addBindValue(p)
        if not q.exec():
            print("Failed to load returns:", q.lastError().text())
            return

        self.return_table.clearContents()
        self.return_table.setRowCount(0)

        row = 0
        while q.next():
            self.return_table.insertRow(row)
            txn_id = q.value(0)
            name = q.value(1) or ""
            em = q.value(2) or ""
            title = q.value(3) or ""
            isbn = q.value(4) or ""
            issue_date = q.value(5) or ""
            due_date = q.value(6) or ""
            fine = q.value(7) or 0.0
            status = q.value(8) or ""
            book_id = q.value(9)

            self.return_table.setItem(row, 0, QTableWidgetItem(str(txn_id)))
            self.return_table.setItem(row, 1, QTableWidgetItem(name))
            self.return_table.setItem(row, 2, QTableWidgetItem(em))
            self.return_table.setItem(row, 3, QTableWidgetItem(title))
            self.return_table.setItem(row, 4, QTableWidgetItem(isbn))
            self.return_table.setItem(row, 5, QTableWidgetItem(str(issue_date)))
            self.return_table.setItem(row, 6, QTableWidgetItem(str(due_date)))
            self.return_table.setItem(row, 7, QTableWidgetItem(f"{float(fine):.2f}"))
            self.return_table.setItem(row, 8, QTableWidgetItem(status))

            act = QWidget()
            h = QHBoxLayout(act)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(6)

            ret_btn = QPushButton("Return")
            ret_btn.clicked.connect(lambda _, tx=txn_id, bid=book_id: self.return_book(tx, bid))
            h.addWidget(ret_btn)

            self.return_table.setCellWidget(row, 9, act)
            row += 1

        self.return_table.resizeColumnsToContents()

    def return_book(self, txn_id: int, book_id: int):
        today = QDate.currentDate()
        today_s = today.toString("yyyy-MM-dd")

        # Mark transaction as returned
        q = QSqlQuery()
        q.prepare("""
            UPDATE Transactions
            SET status='Returned', return_date=?
            WHERE transaction_id=? AND status IN ('Issued','Overdue')
        """)
        q.addBindValue(today_s)
        q.addBindValue(txn_id)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to mark returned: {q.lastError().text()}")
            return

        # Restore inventory
        q2 = QSqlQuery()
        q2.prepare("UPDATE Books SET available_copies = available_copies + 1 WHERE book_id=?")
        q2.addBindValue(book_id)
        if not q2.exec():
            QMessageBox.warning(self, "Warning", f"Returned, but inventory update failed: {q2.lastError().text()}")

        QMessageBox.information(self, "Returned", "Book successfully returned.")
        self.load_return_txns()

    def load_transactions(self):
        # Refresh overdue statuses/fines first
        self._update_overdues()

        email = self.tx_email_input.text().strip()

        sql = """
            SELECT t.transaction_id, u.name, u.email, b.title, b.isbn,
                t.issue_date, t.due_date, t.return_date, t.fine, t.status
            FROM Transactions t
            JOIN Users u ON t.user_id = u.user_id
            JOIN Books b ON t.book_id = b.book_id
            WHERE 1=1
        """
        params = []
        if email:
            sql += " AND u.email LIKE ?"
            params.append(f"%{email}%")
        sql += " ORDER BY t.transaction_id DESC"

        q = QSqlQuery()
        q.prepare(sql)
        for p in params:
            q.addBindValue(p)
        if not q.exec():
            print("Failed to load transactions:", q.lastError().text())
            return

        self.tx_table.clearContents()
        self.tx_table.setRowCount(0)

        row = 0
        while q.next():
            self.tx_table.insertRow(row)
            txn_id   = q.value(0)
            name     = q.value(1) or ""
            em       = q.value(2) or ""
            title    = q.value(3) or ""
            isbn     = q.value(4) or ""
            issue_dt = q.value(5) or ""
            due_dt   = q.value(6) or ""
            ret_dt   = q.value(7) or ""
            fine     = q.value(8) or 0.0
            status   = q.value(9) or ""

            self.tx_table.setItem(row, 0, QTableWidgetItem(str(txn_id)))
            self.tx_table.setItem(row, 1, QTableWidgetItem(name))
            self.tx_table.setItem(row, 2, QTableWidgetItem(em))
            self.tx_table.setItem(row, 3, QTableWidgetItem(title))
            self.tx_table.setItem(row, 4, QTableWidgetItem(isbn))
            self.tx_table.setItem(row, 5, QTableWidgetItem(str(issue_dt)))
            self.tx_table.setItem(row, 6, QTableWidgetItem(str(due_dt)))
            self.tx_table.setItem(row, 7, QTableWidgetItem(str(ret_dt) if ret_dt else "-"))
            self.tx_table.setItem(row, 8, QTableWidgetItem(f"{float(fine):.2f}"))
            self.tx_table.setItem(row, 9, QTableWidgetItem(status))

            row += 1

        self.tx_table.resizeColumnsToContents()


    def on_tab_changed(self, index):
    # Check if the current tab is the "My Books" tab
        if self.tab_widget.tabText(index) == "Dashboard":
            self.setup_dashboard()
        elif self.tab_widget.tabText(index) == "Books":
            self.load_books()
        elif self.tab_widget.tabText(index) == "Users":
            self.load_users()
        elif self.tab_widget.tabText(index) == "Issue Book":
            self.load_issue_books()
        elif self.tab_widget.tabText(index) == "Return Book":
            self.load_return_txns()
        elif self.tab_widget.tabText(index) == "Transactions":
            self.load_transactions()
    

class CheckableComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        self.setView(QListView(self))
        self.view().pressed.connect(self.handle_item_pressed)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        item.setData(data if data is not None else text)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.model().appendRow(item)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    def checked_items(self):
        checked = []
        for index in range(self.model().rowCount()):
            item = self.model().item(index)
            if item.checkState() == Qt.CheckState.Checked:
                checked.append(item.text())
        return checked
    
    def set_all_checked(self, checked=True):
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for i in range(self.model().rowCount()):
            self.model().item(i).setCheckState(state)


# Alright lets make the admin page using these tabs
# 1: Dashboard - Statistics widget showing total books, total users, active loans, overdue books, pending requests. 
# 2: Books - now this has a Add book button, and a search similar to user page without category, which will show the editable table, with columns for Edit and Delete button which will ask for conformation
# 3: Users - has a Add User button , again search with name, email, phone, which will show the editable button with a column for button to toggle status, which says "Activate" or "Deactivate", and another columns for Edit and Delete which will ask for conformation
# 4: Issue Book tab - has input field to input user email, and a search book and table without category option, with an extra Actions Column with Issue button
# 4: Transactions - has a search to view transaction table
# 5: Active Loans - add a search and a checkbox to show only overdue. this shows a table, with a column with Return button
# 6: Requests - has a sub tab for User, and Book, shows tables with columns with buttons to Approve or Deny
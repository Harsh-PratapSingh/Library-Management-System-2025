from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, 
    QPushButton, QHBoxLayout, QLineEdit, QLabel, QMessageBox, QDialog,
    QFormLayout, QSpinBox, QDialogButtonBox,
    QListView, QComboBox
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
        self.users_table.setColumnCount(7)
        self.users_table.setHorizontalHeaderLabels([
            "User ID", "Name", "Email", "Phone", "Role", "Active", "Actions"
        ])
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.verticalHeader().setVisible(False)
        users_layout.addWidget(self.users_table)

        self.tab_widget.addTab(users_tab, "Users")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        # Build + populate
        self.setup_dashboard()

        self.load_books()

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
            SELECT user_id, name, email, phone, role, is_active
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
            is_active = int(q.value(5) or 0)

            self.users_table.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(name))
            self.users_table.setItem(row, 2, QTableWidgetItem(email))
            self.users_table.setItem(row, 3, QTableWidgetItem(phone))
            self.users_table.setItem(row, 4, QTableWidgetItem(role))
            self.users_table.setItem(row, 5, QTableWidgetItem("Yes" if is_active else "No"))

            # Actions cell
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
            self.users_table.setCellWidget(row, 6, action_widget)

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

        # Actions widget in col 6
        action_widget = self.users_table.cellWidget(row, 6)
        if not isinstance(action_widget, QWidget):
            return

        edit_btn = action_widget.findChild(QPushButton, "btn_edit")
        del_btn = action_widget.findChild(QPushButton, "btn_delete")
        if not isinstance(edit_btn, QPushButton):
            return

        is_confirm = edit_btn.text() == "Confirm"

        if not is_confirm:
            # enter edit mode for Name, Email, Phone
            for c in (1, 2, 3):
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
        if not name or not email:
            QMessageBox.warning(self, "Invalid", "Name and Email are required.")
            return

        q = QSqlQuery()
        q.prepare("""
            UPDATE Users
            SET name=?, email=?, phone=?
            WHERE user_id=?
        """)
        for v in (name, email, phone, user_id):
            q.addBindValue(v)
        if not q.exec():
            QMessageBox.warning(self, "Error", f"Failed to update: {q.lastError().text()}")
            return

        # exit edit mode
        for c in (1, 2, 3):
            it = self.users_table.item(row, c)
            if it:
                it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.users_table.closePersistentEditor(it)

        edit_btn.setText("Edit")
        if isinstance(del_btn, QPushButton):
            del_btn.setEnabled(True)

        self.load_users()


    def on_tab_changed(self, index):
    # Check if the current tab is the "My Books" tab
        if self.tab_widget.tabText(index) == "Dashboard":
            self.setup_dashboard()
        elif self.tab_widget.tabText(index) == "Books":
            self.load_books()
        elif self.tab_widget.tabText(index) == "Users":
            self.load_users()

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
# 4: Transactions - has a Issue Book button, has a search to view transaction table
# 5: Active Loans - add a search and a checkbox to show only overdue. this shows a table, with a column with Return button
# 6: Requests - has a sub tab for User, and Book, shows tables with columns with buttons to Approve or Deny
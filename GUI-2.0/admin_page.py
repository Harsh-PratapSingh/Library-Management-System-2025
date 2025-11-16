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
        books_layout.addWidget(self.books_table)

        self.tab_widget.addTab(books_tab, "Books")

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
            "Pending User Requests"  # new
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


    def on_tab_changed(self, index):
    # Check if the current tab is the "My Books" tab
        if self.tab_widget.tabText(index) == "Dashboard":
            self.setup_dashboard()
        elif self.tab_widget.tabText(index) == "Books":
            self.load_books()
        # elif self.tab_widget.tabText(index) == "Profile And History":
        #     self.load_profile_and_history()

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
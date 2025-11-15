from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QComboBox, QListView, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from datetime import datetime, timedelta

class UserPage(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        layout = QVBoxLayout(self)
        
        # Tab system for user features
        self.tab_widget = QTabWidget()
        
        # Tab 1: Search and Browse Books
        search_tab = QWidget()
        search_layout = QVBoxLayout(search_tab)
        
        # Search bar
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title, author, or ISBN...")
        search_btn = QPushButton("Search")
        search_row.addWidget(self.search_input)
        search_row.addWidget(search_btn)
        search_layout.addLayout(search_row)
        
        # Filter by category
        filter_row = QHBoxLayout()
        filter_label = QLabel("Category:")
        self.category_combo = CheckableComboBox()
        categories = ['Fiction', 'Non-Fiction', 'Mystery',
          'Science Fiction', 'Fantasy', 'Romance',
          'Thriller', 'Historical', 'Biography',
          'Children', 'Young Adult', 'Horror',
          'Adventure', 'Classic', 'Graphic Novel',
          'Poetry', 'Self-Help', 'Science',
          'History', 'Travel']
        for cat in categories:
            self.category_combo.addItem(cat)

        self.toggle_btn = QPushButton("Select All")
        self.toggle_btn.clicked.connect(self.handle_select_toggle)

        filter_row.addWidget(filter_label)
        filter_row.addWidget(self.toggle_btn)
        filter_row.addWidget(self.category_combo)
        

        search_layout.addLayout(filter_row)
        
        # Search results placeholder
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)  # Title, Author, ISBN, Categories, Copies
        self.results_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Categories", "Available Copies", "Borrow"])
        header = self.results_table.horizontalHeader()
        for i in range(self.results_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        search_layout.addWidget(self.results_table)
        
        # Connect search button
        search_btn.clicked.connect(self.perform_search)

        self.tab_widget.addTab(search_tab, "Search And Browse Books")
        

        # Tab 2: My Books
        my_books_tab = QWidget()
        my_books_layout = QVBoxLayout(my_books_tab)
        
        self.my_books_table = QTableWidget()
        self.my_books_table.setColumnCount(7)
        self.my_books_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Category", "Issue Date", "Due Date", "Status"])
        my_books_layout.addWidget(self.my_books_table)

        self.tab_widget.addTab(my_books_tab, "My Books")
        
        # Tab 3: User Profile and History
        profile_tab = QWidget()
        profile_layout = QVBoxLayout(profile_tab)

        # Profile info section
        profile_info_layout = QHBoxLayout()
        profile_info_layout.addWidget(QLabel("Name:"))
        self.profile_name_label = QLabel()
        profile_info_layout.addWidget(self.profile_name_label)
        profile_info_layout.addStretch()

        profile_info_layout.addWidget(QLabel("Email:"))
        self.profile_email_label = QLabel()
        profile_info_layout.addWidget(self.profile_email_label)
        profile_info_layout.addStretch()

        profile_info_layout.addWidget(QLabel("Member Since:"))
        self.profile_join_date_label = QLabel()
        profile_info_layout.addWidget(self.profile_join_date_label)
        profile_info_layout.addStretch()

        profile_layout.addLayout(profile_info_layout)

        # Transaction history table
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(8)  # transaction_id, title, issue_date, due_date, return_date, fine, status, book_id
        self.transactions_table.setHorizontalHeaderLabels(["Transaction ID", "Title", "Issue Date", "Due Date", "Return Date", "Fine", "Status", "Book ID"])
        header = self.transactions_table.horizontalHeader()
        for i in range(self.transactions_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        profile_layout.addWidget(QLabel("Transaction History:"))
        profile_layout.addWidget(self.transactions_table)

        self.tab_widget.addTab(profile_tab, "Profile And History")
        
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        layout.addWidget(self.tab_widget)
        # layout.addStretch()

    def handle_select_toggle(self):
        if self.toggle_btn.text() == "Select All":
            self.category_combo.set_all_checked(True)
            self.toggle_btn.setText("Deselect All")
        else:
            self.category_combo.set_all_checked(False)
            self.toggle_btn.setText("Select All")

    def perform_search(self):
        search_text = self.search_input.text().strip()
        selected_categories = self.category_combo.checked_items()

        sql = "SELECT book_id, title, author, isbn, category, available_copies FROM Books WHERE 1=1"
        params = []

        if search_text:
            like_pattern = f"%{search_text}%"
            sql += " AND (title LIKE ? OR author LIKE ? OR isbn LIKE ?)"
            params.extend([like_pattern] * 3)

        if selected_categories:
            sql += " AND ("
            cat_clauses = []
            for _ in selected_categories:
                cat_clauses.append("category LIKE ?")
                params.append(f"%{_}%")
            sql += " OR ".join(cat_clauses)
            sql += ")"

        query = QSqlQuery()
        query.prepare(sql)
        for p in params:
            query.addBindValue(p)

        if not query.exec():
            print("Search failed: ", query.lastError().text())
            return

        self.results_table.clearContents()
        self.results_table.setRowCount(0)

        row = 0
        while query.next():
            self.results_table.insertRow(row)
            self.results_table.setItem(row, 0, QTableWidgetItem(query.value(1)))  # title
            self.results_table.setItem(row, 1, QTableWidgetItem(query.value(2)))  # author
            self.results_table.setItem(row, 2, QTableWidgetItem(query.value(3)))  # isbn
            self.results_table.setItem(row, 3, QTableWidgetItem(query.value(4)))  # category
            self.results_table.setItem(row, 4, QTableWidgetItem(str(query.value(5))))  # available copies

            book_id = query.value(0)  # proper book_id now
            copies_available = query.value(5)

            borrow_btn = QPushButton("Borrow")
            borrow_btn.clicked.connect(lambda _, bid=book_id: self.borrow_book(bid))
            
            # Disable button if no copies available
            if copies_available == 0:
                borrow_btn.setEnabled(False)

            self.results_table.setCellWidget(row, 5, borrow_btn)
            row += 1

        self.results_table.resizeColumnsToContents()
        print(f"Found {row} book(s)")

    def borrow_book(self, book_id):

        # Prepare dates
        issue_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')  # 2 weeks loan
        return_date = None
        fine = 0.0
        status = 'Pending'

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO Transactions 
            (book_id, user_id, issue_date, due_date, return_date, fine, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(book_id)
        query.addBindValue(self.user_id)
        query.addBindValue(issue_date)
        query.addBindValue(due_date)
        query.addBindValue(return_date)
        query.addBindValue(fine)
        query.addBindValue(status)

        if query.exec():
            QMessageBox.information(self, "Request Sent", "Your borrow request has been sent for approval.")
        else:
            QMessageBox.warning(self, "Failed", "Could not send borrow request: " + query.lastError().text())

    def load_my_books(self):
        if not self.user_id:
            return

        sql = """
            SELECT Books.title, Books.author, Books.isbn, Books.category, Transactions.issue_date, Transactions.due_date, Transactions.status
            FROM Transactions
            JOIN Books ON Transactions.book_id = Books.book_id
            WHERE Transactions.user_id = ?
            AND Transactions.status IN ('Pending', 'Issued')
        """

        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(self.user_id)

        if not query.exec():
            print("Failed to load user books:", query.lastError().text())
            return

        self.my_books_table.clearContents()
        self.my_books_table.setRowCount(0)

        row = 0
        while query.next():
            self.my_books_table.insertRow(row)
            self.my_books_table.setItem(row, 0, QTableWidgetItem(query.value(0)))  # title
            self.my_books_table.setItem(row, 1, QTableWidgetItem(query.value(1)))  # author
            self.my_books_table.setItem(row, 2, QTableWidgetItem(query.value(2)))  # isbn
            self.my_books_table.setItem(row, 3, QTableWidgetItem(query.value(3)))  # category
            self.my_books_table.setItem(row, 4, QTableWidgetItem(query.value(4)))  # issue_date
            self.my_books_table.setItem(row, 5, QTableWidgetItem(query.value(5)))  # due_date
            self.my_books_table.setItem(row, 6, QTableWidgetItem(query.value(6)))  # status
            row += 1

        self.my_books_table.resizeColumnsToContents()

    def load_profile_and_history(self):
        if not self.user_id:
            return
            
        # Load user profile info
        query = QSqlQuery()
        query.prepare("SELECT name, email, join_date FROM Users WHERE user_id = ?")
        query.addBindValue(self.user_id)
        if query.exec() and query.next():
            self.profile_name_label.setText(query.value(0))
            self.profile_email_label.setText(query.value(1))
            self.profile_join_date_label.setText(query.value(2))
        
        # Load all transactions for this user
        sql = """
            SELECT Transactions.transaction_id, Books.title, Transactions.issue_date, 
                Transactions.due_date, Transactions.return_date, Transactions.fine, 
                Transactions.status, Transactions.book_id
            FROM Transactions
            JOIN Books ON Transactions.book_id = Books.book_id
            WHERE Transactions.user_id = ?
            ORDER BY Transactions.issue_date DESC
        """
        query.prepare(sql)
        query.addBindValue(self.user_id)
        
        if not query.exec():
            print("Failed to load transaction history:", query.lastError().text())
            return
        
        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        
        row = 0
        while query.next():
            self.transactions_table.insertRow(row)
            self.transactions_table.setItem(row, 0, QTableWidgetItem(str(query.value(0))))  # transaction_id
            self.transactions_table.setItem(row, 1, QTableWidgetItem(query.value(1)))  # title
            self.transactions_table.setItem(row, 2, QTableWidgetItem(query.value(2)))  # issue_date
            self.transactions_table.setItem(row, 3, QTableWidgetItem(query.value(3)))  # due_date
            self.transactions_table.setItem(row, 4, QTableWidgetItem(str(query.value(4) if query.value(4) else "")))  # return_date
            self.transactions_table.setItem(row, 5, QTableWidgetItem(str(query.value(5))))  # fine
            self.transactions_table.setItem(row, 6, QTableWidgetItem(query.value(6)))  # status
            self.transactions_table.setItem(row, 7, QTableWidgetItem(str(query.value(7))))  # book_id
            row += 1
        
        self.transactions_table.resizeColumnsToContents()

    def on_tab_changed(self, index):
    # Check if the current tab is the "My Books" tab
        if self.tab_widget.tabText(index) == "My Books":
            self.load_my_books()
        elif self.tab_widget.tabText(index) == "Search And Browse Books":
            self.perform_search()
        elif self.tab_widget.tabText(index) == "Profile And History":
            self.load_profile_and_history()

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
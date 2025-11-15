from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QComboBox, QListView, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

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
        search_layout.addWidget(self.results_table)
        
        # Connect search button
        search_btn.clicked.connect(self.perform_search)

        self.tab_widget.addTab(search_tab, "Search And Browse Books")
        
        # Tab 2: My Books
        my_books_tab = QWidget()
        my_books_layout = QVBoxLayout(my_books_tab)
        my_books_layout.addWidget(QLabel("Your borrowed books will appear here"))
        self.tab_widget.addTab(my_books_tab, "My Books")
        
        # Tab 3: User Profile and History
        profile_tab = QWidget()
        profile_layout = QVBoxLayout(profile_tab)
        profile_layout.addWidget(QLabel("Profile and transaction history will appear here"))
        self.tab_widget.addTab(profile_tab, "Profile And History")
        
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
            # Skip book_id in table, starts at col 1 for title
            self.results_table.setItem(row, 0, QTableWidgetItem(query.value(1)))  # title
            self.results_table.setItem(row, 1, QTableWidgetItem(query.value(2)))  # author
            self.results_table.setItem(row, 2, QTableWidgetItem(query.value(3)))  # isbn
            self.results_table.setItem(row, 3, QTableWidgetItem(query.value(4)))  # category
            self.results_table.setItem(row, 4, QTableWidgetItem(str(query.value(5))))  # available copies

            book_id = query.value(0)  # proper book_id now

            borrow_btn = QPushButton("Borrow")
            borrow_btn.clicked.connect(lambda _, bid=book_id: self.borrow_book(bid))
            self.results_table.setCellWidget(row, 5, borrow_btn)
            row += 1

        print(f"Found {row} book(s)")

    def borrow_book(self, book_id):
        print(f"Borrow button clicked for book_id: {book_id}")
        # Placeholder for borrowing logic

        
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
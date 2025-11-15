from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QDate
from PyQt6.QtSql import QSqlQuery

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
        self.stats_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.stats_table.verticalHeader().setVisible(False)
        self.stats_table.horizontalHeader().setStretchLastSection(True)

        dash_layout.addWidget(self.stats_table)

        self.tab_widget.addTab(dashboard_tab, "Dashboard")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        # Build + populate
        self.setup_dashboard()

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


    def on_tab_changed(self, index):
    # Check if the current tab is the "My Books" tab
        if self.tab_widget.tabText(index) == "Dashboard":
            self.setup_dashboard()
        # elif self.tab_widget.tabText(index) == "Search And Browse Books":
        #     self.perform_search()
        # elif self.tab_widget.tabText(index) == "Profile And History":
        #     self.load_profile_and_history()
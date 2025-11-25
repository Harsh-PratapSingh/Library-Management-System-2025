# Library-Management-System-2025
A comprehensive Python-based desktop application for managing library operations with a modern PyQt6 GUI and SQLite database backend.

Features

📊 Dashboard
Real-time statistics overview:

Total books in collection

Total registered users

Active loans count

Overdue loans tracking

Pending book requests

Pending user approval requests

📚 Books Management
Add Books: Register new books with title, author, ISBN, category, publication year, and copy count

Edit Books: Modify book details inline with validation

Delete Books: Remove books from collection with confirmation

Search: Find books by title, author, or ISBN

Category Management: Multi-select categories using checkable combo boxes

Inventory Tracking: Automatic tracking of total vs. available copies

👥 User Management
Add Users: Register new users with name, email, phone, password, and role

Edit Users: Update user details including max books limit

Activate/Deactivate: Toggle user account status

Delete Users: Remove users with confirmation

Search: Find users by name, email, or phone

Role-based Access: Separate admin and user roles

Max Books Limit: Configurable per-user loan limits

📖 Issue Books
Direct Issuance: Issue books immediately to active users

Availability Check: Ensures books are in stock before issuance

Loan Limit Validation: Respects per-user max books limit

Due Date Calculation: Automatically sets return dates (7-day default)

✅ Approve Issue Requests
Pending Requests Queue: View all pending book requests

Email Filtering: Search requests by user email

Issue Approval: Approve requests with auto-decrement of inventory

Request Rejection: Reject and delete pending requests

Validation: Checks user status and loan limits before approval

🔄 Return Books
Active Loans View: Shows all issued and overdue books

Overdue Detection: Automatically marks loans as overdue when due date passes

Fine Calculation: Computes fines based on days overdue (configurable rate)

Return Processing: Marks books as returned and restores inventory

Email Filtering: Filter by user email

Overdue-only Filter: Show only overdue items

📋 Transactions History
Complete Audit Trail: View all transactions with full details

Email Search: Filter transactions by user email

Overdue Refresh: Auto-updates overdue status and fines

Status Tracking: Shows Issued, Overdue, Returned, and Denied statuses

Installation
Prerequisites
Python 3.8 or higher

Git



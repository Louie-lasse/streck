import sqlite3
import signal
import sys
from datetime import datetime, timedelta, timezone

class DatabaseHandler:
    """A class to manage SQLite database interactions using a context manager."""

    def __init__(self, db_path="streck/streck.db"):
        """Initialize the database handler with the database file path."""
        self.db_path = db_path
        self.conn, self.cursor = None, None

        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def __enter__(self):
        """Enter the context: open the database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the context: close the database connection."""
        if self.conn:
            self.conn.close()

    def execute_query(self, query, params=(), commit=True):
        """
        Execute a query against the database within a context.
        Args:
            query (str): The SQL query to execute.
            params (tuple): Parameters to bind to the query.
            commit (bool): Whether to commit the changes.
        Returns:
            list: Query results (if applicable).
        """
        with self as db:
            try:
                db.cursor.execute(query, params)
                if commit:
                    db.conn.commit()
                return db.cursor.fetchall()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return None

    def execute_command(self, command, params=(), commit=True):
        """
        Execute a non-SELECT command (INSERT, UPDATE, DELETE) against the database.
        
        Args:
            command (str): The SQL command to execute (INSERT, UPDATE, DELETE, etc.).
            params (tuple): Parameters to bind to the command.
            commit (bool): Whether to commit the changes.

        Returns:
            int: Number of rows affected by the command, or -1 if an error occurred.
        """
        with self as db:
            try:
                db.cursor.execute(command, params)
                if commit:
                    db.conn.commit()
                return db.cursor.rowcount  # Number of affected rows
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                return -1


    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals (e.g., CTRL+C) to close the database connection."""
        print("\nShutting down db gracefully...")
        sys.exit(0)

    def get_recent_users(self, n_minutes = 60):
        """
        Get recently active users from the database
        """

        query = "SELECT name FROM Transactions JOIN Users U on user=U.id WHERE added >= ? GROUP BY name"
        time_span_utc = datetime.now(timezone.utc) - timedelta(minutes=n_minutes)
        time_span_str = time_span_utc.strftime('%Y-%m-%d %H:%M:%S')
        res = self.execute_query(query, (time_span_str,))
        return res or []
    
    def get_user(self, slack_id):
        """
        Gets the users actual database id for identification and interaction with the database
        """
        query = "SELECT id, name FROM Users U where slack_id=?"
        res = self.execute_query(query, (slack_id,))
        return res[0] if res else (None,None)
    
    def remove_slack(self, db_id):
        """
        Clears a bd user of slack_id.
        """
        q = "UPDATE Users SET slack_id=NULL WHERE id = ?"
        res = self.execute_command(q, (db_id,))
        return 0 if res <= 0 else res
    
    def purchase(self, db_id, product, price):
        """
        Adds a transaction to a user
        """
        query = 'INSERT into transactions values (null, datetime("now", "-1 day"), ?, ?, ?, ?)'
        res = self.execute_command(query, (db_id, product, price, ''))
        return 0 if res <= 0 else res
    
    def get_price(self, product):
        """
        Finds the price of a product 
        """
        query = "Select price from products where id = ?"
        res = self.execute_query(query, (product,))
        return res[0][0] if res else 0
    
    def list_users(self, n=5):
        """
        Returns the `n` most recently added users.
        Default 5
        """
        query = "SELECT id, name FROM Users ORDER BY id DESC LIMIT ?"
        res = self.execute_query(query, (n,))
        return reversed(res)
    
    def save_image(self, user, file_name):
        """
        Saves a filename to the db under a specified user
        """
        query = "UPDATE users SET image = ? WHERE id = ?"
        res = self.execute_command(query, (file_name, user))
        return 0 if res <= 0 else res

    def connect_user(self, db_id, slack_id):
        """
        Connects a slack account to a db user
        """
        query = "UPDATE users SET slack_id = ? WHERE id = ?"
        res = self.execute_command(query, (slack_id, db_id))
        if res <= 0:
            return None
        q2 = "SELECT name FROM Users WHERE id = ?"
        res = self.execute_query(q2, (db_id,))
        return res[0]

    def get_debt(self, db_id):
        """
        Get the current debt of a specified user
        """
        query = "SELECT sum(t.price) FROM transactions t WHERE user = ?"
        res = self.execute_query(query, (db_id,))
        return res[0][0] if res else None
    
    def get_all_debts(self):
        query = """
            SELECT u.name, u.slack_id, sum(t.price) AS skuld
            FROM users u
            JOIN transactions t ON t.user = u.id
            GROUP BY u.name
            ORDER BY skuld desc;
            """
        return self.execute_query(query, ())
    
    def add_user(self, code, name):
        """
        Adds a user to the database
        """
        query = "INSERT INTO users VALUES (null, ?, 1, ?, null, null, null)"
        res = self.execute_command(query, (code, name))
        return 0 if res <= 0 else res
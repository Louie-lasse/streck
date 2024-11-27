import sqlite3
import signal
import sys
from datetime import datetime, timedelta, timezone

class DatabaseHandler:
    """A class to manage SQLite database interactions using a context manager."""

    def __init__(self, db_path="tasks.db"):
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

    def _handle_shutdown(self, signum, frame):
        """Handle shutdown signals (e.g., CTRL+C) to close the database connection."""
        print("\nShutting down gracefully...")
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
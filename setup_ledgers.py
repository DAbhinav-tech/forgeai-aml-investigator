import sqlite3
import random
import uuid
from datetime import datetime, timedelta

def setup_db(db_name):
    """Creates a database and transaction table for a bank."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            tx_id TEXT PRIMARY KEY,
            sender_id TEXT,
            receiver_id TEXT,
            amount REAL,
            timestamp TEXT,
            flagged INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

def insert_transaction(conn, sender, receiver, amount, timestamp):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (tx_id, sender_id, receiver_id, amount, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (str(uuid.uuid4()), sender, receiver, amount, timestamp))
    conn.commit()

# 1. Initialize Ledgers
bank_a = setup_db('bank_a.db')
bank_b = setup_db('bank_b.db')

base_time = datetime.now() - timedelta(days=30)

# 2. Generate Normal "Noise" Transactions
print("Generating normal transaction data...")
for _ in range(50):
    amount = round(random.uniform(10.0, 500.0), 2)
    t_time = (base_time + timedelta(days=random.randint(0, 25))).isoformat()
    # Random transfers within Bank A
    insert_transaction(bank_a, f"user_A{random.randint(1,5)}", f"user_A{random.randint(1,5)}", amount, t_time)

# 3. Inject Money Laundering Pattern: "Structuring" (Smurfing)
# Sending amounts just under the $10,000 reporting threshold rapidly across banks
print("Injecting AML structuring pattern...")
fraud_sender = "user_A_suspect"
fraud_receiver = "user_B_shady_corp"

# 3 rapid transfers of $9,500 from Bank A to Bank B to avoid a $10k flag
for i in range(3):
    fraud_time = (datetime.now() - timedelta(hours=i)).isoformat()
    # Deduct from Bank A
    insert_transaction(bank_a, fraud_sender, "External_Bank_B", 9500.00, fraud_time)
    # Receive in Bank B
    insert_transaction(bank_b, "External_Bank_A", fraud_receiver, 9500.00, fraud_time)

print("✅ Setup complete! Created bank_a.db and bank_b.db with mock ledgers.")
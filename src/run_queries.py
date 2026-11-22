"""Print each sample analytics query with its result set."""
from pathlib import Path
import sqlite3
from setup_db import DB_PATH, create_db

ROOT = Path(__file__).resolve().parents[1]

def main():
    create_db()
    with sqlite3.connect(DB_PATH) as conn:
        for path in sorted((ROOT / 'sql').glob('*.sql')):
            print(f'\n## {path.name}')
            cursor = conn.execute(path.read_text(encoding='utf-8'))
            print(' | '.join(col[0] for col in cursor.description))
            for row in cursor.fetchall():
                print(' | '.join(map(str, row)))

if __name__ == '__main__':
    main()

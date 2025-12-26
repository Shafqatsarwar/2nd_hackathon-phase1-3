const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.resolve(process.cwd(), 'todo.db');
console.log('Testing SQLite at:', dbPath);

try {
    const db = new Database(dbPath);
    db.exec('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)');
    console.log('Success! DB opened and written to.');
    db.close();
} catch (err) {
    console.error('Failed to open DB:', err);
}

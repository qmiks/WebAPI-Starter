#!/usr/bin/env python3

import sqlite3

def main():
    # Connect directly to the database file
    conn = sqlite3.connect('webapi_starter.db')
    cursor = conn.cursor()
    
    # Check current roles
    cursor.execute('SELECT id, username, role FROM users')
    users = cursor.fetchall()
    print('Current users:')
    for user in users:
        print(f'- ID: {user[0]}, Username: {user[1]}, Role: {repr(user[2])}')
    
    # Update USER to user
    cursor.execute('UPDATE users SET role = ? WHERE role = ?', ('user', 'USER'))
    print(f'Updated {cursor.rowcount} users with role USER to user')
    
    # Check for other case issues
    cursor.execute('SELECT DISTINCT role FROM users')
    roles = cursor.fetchall()
    print('Current roles in database:', [r[0] for r in roles])
    
    # Commit changes
    conn.commit()
    conn.close()
    print('Changes committed')

if __name__ == "__main__":
    main()

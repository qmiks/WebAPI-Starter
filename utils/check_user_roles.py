#!/usr/bin/env python3

from data.database import user_crud

def main():
    users = user_crud.get_users()
    print(f'Users in database: {len(users)}')
    for user in users:
        print(f'- ID: {user["id"]}, Username: {user["username"]}, Role: {repr(user["role"])}')

if __name__ == "__main__":
    main()

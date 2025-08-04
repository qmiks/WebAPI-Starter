#!/usr/bin/env python3

from data.database import client_app_crud

def main():
    apps = client_app_crud.get_client_apps()
    print(f'Client Apps in Database: {len(apps)}')
    for app in apps:
        print(f'- App ID: {app["app_id"]}')
        print(f'  Name: {app["name"]}')
        print(f'  Active: {app["is_active"]}')
        print(f'  Secret: {app["app_secret"][:10]}...')
        print()

if __name__ == "__main__":
    main()

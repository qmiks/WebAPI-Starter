from data.database import user_crud, item_crud

print("=== DATABASE STATUS ===")

# Check users
users = user_crud.get_users()
print(f"Users: {len(users)}")
for u in users:
    print(f"  {u['id']}: {u['username']} ({u['role']})")

print()

# Check items
items = item_crud.get_items()
print(f"Items: {len(items)}")
for i in items:
    print(f"  {i['id']}: {i['name']} (owner: {i['owner_id']}, status: {i['status']})")

print()

# Check items for user 2 (demo user)
user_items = item_crud.get_items(owner_id=2)
print(f"Items for user 2: {len(user_items)}")
for i in user_items:
    print(f"  {i['id']}: {i['name']} (status: {i['status']})")

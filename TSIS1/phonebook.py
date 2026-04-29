"""
TSIS1 – Extended Phonebook Console Application
Features:
  • Add / list / delete contacts
  • Multiple phones per contact (add_phone procedure)
  • Filter by group, search by email, sort by name/birthday/date
  • Paginated navigation (next / prev / quit)
  • Move contact to group (move_to_group procedure)
  • Export contacts to JSON
  • Import contacts from JSON (duplicate handling)
  • Extend CSV import (email, birthday, group, phone type)
"""

import csv
import json
import sys
from datetime import date

import psycopg2
from connect import get_connection

PAGE_SIZE = 5  # rows per page


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _rows(cur):
    """Return list-of-dicts from cursor."""
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _print_contacts(rows):
    if not rows:
        print("  (no results)")
        return
    print(f"{'ID':<5} {'Name':<25} {'Email':<28} {'Birthday':<12} {'Group':<12} {'Phones'}")
    print("─" * 110)
    for r in rows:
        print(f"{r.get('id', r.get('contact_id', '')):<5} "
              f"{str(r.get('name', r.get('contact_name', ''))):<25} "
              f"{str(r.get('email') or ''):<28} "
              f"{str(r.get('birthday') or ''):<12} "
              f"{str(r.get('group_name') or ''):<12} "
              f"{r.get('phones_list') or r.get('phones') or ''}")


# ─────────────────────────────────────────────
# 1. Schema bootstrap
# ─────────────────────────────────────────────

def init_db():
    conn = get_connection()
    with conn, conn.cursor() as cur:
        with open("schema.sql") as f:
            cur.execute(f.read())
        with open("procedures.sql") as f:
            cur.execute(f.read())
    conn.close()
    print("✅  Database schema & procedures loaded.")


# ─────────────────────────────────────────────
# 2. CRUD
# ─────────────────────────────────────────────

def add_contact(name, email=None, birthday=None, group_name=None):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        group_id = None
        if group_name:
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            row = cur.fetchone()
            if row:
                group_id = row[0]
            else:
                print(f"  Group '{group_name}' not found; contact added without group.")
        cur.execute(
            "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
            (name, email, birthday, group_id)
        )
        cid = cur.fetchone()[0]
    conn.close()
    print(f"✅  Contact added (id={cid}).")
    return cid


def delete_contact(name):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("DELETE FROM contacts WHERE name = %s RETURNING id", (name,))
        deleted = cur.fetchall()
    conn.close()
    if deleted:
        print(f"✅  Deleted {len(deleted)} contact(s) named '{name}'.")
    else:
        print(f"  No contact named '{name}' found.")


def add_phone_to_contact(contact_name, phone, phone_type="mobile"):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
    conn.close()
    print(f"✅  Phone added.")


def move_contact_to_group(contact_name, group_name):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
    conn.close()
    print(f"✅  Contact moved to group '{group_name}'.")


# ─────────────────────────────────────────────
# 3. Search / filter / sort
# ─────────────────────────────────────────────

def search_contacts(query):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = _rows(cur)
    conn.close()
    _print_contacts(rows)


def filter_by_group(group_name):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones_list
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE g.name ILIKE %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY c.name
        """, (group_name,))
        rows = _rows(cur)
    conn.close()
    _print_contacts(rows)


def search_by_email(partial):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones_list
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            LEFT JOIN phones p ON p.contact_id = c.id
            WHERE c.email ILIKE %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
        """, (f"%{partial}%",))
        rows = _rows(cur)
    conn.close()
    _print_contacts(rows)


SORT_COLUMNS = {
    "name":     "c.name",
    "birthday": "c.birthday NULLS LAST",
    "date":     "c.created_at",
}


def list_contacts_sorted(sort_by="name"):
    col = SORT_COLUMNS.get(sort_by, "c.name")
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute(f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones_list
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            LEFT JOIN phones p ON p.contact_id = c.id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
            ORDER BY {col}
        """)
        rows = _rows(cur)
    conn.close()
    _print_contacts(rows)


# ─────────────────────────────────────────────
# 4. Paginated navigation
# ─────────────────────────────────────────────

def _get_page(offset, sort_col="c.name"):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute(f"""
            SELECT c.id, c.name, c.email, c.birthday, g.name AS group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones_list
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            LEFT JOIN phones p ON p.contact_id = c.id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
            ORDER BY {sort_col}
            LIMIT %s OFFSET %s
        """, (PAGE_SIZE, offset))
        rows = _rows(cur)
        cur.execute("SELECT COUNT(*) FROM contacts")
        total = cur.fetchone()[0]
    conn.close()
    return rows, total


def paginated_browse():
    offset = 0
    while True:
        rows, total = _get_page(offset)
        page_num = offset // PAGE_SIZE + 1
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        print(f"\n── Page {page_num}/{total_pages} (total contacts: {total}) ──")
        _print_contacts(rows)
        cmd = input("  [next / prev / quit]: ").strip().lower()
        if cmd == "next":
            if offset + PAGE_SIZE < total:
                offset += PAGE_SIZE
            else:
                print("  Already on the last page.")
        elif cmd == "prev":
            if offset > 0:
                offset -= PAGE_SIZE
            else:
                print("  Already on the first page.")
        elif cmd == "quit":
            break
        else:
            print("  Unknown command.")


# ─────────────────────────────────────────────
# 5. Export / Import JSON
# ─────────────────────────────────────────────

def export_to_json(filepath="contacts_export.json"):
    conn = get_connection()
    with conn, conn.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.email,
                   c.birthday::text, g.name AS group_name,
                   (
                       SELECT JSON_AGG(JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type))
                       FROM phones p WHERE p.contact_id = c.id
                   ) AS phones
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
        """)
        rows = _rows(cur)
    conn.close()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅  Exported {len(rows)} contacts to '{filepath}'.")


def import_from_json(filepath="contacts_export.json"):
    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"  File '{filepath}' not found.")
        return

    conn = get_connection()
    inserted = skipped = overwritten = 0

    for entry in data:
        name = entry.get("name")
        if not name:
            continue

        with conn.cursor() as cur:
            cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
            existing = cur.fetchone()

        if existing:
            action = input(f"  Duplicate '{name}'. [skip / overwrite]: ").strip().lower()
            if action == "overwrite":
                with conn, conn.cursor() as cur:
                    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
                overwritten += 1
            else:
                skipped += 1
                continue

        with conn, conn.cursor() as cur:
            # resolve group
            group_id = None
            if entry.get("group_name"):
                cur.execute("SELECT id FROM groups WHERE name = %s", (entry["group_name"],))
                g = cur.fetchone()
                if g:
                    group_id = g[0]
                else:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (entry["group_name"],))
                    group_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                (name, entry.get("email"), entry.get("birthday"), group_id)
            )
            cid = cur.fetchone()[0]

            for ph in (entry.get("phones") or []):
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                    (cid, ph["phone"], ph.get("type", "mobile"))
                )
        inserted += 1

    conn.close()
    print(f"✅  Import done — inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}.")


# ─────────────────────────────────────────────
# 6. Extended CSV import
# ─────────────────────────────────────────────

def import_csv(filepath="contacts.csv"):
    """
    Expected CSV columns (order flexible, header required):
    name, phone, type, email, birthday, group
    """
    try:
        f = open(filepath, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"  File '{filepath}' not found.")
        return

    conn = get_connection()
    count = 0
    with f, conn:
        reader = csv.DictReader(f)
        for row in reader:
            name  = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            ptype = (row.get("type") or "mobile").strip()
            email = (row.get("email") or None)
            bday  = (row.get("birthday") or None)
            group = (row.get("group") or None)

            if not name:
                continue

            with conn.cursor() as cur:
                # group
                group_id = None
                if group:
                    cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                    g = cur.fetchone()
                    if g:
                        group_id = g[0]
                    else:
                        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group,))
                        group_id = cur.fetchone()[0]

                # upsert contact
                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                existing = cur.fetchone()
                if existing:
                    cid = existing[0]
                    cur.execute(
                        "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                        (email or None, bday or None, group_id, cid)
                    )
                else:
                    cur.execute(
                        "INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s,%s,%s,%s) RETURNING id",
                        (name, email or None, bday or None, group_id)
                    )
                    cid = cur.fetchone()[0]

                if phone:
                    if ptype not in ("home", "work", "mobile"):
                        ptype = "mobile"
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s)",
                        (cid, phone, ptype)
                    )
            count += 1

    conn.close()
    print(f"✅  CSV import done — processed {count} row(s).")


# ─────────────────────────────────────────────
# 7. Interactive menu
# ─────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════╗
║         TSIS1 Phonebook Menu             ║
╠══════════════════════════════════════════╣
║  1. Add contact                          ║
║  2. Delete contact                       ║
║  3. Add phone to contact                 ║
║  4. Move contact to group                ║
║  5. Search (name / email / phone)        ║
║  6. Filter by group                      ║
║  7. Search by email                      ║
║  8. List & sort contacts                 ║
║  9. Browse (paginated)                   ║
║ 10. Export to JSON                       ║
║ 11. Import from JSON                     ║
║ 12. Import from CSV                      ║
║  0. Exit                                 ║
╚══════════════════════════════════════════╝
"""


def main():
    print("Initialising database …")
    try:
        init_db()
    except Exception as e:
        print(f"  ⚠ Could not init DB: {e}\n  (Continuing anyway — DB may already be set up.)")

    while True:
        print(MENU)
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                name     = input("  Name: ").strip()
                email    = input("  Email (blank to skip): ").strip() or None
                birthday = input("  Birthday YYYY-MM-DD (blank to skip): ").strip() or None
                group    = input("  Group (Family/Work/Friend/Other, blank to skip): ").strip() or None
                add_contact(name, email, birthday, group)

            elif choice == "2":
                name = input("  Contact name to delete: ").strip()
                delete_contact(name)

            elif choice == "3":
                name  = input("  Contact name: ").strip()
                phone = input("  Phone number: ").strip()
                ptype = input("  Type (home/work/mobile) [mobile]: ").strip() or "mobile"
                add_phone_to_contact(name, phone, ptype)

            elif choice == "4":
                name  = input("  Contact name: ").strip()
                group = input("  Group name: ").strip()
                move_contact_to_group(name, group)

            elif choice == "5":
                q = input("  Search query: ").strip()
                search_contacts(q)

            elif choice == "6":
                g = input("  Group name: ").strip()
                filter_by_group(g)

            elif choice == "7":
                e = input("  Email (partial): ").strip()
                search_by_email(e)

            elif choice == "8":
                s = input("  Sort by (name / birthday / date) [name]: ").strip() or "name"
                list_contacts_sorted(s)

            elif choice == "9":
                paginated_browse()

            elif choice == "10":
                path = input("  Output file [contacts_export.json]: ").strip() or "contacts_export.json"
                export_to_json(path)

            elif choice == "11":
                path = input("  JSON file [contacts_export.json]: ").strip() or "contacts_export.json"
                import_from_json(path)

            elif choice == "12":
                path = input("  CSV file [contacts.csv]: ").strip() or "contacts.csv"
                import_csv(path)

            elif choice == "0":
                print("Goodbye!")
                sys.exit(0)

            else:
                print("  Unknown option.")

        except psycopg2.Error as e:
            print(f"  ⚠ DB error: {e}")
        except Exception as e:
            print(f"  ⚠ Error: {e}")

        input("\n  Press Enter to continue …")


if __name__ == "__main__":
    main()
import threading
import customtkinter as ctk
from pymongo import MongoClient
from pymongo import ReplaceOne
from pymongo.errors import PyMongoError
from tkinter import messagebox
import certifi

# Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# App Window
root = ctk.CTk()
root.title("PyMongoCopy")
root.geometry("580x660")
root.resizable(False, False)

# Fonts
FONT_TITLE   = ctk.CTkFont(family="Georgia", size=22, weight="bold")
FONT_LABEL   = ctk.CTkFont(family="Courier New", size=11, weight="bold")
FONT_ENTRY   = ctk.CTkFont(family="Courier New", size=12)
FONT_BUTTON  = ctk.CTkFont(family="Georgia", size=13, weight="bold")
FONT_STATUS  = ctk.CTkFont(family="Courier New", size=11)
FONT_BADGE   = ctk.CTkFont(family="Courier New", size=10)

# Colors
BG          = "#0f1117"
CARD        = "#1a1d27"
BORDER      = "#2a2d3e"
ACCENT      = "#00d4aa"
ACCENT_DIM  = "#009e7f"
TEXT        = "#e8eaf0"
TEXT_DIM    = "#6b7280"
ERROR       = "#ff4d6d"
WARNING     = "#f59e0b"

root.configure(fg_color=BG)

# Header
header_frame = ctk.CTkFrame(root, fg_color=CARD, corner_radius=0, height=80,
                             border_width=0)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

header_inner = ctk.CTkFrame(header_frame, fg_color="transparent")
header_inner.place(relx=0.5, rely=0.5, anchor="center")

dot = ctk.CTkLabel(header_inner, text="⬡", font=ctk.CTkFont(size=22),
                    text_color=ACCENT)
dot.pack(side="left", padx=(0, 10))

title = ctk.CTkLabel(header_inner, text="PyMongoCopy", font=FONT_TITLE,
                      text_color=TEXT)
title.pack(side="left")

badge = ctk.CTkLabel(
    header_frame,
    text="MIGRATION TOOL",
    font=FONT_BADGE,
    text_color=TEXT_DIM,
)
badge.place(relx=0.5, rely=0.78, anchor="center")

# Separator
sep = ctk.CTkFrame(root, fg_color=BORDER, height=1)
sep.pack(fill="x")

# Main Card
card = ctk.CTkFrame(root, fg_color=CARD, corner_radius=16,
                     border_width=1, border_color=BORDER)
card.pack(fill="both", expand=True, padx=28, pady=24)

inner = ctk.CTkScrollableFrame(
    card,
    fg_color="transparent",
    corner_radius=0,
    scrollbar_button_color=BORDER,
    scrollbar_button_hover_color=TEXT_DIM,
)
inner.pack(fill="both", expand=True, padx=28, pady=24)

# Input Helper 
def make_field(parent, label, placeholder):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(0, 14))

    lbl = ctk.CTkLabel(row, text=label, font=FONT_LABEL,
                        text_color=ACCENT, anchor="w")
    lbl.pack(fill="x", pady=(0, 5))

    entry = ctk.CTkEntry(
        row,
        placeholder_text=placeholder,
        font=FONT_ENTRY,
        height=42,
        corner_radius=8,
        border_width=1,
        border_color=BORDER,
        fg_color="#12151f",
        text_color=TEXT,
        placeholder_text_color=TEXT_DIM,
    )
    entry.pack(fill="x")
    return entry

# Section: Clusters
section_lbl = ctk.CTkLabel(inner, text="CLUSTER CONNECTIONS",
                             font=FONT_BADGE, text_color=TEXT_DIM, anchor="w")
section_lbl.pack(fill="x", pady=(0, 8))

old_uri_entry = make_field(inner, "SOURCE URI",
                            "mongodb+srv://user:pass@old-cluster.mongodb.net")
new_uri_entry = make_field(inner, "TARGET URI",
                            "mongodb+srv://user:pass@new-cluster.mongodb.net")

# Divider
div = ctk.CTkFrame(inner, fg_color=BORDER, height=1)
div.pack(fill="x", pady=(4, 18))

# Section: Source Namespace
source_ns_lbl = ctk.CTkLabel(inner, text="SOURCE NAMESPACE",
                             font=FONT_BADGE, text_color=TEXT_DIM, anchor="w")
source_ns_lbl.pack(fill="x", pady=(0, 8))

source_row = ctk.CTkFrame(inner, fg_color="transparent")
source_row.pack(fill="x")
source_row.columnconfigure(0, weight=1)
source_row.columnconfigure(1, weight=1)

src_db_col = ctk.CTkFrame(source_row, fg_color="transparent")
src_db_col.grid(row=0, column=0, sticky="ew", padx=(0, 8))
ctk.CTkLabel(src_db_col, text="SOURCE DATABASE", font=FONT_BADGE,
             text_color=ACCENT, anchor="w").pack(fill="x", pady=(0, 5))
source_db_entry = ctk.CTkEntry(src_db_col, placeholder_text="source_database",
                               font=FONT_ENTRY, height=42, corner_radius=8,
                               border_width=1, border_color=BORDER,
                               fg_color="#12151f", text_color=TEXT,
                               placeholder_text_color=TEXT_DIM)
source_db_entry.pack(fill="x")

src_col_col = ctk.CTkFrame(source_row, fg_color="transparent")
src_col_col.grid(row=0, column=1, sticky="ew", padx=(8, 0))
ctk.CTkLabel(src_col_col, text="SOURCE COLLECTION", font=FONT_BADGE,
             text_color=ACCENT, anchor="w").pack(fill="x", pady=(0, 5))
source_collection_entry = ctk.CTkEntry(src_col_col, placeholder_text="user",
                                       font=FONT_ENTRY, height=42, corner_radius=8,
                                       border_width=1, border_color=BORDER,
                                       fg_color="#12151f", text_color=TEXT,
                                       placeholder_text_color=TEXT_DIM)
source_collection_entry.pack(fill="x")

# Section: Target Namespace
target_ns_lbl = ctk.CTkLabel(inner, text="TARGET NAMESPACE",
                             font=FONT_BADGE, text_color=TEXT_DIM, anchor="w")
target_ns_lbl.pack(fill="x", pady=(16, 8))

target_row = ctk.CTkFrame(inner, fg_color="transparent")
target_row.pack(fill="x")
target_row.columnconfigure(0, weight=1)
target_row.columnconfigure(1, weight=1)

tgt_db_col = ctk.CTkFrame(target_row, fg_color="transparent")
tgt_db_col.grid(row=0, column=0, sticky="ew", padx=(0, 8))
ctk.CTkLabel(tgt_db_col, text="TARGET DATABASE", font=FONT_BADGE,
             text_color=ACCENT, anchor="w").pack(fill="x", pady=(0, 5))
target_db_entry = ctk.CTkEntry(tgt_db_col, placeholder_text="target_database",
                               font=FONT_ENTRY, height=42, corner_radius=8,
                               border_width=1, border_color=BORDER,
                               fg_color="#12151f", text_color=TEXT,
                               placeholder_text_color=TEXT_DIM)
target_db_entry.pack(fill="x")

tgt_col_col = ctk.CTkFrame(target_row, fg_color="transparent")
tgt_col_col.grid(row=0, column=1, sticky="ew", padx=(8, 0))
ctk.CTkLabel(tgt_col_col, text="TARGET COLLECTION", font=FONT_BADGE,
             text_color=ACCENT, anchor="w").pack(fill="x", pady=(0, 5))
target_collection_entry = ctk.CTkEntry(tgt_col_col, placeholder_text="user",
                                       font=FONT_ENTRY, height=42, corner_radius=8,
                                       border_width=1, border_color=BORDER,
                                       fg_color="#12151f", text_color=TEXT,
                                       placeholder_text_color=TEXT_DIM)
target_collection_entry.pack(fill="x")

# Progress Area
progress_frame = ctk.CTkFrame(inner, fg_color="#12151f", corner_radius=10,
                               border_width=1, border_color=BORDER)
progress_frame.pack(fill="x", pady=(22, 0))

prog_inner = ctk.CTkFrame(progress_frame, fg_color="transparent")
prog_inner.pack(fill="x", padx=16, pady=12)

progress_bar = ctk.CTkProgressBar(prog_inner, height=6, corner_radius=3,
                                   fg_color=BORDER, progress_color=ACCENT)
progress_bar.pack(fill="x")
progress_bar.set(0)

error_details = ctk.CTkTextbox(
    prog_inner,
    height=120,
    font=FONT_BADGE,
    fg_color="#0f1320",
    border_width=1,
    border_color=ERROR,
    text_color=ERROR,
    corner_radius=8,
    wrap="word",
)
error_details.configure(state="disabled")


def show_error_details(text):
    if not error_details.winfo_ismapped():
        error_details.pack(fill="x", pady=(10, 0))
    error_details.configure(state="normal")
    error_details.delete("1.0", "end")
    error_details.insert("1.0", text)
    error_details.configure(state="disabled")


def hide_error_details():
    if error_details.winfo_ismapped():
        error_details.pack_forget()

def build_client(uri):
    # Atlas/SSL connections are more reliable when an explicit CA bundle is provided.
    return MongoClient(
        uri,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=20000,
        tlsCAFile=certifi.where(),
    )


# Migrate Button
def run_migrations():
    old_uri        = old_uri_entry.get().strip()
    new_uri        = new_uri_entry.get().strip()
    source_db_name = source_db_entry.get().strip()
    source_collection_name = source_collection_entry.get().strip()
    target_db_name = target_db_entry.get().strip()
    target_collection_name = target_collection_entry.get().strip()

    if not all([
        old_uri,
        new_uri,
        source_db_name,
        source_collection_name,
        target_db_name,
        target_collection_name,
    ]):
        messagebox.showerror("Missing Fields", "Please fill in all fields.")
        return
    if old_uri == new_uri:
        messagebox.showerror(
            "Invalid Configuration",
            "Source and target URIs must be different for safe migration.",
        )
        return

    migrate_button.configure(state="disabled", text="MIGRATING…")
    progress_bar.set(0)
    hide_error_details()

    def set_status(text, color=TEXT_DIM):
        # Intentionally kept as a no-op after removing inline status UI.
        return None

    def set_error(text):
        root.after(0, lambda: show_error_details(text))

    def set_progress(value, total):
        root.after(0, lambda: progress_bar.set(value / total if total else 0))

    def task():
        source_client = target_client = None
        try:
            set_status("⟳  Connecting to clusters…", WARNING)
            source_client = build_client(old_uri)
            target_client = build_client(new_uri)
            source_client.admin.command("ping")
            target_client.admin.command("ping")

            src_col = source_client[source_db_name][source_collection_name]
            tgt_col = target_client[target_db_name][target_collection_name]
            src_db = source_client[source_db_name]
            available_collections = src_db.list_collection_names()

            if source_collection_name not in available_collections:
                lower_map = {name.lower(): name for name in available_collections}
                if source_collection_name.lower() in lower_map:
                    suggestion = lower_map[source_collection_name.lower()]
                    msg = (
                        "Source collection name is case-sensitive.\n\n"
                        f"You entered: {source_collection_name}\n"
                        f"Did you mean: {suggestion} ?"
                    )
                else:
                    preview = ", ".join(available_collections[:10]) or "no collections found"
                    msg = (
                        f"Collection '{source_collection_name}' was not found in database '{source_db_name}'.\n\n"
                        f"Available collections: {preview}"
                    )
                set_error(msg)
                root.after(0, lambda: messagebox.showwarning("Source Collection Not Found", msg))
                return

            total = src_col.count_documents({})

            if total == 0:
                empty_msg = (
                    "No documents found in source.\n\n"
                    f"Checked: {source_db_name}.{source_collection_name}\n"
                    "Collection exists but is empty for this user/query.\n"
                    "Verify you are using the intended source cluster and user."
                )
                set_error(empty_msg)
                root.after(0, lambda: messagebox.showwarning("No Source Documents", empty_msg))
                return

            cursor = src_col.find({})
            operations, count = [], 0
            upserted_count = 0
            modified_count = 0

            for doc in cursor:
                operations.append(ReplaceOne({"_id": doc["_id"]}, doc, upsert=True))
                count += 1
                if len(operations) >= 100:
                    result = tgt_col.bulk_write(operations, ordered=False)
                    upserted_count += result.upserted_count
                    modified_count += result.modified_count
                    operations = []
                    set_progress(count, total)
                    set_status(f"⟳  Migrating — {count:,} / {total:,} documents", ACCENT)

            if operations:
                result = tgt_col.bulk_write(operations, ordered=False)
                upserted_count += result.upserted_count
                modified_count += result.modified_count

            set_progress(total, total)
            set_status(
                (
                    f"✓  Done — scanned {total:,}; inserted {upserted_count:,}; "
                    f"updated {modified_count:,}"
                ),
                ACCENT,
            )
            root.after(0, lambda: messagebox.showinfo(
                "Migration Complete",
                (
                    f"Scanned: {total:,}\n"
                    f"Inserted: {upserted_count:,}\n"
                    f"Updated: {modified_count:,}\n"
                    f"From: {source_db_name}.{source_collection_name}\n"
                    f"To: {target_db_name}.{target_collection_name}"
                ),
            ))

        except (KeyError, PyMongoError, ValueError) as e:
            error_text = str(e)
            error_lower = error_text.lower()
            if "ssl" in error_lower or "tls" in error_lower or "certificate" in error_lower:
                error_text = (
                    f"{error_text}\n\n"
                    "TLS/SSL handshake failed.\n"
                    "Try:\n"
                    "1) pip install --upgrade certifi pymongo\n"
                    "2) Verify Atlas IP Access List allows your current IP\n"
                    "3) Ensure your URI is an Atlas SRV URI (mongodb+srv://...)"
                )
            set_status(f"✗  Error: {e}", ERROR)
            set_error(error_text)
            root.after(0, lambda: messagebox.showerror("Migration Error", error_text))
        except Exception as e:
            set_status(f"✗  Unexpected error: {e}", ERROR)
            set_error(str(e))
            root.after(0, lambda: messagebox.showerror("Unexpected Error", str(e)))

        finally:
            for c in (source_client, target_client):
                if c:
                    c.close()
            root.after(0, lambda: migrate_button.configure(
                state="normal", text="START MIGRATION"
            ))

    threading.Thread(target=task, daemon=True).start()

migrate_button = ctk.CTkButton(
    inner,
    text="START MIGRATION",
    command=run_migrations,
    font=FONT_BUTTON,
    height=48,
    corner_radius=10,
    fg_color=ACCENT,
    hover_color=ACCENT_DIM,
    text_color="#0f1117",
)
migrate_button.pack(fill="x", pady=(18, 0))

root.mainloop()

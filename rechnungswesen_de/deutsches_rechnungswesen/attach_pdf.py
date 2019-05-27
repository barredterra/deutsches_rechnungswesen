import frappe
from frappe import _
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import save_file
from frappe.core.doctype.file.file import create_new_folder

def sales_invoice(sinv, event):
    folder = create_folders(_("Sales Invoice"), sinv.customer)
    attach_pdf(sinv, sinv.name, folder)

def create_folders(doctype, party):
    try:
        create_new_folder(doctype, "Home")
    except frappe.DuplicateEntryError:
        frappe.db.rollback()

    try:
        create_new_folder(party, "/".join(["Home", doctype]))
    except frappe.DuplicateEntryError:
        frappe.db.rollback()
    
    return "/".join(["Home", doctype, party])

def attach_pdf(doctype, name, folder):
    html = frappe.get_print(doctype, name)
    file_name = "{}.pdf".format(name.replace(" ", "-").replace("/", "-"))
    content = get_pdf(html)
    save_file(file_name, content, doctype, name, folder=folder, is_private=1)

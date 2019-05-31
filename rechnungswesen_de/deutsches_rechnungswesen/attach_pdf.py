import frappe
from frappe import _
from frappe.utils.pdf import get_pdf
from frappe.utils.file_manager import save_file
from frappe.core.doctype.file.file import create_new_folder

def sales_invoice(sinv, event):
    sinv_folder = create_folder(_("Sales Invoice"), "Home")
    cust_folder = create_folder(sinv.customer, sinv_folder)
    attach_pdf(sinv, sinv.name, cust_folder)

def create_folder(folder, parent):
    try:
        create_new_folder(folder, "Home")
    except frappe.DuplicateEntryError:
        pass

    return "/".join([parent, folder])

def attach_pdf(doctype, name, folder):
    html = frappe.get_print(doctype, name)
    file_name = "{}.pdf".format(name.replace(" ", "-").replace("/", "-"))
    content = get_pdf(html)
    save_file(file_name, content, doctype, name, folder=folder, is_private=1)

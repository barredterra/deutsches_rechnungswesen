import frappe
from frappe import _

def sales_invoice(sinv, event=None):
    execute(sinv.doctype, sinv.name, sinv.customer)

def execute(doctype, name, party):
    doctype_folder = create_folder(_(doctype), "Home")
    party_folder = create_folder(party, doctype_folder)
    pdf_data = get_pdf_data(doctype, name)
    save_and_attach(pdf_data, doctype, name, party_folder)

def create_folder(folder, parent):
    """Make sure the folder exists and return it's name."""
    from frappe.core.doctype.file.file import create_new_folder
    try:
        create_new_folder(folder, "Home")
    except frappe.DuplicateEntryError:
        pass

    return "/".join([parent, folder])

def get_pdf_data(doctype, name):
    """Document -> HTML -> PDF."""
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)

def save_and_attach(content, to_doctype, to_name, folder):
    """
    Save content to disk and create a File document.
    
    File document is linked to another document.
    """
    from frappe.utils.file_manager import save_file
    file_name = "{}.pdf".format(to_name.replace(" ", "-").replace("/", "-"))
    save_file(file_name, content, to_doctype, to_name, folder=folder, is_private=1)

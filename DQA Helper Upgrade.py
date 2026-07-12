import re
import tkinter as tk
import json
from urllib.parse import urlparse
from tkinter import ttk

# Function to show instruction pop-up before launching the app
def show_instruction():
    instruction_window = tk.Toplevel()
    instruction_window.title("DQA HELPER 2.0")
    instruction_window.geometry("400x300")
    
    instruction_label = tk.Label(instruction_window, text=(
        "Welcome to DQA HELPER 2.0!\n\n"
        "This tool helps you correctly format job titles, phone numbers, emails, links, addresses, and more!\n\n"
        "Instructions:\n"
        "- Type or paste on the entry field.\n"
        "- Press ENTER to apply changes.\n"
        "- Then, automatically paste it on your environment.\n"
        "- No need for typing; just CTRL+C & CTRL+V. Easy peasy!\n\n"
        "Hoping this helps speed up your process.\n"
        "Enjoy using the tool!\n\n"
        "Sincerely, JJBartz <3"

    ), wraplength=350, justify="center")
    instruction_label.pack(pady=20)
    
    def close_instruction():
        instruction_window.destroy()
        root.deiconify()  # Show the main window after closing
    
    close_button = tk.Button(instruction_window, text="Got it!", command=close_instruction)
    close_button.pack()
    
    instruction_window.transient(root)  # Make it modal
    instruction_window.grab_set()
    root.wait_window(instruction_window)  # Block execution until closed

# GUI Setup
root = tk.Tk()
root.withdraw()  # Hide main window initially
root.after(100, show_instruction)  # Show instruction pop-up

root.title("DQA HELPER 2.0")
root.geometry("600x300")

# Function to adjust widgets dynamically
def adjust_widgets(event=None):
    for widget in root.winfo_children():
        widget.grid_configure(padx=5, pady=5, sticky="ew")
    for i in range(3):
        root.columnconfigure(i, weight=1)
    for i in range(10):
        root.rowconfigure(i, weight=1)
    # Adjust text box widths dynamically
    entry_company.config(width=root.winfo_width() // 20)
    entry_job_title.config(width=root.winfo_width() // 20)
    entry_email.config(width=root.winfo_width() // 20)
    entry_link.config(width=root.winfo_width() // 20)
    entry_phone1.config(width=root.winfo_width() // 20)
    entry_phone2.config(width=root.winfo_width() // 20)
    text_area_address.config(width=root.winfo_width() // 15)

#COMPANY NAME
# Function to remove punctuation from a string except for specific cases
def remove_punctuation(text, retain_exceptions):
    exceptions = ["L.P.", "L.L.P.", "L.T.E.", "C.O.", "Inc.", "Ltd.", "Corp.", "LLC", "GmbH", "S.A.", "Pte.", "PLC", "&"]
    words = text.split()
    cleaned_words = []
    for word in words:
        if retain_exceptions and any(word.upper() == ex.upper() for ex in exceptions):
            cleaned_words.append(word)  # Retain exact exception, including punctuation and capitalization
        else:
            cleaned_words.append(re.sub(r'[^\w\s]', '', word))  # Remove all punctuation
    return ' '.join(cleaned_words)
def correct_company_format(event=None):
    text = entry_company.get().strip()
    
    if remove_punctuation_var.get():  # If checked, remove all punctuation
        corrected_text = remove_punctuation(text, retain_exceptions=False)
        corrected_text = ' '.join(word.capitalize() if word.upper() not in ["LP", "LLP", "LTE", "CO", "Inc", "Ltd", "Corp", "LLC", "GmbH", "SA", "Pte", "PLC"] else word.upper() 
                                   for word in corrected_text.split())
    else:  # If unchecked, retain punctuation and just fix capitalization
        corrected_text = []
        for word in text.split():
            if word.upper() in ["L.P.", "L.L.P.", "L.T.E.", "C.O.", "Inc.", "Ltd.", "Corp.", "LLC", "GmbH", "S.A.", "Pte.", "PLC"]:
                corrected_text.append(word)  # Retain exact formatting
            else:
                corrected_text.append(word.capitalize())  # Capitalize the rest
        corrected_text = ' '.join(corrected_text)

    update_entry(entry_company, corrected_text)

#JOB TITLE
# File to store job acronyms
ACRONYM_FILE = "job_acronyms.json"

# Load acronyms from file
def load_acronyms():
    try:
        with open(ACRONYM_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
# Save acronyms to file
def save_acronyms():
    with open(ACRONYM_FILE, "w") as file:
        json.dump(job_acronym_dict, file, indent=4)

# Dictionary of job title acronyms
job_acronym_dict = load_acronyms()
if not job_acronym_dict:  # Initialize default values if file is empty
    job_acronym_dict = {
    "ASSOC": "Associate", "CAO": "Chief Administrative Officer", "CEO": "Chief Executive Officer",
    "CDO": "Chief Data Officer", "CFO": "Chief Financial Officer", "CHAIR": "Chairperson",
    "CHRO": "Chief Human Resources Officer", "CIO": "Chief Information Officer", "CLO": "Chief Legal Officer",
    "CMO": "Chief Marketing Officer", "COO": "Chief Operating Officer", "CPO": "Chief People Officer",
    "CSO": "Chief Security Officer", "CCO": "Chief Compliance Officer", "CTO": "Chief Technology Officer",
    "DIR": "Director", "ED": "Executive Director", "EVP": "Executive Vice President",
    "SVP": "Senior Vice President", "MD": "Managing Director", "MP": "Managing Partner",
    "PRES": "President", "VP": "Vice President", "PM": "Project Manager", "MGR": "Manager",
    "ASST": "Assistant", "GC": "General Counsel", "SR": "Senior", "JR": "Junior",
    "M&A": "Mergers and Acquisition", "DEVT": "Development", "MFTG": "Manufacturing",
    "HR": "Human Resources", "IP": "Intellectual Property", "ESG": "Environmental, Social, and Governance",
    "AVP": "Associate Vice President", "CSR": "Corporate Social Responsibility"
    }
    save_acronyms()
# Function to format job titles
def correct_job_title(event=None):
    # Get input text
    text = entry_job_title.get().strip()
    
    # Replace delimiters (except hyphens) with a comma and a space
    delimiters = ["–", "|", "/", "(", ")"]
    for delimiter in delimiters:
        text = text.replace(delimiter, ", ")
    
    # Normalize multiple commas and spaces
    text = re.sub(r',\s+', ', ', text)  # Ensure single space after commas
    text = text.strip(', ')  # Remove leading/trailing commas and spaces
    
    # Handle acronyms with periods
    def remove_periods_from_acronyms(word):
        word_no_periods = word.replace(".", "").upper()
        return job_acronym_dict.get(word_no_periods, word)
    
    corrected_words = []
    # Split input based on comma followed by space
    parts = text.split(", ")
    
    for part in parts:
        words = []
        for word in part.split():
            # Remove periods from acronyms and lookup in the dictionary
            corrected_word = remove_periods_from_acronyms(word)
            if corrected_word.lower() in ["and", "of", "the", "at", "in", "our"]:
                words.append(corrected_word.lower())
            elif corrected_word == "&":
                words.append("and")
            else:
                # Capitalize hyphenated words correctly
                words.append("-".join([w.capitalize() for w in corrected_word.split("-")]))
        corrected_words.append(" ".join(words))
    
    corrected_text = ", ".join(corrected_words)
    update_entry(entry_job_title, corrected_text)

# Function to show a popup for adding acronyms
def show_add_acronym_popup():
    popup = tk.Toplevel(root)
    popup.title("Add Acronym")
    popup.geometry("350x200")
    
    tk.Label(popup, text="Acronym:").pack()
    entry_acronym = tk.Entry(popup, width=20)
    entry_acronym.pack()
    
    tk.Label(popup, text="Full Form:").pack()
    entry_full_form = tk.Entry(popup, width=50)
    entry_full_form.pack()
    
    preview_label = tk.Label(popup, text="")
    preview_label.pack()
    
    def preview_acronym():
        acronym = entry_acronym.get().strip().upper()
        full_form = entry_full_form.get().strip().title()
        if acronym and full_form:
            preview_label.config(text=f"Preview: {acronym} - {full_form}", fg="blue")
    
    def add_to_dictionary():
        acronym = entry_acronym.get().strip().upper()
        full_form = entry_full_form.get().strip().title()
        if acronym and full_form:
            job_acronym_dict[acronym] = full_form
            save_acronyms()
            popup.destroy()
        else:
            preview_label.config(text="Please enter both acronym and full form", fg="red")
    
    entry_acronym.bind("<KeyRelease>", lambda event: preview_acronym())
    entry_full_form.bind("<KeyRelease>", lambda event: preview_acronym())
    
    tk.Button(popup, text="Add", command=add_to_dictionary).pack()

#EMAIL 
def correct_email_format(event=None):
    text = entry_email.get().strip().lower()
    update_entry(entry_email, text)

#LINK
def correct_link(event=None):
    text = entry_link.get().strip()
    parsed_url = urlparse(text, scheme="https")  # Ensure valid parsing
    
    # Extract domain and path
    domain = parsed_url.netloc.lstrip("www.") if not include_www_var.get() else parsed_url.netloc
    path = parsed_url.path.rstrip('/')
    
    formatted_link = f"{domain}{path}" if path else domain
    update_entry(entry_link, formatted_link)

#PHONE NUMBERS (PHONE & FAX)
# Phone number formats
number_formats = {
    "HK": "+852 {}{}{}{} {}{}{}{}",
    "Ireland Direct": "+353 {} {}{}{} {}{}{}{}",
    "Ireland Mobile": "+353 {}{} {}{}{} {}{}{}{}",
    "Singapore": "+65 {}{}{}{} {}{}{}{}",
    "UK Direct": "+44 {}{} {}{}{}{} {}{}{}{}",
    "UK Mobile/Jersey": "+44 {}{}{}{} {}{}{}{}{}{}",
    "US/BVI/Cayman": "+1 {}{}{} {}{}{} {}{}{}{}",
    "UK Regional Direct": "+44 {}{}{} {}{}{} {}{}{}{}"
}

# Function to format phone number
def correct_and_copy_phone(widget):
    phone_number = widget.get().strip()
    country = country_dropdown.get()
    
    if not country:
        # Remove (0) and replace ., /, - with spaces, retain +
        cleaned_number = re.sub(r"\(0\)", "", phone_number)  # Remove (0)
        cleaned_number = re.sub(r"[()./-]", " ", cleaned_number)  # Replace symbols with spaces
        cleaned_number = re.sub(r"\s+", " ", cleaned_number).strip()  # Remove double spaces
        update_entry(widget, cleaned_number)
        return

    # Process normally if a country is selected
    digits_only = re.sub(r"\D", "", phone_number)  # Remove non-numeric characters
    country_format = number_formats.get(country)
    
    if country_format:
        required_digits = country_format.count("{}")
        if len(digits_only) >= required_digits:
            formatted_number = country_format.format(*digits_only[:required_digits])
            update_entry(widget, formatted_number)
        else:
            update_entry(widget, "Invalid Number")  # Handle short input
    else:
        update_entry(widget, "Invalid Country")  # Handle missing country format

#ADDRESS
# Dictionary for address acronyms
address_acronym_dict = {
    "N": "North", "S": "South", "E": "East", "W": "West", "St": "Street", "St.": "Street", "ST": "Street", "ST.": "Street", "Ste": "Suite",
    "Ave": "Avenue", "Ave.": "Avenue", "AVE": "Avenue", "AVE.": "Avenue",
    "Blvd": "Boulevard", "Blvd.": "Boulevard", "BLVD": "Boulevard", "BLVD.": "Boulevard",
    "Rd": "Road", "Rd.": "Road", "RD": "Road", "RD.": "Road",
    "Ln": "Lane", "Ln.": "Lane", "LN": "Lane", "LN.": "Lane",
    "Dr": "Drive", "Dr.": "Drive", "DR": "Drive", "DR.": "Drive",
    "Ct": "Court", "Ct.": "Court", "CT": "Court", "CT.": "Court",
    "Pl": "Place", "Pl.": "Place", "PL": "Place", "PL.": "Place",
    "Pkwy": "Parkway", "Pkwy.": "Parkway", "PKWY": "Parkway", "PKWY.": "Parkway",
    "Hwy": "Highway", "Hwy.": "Highway", "HWY": "Highway", "HWY.": "Highway",
    "Sq": "Square", "Sq.": "Square", "SQ": "Square", "SQ.": "Square",
    "Terr": "Terrace", "Terr.": "Terrace", "TERR": "Terrace", "TERR.": "Terrace",
    "Cir": "Circle", "Cir.": "Circle", "CIR": "Circle", "CIR.": "Circle"
}

# US State Abbreviations (to keep capitalization)
state_abbreviations = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", 
    "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", 
    "WA", "WV", "WI", "WY", "DC"
}

# Function to format address properly
def format_address(text):
    # Move Suite number to a new line if '#' is detected
    text = re.sub(r'\s*#(\d+)', r'\nSuite \1', text)
    
    # Split address into lines using commas
    lines = [line.strip() for line in text.split(",")]
    
    formatted_lines = []
    for line in lines:
        words = re.split(r'\s+', line)
        formatted_words = []
        for word in words:
            if word.upper() in state_abbreviations:  # Keep state abbreviations uppercase
                formatted_words.append(word.upper())
            elif word.upper() in ["NW", "NE", "SE", "SW"]:  # Keep compass directions uppercase
                formatted_words.append(word.upper())
            elif re.match(r'\d+(st|nd|rd|th)', word, re.IGNORECASE):  # Keep ordinal numbers lowercase
                formatted_words.append(word.lower())
            else:
                formatted_words.append(
                    address_acronym_dict.get(word.rstrip("."), 
                    address_acronym_dict.get(word.upper().rstrip("."), word.title()))
                )
        formatted_lines.append(" ".join(formatted_words))
    
    return "\n".join(formatted_lines)

# Function to update preview while typing
def preview_address(event=None):
    if 'text_area_address' in globals():  # Ensure the variable is defined
        text = text_area_address.get("1.0", tk.END).strip()
        formatted_text = format_address(text)

        # Get the current width of the entry field to adjust font size
        entry_width = text_area_address.winfo_width()
        font_size = max(8, entry_width // 25)  # Adjust font size dynamically

        text_area_address.config(font=("Arial", font_size))  # Apply font to entry field
        preview_text_area.config(state=tk.NORMAL, font=("Arial", font_size))
        preview_text_area.delete("1.0", tk.END)
        preview_text_area.insert("1.0", formatted_text)
        preview_text_area.config(state=tk.DISABLED)

# Ensure text_area_address exists before binding events
if 'text_area_address' in globals():
    text_area_address.bind("<Configure>", preview_address)

# Function to apply changes when Enter is pressed
def update_address(event=None):
    text = text_area_address.get("1.0", tk.END).strip()
    corrected_text = format_address(text)

    # Update text area with corrected address
    text_area_address.delete("1.0", tk.END)
    text_area_address.insert("1.0", corrected_text)

    # Update preview
    preview_address()
   
   # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(corrected_text)
    root.update()

#AUTOMATIC UPDATE 
# Function to update an entry widget and copy to clipboard
def update_entry(widget, text):
    widget.delete(0, tk.END)
    widget.insert(0, text)
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

#AUTOMATIC COPY
# Function to copy preset text to clipboard
def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

#Descriptions
def copy_bio():
    copy_to_clipboard("Bio")
def copy_website():
    copy_to_clipboard("Website")
def copy_linkedin():
    copy_to_clipboard("LinkedIn")
def copy_email():
    copy_to_clipboard("Email")

# Function to adjust font size dynamically
def adjust_font(event=None):
    new_size = max(8, int(root.winfo_width() / 50))  # Adjust font size dynamically
    font_config = ("Arial", new_size)
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry, tk.Button, tk.Text)):
            widget.config(font=font_config)

# Main GUI Elements
root.deiconify()

# Checkbox variable for removing punctuation
remove_punctuation_var = tk.BooleanVar(value=True)

#Company Name
tk.Label(root, text="Company:", anchor="w", width=15).grid(row=0, column=0, sticky="w")
entry_company = tk.Entry(root, width=30)
entry_company.grid(row=0, column=1, sticky="ew")
entry_company.bind("<Return>", correct_company_format)
tk.Checkbutton(root, text="Remove Symbols", variable=remove_punctuation_var, command=correct_company_format).grid(row=0, column=2)

#Job Title
tk.Label(root, text="Job Title:", anchor="w", width=15).grid(row=1, column=0, sticky="w")
entry_job_title = tk.Entry(root, width=30)
entry_job_title.grid(row=1, column=1, sticky="ew")
entry_job_title.bind("<Return>", correct_job_title)
tk.Button(root, text="Add Job Title", command=show_add_acronym_popup, width=5).grid(row=1, column=2, sticky="ew", padx=5, pady=5)

#Link
include_www_var = tk.BooleanVar(value=False)
tk.Label(root, text="Link:", anchor="w", width=15).grid(row=2, column=0, sticky="w")
entry_link = tk.Entry(root, width=30)
entry_link.grid(row=2, column=1, sticky="ew")
entry_link.bind("<Return>", correct_link)
tk.Checkbutton(root, text="Include 'www.'", variable=include_www_var, command=correct_link).grid(row=2, column=2, sticky="w")

#Email
tk.Label(root, text="Email:", anchor="w", width=15).grid(row=3, column=0, sticky="w")
entry_email = tk.Entry(root, width=30)
entry_email.grid(row=3, column=1, sticky="ew")
entry_email.bind("<Return>", correct_email_format)

#Phones
# Country Dropdown
tk.Label(root, text="Country:", anchor="w", width=15).grid(row=4, column=0, sticky="w")
country_dropdown = ttk.Combobox(root, values=list(number_formats.keys()))
country_dropdown.grid(row=4, column=1, sticky="ew")

# Phone Number Field
tk.Label(root, text="Phone:", anchor="w", width=15).grid(row=5, column=0, sticky="w")
entry_phone1 = tk.Entry(root, width=30)
entry_phone1.grid(row=5, column=1, sticky="ew")
entry_phone1.bind("<Return>", lambda event: correct_and_copy_phone(entry_phone1))

# Fax Number Field
tk.Label(root, text="Fax:", anchor="w", width=15).grid(row=6, column=0, sticky="w")
entry_phone2 = tk.Entry(root, width=30)
entry_phone2.grid(row=6, column=1, sticky="ew")
entry_phone2.bind("<Return>", lambda event: correct_and_copy_phone(entry_phone2))

#Address
tk.Label(root, text="Address:", anchor="w", width=15).grid(row=7, column=0, sticky="w", padx=5, pady=5)
text_area_address = tk.Text(root, height=3, width=30)
text_area_address.grid(row=7, column=1, padx=5, pady=5, sticky="w")
preview_text_area = tk.Text(root, height=3, width=20, state=tk.DISABLED, fg="blue")
preview_text_area.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

text_area_address.bind("<KeyRelease>", preview_address)
text_area_address.bind("<Return>", update_address)

# Resizeable buttons in column 2
tk.Button(root, text="Bio", command=copy_bio, width=5).grid(row=3, column=2, sticky="ew", padx=5, pady=5)
tk.Button(root, text="LinkedIn", command=copy_linkedin, width=5).grid(row=4, column=2, sticky="ew", padx=5, pady=5)
tk.Button(root, text="Website", command=copy_website, width=5).grid(row=5, column=2, sticky="ew", padx=5, pady=5)
tk.Button(root, text="Email", command=copy_email, width=5).grid(row=6, column=2, sticky="ew", padx=5, pady=5)

tk.Button(root, text="Clear All", width=30, command=lambda: 
          [entry_company.delete(0, tk.END), 
           entry_job_title.delete(0, tk.END), 
           entry_email.delete(0, tk.END), 
           entry_link.delete(0, tk.END), 
           entry_phone1.delete(0, tk.END), 
           entry_phone2.delete(0, tk.END), 
           text_area_address.delete("1.0", tk.END)]).grid(row=8, column=0, columnspan=3, sticky="ew")

# Adjust column weights
root.columnconfigure(0, weight=0)  # Labels column fixed
root.columnconfigure(1, weight=0)  # Entry fields column fixed
root.columnconfigure(2, weight=1)  # Buttons column resizable

# Adjust row weights
for i in range(10):  
    root.rowconfigure(i, weight=1)  # Ensure elements remain visible
root.rowconfigure(7, weight=2)  # Give extra space to preview

# Bind resize event
root.bind("<Configure>", adjust_font)
root.bind("<Configure>", adjust_widgets)
root.mainloop()
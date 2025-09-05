import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger, PdfReader
from tqdm import tqdm
from datetime import datetime
import urllib.parse
import re
from dateutil.parser import parse

# Default URL
DEFAULT_PAGE_URL = "https://www.actuariesindia.org/question-paper-solutions"
BASE_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(BASE_DOWNLOAD_FOLDER, exist_ok=True)

# Date range configuration
START_DATE = datetime(2019, 6, 1)  # June 2019
END_DATE = datetime(2025, 5, 31)   # May 2025

def create_run_folder():
    """Create a timestamped run folder with an 'individuals' subfolder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(BASE_DOWNLOAD_FOLDER, f"session_{timestamp}")
    individuals_folder = os.path.join(run_folder, "individuals")
    os.makedirs(individuals_folder, exist_ok=True)
    return run_folder, individuals_folder

def update_page_param(url, page):
    """Update the 'page' parameter in the URL dynamically."""
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    qs["page"] = [str(page)]
    new_query = urllib.parse.urlencode(qs, doseq=True)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def parse_session_date(session_text):
    """Parse session date from text like 'June 2018' or 'Sep-2005'."""
    try:
        # Handle various date formats
        session_text = session_text.strip().replace("_", " ").replace("-", " ")
        
        # Try parsing common formats
        if re.match(r'\w+\s+\d{4}', session_text):
            return parse(session_text, fuzzy=True)
        elif re.match(r'\w{3}\s+\d{4}', session_text):
            return parse(session_text, fuzzy=True)
        else:
            # Extract month and year using regex
            match = re.search(r'(\w+)\s*(\d{4})', session_text)
            if match:
                month_year = f"{match.group(1)} {match.group(2)}"
                return parse(month_year, fuzzy=True)
    except:
        pass
    return None

def is_date_in_range(session_date):
    """Check if session date is within our target range (June 2005 to September 2018)."""
    if not session_date:
        return False
    return START_DATE <= session_date <= END_DATE

def get_filter_options(base_url):
    """Get available year and subject filter options."""
    response = requests.get(f"{base_url}/question-paper-solutions", verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Look for year dropdown
    year_options = []
    year_select = soup.find("select", {"name": "field_year_target_id"})
    if year_select:
        options = year_select.find_all("option")
        for opt in options:
            if opt.get("value") and opt.get("value") != "All":
                year_text = opt.text.strip()
                year_options.append((opt.get("value"), year_text))
    
    # Look for subject dropdown
    subject_options = []
    subject_select = soup.find("select", {"name": "field_subject_target_id"})
    if subject_select:
        options = subject_select.find_all("option")
        for opt in options:
            if opt.get("value") and opt.get("value") != "All":
                subject_text = opt.text.strip()
                print(f"Found subject option: {subject_text} (value: {opt.get('value')})")
                subject_options.append((opt.get("value"), subject_text))
    
    if not year_options or not subject_options:
        print("Checking all select elements...")
        selects = soup.find_all("select")
        for i, select in enumerate(selects):
            print(f"Select {i}: name='{select.get('name')}', id='{select.get('id')}'")
            for opt in select.find_all("option")[:5]:  # First 5 options
                print(f"  Option: {opt.text.strip()} (value: {opt.get('value')})")
    
    return year_options, subject_options

def get_pdf_links(page_url, base_url, page_num=0):
    """Extract PDF links from the given page URL, filtering by date range."""
    response = requests.get(page_url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Debug: Print page structure only for first few pages
    if page_num <= 1:
        print(f"🔍 Page title: {soup.title.text if soup.title else 'No title'}")
        tables = soup.find_all("table")
        print(f"🔍 Found {len(tables)} tables on page")
    
    rows = soup.select("table.views-table tbody tr")
    if not rows:
        # Try alternative selectors
        rows = soup.select("table tbody tr")
        if not rows:
            rows = soup.select("tr")
    
    if page_num <= 1:
        print(f"🔍 Found {len(rows)} rows total")
    
    pdf_links = []
    
    for i, row in enumerate(rows):
        cols = row.find_all("td")
        print(f"  Row {i}: {len(cols)} columns")
        
        if i < 2 and page_num < 2:  # Show first 2 rows for first 2 pages only
            for j, col in enumerate(cols):
                print(f"    Col {j}: {col.text.strip()[:50]}")
        
        if len(cols) < 5:
            continue
            
        session = cols[2].text.strip()
        session_date = parse_session_date(session)
        print(f"  Session: {session}, Parsed date: {session_date}")
        
        # Skip if date is outside our range
        if not is_date_in_range(session_date):
            print(f"  Skipping {session} - outside date range")
            continue
            
        session_clean = session.replace(" ", "_")
        
        question_link = cols[3].find("a")
        solution_link = cols[4].find("a")
        
        question_url = base_url + question_link["href"] if question_link else None
        solution_url = base_url + solution_link["href"] if solution_link else None
        
        pdf_links.append((session_clean, question_url, solution_url, session_date))
        print(f"  ✅ Added {session} to download list")
    
    return pdf_links

def is_valid_pdf(file_path):
    """Check if a downloaded file is a valid PDF."""
    try:
        PdfReader(file_path)
        return True
    except:
        return False

def download_pdf(url, filename, folder):
    """Download a PDF file and validate it."""
    if not url:
        return None

    filepath = os.path.join(folder, filename)
    response = requests.get(url, stream=True, verify=False)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    
    with open(filepath, "wb") as f, tqdm(
        total=total_size, unit="B", unit_scale=True, desc=filename, leave=False
    ) as progress_bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                progress_bar.update(len(chunk))

    if not is_valid_pdf(filepath):
        print(f"⚠️ Invalid/corrupt PDF detected: {filename}. Skipping.")
        os.remove(filepath)
        return None
    
    return filepath

def merge_pdfs(pdfs, output_filename, output_folder):
    """Merge multiple PDFs into one, ensuring all are valid."""
    merger = PdfMerger()
    valid_pdfs = [pdf for pdf in pdfs if pdf and is_valid_pdf(pdf)]
    
    if not valid_pdfs:
        print("❌ No valid PDFs to merge.")
        return None

    for pdf in valid_pdfs:
        merger.append(pdf)
    
    output_path = os.path.join(output_folder, output_filename)
    merger.write(output_path)
    merger.close()
    print(f"✅ Merged PDF saved: {output_path}")
    return output_path

def get_user_inputs():
    """Get user inputs for date range and subject."""
    print("=" * 60)
    print("🎓 ACTUARIES INDIA - QUESTION PAPERS & SOLUTIONS DOWNLOADER")
    print("=" * 60)
    
    # Get date range
    print("\n📅 DATE RANGE SELECTION:")
    print("Please enter the date range (format: MMM YYYY)")
    print("Examples: 'Jun 2005', 'Sep 2018', 'May 2025'")
    
    while True:
        try:
            start_date_str = input("\nEnter START date (e.g., 'Jun 2005'): ").strip()
            end_date_str = input("Enter END date (e.g., 'Sep 2018'): ").strip()
            
            start_date = parse_session_date(start_date_str)
            end_date = parse_session_date(end_date_str)
            
            if not start_date or not end_date:
                print("❌ Invalid date format. Please use format like 'Jun 2005' or 'Sep 2018'")
                continue
                
            if start_date > end_date:
                print("❌ Start date should be earlier than end date")
                continue
                
            break
        except Exception as e:
            print(f"❌ Error parsing dates: {e}")
            print("Please try again with format like 'Jun 2005'")
    
    return start_date, end_date, start_date_str, end_date_str

def select_subject(subject_options):
    """Allow user to select a subject from available options."""
    print("\n📚 SUBJECT SELECTION:")
    print("Available subjects:")
    
    # Group subjects by category for better display
    categories = {
        'Core Principles (CP)': [],
        'Core Mathematics (CM)': [],
        'Core Statistics (CS)': [],
        'Core Business (CB)': [],
        'Specialist Principles (SP)': [],
        'Specialist Advanced (SA)': [],
        'Core Technical (CT)': [],
        'Specialist Technical (ST)': [],
        'Others': []
    }
    
    for value, text in subject_options:
        if text.startswith('CP'):
            categories['Core Principles (CP)'].append((value, text))
        elif text.startswith('CM'):
            categories['Core Mathematics (CM)'].append((value, text))
        elif text.startswith('CS'):
            categories['Core Statistics (CS)'].append((value, text))
        elif text.startswith('CB'):
            categories['Core Business (CB)'].append((value, text))
        elif text.startswith('SP'):
            categories['Specialist Principles (SP)'].append((value, text))
        elif text.startswith('SA'):
            categories['Specialist Advanced (SA)'].append((value, text))
        elif text.startswith('CT'):
            categories['Core Technical (CT)'].append((value, text))
        elif text.startswith('ST'):
            categories['Specialist Technical (ST)'].append((value, text))
        else:
            categories['Others'].append((value, text))
    
    # Display subjects by category
    subject_map = {}
    counter = 1
    
    for category, subjects in categories.items():
        if subjects:
            print(f"\n📖 {category}:")
            for value, text in subjects:
                print(f"  {counter:2d}. {text}")
                subject_map[counter] = (value, text)
                counter += 1
    
    while True:
        try:
            choice = int(input(f"\nSelect subject (1-{counter-1}): "))
            if choice in subject_map:
                return subject_map[choice]
            else:
                print(f"❌ Please enter a number between 1 and {counter-1}")
        except ValueError:
            print("❌ Please enter a valid number")

def main():
    """Main function to handle PDF scraping, downloading, and merging."""
    try:
        base_url = "https://www.actuariesindia.org"
        
        # Get user inputs
        start_date, end_date, start_date_str, end_date_str = get_user_inputs()
        
        # Update global date range
        global START_DATE, END_DATE
        START_DATE = start_date
        END_DATE = end_date
        
        print(f"\n🎯 Target date range: {start_date_str} to {end_date_str}")
        print(f"📊 Will download and merge in decreasing chronological order")
        
        # Get available filter options
        print("\n🔍 Checking available filters...")
        year_options, subject_options = get_filter_options(base_url)
        
        # Let user select subject
        subject_id, subject_name = select_subject(subject_options)
        print(f"\n✅ Selected subject: {subject_name}")
        
        # Extract subject code for filename
        subject_code = subject_name.split()[0].replace('-', '').replace(':', '')
        
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled by user")
        return
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return
    
    run_folder, individuals_folder = create_run_folder()
    all_pdf_data = []
    
    if not year_options:
        print("⚠️ No year filters found, falling back to basic URL")
        page_url = DEFAULT_PAGE_URL
        # Fallback to original pagination method
        page = 0
        while page < 21:  # Safety limit
            current_page_url = update_page_param(page_url, page)
            print(f"\n🔍 Scraping page {page}: {current_page_url}")
            
            try:
                pdf_data = get_pdf_links(current_page_url, base_url, page)
                if pdf_data:
                    all_pdf_data.extend(pdf_data)
                    print(f"📋 Found {len(pdf_data)} sessions in target date range")
                page += 1
            except Exception as e:
                print(f"❌ Error fetching page {page}: {e}")
                break
    else:
        # Filter years within our target range and process each
        target_years = []
        start_year = START_DATE.year
        end_year = END_DATE.year
        
        for value, text in year_options:
            try:
                if any(str(y) in text for y in range(start_year, end_year + 1)):
                    session_date = parse_session_date(text)
                    if session_date and is_date_in_range(session_date):
                        target_years.append((value, text, session_date))
                        print(f"📅 Will process: {text}")
            except Exception as e:
                print(f"Error parsing {text}: {e}")
        
        # Sort target years in reverse chronological order (newest first)
        target_years.sort(key=lambda x: x[2], reverse=True)
        
        if not target_years:
            print(f"\n❌ No sessions found in the date range {start_date_str} to {end_date_str}")
            print("💡 Try a different date range or check if the website has data for those dates.")
            return
        
        print(f"\n📊 Processing {len(target_years)} sessions...")
        
        # Process each year filter with selected subject
        for value, text, session_date in target_years:
            year_url = f"{base_url}/question-paper-solutions?field_year_target_id={value}&field_subject_target_id={subject_id}"
            print(f"\n🔍 Processing {text} for {subject_code}: {year_url}")
            
            try:
                pdf_data = get_pdf_links(year_url, base_url, 0)
                if pdf_data:
                    all_pdf_data.extend(pdf_data)
                    print(f"📋 Found {len(pdf_data)} {subject_code} sessions for {text}")
                else:
                    print(f"📋 No {subject_code} sessions found for {text}")
            except Exception as e:
                print(f"❌ Error fetching {text}: {e}")

    if not all_pdf_data:
        print("❌ No PDFs found in the specified date range.")
        return

    # Sort by date in decreasing order (newest first: Sep 2018 -> Jun 2005)
    all_pdf_data.sort(key=lambda x: x[3], reverse=True)
    print(f"\n📈 Total sessions found: {len(all_pdf_data)}")
    
    all_downloaded_pdfs = []
    print("📥 Downloading PDFs in chronological order...")
    
    for session, q_url, s_url, session_date in tqdm(all_pdf_data, desc="Processing sessions", unit="session"):
        date_str = session_date.strftime("%Y-%m") if session_date else "Unknown"
        print(f"  📄 Processing {session} ({date_str})")
        
        # Download question paper first, then solution
        if q_url:
            q_filename = f"{session}_Question.pdf"
            q_file = download_pdf(q_url, q_filename, individuals_folder)
            if q_file:
                all_downloaded_pdfs.append(q_file)
        if s_url:
            s_filename = f"{session}_Solution.pdf"
            s_file = download_pdf(s_url, s_filename, individuals_folder)
            if s_file:
                all_downloaded_pdfs.append(s_file)

    if all_downloaded_pdfs:
        # Create a clean filename
        start_str = start_date_str.replace(' ', '').replace('-', '')
        end_str = end_date_str.replace(' ', '').replace('-', '')
        output_filename = f"Actuaries_{subject_code}_{start_str}_to_{end_str}_Merged.pdf"
        
        print(f"\n📂 Merging {len(all_downloaded_pdfs)} {subject_code} PDFs into one file...")
        final_path = merge_pdfs(all_downloaded_pdfs, output_filename, run_folder)
        
        if final_path:
            print(f"\n🎉 SUCCESS! Your merged PDF is ready:")
            print(f"📄 File: {output_filename}")
            print(f"📍 Location: {final_path}")
            print(f"📊 Total PDFs merged: {len(all_downloaded_pdfs)}")
            print(f"📚 Subject: {subject_name}")
            print(f"📅 Date range: {start_date_str} to {end_date_str}")
    else:
        print(f"❌ No valid {subject_code} PDFs downloaded.")

if __name__ == "__main__":
    main()

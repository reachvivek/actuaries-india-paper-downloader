# 🎓 Actuaries India - Question Papers & Solutions Downloader

A user-friendly Python application that automatically downloads and merges actuarial exam papers from the Institute of Actuaries of India website.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📅 **Custom Date Range**: Select any date range (e.g., Jun 2005 to Sep 2018)
- 📚 **All Subjects**: Choose from 40+ available subjects (ST, SP, CT, CP, CM, CS, CB, SA, CA)
- 🔄 **Auto-Merge**: Downloads and merges question papers + solutions into one PDF
- 📊 **Organized**: PDFs are sorted in decreasing chronological order
- 🎯 **User-Friendly**: Interactive menu-driven interface
- ✅ **Validation**: Checks PDF integrity and skips corrupt files
- 📁 **Clean Output**: Organized folder structure with timestamps

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection

### Windows Setup

1. **Download or Clone this repository**
   ```bash
   git clone <repository-url>
   cd PdfMerger
   ```

2. **Run the setup script** (automatically installs dependencies)
   ```bash
   python app.py
   ```
   
   *The first run will automatically install required packages if missing.*

### Manual Setup (if needed)

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   python app.py
   ```

## 📖 How to Use

### Step 1: Run the Application
```bash
python app.py
```

### Step 2: Enter Date Range
```
📅 DATE RANGE SELECTION:
Please enter the date range (format: MMM YYYY)
Examples: 'Jun 2005', 'Sep 2018', 'May 2025'

Enter START date (e.g., 'Jun 2005'): Jun 2005
Enter END date (e.g., 'Sep 2018'): Sep 2018
```

### Step 3: Select Subject
The application will show all available subjects organized by category:
```
📚 SUBJECT SELECTION:
Available subjects:

📖 Core Principles (CP):
   1. CP1A - Actuarial Practice
   2. CP1B - Actuarial Practice
   3. CP2A - Actuarial Modelling

📖 Specialist Technical (ST):
  15. ST1 - Health and Care Insurance
  16. ST2 - Life Insurance
  17. ST6 - Finance and Investment B

Select subject (1-45): 17
```

### Step 4: Wait for Download & Merge
The application will:
- Find all available sessions in your date range
- Download question papers and solutions
- Merge everything into one PDF file
- Show progress with real-time updates

### Step 5: Get Your PDF
```
🎉 SUCCESS! Your merged PDF is ready:
📄 File: Actuaries_ST6_Jun2005_to_Sep2018_Merged.pdf
📍 Location: D:\PdfMerger\downloads\session_20241205_143022\Actuaries_ST6_Jun2005_to_Sep2018_Merged.pdf
📊 Total PDFs merged: 54
📚 Subject: ST6 - Finance and Investment B
📅 Date range: Jun 2005 to Sep 2018
```

## 📂 Output Structure

```
downloads/
├── session_20241205_143022/          # Timestamped session folder
│   ├── individuals/                  # Individual PDF files
│   │   ├── June_2005_Question.pdf
│   │   ├── June_2005_Solution.pdf
│   │   ├── November_2005_Question.pdf
│   │   └── ...
│   └── Actuaries_ST6_Jun2005_to_Sep2018_Merged.pdf  # Final merged PDF
```

## 🎯 Example Use Cases

### For Students
```bash
# Get all ST-6 papers for preparation
Start: Jun 2005
End: Sep 2018
Subject: ST6 - Finance and Investment B
```

### For Reference
```bash
# Get recent SP-6 papers
Start: Jun 2019
End: May 2025
Subject: SP6 - Financial Derivatives
```

### For Complete Study
```bash
# Get all CT-1 papers ever available
Start: Nov 2005
End: Nov 2024
Subject: CT1 - Financial Mathematics
```

## 📚 Available Subjects

The application supports all subjects available on the Actuaries India website:

**Core Subjects:**
- CP (Core Principles): Actuarial Practice, Actuarial Modelling, Communication
- CM (Core Mathematics): Actuarial Mathematics, Financial Engineering
- CS (Core Statistics): Actuarial Statistics, Risk Modelling
- CB (Core Business): Business Finance, Business Economics, Business Management

**Specialist Subjects:**
- ST (Specialist Technical): Health Insurance, Life Insurance, General Insurance, Pensions, Finance & Investment
- SP (Specialist Principles): Health & Care, Life Insurance, Pensions, Investment & Finance, Financial Derivatives, General Insurance
- SA (Specialist Advanced): Advanced versions of specialist subjects

**Legacy Subjects:**
- CT (Core Technical): Financial Mathematics, Finance, Statistics, Models, Economics
- CA (Core Applications): Risk Management, Communications

## ⚠️ Important Notes

1. **Internet Required**: Application downloads files from actuariesindia.org
2. **Large Downloads**: Some date ranges may result in 100+ MB downloads
3. **Processing Time**: Larger ranges take more time (typically 1-5 minutes)
4. **PDF Validation**: Corrupt PDFs are automatically skipped
5. **Respectful Usage**: Application includes reasonable delays between requests

## 🛠️ Troubleshooting

### Common Issues

**"No PDFs found in the specified date range"**
- Check if the website has papers for those dates
- Try a broader date range
- Verify subject availability for that time period

**"SSL Certificate Error"**
- The application handles this automatically
- If issues persist, check your internet connection

**"Module not found" errors**
- Run: `pip install -r requirements.txt`
- Make sure Python 3.7+ is installed

**Slow downloads**
- Normal for large date ranges
- Application shows progress bars
- Can be interrupted with Ctrl+C

## 📋 Requirements

Automatically installed dependencies:
- `requests` - For web scraping
- `beautifulsoup4` - For parsing HTML
- `PyPDF2` - For PDF operations
- `tqdm` - For progress bars
- `python-dateutil` - For date parsing

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest new features
- Submit improvements
- Share with fellow actuaries

## 📄 License

This project is for educational purposes. Please respect the Institute of Actuaries of India's terms of service.

## 🙏 Acknowledgments

- Institute of Actuaries of India for providing question papers
- Python community for excellent libraries
- Fellow actuaries who inspired this tool

---

**Happy studying! 📚✨**

*Made with ❤️ for the actuarial community*
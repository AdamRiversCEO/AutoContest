# AutoContest

**Automated Sweepstakes & Contest Entry Tool**

*by Adam Rivers — A product of Hello Security LLC Research Labs*

AutoContest is a Python-based tool that automates the process of finding and entering online sweepstakes and contests. It scrapes contest URLs from a curated list of aggregator sites, automatically fills out entry forms, and handles both POST and GET submissions, with support for CAPTCHA solving. The tool provides live progress updates and a user-friendly interface using the `rich` library.

## Features

- **Automated Contest Discovery**: Scrapes contest URLs from a comprehensive list of aggregator sites (e.g., SweepstakesFanatics, ContestGirl) and automatically updates the list by scraping hub sites for new aggregators.
- **Form Submission**: Supports both POST and GET form submissions, with robust field mapping for user details (name, email, address, etc.) and handling of inputs, selects, textareas, checkboxes, and radio buttons.
- **CAPTCHA Support**: Detects and solves reCAPTCHA and hCAPTCHA using 2Captcha (requires API key and library installation).
- **Live Output**: Displays real-time progress bars for scraping and form submission using the `rich` library.
- **User Details Management**: Allows users to input and save personal details (e.g., name, email, address) to `config.json` for reuse.
- **Error Handling**: Minimizes errors like 404s by using `urljoin` for accurate URLs and checks response text for success indicators (e.g., "thank you", "success").
- **Menu-Driven Interface**: Offers options to run automation, view results, enter user details, update aggregator URLs, or exit.
- **Logging**: Saves detailed logs to `automation.log` for debugging and tracking.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AdamRiversCEO/AutoContest.git
   cd AutoContest
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.7+ installed, then install the required packages:
   ```bash
   pip install requests aiohttp beautifulsoup4 rich
   ```
   For CAPTCHA support, install the optional 2Captcha library:
   ```bash
   pip install 2captcha-python
   ```

3. **Set Up Configuration**:
   - The script creates a `config.json` file on first run with default settings.
   - Optionally, add a 2Captcha API key to `config.json` for CAPTCHA solving:
     ```json
     "twocaptcha_api_key": "your-api-key-here"
     ```

## Usage

1. **Run the Script**:
   ```bash
   python autocontest.py
   ```

2. **Main Menu Options**:
   - **[1] Run Automation**: Updates aggregator URLs (if enabled), scrapes contest URLs, and submits entry forms.
   - **[2] View Last Results**: Displays results from the last automation run, saved in `contest-results.json`.
   - **[3] Enter User Details**: Prompts for personal details (name, email, address, etc.) and saves them to `config.json`.
   - **[4] Update Aggregator URLs**: Automatically scrapes hub sites to find and add new contest aggregator URLs.
   - **[5] Exit**: Closes the program.

3. **Example Workflow**:
   - Select `[3]` to enter your details (saved for future runs).
   - Select `[4]` to update the aggregator list (optional, as it runs automatically with `[1]`).
   - Select `[1]` to scrape contests and submit entries, with live progress updates.
   - View results with `[2]` to see success/failure details.

## Configuration

The `config.json` file stores:
- **aggregator_urls**: A list of contest aggregator sites (e.g., SweepstakesFanatics, HGTV). Automatically updated via the `[4]` menu option.
- **field_mappings**: Maps form field names to user data fields.
- **user_data**: Stores user details (e.g., name, email, address) for form filling.
- **max_retries**: Number of retry attempts for form submissions (default: 3).
- **twocaptcha_api_key**: API key for 2Captcha (optional, for CAPTCHA solving).

Example `config.json`:
```json
{
  "aggregator_urls": [
    "https://www.sweepstakesfanatics.com/",
    "https://www.contestgirl.com/",
    ...
  ],
  "field_mappings": {
    "first_name": "first_name",
    "last_name": "last_name",
    "email": "email",
    ...
  },
  "user_data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "example@email.com",
    ...
  },
  "max_retries": 3,
  "twocaptcha_api_key": ""
}
```

## Important Notes

- **CAPTCHA Handling**: Without a 2Captcha API key, the script skips forms with CAPTCHAs. Obtain a key from [2Captcha](https://2captcha.com/) and add it to `config.json`.
- **JavaScript Limitations**: The script uses `BeautifulSoup` for scraping and form submission, which doesn't handle JavaScript-heavy forms. For such cases, consider integrating Selenium (not included).
- **Performance**: The large number of aggregator URLs may increase runtime. Adjust `max_retries` or add rate-limiting if needed.
- **Error Handling**: The script minimizes errors (e.g., 404s) by using `urljoin` and checking response text for success indicators. Check `automation.log` for detailed error reports.
- **Maintenance**: Aggregator and hub site URLs may change. Periodically run `[4]` to update the aggregator list.

## Legal and Ethical Considerations

- **Compliance**: Ensure that automating entries complies with the terms of service of each contest site. Some sites prohibit automated submissions.
- **Responsible Use**: Use the tool responsibly to avoid overwhelming servers or violating rules. The authors are not responsible for misuse.
- **Data Privacy**: Only enter personal details you are comfortable sharing with contest sites.

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, contact Adam Rivers at Hello Security LLC Research Labs via [officialadamrivers@gmail.com](mailto:officialadamrivers@gmail.com).

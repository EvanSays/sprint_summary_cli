# Sprint Summary CLI

A Python CLI tool that generates a summary of your completed JIRA tickets and GitHub PR reviews for a given date range.

## Features

- Fetch completed JIRA tickets within a custom date range
- Fetch GitHub PR reviews within a custom date range
- Interactive prompts for start and end dates
- Flexible date input (specific date or days back)
- Clean, formatted output with clickable URLs

## Requirements

- Python 3.7 or higher
- JIRA account with API access
- GitHub account with Personal Access Token

## Installation

1. Clone or download this repository

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or with a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```
   JIRA_URL=https://yourcompany.atlassian.net
   JIRA_EMAIL=your.email@company.com
   JIRA_API_TOKEN=your_jira_api_token
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_personal_access_token
   ```

### Getting API Tokens

**JIRA API Token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name and copy the token

**GitHub Personal Access Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" (classic)
3. Select scopes:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories only)
4. Generate and copy the token

## Usage

### Basic Usage

Run the script:
```bash
python sprint_summary.py
```

You'll be prompted to enter:
1. **Start date** - Enter a date (YYYY-MM-DD) or number of days back (e.g., `14`)
2. **End date** - Enter a date (YYYY-MM-DD) or press Enter for today

### Output Formats

**Detailed format** (default) - Shows full details with emojis and formatted sections:
```bash
python sprint_summary.py
```

**Concise format** - Plain text format optimized for copy/paste to Lattice or other tools:
```bash
python sprint_summary.py --concise
```

### Example - Detailed Output:
```
📅 Enter the sprint start date

Start date (YYYY-MM-DD) or days back (e.g., '14'): 14
Using start date: 2024-10-17

📅 Enter the sprint end date

End date (YYYY-MM-DD) or press Enter for today:
Using end date: 2024-10-31

============================================================
📊 SPRINT SUMMARY
📅 Date Range: 2024-10-17 to 2024-10-31
============================================================

✅ COMPLETED JIRA TICKETS
------------------------------------------------------------
PROJ-123: Implement user authentication
   https://yourcompany.atlassian.net/browse/PROJ-123

PROJ-124: Fix login bug
   https://yourcompany.atlassian.net/browse/PROJ-124

Total: 2 ticket(s)

============================================================

👀 GITHUB PR REVIEWS
------------------------------------------------------------
✅ [repo-name] #456: Add new feature
   https://github.com/org/repo-name/pull/456

🔄 [another-repo] #789: Update dependencies
   https://github.com/org/another-repo/pull/789

Total: 2 PR(s) reviewed

============================================================
```

### Example - Concise Output:
```
📅 Enter the sprint start date

Start date (YYYY-MM-DD) or days back (e.g., '14'): 14
Using start date: 2024-10-17

📅 Enter the sprint end date

End date (YYYY-MM-DD) or press Enter for today:
Using end date: 2024-10-31

Completed JIRA Tickets:
PROJ-123: Implement user authentication - https://yourcompany.atlassian.net/browse/PROJ-123
PROJ-124: Fix login bug - https://yourcompany.atlassian.net/browse/PROJ-124

GitHub PR Reviews:
repo-name #456: Add new feature - https://github.com/org/repo-name/pull/456
another-repo #789: Update dependencies - https://github.com/org/another-repo/pull/789
```

The concise format is designed for easy copy/paste into Lattice or other performance review tools.

## Troubleshooting

**ModuleNotFoundError: No module named 'requests'**
- Make sure you've installed the dependencies: `pip install -r requirements.txt`

**Missing required environment variables**
- Ensure your `.env` file exists and contains all required variables
- Check that there are no extra spaces or quotes around values

**No tickets/PRs found**
- Verify your API tokens are correct and have the necessary permissions
- Check that the date range includes the period you're looking for
- Ensure your JIRA tickets are assigned to you and marked as "Done"

## License

MIT

#!/usr/bin/env python3
"""
Sprint Summary Generator
Fetches completed JIRA tickets and GitHub PR reviews for the current sprint.
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Dict
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SprintSummary:
    def __init__(self, start_date: datetime, end_date: datetime):
        # JIRA configuration
        jira_url = os.getenv('JIRA_URL', '')
        self.jira_url = jira_url.rstrip('/')  # Remove trailing slash
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')

        # GitHub configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')

        # Date range
        self.start_date = start_date
        self.end_date = end_date

        self.validate_config()

    def validate_config(self):
        """Validate that all required environment variables are set."""
        missing = []

        if not self.jira_url:
            missing.append('JIRA_URL')
        if not self.jira_email:
            missing.append('JIRA_EMAIL')
        if not self.jira_token:
            missing.append('JIRA_API_TOKEN')
        if not self.github_token:
            missing.append('GITHUB_TOKEN')
        if not self.github_username:
            missing.append('GITHUB_USERNAME')

        if missing:
            print("❌ Missing required environment variables:")
            for var in missing:
                print(f"   - {var}")
            print("\nPlease set these variables and try again.")
            sys.exit(1)

    def get_completed_jira_tickets(self) -> List[Dict]:
        """Fetch JIRA tickets completed in the date range."""
        # Format dates for JQL
        start_str = self.start_date.strftime('%Y-%m-%d')
        end_str = self.end_date.strftime('%Y-%m-%d')

        # JQL query to find tickets completed by the user in date range
        jql = f'assignee = currentUser() AND status = Done AND updated >= "{start_str}" AND updated <= "{end_str}"'

        url = f'{self.jira_url}/rest/api/3/search/jql'
        auth = HTTPBasicAuth(self.jira_email, self.jira_token)

        params = {
            'jql': jql,
            'fields': 'summary,status,key,updated',
            'maxResults': 100
        }

        try:
            response = requests.get(url, auth=auth, params=params)
            response.raise_for_status()
            data = response.json()

            tickets = []
            for issue in data.get('issues', []):
                tickets.append({
                    'key': issue['key'],
                    'summary': issue['fields']['summary'],
                    'status': issue['fields']['status']['name'],
                    'url': f"{self.jira_url}/browse/{issue['key']}"
                })

            return tickets

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching JIRA tickets: {e}")
            return []

    def get_github_pr_reviews(self) -> List[Dict]:
        """Fetch GitHub PR reviews by the user in the date range."""
        # Search for PRs reviewed by the user
        start_str = self.start_date.strftime('%Y-%m-%d')
        end_str = self.end_date.strftime('%Y-%m-%d')

        # GitHub Search API query
        query = f'is:pr reviewed-by:{self.github_username} updated:{start_str}..{end_str}'

        url = 'https://api.github.com/search/issues'
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        params = {
            'q': query,
            'sort': 'updated',
            'order': 'desc',
            'per_page': 100
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            prs = []
            for item in data.get('items', []):
                prs.append({
                    'number': item['number'],
                    'title': item['title'],
                    'repo': item['repository_url'].split('/')[-1],
                    'state': item['state'],
                    'url': item['html_url'],
                    'updated': item['updated_at']
                })

            return prs

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching GitHub PR reviews: {e}")
            return []

    def print_summary(self):
        """Generate and print the sprint summary."""
        start_str = self.start_date.strftime('%Y-%m-%d')
        end_str = self.end_date.strftime('%Y-%m-%d')

        print("=" * 60)
        print("📊 SPRINT SUMMARY")
        print(f"📅 Date Range: {start_str} to {end_str}")
        print("=" * 60)
        print()

        # JIRA tickets
        print("✅ COMPLETED JIRA TICKETS")
        print("-" * 60)
        tickets = self.get_completed_jira_tickets()

        if tickets:
            for ticket in tickets:
                print(f"{ticket['key']}: {ticket['summary']}")
                print(f"   {ticket['url']}")
                print()
            print(f"Total: {len(tickets)} ticket(s)")
        else:
            print("No completed tickets found in date range.")

        print()
        print("=" * 60)
        print()

        # GitHub PR reviews
        print("👀 GITHUB PR REVIEWS")
        print("-" * 60)
        prs = self.get_github_pr_reviews()

        if prs:
            for pr in prs:
                state_emoji = "✅" if pr['state'] == 'closed' else "🔄"
                print(f"{state_emoji} [{pr['repo']}] #{pr['number']}: {pr['title']}")
                print(f"   {pr['url']}")
                print()
            print(f"Total: {len(prs)} PR(s) reviewed")
        else:
            print("No PR reviews found in date range.")

        print()
        print("=" * 60)

    def print_concise_summary(self):
        """Generate and print a concise summary for Lattice."""
        # JIRA tickets
        print("Completed JIRA Tickets:")
        tickets = self.get_completed_jira_tickets()

        if tickets:
            for ticket in tickets:
                print(f"{ticket['key']}: {ticket['summary']} - {ticket['url']}")
        else:
            print("None")

        print()

        # GitHub PR reviews
        print("GitHub PR Reviews:")
        prs = self.get_github_pr_reviews()

        if prs:
            for pr in prs:
                print(f"{pr['repo']} #{pr['number']}: {pr['title']} - {pr['url']}")
        else:
            print("None")


def get_start_date() -> datetime:
    """Prompt user for start date."""
    print("📅 Enter the sprint start date")
    print()

    while True:
        date_input = input("Start date (YYYY-MM-DD) or days back (e.g., '14'): ").strip()

        # Check if input is a number (days back)
        if date_input.isdigit():
            days_back = int(date_input)
            start_date = datetime.now() - timedelta(days=days_back)
            print(f"Using start date: {start_date.strftime('%Y-%m-%d')}")
            print()
            return start_date

        # Try to parse as date
        try:
            start_date = datetime.strptime(date_input, '%Y-%m-%d')
            print(f"Using start date: {start_date.strftime('%Y-%m-%d')}")
            print()
            return start_date
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD or enter number of days back.")
            print()


def get_end_date() -> datetime:
    """Prompt user for end date."""
    print("📅 Enter the sprint end date")
    print()

    while True:
        date_input = input("End date (YYYY-MM-DD) or press Enter for today: ").strip()

        # If empty, use today
        if not date_input:
            end_date = datetime.now()
            print(f"Using end date: {end_date.strftime('%Y-%m-%d')}")
            print()
            return end_date

        # Try to parse as date
        try:
            end_date = datetime.strptime(date_input, '%Y-%m-%d')
            print(f"Using end date: {end_date.strftime('%Y-%m-%d')}")
            print()
            return end_date
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD or press Enter for today.")
            print()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Generate a summary of completed JIRA tickets and GitHub PR reviews'
    )
    parser.add_argument(
        '--concise',
        action='store_true',
        help='Output in concise format for easy copy/paste to Lattice'
    )
    args = parser.parse_args()

    start_date = get_start_date()
    end_date = get_end_date()
    summary = SprintSummary(start_date, end_date)

    if args.concise:
        summary.print_concise_summary()
    else:
        summary.print_summary()


if __name__ == '__main__':
    main()

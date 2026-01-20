#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Track token usage and estimated costs per session/command.
Logs to .claude/metrics/ for analysis.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Any, Optional

METRICS_DIR = Path('.claude/metrics')
DAILY_LOG = METRICS_DIR / 'daily'
SUMMARY_FILE = METRICS_DIR / 'usage_summary.json'

# Approximate costs per 1M tokens (adjust as needed)
PRICING = {
    'claude-3-haiku': {'input': 0.25, 'output': 1.25},
    'claude-3-5-sonnet': {'input': 3.0, 'output': 15.0},
    'claude-3-opus': {'input': 15.0, 'output': 75.0},
    'claude-sonnet-4': {'input': 3.0, 'output': 15.0},
    'claude-opus-4': {'input': 15.0, 'output': 75.0},
    'claude-opus-4-5': {'input': 15.0, 'output': 75.0},
}


class CostTracker:
    """Track and log token usage costs."""

    def __init__(self):
        METRICS_DIR.mkdir(parents=True, exist_ok=True)
        DAILY_LOG.mkdir(parents=True, exist_ok=True)

    def log_session(self, session_data: Dict[str, Any]):
        """Log a session's usage."""
        today = date.today().isoformat()
        daily_file = DAILY_LOG / f'{today}.json'

        # Load existing daily data
        if daily_file.exists():
            daily_data = json.loads(daily_file.read_text())
        else:
            daily_data = {'date': today, 'sessions': [], 'totals': {}}

        # Add session
        daily_data['sessions'].append({
            'session_id': session_data.get('session_id', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'commands': session_data.get('commands', []),
            'duration_seconds': session_data.get('duration', 0),
        })

        # Save
        daily_file.write_text(json.dumps(daily_data, indent=2))

    def get_daily_summary(self, day: Optional[str] = None) -> Dict[str, Any]:
        """Get usage summary for a day."""
        day = day or date.today().isoformat()
        daily_file = DAILY_LOG / f'{day}.json'

        if not daily_file.exists():
            return {'date': day, 'sessions': 0, 'commands': {}}

        data = json.loads(daily_file.read_text())
        return {
            'date': day,
            'sessions': len(data.get('sessions', [])),
            'commands': self._count_commands(data),
        }

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get usage summary for the past 7 days."""
        from datetime import timedelta

        today = date.today()
        total_sessions = 0
        command_counts: Dict[str, int] = {}
        days_active = 0

        for i in range(7):
            day = (today - timedelta(days=i)).isoformat()
            daily_file = DAILY_LOG / f'{day}.json'

            if daily_file.exists():
                days_active += 1
                data = json.loads(daily_file.read_text())
                total_sessions += len(data.get('sessions', []))

                for cmd, count in self._count_commands(data).items():
                    command_counts[cmd] = command_counts.get(cmd, 0) + count

        return {
            'period': 'week',
            'days_active': days_active,
            'sessions': total_sessions,
            'commands': command_counts,
        }

    def get_monthly_report(self) -> str:
        """Generate monthly usage report."""
        current_month = date.today().strftime('%Y-%m')

        total_sessions = 0
        command_counts: Dict[str, int] = {}
        days_active = 0

        for daily_file in DAILY_LOG.glob(f'{current_month}-*.json'):
            days_active += 1
            data = json.loads(daily_file.read_text())
            total_sessions += len(data.get('sessions', []))

            for cmd, count in self._count_commands(data).items():
                command_counts[cmd] = command_counts.get(cmd, 0) + count

        report = f"""
──────────────────────────────────────────────────
📊 MONTHLY USAGE REPORT - {current_month}
──────────────────────────────────────────────────

Days Active:    {days_active}
Total Sessions: {total_sessions}

Command Usage:
"""
        for cmd, count in sorted(command_counts.items(), key=lambda x: -x[1]):
            report += f"  • {cmd}: {count}\n"

        report += """
──────────────────────────────────────────────────
"""
        return report

    def _count_commands(self, data: Dict) -> Dict[str, int]:
        """Count commands in daily data."""
        counts: Dict[str, int] = {}
        for session in data.get('sessions', []):
            for cmd in session.get('commands', []):
                counts[cmd] = counts.get(cmd, 0) + 1
        return counts


def format_usage_output(tracker: CostTracker) -> str:
    """Format usage for display."""
    summary = tracker.get_daily_summary()

    output = "\n" + "─" * 50 + "\n"
    output += "📊 TODAY'S USAGE\n"
    output += "─" * 50 + "\n"
    output += f"Sessions: {summary['sessions']}\n"

    if summary['commands']:
        output += "Commands:\n"
        for cmd, count in summary['commands'].items():
            output += f"  • {cmd}: {count}\n"

    output += "─" * 50 + "\n"

    return output


def main():
    """Hook entry point - runs on Stop event."""
    try:
        input_data = json.load(sys.stdin)

        tracker = CostTracker()

        # Log session
        tracker.log_session({
            'session_id': input_data.get('session_id', 'unknown'),
            'commands': input_data.get('commands', []),
            'duration': input_data.get('duration', 0),
        })

        # Output daily summary
        print(format_usage_output(tracker))

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

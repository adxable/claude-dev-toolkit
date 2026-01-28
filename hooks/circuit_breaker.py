#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Circuit breaker for autonomous loops.
Prevents runaway execution and API budget burn.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Tuple

# Configuration (can be overridden via flags)
DEFAULT_MAX_ITERATIONS = 50
DEFAULT_MAX_CALLS_PER_HOUR = 100
STAGNATION_THRESHOLD = 3  # Loops with no file changes
ERROR_REPEAT_THRESHOLD = 5  # Same error repeated

STATE_FILE = Path('.claude/circuit_breaker_state.json')


class CircuitBreaker:
    """
    Three-state circuit breaker:
    - CLOSED: Normal operation
    - HALF_OPEN: Testing recovery
    - OPEN: Stopped, requires reset
    """

    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
        return self._initial_state()

    def _initial_state(self) -> dict:
        return {
            'status': 'CLOSED',
            'iterations': 0,
            'calls_this_hour': 0,
            'hour_started': datetime.now().isoformat(),
            'consecutive_no_changes': 0,
            'last_error': None,
            'error_repeat_count': 0,
            'trip_reason': None,
            'history': []
        }

    def _save_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(self.state, indent=2))

    def should_continue(self, max_iterations: int = DEFAULT_MAX_ITERATIONS) -> Tuple[bool, Optional[str]]:
        """Check if execution should continue."""

        # Circuit open
        if self.state['status'] == 'OPEN':
            return False, f"Circuit OPEN: {self.state.get('trip_reason', 'Manual stop')}"

        # Iteration limit
        if self.state['iterations'] >= max_iterations:
            self._trip(f"Max iterations ({max_iterations}) reached")
            return False, f"Max iterations ({max_iterations}) reached"

        # Rate limit (hourly reset)
        hour_start = datetime.fromisoformat(self.state['hour_started'])
        if datetime.now() - hour_start > timedelta(hours=1):
            self.state['calls_this_hour'] = 0
            self.state['hour_started'] = datetime.now().isoformat()

        if self.state['calls_this_hour'] >= DEFAULT_MAX_CALLS_PER_HOUR:
            minutes_left = 60 - (datetime.now() - hour_start).seconds // 60
            return False, f"Rate limit ({DEFAULT_MAX_CALLS_PER_HOUR}/hour) - resets in {minutes_left} min"

        # Stagnation detection
        if self.state['consecutive_no_changes'] >= STAGNATION_THRESHOLD:
            self._trip(f"Stagnation: {STAGNATION_THRESHOLD} loops with no changes")
            return False, f"Stagnation detected ({STAGNATION_THRESHOLD} loops with no file changes)"

        # Repeated errors
        if self.state['error_repeat_count'] >= ERROR_REPEAT_THRESHOLD:
            self._trip(f"Repeated error: {self.state['last_error'][:50] if self.state['last_error'] else 'unknown'}")
            return False, f"Same error repeated {ERROR_REPEAT_THRESHOLD} times"

        return True, None

    def record_iteration(self, files_changed: int, error: Optional[str] = None):
        """Record iteration result."""
        self.state['iterations'] += 1
        self.state['calls_this_hour'] += 1

        # Track stagnation
        if files_changed == 0:
            self.state['consecutive_no_changes'] += 1
        else:
            self.state['consecutive_no_changes'] = 0

        # Track repeated errors
        if error:
            if error == self.state['last_error']:
                self.state['error_repeat_count'] += 1
            else:
                self.state['last_error'] = error
                self.state['error_repeat_count'] = 1
        else:
            self.state['last_error'] = None
            self.state['error_repeat_count'] = 0

        # History (last 50)
        self.state['history'].append({
            'iteration': self.state['iterations'],
            'files_changed': files_changed,
            'error': error[:100] if error else None,
            'timestamp': datetime.now().isoformat()
        })
        self.state['history'] = self.state['history'][-50:]

        self._save_state()

    def _trip(self, reason: str):
        """Open the circuit breaker."""
        self.state['status'] = 'OPEN'
        self.state['trip_reason'] = reason
        self._save_state()

    def reset(self):
        """Reset circuit breaker."""
        self.state = self._initial_state()
        self._save_state()

    def get_status(self) -> str:
        """Get formatted status."""
        trip_line = f"\nTrip Reason:    {self.state['trip_reason']}" if self.state['trip_reason'] else ""
        return f"""
──────────────────────────────────────────────────
🔌 CIRCUIT BREAKER STATUS
──────────────────────────────────────────────────
Status:         {self.state['status']}
Iterations:     {self.state['iterations']}
Calls/Hour:     {self.state['calls_this_hour']}/{DEFAULT_MAX_CALLS_PER_HOUR}
No-Change Runs: {self.state['consecutive_no_changes']}/{STAGNATION_THRESHOLD}
Error Repeats:  {self.state['error_repeat_count']}/{ERROR_REPEAT_THRESHOLD}{trip_line}
──────────────────────────────────────────────────
"""


def main():
    """Hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Apply to /ralph and /ship
        is_ralph = '/ralph' in prompt or '/adx:ralph' in prompt
        is_ship = '/ship' in prompt or '/adx:ship' in prompt

        if not is_ralph and not is_ship:
            sys.exit(0)

        # Check for reset flag (applies to both commands)
        if '--reset' in prompt:
            cb = CircuitBreaker()
            cb.reset()
            print("[circuit-breaker] Reset complete")
            sys.exit(0)

        # Check for status flag (circuit breaker status)
        if '--cb-status' in prompt:
            cb = CircuitBreaker()
            print(cb.get_status())
            sys.exit(0)

        # Normal check
        cb = CircuitBreaker()
        can_continue, reason = cb.should_continue()

        if not can_continue:
            cmd = "ralph" if is_ralph else "ship"
            print(f"""
──────────────────────────────────────────────────
🛑 CIRCUIT BREAKER TRIGGERED
──────────────────────────────────────────────────
{reason}

Options:
  /{cmd} --status   View detailed status
  /{cmd} --reset    Reset circuit breaker
  Fix issues manually, then retry
──────────────────────────────────────────────────
""")
            sys.exit(1)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

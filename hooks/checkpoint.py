#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Checkpoint system for /ship command.
Creates restore points after each phase for rollback/resume.
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

CHECKPOINT_DIR = Path('.claude/checkpoints')


class CheckpointManager:
    """Manage checkpoints for /ship workflow."""

    def __init__(self, ship_id: str):
        self.ship_id = ship_id
        self.checkpoint_file = CHECKPOINT_DIR / f'{ship_id}.json'

    def save(self, phase: str, state: Dict[str, Any]):
        """Save checkpoint after successful phase completion."""
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

        checkpoint = self.load() or {
            'ship_id': self.ship_id,
            'started': datetime.now().isoformat(),
            'phases': {}
        }

        # Save git state for potential rollback
        git_sha = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True, text=True
        ).stdout.strip()

        checkpoint['phases'][phase] = {
            'completed': datetime.now().isoformat(),
            'git_sha': git_sha,
            'state': state
        }
        checkpoint['last_phase'] = phase
        checkpoint['last_updated'] = datetime.now().isoformat()

        self.checkpoint_file.write_text(json.dumps(checkpoint, indent=2))

        print(f"[checkpoint] ✓ Saved after {phase} (git: {git_sha[:7]})")

    def load(self) -> Optional[Dict[str, Any]]:
        """Load existing checkpoint."""
        if self.checkpoint_file.exists():
            return json.loads(self.checkpoint_file.read_text())
        return None

    def get_resume_point(self) -> Optional[str]:
        """Get the phase to resume from."""
        checkpoint = self.load()
        if not checkpoint:
            return None

        phases_order = ['plan', 'implement', 'refactor', 'verify', 'review', 'commit', 'pr']
        last_phase = checkpoint.get('last_phase')

        if last_phase in phases_order:
            idx = phases_order.index(last_phase)
            if idx + 1 < len(phases_order):
                return phases_order[idx + 1]

        return None

    def rollback(self, phase: str) -> bool:
        """Rollback to checkpoint state."""
        checkpoint = self.load()
        if not checkpoint or phase not in checkpoint.get('phases', {}):
            return False

        git_sha = checkpoint['phases'][phase]['git_sha']

        print(f"[checkpoint] Rolling back to {phase} (git: {git_sha[:7]})")
        result = subprocess.run(
            ['git', 'reset', '--hard', git_sha],
            capture_output=True
        )

        return result.returncode == 0

    def list_checkpoints(self) -> Dict[str, str]:
        """List all saved checkpoints."""
        checkpoint = self.load()
        if not checkpoint:
            return {}

        return {
            phase: data['completed']
            for phase, data in checkpoint.get('phases', {}).items()
        }

    def clear(self):
        """Clear checkpoint after successful completion."""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


def format_checkpoint_status(manager: CheckpointManager) -> str:
    """Format checkpoint status for display."""
    checkpoints = manager.list_checkpoints()

    if not checkpoints:
        return "No checkpoints saved"

    output = "\n" + "─" * 50 + "\n"
    output += "📍 CHECKPOINTS\n"
    output += "─" * 50 + "\n\n"

    phases_order = ['plan', 'implement', 'refactor', 'verify', 'review', 'commit', 'pr']

    for phase in phases_order:
        if phase in checkpoints:
            output += f"  ✓ {phase}: {checkpoints[phase]}\n"
        else:
            output += f"  ○ {phase}: not reached\n"

    resume_point = manager.get_resume_point()
    if resume_point:
        output += f"\n  → Resume from: {resume_point}\n"
        output += f"  → Command: /ship --continue\n"

    output += "\n" + "─" * 50 + "\n"

    return output


def get_active_ship_id() -> Optional[str]:
    """Get the active ship ID from the most recent checkpoint file."""
    if not CHECKPOINT_DIR.exists():
        return None

    checkpoint_files = list(CHECKPOINT_DIR.glob('*.json'))
    if not checkpoint_files:
        return None

    # Get most recently modified
    latest = max(checkpoint_files, key=lambda p: p.stat().st_mtime)
    return latest.stem


def main():
    """Hook entry point."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Check for /ship with flags
        if '/ship' not in prompt and '/adx:ship' not in prompt:
            sys.exit(0)

        # Get or create ship ID
        ship_id = get_active_ship_id()
        if not ship_id:
            # Generate new ship ID from timestamp
            ship_id = datetime.now().strftime('%Y%m%d_%H%M%S')

        manager = CheckpointManager(ship_id)

        # Handle --status flag
        if '--status' in prompt:
            print(format_checkpoint_status(manager))
            sys.exit(0)

        # Handle --continue flag
        if '--continue' in prompt:
            resume_point = manager.get_resume_point()
            if resume_point:
                print(f"\n[checkpoint] Resuming from: {resume_point}")
                print(f"[checkpoint] Ship ID: {ship_id}\n")
            else:
                print("\n[checkpoint] No checkpoint found to resume from.\n")
            sys.exit(0)

        # Handle --rollback flag
        if '--rollback' in prompt:
            # Extract phase name from prompt
            parts = prompt.split('--rollback')
            if len(parts) > 1:
                phase = parts[1].strip().split()[0] if parts[1].strip() else None
                if phase and manager.rollback(phase):
                    print(f"\n[checkpoint] Rolled back to: {phase}\n")
                else:
                    print(f"\n[checkpoint] Failed to rollback to: {phase}\n")
            sys.exit(0)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()

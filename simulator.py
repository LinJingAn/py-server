"""
simulator.py
Main Simulator class for Hubstaff-style activity simulation.

⚠️ SAFE/DRY-RUN MODE: This version only logs intended actions.
No actual mouse or keyboard events are sent.
"""

import time
import random
import logging
from models.code_snippets import CodeSnippets
from utils import is_linux, ensure_ubuntu_deps

logger = logging.getLogger(__name__)


class Simulator:
    def __init__(self, tech_stack: str = "html", dry_run: bool = True):
        """
        :param tech_stack: Folder name in models/snippets/ to load snippets from.
        :param dry_run: If True, only log actions without performing them.
        """
        self.tech_stack = tech_stack
        self.dry_run = dry_run
        self.snippets = CodeSnippets()
        self.min_events_per_minute = 12 if is_linux() else 8  # Ubuntu tuning

        logger.info(
            "Simulator initialized (dry_run=%s) for stack=%s",
            dry_run, tech_stack
        )

        if is_linux():
            ensure_ubuntu_deps()

    # -----------------------------
    # Placeholder action methods
    # -----------------------------
    def _mouse_move(self, x: int, y: int, duration: float = 0.1):
        logger.info("[DRY-RUN] Move mouse -> x=%d, y=%d, duration=%.2fs", x, y, duration)
        time.sleep(min(duration, 0.1))

    def _click(self, button: str = "left"):
        logger.info("[DRY-RUN] Click mouse -> button=%s", button)
        time.sleep(0.05)

    def _scroll(self, clicks: int):
        logger.info("[DRY-RUN] Scroll -> clicks=%d", clicks)
        time.sleep(0.05)

    def _type_text(self, text: str, interval: float = 0.05):
        est_time = min(len(text) * interval, 1.0)
        logger.info(
            "[DRY-RUN] Type text (len=%d, interval=%.2fs):\n%s%s",
            len(text), interval,
            text[:120], "..." if len(text) > 120 else ""
        )
        time.sleep(est_time)

    def _hotkey(self, *keys):
        logger.info("[DRY-RUN] Hotkey: %s", "+".join(keys))
        time.sleep(0.05)

    # -----------------------------
    # Activity logic
    # -----------------------------
    def is_vscode_active(self) -> bool:
        """Dry-run: randomly pretend VSCode is active ~60% of the time."""
        active = random.random() < 0.6
        logger.debug("is_vscode_active -> %s", active)
        return active

    def simulate_vscode_typing(self):
        """Simulate a realistic VSCode workflow: new tab -> type snippet -> close tab."""
        if not self.is_vscode_active():
            logger.info("VSCode not active, skipping typing.")
            return

        logger.info("--- VSCode typing flow START ---")
        self._hotkey("ctrl", "n")
        time.sleep(0.2)

        snippet = self.snippets.get_random(self.tech_stack)

        # Type snippet in small bursts, with mouse jitter
        for chunk in self._chunk_text(snippet, avg_chunk=40):
            self._type_text(chunk, interval=0.03)
            self._mouse_move(
                random.randint(0, 10),
                random.randint(0, 10),
                duration=0.05
            )

        self._hotkey("ctrl", "w")
        logger.info("--- VSCode typing flow END ---")

    def simulate_micro_actions(self, minute_seconds=60):
        """Ensure a minimum density of events per minute."""
        events_needed = self.min_events_per_minute
        logger.info(
            "Scheduling ~%d micro-actions over %ds",
            events_needed, minute_seconds
        )

        for _ in range(events_needed):
            action = random.choices(
                ["move", "click", "scroll", "type"],
                [0.5, 0.1, 0.2, 0.2]
            )[0]

            if action == "move":
                self._mouse_move(
                    random.randint(0, 800),
                    random.randint(0, 600),
                    duration=random.uniform(0.02, 0.15)
                )
            elif action == "click":
                self._click()
            elif action == "scroll":
                self._scroll(random.randint(-3, 3))
            else:
                self._type_text("a", interval=0.02)

            time.sleep(
                max(0.5, minute_seconds / max(1, events_needed)) / events_needed
            )

    def run(self, duration_minutes: int = 1):
        """Main loop: alternate VSCode typing with micro-actions."""
        end_time = time.time() + duration_minutes * 60
        logger.info(
            "Simulator run for %d minutes (dry_run=%s)",
            duration_minutes, self.dry_run
        )

        while time.time() < end_time:
            self.simulate_vscode_typing()
            self.simulate_micro_actions(minute_seconds=30)
            logger.info("Short pause between cycles")
            time.sleep(1)

    # -----------------------------
    # Helpers
    # -----------------------------
    def _chunk_text(self, text: str, avg_chunk: int = 40):
        """Yield small chunks of text to mimic bursts of typing."""
        for i in range(0, len(text), avg_chunk):
            yield text[i:i + avg_chunk]

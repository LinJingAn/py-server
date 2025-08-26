
import pyautogui
import random
import time
import math
from datetime import datetime, timedelta
import subprocess
import os
from typing import List, Tuple, Optional
# -------------------------------------------------------------------------
try:
    import uinput  # type: ignore
    LOW_LEVEL_AVAILABLE = True
except ImportError:
    LOW_LEVEL_AVAILABLE = False

try:
    from Xlib import display, X
    from Xlib.error import XError
    XLIB_AVAILABLE = True
except ImportError:
    XLIB_AVAILABLE = False
    print("Warning: python-xlib not available. Some features may be limited.")

pyautogui.FAILSAFE = True

class Simulator:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_activity_time = datetime.now()
        self.activity_level = 0.0
        self.current_window: Optional[str] = None
        self.window_list: List[Tuple[str, str]] = []
        self.last_written_pattern = ""
        self.display_env = self._detect_display_server()
        self.ui_device = None
        if LOW_LEVEL_AVAILABLE and os.geteuid() == 0:
            try:
                events = [
                    # Mouse relative & buttons
                    uinput.REL_X,
                    uinput.REL_Y,
                    uinput.REL_WHEEL,
                    uinput.BTN_LEFT,
                    uinput.BTN_RIGHT,
                    uinput.KEY_BACKSPACE,
                    uinput.KEY_SPACE,
                    uinput.KEY_ENTER,
                    uinput.KEY_TAB,
                ] + [getattr(uinput, f"KEY_{c.upper()}") for c in "abcdefghijklmnopqrstuvwxyz"]

                self.ui_device = uinput.Device(events, name="sim-virt")
                time.sleep(0.1)
            except Exception as exc:
                print(f"[uinput] Failed to create virtual device: {exc}")
                self.ui_device = None
        self.update_window_list()

    def _detect_display_server(self) -> str:
        if os.environ.get("WAYLAND_DISPLAY"):
            return "wayland"
        elif os.environ.get("DISPLAY"):
            return "x11"
        return "unknown"

    def update_window_list(self) -> None:
        self.window_list.clear()
        try:
            if self.display_env == "x11" and XLIB_AVAILABLE:
                self._update_window_list_x11()
            else:
                self._update_window_list_wmctrl()
        except Exception as exc:
            print(f"Error updating window list: {exc}")
            self._update_window_list_wmctrl()

    def _update_window_list_x11(self) -> None:
        try:
            d = display.Display()
            root = d.screen().root
            window_ids = root.get_full_property(
                d.intern_atom("_NET_CLIENT_LIST"), X.AnyPropertyType
            ).value
            for win_id in window_ids:
                try:
                    window = d.create_resource_object("window", win_id)
                    title_prop = window.get_full_property(
                        d.intern_atom("_NET_WM_NAME"), X.AnyPropertyType
                    )
                    if title_prop and title_prop.value:
                        title = title_prop.value.decode("utf-8")
                        if self._is_valid_window(title):
                            self.window_list.append((str(win_id), title))
                except (XError, UnicodeDecodeError, AttributeError):
                    continue
        except Exception as exc:
            print(f"X11 window enumeration failed: {exc}")
            self._update_window_list_wmctrl()

    def _update_window_list_wmctrl(self) -> None:
        try:
            result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if not line:
                        continue
                    parts = line.split(None, 3)
                    if len(parts) >= 4:
                        win_id, title = parts[0], parts[3]
                        if self._is_valid_window(title):
                            self.window_list.append((win_id, title))
        except (subprocess.SubprocessError, FileNotFoundError):
            print("wmctrl not available. Window enumeration is limited.")

    def _is_valid_window(self, title: str) -> bool:
        if not title:
            return False
        exclude_kw = [
            "desktop",
            "panel",
            "dock",
            "taskbar",
            "notification",
            "tray",
            "unity",
            "gnome",
            "kde",
            "plasma",
            "conky",
            "compiz",
            "window list",
            "workspace",
            "activities",
            "overview",
            "screenshot",
            "screen",
            "lock",
            "login",
            "gdm",
            "lightdm",
            "slack",
            "hubstaff",
        ]
        lower = title.lower()
        return not any(kw in lower for kw in exclude_kw)

    def _ll_move(self, dx: int, dy: int):
        if self.ui_device and (dx or dy):
            self.ui_device.emit(uinput.REL_X, dx, syn=False)
            self.ui_device.emit(uinput.REL_Y, dy)

    def _ll_scroll(self, amount: int):
        if self.ui_device and amount:
            self.ui_device.emit(uinput.REL_WHEEL, amount)

    def _ll_click(self):
        if self.ui_device:
            self.ui_device.emit(uinput.BTN_LEFT, 1)  # press
            self.ui_device.emit(uinput.BTN_LEFT, 0)  # release

    _KEY_MAP = {c: getattr(uinput, f"KEY_{c.upper()}") for c in "abcdefghijklmnopqrstuvwxyz"} if LOW_LEVEL_AVAILABLE else {}
    _KEY_MAP.update({
        " ": uinput.KEY_SPACE if LOW_LEVEL_AVAILABLE else None,
        "enter": uinput.KEY_ENTER if LOW_LEVEL_AVAILABLE else None,
        "tab": uinput.KEY_TAB if LOW_LEVEL_AVAILABLE else None,
        "backspace": uinput.KEY_BACKSPACE if LOW_LEVEL_AVAILABLE else None,
        "shift": uinput.KEY_LEFTSHIFT if LOW_LEVEL_AVAILABLE else None,
    })

    def _ll_keypress(self, key: str):
        if not self.ui_device:
            return
        kc = self._KEY_MAP.get(key.lower())
        if kc is None:
            return
        self.ui_device.emit(kc, 1, syn=False)
        self.ui_device.emit(kc, 0)

    def _press_key(self, key: str):
        if self.ui_device:
            self._ll_keypress(key)
        else:
            pyautogui.press(key)


    def get_active_window(self) -> Optional[str]:
        try:
            if self.display_env == "x11" and XLIB_AVAILABLE:
                return self._get_active_window_x11()
            return self._get_active_window_wmctrl()
        except Exception as exc:
            print(f"Error obtaining active window: {exc}")
            return None

    def _get_active_window_x11(self) -> Optional[str]:
        try:
            d = display.Display()
            root = d.screen().root
            active = root.get_full_property(
                d.intern_atom("_NET_ACTIVE_WINDOW"), X.AnyPropertyType
            )
            if active and active.value:
                win_id = active.value[0]
                win = d.create_resource_object("window", win_id)
                title_prop = win.get_full_property(
                    d.intern_atom("_NET_WM_NAME"), X.AnyPropertyType
                )
                if title_prop and title_prop.value:
                    return title_prop.value.decode("utf-8")
        except Exception:
            pass
        return None

    def _get_active_window_wmctrl(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        return None


    def _active_contains(self, needles) -> bool:
        if not self.current_window:
            return False
        lower = self.current_window.lower()
        return any(n in lower for n in needles)

    def is_chrome_active(self) -> bool:
        return self._active_contains([
            "google chrome",
            "chromium",
            "chrome",
            "firefox",
            "mozilla firefox",
        ]) 

    def is_cursor_ide_active(self) -> bool:
        return self._active_contains([
            "cursor",
            "visual studio code",
            "vscode",
            "code",
            "atom",
            "sublime",
        ])


    def _activate_window(self, win_id: str) -> None:
        try:
            if self.display_env == "x11":
                subprocess.run([
                    "wmctrl",
                    "-i",
                    "-a",
                    str(win_id),
                ], capture_output=True)
            else:
                subprocess.run([
                    "wmctrl",
                    "-i",
                    "-a",
                    str(win_id),
                ], capture_output=True)
        except Exception as exc:
            print(f"Error activating window {win_id}: {exc}")

    def _get_window_geometry(self) -> Optional[Tuple[int, int, int, int]]:
        if not self.current_window:
            return None
        for win_id, title in self.window_list:
            if title == self.current_window:
                try:
                    res = subprocess.run(
                        ["xwininfo", "-i", str(win_id)],
                        capture_output=True,
                        text=True,
                    )
                    if res.returncode != 0:
                        break
                    geom_str = res.stdout.strip().split("\n")
                    geom = {}
                    for line in geom_str:
                        if "x" in line:
                            k, v = line.split(":", 1)
                            geom[k.strip()] = int(v.strip())
                    if all(k in geom for k in ("x", "y", "width", "height")):
                        return geom["x"], geom["y"], geom["width"], geom["height"]
                except Exception:
                    pass
                break
        return None


    def simulate_scroll(self):
        for _ in range(random.randint(2, 5)):
            scroll_amt = random.randint(-100, 100)
            steps = random.randint(2, 4)
            for _ in range(steps):
                pyautogui.scroll(scroll_amt // steps)
                self._ll_scroll(scroll_amt // steps)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.1, 0.3))

    def natural_mouse_movement(self):
        margin = 20  # stay this many pixels away from edges to avoid tri
        start_x, start_y = pyautogui.position()

        def near_corner(x, y):
            return (
                (x < margin and y < margin) or
                (x < margin and y > self.screen_height - margin) or
                (x > self.screen_width - margin and y < margin) or
                (x > self.screen_width - margin and y > self.screen_height - margin)
            )

        # If cursor is already in a fail-safe corner, temporarily disable FAILSAFE to move it away.
        if near_corner(start_x, start_y):
            safe_x, safe_y = self.screen_width // 2, self.screen_height // 2
            orig_flag = pyautogui.FAILSAFE
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(safe_x, safe_y, duration=0.15)
            pyautogui.FAILSAFE = orig_flag
            start_x, start_y = safe_x, safe_y

        # Calculate modest destination keeping margin from screen borders.
        # Reduce the travel distance so cursor movements stay more subtle
        max_delta = 60  # pixels (was 150)
        dx = random.randint(-max_delta, max_delta)
        dy = random.randint(-max_delta, max_delta)

        end_x = max(margin, min(self.screen_width - margin, start_x + dx))
        end_y = max(margin, min(self.screen_height - margin, start_y + dy))
        steps = random.randint(10, 20)
        for i in range(steps):
            prog = i / steps
            ease = 0.5 - math.cos(prog * math.pi) / 2
            x = start_x + (end_x - start_x) * ease
            y = start_y + (end_y - start_y) * ease
            pyautogui.moveTo(x, y, duration=0.005)
            self._ll_move(int(x - start_x), int(y - start_y))
            time.sleep(random.uniform(0.001, 0.005))

    def switch_chrome_tabs(self):
        if not self.is_chrome_active():
            return
        for _ in range(random.randint(1, 3)):
            pyautogui.hotkey("ctrl", "tab")
            time.sleep(random.uniform(0.2, 0.5))

    def switch_cursor_files(self):
        if not self.is_cursor_ide_active():
            return
        pyautogui.hotkey("ctrl", "p")
        time.sleep(random.uniform(0.3, 0.5))
        patterns = [
            ".tsx",
            ".jsx",
            ".ts",
            ".js",
            "use",
            "get",
            "set",
            "handle",
            "create",
            "fetch",
            "update",
            "delete",
            "Button",
            "Modal",
            "Form",
            "Input",
            "Card",
            "Header",
            "Footer",
            "Nav",
            "Layout",
            "Page",
            "Component",
            "Hook",
            "Context",
            "Provider",
            "src/",
            "components/",
            "pages/",
            "hooks/",
            "utils/",
            "lib/",
            "api/",
        ]
        for _ in range(random.randint(1, 2)):
            pat = random.choice(patterns)
            for char in pat:
                self._press_key(char)
                time.sleep(random.uniform(0.12, 0.25))
            time.sleep(random.uniform(0.2, 0.4))
        if random.random() < 0.4:
            for _ in range(random.randint(1, 3)):
                self._press_key('down')
                time.sleep(random.uniform(0.1, 0.2))
        self._press_key("enter")
        time.sleep(random.uniform(0.2, 0.4))

    def switch_window(self):
        if not self.window_list:
            self.update_window_list()
            if not self.window_list:
                return
        available = [w for w in self.window_list if w[1] != self.current_window]
        if not available:
            return
        win_id, title = random.choice(available)
        self.current_window = title
        self._activate_window(win_id)
        time.sleep(random.uniform(0.5, 1.0))
        if self.is_chrome_active():
            if random.random() < 0.7:
                self.switch_chrome_tabs()
        elif self.is_cursor_ide_active():
            if random.random() < 0.6:
                self.switch_cursor_files()

    def delete_last_written_code(self):
        for _ in range(len(self.last_written_pattern)):
            self._press_key('backspace')
            time.sleep(random.uniform(0.05, 0.15))

    def simulate_coding_activity(self):
        if not self.is_cursor_ide_active():
            return
        patterns = [
            "const HomePage = () => {",
            "const UserProfile = ({ user }: { user: User }) => {",
            "const [isLoading, setIsLoading] = useState<boolean>(false)",
            "useEffect(() => { fetchUserData() }, [userId])",
            "const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {",
            "interface User { id: string; name: string; email: string }",
            "return ( <div className=\"container mx-auto px-4\">",
            "return isLoading ? <LoadingSpinner /> : <UserProfile user={user} />",
            "const filteredProducts = products.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))",
            "try { const response = await api.fetchUser(userId); setUser(response.data) }",
            "const useAuth = () => { const [user, setUser] = useState(null); return { user, login, logout } }",
        ]
        self.last_written_pattern = pat = random.choice(patterns)
        for char in pat:
            self._press_key(char)
            time.sleep(random.uniform(0.12, 0.25))
        time.sleep(random.uniform(0.5, 1.0))
        self.delete_last_written_code()

    def update_activity_level(self):
        base = random.uniform(0.4, 0.5)
        t_factor = time.time() % 3600
        variation = math.sin(t_factor / 600) * 0.15
        target = max(0.3, min(0.55, base + variation))
        while abs(self.activity_level - target) > 0.01:
            self.activity_level += (target - self.activity_level) * 0.15
            time.sleep(0.08)

    def simulate_break(self):
        """Simulate a natural break in activity"""
        break_duration = random.uniform(60, 120)
        time.sleep(break_duration)

    def choose_mixed_input_activity(self) -> str:
        choices = [("mouse", 0.35), ("keyboard", 0.25), ("mixed", 0.4)]
        r = random.random()
        cum = 0
        for typ, wt in choices:
            cum += wt
            if r <= cum:
                return typ
        return "mixed"

    def execute_activity(self, input_type: str):
        if input_type == "mouse":
            rnd = random.random()
            if rnd < 0.6:
                self.simulate_scroll()
            elif rnd < 0.9:
                self.natural_mouse_movement()
            else:
                pyautogui.click()
                self._ll_click()
        elif input_type == "keyboard":
            if self.is_cursor_ide_active():
                if random.random() < 0.8:
                    self.simulate_coding_activity()
                else:
                    self.switch_cursor_files()
            else:
                if random.random() < 0.5:
                    pyautogui.hotkey("ctrl", "f")
                    time.sleep(random.uniform(0.2, 0.5))
                    self._press_key("escape")
        else:  # mixed
            r = random.random()
            if r < 0.4:
                self.simulate_scroll()
            elif r < 0.7:
                self.natural_mouse_movement()
            elif r < 0.9:
                if self.is_cursor_ide_active():
                    self.simulate_coding_activity()
                elif self.is_chrome_active():
                    self.switch_chrome_tabs()
            else:
                pyautogui.click()
                self._ll_click()
                time.sleep(random.uniform(0.1, 0.3))
                if random.random() < 0.3:
                    for _ in range(random.randint(1, 3)):
                        self._press_key(random.choice(['tab', 'space', 'enter']))
                        time.sleep(random.uniform(0.1, 0.2))


    def run(self, duration_minutes: Optional[int] = 60):
        end_time: Optional[datetime]
        if duration_minutes is None or duration_minutes <= 0:
            end_time = None
        else:
            end_time = datetime.now() + timedelta(minutes=duration_minutes)

        start_time = datetime.now()
        last_input_type = None
        input_type_duration = 0

        print(f"🚀 Starting Hubstaff-safe activity simulation for {duration_minutes} minutes")
        print("📊 Activity patterns designed to avoid suspicious detection")

        while end_time is None or datetime.now() < end_time:
            current_time = datetime.now()

            if random.random() < 0.1:
                self.update_window_list()
                active = self.get_active_window()
                if active:
                    self.current_window = active
            if random.random() < random.uniform(0.25, 0.45):
                self.switch_window()
            elif self.is_chrome_active() and random.random() < 0.3:
                self.switch_chrome_tabs()
            elif self.is_cursor_ide_active() and random.random() < 0.3:
                self.switch_cursor_files()

            current_input_type = self.choose_mixed_input_activity()

            if current_input_type == last_input_type:
                input_type_duration += 1
            else:
                input_type_duration = 0
                last_input_type = current_input_type

            if input_type_duration > 120:
                print("🔄 Switching input type to avoid single input detection")
                current_input_type = "mixed" if current_input_type in ["keyboard", "mouse"] else "mouse"
                input_type_duration = 0

            self.execute_activity(current_input_type)

            self.update_activity_level()

            if random.random() < 0.03:
                self.simulate_break()
                # schedule next one 5–10 minutes ahead
                self.next_long_break = current_time + timedelta(minutes=random.uniform(5, 10))

            # Occasional short break chance
            if random.random() < 0.05:
                self.simulate_break()

            delay = random.uniform(0.5, 2.5)
            time.sleep(delay)

if __name__ == "__main__":
    simulator = Simulator()
    try:
        simulator.run(duration_minutes=None)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")

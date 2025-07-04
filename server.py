import pyautogui
import random
import time
import math
from datetime import datetime, timedelta
import platform
import psutil

# Platform-specific imports
if platform.system() == "Windows":
    import win32gui
    import win32con
    import win32process
else:
    # Linux/Ubuntu alternatives
    import subprocess
    import re
    import os

# Safety feature - move mouse to corner to stop
pyautogui.FAILSAFE = True

class Simulator:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_activity_time = datetime.now()
        self.activity_level = 0.0  # 0.0 to 1.0
        self.current_window = None
        self.window_list = []
        self.platform = platform.system()
        
        # Scroll position tracking
        self.scroll_position = 0  # 0 = top, positive = scrolled down
        self.max_scroll_position = 1000  # Arbitrary max scroll position
        self.scroll_threshold = 800  # When to start scrolling up
        
        self.update_window_list()
        
    def update_window_list(self):
        """Update the list of visible windows"""
        self.window_list = []
        
        if self.platform == "Windows":
            def callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    # Filter out system windows, settings, and unwanted applications
                    if title and not any(keyword in title.lower() for keyword in [
                        "default ime", "settings", "control panel", "task manager", 
                        "registry editor", "system configuration", "windows security",
                        "device manager", "event viewer", "services", "computer management",
                        "microsoft management console", "windows powershell", "command prompt",
                        "cortana", "search", "start", "taskbar", "notification area",
                        "slack", "hubstaff"
                    ]):
                        windows.append((hwnd, title))
                return True
            
            win32gui.EnumWindows(callback, self.window_list)
            self.window_list = [w for w in self.window_list if w[1]]  # Filter out empty titles
        
        else:
            # Linux/Ubuntu window management using wmctrl
            try:
                # Get list of windows using wmctrl
                result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 4:
                                window_id = parts[0]
                                title = ' '.join(parts[3:])
                                # Filter out system windows and unwanted applications
                                if title and not any(keyword in title.lower() for keyword in [
                                    "desktop", "panel", "dock", "launcher", "notification",
                                    "system settings", "ubuntu software", "software updater",
                                    "terminal", "gnome-terminal", "konsole", "xfce4-terminal",
                                    "slack", "hubstaff"
                                ]):
                                    self.window_list.append((window_id, title))
            except (subprocess.SubprocessError, FileNotFoundError):
                # Fallback: try using xdotool if wmctrl is not available
                try:
                    result = subprocess.run(['xdotool', 'search', '--name', ''], capture_output=True, text=True)
                    if result.returncode == 0:
                        window_ids = result.stdout.strip().split('\n')
                        for window_id in window_ids:
                            if window_id.strip():
                                try:
                                    title_result = subprocess.run(['xdotool', 'getwindowname', window_id], 
                                                                 capture_output=True, text=True)
                                    if title_result.returncode == 0:
                                        title = title_result.stdout.strip()
                                        if title and not any(keyword in title.lower() for keyword in [
                                            "desktop", "panel", "dock", "launcher", "notification",
                                            "system settings", "ubuntu software", "software updater",
                                            "terminal", "gnome-terminal", "konsole", "xfce4-terminal",
                                            "slack", "hubstaff"
                                        ]):
                                            self.window_list.append((window_id, title))
                                except:
                                    continue
                except (subprocess.SubprocessError, FileNotFoundError):
                    # If no window management tools are available, create a basic list
                    self.window_list = [("default", "Default Window")]
    
    def is_chrome_active(self):
        """Check if Google Chrome is the active window"""
        if not self.current_window:
            return False
        return "Google Chrome" in self.current_window

    def is_cursor_ide_active(self):
        """Check if Cursor IDE is the active window"""
        if not self.current_window:
            return False
        return "Cursor" in self.current_window

    def is_vscode_active(self):
        """Check if Visual Studio Code is the active window"""
        if not self.current_window:
            return False
        return "Visual Studio Code" in self.current_window or "Code" in self.current_window

    def switch_chrome_tabs(self):
        """Switch between Chrome tabs using keyboard shortcuts"""
        if not self.is_chrome_active():
            return

        # Randomly decide how many tabs to switch (1-3)
        num_switches = random.randint(1, 3)
        for _ in range(num_switches):
            # Use Ctrl+Tab to switch to next tab
            pyautogui.hotkey('ctrl', 'tab')
            # Slower tab switching on Ubuntu
            if self.platform != "Windows":
                time.sleep(random.uniform(0.4, 0.8))  # Increased delay for Ubuntu
            else:
                time.sleep(random.uniform(0.2, 0.5))

    def switch_cursor_files(self):
        """Switch between Cursor files using keyboard shortcuts"""
        if not self.is_cursor_ide_active():
            return

        # Open file switcher
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(random.uniform(0.3, 0.5))

        # Code file specific search patterns - targeting both React/TypeScript and vanilla JS/HTML
        search_patterns = [
            # File extensions for React/TypeScript, vanilla JS/HTML, and PHP
            '.tsx', '.jsx', '.ts', '.js', '.html', '.css', '.scss', '.sass',
            '.php', '.phtml', '.phar',
            
            # React/TypeScript specific patterns
            'use', 'get', 'set', 'handle', 'create', 'fetch', 'update', 'delete',
            'Button', 'Modal', 'Form', 'Input', 'Card', 'Header', 'Footer', 'Nav',
            'Layout', 'Page', 'Component', 'Hook', 'Context', 'Provider',
            'page', 'layout', 'component', 'hook', 'util', 'service', 'api',
            'store', 'reducer', 'action', 'selector', 'middleware', 'config',
            'index.tsx', 'index.jsx', 'App.tsx', 'App.jsx',
            'layout.tsx', 'page.tsx', 'loading.tsx', 'types.ts',
            
            # Vanilla JavaScript/HTML patterns
            'script', 'main', 'app', 'index', 'utils', 'helpers', 'functions',
            'validation', 'form', 'modal', 'popup', 'menu', 'nav', 'header', 'footer',
            'sidebar', 'content', 'container', 'wrapper', 'section', 'article',
            'button', 'input', 'select', 'textarea', 'label', 'div', 'span',
            'table', 'list', 'item', 'card', 'box', 'panel', 'dialog',
            
            # Common JavaScript function patterns
            'init', 'setup', 'load', 'save', 'export', 'import', 'render',
            'calculate', 'process', 'validate', 'format', 'parse', 'convert',
            'filter', 'sort', 'search', 'find', 'add', 'remove', 'update',
            'show', 'hide', 'toggle', 'open', 'close', 'start', 'stop',
            
            # HTML structure patterns
            'index.html', 'main.html', 'template.html', 'base.html',
            'head', 'body', 'header', 'footer', 'nav', 'main', 'aside',
            'section', 'article', 'div', 'span', 'p', 'h1', 'h2', 'h3',
            
            # CSS/SCSS patterns
            'style', 'styles', 'css', 'scss', 'sass', 'theme', 'variables',
            'layout', 'grid', 'flex', 'responsive', 'mobile', 'desktop',
            'header', 'footer', 'nav', 'sidebar', 'content', 'container',
            'button', 'input', 'form', 'modal', 'popup', 'card', 'list',
            
            # PHP specific patterns
            'class', 'function', 'namespace', 'use', 'require', 'include',
            'public', 'private', 'protected', 'static', 'abstract', 'interface',
            'trait', 'extends', 'implements', 'new', 'return', 'echo', 'print',
            'isset', 'empty', 'unset', 'array', 'string', 'int', 'float', 'bool',
            'null', 'true', 'false', 'try', 'catch', 'throw', 'finally',
            'foreach', 'while', 'for', 'if', 'else', 'elseif', 'switch', 'case',
            'default', 'break', 'continue', 'do', 'while', 'endwhile', 'endif',
            'endforeach', 'endfor', 'endforeach', 'endswitch', 'enddeclare',
            
            # PHP file patterns
            'index.php', 'config.php', 'database.php', 'functions.php',
            'utils.php', 'helpers.php', 'classes.php', 'models.php',
            'controllers.php', 'views.php', 'templates.php', 'api.php',
            'auth.php', 'session.php', 'cookies.php', 'validation.php',
            'form.php', 'mail.php', 'upload.php', 'download.php',
            
            # PHP framework patterns (Laravel, Symfony, CodeIgniter, etc.)
            'app/', 'config/', 'database/', 'resources/', 'routes/',
            'storage/', 'vendor/', 'public/', 'bootstrap/', 'tests/',
            'migrations/', 'seeders/', 'factories/', 'providers/',
            'middleware/', 'controllers/', 'models/', 'views/',
            'layouts/', 'components/', 'partials/', 'templates/',
            
            # PHP Composer patterns
            'composer.json', 'composer.lock', 'autoload.php', 'vendor/',
            'psr-4', 'psr-0', 'require', 'require-dev', 'autoload',
            
            # Common PHP project patterns
            'index.php', 'main.php', 'app.php', 'bootstrap.php',
            'init.php', 'setup.php', 'config.php', 'database.php',
            'connection.php', 'db.php', 'mysql.php', 'pdo.php',
            'session.php', 'auth.php', 'login.php', 'register.php',
            'profile.php', 'admin.php', 'dashboard.php', 'api.php',
            'rest.php', 'ajax.php', 'cron.php', 'cli.php',
            
            # Common directory patterns for all project types
            'src/', 'components/', 'pages/', 'js/', 'css/', 'styles/',
            'utils/', 'helpers/', 'lib/', 'api/', 'assets/', 'images/',
            'public/', 'static/', 'dist/', 'build/', 'node_modules/',
            'includes/', 'classes/', 'functions/', 'templates/',
            
            # Project configuration files
            'package.json', 'package-lock.json', 'yarn.lock', 'webpack.config',
            'vite.config', 'rollup.config', 'babel.config', 'eslint.config',
            'tsconfig.json', 'jsconfig.json', '.env', '.gitignore',
            'composer.json', 'composer.lock', 'phpunit.xml', '.htaccess',
            
            # Common vanilla JS project patterns
            'app.js', 'main.js', 'index.js', 'script.js', 'utils.js',
            'functions.js', 'helpers.js', 'validation.js', 'api.js',
            'dom.js', 'events.js', 'storage.js', 'cookies.js',
            
            # Common HTML project patterns
            'index.html', 'main.html', 'template.html', 'base.html',
            'header.html', 'footer.html', 'nav.html', 'sidebar.html',
        ]
        
        # Type 1-2 search patterns (reduced to avoid too long searches)
        num_patterns = random.randint(1, 2)
        for _ in range(num_patterns):
            pattern = random.choice(search_patterns)
            for char in pattern:
                pyautogui.press(char)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.2, 0.4))

        # Sometimes use arrow keys to navigate through results
        if random.random() < 0.4:  # Increased chance to navigate
            num_arrows = random.randint(1, 3)
            for _ in range(num_arrows):
                pyautogui.press('down')
                time.sleep(random.uniform(0.1, 0.2))

        # Press Enter to select the file
        pyautogui.press('enter')
        time.sleep(random.uniform(0.2, 0.4))

    def switch_vscode_tabs(self):
        """Switch between VS Code tabs using keyboard shortcuts"""
        if not self.is_vscode_active():
            return

        # Randomly decide how many tabs to switch (1-3)
        num_switches = random.randint(1, 3)
        for _ in range(num_switches):
            # Use Ctrl+Tab to switch to next tab in VS Code
            pyautogui.hotkey('ctrl', 'tab')
            # Slower tab switching on Ubuntu
            if self.platform != "Windows":
                time.sleep(random.uniform(0.4, 0.8))  # Increased delay for Ubuntu
            else:
                time.sleep(random.uniform(0.2, 0.5))

    def switch_vscode_files(self):
        """Switch between VS Code files using keyboard shortcuts"""
        if not self.is_vscode_active():
            return

        # Open file switcher in VS Code (Ctrl+P)
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(random.uniform(0.3, 0.5))

        # VS Code file search patterns - targeting common development files
        search_patterns = [
            # File extensions for various programming languages
            '.tsx', '.jsx', '.ts', '.js', '.html', '.css', '.scss', '.sass',
            '.php', '.phtml', '.py', '.java', '.cpp', '.c', '.cs', '.go',
            '.rs', '.rb', '.swift', '.kt', '.scala', '.clj', '.hs', '.ml',
            '.sql', '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
            '.md', '.txt', '.log', '.sh', '.bat', '.ps1', '.dockerfile',
            
            # React/TypeScript specific patterns
            'use', 'get', 'set', 'handle', 'create', 'fetch', 'update', 'delete',
            'Button', 'Modal', 'Form', 'Input', 'Card', 'Header', 'Footer', 'Nav',
            'Layout', 'Page', 'Component', 'Hook', 'Context', 'Provider',
            'page', 'layout', 'component', 'hook', 'util', 'service', 'api',
            'store', 'reducer', 'action', 'selector', 'middleware', 'config',
            'index.tsx', 'index.jsx', 'App.tsx', 'App.jsx',
            'layout.tsx', 'page.tsx', 'loading.tsx', 'types.ts',
            
            # Common file patterns
            'main', 'app', 'index', 'utils', 'helpers', 'functions',
            'validation', 'form', 'modal', 'popup', 'menu', 'nav', 'header', 'footer',
            'sidebar', 'content', 'container', 'wrapper', 'section', 'article',
            'button', 'input', 'select', 'textarea', 'label', 'div', 'span',
            'table', 'list', 'item', 'card', 'box', 'panel', 'dialog',
            
            # Common function patterns
            'init', 'setup', 'load', 'save', 'export', 'import', 'render',
            'calculate', 'process', 'validate', 'format', 'parse', 'convert',
            'filter', 'sort', 'search', 'find', 'add', 'remove', 'update',
            'show', 'hide', 'toggle', 'open', 'close', 'start', 'stop',
            
            # HTML structure patterns
            'index.html', 'main.html', 'template.html', 'base.html',
            'head', 'body', 'header', 'footer', 'nav', 'main', 'aside',
            'section', 'article', 'div', 'span', 'p', 'h1', 'h2', 'h3',
            
            # CSS/SCSS patterns
            'style', 'styles', 'css', 'scss', 'sass', 'theme', 'variables',
            'layout', 'grid', 'flex', 'responsive', 'mobile', 'desktop',
            'header', 'footer', 'nav', 'sidebar', 'content', 'container',
            'button', 'input', 'form', 'modal', 'popup', 'card', 'list',
            
            # Python patterns
            'main.py', 'app.py', 'config.py', 'settings.py', 'utils.py',
            'helpers.py', 'models.py', 'views.py', 'controllers.py',
            'routes.py', 'api.py', 'auth.py', 'database.py', 'db.py',
            'test_', 'tests/', 'test/', '__init__.py', 'requirements.txt',
            
            # Java patterns
            'Main.java', 'App.java', 'Controller.java', 'Service.java',
            'Repository.java', 'Model.java', 'Entity.java', 'Config.java',
            'Application.java', 'Test.java', 'pom.xml', 'build.gradle',
            
            # C/C++ patterns
            'main.c', 'main.cpp', 'app.c', 'app.cpp', 'utils.c', 'utils.cpp',
            'header.h', 'config.h', 'CMakeLists.txt', 'Makefile',
            
            # Common directory patterns
            'src/', 'components/', 'pages/', 'js/', 'css/', 'styles/',
            'utils/', 'helpers/', 'lib/', 'api/', 'assets/', 'images/',
            'public/', 'static/', 'dist/', 'build/', 'node_modules/',
            'includes/', 'classes/', 'functions/', 'templates/',
            
            # Project configuration files
            'package.json', 'package-lock.json', 'yarn.lock', 'webpack.config',
            'vite.config', 'rollup.config', 'babel.config', 'eslint.config',
            'tsconfig.json', 'jsconfig.json', '.env', '.gitignore',
            'composer.json', 'composer.lock', 'phpunit.xml', '.htaccess',
            'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile',
            'pom.xml', 'build.gradle', 'CMakeLists.txt', 'Makefile',
            
            # Common file names
            'app.js', 'main.js', 'index.js', 'script.js', 'utils.js',
            'functions.js', 'helpers.js', 'validation.js', 'api.js',
            'dom.js', 'events.js', 'storage.js', 'cookies.js',
            'index.html', 'main.html', 'template.html', 'base.html',
            'header.html', 'footer.html', 'nav.html', 'sidebar.html',
        ]
        
        # Type 1-2 search patterns (reduced to avoid too long searches)
        num_patterns = random.randint(1, 2)
        for _ in range(num_patterns):
            pattern = random.choice(search_patterns)
            for char in pattern:
                pyautogui.press(char)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(0.2, 0.4))

        # Sometimes use arrow keys to navigate through results
        if random.random() < 0.4:  # Increased chance to navigate
            num_arrows = random.randint(1, 3)
            for _ in range(num_arrows):
                pyautogui.press('down')
                time.sleep(random.uniform(0.1, 0.2))

        # Press Enter to select the file
        pyautogui.press('enter')
        time.sleep(random.uniform(0.2, 0.4))

    def switch_window(self):
        """Switch to a random window and handle special cases for Chrome and Cursor"""
        if not self.window_list:
            self.update_window_list()
            if not self.window_list:
                return
        
        # Choose a different window than current
        available_windows = [w for w in self.window_list if w[1] != self.current_window]
        if not available_windows:
            return
            
        window_id, title = random.choice(available_windows)
        self.current_window = title
        
        # Activate and maximize the window
        if self.platform == "Windows":
            try:
                hwnd = int(window_id, 16) if isinstance(window_id, str) else window_id
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(hwnd)
            except:
                pass
        else:
            # Linux/Ubuntu window activation
            try:
                # Try wmctrl first
                subprocess.run(['wmctrl', '-ia', window_id], check=False)
                subprocess.run(['wmctrl', '-ir', window_id, '-b', 'add,maximized_vert,maximized_horz'], check=False)
            except (subprocess.SubprocessError, FileNotFoundError):
                try:
                    # Fallback to xdotool
                    subprocess.run(['xdotool', 'windowactivate', window_id], check=False)
                    subprocess.run(['xdotool', 'windowmaximize', window_id], check=False)
                except (subprocess.SubprocessError, FileNotFoundError):
                    pass
        
        time.sleep(random.uniform(0.5, 1.0))

        # Handle special cases for Chrome, Cursor, and VS Code
        if self.is_chrome_active():
            if random.random() < 0.7:  # 70% chance to switch tabs when Chrome is active
                self.switch_chrome_tabs()
        elif self.is_cursor_ide_active():
            if random.random() < 0.6:  # 60% chance to switch files when Cursor is active
                self.switch_cursor_files()
        elif self.is_vscode_active():
            if random.random() < 0.6:  # 60% chance to switch tabs when VS Code is active
                self.switch_vscode_tabs()
            elif random.random() < 0.4:  # 40% chance to switch files when VS Code is active
                self.switch_vscode_files()
    
    def simulate_scroll(self):
        """Simulate natural scrolling behavior with bottom detection"""
        # More frequent small scrolls
        num_scrolls = random.randint(2, 5)  # Do multiple scrolls in sequence
        
        for _ in range(num_scrolls):
            # Check if we're near the bottom and should scroll up
            if self.scroll_position >= self.scroll_threshold:
                # Scroll up a little bit to simulate natural behavior
                scroll_amount = random.randint(-50, -20)  # Scroll up
                self.scroll_position = max(0, self.scroll_position + scroll_amount)
            else:
                # Normal scrolling behavior
                # Smaller scroll amounts for more natural movement
                # Reduce scroll amount on Ubuntu for slower scrolling
                if self.platform != "Windows":
                    scroll_amount = random.randint(-30, 30)  # Reduced from -100, 100
                else:
                    scroll_amount = random.randint(-100, 100)
                # Update scroll position (positive = scrolled down)
                self.scroll_position = max(0, min(self.max_scroll_position, self.scroll_position + scroll_amount))
            
            # Split into smaller steps for smoother scrolling
            steps = random.randint(2, 4)
            for _ in range(steps):
                pyautogui.scroll(scroll_amount // steps)
                time.sleep(random.uniform(0.05, 0.15))  # Shorter delays between scrolls
            
            # Small pause between scroll sequences
            time.sleep(random.uniform(0.1, 0.3))
    
    def natural_mouse_movement(self):
        """Simulate natural mouse movement with acceleration and deceleration"""
        start_x, start_y = pyautogui.position()
        
        # Get window position if we have a current window
        if self.current_window:
            if self.platform == "Windows":
                try:
                    hwnd = win32gui.FindWindow(None, self.current_window)
                    if hwnd:
                        rect = win32gui.GetWindowRect(hwnd)
                        end_x = random.randint(rect[0] + 100, rect[2] - 100)
                        end_y = random.randint(rect[1] + 100, rect[3] - 100)
                    else:
                        end_x = random.randint(0, self.screen_width)
                        end_y = random.randint(0, self.screen_height)
                except:
                    end_x = random.randint(0, self.screen_width)
                    end_y = random.randint(0, self.screen_height)
            else:
                # Linux/Ubuntu: use screen coordinates for now
                # Could be enhanced with xdotool window geometry if needed
                end_x = random.randint(0, self.screen_width)
                end_y = random.randint(0, self.screen_height)
        else:
            end_x = random.randint(0, self.screen_width)
            end_y = random.randint(0, self.screen_height)
        
        # Create a natural curve for the mouse movement with fewer steps for faster movement
        if self.platform != "Windows":
            # Ubuntu: More visible mouse movement with longer duration
            steps = random.randint(15, 25)  # More steps for smoother movement
            for i in range(steps):
                progress = i / steps
                ease = 0.5 - math.cos(progress * math.pi) / 2
                
                x = start_x + (end_x - start_x) * ease
                y = start_y + (end_y - start_y) * ease
                
                pyautogui.moveTo(x, y, duration=0.02)  # Longer duration for Ubuntu
                time.sleep(random.uniform(0.01, 0.03))  # Longer delays for Ubuntu
        else:
            # Windows: Faster movement
            steps = random.randint(10, 20)  # Reduced from 20-40 to 10-20
            for i in range(steps):
                progress = i / steps
                ease = 0.5 - math.cos(progress * math.pi) / 2
                
                x = start_x + (end_x - start_x) * ease
                y = start_y + (end_y - start_y) * ease
                
                pyautogui.moveTo(x, y, duration=0.005)  # Reduced from 0.01 to 0.005
                time.sleep(random.uniform(0.001, 0.005))  # Reduced from 0.01-0.03 to 0.001-0.005
    
    def delete_last_written_code(self):
        """Delete the last written code pattern by pressing backspace for each character"""
        # Press backspace for each character in the pattern
        for _ in range(len(self.last_written_pattern)):
            pyautogui.press('backspace')
            time.sleep(random.uniform(0.05, 0.15))

    def simulate_coding_activity(self):
        """Simulate coding-like behavior without actually modifying code"""
        # Only proceed if Cursor IDE is active
        if not self.is_cursor_ide_active():
            return

        # Code patterns for both React/TypeScript and vanilla JavaScript/HTML development
        patterns = [
            # React functional component patterns
            "const HomePage = () => {",
            "const UserProfile = ({ user }: { user: User }) => {",
            "const ProductCard = ({ product, onSelect }: ProductCardProps) => {",
            "const SearchInput = ({ value, onChange, placeholder }: SearchInputProps) => {",
            "const LoadingSpinner = ({ size = 'medium' }: { size?: 'small' | 'medium' | 'large' }) => {",
            
            # React hooks patterns
            "const [isLoading, setIsLoading] = useState<boolean>(false)",
            "const [user, setUser] = useState<User | null>(null)",
            "const [products, setProducts] = useState<Product[]>([])",
            "const [searchQuery, setSearchQuery] = useState<string>('')",
            "const [selectedId, setSelectedId] = useState<string | null>(null)",
            
            # useEffect patterns
            "useEffect(() => { fetchUserData() }, [userId])",
            "useEffect(() => { const timer = setTimeout(() => {}, 1000); return () => clearTimeout(timer) }, [])",
            "useEffect(() => { if (isAuthenticated) { loadUserPreferences() } }, [isAuthenticated])",
            
            # Event handlers
            "const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {",
            "const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {",
            "const handleSelectChange = (e: ChangeEvent<HTMLSelectElement>) => {",
            "const handleButtonClick = useCallback(() => {",
            "const handleModalClose = () => { setIsModalOpen(false) }",
            
            # API calls and async operations
            "const fetchUserData = async (userId: string): Promise<User> => {",
            "const updateUserProfile = async (data: Partial<User>) => {",
            "const deleteProduct = async (productId: string) => {",
            "const { data, error, isLoading } = useSWR(`/api/users/${userId}`, fetcher)",
            "const { mutate, isLoading: isMutating } = useMutation(updateUser)",
            
            # TypeScript interfaces and types
            "interface User { id: string; name: string; email: string; role: 'admin' | 'user' }",
            "interface Product { id: string; name: string; price: number; category: string }",
            "type UserRole = 'admin' | 'user' | 'moderator'",
            "type ApiResponse<T> = { data: T; error?: string; success: boolean }",
            "interface ComponentProps { children: ReactNode; className?: string }",
            
            # JSX return statements
            "return ( <div className=\"container mx-auto px-4\">",
            "return ( <button onClick={handleClick} className=\"btn btn-primary\">",
            "return ( <form onSubmit={handleSubmit} className=\"space-y-4\">",
            "return ( <input type=\"text\" value={value} onChange={onChange} className=\"input\" />",
            "return ( <div className=\"flex items-center justify-between\">",
            
            # Conditional rendering
            "return isLoading ? <LoadingSpinner /> : <UserProfile user={user} />",
            "return error ? <ErrorMessage error={error} /> : null",
            "return user ? <Dashboard user={user} /> : <LoginForm />",
            "{isModalOpen && <Modal onClose={handleModalClose}>}",
            "{products.length > 0 ? products.map(product => <ProductCard key={product.id} product={product} />) : <EmptyState />}",
            
            # Modern JavaScript patterns
            "const filteredProducts = products.filter(p => p.name.toLowerCase().includes(searchQuery.toLowerCase()))",
            "const sortedUsers = [...users].sort((a, b) => a.name.localeCompare(b.name))",
            "const userById = users.reduce((acc, user) => ({ ...acc, [user.id]: user }), {})",
            "const { name, email, ...otherUserData } = user",
            "const updatedUser = { ...user, lastLoginAt: new Date() }",
            
            # Error handling
            "try { const response = await api.fetchUser(userId); setUser(response.data) }",
            "catch (error) { console.error('Failed to fetch user:', error); setError(error.message) }",
            "finally { setIsLoading(false) }",
            
            # Custom hooks
            "const useAuth = () => { const [user, setUser] = useState(null); return { user, login, logout } }",
            "const useLocalStorage = <T>(key: string, initialValue: T) => {",
            "const useDebounce = <T>(value: T, delay: number): T => {",
            "const useFetch = <T>(url: string) => { const [data, setData] = useState<T | null>(null)",
            
            # Vanilla JavaScript patterns
            "function initApp() {",
            "function setupEventListeners() {",
            "function loadUserData() {",
            "function saveToLocalStorage(key, value) {",
            "function getFromLocalStorage(key) {",
            "function validateForm(formData) {",
            "function formatDate(date) {",
            "function calculateTotal(items) {",
            "function showModal(modalId) {",
            "function hideModal(modalId) {",
            "function toggleMenu() {",
            "function updateUI(data) {",
            "function handleFormSubmit(event) {",
            "function handleButtonClick(event) {",
            "function handleInputChange(event) {",
            "function fetchData(url) {",
            "function processResponse(response) {",
            "function displayError(message) {",
            "function showSuccess(message) {",
            "function debounce(func, delay) {",
            "function throttle(func, limit) {",
            
            # DOM manipulation patterns
            "document.getElementById('app').innerHTML = template",
            "document.querySelector('.container').appendChild(element)",
            "document.querySelectorAll('.item').forEach(item => {",
            "element.classList.add('active')",
            "element.classList.remove('hidden')",
            "element.classList.toggle('expanded')",
            "element.style.display = 'block'",
            "element.style.backgroundColor = '#f0f0f0'",
            "element.setAttribute('data-id', id)",
            "element.getAttribute('data-value')",
            
            # Event handling patterns
            "element.addEventListener('click', handleClick)",
            "element.addEventListener('submit', handleSubmit)",
            "element.addEventListener('input', handleInput)",
            "element.addEventListener('change', handleChange)",
            "element.addEventListener('keydown', handleKeyDown)",
            "element.addEventListener('mouseover', handleMouseOver)",
            "element.addEventListener('mouseout', handleMouseOut)",
            "element.addEventListener('focus', handleFocus)",
            "element.addEventListener('blur', handleBlur)",
            
            # Array and object manipulation
            "const filteredItems = items.filter(item => item.active)",
            "const sortedItems = items.sort((a, b) => a.name.localeCompare(b.name))",
            "const mappedItems = items.map(item => ({ ...item, processed: true }))",
            "const reducedValue = items.reduce((acc, item) => acc + item.value, 0)",
            "const foundItem = items.find(item => item.id === targetId)",
            "const hasItem = items.some(item => item.valid)",
            "const allValid = items.every(item => item.valid)",
            
            # Async/await patterns
            "async function fetchUserData() {",
            "const response = await fetch('/api/users')",
            "const data = await response.json()",
            "const result = await processData(data)",
            "try { const data = await apiCall() } catch (error) { console.error(error) }",
            
            # HTML structure patterns
            "<div class=\"container\">",
            "<header class=\"header\">",
            "<nav class=\"navigation\">",
            "<main class=\"main-content\">",
            "<aside class=\"sidebar\">",
            "<footer class=\"footer\">",
            "<section class=\"hero-section\">",
            "<article class=\"content-article\">",
            "<form class=\"contact-form\">",
            "<input type=\"text\" class=\"form-input\">",
            "<button type=\"submit\" class=\"btn btn-primary\">",
            "<select class=\"form-select\">",
            "<textarea class=\"form-textarea\">",
            "<label class=\"form-label\">",
            "<table class=\"data-table\">",
            "<ul class=\"item-list\">",
            "<li class=\"list-item\">",
            
            # CSS class patterns
            "class=\"container mx-auto px-4\"",
            "class=\"flex items-center justify-between\"",
            "class=\"grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3\"",
            "class=\"bg-white shadow-lg rounded-lg\"",
            "class=\"text-center text-gray-700\"",
            "class=\"hover:bg-gray-100 transition-colors\"",
            "class=\"focus:outline-none focus:ring-2\"",
            "class=\"disabled:opacity-50 cursor-not-allowed\"",
            "class=\"responsive-image max-w-full h-auto\"",
            "class=\"card-header bg-primary text-white\"",
            
            # Utility function patterns
            "function debounce(func, delay) {",
            "function throttle(func, limit) {",
            "function deepClone(obj) {",
            "function isEmpty(value) {",
            "function isValidEmail(email) {",
            "function formatCurrency(amount) {",
            "function formatPhoneNumber(phone) {",
            "function generateId() {",
            "function randomString(length) {",
            "function capitalizeFirst(str) {",
            
            # PHP patterns
            "<?php",
            "<?php namespace App\\Controllers;",
            "<?php namespace App\\Models;",
            "<?php namespace App\\Services;",
            "class UserController {",
            "class UserModel {",
            "class DatabaseConnection {",
            "class AuthService {",
            "class ValidationHelper {",
            "interface UserInterface {",
            "trait Loggable {",
            "abstract class BaseController {",
            "public function index() {",
            "public function show($id) {",
            "public function store(Request $request) {",
            "public function update(Request $request, $id) {",
            "public function destroy($id) {",
            "private function validateData($data) {",
            "protected function getCurrentUser() {",
            "static function getInstance() {",
            "function connectDatabase() {",
            "function validateEmail($email) {",
            "function sanitizeInput($input) {",
            "function generateToken() {",
            "function hashPassword($password) {",
            "function verifyPassword($password, $hash) {",
            "function sendEmail($to, $subject, $message) {",
            "function uploadFile($file) {",
            "function downloadFile($filename) {",
            "function createSession($user) {",
            "function destroySession() {",
            "function checkAuth() {",
            "function redirect($url) {",
            "function jsonResponse($data) {",
            "function errorResponse($message) {",
            "function successResponse($message) {",
            "try { $result = $this->processData($data); }",
            "catch (Exception $e) { error_log($e->getMessage()); }",
            "finally { $this->cleanup(); }",
            "foreach ($items as $item) {",
            "while ($row = $result->fetch()) {",
            "for ($i = 0; $i < count($array); $i++) {",
            "if ($condition) {",
            "elseif ($otherCondition) {",
            "else {",
            "switch ($value) {",
            "case 'option1': break;",
            "default: break;",
            "$user = new User();",
            "$user->name = 'John';",
            "$user->email = 'john@example.com';",
            "$user->save();",
            "$users = User::all();",
            "$user = User::find($id);",
            "$user = User::where('email', $email)->first();",
            "$result = DB::table('users')->get();",
            "$result = DB::select('SELECT * FROM users');",
            "$session = $_SESSION['user_id'];",
            "$cookie = $_COOKIE['remember_token'];",
            "$post = $_POST['email'];",
            "$get = $_GET['id'];",
            "$files = $_FILES['upload'];",
            "require_once 'config.php';",
            "include 'functions.php';",
            "use App\\Models\\User;",
            "use App\\Services\\EmailService;",
            "use Illuminate\\Http\\Request;",
            "use Illuminate\\Support\\Facades\\DB;",
            "namespace App\\Controllers;",
            "namespace App\\Models;",
            "namespace App\\Services;",
            "extends BaseController",
            "implements UserInterface",
            "use Loggable;",
            "public $name;",
            "private $email;",
            "protected $password;",
            "static $instance;",
            "const MAX_LOGIN_ATTEMPTS = 3;",
            "const DEFAULT_TIMEZONE = 'UTC';",
            "define('APP_NAME', 'MyApp');",
            "define('APP_VERSION', '1.0.0');",
            "return response()->json($data);",
            "return view('welcome');",
            "return redirect('/dashboard');",
            "return $this->successResponse('Success');",
            "return $this->errorResponse('Error');",
            "echo json_encode($data);",
            "print_r($array);",
            "var_dump($variable);",
            "isset($variable)",
            "empty($variable)",
            "unset($variable)",
            "array_key_exists($key, $array)",
            "in_array($value, $array)",
            "array_push($array, $value)",
            "array_pop($array)",
            "array_shift($array)",
            "array_unshift($array, $value)",
            "count($array)",
            "sizeof($array)",
            "strlen($string)",
            "strtolower($string)",
            "strtoupper($string)",
            "trim($string)",
            "substr($string, 0, 10)",
            "str_replace('old', 'new', $string)",
            "preg_match('/pattern/', $string)",
            "preg_replace('/pattern/', 'replacement', $string)",
            "date('Y-m-d H:i:s')",
            "time()",
            "strtotime('2023-01-01')",
            "date_default_timezone_set('UTC')",
            "password_hash($password, PASSWORD_DEFAULT)",
            "password_verify($password, $hash)",
            "md5($string)",
            "sha1($string)",
            "base64_encode($data)",
            "base64_decode($data)",
            "json_encode($data)",
            "json_decode($json, true)",
            "serialize($data)",
            "unserialize($serialized)",
            "file_get_contents($filename)",
            "file_put_contents($filename, $data)",
            "fopen($filename, 'r')",
            "fclose($handle)",
            "fgets($handle)",
            "fwrite($handle, $data)",
            "mkdir($dirname)",
            "rmdir($dirname)",
            "unlink($filename)",
            "copy($source, $dest)",
            "rename($oldname, $newname)",
            "is_file($filename)",
            "is_dir($dirname)",
            "file_exists($filename)",
            "filesize($filename)",
            "filemtime($filename)",
            "glob('*.php')",
            "scandir($dirname)",
            "opendir($dirname)",
            "readdir($handle)",
            "closedir($handle)",
            "chmod($filename, 0644)",
            "chown($filename, $user)",
            "chgrp($filename, $group)",
            "touch($filename)",
            "link($target, $link)",
            "symlink($target, $link)",
            "realpath($path)",
            "dirname($path)",
            "basename($path)",
            "pathinfo($path)",
            "parse_url($url)",
            "urlencode($string)",
            "urldecode($string)",
            "htmlspecialchars($string)",
            "htmlentities($string)",
            "strip_tags($string)",
            "addslashes($string)",
            "stripslashes($string)",
            "quotemeta($string)",
            "nl2br($string)",
            "wordwrap($string, 80)",
            "str_word_count($string)",
            "strpos($haystack, $needle)",
            "strrpos($haystack, $needle)",
            "stripos($haystack, $needle)",
            "strripos($haystack, $needle)",
            "substr_count($haystack, $needle)",
            "str_split($string)",
            "explode(',', $string)",
            "implode(',', $array)",
            "join(',', $array)",
            "str_pad($string, 10)",
            "str_repeat($string, 3)",
            "str_shuffle($string)",
            "strrev($string)",
            "ucfirst($string)",
            "ucwords($string)",
            "lcfirst($string)",
            "number_format($number)",
            "round($number)",
            "ceil($number)",
            "floor($number)",
            "abs($number)",
            "max($a, $b)",
            "min($a, $b)",
            "rand(1, 100)",
            "mt_rand(1, 100)",
            "srand($seed)",
            "mt_srand($seed)",
            "pi()",
            "pow($base, $exponent)",
            "sqrt($number)",
            "exp($number)",
            "log($number)",
            "log10($number)",
            "sin($angle)",
            "cos($angle)",
            "tan($angle)",
            "asin($number)",
            "acos($number)",
            "atan($number)",
            "deg2rad($degrees)",
            "rad2deg($radians)",
            "bindec($binary)",
            "decbin($decimal)",
            "bindec($binary)",
            "dechex($decimal)",
            "hexdec($hex)",
            "decoct($decimal)",
            "octdec($octal)",
            "base_convert($number, 10, 2)",
            "is_numeric($value)",
            "is_int($value)",
            "is_float($value)",
            "is_string($value)",
            "is_array($value)",
            "is_object($value)",
            "is_null($value)",
            "is_bool($value)",
            "is_callable($value)",
            "is_resource($value)",
            "is_scalar($value)",
            "gettype($value)",
            "settype($value, 'string')",
            "intval($value)",
            "floatval($value)",
            "strval($value)",
            "boolval($value)",
            "arrayval($value)",
            "objectval($value)",
            "unset($variable)",
            "isset($variable)",
            "empty($variable)",
            "defined('CONSTANT')",
            "constant('CONSTANT_NAME')",
            "function_exists('function_name')",
            "class_exists('ClassName')",
            "method_exists($object, 'method')",
            "property_exists($object, 'property')",
            "get_class($object)",
            "get_parent_class($object)",
            "get_class_methods($object)",
            "get_class_vars($object)",
            "get_object_vars($object)",
            "get_declared_classes()",
            "get_declared_functions()",
            "get_defined_functions()",
            "get_defined_vars()",
            "get_included_files()",
            "get_required_files()",
            "debug_backtrace()",
            "debug_print_backtrace()",
            "error_get_last()",
            "error_reporting(E_ALL)",
            "ini_set('display_errors', 1)",
            "ini_get('max_execution_time')",
            "set_time_limit(30)",
            "memory_get_usage()",
            "memory_get_peak_usage()",
            "gc_collect_cycles()",
            "gc_enable()",
            "gc_disable()",
            "register_shutdown_function('cleanup')",
            "set_error_handler('error_handler')",
            "set_exception_handler('exception_handler')",
            "restore_error_handler()",
            "restore_exception_handler()",
            "trigger_error('Error message', E_USER_ERROR)",
            "user_error('Error message', E_USER_WARNING)",
            "error_log('Error message')",
            "syslog(LOG_ERR, 'Error message')",
            "openlog('MyApp', LOG_PID, LOG_LOCAL0)",
            "closelog()",
            "header('Content-Type: application/json')",
            "header('Location: /redirect')",
            "header('Cache-Control: no-cache')",
            "setcookie('name', 'value', time() + 3600)",
            "session_start()",
            "session_destroy()",
            "session_regenerate_id()",
            "session_id()",
            "session_name()",
            "session_save_path()",
            "session_status()",
            "session_write_close()",
            "session_cache_limiter('nocache')",
            "session_cache_expire(30)",
            "session_set_cookie_params(3600)",
            "session_get_cookie_params()",
            "ob_start()",
            "ob_end_flush()",
            "ob_get_contents()",
            "ob_get_length()",
            "ob_get_level()",
            "ob_clean()",
            "ob_flush()",
            "flush()",
            "sleep(1)",
            "usleep(1000000)",
            "time_nanosleep(0, 1000000)",
            "microtime(true)",
            "microtime(false)",
            "gettimeofday()",
            "date_sunrise(time())",
            "date_sunset(time())",
            "date_sun_info(time(), 40.7128, -74.0060)",
            "checkdate(12, 31, 2023)",
            "date_parse('2023-12-31')",
            "date_parse_from_format('Y-m-d', '2023-12-31')",
            "date_create('2023-12-31')",
            "date_create_from_format('Y-m-d', '2023-12-31')",
            "date_modify($date, '+1 day')",
            "date_add($date, new DateInterval('P1D'))",
            "date_sub($date, new DateInterval('P1D'))",
            "date_diff($date1, $date2)",
            "date_format($date, 'Y-m-d H:i:s')",
            "date_timezone_get($date)",
            "date_timezone_set($date, new DateTimeZone('UTC'))",
            "date_offset_get($date)",
            "date_timestamp_get($date)",
            "date_timestamp_set($date, time())",
            "timezone_open('UTC')",
            "timezone_name_get($timezone)",
            "timezone_offset_get($timezone, $date)",
            "timezone_transitions_get($timezone)",
            "timezone_location_get($timezone)",
            "timezone_identifiers_list()",
            "timezone_abbreviations_list()",
            "timezone_version_get()",
            "cal_days_in_month(CAL_GREGORIAN, 12, 2023)",
            "cal_from_jd(jddayofweek(1, 1))",
            "cal_to_jd(CAL_GREGORIAN, 12, 31, 2023)",
            "easter_date(2023)",
            "easter_days(2023)",
            "frenchtojd(12, 31, 2023)",
            "gregoriantojd(12, 31, 2023)",
            "jddayofweek(2459945, 1)",
            "jdmonthname(2459945, 1)",
            "jdtofrench(2459945)",
            "jdtogregorian(2459945)",
            "jdtojewish(2459945)",
            "jdtojulian(2459945)",
            "jdtounix(2459945)",
            "jewishtojd(1, 1, 2023)",
            "juliantojd(12, 31, 2023)",
            "unixtojd(time())",
            "cal_info(CAL_GREGORIAN)",
            "cal_info(CAL_JULIAN)",
            "cal_info(CAL_JEWISH)",
            "cal_info(CAL_FRENCH)",
            "cal_days_in_month(CAL_GREGORIAN, 12, 2023)",
            "cal_from_jd(jddayofweek(1, 1))",
            "cal_to_jd(CAL_GREGORIAN, 12, 31, 2023)",
            "easter_date(2023)",
            "easter_days(2023)",
            "frenchtojd(12, 31, 2023)",
            "gregoriantojd(12, 31, 2023)",
            "jddayofweek(2459945, 1)",
            "jdmonthname(2459945, 1)",
            "jdtofrench(2459945)",
            "jdtogregorian(2459945)",
            "jdtojewish(2459945)",
            "jdtojulian(2459945)",
            "jdtounix(2459945)",
            "jewishtojd(1, 1, 2023)",
            "juliantojd(12, 31, 2023)",
            "unixtojd(time())",
            "cal_info(CAL_GREGORIAN)",
            "cal_info(CAL_JULIAN)",
            "cal_info(CAL_JEWISH)",
            "cal_info(CAL_FRENCH)",
        ]
        
        # Type a pattern
        pattern = random.choice(patterns)
        self.last_written_pattern = pattern  # Store the pattern for deletion
        for char in pattern:
            pyautogui.press(char)
            time.sleep(random.uniform(0.05, 0.15))
        
        # Always delete what we typed
        time.sleep(random.uniform(0.5, 1.0))
        self.delete_last_written_code()
    
    def simulate_break(self):
        """Simulate a natural break in activity"""
        break_duration = random.uniform(15, 30)  # Reduced break duration
        time.sleep(break_duration)
    
    def update_activity_level(self):
        """Update activity level with natural variations"""
        # Higher target activity level for more human-like behavior
        target_level = random.uniform(0.7, 0.9)  # Increased from 0.55-0.8 to 0.7-0.9
        while abs(self.activity_level - target_level) > 0.01:
            self.activity_level += (target_level - self.activity_level) * 0.2  # Increased from 0.1 to 0.2 for faster transitions
            time.sleep(0.05)  # Reduced from 0.1 to 0.05
    
    def run(self, duration_minutes=60):
        """Run the activity simulator for specified duration"""
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            # Update window list periodically
            if random.random() < 0.1:
                self.update_window_list()
            
            # Switch windows more frequently
            if random.random() < 0.4:  # 40% chance to switch windows
                self.switch_window()
            # Additional tab/file switching without window switch
            elif self.is_chrome_active() and random.random() < 0.3:  # 30% chance to switch tabs
                self.switch_chrome_tabs()
            elif self.is_cursor_ide_active() and random.random() < 0.3:  # 30% chance to switch files
                self.switch_cursor_files()
            elif self.is_vscode_active() and random.random() < 0.3:  # 30% chance to switch tabs
                self.switch_vscode_tabs()
            elif self.is_vscode_active() and random.random() < 0.2:  # 20% chance to switch files
                self.switch_vscode_files()
            
            # Choose activity with increased scroll probability
            activity = random.random()
            if activity < 0.4:  # 40% chance for scrolling
                self.simulate_scroll()
            elif activity < 0.6:  # 20% chance for mouse movement (increased for Ubuntu)
                self.natural_mouse_movement()
            elif activity < 0.75:  # 15% chance for coding activity
                self.simulate_coding_activity()
            else:  # 25% chance for clicking (increased for Ubuntu)
                pyautogui.click()
            
            # Update activity level
            self.update_activity_level()
            
            # Take shorter breaks less frequently
            if random.random() < 0.03:  # Reduced from 0.05 to 0.03 for less frequent breaks
                self.simulate_break()
            
            # Shorter delays between actions
            time.sleep(random.uniform(0.1, 0.5))  # Reduced from 0.2-1.0 to 0.1-0.5

if __name__ == "__main__":
    
    simulator = Simulator()
    try:
        simulator.run(duration_minutes=60)  # Run for 1 hour by default
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    except pyautogui.FailSafeException:
        print("\nPyAutoGUI fail-safe triggered. This usually happens when the mouse moves to a corner.")
        print("The simulation will continue after a brief pause...")
        time.sleep(2)
        try:
            simulator.run(duration_minutes=60)  # Restart the simulation
        except Exception as e:
            print(f"Simulation error: {e}")
    except Exception as e:
        print(f"Simulation error: {e}")
        print("If you're getting frequent fail-safe exceptions, you can:")
        print("1. Keep your mouse away from screen corners during simulation")
        print("2. The simulator will automatically recover from fail-safe triggers") 
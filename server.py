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
            # File extensions for both React/TypeScript and vanilla JS/HTML
            '.tsx', '.jsx', '.ts', '.js', '.html', '.css', '.scss', '.sass',
            
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
            
            # Common directory patterns for both project types
            'src/', 'components/', 'pages/', 'js/', 'css/', 'styles/',
            'utils/', 'helpers/', 'lib/', 'api/', 'assets/', 'images/',
            'public/', 'static/', 'dist/', 'build/', 'node_modules/',
            
            # Project configuration files
            'package.json', 'package-lock.json', 'yarn.lock', 'webpack.config',
            'vite.config', 'rollup.config', 'babel.config', 'eslint.config',
            'tsconfig.json', 'jsconfig.json', '.env', '.gitignore',
            
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

        # Handle special cases for Chrome and Cursor
        if self.is_chrome_active():
            if random.random() < 0.7:  # 70% chance to switch tabs when Chrome is active
                self.switch_chrome_tabs()
        elif self.is_cursor_ide_active():
            if random.random() < 0.6:  # 60% chance to switch files when Cursor is active
                self.switch_cursor_files()
    
    def simulate_scroll(self):
        """Simulate natural scrolling behavior"""
        # More frequent small scrolls
        num_scrolls = random.randint(2, 5)  # Do multiple scrolls in sequence
        
        for _ in range(num_scrolls):
            # Smaller scroll amounts for more natural movement
            # Reduce scroll amount on Ubuntu for slower scrolling
            if self.platform != "Windows":
                scroll_amount = random.randint(-30, 30)  # Reduced from -100, 100
            else:
                scroll_amount = random.randint(-100, 100)
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
            # Ubuntu: Try xdotool first, fallback to pyautogui
            try:
                # Use xdotool for more reliable mouse movement on Ubuntu
                steps = random.randint(10, 15)
                for i in range(steps):
                    progress = i / steps
                    ease = 0.5 - math.cos(progress * math.pi) / 2
                    
                    x = int(start_x + (end_x - start_x) * ease)
                    y = int(start_y + (end_y - start_y) * ease)
                    
                    # Use xdotool for mouse movement
                    subprocess.run(['xdotool', 'mousemove', str(x), str(y)], 
                                 capture_output=True, check=False)
                    time.sleep(random.uniform(0.05, 0.1))
                    
            except (subprocess.SubprocessError, FileNotFoundError):
                # Fallback to pyautogui if xdotool is not available
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
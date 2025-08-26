import pyautogui
import random
import time
import math
from datetime import datetime, timedelta
import win32gui
import win32con
import win32process
import psutil

# Safety feature - move mouse to corner to stop
pyautogui.FAILSAFE = True

class Simulator:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_activity_time = datetime.now()
        self.activity_level = 0.0  # 0.0 to 1.0
        self.current_window = None
        self.window_list = []
        self.update_window_list()
        
    def update_window_list(self):
        """Update the list of visible windows"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                # Filter out system windows, settings, and unwanted applications
                if title and not any(keyword in title.lower() for keyword in [
                    "default ime", "settings", "control panel", "task manager", 
                    "registry editor", "system configuration", "windows security",
                    "device manager", "event viewer", "services", "computer management",
                    "microsoft management console", "windows powershell", "command prompt",
                    "cortana", "search", "start", "taskbar", "notification area"
                ]):
                    windows.append((hwnd, title))
            return True
        
        self.window_list = []
        win32gui.EnumWindows(callback, self.window_list)
        self.window_list = [w for w in self.window_list if w[1]]  # Filter out empty titles
    
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
            time.sleep(random.uniform(0.2, 0.5))

    def switch_cursor_files(self):
        """Switch between Cursor files using keyboard shortcuts"""
        if not self.is_cursor_ide_active():
            return

        # Open file switcher
        pyautogui.hotkey('ctrl', 'p')
        time.sleep(random.uniform(0.3, 0.5))

        # Code file specific search patterns - only target code files
        search_patterns = [
            # JavaScript/TypeScript file extensions
            '.tsx', '.jsx', '.ts', '.js',
            # Common React component prefixes
            'use', 'get', 'set', 'handle', 'create', 'fetch', 'update', 'delete',
            # Common React component names
            'Button', 'Modal', 'Form', 'Input', 'Card', 'Header', 'Footer', 'Nav',
            'Layout', 'Page', 'Component', 'Hook', 'Context', 'Provider',
            # Common file patterns for React/Next.js
            'page', 'layout', 'component', 'hook', 'util', 'service', 'api',
            'store', 'reducer', 'action', 'selector', 'middleware', 'config',
            # Common directory patterns
            'src/', 'components/', 'pages/', 'hooks/', 'utils/', 'lib/', 'api/',
            'stores/', 'contexts/', 'services/', 'types/', 'interfaces/',
            # Specific React/Next.js file patterns
            'index.tsx', 'index.jsx', 'App.tsx', 'App.jsx',
            'layout.tsx', 'page.tsx', 'loading.tsx', 'types.ts',
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
            
        hwnd, title = random.choice(available_windows)
        self.current_window = title
        
        # Activate and maximize the window
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd)
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
            hwnd = win32gui.FindWindow(None, self.current_window)
            if hwnd:
                rect = win32gui.GetWindowRect(hwnd)
                end_x = random.randint(rect[0] + 100, rect[2] - 100)
                end_y = random.randint(rect[1] + 100, rect[3] - 100)
            else:
                end_x = random.randint(0, self.screen_width)
                end_y = random.randint(0, self.screen_height)
        else:
            end_x = random.randint(0, self.screen_width)
            end_y = random.randint(0, self.screen_height)
        
        # Create a natural curve for the mouse movement with fewer steps for faster movement
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

        # More focused code patterns for React/TypeScript development
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
            if activity < 0.5:  # 50% chance for scrolling
                self.simulate_scroll()
            elif activity < 0.65:  # 15% chance for mouse movement
                self.natural_mouse_movement()
            elif activity < 0.8:  # 15% chance for coding activity
                self.simulate_coding_activity()
            else:  # 20% chance for clicking
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
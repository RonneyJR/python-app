from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6 import uic
import sys
import os
from data_io import *

def normalize_path(path):
    # Handle None or empty
    if not path:
        return ""
    # Convert path separators to system-specific format
    try:
        normalized = os.path.normpath(path)
    except Exception:
        return ""
    # Check if path exists, if not try to find it relative to current directory
    if not os.path.exists(normalized):
        # Try relative to current directory
        relative_path = os.path.join(os.getcwd(), normalized)
        if os.path.exists(relative_path):
            return relative_path
    return normalized

class Alert(QMessageBox):
    def error_message(self, *args):
        # Supports: (message) or (title, message)
        if len(args) == 1:
            title, message = "Error", str(args[0])
        elif len(args) >= 2:
            title, message = str(args[0]), str(args[1])
        else:
            title, message = "Error", "An error occurred"
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

    def success_message(self, *args):
        # Supports: (message) or (title, message)
        if len(args) == 1:
            title, message = "Success", str(args[0])
        elif len(args) >= 2:
            title, message = str(args[0]), str(args[1])
        else:
            title, message = "Success", "Action completed successfully"
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        # Load UI
        uic.loadUi("ui/login.ui", self)

        # Find widgets
        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login") 
        self.btn_register = self.findChild(QPushButton, "btn_register") 
        self.btn_eye = self.findChild(QPushButton, "btn_eye")

        # Connect signals
        if self.btn_eye:
            self.btn_eye.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input))
        if self.btn_login:
            self.btn_login.clicked.connect(self.login)
        if self.btn_register:
            self.btn_register.clicked.connect(self.show_register)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return

        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return
        
        user = get_user_by_email_and_password(email, password)
        if user:
            msg.success_message("Login", "Welcome to the system")
            self.show_home(user["id"])
            return
        
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()    

    def show_home(self, id):
        self.home = Home(id)
        self.home.show()
        self.close()

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(1000, 600)
        
        # Load UI
        uic.loadUi("ui/register.ui", self)

        # Find widgets
        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.name_input = self.findChild(QLineEdit, "txt_name")
        self.confirm_password_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.btn_login = self.findChild(QPushButton, "btn_login") 
        self.btn_register = self.findChild(QPushButton, "btn_register") 
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")    
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        # Connect signals
        if self.btn_eye_p:
            self.btn_eye_p.clicked.connect(lambda: self.show_password(self.btn_eye_p, self.password_input))
        if self.btn_eye_cp:
            self.btn_eye_cp.clicked.connect(lambda: self.show_password(self.btn_eye_cp, self.confirm_password_input))
        if self.btn_register:
            self.btn_register.clicked.connect(self.register)
        if self.btn_login:
            self.btn_login.clicked.connect(self.show_login)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    
        # Hàm mới để kiểm tra độ mạnh của mật khẩu
    def validate_password_strength(self, password):
        # Yêu cầu 1: Mật khẩu phải có ít nhất 8 ký tự
        if len(password) < 8:
            return "Password must be at least 8 characters long"

        # Yêu cầu 2: Mật khẩu phải chứa ít nhất một chữ số
        has_digit = any(char.isdigit() for char in password)
        if not has_digit:
            return "Password must contain at least one digit"

        # Yêu cầu 3: Mật khẩu phải chứa ít nhất một ký tự đặc biệt
        special_chars = "!@#$%^&*()-_+=[]{}|;:',.<>/?`~"
        has_special = any(char in special_chars for char in password)
        if not has_special:
            return "Password must contain at least one special character"
        
        return None # Trả về None nếu mật khẩu hợp lệ

    def register(self):
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if email == "":
            msg.error_message("Register", "Email is required")
            self.email_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Register", "Password is required")
            self.password_input.setFocus()
            return
        
        if self.validate_password_strength(password):
            msg.error_message("Register",self.validate_password_strength(password))
            self.password_input.setFocus()
            return
        
        if confirm_password == "":
            msg.error_message("Register", "Confirm Password is required")
            self.confirm_password_input.setFocus()
            return
        
        if password != confirm_password:
            msg.error_message("Register", "Password and Confirm Password do not match")
            self.password_input.setFocus()
            return

        user = get_user_by_email(email)
        if user:
            msg.error_message("Register", "Email already exists")
            self.email_input.setFocus()
            return   
        
        create_user(email, password, name)
        
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()
        

class SongItemWidget(QWidget):
    play_song = pyqtSignal(str)
    add_song_to_playlist = pyqtSignal(str)
    remove_song_from_playlist = pyqtSignal(str)

    def __init__(self, song_id, song_name, image_path, artist_names, is_playlist_mode=False):
        super().__init__()
        uic.loadUi("ui/song_item.ui", self)
        
        # Store song data
        self.song_id = song_id
        self.song_name = song_name
        self.image_path = image_path
        self.artist_names = artist_names
        self.is_playlist_mode = is_playlist_mode
        
        # Find UI elements
        self.name = self.findChild(QLabel, "lbl_name")
        self.artist = self.findChild(QLabel, "lbl_artist")
        self.image = self.findChild(QLabel, "lbl_image")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_playlist = self.findChild(QPushButton, "btn_add")
        
        # Set initial values
        self.name.setText(self.song_name)
        self.artist.setText(self.artist_names)
        img_path = normalize_path(self.image_path)
        if img_path:
            self.image.setPixmap(QPixmap(img_path))
        
        # Connect signals
        self.btn_play.clicked.connect(self.play)
        self.btn_playlist.clicked.connect(self.handle_playlist_action)
        
        # Set button text based on mode
        self.setup_playlist_button()
        
        # Set minimum size
        self.setMinimumSize(400, 80)
    
    def play(self):
        self.play_song.emit(str(self.song_id))

    def handle_playlist_action(self):
        if self.is_playlist_mode:
            self.remove_song_from_playlist.emit(str(self.song_id))
        else:
            self.add_song_to_playlist.emit(str(self.song_id))
    
    def setup_playlist_button(self):
        if self.is_playlist_mode:
            self.btn_playlist.setText("Remove")
            self.btn_playlist.setProperty("class", "remove")
        else:
            self.btn_playlist.setText("Add")
            self.btn_playlist.setProperty("class", "")

class PlaylistWidget(QWidget):
    play_song_signal = pyqtSignal(str)  # Add signal at class level
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create container for songs
        self.songs_container = QWidget()
        self.songs_layout = QGridLayout(self.songs_container)
        self.songs_layout.setSpacing(20)
        self.songs_layout.setContentsMargins(20, 20, 20, 20)
        self.songs_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Setup scroll area
        self.scroll_area.setWidget(self.songs_container)
        self.layout.addWidget(self.scroll_area)
        
        # Load initial songs
        self.load_songs()
    
    def load_songs(self):
        # Clear existing widgets
        for i in reversed(range(self.songs_layout.count())):
            self.songs_layout.itemAt(i).widget().setParent(None)
            
        # Get user's playlist songs
        songs = get_user_playlist_songs_json(self.user_id)
        
        # Add songs to the layout in 2 columns
        row = 0
        col = 0
        for song in songs:
            # Create widget in playlist mode (Remove button only)
            item = SongItemWidget(song['id'], song['name'], normalize_path(song['image_path']), song['artist_names'], is_playlist_mode=True)
            item.setFixedSize(400, 80)  # Set fixed size for each item
            item.play_song.connect(self.on_play_song)  # Connect to intermediate handler
            item.remove_song_from_playlist.connect(self.remove_song)
            self.songs_layout.addWidget(item, row, col)
            col += 1
            if col == 2:  # Show 2 columns
                col = 0
                row += 1
        
        # Add stretch to push items to the top-left
        self.songs_layout.setRowStretch(row + 1, 1)
    
    def on_play_song(self, song_id):
        # Emit signal to parent
        self.play_song_signal.emit(song_id)
    
    def remove_song(self, song_id):
        remove_song_from_user_playlist_json(self.user_id, song_id)
        self.load_songs()  # Refresh the view


class Home(QWidget):
    def __init__(self, id):
        super().__init__()
        self.setWindowTitle("Home")
        
        # Load UI
        uic.loadUi("ui/home.ui", self)
        
        self.id = id
        self.user_id = id  # Add user_id for compatibility
        self.user = get_user_by_id(id)
        self.load_user_info()


        # Initialize media player and audio output early
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)

        # Initialize playback/playlist state
        self.current_playlist = []
        self.current_song_index = -1
        self.current_volume = 50

        self.stack_widget = self.findChild(QStackedWidget, "stackedWidget")

        # Ensure we show the 'home' page initially (no extra wrapping)
        home_page = self.findChild(QWidget, 'home')
        if self.stack_widget and home_page:
            self.stack_widget.setCurrentIndex(self.stack_widget.indexOf(home_page))
        
        # Build UI elements and layouts, then load data
        self.setup_ui()
        self.load_initial_songs()
        self.render_history()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()
    
    def navigate_screen(self, stackWidget: QStackedWidget, index: int):
        stackWidget.setCurrentIndex(index)

    def load_user_info(self):
        self.user = get_user_by_id(self.id)
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_birthday.setDate(QDate.fromString(self.user["birthday"], "dd/MM/yyyy"))
        self.txt_gender.setCurrentText(self.user["gender"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"] if self.user["avatar"] else "img/circle-user-solid.svg"))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *jpeg *bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file if file else "img/default-avatar.png"))
            update_user_avatar(self.id, file)
            msg.success_message("Update", "Avatar updated succesfully")

    def update_user_info(self):
        name = self.txt_name.text().strip()
        birthday = self.txt_birthday.date().toString("dd/MM/yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.id, name, birthday, gender)
        msg.success_message("Update", "User info updated succesfully")
        self.load_user_info()
    
    def setup_ui(self):
        # Connect player signals
        self.player.errorOccurred.connect(self.handle_player_error)
        self.player.playbackStateChanged.connect(self.mediaStateChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        
        # Initialize UI elements
        self.playBtn = self.findChild(QPushButton, "btn_play")
        self.volumeBtn = self.findChild(QPushButton, "btn_volume")
        self.volumeBar = self.findChild(QSlider, "slider_volume")
        self.durationBar = self.findChild(QSlider, "slider_duration")
        self.timeLabel = self.findChild(QLabel, "lbl_time")
        # Current playing info labels (fallback to existing objectNames in ui/home.ui)
        self.curr_name = self.findChild(QLabel, "lbl_curr_name")
        self.curr_img = self.findChild(QLabel, "lbl_curr_img")
        self.curr_artist = self.findChild(QLabel, "lbl_curr_artist")  # May not exist in UI
        
        # Initialize icons
        try:
            self.playIcon = QIcon("img/play-solid.svg")
            self.pauseIcon = QIcon("img/pause-solid.svg")
            self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
            self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
            self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
            self.muteIcon = QIcon("img/volume-xmark-solid.svg")
        except:
            print("Warning: Could not load some icons")
            self.playIcon = None
            self.pauseIcon = None
            self.volumeHighIcon = None
            self.volumeLowIcon = None
            self.volumeOffIcon = None
            self.muteIcon = None
        
        # Set initial volume
        self.playBtn.setIcon(self.playIcon)
        self.playBtn.clicked.connect(self.togglePlay)
        self.volumeBtn.setIcon(self.volumeOffIcon)
        self.volumeBtn.clicked.connect(self.toggleMute)

        self.volumeBar.valueChanged.connect(self.setVolume)
        self.durationBar.sliderMoved.connect(self.setPosition)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.playbackStateChanged.connect(self.mediaStateChanged)
        self.volumeBar.setValue(50)
        self.durationBar.setValue(0)
        self.audio_output.setVolume(0.5)
        self.current_volume = 50

        # Find navigation buttons
        self.btn_user = self.findChild(QPushButton, 'user_btn')
        self.btn_song_list = self.findChild(QPushButton, 'btn_song_list')
        self.btn_playlist = self.findChild(QPushButton, 'playlist_btn')
        self.btn_history = self.findChild(QPushButton, 'btn_history')
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.btn_log_out = self.findChild(QPushButton, "btn_log_out")
        self.btn_log_out.clicked.connect(self.show_login)
        # Ensure default page shows the song list (the 'home' page)
        if self.stackedWidget:
            for i in range(self.stackedWidget.count()):
                wrapper = self.stackedWidget.widget(i)
                if wrapper.findChild(QWidget, 'home') is not None:
                    self.stackedWidget.setCurrentIndex(i)
                    break
        # Detail page disabled
        
        # Find player control buttons
        self.btn_prev_song = self.findChild(QPushButton, 'btn_prev_song')
        self.btn_next_song = self.findChild(QPushButton, 'btn_next_song')
        
        # Connect player control buttons
        self.btn_prev_song.clicked.connect(self.previous_song)
        self.btn_next_song.clicked.connect(self.next_song)
        
        # START - PHẦN BỔ SUNG CHO CHỨC NĂNG TRỘN BÀI HÁT
        self.btn_shuffle = self.findChild(QPushButton, 'btn_shuffle')
        if self.btn_shuffle:
            self.btn_shuffle.clicked.connect(self.shuffle_songs)
        # END - PHẦN BỔ SUNG CHO CHỨC NĂNG TRỘN BÀI HÁT
        
        
        # Setup song container with scroll area
        self.btn_search = self.findChild(QPushButton, 'btn_search')
        self.txt_search = self.findChild(QLineEdit, 'txt_search')
        self.song_container = self.findChild(QWidget, 'song_container')
        
        # Setup scroll area
        self.scroll_area = QScrollArea(self.song_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea{background: transparent;} QWidget{background: transparent;}")
        
        # Create scroll content
        self.scroll_content = QWidget()
        self.scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.song_layout = QGridLayout(self.scroll_content)
        self.song_layout.setSpacing(20)
        self.song_layout.setContentsMargins(20, 20, 20, 20)
        self.song_layout.setColumnStretch(0, 1)
        self.song_layout.setColumnStretch(1, 1)
        
        # Setup scroll area layout
        self.scroll_area.setWidget(self.scroll_content)
        scroll_layout = QVBoxLayout(self.song_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(self.scroll_area)

        # Make sure container is visible and has a size
        self.song_container.show()
        self.song_container.raise_()
        self.scroll_area.show()
        self.scroll_content.show()
        self.scroll_area.raise_()
        
        # Setup playlist container
        self.playlist_container = self.findChild(QWidget, 'playlist_widget')
        if self.playlist_container is None:
            # Fallback: use the 'playlist' page itself as container
            self.playlist_container = self.findChild(QWidget, 'playlist')
        if self.playlist_container is not None:
            self.playlist_widget = PlaylistWidget(self.user_id)
            self.playlist_widget.play_song_signal.connect(self.play_song)  # Connect playlist signal
            playlist_layout = QVBoxLayout(self.playlist_container)
            playlist_layout.setContentsMargins(0, 0, 0, 0)
            playlist_layout.addWidget(self.playlist_widget)
        
        # Connect signals (stack order: 0=home, 1=profile, 2=playlist)
        self.btn_song_list.clicked.connect(lambda: self.navigate(0))  # Home (song list)
        self.btn_user.clicked.connect(lambda: self.navigate(1))       # Profile page
        self.btn_playlist.clicked.connect(lambda: self.navigate(2))   # Playlist page
        self.btn_history.clicked.connect(lambda: self.navigate(3))   # History page
        self.btn_search.clicked.connect(self.search_song)

        # Setup history container on 'history' page if present
        self.history_page = self.findChild(QWidget, 'history')
        if self.history_page is not None:
            self.history_scroll = QScrollArea(self.history_page)
            self.history_scroll.setWidgetResizable(True)
            self.history_content = QWidget()
            self.history_layout = QVBoxLayout(self.history_content)
            self.history_layout.setContentsMargins(10,10,10,10)
            self.history_layout.setSpacing(10)
            self.history_scroll.setWidget(self.history_content)
            h_layout = QVBoxLayout(self.history_page)
            h_layout.setContentsMargins(0,0,0,0)
            h_layout.addWidget(self.history_scroll)
    
    def load_initial_songs(self):
        # Clear existing widgets
        if not hasattr(self, 'song_layout') or self.song_layout is None:
            print('song_layout not initialized')
            return
        for i in reversed(range(self.song_layout.count())):
            self.song_layout.itemAt(i).widget().setParent(None)
            
        # Get first 15 songs using JSON
        songs = get_first_15_songs_json()
        print(f'Loaded {len(songs)} songs')
        
        # Add songs to the layout in 2 columns
        row = 0
        col = 0
        added = 0
        for song in songs:
            item = SongItemWidget(song['id'], song['name'], normalize_path(song['image_path']), song['artist_names'], is_playlist_mode=False)
            item.setFixedSize(400, 80)  # Set fixed size for each item
            # Temporary debug styling to make items visible
            item.setStyleSheet("background: rgba(255,255,255,0.06); color: white;")
            item.play_song.connect(self.play_song)
            item.add_song_to_playlist.connect(self.add_to_playlist)
            item.remove_song_from_playlist.connect(self.remove_from_playlist)
            self.song_layout.addWidget(item, row, col)
            item.show()
            col += 1
            if col == 2:  # Show 2 columns
                col = 0
                row += 1
            added += 1
        self.scroll_content.adjustSize()
        self.scroll_area.update()
        self.scroll_content.update()
        print(f'Grid now has {self.song_layout.count()} widgets, attempted to add {added}')

    def add_to_playlist(self, song_id):
        try:
            # Check if song is already in playlist
            if is_song_in_user_playlist_json(self.user_id, song_id):
                msg = Alert()
                msg.error_message("This song is already in your playlist")
                return
                
            # Add song to playlist
            add_song_to_user_playlist_json(self.user_id, song_id)
            
            # Update current playlist
            self.current_playlist = get_user_playlist_songs_json(self.user_id)
            
            # Always refresh playlist widget to keep it in sync
            self.playlist_widget.load_songs()
            
            # Show success message
            msg = Alert()
            msg.success_message("Song added to playlist successfully")
            
        except Exception as e:
            print(f"Error adding song to playlist: {e}")
            msg = Alert()
            msg.error_message("Failed to add song to playlist")

    def remove_from_playlist(self, song_id):
        try:
            # Remove song from playlist
            remove_song_from_user_playlist_json(self.user_id, song_id)
            
            # Update current playlist
            self.current_playlist = get_user_playlist_songs_json(self.user_id)
            
            # Always refresh playlist widget to keep it in sync
            self.playlist_widget.load_songs()
            
            # Show success message
            msg = Alert()
            msg.success_message("Song removed from playlist successfully")
            
        except Exception as e:
            print(f"Error removing song from playlist: {e}")
            msg = Alert()
            msg.error_message("Failed to remove song from playlist")

    def update_song_item_state(self, song_id, is_in_playlist):
        # Find and update the song item in the current view
        for i in range(self.song_layout.count()):
            item = self.song_layout.itemAt(i).widget()
            if isinstance(item, SongItemWidget) and str(item.song_id) == str(song_id):
                item.is_playlist_mode = is_in_playlist
                item.setup_playlist_button()
                break

    def play_song(self, song_id):
        # Always refresh the playlist when playing a song
        self.current_playlist = get_user_playlist_songs_json(self.user_id)
        
        # Find the song in the current playlist
        self.current_song_index = -1  # Reset index
        for i, song in enumerate(self.current_playlist):
            if str(song['id']) == str(song_id):
                self.current_song_index = i
                break
        
        self.current_song = song_id
        song = get_song_by_id_json(song_id)
        if not song:
            msg = Alert()
            msg.error_message("Song not found")
            return
        file_str = normalize_path(song.get("file_path"))
        if not file_str:
            msg = Alert()
            msg.error_message("Audio file path missing or invalid")
            return
        file_url = QUrl.fromLocalFile(file_str)
        self.player.setSource(file_url)
        self.player.play()

        # Add to listening history
        try:
            add_song_to_history_json(self.user_id, song_id)
            self.render_history()
        except Exception as e:
            print(f"Warning: cannot add to history: {e}")
        
        if self.playBtn and self.pauseIcon:
            self.playBtn.setIcon(self.pauseIcon)
        elif self.playBtn:
            self.playBtn.setText("Pause")
        
        if self.curr_name:
            self.curr_name.setText(f"Now playing: {song['name']}")
        img = normalize_path(song.get("image_path"))
        if self.curr_img and img:
            self.curr_img.setPixmap(QPixmap(img))
            self.curr_img.setScaledContents(True)
        if self.curr_artist:
            self.curr_artist.setText(f"Artist: {song['artist_names']}")
    
    def navigate(self, index):
        self.stackedWidget.setCurrentIndex(index)
        
    def render_song_list(self, song_list:list):
        # clear the grid layout
        for i in reversed(range(self.song_layout.count())):
            widgetToRemove = self.song_layout.itemAt(i).widget()
            self.song_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for song in song_list:
            # Create widget in song list mode (Add button only)
            itemWidget = SongItemWidget(song["id"], song["name"], normalize_path(song["image_path"]), song["artist_names"], is_playlist_mode=False)
            itemWidget.setFixedSize(400, 80)  # Set fixed size for each item
            itemWidget.play_song.connect(self.play_song)
            itemWidget.add_song_to_playlist.connect(self.add_to_playlist)
            self.song_layout.addWidget(itemWidget, row, column)
            column += 1
            if column == 2:  # Show 2 columns
                column = 0
                row += 1
        # push items to top and enable proper scrolling
        self.song_layout.setRowStretch(row + 1, 1)
        self.scroll_content.adjustSize()
        self.scroll_area.update()

    def render_history(self):
        if not hasattr(self, 'history_layout') or self.history_layout is None:
            return
        # Clear
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            w = child.widget()
            if w:
                w.setParent(None)
        # Load recent songs
        songs = get_user_history_songs_json(self.user_id, limit=50)
        for song in songs:
            widget = SongItemWidget(song['id'], song['name'], normalize_path(song['image_path']), song['artist_names'], is_playlist_mode=False)
            widget.setFixedHeight(80)
            widget.play_song.connect(self.play_song)
            self.history_layout.addWidget(widget)
        self.history_layout.addStretch(1)

    def search_song(self):
        name = self.txt_search.text().strip()
        if name == "":
            # show the first 15 only when query is empty
            self.load_initial_songs()
            return
        song_list = get_songs_by_name_json(name)
        self.render_song_list(song_list)
        
    def handle_player_error(self, error, error_string):
        print(f"Media player error: {error} - {error_string}")
        
    def mediaStateChanged(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        # Convert position and duration from milliseconds to hh:mm:ss format
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.player.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self, duration):
        self.durationBar.setRange(0, duration)
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.player.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def setPosition(self, position):
        if self.player.duration() > 0:  # Only set position if media is loaded
            self.player.setPosition(position)
        
    def setVolume(self, volume):
        # Convert the slider value to a float between 0.0 and 1.0
        volume = volume / 100.0
        self.audio_output.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audio_output.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audio_output.setMuted(False)
    
    def toggleMute(self):
        if self.audio_output.isMuted():
            self.audio_output.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audio_output.setMuted(True)
            self.volumeBtn.setIcon(self.muteIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def togglePlay(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.playBtn.setIcon(self.playIcon)
        else:
            self.player.play()
            self.playBtn.setIcon(self.pauseIcon)

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def next_song(self):
        if not self.current_playlist:
            msg = Alert()
            msg.error_message("No playlist is currently loaded")
            return
            
        if self.current_song_index < len(self.current_playlist) - 1:
            next_song = self.current_playlist[self.current_song_index + 1]
            self.play_song(next_song['id'])
        else:
            # Loop back to the start of the playlist
            first_song = self.current_playlist[0]
            self.play_song(first_song['id'])

    def previous_song(self):
        if not self.current_playlist:
            msg = Alert()
            msg.error_message("No playlist is currently loaded")
            return
            
        if self.current_song_index > 0:
            prev_song = self.current_playlist[self.current_song_index - 1]
            self.play_song(prev_song['id'])
        else:
            # Go to the last song in the playlist
            last_song = self.current_playlist[-1]
            self.play_song(last_song['id'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg = Alert()
    login = Login()
    login.show()
    sys.exit(app.exec())
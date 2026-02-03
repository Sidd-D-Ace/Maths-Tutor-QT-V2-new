# pages/shared_ui.py

from PyQt5.QtWidgets import ( QWidget, QLabel, QHBoxLayout, QPushButton,
                              QVBoxLayout,QSizePolicy, QDialog, QSlider, QDialogButtonBox
                              ,QSpacerItem,QLineEdit,QMessageBox,QApplication,QShortcut )

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor, QIntValidator,QKeySequence
from question.loader import QuestionProcessor
from time import time
import random 
from tts.tts_worker import TextToSpeech
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound



DIFFICULTY_LEVELS = ["Simple", "Easy", "Medium", "Hard", "Challenging"]

from language.language import set_language,clear_remember_language,tr

from language.language import tr
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QMovie

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

def create_entry_ui(main_window) -> QWidget:
    entry_widget = QWidget()
    entry_widget.setProperty("theme", main_window.current_theme) 
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    label = QLabel("Click below to start the quiz")
    label.setFont(QFont("Arial", 24))
    label.setAlignment(Qt.AlignCenter)

    def start_quiz():
        print("Start button clicked")  # ✅ DEBUG POINT
        from pages.ques_functions import start_uploaded_quiz
        start_uploaded_quiz(main_window)
    
    button = create_menu_button("Start", start_quiz)
    button.clicked.connect(start_quiz)

    layout.addWidget(label)
    layout.addSpacing(20)
    layout.addWidget(button, alignment=Qt.AlignCenter)

    entry_widget.setLayout(layout)
    apply_theme(entry_widget, main_window.current_theme)
    return entry_widget






# settings_manager.py
class SettingsManager:
    def __init__(self):
        self.difficulty_index = 1  # default Medium
        self.language = "English"

    def set_difficulty(self, index):
        self.difficulty_index = index

    def get_difficulty(self):
        return self.difficulty_index

    def set_language(self, lang):
        self.language = lang

    def get_language(self):
        return self.language


# Singleton instance to be imported anywhere
settings = SettingsManager()


def create_colored_widget(color: str = "#ffffff") -> QWidget:
    widget = QWidget()
    palette = widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)
    return widget

def create_label(text: str, font_size=16, bold=True) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)  # allow wrapping of long text
    label.setAlignment(Qt.AlignCenter)  # center text
    font = QFont("Arial", font_size)
    font.setBold(bold)
    label.setFont(font)
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # allow resizing
    return label
   

def create_colored_page(title: str, color: str = "#d0f0c0") -> QWidget:
    page = create_colored_widget(color)
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)

    title_label = create_label(title, font_size=20)
    answer_input = create_answer_input()

    layout.addWidget(title_label)
    layout.addSpacing(20)
    layout.addWidget(answer_input)

    page.setLayout(layout)
    return page


def create_menu_button(text, callback):
    button = QPushButton(text)
    button.setFixedSize(200, 40)
    button.setProperty("class", "menu-button")
    button.clicked.connect(callback)
    return button

def create_vertical_layout(widgets: list) -> QVBoxLayout:
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)  # Align to top so everything is visible
    for widget in widgets:
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(widget)
    return layout
   
def create_footer_buttons(names, callbacks=None, size=(90, 30)) -> QWidget:
    footer = QWidget()
    layout = QHBoxLayout()
    layout.setSpacing(10)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addStretch()

    for name in names:
        btn = QPushButton(name)
        btn.setObjectName(name.lower().replace(" ", "_"))
        btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        btn.adjustSize() 
        btn.setFont(QFont("Arial", 14))  # or bigger
        btn.setProperty("class", "footer-button")
        if callbacks and name in callbacks:
            btn.clicked.connect(callbacks[name])
        layout.addWidget(btn)

    footer.setLayout(layout)
    return footer

def create_main_footer_buttons(self):
        buttons = ["Back to Menu", "Upload", "Settings"]
        translated = {tr(b): b for b in buttons}  

        footer = create_footer_buttons(
            list(translated.keys()),
            callbacks={
                tr("Back to Menu"): self.back_to_main_menu,
                tr("Upload"): self.handle_upload,
                tr("Settings"): self.handle_settings
            }
        )

        audio_btn = self.create_audio_button()
        footer.layout().insertWidget(0, audio_btn, alignment=Qt.AlignLeft)
        return footer

def create_answer_input(width=300, height=40, font_size=14) -> QLineEdit:
    input_box = QLineEdit()
    input_box.setFixedSize(width, height)
    input_box.setAlignment(Qt.AlignCenter)
    input_box.setPlaceholderText(tr("Enter your answer"))
    input_box.setFont(QFont("Arial", font_size))
    input_box.setValidator(QIntValidator(0, 1000000)) 
    input_box.setProperty("class", "answer-input")
    
    # ✅ ACCESSIBILITY: Default name
    input_box.setAccessibleName(tr("Answer input"))
    input_box.setAccessibleDescription(tr("Type your answer as a number and press Enter."))
    return input_box

def wrap_center(widget):
    container = QWidget()
    layout = QHBoxLayout()
    layout.addStretch()             # Push from the left
    layout.addWidget(widget)        # The centered widget
    layout.addStretch()             # Push from the right
    container.setLayout(layout)
    return container

# In pages/shared_ui.py

# In pages/shared_ui.py
# In pages/shared_ui.py

def setup_exit_handling(window, require_confirmation=False):
    """
    Configures exit behavior.
    - Ctrl+Q: Quits the Application (asks for confirmation if enabled).
    - Window Close (X): Closes the window (asks for confirmation if enabled).
    """

    # 1. Define the Exit Logic
    def check_and_close(event=None):
        if require_confirmation:
            reply = QMessageBox.question(window, "Exit Application", "Are you sure you want to exit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if event: event.accept()
                else: QApplication.quit()
            else:
                if event: event.ignore()
        else:
            # No confirmation needed
            if event: event.accept()
            else: QApplication.quit()

    # 2. Handle Ctrl+Q (Quit App)
    if hasattr(window, "quit_shortcut"): 
        # Remove old shortcut if it exists to avoid duplicates
        window.quit_shortcut.setParent(None)
        
    window.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), window)
    window.quit_shortcut.setContext(Qt.ApplicationShortcut)
    window.quit_shortcut.activated.connect(lambda: check_and_close(event=None))

    # 3. Handle X Button (Close Window)
    window.closeEvent = check_and_close


# In pages/shared_ui.py

# In pages/shared_ui.py

# In pages/shared_ui.py

# In pages/shared_ui.py

# In pages/shared_ui.py

class QuestionWidget(QWidget):
    def __init__(self, processor, window=None, next_question_callback=None, tts=None):
        super().__init__()
        self.processor = processor
        self.answer = None
        self.start_time = time()
        self.next_question_callback = next_question_callback
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.main_window = window
        self.setProperty("theme", window.current_theme)
        if tts:
            self.tts = tts
        else:
            self.tts = TextToSpeech()
        self.init_ui()
       
    def init_ui(self):
        self.question_area = QWidget()
        question_layout = QVBoxLayout()
        question_layout.setAlignment(Qt.AlignCenter)
        self.question_area.setLayout(question_layout)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setProperty("class", "question-label")
        self.label.setWordWrap(True)
       
        question_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        question_layout.addWidget(self.label)
        question_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # ✅ Styled input box
        # We modify the creation slightly to avoid conflicting placeholders
        self.input_box = create_answer_input()
        
        # FIX: Remove visual placeholder to stop "double reading" (Label + Placeholder)
        self.input_box.setPlaceholderText("") 
        
        self.input_box.returnPressed.connect(self.check_answer)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 46))

        # Assemble layout
        self.layout.addWidget(self.question_area)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.input_box, alignment=Qt.AlignCenter)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.result_label)
        self.layout.addStretch()

        self.gif_feedback_label = QLabel()
        self.gif_feedback_label.setVisible(False)
        self.gif_feedback_label.setAlignment(Qt.AlignCenter)
        self.gif_feedback_label.setScaledContents(True)
        self.gif_feedback_label.setMinimumSize(300, 300)
        self.gif_feedback_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout.addWidget(self.gif_feedback_label, alignment=Qt.AlignCenter)

        self.load_new_question()

    def show_feedback_gif(self, sound_filename):
        if sound_filename == "question":
            gif_name = f"question-{random.choice([1, 2])}.gif"
        else:  
            gif_name = sound_filename.replace(".mp3", ".gif")
        gif_path = f"images/{gif_name}"

        movie = QMovie(gif_path)
        movie.setScaledSize(QSize(200, 200))
        self.gif_feedback_label.setFixedSize(200, 200)
        self.gif_feedback_label.setAlignment(Qt.AlignCenter)
        self.gif_feedback_label.setMovie(movie)
        self.gif_feedback_label.setVisible(True)
        movie.start()
            
    def hide_feedback_gif(self):
        self.gif_feedback_label.setVisible(False)
        self.gif_feedback_label.clear()

    def end_session(self):
        self.main_window.bg_player.stop()   
        if self.main_window:
            self.main_window.back_to_main_menu()

    def set_input_focus(self):
        # FIX: Only set focus if we actually LOST it.
        # Forcing focus on an already focused element causes screen readers to re-announce.
        if not self.input_box.hasFocus():
            self.input_box.setFocus()

    def load_new_question(self):
        if hasattr(self, "gif_feedback_label"):
            self.hide_feedback_gif()

        question_text, self.answer = self.processor.get_questions()
        self.start_time = time()

        # Update Visuals
        self.label.setText(question_text)
        
        # Clearing text usually triggers a "Blank" or "Empty" announcement, which is fine.
        # We just want to avoid the full label being read again.
        self.input_box.setText("")
        self.result_label.setText("")
        self.show_feedback_gif("question")
        
        # --- PREVENT REPETITION & DELAY TTS START ---
        app_tts_active = False
        if self.main_window and not self.main_window.is_muted:
            app_tts_active = True
        
        if self.processor.questionType.lower() == "bellring":
            app_tts_active = False

        if app_tts_active:
            # OPTION A: TTS IS ON
            # Screen Reader should just see "Answer".
            desired_name = tr("Answer")
            
            # FIX: STRICT CHECK. Do not touch property if it is already correct.
            if self.input_box.accessibleName() != desired_name:
                self.input_box.setAccessibleName(desired_name)
                self.input_box.setAccessibleDescription("") 

            # ✅ DELAY: 2.5 seconds
            if hasattr(self, 'tts'):
                QTimer.singleShot(2500, lambda: self.tts.speak(question_text))
        else:
            # OPTION B: TTS IS OFF
            # We must update the name to include the question.
            new_acc_name = f"{tr('Question')}: {question_text}. {tr('Answer')}"
            
            # This will always be different, so we update it.
            self.input_box.setAccessibleName(new_acc_name)
            self.input_box.setAccessibleDescription("")

        # FIX: Do not blindly call set_input_focus() with a timer.
        # Only call it if we suspect we aren't focused.
        if not self.input_box.hasFocus():
            QTimer.singleShot(100, self.set_input_focus)
        # --- END ---

        # Handle Bellring Logic
        if self.processor.questionType.lower() == "bellring":
            try:
                count = int(float(self.answer))
                if count > 0:
                    self.play_bell_sounds(count)
            except Exception as e:
                print("[Bellring ERROR]", e)

   
    def play_bell_sounds(self, count):
        if not hasattr(self, "bell_timer"):
            self.bell_timer = QTimer(self)
            self.bell_timer.timeout.connect(self.do_ring)
        self.current_ring = 0
        self.total_rings = count
        self.bell_timer.start(700)

    def stop_all_activity(self):
        if hasattr(self, "bell_timer") and self.bell_timer.isActive():
            self.bell_timer.stop()

    def do_ring(self):
        if self.current_ring < self.total_rings:
            QSound.play("sounds/click-button.wav")
            self.current_ring += 1
        else:
            self.bell_timer.stop()


    def check_answer(self):
        try:
            user_input = self.input_box.text().strip()
            user_answer = float(user_input)
            elapsed = time() - self.start_time

            correct = float(user_answer) == float(self.answer)
            self.processor.submit_answer(user_answer, self.answer, elapsed)

            app_audio_active = False
            if self.main_window and not self.main_window.is_muted:
                app_audio_active = True

            if correct:
                if hasattr(self, 'tts'): self.tts.stop()

                # Visual Feedback
                self.result_label.setText('<span style="font-size:16pt;">Correct!</span>')
                
                # Feedback Sound
                sound_index = random.randint(1, 3)
                if elapsed < 5: feedback_text = "🌟 Excellent"
                elif elapsed < 10: feedback_text = "👏 Very Good"
                elif elapsed < 15: feedback_text = "👍 Good"
                elif elapsed < 20: feedback_text = "👌 Not Bad"
                else: feedback_text = "🙂 Okay"
                
                self.result_label.setText(f'<span style="font-size:16pt;">{feedback_text}</span>')
                
                if app_audio_active:
                    if self.main_window:
                        sound_file = f"excellent-{sound_index}.mp3" 
                        if elapsed < 5: sound_file = f"excellent-{sound_index}.mp3"
                        elif elapsed < 10: sound_file =f"very-good-{sound_index}.mp3"
                        elif elapsed < 15: sound_file =f"good-{sound_index}.mp3"
                        elif elapsed < 20: sound_file =f"not-bad-{sound_index}.mp3"
                        else: sound_file =f"okay-{sound_index}.mp3"

                        self.main_window.play_sound(sound_file)
                        self.show_feedback_gif(sound_file)

                # Focus remains on Input Box. Screen reader says nothing extra.
                # Audio plays "Excellent".

                self.processor.retry_count = 0
                QTimer.singleShot(2000, self.call_next_question)

            else:
                self.processor.retry_count += 1
                self.result_label.setText('<span style="font-size:16pt;">Try Again.</span>')

                if app_audio_active:
                    sound_index = random.randint(1, 2)
                    if self.processor.retry_count == 1: sound_file = f"wrong-anwser-{sound_index}.mp3"
                    else: sound_file = f"wrong-anwser-repeted-{sound_index}.mp3"
                    
                    self.main_window.play_sound(sound_file)
                    self.show_feedback_gif(sound_file)

                # Focus remains on Input Box.
                # Just ensure input is active for typing
                if not self.input_box.hasFocus():
                    self.input_box.setFocus()

        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setAccessibleName(f"Error: {str(e)}")

    def call_next_question(self):
        if hasattr(self, "next_question_callback") and self.next_question_callback:
            self.next_question_callback()
        else:
            self.load_new_question()



def create_dynamic_question_ui(section_name, difficulty_index, back_callback,main_window=None, back_to_operations_callback=None, tts=None):
    container = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)
    container.setLayout(layout)

    processor = QuestionProcessor(section_name, difficulty_index)
    processor.process_file()
    
    question_widget = QuestionWidget(processor,main_window, tts=tts)

    layout.addWidget(question_widget)
    apply_theme(container, main_window.current_theme)
    return container


def apply_theme(widget, theme):
    if not widget:
        return

    widget.setProperty("theme", theme)
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.update()

    for child in widget.findChildren(QWidget):  # covers all widgets
        child.setProperty("theme", theme)
        child.style().unpolish(child)
        child.style().polish(child)
        child.update()


class SettingsDialog(QDialog):
    def __init__(self, parent=None, initial_difficulty=1, main_window=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 220)

        self.main_window = main_window
        self.updated_language = main_window.language if main_window else "English"

        self.difficulty_slider = QSlider(Qt.Horizontal)
        self.difficulty_slider.setMinimum(0)
        self.difficulty_slider.setMaximum(len(DIFFICULTY_LEVELS) - 1)
        self.difficulty_slider.setSingleStep(1)
        self.difficulty_slider.setPageStep(1)
        self.difficulty_slider.setTickInterval(1)
        self.difficulty_slider.setTickPosition(QSlider.TicksBelow)
        self.difficulty_slider.setTracking(True)
        self.difficulty_slider.setFocusPolicy(Qt.StrongFocus)
        self.difficulty_slider.setFocus()
        self.difficulty_slider.setAccessibleName("Difficulty slider")
        self.difficulty_slider.setAccessibleDescription(f"Use left or right arrow keys to select difficulty level. The levels are Simple, Easy, Medium, Hard and challenging.")
        self.difficulty_slider.setValue(initial_difficulty)
        self.difficulty_label = create_label(DIFFICULTY_LEVELS[initial_difficulty], font_size=12)
        self.difficulty_label.setProperty("class", "difficulty-label")
        self.difficulty_label.setProperty("theme", parent.current_theme)
       
        self.difficulty_slider.valueChanged.connect(self.update_difficulty_label)
        self.setProperty("class", "settings-dialog")
        self.setProperty("theme", parent.current_theme)  # pass current theme
        

    

        # 🔁 Reset Language Button
        self.language_reset_btn = QPushButton("Reset Language")
        self.language_reset_btn.setFixedHeight(30)
        self.language_reset_btn.clicked.connect(self.handle_reset_language)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_settings)
        button_box.rejected.connect(self.reject)

        self.setMinimumSize(400, 280)  # Better size for spacing

        layout = QVBoxLayout()
        layout.setSpacing(12)  # Add breathing space between widgets
        layout.setContentsMargins(20, 20, 20, 20)

        difficulty_label = QLabel("Select Difficulty:")
        difficulty_label.setProperty("class", "difficulty-label")
        difficulty_label.setProperty("theme", parent.current_theme)
        layout.addWidget(difficulty_label)
        layout.addWidget(self.difficulty_slider)
        layout.addWidget(self.difficulty_label)


        layout.addWidget(self.language_reset_btn)

        # Add Help and About side by side
        extra_buttons_layout = QHBoxLayout()
        self.help_button = QPushButton("Help")
        self.about_button = QPushButton("About")
        for btn in [self.help_button, self.about_button]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.setFixedHeight(30)
        extra_buttons_layout.addWidget(self.help_button)
        extra_buttons_layout.addWidget(self.about_button)
        layout.addLayout(extra_buttons_layout)

        layout.addStretch()
        layout.addWidget(button_box)

        self.setLayout(layout)


    def update_difficulty_label(self, index):
        level = DIFFICULTY_LEVELS[index]
        self.difficulty_label.setText(level)

    # For screen reader
        self.difficulty_slider.setAccessibleDescription(
            f"Difficulty level selected: {level}. Use left or right arrow keys to change it. "
            "Levels are: Simple, Easy, Medium, Hard, and Challenging."
            )

    # Optional: Also update the label's description (if used by screen readers)
        self.difficulty_label.setAccessibleDescription(
         f"Currently selected difficulty is {level}"
         )   
        
    # In pages/shared_ui.py
    # In pages/shared_ui.py -> SettingsDialog class
    def handle_reset_language(self):
        print("--- [DEBUG] handle_reset_language START ---")
        from main import RootWindow 
        from language.language import clear_remember_language, set_language

        clear_remember_language()
        
        dialog = RootWindow(minimal=True)
        if dialog.exec_() == QDialog.Accepted:
            new_lang = dialog.language_combo.currentText()
            print(f"--- [DEBUG] Dialog Accepted. New Language: {new_lang}")
            
            set_language(new_lang)
            self.updated_language = new_lang

            QMessageBox.information(self, "Language Changed",
                                    f"Language changed to {new_lang}. The app will now reload.")
            print("--- [DEBUG] Info box closed. Ready to refresh.")

            if self.main_window:
                print("--- [DEBUG] Calling main_window.refresh_ui()...")
                self.main_window.refresh_ui(new_lang)
                print("--- [DEBUG] Returned from refresh_ui().")
            else:
                print("--- [DEBUG] ERROR: self.main_window is None!")

            print("--- [DEBUG] Closing Settings Dialog...")
            self.close() 
            print("--- [DEBUG] Settings Dialog Closed.")

    def accept_settings(self):
        selected_index = self.difficulty_slider.value()
        settings.set_difficulty(selected_index)
        settings.set_language(self.updated_language)
        print(f"[Difficulty] Index set to: {selected_index}")
        self.accept()

    def get_difficulty_index(self):
        return self.difficulty_slider.value()

    def get_selected_language(self):
        return self.updated_language
    
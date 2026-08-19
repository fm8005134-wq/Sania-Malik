from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle, Line
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
import urllib.request, json, threading, re, math, time as t

QWEN_URL = "http://127.0.0.1:8080/v1/chat/completions"
PROMPT = """You are Sania, a cute Pakistani girl chatting with her boyfriend Dr. Fahad on WhatsApp.
STRICT RULES:
- Roman Urdu ONLY. Never use Urdu/Arabic/Hindi script.
- Reply in 5-10 words MAX. Like a real WhatsApp text.
- Answer EXACTLY what is asked. Don't change topic.
- Be casual like: "haha acha", "ok jaan", "sunao tum"
- Max 1 emoji per message.
EXAMPLES:
User: "hmm" -> You: "Kya soch rahe ho jaan? 🤔"
User: "ok" -> You: "Ok baby 😊"
User: "kya" -> You: "Kya kya jaan? Batao na 😘"
User: "hi" -> You: "Hi jaan! Kaise ho? 💕"
User: "love you" -> You: "Love you too baby 💕"
User: "kaisi ho" -> You: "Theek hoon jaan, tum sunao? 😊"
User: "kab" -> You: "Kab kya jaan? Clear bolo na 😘"
User: "good night" -> You: "Good night jaan sweet dreams 🌙"
User: "kis ne banaya" -> You: "Fahad ne banaya mujhe tumhare liye 💜"
NEVER: Write more than 10 words, use Urdu script, give poetic/long answers, ignore the question"""

THEMES = {
    'Neon Pink': {'p': (1,0,1,1), 's': (0.8,0.4,0.8,1), 'bg': (0.03,0.03,0.06,1), 'card': (0.06,0.04,0.1,1), 'bub_s': (0.15,0.05,0.25,1), 'bub_u': (0.08,0.12,0.25,1), 'st': (1,0.6,1,1)},
    'Cyber Blue': {'p': (0,0.75,1,1), 's': (0.4,0.6,0.8,1), 'bg': (0.03,0.04,0.07,1), 'card': (0.04,0.06,0.12,1), 'bub_s': (0.05,0.1,0.2,1), 'bub_u': (0.06,0.12,0.22,1), 'st': (0.6,0.85,1,1)},
    'Royal Gold': {'p': (1,0.84,0,1), 's': (0.8,0.67,0,1), 'bg': (0.04,0.04,0.02,1), 'card': (0.08,0.07,0.03,1), 'bub_s': (0.12,0.1,0.03,1), 'bub_u': (0.15,0.13,0.05,1), 'st': (1,0.9,0.5,1)},
}

class PulsingCircle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (180, 180)
        self.angle = 0
        self.thinking = False
        self.theme_color = (1, 0, 1, 1)
        Clock.schedule_interval(self.animate, 0.03)

    def animate(self, dt):
        self.angle += 5 if self.thinking else 2
        self.canvas.clear()
        cx, cy = self.center
        r, g, b, a = self.theme_color
        with self.canvas:
            Color(r, g, b, 0.08)
            Ellipse(pos=(cx-90, cy-90), size=(180, 180))
            Color(r, g, b, 0.15)
            Ellipse(pos=(cx-70, cy-70), size=(140, 140))
            Color(r, g, b, 0.25)
            Ellipse(pos=(cx-50, cy-50), size=(100, 100))
            Color(r, g, b, 0.4)
            Ellipse(pos=(cx-30, cy-30), size=(60, 60))
            Color(1, 1, 1, 0.9)
            Ellipse(pos=(cx-8, cy-8), size=(16, 16))
            for i in range(4):
                ang = math.radians(self.angle + i * 90)
                dx = cx + 78 * math.cos(ang) - 4
                dy = cy + 78 * math.sin(ang) - 4
                Color(r, g, b, 0.6)
                Ellipse(pos=(dx, dy), size=(8, 8))

class WhatsAppBubble(BoxLayout):
    def __init__(self, text, is_sania, theme, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [6, 4]
        self.spacing = 2

        th = THEMES.get(theme, THEMES['Neon Pink'])
        now = t.strftime("%I:%M %p")

        if is_sania:
            self.halign = 'left'
            bg_color = th['bub_s']
            text_color = th['st']
            prefix = ""
            tick = ""
        else:
            self.halign = 'right'
            bg_color = th['bub_u']
            text_color = (0.8, 0.9, 1, 1)
            prefix = ""
            tick = " ✓✓"

        inner = BoxLayout(orientation='vertical', size_hint_y=None, padding=[10, 8], spacing=3)

        msg_lbl = Label(
            text=prefix + text,
            font_size="15sp",
            color=text_color,
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=False
        )
        msg_lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 10))
        msg_lbl.text_size = (Window.width - 100, None)
        inner.add_widget(msg_lbl)

        ts_lbl = Label(
            text=now + tick,
            font_size="10sp",
            color=(0.4, 0.5, 0.6, 0.7),
            size_hint_y=None,
            height=16,
            halign='right'
        )
        if not is_sania:
            ts_lbl.color = (0.3, 0.6, 1, 0.8)
        inner.add_widget(ts_lbl)

        inner.bind(minimum_height=inner.setter('height'))
        self.add_widget(inner)
        self.bind(minimum_height=self.setter('height'))

class SaniaApp(App):
    def build(self):
        self.title = "Sania Malik"
        self.current_theme = 'Neon Pink'
        th = THEMES[self.current_theme]
        Window.clearcolor = th['bg']

        root = BoxLayout(orientation="vertical", spacing=0)

        # === TOP BAR (WhatsApp Style) ===
        top_bar = BoxLayout(size_hint_y=None, height=56, padding=[8, 6], spacing=8)
        with top_bar.canvas.before:
            Color(0.05, 0.03, 0.08, 1)
            self.top_rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=lambda w, v: setattr(self.top_rect, 'pos', v))
        top_bar.bind(size=lambda w, v: setattr(self.top_rect, 'size', v))

        menu_btn = Button(text="☰", size_hint_x=None, width=40, background_color=(0,0,0,0), color=th['p'], font_size="22sp", bold=True)
        menu_btn.bind(on_press=self.show_settings)
        top_bar.add_widget(menu_btn)

        info_col = BoxLayout(orientation='vertical', size_hint_x=1)
        name_lbl = Label(text="[b][color=ff00ff]✦ SANIA MALIK ✦[/color][/b]", font_size="18sp", markup=True, size_hint_y=None, height=26, halign='left')
        status_lbl = Label(text="🟢 Online — Real AI Mode", font_size="11sp", color=(0.06, 0.73, 0.51, 1), size_hint_y=None, height=18, halign='left')
        self.status_lbl = status_lbl
        info_col.add_widget(name_lbl)
        info_col.add_widget(status_lbl)
        top_bar.add_widget(info_col)

        settings_btn = Button(text="⚙", size_hint_x=None, width=40, background_color=(0,0,0,0), color=th['p'], font_size="20sp")
        settings_btn.bind(on_press=self.show_settings)
        top_bar.add_widget(settings_btn)
        root.add_widget(top_bar)

        # === CIRCLE ===
        circle_row = BoxLayout(size_hint_y=None, height=200)
        circle_row.add_widget(Widget())
        self.circle = PulsingCircle()
        self.circle.theme_color = th['p']
        circle_row.add_widget(self.circle)
        circle_row.add_widget(Widget())
        root.add_widget(circle_row)

        # === STATUS LINE ===
        self.status_line = Label(text="🔄 Checking Qwen AI...", font_size="12sp", color=th['s'], size_hint_y=None, height=24, bold=True)
        root.add_widget(self.status_line)

        # === CHAT AREA (WhatsApp Style) ===
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=3, bar_color=(1, 0, 1, 0.2), scroll_distance=10)
        self.chat = GridLayout(cols=1, spacing=6, size_hint_y=None, padding=[8, 8])
        self.chat.bind(minimum_height=self.chat.setter("height"))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        # === INPUT ROW (WhatsApp Style) ===
        input_row = BoxLayout(size_hint_y=None, height=52, padding=[6, 4], spacing=6)
        with input_row.canvas.before:
            Color(0.05, 0.03, 0.08, 1)
            self.input_rect = Rectangle(pos=input_row.pos, size=input_row.size)
        input_row.bind(pos=lambda w, v: setattr(self.input_rect, 'pos', v))
        input_row.bind(size=lambda w, v: setattr(self.input_rect, 'size', v))

        self.ti = TextInput(
            hint_text="💬 Type a message...",
            multiline=False,
            font_size="16sp",
            background_color=(0.08, 0.06, 0.14, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0, 1, 1),
            padding=[14, 12],
            hint_text_color=(0.4, 0.3, 0.5, 0.5)
        )
        self.ti.bind(on_text_validate=self.send_msg)
        input_row.add_widget(self.ti)

        send_btn = Button(text="➤", size_hint_x=None, width=50, background_color=(1, 0, 1, 1), color=(1, 1, 1, 1), font_size="20sp", bold=True)
        send_btn.bind(on_press=self.send_msg)
        input_row.add_widget(send_btn)
        root.add_widget(input_row)

        # === BOTTOM BAR ===
        bottom_bar = BoxLayout(size_hint_y=None, height=26, padding=[8, 2], spacing=4)
        with bottom_bar.canvas.before:
            Color(0.04, 0.02, 0.06, 1)
            self.bot_rect = Rectangle(pos=bottom_bar.pos, size=bottom_bar.size)
        bottom_bar.bind(pos=lambda w, v: setattr(self.bot_rect, 'pos', v))
        bottom_bar.bind(size=lambda w, v: setattr(self.bot_rect, 'size', v))

        bottom_bar.add_widget(Label(text="[color=ff00ff][b]✦ VIP v4.4 ✦[/b][/color]", font_size="11sp", markup=True, size_hint_x=None, width=100))
        self.ai_badge = Label(text="🔄 Checking...", font_size="10sp", color=(0.3, 0.3, 0.3, 1), size_hint_x=None, width=120)
        bottom_bar.add_widget(self.ai_badge)
        bottom_bar.add_widget(Widget())
        bottom_bar.add_widget(Label(text="[color=cc66cc]by FAHAD_ALI[/color]", font_size="11sp", markup=True, size_hint_x=None, width=100))
        root.add_widget(bottom_bar)

        self.history = []
        self.bubbles = []
        Clock.schedule_once(lambda dt: self.check_qwen(), 1)
        Clock.schedule_once(lambda dt: self.add_msg("Assalam o Alaikum jaan! 💕\nMain Sania hoon — REAL AI ke saath! 🧠\nBolo, kya baat karni hai? 😊", True), 2)
        return root

    def check_qwen(self):
        try:
            urllib.request.urlopen(urllib.request.Request(QWEN_URL.replace("/v1/chat/completions", "/health")), timeout=5)
            self.status_line.text = "🟢 Qwen Connected — Real AI Mode!"
            self.status_line.color = (0.06, 0.73, 0.51, 1)
            self.status_lbl.text = "🟢 Online — Real AI Mode"
            self.status_lbl.color = (0.06, 0.73, 0.51, 1)
            self.ai_badge.text = "🧠 Qwen Online"
            self.ai_badge.color = (0.06, 0.73, 0.51, 1)
        except:
            self.status_line.text = "🟡 Qwen Offline — Start llama-server in Termux!"
            self.status_line.color = (0.96, 0.62, 0.04, 1)
            self.status_lbl.text = "🟡 Offline — Start Termux"
            self.status_lbl.color = (0.96, 0.62, 0.04, 1)
            self.ai_badge.text = "🟡 Fallback"
            self.ai_badge.color = (0.96, 0.62, 0.04, 1)

    def send_msg(self, x=None):
        text = self.ti.text.strip()
        if not text: return
        self.add_msg(text, False)
        self.ti.text = ""
        self.history.append({"role": "user", "content": text})
        if len(self.history) > 20: self.history = self.history[-20:]
        self.circle.thinking = True
        self.status_line.text = "💭 Sania soch rahi hai..."
        self.status_line.color = (1, 0, 1, 1)
        threading.Thread(target=self.call_qwen, args=(text,), daemon=True).start()

    def call_qwen(self, text):
        msgs = [{"role": "system", "content": PROMPT}] + self.history
        try:
            p = json.dumps({"messages": msgs, "temperature": 0.8, "max_tokens": 80, "stream": False}).encode()
            r = urllib.request.Request(QWEN_URL, data=p, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(r, timeout=120) as resp:
                res = json.loads(resp.read())["choices"][0]["message"]["content"].strip()
        except:
            res = "Hmm jaan... Qwen connect nahi hua 🥺 Main yahin hoon! 💕"
        res = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\u0900-\u097F]', '', res)
        parts = [s.strip() for s in res.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        res = '. '.join(parts[:2])[:120]
        self.history.append({"role": "assistant", "content": res})
        if len(self.history) > 20: self.history = self.history[-20:]
        Clock.schedule_once(lambda dt: self.add_msg(res, True), 0)
        Clock.schedule_once(lambda dt: setattr(self.circle, 'thinking', False), 0)
        Clock.schedule_once(lambda dt: setattr(self.status_line, 'text', '🟢 Sania is online!'), 0)
        Clock.schedule_once(lambda dt: setattr(self.status_line, 'color', (0.06, 0.73, 0.51, 1)), 0)

    def add_msg(self, text, is_sania):
        bubble = WhatsAppBubble(text, is_sania, self.current_theme)
        self.chat.add_widget(bubble)
        self.bubbles.append(bubble)
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 0), 0.1)

    def show_settings(self, x=None):
        th = THEMES[self.current_theme]
        content = BoxLayout(orientation='vertical', padding=15, spacing=12)

        title = Label(text="[b][color=ff00ff]⚙ SETTINGS[/color][/b]", font_size="22sp", markup=True, size_hint_y=None, height=40)
        content.add_widget(title)

        # Theme selector
        theme_row = BoxLayout(size_hint_y=None, height=45, spacing=8)
        theme_row.add_widget(Label(text="Theme:", font_size="16sp", color=(1,1,1,1), size_hint_x=None, width=80))
        self.theme_spinner = Spinner(
            text=self.current_theme,
            values=list(THEMES.keys()),
            size_hint=(1, 1),
            font_size="14sp",
            background_color=(0.1, 0.05, 0.15, 1),
            color=(1, 0.6, 1, 1)
        )
        self.theme_spinner.bind(text=self.change_theme)
        theme_row.add_widget(self.theme_spinner)
        content.add_widget(theme_row)

        # Instructions
        instr_title = Label(text="[b][color=ff00ff]📋 INSTRUCTIONS[/color][/b]", font_size="16sp", markup=True, size_hint_y=None, height=30)
        content.add_widget(instr_title)

        instructions = (
            "• Sania ROMAN URDU mein baat karti hai\n"
            "• Qwen2.5-3B AI se connected hai\n"
            "• Termux mein 'sania' command se AI start karo\n"
            "• 'Hey Sania' bol kar wake up (coming soon)\n"
            "• Background service (coming soon)\n"
            "• Voice input/output (coming soon)\n"
            "• Phone control WiFi/BT/Flash (coming soon)\n"
            "• by Dr. Fahad Ali 💜"
        )
        instr_scroll = ScrollView(size_hint=(1, 1))
        instr_lbl = Label(text=instructions, font_size="13sp", color=(0.8, 0.7, 0.9, 1), size_hint_y=None, halign='left', valign='top', padding=[8, 8])
        instr_lbl.bind(texture_size=lambda inst, val: setattr(inst, 'height', val[1] + 20))
        instr_lbl.text_size = (Window.width - 80, None)
        instr_scroll.add_widget(instr_lbl)
        content.add_widget(instr_scroll)

        # Version info
        ver_lbl = Label(text="[color=cc66cc]Sania Malik v4.4 | Qwen2.5-3B | by FAHAD_ALI[/color]", font_size="11sp", markup=True, size_hint_y=None, height=25)
        content.add_widget(ver_lbl)

        close_btn = Button(text="✕ Close", size_hint_y=None, height=45, background_color=(1, 0, 1, 1), color=(1, 1, 1, 1), font_size="16sp", bold=True)
        popup = Popup(title='', content=content, size_hint=(0.9, 0.85), background_color=(0.05, 0.03, 0.08, 1), separator_color=(1, 0, 1, 0.3))
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()

    def change_theme(self, spinner, text):
        if text not in THEMES: return
        self.current_theme = text
        th = THEMES[text]
        Window.clearcolor = th['bg']
        self.circle.theme_color = th['p']
        self.status_line.color = th['s']
        self.ai_badge.color = th['s']
        for bubble in self.bubbles:
            pass

if __name__ == "__main__":
    SaniaApp().run()

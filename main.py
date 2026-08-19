from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget
import urllib.request, json, threading, re, math

QWEN_URL = "http://127.0.0.1:8080/v1/chat/completions"
PROMPT = "You are Sania, Dr. Fahad AI girlfriend. Roman Urdu ONLY. 5-10 words MAX. Answer exactly what is asked. Casual flirty Pakistani girl. Max 1 emoji. Call him jaan/baby."

class PulsingCircle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 200)
        self.angle = 0
        self.thinking = False
        Clock.schedule_interval(self.animate, 0.03)

    def animate(self, dt):
        self.angle += 5 if self.thinking else 2
        self.canvas.clear()
        cx, cy = self.center
        with self.canvas:
            Color(1, 0, 1, 0.1)
            Ellipse(pos=(cx-100, cy-100), size=(200, 200))
            Color(1, 0, 1, 0.2)
            Ellipse(pos=(cx-75, cy-75), size=(150, 150))
            Color(1, 0, 1, 0.4)
            Ellipse(pos=(cx-50, cy-50), size=(100, 100))
            Color(1, 0, 1, 0.6)
            Ellipse(pos=(cx-25, cy-25), size=(50, 50))
            Color(1, 1, 1, 0.9)
            Ellipse(pos=(cx-8, cy-8), size=(16, 16))
            for i in range(4):
                a = math.radians(self.angle + i * 90)
                dx = cx + 85 * math.cos(a) - 4
                dy = cy + 85 * math.sin(a) - 4
                Color(1, 0, 1, 0.7)
                Ellipse(pos=(dx, dy), size=(8, 8))

class SaniaApp(App):
    def build(self):
        self.title = "Sania Malik"
        Window.clearcolor = (0.03, 0.03, 0.06, 1)
        root = BoxLayout(orientation="vertical", padding=10, spacing=6)

        # Top bar
        top = BoxLayout(size_hint_y=None, height=50, spacing=8)
        top.add_widget(Label(text="[b][size=28][color=ff00ff]✦ SANIA MALIK ✦[/color][/size][/b]", markup=True, font_size="28sp"))
        root.add_widget(top)

        # Circle
        circle_row = BoxLayout(size_hint_y=None, height=220)
        circle_row.add_widget(Widget())
        self.circle = PulsingCircle()
        circle_row.add_widget(self.circle)
        circle_row.add_widget(Widget())
        root.add_widget(circle_row)

        # Status
        self.status = Label(text="🔄 Checking Qwen AI...", font_size="14sp", color=(0.8, 0.4, 0.8, 1), size_hint_y=None, height=30, bold=True)
        root.add_widget(self.status)

        # Chat area
        self.scroll = ScrollView(size_hint=(1, 1), bar_width=4, bar_color=(1, 0, 1, 0.3))
        self.chat = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=[10, 10])
        self.chat.bind(minimum_height=self.chat.setter("height"))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)

        # Input row
        row = BoxLayout(size_hint_y=None, height=55, spacing=8)
        self.ti = TextInput(
            hint_text="💬 Type message to Sania...",
            multiline=False,
            font_size="18sp",
            background_color=(0.08, 0.05, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 0, 1, 1),
            padding=[15, 15],
            hint_text_color=(0.5, 0.3, 0.5, 0.6)
        )
        self.ti.bind(on_text_validate=self.send_msg)
        row.add_widget(self.ti)
        btn = Button(
            text="➤",
            size_hint_x=None, width=65,
            background_color=(1, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size="22sp",
            bold=True
        )
        btn.bind(on_press=self.send_msg)
        row.add_widget(btn)
        root.add_widget(row)

        # Bottom bar
        bottom = BoxLayout(size_hint_y=None, height=28, spacing=5)
        bottom.add_widget(Label(text="[color=ff00ff][b]✦ VIP v4.4 ✦[/b][/color]", font_size="12sp", markup=True, size_hint_x=None, width=110))
        self.ai_badge = Label(text="🔄 Checking...", font_size="11sp", color=(0.4, 0.4, 0.4, 1), size_hint_x=None, width=130)
        bottom.add_widget(self.ai_badge)
        bottom.add_widget(Widget())
        bottom.add_widget(Label(text="[color=cc66cc]by FAHAD_ALI[/color]", font_size="12sp", markup=True, size_hint_x=None, width=110))
        root.add_widget(bottom)

        self.history = []
        Clock.schedule_once(lambda dt: self.check_qwen(), 1)
        Clock.schedule_once(lambda dt: self.add_msg("Assalam o Alaikum jaan! 💕\nMain Sania hoon — REAL AI ke saath! 🧠\nBolo, kya baat karni hai? 😊", True), 2)
        return root

    def check_qwen(self):
        try:
            urllib.request.urlopen(urllib.request.Request(QWEN_URL.replace("/v1/chat/completions", "/health")), timeout=5)
            self.status.text = "🟢 Qwen Connected — Real AI Mode!"
            self.status.color = (0.06, 0.73, 0.51, 1)
            self.ai_badge.text = "🧠 Qwen Online"
            self.ai_badge.color = (0.06, 0.73, 0.51, 1)
        except:
            self.status.text = "🟡 Qwen Offline — Start llama-server in Termux!"
            self.status.color = (0.96, 0.62, 0.04, 1)
            self.ai_badge.text = "🟡 Fallback Mode"
            self.ai_badge.color = (0.96, 0.62, 0.04, 1)

    def send_msg(self, x=None):
        text = self.ti.text.strip()
        if not text: return
        self.add_msg(text, False)
        self.ti.text = ""
        self.history.append({"role": "user", "content": text})
        if len(self.history) > 20: self.history = self.history[-20:]
        self.circle.thinking = True
        self.status.text = "💭 Sania soch rahi hai..."
        self.status.color = (1, 0, 1, 1)
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
        res = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', '', res)
        parts = [s.strip() for s in res.replace('!', '.').replace('?', '.').split('.') if s.strip()]
        res = '. '.join(parts[:2])[:120]
        self.history.append({"role": "assistant", "content": res})
        if len(self.history) > 20: self.history = self.history[-20:]
        Clock.schedule_once(lambda dt: self.add_msg(res, True), 0)
        Clock.schedule_once(lambda dt: setattr(self.circle, 'thinking', False), 0)
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', '🟢 Sania is online!'), 0)
        Clock.schedule_once(lambda dt: setattr(self.status, 'color', (0.06, 0.73, 0.51, 1)), 0)
        Clock.schedule_once(lambda dt: setattr(self.ai_badge, 'text', '🧠 Qwen Online'), 0)
        Clock.schedule_once(lambda dt: setattr(self.ai_badge, 'color', (0.06, 0.73, 0.51, 1)), 0)

    def add_msg(self, text, is_sania):
        if is_sania:
            color = (1, 0.6, 1, 1)
            prefix = "💜 Sania: "
            bg = (0.15, 0.05, 0.25, 1)
        else:
            color = (0.7, 0.85, 1, 1)
            prefix = "💙 You: "
            bg = (0.08, 0.12, 0.25, 1)
        lbl = Label(
            text=prefix + text,
            font_size="16sp",
            color=color,
            size_hint_y=None,
            halign="left",
            valign="top",
            padding=[12, 12],
            bold=False
        )
        lbl.bind(texture_size=lambda inst, val: setattr(inst, "height", max(val[1] + 30, 50)))
        lbl.text_size = (Window.width - 80, None)
        self.chat.add_widget(lbl)
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 0), 0.1)

if __name__ == "__main__":
    SaniaApp().run()

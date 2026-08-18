from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
import urllib.request, json, threading, re

QWEN_URL = "http://127.0.0.1:8080/v1/chat/completions"
PROMPT = "You are Sania, Dr. Fahad AI girlfriend. Roman Urdu ONLY. 5-10 words MAX. Answer exactly what is asked. Casual flirty Pakistani girl. Max 1 emoji. Call him jaan/baby."

class SaniaApp(App):
    def build(self):
        self.title = "Sania Malik"
        Window.clearcolor = (0.04, 0.04, 0.04, 1)
        root = BoxLayout(orientation="vertical", padding=8, spacing=5)
        root.add_widget(Label(text="[b][color=ff00ff]SANIA MALIK[/color][/b]", font_size="20sp", markup=True, size_hint_y=None, height=40))
        self.status = Label(text="Checking Qwen...", font_size="10sp", color=(0.6,0.6,0.8,1), size_hint_y=None, height=22)
        root.add_widget(self.status)
        self.scroll = ScrollView(size_hint=(1,1))
        self.chat = GridLayout(cols=1, spacing=4, size_hint_y=None, padding=[4,4])
        self.chat.bind(minimum_height=self.chat.setter("height"))
        self.scroll.add_widget(self.chat)
        root.add_widget(self.scroll)
        row = BoxLayout(size_hint_y=None, height=42, spacing=5)
        self.ti = TextInput(hint_text="Type message...", multiline=False, font_size="14sp", background_color=(0.08,0.08,0.15,1), foreground_color=(1,1,1,1), cursor_color=(1,0,1,1))
        self.ti.bind(on_text_validate=self.send_msg)
        row.add_widget(self.ti)
        btn = Button(text="Send", size_hint_x=None, width=60, background_color=(1,0,1,1), font_size="14sp")
        btn.bind(on_press=self.send_msg)
        row.add_widget(btn)
        root.add_widget(row)
        self.history = []
        Clock.schedule_once(lambda dt: self.check_qwen(), 1)
        Clock.schedule_once(lambda dt: self.add_msg("Assalam o Alaikum jaan! Main Sania hoon - REAL AI! Bolo kya baat karni hai?", True), 2)
        return root

    def check_qwen(self):
        try:
            urllib.request.urlopen(urllib.request.Request(QWEN_URL.replace("/v1/chat/completions","/health")), timeout=5)
            self.status.text = "Qwen Connected!"
            self.status.color = (0.06,0.73,0.51,1)
        except:
            self.status.text = "Qwen Offline - Start llama-server!"
            self.status.color = (0.96,0.62,0.04,1)

    def send_msg(self, x=None):
        text = self.ti.text.strip()
        if not text: return
        self.add_msg(text, False)
        self.ti.text = ""
        self.history.append({"role":"user","content":text})
        if len(self.history)>20: self.history=self.history[-20:]
        self.status.text = "Thinking..."
        threading.Thread(target=self.call_qwen, args=(text,), daemon=True).start()

    def call_qwen(self, text):
        msgs = [{"role":"system","content":PROMPT}] + self.history
        try:
            p = json.dumps({"messages":msgs,"temperature":0.8,"max_tokens":80,"stream":False}).encode()
            r = urllib.request.Request(QWEN_URL, data=p, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(r, timeout=120) as resp:
                res = json.loads(resp.read())["choices"][0]["message"]["content"].strip()
        except:
            res = "Hmm jaan... Qwen connect nahi hua. Main yahin hoon!"
        res = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', '', res)
        parts = [s.strip() for s in res.replace('!','.').replace('?','.').split('.') if s.strip()]
        res = '. '.join(parts[:2])[:120]
        self.history.append({"role":"assistant","content":res})
        if len(self.history)>20: self.history=self.history[-20:]
        Clock.schedule_once(lambda dt: self.add_msg(res, True), 0)
        Clock.schedule_once(lambda dt: setattr(self.status,'text','Sania online!'), 0)

    def add_msg(self, text, is_s):
        c = (1,0.6,1,1) if is_s else (1,1,1,1)
        pre = "Sania: " if is_s else "You: "
        l = Label(text=pre+text, font_size="13sp", color=c, size_hint_y=None, halign="left", valign="top", padding=[8,8])
        l.bind(texture_size=lambda i,v: setattr(i,"height",v[1]+20))
        l.text_size = (Window.width-60, None)
        self.chat.add_widget(l)
        Clock.schedule_once(lambda dt: setattr(self.scroll,"scroll_y",0), 0.1)

if __name__ == "__main__":
    SaniaApp().run()

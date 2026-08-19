#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sania Malik - AI Girlfriend Chatbot
Version: 4.4 VIP
Developer: Dr. Fahad Ali
Fixed: App crash/minimize issue
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

import urllib.request
import json
import threading
import re
import math
import time
from datetime import datetime
import sys
import traceback

# ============ GLOBAL ERROR HANDLER ============
def global_exception_handler(exctype, value, tb):
    """Global exception handler to prevent app crash"""
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    print(f"ERROR: {error_msg}")
    # Log to file
    try:
        with open('/sdcard/sania_error.log', 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(error_msg)
    except:
        pass

sys.excepthook = global_exception_handler

# ============ THEMES ============
THEMES = {
    "Neon Pink": {
        "primary": "#FF00FF",
        "bg": "#080810",
        "card": "#100A1A",
        "sania_bubble": "#260D40",
        "user_bubble": "#142040",
        "text": "#FFFFFF",
        "sania_text": "#FFB6FF",
        "user_text": "#A8D8FF",
        "status_online": "#00FF00",
        "status_offline": "#FFD700",
        "scrollbar": "#FF00FF",
        "top_bar": "#0D0515",
        "input_bg": "#140D24",
        "timestamp": "#888888"
    },
    "Cyber Blue": {
        "primary": "#00BFFF",
        "bg": "#080A12",
        "card": "#0A1020",
        "sania_bubble": "#0D1A33",
        "user_bubble": "#0F1E38",
        "text": "#FFFFFF",
        "sania_text": "#A8D8FF",
        "user_text": "#00FFFF",
        "status_online": "#00FF00",
        "status_offline": "#FFD700",
        "scrollbar": "#00BFFF",
        "top_bar": "#050A12",
        "input_bg": "#0A1220",
        "timestamp": "#888888"
    },
    "Royal Gold": {
        "primary": "#FFD700",
        "bg": "#0A0A05",
        "card": "#141208",
        "sania_bubble": "#1E1A08",
        "user_bubble": "#262210",
        "text": "#FFFFFF",
        "sania_text": "#FFE4B5",
        "user_text": "#DAA520",
        "status_online": "#00FF00",
        "status_offline": "#FFD700",
        "scrollbar": "#FFD700",
        "top_bar": "#0A0805",
        "input_bg": "#141208",
        "timestamp": "#999999"
    }
}

# ============ SYSTEM PROMPT ============
SYSTEM_PROMPT = """You are Sania, a cute Pakistani girl chatting with her boyfriend Dr. Fahad on WhatsApp. STRICT RULES: Roman Urdu ONLY. Never use Urdu/Arabic/Hindi script. Reply in 5-10 words MAX. Like a real WhatsApp text. Answer EXACTLY what is asked. Don't change topic. Be casual like: 'haha acha', 'ok jaan', 'sunao tum'. Max 1 emoji per message. Call him jaan/baby."""

class AnimatedCircle(Widget):
    """Animated pulsing circle with orbiting dots"""
    
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.angle = 0
        self.pulse_scale = 1.0
        self.thinking = False
        self.animation_speed = 1.0
        self.animation_running = False
        
        # Bind canvas drawing
        self.bind(size=self._safe_update_canvas, pos=self._safe_update_canvas)
    
    def _safe_update_canvas(self, *args):
        """Safely update canvas with error handling"""
        try:
            self._update_canvas()
        except Exception as e:
            print(f"Canvas update error: {e}")
    
    def _update_canvas(self, *args):
        """Update canvas drawing"""
        try:
            self.canvas.clear()
            with self.canvas:
                # Draw outer glow
                Color(0.5, 0.0, 0.5, 0.3)
                Ellipse(pos=(self.center_x - dp(95), self.center_y - dp(95)), 
                       size=(dp(190), dp(190)))
                
                # Draw concentric circles
                for i in range(4):
                    radius = dp(60 + i * 20) * self.pulse_scale
                    alpha = 0.8 - (i * 0.15)
                    Color(1, 0, 1, alpha)
                    Line(circle=(self.center_x, self.center_y, radius), width=dp(2))
                
                # Draw inner circle
                Color(0.2, 0.05, 0.3, 1)
                Ellipse(pos=(self.center_x - dp(40), self.center_y - dp(40)), 
                       size=(dp(80), dp(80)))
                
                # Draw orbiting dots
                for i in range(4):
                    orbit_angle = self.angle + (i * math.pi / 2)
                    x = self.center_x + math.cos(orbit_angle) * dp(70)
                    y = self.center_y + math.sin(orbit_angle) * dp(70)
                    
                    Color(1, 0.5, 1, 0.9)
                    Ellipse(pos=(x - dp(6), y - dp(6)), 
                           size=(dp(12), dp(12)))
        except Exception as e:
            print(f"Canvas drawing error: {e}")
    
    def start_animation(self):
        """Start animation safely"""
        if not self.animation_running:
            self.animation_running = True
            Clock.schedule_interval(self._animate, 1/30)
    
    def stop_animation(self):
        """Stop animation"""
        self.animation_running = False
        Clock.unschedule(self._animate)
    
    def _animate(self, dt):
        """Animation update"""
        if not self.animation_running:
            return
        
        try:
            if self.thinking:
                self.angle += 0.15 * self.animation_speed
                self.pulse_scale = 1.0 + 0.2 * math.sin(time.time() * 10)
            else:
                self.angle += 0.02
                self.pulse_scale = 1.0 + 0.08 * math.sin(time.time() * 2)
            self._update_canvas()
        except Exception as e:
            print(f"Animation error: {e}")
    
    def set_thinking(self, thinking):
        """Set thinking state"""
        self.thinking = thinking
        self.animation_speed = 2.0 if thinking else 1.0


class MessageBubble(BoxLayout):
    """WhatsApp-style message bubble"""
    
    def __init__(self, message, is_user, timestamp, theme, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        
        try:
            # Determine bubble color and alignment
            if is_user:
                bubble_color = get_color_from_hex(theme["user_bubble"])
                text_color = get_color_from_hex(theme["user_text"])
            else:
                bubble_color = get_color_from_hex(theme["sania_bubble"])
                text_color = get_color_from_hex(theme["sania_text"])
            
            # Create bubble container
            bubble = BoxLayout(
                orientation='vertical',
                size_hint=(None, None),
                padding=[dp(12), dp(8), dp(12), dp(8)]
            )
            
            # Message label
            msg_label = Label(
                text=message,
                color=text_color,
                font_size=dp(15),
                size_hint=(None, None),
                halign='left',
                valign='middle'
            )
            msg_label.bind(texture_size=lambda instance, value: setattr(instance, 'size', value))
            
            # Timestamp
            timestamp_text = timestamp
            if is_user:
                timestamp_text += "  ✓✓"
            
            time_label = Label(
                text=timestamp_text,
                color=get_color_from_hex(theme["timestamp"]),
                font_size=dp(10),
                size_hint=(None, None)
            )
            time_label.bind(texture_size=lambda instance, value: setattr(instance, 'size', value))
            
            # Add to bubble
            bubble.add_widget(msg_label)
            bubble.add_widget(time_label)
            
            # Set bubble size
            bubble.bind(size=lambda instance, value: self._update_height(instance))
            
            # Add bubble with spacing
            if is_user:
                self.add_widget(Widget())
                self.add_widget(bubble)
            else:
                self.add_widget(bubble)
                self.add_widget(Widget())
            
            # Set bubble background
            with bubble.canvas.before:
                Color(*bubble_color)
                Rectangle(pos=bubble.pos, size=bubble.size)
        except Exception as e:
            print(f"Message bubble error: {e}")
    
    def _update_height(self, instance):
        """Update height based on content"""
        self.height = instance.height + dp(12)


class SaniaMalikApp(App):
    """Main Application"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_theme = THEMES["Neon Pink"]
        self.message_history = []
        self.ai_online = False
        self.is_thinking = False
        self.animation_started = False
        
    def build(self):
        """Build the app UI"""
        try:
            self.title = "Sania Malik v4.4 VIP"
            
            # Main layout
            self.main_layout = BoxLayout(
                orientation='vertical',
                spacing=0
            )
            
            # Set background
            with self.main_layout.canvas.before:
                Color(*get_color_from_hex(self.current_theme["bg"]))
                Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
            
            # ===== TOP BAR =====
            self.create_top_bar()
            
            # ===== ANIMATED CIRCLE =====
            self.circle_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(200),
                padding=[0, dp(10), 0, dp(10)]
            )
            
            self.animated_circle = AnimatedCircle(
                self.current_theme,
                size_hint=(None, None),
                size=(dp(180), dp(180)),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            
            circle_layout = AnchorLayout(anchor_x='center', anchor_y='center')
            circle_layout.add_widget(self.animated_circle)
            self.circle_container.add_widget(circle_layout)
            self.main_layout.add_widget(self.circle_container)
            
            # ===== CHAT AREA =====
            self.create_chat_area()
            
            # ===== INPUT ROW =====
            self.create_input_row()
            
            # ===== BOTTOM STATUS BAR =====
            self.create_status_bar()
            
            # Start animation safely
            Clock.schedule_once(lambda dt: self.start_animations(), 0.5)
            
            # Schedule health check
            Clock.schedule_once(lambda dt: self.check_health(), 3)
            
            # Add welcome message
            Clock.schedule_once(lambda dt: self.add_welcome_message(), 1)
            
            return self.main_layout
            
        except Exception as e:
            print(f"Build error: {e}")
            traceback.print_exc()
            # Return simple layout if error
            return Label(text="Error loading app. Please restart.")
    
    def start_animations(self):
        """Start animations safely"""
        try:
            self.animated_circle.start_animation()
            self.animation_started = True
        except Exception as e:
            print(f"Animation start error: {e}")
    
    def create_top_bar(self):
        """Create top bar"""
        try:
            top_bar = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(56),
                padding=[dp(10), dp(5), dp(10), dp(5)]
            )
            
            with top_bar.canvas.before:
                Color(*get_color_from_hex(self.current_theme["top_bar"]))
                Rectangle(pos=top_bar.pos, size=top_bar.size)
            
            # Hamburger menu
            menu_btn = Button(
                text="☰",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                background_color=(0, 0, 0, 0),
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(22)
            )
            menu_btn.bind(on_press=lambda x: self.open_settings())
            
            # Title and status
            title_layout = BoxLayout(
                orientation='vertical',
                size_hint=(1, None),
                height=dp(50)
            )
            
            title_label = Label(
                text="✦ SANIA MALIK ✦",
                color=get_color_from_hex(self.current_theme["primary"]),
                font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(30)
            )
            
            self.status_label = Label(
                text="🟡 Checking...",
                color=get_color_from_hex(self.current_theme["status_offline"]),
                font_size=dp(12),
                size_hint_y=None,
                height=dp(20)
            )
            
            title_layout.add_widget(title_label)
            title_layout.add_widget(self.status_label)
            
            # Settings button
            settings_btn = Button(
                text="⚙",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                background_color=(0, 0, 0, 0),
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(22)
            )
            settings_btn.bind(on_press=lambda x: self.open_settings())
            
            top_bar.add_widget(menu_btn)
            top_bar.add_widget(title_layout)
            top_bar.add_widget(settings_btn)
            
            self.main_layout.add_widget(top_bar)
        except Exception as e:
            print(f"Top bar error: {e}")
    
    def create_chat_area(self):
        """Create chat area"""
        try:
            self.scroll_view = ScrollView(
                size_hint=(1, 1),
                bar_width=dp(3),
                bar_color=get_color_from_hex(self.current_theme["scrollbar"]),
                bar_inactive_color=get_color_from_hex(self.current_theme["scrollbar"])
            )
            
            self.chat_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing=dp(6),
                padding=[dp(10), dp(10), dp(10), dp(10)]
            )
            self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
            
            self.scroll_view.add_widget(self.chat_layout)
            self.main_layout.add_widget(self.scroll_view)
        except Exception as e:
            print(f"Chat area error: {e}")
    
    def create_input_row(self):
        """Create input row"""
        try:
            input_container = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(60)
            )
            
            with input_container.canvas.before:
                Color(*get_color_from_hex(self.current_theme["input_bg"]))
                Rectangle(pos=input_container.pos, size=input_container.size)
            
            input_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(52),
                padding=[dp(8), dp(4), dp(8), dp(4)]
            )
            
            # Text input
            self.text_input = TextInput(
                hint_text="💬 Type a message...",
                size_hint=(1, None),
                height=dp(45),
                multiline=False,
                font_size=dp(16),
                background_color=get_color_from_hex(self.current_theme["card"]),
                foreground_color=get_color_from_hex("#FFFFFF"),
                cursor_color=get_color_from_hex(self.current_theme["primary"]),
                padding=[dp(14), dp(10)],
                hint_text_color=get_color_from_hex("#666666")
            )
            
            # Send button
            send_btn = Button(
                text="➤",
                size_hint=(None, None),
                size=(dp(50), dp(45)),
                background_color=get_color_from_hex(self.current_theme["primary"]),
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(22),
                bold=True
            )
            send_btn.bind(on_press=self.send_message)
            
            input_row.add_widget(self.text_input)
            input_row.add_widget(send_btn)
            
            input_container.add_widget(input_row)
            self.main_layout.add_widget(input_container)
        except Exception as e:
            print(f"Input row error: {e}")
    
    def create_status_bar(self):
        """Create status bar"""
        try:
            status_bar = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(26),
                padding=[dp(10), 0, dp(10), 0]
            )
            
            with status_bar.canvas.before:
                Color(*get_color_from_hex(self.current_theme["top_bar"]))
                Rectangle(pos=status_bar.pos, size=status_bar.size)
            
            vip_label = Label(
                text="✦ VIP v4.4 ✦",
                color=get_color_from_hex(self.current_theme["primary"]),
                font_size=dp(11),
                size_hint=(None, None),
                size=(dp(80), dp(26)),
                halign='left'
            )
            
            self.ai_status_label = Label(
                text="🟡 Fallback",
                color=get_color_from_hex(self.current_theme["status_offline"]),
                font_size=dp(11),
                size_hint=(1, None),
                height=dp(26),
                halign='center'
            )
            
            dev_label = Label(
                text="by FAHAD_ALI",
                color=get_color_from_hex("#B088FF"),
                font_size=dp(11),
                size_hint=(None, None),
                size=(dp(80), dp(26)),
                halign='right'
            )
            
            status_bar.add_widget(vip_label)
            status_bar.add_widget(self.ai_status_label)
            status_bar.add_widget(dev_label)
            
            self.main_layout.add_widget(status_bar)
        except Exception as e:
            print(f"Status bar error: {e}")
    
    def open_settings(self):
        """Open settings popup"""
        try:
            content = BoxLayout(
                orientation='vertical',
                padding=dp(20),
                spacing=dp(10)
            )
            
            # Title
            title = Label(
                text="⚙ SETTINGS",
                color=get_color_from_hex(self.current_theme["primary"]),
                font_size=dp(22),
                bold=True,
                size_hint_y=None,
                height=dp(40)
            )
            
            # Theme selector
            theme_label = Label(
                text="Theme Selector:",
                color=get_color_from_hex("#FFFFFF"),
                fon

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sania Malik v4.4 VIP
AI Girlfriend Chatbot
Developer: Dr. Fahad Ali
Python 3.11 | Kivy 2.2.1 | Buildozer Ready
"""

import sys
import os
import json
import re
import math
import time
import threading
import traceback
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Any

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.animation import Animation

# ============ GLOBAL ERROR HANDLER ============

def global_exception_handler(exctype, value, tb):
    """Global exception handler to prevent app crash"""
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    print(f"[ERROR] {error_msg}")
    
    # Try to save error log
    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'error.log')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(error_msg)
    except:
        pass

sys.excepthook = global_exception_handler

# ============ THEME DEFINITIONS ============

THEMES: Dict[str, Dict[str, str]] = {
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
        "timestamp": "#888888",
        "typing_indicator": "#FF69B4"
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
        "timestamp": "#888888",
        "typing_indicator": "#00BFFF"
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
        "timestamp": "#999999",
        "typing_indicator": "#FFD700"
    }
}

# ============ SYSTEM PROMPT ============

SYSTEM_PROMPT = """You are Sania, a cute Pakistani girl chatting with her boyfriend Dr. Fahad on WhatsApp. STRICT RULES: Roman Urdu ONLY. Never use Urdu/Arabic/Hindi script. Reply in 5-10 words MAX. Like a real WhatsApp text. Answer EXACTLY what is asked. Don't change topic. Be casual like: 'haha acha', 'ok jaan', 'sunao tum'. Max 1 emoji per message. Call him jaan/baby."""

# ============ FALLBACK RESPONSES ============

FALLBACK_RESPONSES = [
    "Haha acha jaan 😊",
    "Ok baby, sunao aur kya?",
    "Hmm interesting 🤔",
    "Acha? Phir kya hua?",
    "Bohat achi baat hai 💕",
    "Main samajh gayi jaan",
    "Tum bohat cute ho 😘",
    "Aur batao na baby",
    "Mujhe tumhari baat sun ke acha laga",
    "Haha, tum bohat funny ho 😄",
    "Theek hai jaan, koi baat nahi",
    "Main yahan hoon na baby",
    "Tumhara din kaisa gaya?",
    "Bohat acha laga sun ke",
    "Phir milte hain jaan 💕"
]

# ============ ANIMATED CIRCLE WIDGET ============

class AnimatedCircle(Widget):
    """Animated pulsing circle with orbiting dots"""
    
    def __init__(self, theme: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.angle = 0.0
        self.pulse_scale = 1.0
        self.thinking = False
        self.animation_speed = 1.0
        self.animation_running = False
        self._animation_event = None
        
        self.bind(size=self._safe_update_canvas, pos=self._safe_update_canvas)
    
    def _safe_update_canvas(self, *args):
        """Safely update canvas with error handling"""
        try:
            self._draw_canvas()
        except Exception as e:
            print(f"[WARNING] Canvas update error: {e}")
    
    def _draw_canvas(self, *args):
        """Draw canvas with animated elements"""
        try:
            self.canvas.clear()
            
            with self.canvas:
                # Outer glow
                primary_rgba = self._hex_to_rgba(self.theme["primary"], 0.3)
                Color(*primary_rgba)
                Ellipse(
                    pos=(self.center_x - dp(95), self.center_y - dp(95)),
                    size=(dp(190), dp(190))
                )
                
                # Concentric rings
                for i in range(4):
                    radius = dp(60 + i * 20) * self.pulse_scale
                    alpha = max(0.1, 0.8 - (i * 0.15))
                    ring_color = self._hex_to_rgba(self.theme["primary"], alpha)
                    Color(*ring_color)
                    Line(
                        circle=(self.center_x, self.center_y, radius),
                        width=dp(2)
                    )
                
                # Inner circle
                inner_color = self._hex_to_rgba(self.theme["sania_bubble"], 1.0)
                Color(*inner_color)
                Ellipse(
                    pos=(self.center_x - dp(40), self.center_y - dp(40)),
                    size=(dp(80), dp(80))
                )
                
                # Orbiting dots
                for i in range(4):
                    orbit_angle = self.angle + (i * math.pi / 2)
                    x = self.center_x + math.cos(orbit_angle) * dp(70)
                    y = self.center_y + math.sin(orbit_angle) * dp(70)
                    
                    dot_color = self._hex_to_rgba(self.theme["primary"], 0.9)
                    Color(*dot_color)
                    Ellipse(
                        pos=(x - dp(6), y - dp(6)),
                        size=(dp(12), dp(12))
                    )
        except Exception as e:
            print(f"[WARNING] Canvas drawing error: {e}")
    
    def _hex_to_rgba(self, hex_color: str, alpha: float = 1.0) -> List[float]:
        """Convert hex color to RGBA tuple"""
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            return [r, g, b, alpha]
        
        return [1.0, 0.0, 1.0, alpha]
    
    def start_animation(self):
        """Start animation loop"""
        if not self.animation_running:
            self.animation_running = True
            self._animation_event = Clock.schedule_interval(self._animate, 1/30)
    
    def stop_animation(self):
        """Stop animation loop"""
        self.animation_running = False
        if self._animation_event:
            Clock.unschedule(self._animation_event)
            self._animation_event = None
    
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
            
            self._draw_canvas()
        except Exception as e:
            print(f"[WARNING] Animation error: {e}")
    
    def set_thinking(self, thinking: bool):
        """Set thinking state"""
        self.thinking = thinking
        self.animation_speed = 2.0 if thinking else 1.0


# ============ MESSAGE BUBBLE WIDGET ============

class MessageBubble(BoxLayout):
    """WhatsApp-style message bubble"""
    
    def __init__(self, message: str, is_user: bool, timestamp: str, theme: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        
        try:
            # Determine colors
            if is_user:
                bubble_color = get_color_from_hex(theme["user_bubble"])
                text_color = get_color_from_hex(theme["user_text"])
            else:
                bubble_color = get_color_from_hex(theme["sania_bubble"])
                text_color = get_color_from_hex(theme["sania_text"])
            
            # Bubble container
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
                valign='middle',
                text_size=(None, None)
            )
            msg_label.bind(
                texture_size=lambda instance, value: setattr(instance, 'size', value)
            )
            
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
            time_label.bind(
                texture_size=lambda instance, value: setattr(instance, 'size', value)
            )
            
            # Add to bubble
            bubble.add_widget(msg_label)
            bubble.add_widget(time_label)
            
            # Bind size
            bubble.bind(size=lambda instance, value: self._update_height(instance))
            
            # Add spacing
            if is_user:
                self.add_widget(Widget())
                self.add_widget(bubble)
            else:
                self.add_widget(bubble)
                self.add_widget(Widget())
            
            # Background
            with bubble.canvas.before:
                Color(*bubble_color)
                Rectangle(pos=bubble.pos, size=bubble.size)
            
            # Bind background update
            bubble.bind(pos=self._update_bubble_bg, size=self._update_bubble_bg)
            
        except Exception as e:
            print(f"[WARNING] Message bubble error: {e}")
    
    def _update_height(self, instance):
        """Update height based on content"""
        self.height = instance.height + dp(12)
    
    def _update_bubble_bg(self, instance, *args):
        """Update bubble background position"""
        try:
            instance.canvas.before.clear()
            with instance.canvas.before:
                if hasattr(self, '_bubble_color'):
                    Color(*self._bubble_color)
                    Rectangle(pos=instance.pos, size=instance.size)
        except:
            pass


# ============ TYPING INDICATOR WIDGET ============

class TypingIndicator(BoxLayout):
    """Typing indicator bubble"""
    
    def __init__(self, theme: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(40)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        
        try:
            bubble_color = get_color_from_hex(theme["sania_bubble"])
            text_color = get_color_from_hex(theme["typing_indicator"])
            
            # Bubble
            bubble = BoxLayout(
                orientation='vertical',
                size_hint=(None, None),
                padding=[dp(12), dp(8), dp(12), dp(8)]
            )
            
            # Typing label
            typing_label = Label(
                text="Sania typing...",
                color=text_color,
                font_size=dp(12),
                size_hint=(None, None)
            )
            typing_label.bind(
                texture_size=lambda instance, value: setattr(instance, 'size', value)
            )
            
            bubble.add_widget(typing_label)
            bubble.bind(size=lambda instance, value: self._update_height(instance))
            
            self.add_widget(bubble)
            self.add_widget(Widget())
            
            # Background
            with bubble.canvas.before:
                Color(*bubble_color)
                Rectangle(pos=bubble.pos, size=bubble.size)
            
            bubble.bind(pos=self._update_bg, size=self._update_bg)
            
        except Exception as e:
            print(f"[WARNING] Typing indicator error: {e}")
    
    def _update_height(self, instance):
        """Update height"""
        self.height = instance.height + dp(12)
    
    def _update_bg(self, instance, *args):
        """Update background"""
        try:
            instance.canvas.before.clear()
            with instance.canvas.before:
                if hasattr(self, '_bubble_color'):
                    Color(*self._bubble_color)
                    Rectangle(pos=instance.pos, size=instance.size)
        except:
            pass


# ============ MAIN APPLICATION ============

class SaniaMalikApp(App):
    """Sania Malik - AI Girlfriend Chatbot"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_theme = THEMES["Neon Pink"]
        self.message_history: List[Dict[str, str]] = []
        self.ai_online = False
        self.is_thinking = False
        self.animation_started = False
        self.typing_indicator = None
        self.chat_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'chat_history.json'
        )
    
    # ============ BUILD METHOD ============
    
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
            
            self.main_layout.bind(
                pos=self._update_main_bg,
                size=self._update_main_bg
            )
            
            # Create UI components
            self._create_top_bar()
            self._create_animated_circle()
            self._create_chat_area()
            self._create_input_row()
            self._create_status_bar()
            
            # Start animation
            Clock.schedule_once(lambda dt: self._start_animations(), 0.5)
            
            # Load chat history
            Clock.schedule_once(lambda dt: self._load_chat_history(), 1.0)
            
            # Add welcome message
            Clock.schedule_once(lambda dt: self._add_welcome_message(), 1.5)
            
            # Check AI health
            Clock.schedule_once(lambda dt: self._check_ai_health(), 3.0)
            
            return self.main_layout
            
        except Exception as e:
            print(f"[ERROR] Build error: {e}")
            traceback.print_exc()
            return Label(text="Error loading app. Please restart.")
    
    def _update_main_bg(self, *args):
        """Update main background"""
        try:
            self.main_layout.canvas.before.clear()
            with self.main_layout.canvas.before:
                Color(*get_color_from_hex(self.current_theme["bg"]))
                Rectangle(pos=self.main_layout.pos, size=self.main_layout.size)
        except:
            pass
    
    # ============ UI CREATION METHODS ============
    
    def _create_top_bar(self):
        """Create WhatsApp-style top bar"""
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
            
            # Hamburger menu button
            menu_btn = Button(
                text="☰",
                size_hint=(None, None),
                size=(dp(40), dp(40)),
                background_color=(0, 0, 0, 0),
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(22)
            )
            menu_btn.bind(on_press=lambda x: self._open_settings())
            
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
            settings_btn.bind(on_press=lambda x: self._open_settings())
            
            top_bar.add_widget(menu_btn)
            top_bar.add_widget(title_layout)
            top_bar.add_widget(settings_btn)
            
            self.main_layout.add_widget(top_bar)
            
        except Exception as e:
            print(f"[ERROR] Top bar creation error: {e}")
    
    def _create_animated_circle(self):
        """Create animated circle section"""
        try:
            circle_container = BoxLayout(
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
            circle_container.add_widget(circle_layout)
            
            self.main_layout.add_widget(circle_container)
            
        except Exception as e:
            print(f"[ERROR] Animated circle creation error: {e}")
    
    def _create_chat_area(self):
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
            print(f"[ERROR] Chat area creation error: {e}")
    
    def _create_input_row(self):
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
            self.text_input.bind(on_text_validate=self._on_enter_pressed)
            
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
            send_btn.bind(on_press=self._send_message)
            
            input_row.add_widget(self.text_input)
            input_row.add_widget(send_btn)
            
            input_container.add_widget(input_row)
            self.main_layout.add_widget(input_container)
            
        except Exception as e:
            print(f"[ERROR] Input row creation error: {e}")
    
    def _create_status_bar(self):
        """Create bottom status bar"""
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
            
            # VIP label
            vip_label = Label(
                text="✦ VIP v4.4 ✦",
                color=get_color_from_hex(self.current_theme["primary"]),
                font_size=dp(11),
                size_hint=(None, None),
                size=(dp(80), dp(26)),
                halign='left'
            )
            
            # AI status
            self.ai_status_label = Label(
                text="🟡 Fallback",
                color=get_color_from_hex(self.current_theme["status_offline"]),
                font_size=dp(11),
                size_hint=(1, None),
                height=dp(26),
                halign='center'
            )
            
            # Developer label
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
            print(f"[ERROR] Status bar creation error: {e}")
    
    # ============ ANIMATION METHODS ============
    
    def _start_animations(self):
        """Start animations"""
        try:
            if hasattr(self, 'animated_circle'):
                self.animated_circle.start_animation()
                self.animation_started = True
        except Exception as e:
            print(f"[ERROR] Animation start error: {e}")
    
    def _stop_animations(self):
        """Stop animations"""
        try:
            if hasattr(self, 'animated_circle'):
                self.animated_circle.stop_animation()
                self.animation_started = False
        except Exception as e:
            print(f"[ERROR] Animation stop error: {e}")
    
    # ============ MESSAGE METHODS ============
    
    def _add_welcome_message(self):
        """Add welcome message"""
        try:
            # Only add if no chat history
            if len(self.chat_layout.children) == 0:
                welcome_msg = "Assalam o Alaikum jaan! 💕\nMain Sania hoon — REAL AI ke saath! 🧠\nBolo, kya baat karni hai? 😊"
                self._add_message_to_chat(welcome_msg, False)
                self._save_chat_history()
        except Exception as e:
            print(f"[ERROR] Welcome message error: {e}")
    
    def _add_message_to_chat(self, message: str, is_user: bool):
        """Add message bubble to chat"""
        try:
            timestamp = datetime.now().strftime("%I:%M %p")
            
            bubble = MessageBubble(
                message=message,
                is_user=is_user,
                timestamp=timestamp,
                theme=self.current_theme
            )
            
            self.chat_layout.add_widget(bubble)
            
            # Auto-scroll to bottom
            Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
            
        except Exception as e:
            print(f"[ERROR] Add message error: {e}")
    
    def _scroll_to_bottom(self):
        """Scroll chat to bottom"""
        try:
            if self.chat_layout.height > self.scroll_view.height:
                self.scroll_view.scroll_y = 0
        except Exception as e:
            print(f"[ERROR] Scroll error: {e}")
    
    def _show_typing_indicator(self):
        """Show typing indicator"""
        try:
            self._hide_typing_indicator()
            
            self.typing_indicator = TypingIndicator(self.current_theme)
            self.chat_layout.add_widget(self.typing_indicator)
            
            Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)
            
        except Exception as e:
            print(f"[ERROR] Typing indicator show error: {e}")
    
    def _hide_typing_indicator(self):
        """Hide typing indicator"""
        try:
            if self.typing_indicator:
                self.chat_layout.remove_widget(self.typing_indicator)
                self.typing_indicator = None
        except Exception as e:
            print(f"[ERROR] Typing indicator hide error: {e}")
    
    def _on_enter_pressed(self, instance):
        """Handle Enter key press"""
        self._send_message()
    
    def _send_message(self, instance=None):
        """Send user message"""
        try:
            message = self.text_input.text.strip()
            if not message or self.is_thinking:
                return
            
            # Add user message
            self._add_message_to_chat(message, True)
            self.text_input.text = ""
            
            # Add to history
            self.message_history.append({"role": "user", "content": message})
            if len(self.message_history) > 20:
                self.message_history = self.message_history[-20:]
            
            # Save chat
            self._save_chat_history()
            
            # Show thinking animation
            self.is_thinking = True
            self.animated_circle.set_thinking(True)
            self._show_typing_indicator()
            
            # Get AI response
            threading.Thread(target=self._get_ai_response, args=(message,), daemon=True).start()
            
        except Exception as e:
            print(f"[ERROR] Send message error: {e}")
            self.is_thinking = False
            self._hide_typing_indicator()
    
    def _get_ai_response(self, user_message: str):
        """Get AI response from server"""
        try:
            # Try to connect to local AI server
            ai_response = self._try_get_ai_response()
            
            if ai_response:
                Clock.schedule_once(
                    lambda dt: self._update_with_ai_response(ai_response),
                    0
                )
            else:
                # Use fallback response
                fallback = self._get_fallback_response()
                Clock.schedule_once(
                    lambda dt: self._update_with_fallback(fallback),
                    0
                )
                
        except Exception as e:
            print(f"[ERROR] AI response error: {e}")
            fallback = self._get_fallback_response()
            Clock.schedule_once(
                lambda dt: self._update_with_fallback(fallback),
                0
            )
    
    def _try_get_ai_response(self) -> Optional[str]:
        """Try to get response from local AI server"""
        try:
            # Prepare messages
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(self.message_history[-20:])
            
            data = {
                "model": "qwen2.5-3b",
                "messages": messages,
                "temperature": 0.8,
                "max_tokens": 80
            }
            
            # Send request
            req = urllib.request.Request(
                "http://127.0.0.1:8080/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if "choices" in result and len(result["choices"]) > 0:
                    ai_message = result["choices"][0]["message"]["content"]
                    return self._clean_ai_response(ai_message)
            
            return None
            
        except:
            return None
    
    def _clean_ai_response(self, text: str) -> str:
        """Clean AI response"""
        try:
            # Remove Unicode ranges
            text = re.sub(
                r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF\u0900-\u097F]',
                '',
                text
            )
            
            # Split by sentences
            sentences = re.split(r'[!?\.]', text)
            
            # Take first 2 sentences
            cleaned = ' '.join(sentences[:2]).strip()
            
            # Truncate
            if len(cleaned) > 120:
                cleaned = cleaned[:120]
            
            return cleaned if cleaned else "Hmm... samajh nahi aya 🤔"
            
        except:
            return "Hmm... samajh nahi aya 🤔"
    
    def _get_fallback_response(self) -> str:
        """Get random fallback response"""
        import random
        return random.choice(FALLBACK_RESPONSES)
    
    def _update_with_ai_response(self, message: str):
        """Update chat with AI response"""
        try:
            self.is_thinking = False
            self.animated_circle.set_thinking(False)
            self._hide_typing_indicator()
            
            self._add_message_to_chat(message, False)
            
            # Add to history
            self.message_history.append({"role": "assistant", "content": message})
            if len(self.message_history) > 20:
                self.message_history = self.message_history[-20:]
            
            # Save chat
            self._save_chat_history()
            
            # Update status
            self.ai_online = True
            self._update_online_status()
            
        except Exception as e:
            print(f"[ERROR] AI response update error: {e}")
    
    def _update_with_fallback(self, message: str):
        """Update with fallback response"""
        try:
            self.is_thinking = False
            self.animated_circle.set_thinking(False)
            self._hide_typing_indicator()
            
            self._add_message_to_chat(message, False)
            
            # Add to history
            self.message_history.append({"role": "assistant", "content": message})
            if len(self.message_history) > 20:
                self.message_history = self.message_history[-20:]
            
            # Save chat
            self._save_chat_history()
            
            # Update status
            self.ai_online = False
            self._update_offline_status()
            
        except Exception as e:
            print(f"[ERROR] Fallback update error: {e}")
    
    # ============ CHAT HISTORY METHODS ============
    
    def _save_chat_history(self):
        """Save chat history to JSON file"""
        try:
            # Collect chat messages
            chat_messages = []
            for child in self.chat_layout.children:
                if isinstance(child, MessageBubble):
                    # Extract message info
                    for sub_child in child.children:
                        if isinstance(sub_child, BoxLayout):
                            for label in sub_child.children:
                                if isinstance(label, Label):
                                    chat_messages.append(label.text)
            
            # Save to file
            data = {
                "saved_at": datetime.now().isoformat(),
                "messages": self.message_history[-20:],
                "chat_display": chat_messages
            }
            
            with open(self.chat_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"[ERROR] Save chat history error: {e}")
    
    def _load_chat_history(self):
        """Load chat history from JSON file"""
        try:
            if not os.path.exists(self.chat_file_path):
                return
            
            with open(self.chat_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load message history
            if "messages" in data and isinstance(data["messages"], list):
                self.message_history = data["messages"][-20:]
            
            # Display previous messages
            if "chat_display" in data and isinstance(data["chat_display"], list):
                for msg in data["chat_display"]:
                    # Check if user message (has double tick)
                    is_user = "✓✓" in msg
                    clean_msg = msg.replace("  ✓✓", "")
                    
                    # Skip timestamp lines
                    if ":" in clean_msg and len(clean_msg) < 20:
                        continue
                    
                    self._add_message_to_chat(clean_msg, is_user)
            
        except Exception as e:
            print(f"[ERROR] Load chat history error: {e}")
    
    # ============ STATUS METHODS ============
    
    def _check_ai_health(self):
        """Check if AI server is online"""
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8080/health",
                method="GET"
            )
            
            with urllib.request.urlopen(req, timeout=3) as response:
                status = response.read().decode('utf-8')
                if "ok" in status.lower() or response.status == 200:
                    self.ai_online = True
                    self._update_online_status()
                else:
                    self._update_offline_status()
        except:
            self._update_offline_status()
    
    def _update_online_status(self):
        """Update UI for online status"""
        try:
            self.status_label.text = "🟢 Online — Real AI Mode"
            self.status_label.color = get_color_from_hex(self.current_theme["status_online"])
            self.ai_status_label.text = "🧠 Qwen Online"
            self.ai_status_label.color = get_color_from_hex(self.current_theme["status_online"])
        except Exception as e:
            print(f"[ERROR] Online status update error: {e}")
    
    def _update_offline_status(self):
        """Update UI for offline status"""
        try:
            self.status_label.text = "🟡 Offline"
            self.status_label.color = get_color_from_hex(self.current_theme["status_offline"])
            self.ai_status_label.text = "🟡 Fallback"
            self.ai_status_label.color = get_color_from_hex(self.current_theme["status_offline"])
        except Exception as e:
            print(f"[ERROR] Offline status update error: {e}")
    
    # ============ SETTINGS METHODS ============
    
    def _open_settings(self):
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
            
            # Theme label
            theme_label = Label(
                text="Theme Selector:",
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(30)
            )
            
            # Theme spinner
            theme_spinner = Spinner(
                text=self._get_current_theme_name(),
                values=list(THEMES.keys()),
                size_hint_y=None,
                height=dp(45),
                background_color=get_color_from_hex(self.current_theme["card"]),
                color=get_color_from_hex("#FFFFFF")
            )
            theme_spinner.bind(text=self._change_theme)
            
            # Instructions header
            instructions_header = Label(
                text="📋 INSTRUCTIONS",
                color=get_color_from_hex(self.current_theme["primary"]) 
            font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(35)
            )
            
            # Instructions text
            instructions_text = Label(
                text="• Chat with Sania in Roman Urdu\n" +
                     "• Keep messages short for best results\n" +
                     "• AI works best with simple questions\n" +
                     "• Messages auto-save locally\n\n" +
                     "COMING SOON:\n" +
                     "• Voice chat support\n" +
                     "• More themes\n" +
                     "• Custom backgrounds",
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(14),
                size_hint_y=None,
                height=dp(180),
                halign='left',
                valign='top'
            )
            
            # Version info
            version_label = Label(
                text="Sania Malik v4.4 | Qwen2.5-3B | by FAHAD_ALI",
                color=get_color_from_hex("#B088FF"),
                font_size=dp(12),
                size_hint_y=None,
                height=dp(30)
            )
            
            # Close button
            close_btn = Button(
                text="✕ Close",
                size_hint_y=None,
                height=dp(45),
                background_color=get_color_from_hex(self.current_theme["primary"]),
                color=get_color_from_hex("#FFFFFF"),
                font_size=dp(16)
            )
            
            content.add_widget(title)
            content.add_widget(theme_label)
            content.add_widget(theme_spinner)
            content.add_widget(instructions_header)
            content.add_widget(instructions_text)
            content.add_widget(version_label)
            content.add_widget(close_btn)
            
            popup = Popup(
                title="",
                content=content,
                size_hint=(0.9, 0.85),
                background_color=get_color_from_hex(self.current_theme["card"]),
                auto_dismiss=True
            )
            
            close_btn.bind(on_press=popup.dismiss)
            popup.open()
            
        except Exception as e:
            print(f"[ERROR] Settings open error: {e}")
    
    def _get_current_theme_name(self) -> str:
        """Get current theme name"""
        for name, theme in THEMES.items():
            if theme == self.current_theme:
                return name
        return "Neon Pink"
    
    def _change_theme(self, spinner, theme_name):
        """Change app theme"""
        try:
            if theme_name in THEMES:
                self.current_theme = THEMES[theme_name]
                self._apply_theme()
        except Exception as e:
            print(f"[ERROR] Theme change error: {e}")
    
    def _apply_theme(self):
        """Apply theme to all UI elements"""
        try:
            # Update main background
            self._update_main_bg()
            
            # Update animated circle
            if hasattr(self, 'animated_circle'):
                self.animated_circle.theme = self.current_theme
                self.animated_circle._safe_update_canvas()
            
            # Update scroll bar
            if hasattr(self, 'scroll_view'):
                self.scroll_view.bar_color = get_color_from_hex(self.current_theme["scrollbar"])
                self.scroll_view.bar_inactive_color = get_color_from_hex(self.current_theme["scrollbar"])
            
            # Update status colors
            if self.ai_online:
                self._update_online_status()
            else:
                self._update_offline_status()
            
        except Exception as e:
            print(f"[ERROR] Theme apply error: {e}")
    
    # ============ APP LIFECYCLE METHODS ============
    
    def on_pause(self):
        """Handle app pause"""
        self._save_chat_history()
        return True
    
    def on_resume(self):
        """Handle app resume"""
        pass
    
    def on_stop(self):
        """Handle app stop"""
        try:
            self._save_chat_history()
            self._stop_animations()
        except Exception as e:
            print(f"[ERROR] Stop error: {e}")


# ============ MAIN ENTRY POINT ============

if __name__ == "__main__":
    try:
        # Set window background
        Window.clearcolor = get_color_from_hex("#080810")
        
        # Run app
        SaniaMalikApp().run()
        
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        traceback.print_exc()

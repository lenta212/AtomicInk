import os
import sys
import subprocess
import platform
import json
import threading
import uuid
import datetime
import traceback
import math
import random
import urllib.parse
import re
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

import minecraft_launcher_lib
import psutil


# ══════════════════════════════════════════
#  ВЕРСИИ MINECRAFT + FORGE
# ══════════════════════════════════════════

# Файл для хранения пользовательских версий
CUSTOM_VERSIONS_FILE = os.path.join(os.path.expanduser("~"), ".minecraft", "launcher_custom_versions.json")

def load_custom_versions():
    """Загружает пользовательские версии из файла"""
    if os.path.exists(CUSTOM_VERSIONS_FILE):
        try:
            with open(CUSTOM_VERSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_custom_versions(custom_versions):
    """Сохраняет пользовательские версии в файл"""
    os.makedirs(os.path.dirname(CUSTOM_VERSIONS_FILE), exist_ok=True)
    with open(CUSTOM_VERSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(custom_versions, f, indent=2, ensure_ascii=False)

def get_all_versions():
    """Возвращает словарь всех версий (встроенные + пользовательские)"""
    all_vers = VERSIONS.copy()
    custom = load_custom_versions()
    all_vers.update(custom)
    return all_vers

VERSIONS = {
    # ── 1.7.10 ─────────────────────────────────────────────────────────────
    "1.7.10 Vanilla":  {"mc_version": "1.7.10",  "loader": "vanilla"},
    "1.7.10 Forge":    {"mc_version": "1.7.10",  "forge": "1.7.10-10.13.4.1614-1.7.10", "loader": "forge"},
    # ── 1.8.9 ──────────────────────────────────────────────────────────────
    "1.8.9 Vanilla":   {"mc_version": "1.8.9",   "loader": "vanilla"},
    "1.8.9 Forge":     {"mc_version": "1.8.9",   "forge": "1.8.9-11.15.1.2318-1.8.9", "loader": "forge"},
    # ── 1.9.4 ──────────────────────────────────────────────────────────────
    "1.9.4 Vanilla":   {"mc_version": "1.9.4",   "loader": "vanilla"},
    "1.9.4 Forge":     {"mc_version": "1.9.4",   "forge": "1.9.4-12.17.0.2317-1.9.4", "loader": "forge"},
    # ── 1.10.2 ─────────────────────────────────────────────────────────────
    "1.10.2 Vanilla":  {"mc_version": "1.10.2",  "loader": "vanilla"},
    "1.10.2 Forge":    {"mc_version": "1.10.2",  "forge": "1.10.2-12.18.3.2511", "loader": "forge"},
    # ── 1.11.2 ─────────────────────────────────────────────────────────────
    "1.11.2 Vanilla":  {"mc_version": "1.11.2",  "loader": "vanilla"},
    "1.11.2 Forge":    {"mc_version": "1.11.2",  "forge": "1.11.2-13.20.1.2588", "loader": "forge"},
    # ── 1.12.2 ─────────────────────────────────────────────────────────────
    "1.12.2 Vanilla":  {"mc_version": "1.12.2",  "loader": "vanilla"},
    "1.12.2 Forge":    {"mc_version": "1.12.2",  "forge": "1.12.2-14.23.5.2859",  "loader": "forge"},
    # ── 1.13.2 ─────────────────────────────────────────────────────────────
    "1.13.2 Vanilla":  {"mc_version": "1.13.2",  "loader": "vanilla"},
    "1.13.2 Forge":    {"mc_version": "1.13.2",  "forge": "1.13.2-25.0.223", "loader": "forge"},
    # ── 1.14.4 ─────────────────────────────────────────────────────────────
    "1.14.4 Vanilla":  {"mc_version": "1.14.4",  "loader": "vanilla"},
    "1.14.4 Forge":    {"mc_version": "1.14.4",  "forge": "1.14.4-28.2.26", "loader": "forge"},
    # ── 1.15.2 ─────────────────────────────────────────────────────────────
    "1.15.2 Vanilla":  {"mc_version": "1.15.2",  "loader": "vanilla"},
    "1.15.2 Forge":    {"mc_version": "1.15.2",  "forge": "1.15.2-31.2.57", "loader": "forge"},
    # ── 1.16.5 ─────────────────────────────────────────────────────────────
    "1.16.5 Vanilla":  {"mc_version": "1.16.5",  "loader": "vanilla"},
    "1.16.5 Forge":    {"mc_version": "1.16.5",  "forge": "1.16.5-36.2.39",        "loader": "forge"},
    "1.16.5 Fabric":   {"mc_version": "1.16.5",  "fabric": "0.14.22",              "loader": "fabric"},
    # ── 1.17.1 ─────────────────────────────────────────────────────────────
    "1.17.1 Vanilla":  {"mc_version": "1.17.1",  "loader": "vanilla"},
    "1.17.1 Forge":    {"mc_version": "1.17.1",  "forge": "1.17.1-37.1.1", "loader": "forge"},
    "1.17.1 Fabric":   {"mc_version": "1.17.1",  "fabric": "0.14.22",              "loader": "fabric"},
    # ── 1.18.2 ─────────────────────────────────────────────────────────────
    "1.18.2 Vanilla":  {"mc_version": "1.18.2",  "loader": "vanilla"},
    "1.18.2 Forge":    {"mc_version": "1.18.2",  "forge": "1.18.2-40.2.0",         "loader": "forge"},
    "1.18.2 Fabric":   {"mc_version": "1.18.2",  "fabric": "0.14.22",              "loader": "fabric"},
    # ── 1.19.2 ─────────────────────────────────────────────────────────────
    "1.19.2 Vanilla":  {"mc_version": "1.19.2",  "loader": "vanilla"},
    "1.19.2 Forge":    {"mc_version": "1.19.2",  "forge": "1.19.2-43.3.0",         "loader": "forge"},
    "1.19.2 Fabric":   {"mc_version": "1.19.2",  "fabric": "0.14.22",              "loader": "fabric"},
    # ── 1.19.4 ─────────────────────────────────────────────────────────────
    "1.19.4 Vanilla":  {"mc_version": "1.19.4",  "loader": "vanilla"},
    "1.19.4 Forge":    {"mc_version": "1.19.4",  "forge": "1.19.4-45.2.0",         "loader": "forge"},
    "1.19.4 Fabric":   {"mc_version": "1.19.4",  "fabric": "0.15.11",              "loader": "fabric"},
    # ── 1.20.1 ─────────────────────────────────────────────────────────────
    "1.20.1 Vanilla":  {"mc_version": "1.20.1",  "loader": "vanilla"},
    "1.20.1 Forge":    {"mc_version": "1.20.1",  "forge": "1.20.1-47.2.0",         "loader": "forge"},
    "1.20.1 Fabric":   {"mc_version": "1.20.1",  "fabric": "0.15.11",               "loader": "fabric"},
    # ── 1.20.4 ─────────────────────────────────────────────────────────────
    "1.20.4 Vanilla":  {"mc_version": "1.20.4",  "loader": "vanilla"},
    "1.20.4 Forge":    {"mc_version": "1.20.4",  "forge": "1.20.4-49.0.3",         "loader": "forge"},
    "1.20.4 Fabric":   {"mc_version": "1.20.4",  "fabric": "0.15.11",              "loader": "fabric"},
    "1.20.4 NeoForge": {"mc_version": "1.20.4",  "neoforge": "", "loader": "neoforge"},
    # ── 1.20.6 ─────────────────────────────────────────────────────────────
    "1.20.6 Vanilla":  {"mc_version": "1.20.6",  "loader": "vanilla"},
    "1.20.6 Forge":    {"mc_version": "1.20.6",  "forge": "1.20.6-50.1.0",         "loader": "forge"},
    "1.20.6 Fabric":   {"mc_version": "1.20.6",  "fabric": "0.15.11",              "loader": "fabric"},
    "1.20.6 NeoForge": {"mc_version": "1.20.6",  "neoforge": "", "loader": "neoforge"},
    # ── 1.21.1 ─────────────────────────────────────────────────────────────
    "1.21.1 Vanilla":  {"mc_version": "1.21.1",  "loader": "vanilla"},
    "1.21.1 Forge":    {"mc_version": "1.21.1",  "forge": "1.21.1-52.0.38",        "loader": "forge"},
    "1.21.1 Fabric":   {"mc_version": "1.21.1",  "fabric": "0.16.14",              "loader": "fabric"},
    "1.21.1 NeoForge": {"mc_version": "1.21.1",  "neoforge": "", "loader": "neoforge"},
    # ── 1.21.3 ─────────────────────────────────────────────────────────────
    "1.21.3 Vanilla":  {"mc_version": "1.21.3",  "loader": "vanilla"},
    "1.21.3 Fabric":   {"mc_version": "1.21.3",  "fabric": "0.16.14",              "loader": "fabric"},
    "1.21.3 NeoForge": {"mc_version": "1.21.3",  "neoforge": "", "loader": "neoforge"},
    # ── 1.21.4 ─────────────────────────────────────────────────────────────
    "1.21.4 Vanilla":  {"mc_version": "1.21.4",  "loader": "vanilla"},
    "1.21.4 Fabric":   {"mc_version": "1.21.4",  "fabric": "0.16.14",              "loader": "fabric"},
    "1.21.4 NeoForge": {"mc_version": "1.21.4",  "neoforge": "", "loader": "neoforge"},
    # ── 1.21.11 ────────────────────────────────────────────────────────────
    "1.21.11 Vanilla": {"mc_version": "1.21.11", "loader": "vanilla"},
    "1.21.11 Forge":   {"mc_version": "1.21.11", "forge": "1.21.11-52.0.38",       "loader": "forge"},
    "1.21.11 Fabric":  {"mc_version": "1.21.11", "fabric": "0.17.3",               "loader": "fabric"},
    "1.21.11 NeoForge":{"mc_version": "1.21.11", "neoforge": "", "loader": "neoforge"},
}

# Fabric API JAR под каждую MC версию — скачивается автоматически при установке
# (filename, version_string)
FABRIC_API_VERSIONS = {
    "1.16.5":  ("fabric-api-0.42.0+1.16.jar",    "0.42.0+1.16"),
    "1.17.1":  ("fabric-api-0.46.1+1.17.jar",    "0.46.1+1.17"),
    "1.18.2":  ("fabric-api-0.77.0+1.18.2.jar",  "0.77.0+1.18.2"),
    "1.19.2":  ("fabric-api-0.77.0+1.19.2.jar",  "0.77.0+1.19.2"),
    "1.19.4":  ("fabric-api-0.87.2+1.19.4.jar",  "0.87.2+1.19.4"),
    "1.20.1":  ("fabric-api-0.92.3+1.20.1.jar",   "0.92.3+1.20.1"),
    "1.20.4":  ("fabric-api-0.97.0+1.20.4.jar",  "0.97.0+1.20.4"),
    "1.20.6":  ("fabric-api-0.100.8+1.20.6.jar", "0.100.8+1.20.6"),
    "1.21.1":  ("fabric-api-0.110.5+1.21.1.jar",  "0.110.5+1.21.1"),
    "1.21.3":  ("fabric-api-0.111.0+1.21.3.jar", "0.111.0+1.21.3"),
    "1.21.4":  ("fabric-api-0.119.5+1.21.4.jar",  "0.119.5+1.21.4"),
    "1.21.11": ("fabric-api-0.127.1+1.21.11.jar", "0.127.1+1.21.11"),
}

VERSION_SIZES = {
    "1.7.10 Vanilla": 180,   "1.7.10 Forge":   320,
    "1.8.9 Vanilla":  190,   "1.8.9 Forge":    350,
    "1.9.4 Vanilla":  195,   "1.9.4 Forge":    360,
    "1.10.2 Vanilla": 200,   "1.10.2 Forge":   370,
    "1.11.2 Vanilla": 205,   "1.11.2 Forge":   390,
    "1.12.2 Vanilla": 220,   "1.12.2 Forge":   480,
    "1.13.2 Vanilla": 240,   "1.13.2 Forge":   500,
    "1.14.4 Vanilla": 255,   "1.14.4 Forge":   540,
    "1.15.2 Vanilla": 265,   "1.15.2 Forge":   570,
    "1.16.5 Vanilla": 280,   "1.16.5 Forge":   620,   "1.16.5 Fabric": 480,
    "1.17.1 Vanilla": 295,   "1.17.1 Forge":   680,   "1.17.1 Fabric": 500,
    "1.18.2 Vanilla": 320,   "1.18.2 Forge":   750,   "1.18.2 Fabric": 510,
    "1.19.2 Vanilla": 340,   "1.19.2 Forge":   800,   "1.19.2 Fabric": 515,
    "1.19.4 Vanilla": 350,   "1.19.4 Forge":   820,   "1.19.4 Fabric": 520,
    "1.20.1 Vanilla": 370,   "1.20.1 Forge":   900,   "1.20.1 Fabric": 520,
    "1.20.4 Vanilla": 380,   "1.20.4 Forge":   920,   "1.20.4 Fabric": 540,
    "1.20.6 Vanilla": 382,   "1.20.6 Forge":   930,   "1.20.6 Fabric": 545,
    "1.21.1 Vanilla": 390,   "1.21.1 Forge":   960,   "1.21.1 Fabric": 560,
    "1.21.3 Vanilla": 393,                             "1.21.3 Fabric": 575,
    "1.21.4 Vanilla": 395,                             "1.21.4 Fabric": 580,
    "1.21.11 Vanilla": 400,  "1.21.11 Forge":  970,   "1.21.11 Fabric": 600,
}

# ══════════════════════════════════════════
#  ПУТИ
# ══════════════════════════════════════════
if getattr(sys, "frozen", False):
    BASE_DIR      = os.path.dirname(sys.executable)
    BASE_RESOURCE = sys._MEIPASS
else:
    BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
    BASE_RESOURCE = BASE_DIR

LAUNCHER_VERSION  = "2.1.0"

_PLATFORM_EXT = ".exe" if sys.platform.startswith("win") else ""
_PLATFORM_KEY = "windows" if sys.platform.startswith("win") else ("mac" if sys.platform == "darwin" else "linux")

CONFIG_FILE = os.path.join(BASE_DIR, "launcher_config.json")
CRASH_DIR   = os.path.join(BASE_DIR, "crash_reports")
os.makedirs(CRASH_DIR, exist_ok=True)

# ══════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════
_DEFAULT_SERVER_URL = "http://10.55.9.173:25580"


def _default_config():
    return {
        "install_path": "", "selected_version": "1.20.1 Forge",
        "nickname": "", "memory": "2",
        "show_console": False, "theme": "night",
        "auto_update": True,               # проверять обновления лаунчера на сервере lenta.co
        "custom_theme": None,
        "custom_theme_name": "CUSTOM",
        "photo_bg_path": "",
        "custom_banner_path": "",  # кастомное фото вместо атома на баннере
        "bg_overlay_alpha": 120,   # прозрачность затемнения поверх фото/gif (0=нет, 255=чёрный)
        "glass_strength": 0.3,     # прозрачность элементов UI (0.0=непрозрачно, 1.0=максимально стекло)
        # Аккаунт
        "account_type": "offline",     # "offline" | "microsoft" | "atomic" (сервер lenta.co)
        "atomic_server_url": _DEFAULT_SERVER_URL,
        "atomic_client_token": "",
        "atomic_access_token": "",
        "atomic_uuid": "",
        "atomic_username": "",
        "ms_access_token": "",
        "ms_refresh_token": "",
        "ms_uuid": "",
        "ms_username": "",
    }


# Ключи старых версий лаунчера (Google Drive, сборки, ИИ, музыка, ImgBB) — удаляются из конфига
_OBSOLETE_CONFIG_KEYS = (
    "drive_api_key", "forge_folder_drive_id", "versions", "lenta_builds", "update_mods",
    "ai_provider", "openai_key", "claude_key_inline",
    "skins_folder_id", "imgbb_key", "skin_url", "skin_download_mode", "skin_whitelist",
    "music_dir", "music_bind_pause", "music_bind_next", "music_bind_prev",
)


def _fill_defaults(data: dict) -> dict:
    for k in _OBSOLETE_CONFIG_KEYS:
        data.pop(k, None)
    for k, v in _default_config().items():
        data.setdefault(k, v)
    if data.get("selected_version") not in get_all_versions():
        data["selected_version"] = "1.20.1 Forge"
    return data

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return _fill_defaults(json.load(f))
        except Exception:
            pass
    return _fill_defaults(_default_config())

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ══════════════════════════════════════════
#  ТЕМЫ
# ══════════════════════════════════════════
THEMES = {
    "atomic": {
        "name": "ATOMIC  (default)",
        "bg": "#0C0A09", "bg_panel": "#131110", "bg_input": "#1A1715",
        "bg_header": "#100D0B", "orange": "#FF5E1A", "orange_dim": "#CC4A12",
        "orange_glow": "#2A1208", "red": "#E8222A", "red_dim": "#B81820",
        "red_glow": "#200508", "amber": "#FFA030", "amber_dim": "#CC7A1A",
        "text": "#EDE0D0", "text_muted": "#6A5C50", "text_dim": "#3D3028",
        "border": "#2A2018", "sep": "#241C14", "log_bg": "#080604",
        "green": "#6FCF4A", "accent": "#FF5E1A", "accent_dim": "#CC4A12",
        "accent_glow": "#2A1208", "header_stripe1": "#E8222A",
        "header_stripe2": "#FF5E1A", "btn_stop": "#E8222A",
        "btn_stop_glow": "#200508", "section_lbl": "#FFA030",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "phosphor": {
        "name": "PHOSPHOR GREEN",
        "bg": "#030D02", "bg_panel": "#060F05", "bg_input": "#040A03",
        "bg_header": "#020A01", "orange": "#33FF33", "orange_dim": "#1A9910",
        "orange_glow": "#021402", "red": "#FF3333", "red_dim": "#CC2222",
        "red_glow": "#1A0101", "amber": "#22CC22", "amber_dim": "#158815",
        "text": "#CCFFCC", "text_muted": "#1A6614", "text_dim": "#0D3A0A",
        "border": "#1A5C12", "sep": "#0D3A0A", "log_bg": "#010601",
        "green": "#55FF55", "accent": "#33FF33", "accent_dim": "#1A9910",
        "accent_glow": "#021402", "header_stripe1": "#1A9910",
        "header_stripe2": "#33FF33", "btn_stop": "#FF3333",
        "btn_stop_glow": "#1A0101", "section_lbl": "#22CC22",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "amber": {
        "name": "AMBER CRT",
        "bg": "#0A0800", "bg_panel": "#0F0C00", "bg_input": "#0D0A00",
        "bg_header": "#080600", "orange": "#FFAA00", "orange_dim": "#CC8800",
        "orange_glow": "#1A1100", "red": "#FF6600", "red_dim": "#CC5200",
        "red_glow": "#1A0C00", "amber": "#FF8800", "amber_dim": "#CC6600",
        "text": "#FFD080", "text_muted": "#8B6914", "text_dim": "#4A3408",
        "border": "#5C4410", "sep": "#3A2A08", "log_bg": "#060400",
        "green": "#FFCC44", "accent": "#FFAA00", "accent_dim": "#CC8800",
        "accent_glow": "#1A1100", "header_stripe1": "#FF6600",
        "header_stripe2": "#FFAA00", "btn_stop": "#FF6600",
        "btn_stop_glow": "#1A0C00", "section_lbl": "#FF8800",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "bios": {
        "name": "BIOS / DOS",
        "bg": "#000080", "bg_panel": "#0000AA", "bg_input": "#0000AA",
        "bg_header": "#000066", "orange": "#FFFF55", "orange_dim": "#CCCC33",
        "orange_glow": "#000033", "red": "#FF5555", "red_dim": "#CC3333",
        "red_glow": "#110000", "amber": "#AAAAAA", "amber_dim": "#888888",
        "text": "#FFFFFF", "text_muted": "#AAAAAA", "text_dim": "#555566",
        "border": "#AAAAAA", "sep": "#555566", "log_bg": "#000055",
        "green": "#55FF55", "accent": "#FFFF55", "accent_dim": "#CCCC33",
        "accent_glow": "#000033", "header_stripe1": "#AAAAAA",
        "header_stripe2": "#FFFF55", "btn_stop": "#FF5555",
        "btn_stop_glow": "#110000", "section_lbl": "#AAAAAA",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "galaxy": {
        "name": "GALAXY",
        "bg": "#04020F", "bg_panel": "#080518", "bg_input": "#0A0720",
        "bg_header": "#030110", "orange": "#A855F7", "orange_dim": "#7C3AED",
        "orange_glow": "#1A0A3A", "red": "#EC4899", "red_dim": "#BE185D",
        "red_glow": "#2A0520", "amber": "#38BDF8", "amber_dim": "#0EA5E9",
        "text": "#E2D9F3", "text_muted": "#6B5A8A", "text_dim": "#2E1F4A",
        "border": "#2A1A4A", "sep": "#1A0F30", "log_bg": "#020010",
        "green": "#34D399", "accent": "#A855F7", "accent_dim": "#7C3AED",
        "accent_glow": "#1A0A3A", "header_stripe1": "#EC4899",
        "header_stripe2": "#A855F7", "btn_stop": "#EC4899",
        "btn_stop_glow": "#2A0520", "section_lbl": "#38BDF8",
        "galaxy_fx": True, "reich_fx": False, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "nebula": {
        "name": "* NEBULA  [secret]",
        "bg": "#000308", "bg_panel": "#000A14", "bg_input": "#001020",
        "bg_header": "#000208", "orange": "#00FFFF", "orange_dim": "#008888",
        "orange_glow": "#001A1A", "red": "#FF00AA", "red_dim": "#AA0066",
        "red_glow": "#1A001A", "amber": "#AAFFFF", "amber_dim": "#55AAAA",
        "text": "#D0F8FF", "text_muted": "#2A6878", "text_dim": "#0A2030",
        "border": "#003850", "sep": "#001828", "log_bg": "#000205",
        "green": "#00FFB8", "accent": "#00FFFF", "accent_dim": "#008888",
        "accent_glow": "#001A1A", "header_stripe1": "#FF00AA",
        "header_stripe2": "#00FFFF", "btn_stop": "#FF00AA",
        "btn_stop_glow": "#1A001A", "section_lbl": "#AAFFFF",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": True, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "reich": {
        "name": "+ REICH 1939  [secret]",
        "bg": "#0A0800", "bg_panel": "#141000", "bg_input": "#1A1400",
        "bg_header": "#080600", "orange": "#CC9900", "orange_dim": "#886600",
        "orange_glow": "#1A1000", "red": "#CC2200", "red_dim": "#881500",
        "red_glow": "#150800", "amber": "#DDAA00", "amber_dim": "#AA8800",
        "text": "#F0E8C8", "text_muted": "#7A6840", "text_dim": "#3A3018",
        "border": "#4A3A10", "sep": "#2A2008", "log_bg": "#060400",
        "green": "#88BB44", "accent": "#CC9900", "accent_dim": "#886600",
        "accent_glow": "#1A1000", "header_stripe1": "#CC2200",
        "header_stripe2": "#CC9900", "btn_stop": "#CC2200",
        "btn_stop_glow": "#150800", "section_lbl": "#DDAA00",
        "galaxy_fx": False, "reich_fx": True, "nebula_fx": False, "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "aurora": {
        "name": "~ AURORA INFINITA  [secret]",
        "bg": "#000510", "bg_panel": "#000C1A", "bg_input": "#001428",
        "bg_header": "#000308", "orange": "#FF6EC7", "orange_dim": "#CC44AA",
        "orange_glow": "#1A0018", "red": "#FF2266", "red_dim": "#AA0044",
        "red_glow": "#1A0010", "amber": "#AAFFEE", "amber_dim": "#55CCAA",
        "text": "#E8F8FF", "text_muted": "#336688", "text_dim": "#0A1A28",
        "border": "#0A3A5A", "sep": "#041830", "log_bg": "#000208",
        "green": "#44FFCC", "accent": "#FF6EC7", "accent_dim": "#CC44AA",
        "accent_glow": "#1A0018", "header_stripe1": "#FF2266",
        "header_stripe2": "#7744FF", "btn_stop": "#FF2266",
        "btn_stop_glow": "#1A0010", "section_lbl": "#AAFFEE",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": True, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    },
    "dedinsaid": {
        "name": "# DEAD INSIDE  [secret]",
        "bg": "#080808", "bg_panel": "#0F0F0F", "bg_input": "#111111",
        "bg_header": "#050505", "orange": "#CC0000", "orange_dim": "#880000",
        "orange_glow": "#1A0000", "red": "#FF0000", "red_dim": "#CC0000",
        "red_glow": "#200000", "amber": "#888888", "amber_dim": "#555555",
        "text": "#CCCCCC", "text_muted": "#444444", "text_dim": "#222222",
        "border": "#2A0000", "sep": "#1A0000", "log_bg": "#030303",
        "green": "#AA0000", "accent": "#CC0000", "accent_dim": "#880000",
        "accent_glow": "#1A0000", "header_stripe1": "#CC0000",
        "header_stripe2": "#880000", "btn_stop": "#FF0000",
        "btn_stop_glow": "#200000", "section_lbl": "#888888",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False,
        "aurora_fx": False, "dedinsaid_fx": True,
    },
    "stal": {
        "name": "@ STAL  [secret]",
        "bg": "#0A0800", "bg_panel": "#111000", "bg_input": "#161200",
        "bg_header": "#070500", "orange": "#CC3300", "orange_dim": "#881500",
        "orange_glow": "#1A0500", "red": "#FF1100", "red_dim": "#BB0000",
        "red_glow": "#1F0000", "amber": "#DDAA00", "amber_dim": "#AA7700",
        "text": "#F5E6C8", "text_muted": "#7A6030", "text_dim": "#3A2A08",
        "border": "#5A3A00", "sep": "#2A1A00", "log_bg": "#050300",
        "green": "#88AA33", "accent": "#CC3300", "accent_dim": "#881500",
        "accent_glow": "#1A0500", "header_stripe1": "#CC0000",
        "header_stripe2": "#CC3300", "btn_stop": "#FF1100",
        "btn_stop_glow": "#1F0000", "section_lbl": "#DDAA00",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False,
        "dedinsaid_fx": False, "stal_fx": True, "ducklake_fx": False, "am_fx": False,
    },
    "ducklake": {
        "name": "~ DUCK LAKE  [secret]",
        "bg": "#061008", "bg_panel": "#0A1A0C", "bg_input": "#0D2010",
        "bg_header": "#040C06", "orange": "#FFD700", "orange_dim": "#CCAA00",
        "orange_glow": "#1A1400", "red": "#FF6600", "red_dim": "#CC4400",
        "red_glow": "#1A0800", "amber": "#88DD44", "amber_dim": "#66AA22",
        "text": "#E0FFD0", "text_muted": "#4A7A30", "text_dim": "#243A14",
        "border": "#2A5518", "sep": "#162E0A", "log_bg": "#030804",
        "green": "#44FF88", "accent": "#FFD700", "accent_dim": "#CCAA00",
        "accent_glow": "#1A1400", "header_stripe1": "#3A7A18",
        "header_stripe2": "#FFD700", "btn_stop": "#FF6600",
        "btn_stop_glow": "#1A0800", "section_lbl": "#88DD44",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False,
        "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": True,
        "am_fx": False,
    },
    "am": {
        "name": "! A.M.  [secret]",
        "bg": "#000000", "bg_panel": "#030503", "bg_input": "#050805",
        "bg_header": "#000000", "orange": "#00FF41", "orange_dim": "#008F26",
        "orange_glow": "#001A08", "red": "#FF0000", "red_dim": "#AA0000",
        "red_glow": "#1A0000", "amber": "#00CC33", "amber_dim": "#007A1A",
        "text": "#C8FFC8", "text_muted": "#1A5C1A", "text_dim": "#0A2A0A",
        "border": "#0A3A0A", "sep": "#051505", "log_bg": "#000200",
        "green": "#00FF41", "accent": "#00FF41", "accent_dim": "#008F26",
        "accent_glow": "#001A08", "header_stripe1": "#FF0000",
        "header_stripe2": "#00FF41", "btn_stop": "#FF0000",
        "btn_stop_glow": "#1A0000", "section_lbl": "#00CC33",
        "galaxy_fx": False, "reich_fx": False, "nebula_fx": False,
        "aurora_fx": False, "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False,
        "am_fx": True,
    },
}

# ── «НОЧЬ» — основная тема 2.x. Спокойная, тёмная, читаемая: тёплый свет лампы
#    на фоне ночного дома (в духе No, I'm not a Human). Читаемый шрифт, мягкие
#    кнопки, сцена с домом в шапке.
THEMES["night"] = {
    "name": "🌙 НОЧЬ  (по умолчанию)",
    "bg": "#121417", "bg_panel": "#1A1D22", "bg_input": "#23272E",
    "bg_header": "#0D0F12", "orange": "#E8C37A", "orange_dim": "#B9975A",
    "orange_glow": "#2A2620", "red": "#D07A6C", "red_dim": "#9A564B",
    "red_glow": "#2E1F1C", "amber": "#A9B7C6", "amber_dim": "#7F8C99",
    "text": "#E6E1D6", "text_muted": "#A39D90", "text_dim": "#7C776E",
    "border": "#2E333B", "sep": "#262A30", "log_bg": "#0F1114",
    "green": "#9CC78C", "accent": "#E8C37A", "accent_dim": "#B9975A",
    "accent_glow": "#2A2620", "header_stripe1": "#D07A6C",
    "header_stripe2": "#E8C37A", "btn_stop": "#D07A6C",
    "btn_stop_glow": "#2E1F1C", "section_lbl": "#A9B7C6",
    "galaxy_fx": False, "reich_fx": False, "nebula_fx": False, "aurora_fx": False,
    "dedinsaid_fx": False, "stal_fx": False, "ducklake_fx": False, "am_fx": False,
    "night_fx": True, "ui_font": True, "soft_ui": True,
}

SECRET_THEMES = {"nebula", "reich", "aurora", "dedinsaid", "stal", "ducklake", "am"}

# custom+ — только для девов: любая картинка как фон
THEMES["custom_plus"] = dict(THEMES["atomic"])
THEMES["custom_plus"]["name"] = "📷  CUSTOM+ (фото/GIF фон)"
THEMES["custom_plus"]["galaxy_fx"] = False
THEMES["custom_plus"]["reich_fx"]  = False
THEMES["custom_plus"]["nebula_fx"] = False
THEMES["custom_plus"]["aurora_fx"] = False
THEMES["custom_plus"]["dedinsaid_fx"] = False
THEMES["custom_plus"]["stal_fx"]   = False
THEMES["custom_plus"]["ducklake_fx"] = False
THEMES["custom_plus"]["am_fx"]     = False
THEMES["custom_plus"]["photo_bg"]  = True   # признак фото-фона

# Кастомная тема — заполняется из конфига
THEMES["custom"] = dict(THEMES["atomic"])
THEMES["custom"]["name"] = "✏  CUSTOM"
THEMES["custom"]["galaxy_fx"] = False
THEMES["custom"]["reich_fx"] = False
THEMES["custom"]["nebula_fx"] = False
THEMES["custom"]["aurora_fx"] = False
THEMES["custom"]["dedinsaid_fx"] = False
THEMES["custom"]["stal_fx"] = False
THEMES["custom"]["ducklake_fx"] = False
THEMES["custom"]["am_fx"] = False
C = dict(THEMES["atomic"])
C["panel"]       = C["bg_panel"]
C["panel_hover"] = C["bg_input"]
C["input_bg"]    = C["bg_input"]
_unlocked_themes: set = set()

# Сила стеклянного эффекта (0.0 = непрозрачно, 1.0 = максимальная прозрачность панелей)
_GLASS_STRENGTH: float = 0.3

def apply_theme(theme_key: str, custom_data: dict = None):
    global C
    if theme_key == "custom":
        base = dict(THEMES["atomic"])
        if custom_data:
            base.update(custom_data)
        THEMES["custom"].update(base)
        THEMES["custom"]["name"] = "✏  CUSTOM"
    t = THEMES.get(theme_key) or THEMES["night"]
    C.clear(); C.update(t)
    C["orange"]      = C["accent"]
    C["orange_dim"]  = C["accent_dim"]
    C["orange_glow"] = C["accent_glow"]
    C["amber"]       = C["section_lbl"]
    # Алиасы для совместимости (open_version_manager и др.)
    C["panel"]       = C["bg_panel"]
    C["panel_hover"] = C["bg_input"]
    C["input_bg"]    = C["bg_input"]
    _set_fonts()

# ── Шрифты ──────────────────────────────────────────────────────────────
# Старые темы — моноширинный Courier New (как раньше). Тема с "ui_font" —
# читаемый системный шрифт (Inter / Segoe UI / Noto Sans / DejaVu Sans...)
# и размеры чуть крупнее. Реальные семейства подбираются после создания окна.
_UI_FAMILY   = "DejaVu Sans"
_MONO_FAMILY = "Courier New"
_UI_FAMILY_CANDIDATES = ("Inter", "Segoe UI", "Noto Sans", "Cantarell", "Ubuntu",
                         "SF Pro Text", "Helvetica Neue", "DejaVu Sans", "Liberation Sans", "Arial")
_MONO_FAMILY_CANDIDATES = ("JetBrains Mono", "Cascadia Mono", "Consolas", "DejaVu Sans Mono",
                           "Noto Sans Mono", "Liberation Mono", "Courier New")


def _resolve_font_families(root):
    """Выбирает установленные шрифты (вызывается после создания tk.Tk)."""
    global _UI_FAMILY, _MONO_FAMILY
    try:
        from tkinter import font as _tkfont
        have = {f.lower(): f for f in _tkfont.families(root)}
        _UI_FAMILY = next((have[c.lower()] for c in _UI_FAMILY_CANDIDATES if c.lower() in have), _UI_FAMILY)
        _MONO_FAMILY = next((have[c.lower()] for c in _MONO_FAMILY_CANDIDATES if c.lower() in have), _MONO_FAMILY)
    except Exception:
        pass
    _set_fonts()


def _font(size: int, weight: str = None):
    """Шрифт с учётом темы: в «ui_font»-темах — читаемый и чуть крупнее."""
    if C.get("ui_font"):
        size = size + 2 if size <= 9 else size + 1
        fam = _UI_FAMILY
    else:
        fam = "Courier New"
    return (fam, size, weight) if weight else (fam, size)


def _mono(size: int, weight: str = None):
    fam = _MONO_FAMILY if C.get("ui_font") else "Courier New"
    return (fam, size, weight) if weight else (fam, size)


def _set_fonts():
    global FT, FT2, FL, FE, FLG, FB, FS, FSB
    FT  = _font(20, "bold")
    FT2 = _font(8, "bold")
    FL  = _font(9)
    FE  = _font(11)
    FLG = _mono(10) if C.get("ui_font") else _font(9)
    FB  = _font(12, "bold")
    FS  = _font(8)
    FSB = _font(8, "bold")


F_FRAK = ("Times New Roman", 11, "bold")
_set_fonts()


# ══════════════════════════════════════════
#  GLASSMORPHISM — вспомогательные функции
#  Для секретных тем с FX используем полупрозрачный стиль
# ══════════════════════════════════════════

def _is_fx_theme():
    """Возвращает True если активна тема с анимированным или фото-фоном."""
    return bool(C.get("nebula_fx") or C.get("reich_fx") or C.get("aurora_fx") or
                C.get("dedinsaid_fx") or C.get("stal_fx") or C.get("ducklake_fx") or
                C.get("am_fx") or C.get("photo_bg"))

def _glass_bg():
    """Прозрачный фон для контейнеров поверх FX/photo — почти совпадает с bg темы."""
    if _is_fx_theme():
        return C["bg"]
    return C["bg"]

def _glass_panel():
    """Полупрозрачная панель — прозрачность зависит от _GLASS_STRENGTH."""
    if _is_fx_theme():
        # strength=0 → обычный bg_panel (слегка светлее bg), strength=1 → = bg (полностью прозрачно)
        base_alpha = 0.10
        alpha = base_alpha * (1.0 - _GLASS_STRENGTH)
        return _blend("#FFFFFF", C["bg"], max(0.0, alpha))
    return C["bg_panel"]

def _glass_input():
    """Цвет поля ввода — слегка светлее bg при strength=0, совпадает с bg при strength=1."""
    if _is_fx_theme():
        # strength=0 → слегка светлее (alpha=0.14), strength=1 → полностью совпадает с bg (alpha=0)
        alpha = 0.14 * (1.0 - _GLASS_STRENGTH)
        return _blend("#FFFFFF", C["bg"], max(0.0, alpha))
    return C["bg_input"]

def _glass_border():
    """Полупрозрачный бордюр — акцентный цвет с низкой насыщенностью."""
    if _is_fx_theme():
        base = 0.45
        alpha = base * (0.3 + 0.7 * (1.0 - _GLASS_STRENGTH))
        return _blend(C["accent"], C["bg"], max(0.1, alpha))
    return C["border"]

def _glass_log():
    """Почти прозрачный лог-бокс."""
    if _is_fx_theme():
        alpha = 0.07 * (1.0 - _GLASS_STRENGTH * 0.8)
        return _blend("#FFFFFF", C["bg"], max(0.0, alpha))
    return C["log_bg"]

def _glass_entry_bg():
    """Фон поля ввода с заметной прозрачностью через blend с белым."""
    if _is_fx_theme():
        alpha = 0.14 * (1.0 - _GLASS_STRENGTH)
        return _blend("#FFFFFF", C["bg"], max(0.0, alpha))
    return C["bg_input"]


# ══════════════════════════════════════════
#  JAVA — поиск Java (Windows + Linux)
# ══════════════════════════════════════════
def find_java_linux():
    """Ищет java на Linux: JAVA_HOME, стандартные пути, PATH."""
    import shutil
    candidates = []
    jh = os.environ.get("JAVA_HOME", "")
    if jh:
        for sub in ["bin/java"]:
            p = os.path.join(jh, sub)
            if os.path.exists(p): candidates.append(p)
    roots = [
        "/usr/lib/jvm",
        "/usr/local/lib/jvm",
        os.path.expanduser("~/.sdkman/candidates/java"),
        "/opt/java",
        "/opt/jdk",
    ]
    for root in roots:
        if not os.path.isdir(root): continue
        try:
            for entry in os.listdir(root):
                p = os.path.join(root, entry, "bin", "java")
                if os.path.exists(p): candidates.append(p)
        except Exception:
            pass
    for exe in ["java"]:
        p = shutil.which(exe)
        if p: candidates.append(p)
    candidates = list(dict.fromkeys(candidates))
    return candidates[0] if candidates else None

def find_java_windows():
    candidates = []
    jh = os.environ.get("JAVA_HOME", "")
    if jh:
        for sub in ["bin\\javaw.exe", "bin\\java.exe"]:
            p = os.path.join(jh, sub)
            if os.path.exists(p): candidates.append(p)
    roots = [
        os.environ.get("ProgramFiles",      r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.environ.get("ProgramW6432",      r"C:\Program Files"),
        r"C:\Program Files\Eclipse Adoptium",
        r"C:\Program Files\Microsoft",
        r"C:\Program Files\Java",
    ]
    for root in roots:
        if not root or not os.path.isdir(root): continue
        for vendor_dir in os.listdir(root):
            vp = os.path.join(root, vendor_dir)
            if not os.path.isdir(vp): continue
            for sub in ["bin\\javaw.exe", "bin\\java.exe"]:
                p = os.path.join(vp, sub)
                if os.path.exists(p): candidates.append(p)
            try:
                for sub2 in os.listdir(vp):
                    for sub in ["bin\\javaw.exe", "bin\\java.exe"]:
                        p = os.path.join(vp, sub2, sub)
                        if os.path.exists(p): candidates.append(p)
            except PermissionError:
                pass
    import shutil
    for exe in ["javaw", "java"]:
        p = shutil.which(exe)
        if p: candidates.append(p)
    candidates = list(dict.fromkeys(candidates))
    javaw = [c for c in candidates if "javaw" in c.lower()]
    java  = [c for c in candidates if "javaw" not in c.lower()]
    ordered = javaw + java
    return ordered[0] if ordered else None

def patch_command_java(cmd):
    if not cmd:
        return cmd
    first = cmd[0]
    if os.path.isabs(first) and os.path.exists(first):
        return cmd
    if first.lower() in ("java", "javaw", "java.exe", "javaw.exe"):
        if sys.platform.startswith("win"):
            found = find_java_windows()
        else:
            found = find_java_linux()
        if found: return [found] + list(cmd[1:])
    return cmd

def patch_command_offline(cmd, nickname):
    """Патч команды запуска для офлайн/пиратского режима.
    Заменяет --accessToken и --userType прямо в аргументах команды,
    чтобы обойти проверку Microsoft даже если launcher_lib их перезаписал.
    """
    result = list(cmd)
    i = 0
    while i < len(result):
        if result[i] == "--accessToken" and i + 1 < len(result):
            result[i + 1] = "0"
        elif result[i] == "--userType" and i + 1 < len(result):
            result[i + 1] = "legacy"
        elif result[i] == "--uuid" and i + 1 < len(result):
            result[i + 1] = generate_uuid(nickname)
        elif result[i] == "--username" and i + 1 < len(result):
            result[i + 1] = nickname
        i += 1
    return result


# ══════════════════════════════════════════
#  MICROSOFT AUTH — Device Code Flow
#  Не требует redirect URI / localhost сервера.
#  Пользователь видит код → открывает браузер → подтверждает.
# ══════════════════════════════════════════

_MS_CLIENT_ID   = "b0196b00-1d72-443e-ae32-94da9d7abd3a"   # свой client_id (Azure, AtomicInc)
_MS_DEVICE_URL  = "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
_MS_TOKEN_URL   = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
_MS_SCOPE       = "XboxLive.signin offline_access"
_XBL_URL        = "https://user.auth.xboxlive.com/user/authenticate"
_XSTS_URL       = "https://xsts.auth.xboxlive.com/xsts/authorize"
_MC_AUTH_URL    = "https://api.minecraftservices.com/authentication/login_with_xbox"
_MC_PROFILE_URL = "https://api.minecraftservices.com/minecraft/profile"


def _ms_http_post(url: str, data: dict, headers: dict = None) -> dict:
    import urllib.request, urllib.parse, json as _j, ssl
    ctx = ssl.create_default_context()
    body = urllib.parse.urlencode(data).encode()
    h = {"Content-Type": "application/x-www-form-urlencoded"}
    if headers: h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return _j.loads(r.read())


def _ms_http_post_json(url: str, payload: dict, token: str = None) -> dict:
    import urllib.request, json as _j, ssl
    ctx = ssl.create_default_context()
    body = _j.dumps(payload).encode()
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if token: h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return _j.loads(r.read())


def _ms_http_get(url: str, token: str) -> dict:
    import urllib.request, json as _j, ssl
    ctx = ssl.create_default_context()
    h = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
        return _j.loads(r.read())


def _ms_step(label, func, *args, **kw):
    """Вызов с понятной ошибкой: имя шага + код и тело ответа сервера."""
    import urllib.error
    try:
        return func(*args, **kw)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace").strip()[:200]
        except Exception:
            body = ""
        raise RuntimeError(f"[{label}] HTTP {e.code}: {body}") from None
    except Exception as e:
        raise RuntimeError(f"[{label}] {e}") from None


def ms_device_code_flow(progress_cb=None) -> dict:
    """
    Полный Microsoft Device Code Flow → возвращает dict с ключами:
        access_token, refresh_token, uuid, username
    или бросает Exception при ошибке.
    progress_cb(str) — вызывается с сообщениями о ходе аутентификации.
    """
    import time

    def log(msg):
        if progress_cb: progress_cb(msg)

    # 1. Запрашиваем device code
    log("Запрос кода авторизации...")
    dc = _ms_step("Код устройства", _ms_http_post, _MS_DEVICE_URL, {
        "client_id": _MS_CLIENT_ID,
        "scope": _MS_SCOPE,
    })
    user_code    = dc["user_code"]
    device_code  = dc["device_code"]
    interval     = int(dc.get("interval", 5))
    expires_in   = int(dc.get("expires_in", 900))
    verify_uri   = dc.get("verification_uri", "https://microsoft.com/link")

    log(f"Код: {user_code}  →  {verify_uri}")

    # 2. Ожидаем подтверждения (polling)
    deadline = time.time() + expires_in
    ms_token = None
    while time.time() < deadline:
        time.sleep(interval)
        try:
            resp = _ms_http_post(_MS_TOKEN_URL, {
                "grant_type":  "urn:ietf:params:oauth:grant-type:device_code",
                "client_id":   _MS_CLIENT_ID,
                "device_code": device_code,
            })
            if "access_token" in resp:
                ms_token = resp
                break
            err = resp.get("error", "")
            if err == "authorization_pending":
                log("Ожидаю подтверждения в браузере...")
                continue
            elif err == "authorization_declined":
                raise Exception("Пользователь отклонил вход.")
            elif err == "expired_token":
                raise Exception("Время вышло. Попробуй снова.")
        except Exception as e:
            if "Пользователь" in str(e) or "Время" in str(e):
                raise
            log(f"  Ожидание... ({e})")

    if not ms_token:
        raise Exception("Время ожидания подтверждения истекло.")

    log("Microsoft токен получен. Вход в Xbox Live...")

    # 3. XBL
    xbl = _ms_step("Xbox Live", _ms_http_post_json, _XBL_URL, {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName":   "user.auth.xboxlive.com",
            "RpsTicket":  f"d={ms_token['access_token']}",
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT",
    })
    xbl_token = xbl["Token"]
    xbl_uhs   = xbl["DisplayClaims"]["xui"][0]["uhs"]
    log("XBL токен получен. Получаю XSTS...")

    # 4. XSTS
    xsts = _ms_step("XSTS", _ms_http_post_json, _XSTS_URL, {
        "Properties": {
            "SandboxId":  "RETAIL",
            "UserTokens": [xbl_token],
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT",
    })
    xsts_token = xsts["Token"]
    log("XSTS токен получен. Вход в Minecraft...")

    # 5. Minecraft token
    mc = _ms_step("Вход в Minecraft", _ms_http_post_json, _MC_AUTH_URL, {
        "identityToken": f"XBL3.0 x={xbl_uhs};{xsts_token}",
    })
    mc_token = mc["access_token"]
    log("Minecraft токен получен. Загружаю профиль...")

    # 6. Профиль (UUID + username)
    profile = _ms_step("Профиль Minecraft", _ms_http_get, _MC_PROFILE_URL, mc_token)
    raw_uuid = profile["id"]
    # Форматируем UUID стандартно: 8-4-4-4-12
    fmt_uuid = f"{raw_uuid[0:8]}-{raw_uuid[8:12]}-{raw_uuid[12:16]}-{raw_uuid[16:20]}-{raw_uuid[20:]}"
    username = profile["name"]
    log(f"Привет, {username}! UUID: {fmt_uuid}")

    return {
        "access_token":   mc_token,
        "refresh_token":  ms_token.get("refresh_token", ""),
        "uuid":           fmt_uuid,
        "username":       username,
    }


def ms_refresh_session(config, progress_cb=None) -> bool:
    """Обновляет Minecraft-токен по сохранённому refresh_token (без браузера).
    Токен Minecraft живёт ~сутки: без обновления онлайн-серверы отвечают
    «Invalid session». Возвращает True и пишет новые данные в config."""
    def log(msg):
        if progress_cb: progress_cb(msg)

    refresh_token = config.get("ms_refresh_token")
    if not refresh_token:
        return False
    log("Обновляю токен Microsoft...")
    ms = _ms_step("Обновление токена", _ms_http_post, _MS_TOKEN_URL, {
        "grant_type":    "refresh_token",
        "client_id":     _MS_CLIENT_ID,
        "refresh_token": refresh_token,
        "scope":         _MS_SCOPE,
    })
    xbl = _ms_step("Xbox Live", _ms_http_post_json, _XBL_URL, {
        "Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com",
                       "RpsTicket": f"d={ms['access_token']}"},
        "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT",
    })
    xsts = _ms_step("XSTS", _ms_http_post_json, _XSTS_URL, {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbl["Token"]]},
        "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT",
    })
    uhs = xbl["DisplayClaims"]["xui"][0]["uhs"]
    mc = _ms_step("Вход в Minecraft", _ms_http_post_json, _MC_AUTH_URL, {
        "identityToken": f"XBL3.0 x={uhs};{xsts['Token']}",
    })
    profile = _ms_step("Профиль Minecraft", _ms_http_get, _MC_PROFILE_URL, mc["access_token"])
    raw = profile["id"]
    config["ms_access_token"]  = mc["access_token"]
    config["ms_refresh_token"] = ms.get("refresh_token", refresh_token)
    config["ms_uuid"]          = f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
    config["ms_username"]      = profile["name"]
    return True


def ms_fetch_skin(uuid: str, dest_path: str, log_cb=None) -> bool:
    """
    Скачивает скин с официального Mojang Session API по UUID.
    Возвращает True при успехе.
    """
    import urllib.request, ssl, json as _j, base64
    try:
        ctx = ssl.create_default_context()
        clean_uuid = uuid.replace("-", "")
        profile_url = f"https://sessionserver.mojang.com/session/minecraft/profile/{clean_uuid}"
        req = urllib.request.Request(profile_url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            data = _j.loads(r.read())
        # Декодируем textures property
        for prop in data.get("properties", []):
            if prop.get("name") == "textures":
                tex = _j.loads(base64.b64decode(prop["value"]))
                skin_url = tex.get("textures", {}).get("SKIN", {}).get("url", "")
                if not skin_url:
                    break
                req2 = urllib.request.Request(skin_url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req2, context=ctx, timeout=15) as r2:
                    skin_data = r2.read()
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "wb") as f:
                    f.write(skin_data)
                if log_cb: log_cb(f"  [Скин] Скачан официальный скин: {dest_path}", "ok")
                return True
    except Exception as e:
        if log_cb: log_cb(f"  [Скин] Не удалось скачать скин с Mojang: {e}", "warn")
    return False


def ms_login_dialog(master, config, on_success=None):
    """
    Открывает диалог Microsoft Device Code Flow.
    Показывает код, ссылку и ждёт подтверждения.
    После успеха — сохраняет токен в конфиг и вызывает on_success().
    """
    import webbrowser

    dlg = tk.Toplevel(master)
    dlg.title("Вход через Microsoft")
    dlg.geometry("480x340"); dlg.resizable(False, False)
    dlg.configure(bg=C["bg"]); dlg.grab_set()
    dlg.transient(master)

    tk.Frame(dlg, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(dlg, text="  🔑  ВХОД ЧЕРЕЗ MICROSOFT / MOJANG",
             bg=C["bg"], fg=C["orange"], font=_font(10, "bold"), pady=6).pack(anchor="w")
    tk.Frame(dlg, height=1, bg=C["border"]).pack(fill="x")

    status_lbl = tk.Label(dlg, text="Подключение...", bg=C["bg"], fg=C["text_muted"],
                          font=_font(9), wraplength=440, justify="left")
    status_lbl.pack(padx=20, pady=(14, 4), anchor="w")

    code_frame = tk.Frame(dlg, bg=C["bg_panel"],
                          highlightthickness=1, highlightbackground=C["border"])
    code_frame.pack(fill="x", padx=20, pady=8)

    code_lbl = tk.Label(code_frame, text="", bg=C["bg_panel"], fg=C["orange"],
                        font=_font(22, "bold"), pady=8)
    code_lbl.pack()

    link_lbl = tk.Label(code_frame, text="", bg=C["bg_panel"], fg=C["amber"],
                        font=_font(9), cursor="hand2")
    link_lbl.pack(pady=(0, 8))

    _link_url = [""]

    def _open_link(e=None):
        if _link_url[0]:
            import webbrowser
            webbrowser.open(_link_url[0])

    link_lbl.bind("<Button-1>", _open_link)

    btn_row = tk.Frame(dlg, bg=C["bg"]); btn_row.pack(pady=(6, 12))
    open_btn = tk.Button(btn_row, text="  🌐  Открыть браузер  ",
                         command=_open_link,
                         bg=C["orange_glow"], fg=C["orange"],
                         font=_font(9, "bold"), relief="flat",
                         highlightthickness=1, highlightbackground=C["orange"],
                         cursor="hand2", padx=8, pady=4)
    open_btn.pack(side="left", padx=(0, 8))

    cancel_flag = [False]

    def _cancel():
        cancel_flag[0] = True
        dlg.destroy()

    tk.Button(btn_row, text="  Отмена  ", command=_cancel,
              bg=_glass_panel(), fg=C["text_muted"],
              font=_font(9), relief="flat",
              highlightthickness=1, highlightbackground=_glass_border(),
              cursor="hand2", padx=8, pady=4).pack(side="left")

    result_box = [None]

    def _do_auth():
        def _progress(msg):
            if cancel_flag[0]: return
            # Если это строка с кодом — показываем крупно
            if msg.startswith("Код:"):
                parts = msg.split("→")
                code_part = parts[0].replace("Код:", "").strip()
                link_part = parts[1].strip() if len(parts) > 1 else "https://microsoft.com/link"
                _link_url[0] = link_part
                dlg.after(0, lambda c=code_part: code_lbl.config(text=c))
                dlg.after(0, lambda lp=link_part: link_lbl.config(text=f"↗ {lp}"))
                dlg.after(0, lambda: _open_link())  # авто-открыть браузер
                dlg.after(0, lambda: status_lbl.config(
                    text=f"1. Введи код на сайте Microsoft\n2. Войди в аккаунт Mojang/Microsoft\n3. Жди подтверждения здесь"))
            else:
                dlg.after(0, lambda m=msg: status_lbl.config(text=m))

        try:
            result = ms_device_code_flow(progress_cb=_progress)
            result_box[0] = result
            if not cancel_flag[0]:
                dlg.after(0, lambda: _on_success(result))
        except Exception as e:
            if not cancel_flag[0]:
                dlg.after(0, lambda err=str(e): status_lbl.config(
                    text=f"✗ Ошибка: {err}", fg=C["red"]))

    def _on_success(result):
        config["account_type"]    = "microsoft"
        config["ms_access_token"] = result["access_token"]
        config["ms_refresh_token"]= result.get("refresh_token", "")
        config["ms_uuid"]         = result["uuid"]
        config["ms_username"]     = result["username"]
        config["nickname"]        = result["username"]
        save_config(config)
        status_lbl.config(text=f"✓ Вошёл как {result['username']}!", fg=C["green"])
        code_lbl.config(text="✓", fg=C["green"])
        link_lbl.config(text="")
        # Скачиваем официальный скин в фоне
        def _skin_bg():
            dest = _local_skin_path(config, result["username"])
            ms_fetch_skin(result["uuid"], dest)
        threading.Thread(target=_skin_bg, daemon=True).start()
        dlg.after(1500, dlg.destroy)
        if on_success: dlg.after(1600, on_success)

    threading.Thread(target=_do_auth, daemon=True).start()


# ══════════════════════════════════════════
#  UTILS
# ══════════════════════════════════════════
# ── Отмена загрузки ─────────────────────────────────────────────────────
# Кнопка «Отмена» ставит флаг. Колбэки minecraft_launcher_lib вызываются прямо
# перед скачиванием каждого файла (в т.ч. в его потоках) — там бросаем
# DownloadCancelled, и оставшиеся загрузки обрываются за секунду. Это
# BaseException, чтобы его не «проглотили» блоки except Exception.
_CANCEL_EVENT = threading.Event()


class DownloadCancelled(BaseException):
    pass


def _raise_if_cancelled(*_):
    if _CANCEL_EVENT.is_set():
        raise DownloadCancelled()


def _run_cancellable(cmd, timeout=600, **kw):
    """Как subprocess.run(capture_output=True, text=True), но убивает процесс по «Отмене»."""
    kw.setdefault("stdout", subprocess.PIPE)
    kw.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, text=True, encoding="utf-8", errors="replace", **kw)
    deadline = time.time() + timeout
    while True:
        try:
            out, err = proc.communicate(timeout=0.5)
            return subprocess.CompletedProcess(cmd, proc.returncode, out, err)
        except subprocess.TimeoutExpired:
            if _CANCEL_EVENT.is_set() or time.time() > deadline:
                proc.kill()
                proc.communicate()
                if _CANCEL_EVENT.is_set():
                    raise DownloadCancelled()
                raise subprocess.TimeoutExpired(cmd, timeout)


def get_available_ram_gb():
    return psutil.virtual_memory().total // (1024 ** 3)

def _ensure_launcher_profiles(mc_dir: str):
    os.makedirs(mc_dir, exist_ok=True)
    profiles_path = os.path.join(mc_dir, "launcher_profiles.json")
    if not os.path.exists(profiles_path):
        import time
        profile = {
            "profiles": {
                "forge": {
                    "name": "forge",
                    "type": "custom",
                    "created": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                    "lastUsed": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
                    "lastVersionId": "forge",
                }
            },
            "selectedProfile": "forge",
            "clientToken": "00000000-0000-0000-0000-000000000000",
            "authenticationDatabase": {},
            "settings": {"enableSnapshots": False, "profileSorting": "ByLastPlayed"},
            "launcherVersion": {"format": 21, "name": "2.2.1376"}
        }
        with open(profiles_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4)

def _get_proxy_jvm_args() -> list:
    import urllib.request
    args = []
    for env_var in ["https_proxy", "HTTPS_PROXY", "http_proxy", "HTTP_PROXY"]:
        proxy_url = os.environ.get(env_var, "")
        if proxy_url:
            try:
                from urllib.parse import urlparse
                p = urlparse(proxy_url)
                host = p.hostname or ""
                port = p.port or 8080
                if host:
                    args += [
                        f"-Dhttps.proxyHost={host}",
                        f"-Dhttps.proxyPort={port}",
                        f"-Dhttp.proxyHost={host}",
                        f"-Dhttp.proxyPort={port}",
                    ]
                    if p.username:
                        args += [
                            f"-Dhttps.proxyUser={p.username}",
                            f"-Dhttps.proxyPassword={p.password or ''}",
                        ]
                    return args
            except Exception:
                pass
    try:
        proxies = urllib.request.getproxies()
        for key in ("https", "http"):
            if key in proxies:
                from urllib.parse import urlparse
                p = urlparse(proxies[key])
                host = p.hostname or ""
                port = p.port or 8080
                if host:
                    args += [
                        f"-Dhttps.proxyHost={host}",
                        f"-Dhttps.proxyPort={port}",
                        f"-Dhttp.proxyHost={host}",
                        f"-Dhttp.proxyPort={port}",
                    ]
                    return args
    except Exception:
        pass
    return args

def get_mc_dir(base_path, version):
    safe = re.sub(r'[<>:"/\\|?*\[\]]', "_", version.replace(".", "_")).strip(" .") or "custom"
    return os.path.join(base_path, f"mc_{safe}", ".minecraft")


_LOADER_TITLES = {"forge": "Forge", "fabric": "Fabric", "neoforge": "NeoForge", "vanilla": "Vanilla"}


def get_game_dir(base_path, version):
    """Папка с модами/ресурспаками/сохранениями выбранной версии.
    Для импортированных из других лаунчеров — их собственная папка."""
    info = get_all_versions().get(version, {})
    return info.get("game_dir") or info.get("external_dir") or get_mc_dir(base_path, version)

def find_forge_profile(mc_dir, forge_ver=None):
    """Ищет установленный Forge профиль. Если forge_ver задан — ищет точное совпадение,
    иначе возвращает первый попавшийся forge-профиль (legacy поведение)."""
    vp = os.path.join(mc_dir, "versions")
    if not os.path.exists(vp):
        return None
    # Сначала ищем точное совпадение по forge_ver
    if forge_ver:
        for folder in os.listdir(vp):
            jf = os.path.join(vp, folder, folder + ".json")
            if os.path.exists(jf) and "forge" in folder.lower() and forge_ver in folder:
                return folder
        # Если точного нет — ищем по mc_version (первая часть forge_ver до '-')
        mc_ver = forge_ver.split("-")[0] if "-" in forge_ver else forge_ver
        for folder in os.listdir(vp):
            jf = os.path.join(vp, folder, folder + ".json")
            if os.path.exists(jf) and "forge" in folder.lower() and folder.startswith(mc_ver):
                return folder
        return None
    # Без фильтра — старое поведение (не использовать без forge_ver!)
    for folder in os.listdir(vp):
        jf = os.path.join(vp, folder, folder + ".json")
        if os.path.exists(jf) and "forge" in folder.lower():
            return folder
    return None

def _fabric_ensure_api(mc_dir: str, mc_version: str, log_cb=None) -> bool:
    """Скачивает правильный Fabric API в папку mods если его там ещё нет."""
    import urllib.request, ssl, json as _js, urllib.parse as _up
    api_info = FABRIC_API_VERSIONS.get(mc_version)
    if not api_info:
        if log_cb: log_cb(f"  [Fabric API] нет записи для MC {mc_version}, пропускаю", "muted")
        return True
    fname, version_str = api_info
    mods_dir = os.path.join(mc_dir, "mods")
    os.makedirs(mods_dir, exist_ok=True)
    dest = os.path.join(mods_dir, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        if log_cb: log_cb(f"  [Fabric API] уже есть: {fname}", "muted")
        return True
    # Удаляем старые fabric-api джары для этой MC версии
    mc_ver_tag = "+" + mc_version
    for old_f in os.listdir(mods_dir):
        if old_f.startswith("fabric-api-") and mc_ver_tag in old_f and old_f != fname:
            try:
                os.remove(os.path.join(mods_dir, old_f))
                if log_cb: log_cb(f"  [Fabric API] удалён старый: {old_f}", "muted")
            except Exception:
                pass
    ctx = ssl.create_default_context()
    if log_cb: log_cb(f"  [Fabric API] скачиваю {fname}...", "info")
    # Ищем версию через Modrinth API (надёжнее хардкоженного CDN URL)
    try:
        params = _up.quote(_js.dumps([mc_version]))
        api_url = (f"https://api.modrinth.com/v2/project/fabric-api/version"
                   f"?game_versions={params}&loaders={_up.quote(_js.dumps(['fabric']))}")
        req = urllib.request.Request(api_url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
            versions = _js.loads(r.read())
        if not versions:
            if log_cb: log_cb(f"  [Fabric API] не найден для MC {mc_version}", "warn")
            return False
        # Берём самую свежую версию
        file_info = versions[0]["files"][0]
        dl_url  = file_info["url"]
        dl_name = file_info["filename"]
        dest = os.path.join(mods_dir, dl_name)
        if os.path.exists(dest) and os.path.getsize(dest) > 10000:
            if log_cb: log_cb(f"  [Fabric API] уже есть: {dl_name}", "muted")
            return True
        req2 = urllib.request.Request(dl_url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
        with urllib.request.urlopen(req2, context=ctx, timeout=120) as r:
            data = r.read()
        with open(dest, "wb") as f:
            f.write(data)
        if log_cb: log_cb(f"  [Fabric API] готов ({len(data)//1024} KB) → {dl_name}", "ok")
        return True
    except Exception as e:
        if log_cb: log_cb(f"  [Fabric API] ошибка: {e}", "warn")
        return False


def _fabric_download_loader_jar(mc_dir: str, mc_version: str, fabric_version: str, log_cb=None) -> bool:
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    profile_name = f"fabric-loader-{fabric_version}-{mc_version}"
    jar_path = os.path.join(mc_dir, "versions", profile_name, profile_name + ".jar")
    if os.path.exists(jar_path) and os.path.getsize(jar_path) > 10000:
        return True
    os.makedirs(os.path.dirname(jar_path), exist_ok=True)
    url = (f"https://maven.fabricmc.net/net/fabricmc/fabric-loader/"
           f"{fabric_version}/fabric-loader-{fabric_version}.jar")
    if log_cb: log_cb(f"  [Fabric] Скачиваю loader jar {fabric_version}...", "info")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
            data = r.read()
        with open(jar_path, "wb") as f:
            f.write(data)
        if log_cb: log_cb(f"  [Fabric] loader jar скачан ({len(data)//1024} KB)", "ok")
        return True
    except Exception as e:
        if log_cb: log_cb(f"  [Fabric] Ошибка загрузки loader jar: {e}", "warn")
        return False


def find_fabric_profile(mc_dir, mc_version: str = None, fabric_ver: str = None):
    """Ищет установленный Fabric профиль в папке versions.
    Если fabric_ver указан — предпочитает профиль с этой версией лоадера."""
    vp = os.path.join(mc_dir, "versions")
    if not os.path.exists(vp):
        return None
    candidates = []
    for folder in os.listdir(vp):
        if "fabric" not in folder.lower():
            continue
        if not os.path.exists(os.path.join(vp, folder, folder + ".json")):
            continue
        if mc_version and mc_version not in folder:
            continue
        candidates.append(folder)
    if not candidates:
        return None
    # Если нужна конкретная версия лоадера — ищем точное совпадение
    if fabric_ver:
        for c in candidates:
            if fabric_ver in c:
                return c
    # Иначе берём с самой новой версией лоадера
    def _loader_ver(name):
        try:
            parts = name.split("-")
            li = parts.index("loader")
            return tuple(int(x) for x in parts[li + 1].split("."))
        except Exception:
            return (0,)
    candidates.sort(key=_loader_ver, reverse=True)
    return candidates[0]


def _neoforge_series_prefix(mc_version: str):
    """Преобразует Minecraft 1.21.1 в серию NeoForge 21.1."""
    parts = str(mc_version).strip().split(".")
    if len(parts) >= 3 and parts[0] == "1":
        return f"{parts[1]}.{parts[2]}"
    if len(parts) == 2 and parts[0] == "1":
        return f"{parts[1]}.0"
    return None


def _neoforge_resolve_version(mc_version: str, requested: str = "", log_cb=None) -> str:
    """Возвращает выбранную стабильную NeoForge-версию для указанного Minecraft."""
    import urllib.request
    import xml.etree.ElementTree as _ET

    series = _neoforge_series_prefix(mc_version)
    if not series:
        raise RuntimeError(f"Не удалось определить серию NeoForge для Minecraft {mc_version}")

    metadata_url = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
    req = urllib.request.Request(
        metadata_url,
        headers={"User-Agent": "AtomicIndustryLauncher/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            metadata = _ET.fromstring(response.read())
    except Exception as exc:
        raise RuntimeError(f"Не удалось получить список версий NeoForge: {exc}") from exc

    versions = []
    for node in metadata.findall(".//version"):
        version = (node.text or "").strip()
        if version.startswith(series + ".") and re.fullmatch(r"\d+(?:\.\d+)+", version):
            versions.append(version)
    if not versions:
        raise RuntimeError(f"NeoForge не найден для Minecraft {mc_version}")

    requested = str(requested or "").strip()
    if requested.lower().startswith("neoforge-"):
        requested = requested[len("neoforge-"):]
    if requested in versions:
        if log_cb:
            log_cb(f"  [NeoForge] выбрана версия {requested}", "info")
        return requested
    if requested and log_cb:
        log_cb(
            f"  [NeoForge] версия {requested} не найдена для MC {mc_version}; беру последнюю стабильную",
            "warn",
        )

    latest = max(versions, key=lambda value: tuple(int(part) for part in value.split(".")))
    if log_cb:
        log_cb(f"  [NeoForge] последняя стабильная версия для MC {mc_version}: {latest}", "info")
    return latest


def find_neoforge_profile(mc_dir, mc_version: str = None, neoforge_ver: str = None):
    """Находит NeoForge-профиль по parent Minecraft и библиотекам из его JSON."""
    versions_dir = os.path.join(mc_dir, "versions")
    if not os.path.isdir(versions_dir):
        return None

    candidates = []
    for folder in os.listdir(versions_dir):
        json_path = os.path.join(versions_dir, folder, folder + ".json")
        if not os.path.isfile(json_path):
            continue
        try:
            with open(json_path, "r", encoding="utf-8") as source:
                profile = json.load(source)
        except Exception:
            continue

        profile_id = str(profile.get("id", folder))
        parent = str(profile.get("inheritsFrom", ""))
        libraries = profile.get("libraries", [])
        library_names = [
            str(item.get("name", ""))
            for item in libraries
            if isinstance(item, dict)
        ]
        identity = " ".join([folder, profile_id, *library_names]).lower()
        if "neoforge" not in identity and "net.neoforged:" not in identity:
            continue

        if mc_version:
            if parent:
                if parent != mc_version:
                    continue
            elif mc_version not in folder and mc_version not in profile_id:
                continue

        if neoforge_ver and neoforge_ver.lower() not in identity:
            continue
        candidates.append((os.path.getmtime(json_path), folder))

    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])[1]


def _neoforge_client_extra_jar(mc_dir: str, profile_id: str, mc_version: str):
    """Находит вспомогательный NeoForge client-extra JAR по neoFormVersion профиля."""
    import glob

    profile_path = os.path.join(mc_dir, "versions", profile_id, profile_id + ".json")
    neoform_version = None
    try:
        with open(profile_path, "r", encoding="utf-8") as source:
            profile = json.load(source)
        game_args = profile.get("arguments", {}).get("game", [])
        flattened = []
        for item in game_args:
            if isinstance(item, str):
                flattened.append(item)
            elif isinstance(item, dict):
                value = item.get("value")
                if isinstance(value, str):
                    flattened.append(value)
                elif isinstance(value, list):
                    flattened.extend(str(part) for part in value)
        for index, argument in enumerate(flattened[:-1]):
            if argument == "--fml.neoFormVersion":
                neoform_version = flattened[index + 1]
                break
    except Exception:
        pass

    candidates = []
    if neoform_version:
        version_folder = f"{mc_version}-{neoform_version}"
        candidates.append(
            os.path.join(
                mc_dir,
                "libraries",
                "net",
                "minecraft",
                "client",
                version_folder,
                f"client-{version_folder}-extra.jar",
            )
        )

    # Older/custom profiles may omit neoFormVersion; prefer any matching client-extra
    # artifact for this MC version rather than silently losing CSL's version detection.
    pattern = os.path.join(
        mc_dir,
        "libraries",
        "net",
        "minecraft",
        "client",
        f"{mc_version}-*",
        f"client-{mc_version}-*-extra.jar",
    )
    candidates.extend(
        sorted(
            glob.glob(pattern),
            key=lambda path: os.path.getmtime(path),
            reverse=True,
        )
    )

    seen = set()
    for candidate in candidates:
        normalized = os.path.normcase(os.path.abspath(candidate))
        if normalized in seen:
            continue
        seen.add(normalized)
        if os.path.isfile(candidate) and os.path.getsize(candidate) > 0:
            return candidate
    return None


def _neoforge_add_client_extra_to_command(cmd, mc_dir: str, profile_id: str, mc_version: str, log_cb=None):
    """Добавляет client-extra.jar в Java classpath, сохраняя модульный путь NeoForge."""
    extra_jar = _neoforge_client_extra_jar(mc_dir, profile_id, mc_version)
    if not extra_jar:
        if log_cb:
            log_cb(
                f"  [NeoForge] client-extra.jar не найден для MC {mc_version}; "
                "CustomSkinLoader может не определить версию игры",
                "warn",
            )
        return cmd

    normalized_extra = os.path.normcase(os.path.abspath(extra_jar))
    for index, argument in enumerate(cmd):
        if argument in ("-cp", "-classpath", "--class-path") and index + 1 < len(cmd):
            classpath_entries = cmd[index + 1].split(os.pathsep) if cmd[index + 1] else []
            if not any(
                os.path.normcase(os.path.abspath(entry)) == normalized_extra
                for entry in classpath_entries
                if entry
            ):
                classpath_entries.append(extra_jar)
                cmd[index + 1] = os.pathsep.join(classpath_entries)
                if log_cb:
                    log_cb(f"  [NeoForge] client-extra.jar добавлен в classpath", "ok")
            else:
                if log_cb:
                    log_cb("  [NeoForge] client-extra.jar уже в classpath", "muted")
            return cmd

    # NeoForge uses a module path for bootstrap jars. Add the resource-only extra
    # archive as a separate classpath before the main class; it contains no classes.
    profile_path = os.path.join(mc_dir, "versions", profile_id, profile_id + ".json")
    main_class = None
    try:
        with open(profile_path, "r", encoding="utf-8") as source:
            main_class = json.load(source).get("mainClass")
    except Exception:
        pass
    if main_class and main_class in cmd:
        cmd[cmd.index(main_class):cmd.index(main_class)] = ["-cp", extra_jar]
        if log_cb:
            log_cb("  [NeoForge] client-extra.jar добавлен в classpath", "ok")
    elif log_cb:
        log_cb("  [NeoForge] не удалось определить позицию classpath в Java-команде", "warn")
    return cmd


def install_neoforge(mc_dir: str, mc_version: str, neoforge_ver: str, log_cb=None) -> bool:
    """Скачивает официальный NeoForge installer и ставит client-профиль в mc_dir."""
    import ssl
    import urllib.request

    installer_name = f"neoforge-{neoforge_ver}-installer.jar"
    installer_path = os.path.join(mc_dir, installer_name)
    installer_url = (
        "https://maven.neoforged.net/releases/net/neoforged/neoforge/"
        f"{neoforge_ver}/{installer_name}"
    )
    os.makedirs(mc_dir, exist_ok=True)
    _ensure_launcher_profiles(mc_dir)

    try:
        if log_cb:
            log_cb(f"  [NeoForge] скачиваю installer {neoforge_ver}...", "info")
        request = urllib.request.Request(
            installer_url,
            headers={"User-Agent": "AtomicIndustryLauncher/1.0"},
        )
        with urllib.request.urlopen(request, context=ssl.create_default_context(), timeout=90) as response:
            installer_data = response.read()
        if len(installer_data) < 100_000:
            raise RuntimeError("скачанный installer слишком мал или повреждён")
        with open(installer_path, "wb") as installer_file:
            installer_file.write(installer_data)

        if log_cb:
            log_cb("  [NeoForge] запускаю официальный client installer...", "info")
        java_exe = patch_command_java(["java"])[0]
        proxy_args = _get_proxy_jvm_args()
        commands = [
            [java_exe] + proxy_args + ["-jar", installer_path, "--install-client", mc_dir],
            [java_exe] + proxy_args + ["-jar", installer_path, "--installClient", mc_dir],
        ]
        run_options = {}
        if sys.platform.startswith("win"):
            run_options["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        for command in commands:
            try:
                result = _run_cancellable(command, timeout=600, cwd=mc_dir, **run_options)
            except Exception as exc:
                if log_cb:
                    log_cb(f"  [NeoForge] ошибка запуска installer: {exc}", "warn")
                continue

            profile = find_neoforge_profile(mc_dir, mc_version, neoforge_ver)
            if result.returncode == 0 and profile:
                if log_cb:
                    log_cb(f"  [NeoForge] установлен профиль {profile}", "ok")
                return True
            if profile:
                if log_cb:
                    log_cb(f"  [NeoForge] профиль установлен: {profile}", "ok")
                return True

            diagnostic = result.stderr or result.stdout or ""
            if log_cb and diagnostic:
                for line in diagnostic.strip().splitlines()[-5:]:
                    if line.strip():
                        log_cb(f"    {line.strip()}", "warn")

        if log_cb:
            log_cb("  [NeoForge] installer завершился, но профиль не найден", "warn")
        return False
    except Exception as exc:
        if log_cb:
            log_cb(f"  [NeoForge] ошибка установки: {exc}", "warn")
        return False
    finally:
        try:
            os.remove(installer_path)
        except OSError:
            pass


def _fabric_resolve_loader_version(mc_version: str, requested: str, log_cb=None) -> str:
    """
    Проверяет совместимость запрошенной версии Fabric Loader с последней Fabric API
    для данной MC версии. Если API требует более новый лоадер — возвращает нужную версию.
    Иначе возвращает requested без изменений.
    """
    import urllib.request, ssl, json as _js, urllib.parse as _up
    try:
        ctx = ssl.create_default_context()
        # Запрашиваем список лоадеров для данной MC версии с Fabric meta API
        url = f"https://meta.fabricmc.net/v2/versions/loader/{mc_version}"
        req = urllib.request.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            entries = _js.loads(r.read())
        if not entries:
            return requested
        # Берём самую свежую стабильную версию лоадера
        latest = entries[0]["loader"]["version"]
        # Сравниваем версии как кортежи чисел
        def _ver(s):
            try: return tuple(int(x) for x in s.split("."))
            except: return (0,)
        if _ver(latest) > _ver(requested):
            if log_cb:
                log_cb(f"  [Fabric] Обновляю Loader {requested} → {latest} (требуется Fabric API)", "info")
            return latest
        return requested
    except Exception:
        return requested


def install_fabric(mc_dir: str, mc_version: str, fabric_version: str, log_cb=None) -> bool:
    """
    Устанавливает Fabric Loader через официальный installer API.
    Скачивает fabric-installer.jar и запускает его.
    Возвращает True при успехе.
    """
    import urllib.request, ssl, tempfile
    ctx = ssl.create_default_context()

    if log_cb: log_cb("  [Fabric] Скачиваю Fabric installer...", "info")

    # Скачиваем последний fabric-installer
    installer_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar"
    tmp_jar = os.path.join(BASE_DIR, "fabric-installer.jar")
    try:
        req = urllib.request.Request(installer_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            with open(tmp_jar, "wb") as f:
                f.write(r.read())
    except Exception as e:
        if log_cb: log_cb(f"  [Fabric] Ошибка загрузки installer: {e}", "warn")
        return False

    if log_cb: log_cb("  [Fabric] Запускаю installer...", "info")

    # Убеждаемся что launcher_profiles.json существует
    profiles_path = os.path.join(mc_dir, "launcher_profiles.json")
    if not os.path.exists(profiles_path):
        os.makedirs(mc_dir, exist_ok=True)
        with open(profiles_path, "w") as f:
            f.write('{"profiles":{},"selectedProfile":null}')

    java_exe = patch_command_java(["java"])[0]
    cmd = [java_exe, "-jar", tmp_jar, "client",
           "-dir", mc_dir,
           "-mcversion", mc_version,
           "-loader", fabric_version,
           "-noprofile"]
    kw = {}
    if sys.platform.startswith("win"):
        kw["creationflags"] = subprocess.CREATE_NO_WINDOW
    try:
        proc = _run_cancellable(cmd, timeout=180, **kw)
        if proc.returncode == 0:
            if log_cb: log_cb("  [Fabric] Установлен успешно.", "ok")
            return True
        else:
            if log_cb: log_cb(f"  [Fabric] Installer завершился с кодом {proc.returncode}", "warn")
            if proc.stderr and log_cb:
                for line in proc.stderr.strip().split("\n")[-3:]:
                    if line.strip(): log_cb(f"    {line.strip()}", "warn")
            return False
    except Exception as e:
        if log_cb: log_cb(f"  [Fabric] Ошибка: {e}", "warn")
        return False
    finally:
        try: os.remove(tmp_jar)
        except: pass

def generate_uuid(nickname):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, nickname)).replace("-", "")

def write_crash_report(error_text: str) -> str:
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(CRASH_DIR, f"crash_{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("ATOMIC INDUSTRY LMPD — Crash Report\n" + "="*50 + f"\nTime: {ts}\n\n" + error_text)
    return path

def open_file(path: str):
    if sys.platform.startswith("win"):   os.startfile(path)
    elif sys.platform == "darwin":       subprocess.Popen(["open", path])
    else:                                subprocess.Popen(["xdg-open", path])

# ══════════════════════════════════════════
#  TTK СТИЛИ
# ══════════════════════════════════════════
def apply_styles():
    s = ttk.Style()
    s.theme_use("clam")
    bg_inp = _glass_entry_bg() if _is_fx_theme() else C["bg_input"]
    border = _glass_border()   if _is_fx_theme() else C["border"]
    soft = bool(C.get("soft_ui"))
    s.configure("AI.TCombobox",
        fieldbackground=bg_inp, background=bg_inp,
        foreground=C["text"], arrowcolor=C["orange"],
        bordercolor=border, lightcolor=border,
        darkcolor=border, padding=(8, 6) if soft else 4, arrowsize=16 if soft else 12)
    s.configure("AI.Horizontal.TScale", background=C["accent"], troughcolor=C["bg_input"],
                bordercolor=border, lightcolor=C["accent"], darkcolor=C["accent_dim"],
                sliderthickness=18 if soft else 14, gripcount=0 if soft else 5)
    root = tk._default_root
    if root is not None:
        root.option_add("*TCombobox*Listbox.background", C["bg_input"])
        root.option_add("*TCombobox*Listbox.foreground", C["text"])
        root.option_add("*TCombobox*Listbox.selectBackground", C["accent_dim"])
        root.option_add("*TCombobox*Listbox.selectForeground", C["bg"])
        root.option_add("*TCombobox*Listbox.font", _font(10))
    s.map("AI.TCombobox",
        fieldbackground=[("readonly", bg_inp)],
        foreground=[("readonly", C["text"])],
        selectbackground=[("readonly", bg_inp)],
        selectforeground=[("readonly", C["text"])])
    trough = _blend("#FFFFFF", C["bg"], 0.07) if _is_fx_theme() else C["bg_panel"]
    s.configure("AI.Horizontal.TProgressbar",
        troughcolor=trough, background=C["orange"],
        bordercolor=border if not soft else trough, lightcolor=C["orange"],
        darkcolor=C["orange_dim"], thickness=6 if soft else 14)
    # Убираем белые края — глобальные стили фона
    s.configure("TNotebook",     background=C["bg"], borderwidth=0)
    s.configure("TNotebook.Tab", background=C["bg_panel"], foreground=C["text_muted"],
                font=_font(8, "bold"), padding=[8, 4])
    s.map("TNotebook.Tab",
          background=[("selected", C.get("orange_glow", C["bg_panel"]))],
          foreground=[("selected", C["orange"])])
    s.configure("TFrame",  background=C["bg"])
    s.configure("TLabel",  background=C["bg"], foreground=C["text"])
    s.configure("Vertical.TScrollbar",
                background=C["bg_panel"], troughcolor=C["bg"],
                bordercolor=C["border"], arrowcolor=C["text_muted"],
                lightcolor=C["bg_panel"], darkcolor=C["bg"])
    s.configure("Horizontal.TScrollbar",
                background=C["bg_panel"], troughcolor=C["bg"],
                bordercolor=C["border"], arrowcolor=C["text_muted"],
                lightcolor=C["bg_panel"], darkcolor=C["bg"])
    thumb = _blend(C["text_dim"], C["bg"], 0.55)
    for orient in ("Vertical", "Horizontal"):
        s.map(f"{orient}.TScrollbar",
              background=[("disabled", C["bg"]), ("pressed", C["accent_dim"]), ("active", C["bg_input"])],
              arrowcolor=[("disabled", C["text_dim"])])
    # Тонкий скроллбар без стрелок для мягких тем
    s.layout("Soft.Vertical.TScrollbar", [
        ("Vertical.Scrollbar.trough", {"sticky": "ns", "children": [
            ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"})]})])
    s.configure("Soft.Vertical.TScrollbar", background=thumb, troughcolor=C["bg"],
                bordercolor=C["bg"], lightcolor=thumb, darkcolor=thumb, gripcount=0, arrowsize=8)
    s.map("Soft.Vertical.TScrollbar",
          background=[("pressed", C["accent_dim"]), ("active", _blend(C["text_muted"], C["bg"], 0.6))],
          lightcolor=[("pressed", C["accent_dim"])], darkcolor=[("pressed", C["accent_dim"])])

def mk_cb(parent, values, width=26):
    return ttk.Combobox(parent, values=values, state="readonly",
                        width=width, style="AI.TCombobox", font=FE)

# ══════════════════════════════════════════
#  ИКОНКА
# ══════════════════════════════════════════
def _draw_atom_pil(size: int):
    from PIL import Image as PILImage
    img = PILImage.new("RGBA", (size, size), (12, 10, 9, 255))
    pixels = img.load()
    cx, cy = size // 2, size // 2
    def hex2rgb(h): return int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    def put(px, py, col):
        if 0 <= px < size and 0 <= py < size:
            r, g, b = hex2rgb(col); pixels[px, py] = (r, g, b, 255)
    R = int(size*0.43); rm = int(size*0.17); nc = int(size*0.22)
    for col, ang_deg in zip(["#FF5E1A","#E8222A","#FFA030"], [0, 60, 120]):
        ang = math.radians(ang_deg); ca, sa = math.cos(ang), math.sin(ang)
        for t_deg in range(0, 360, 1):
            t = math.radians(t_deg); lx = R*math.cos(t); ly = rm*math.sin(t)
            px = int(cx + lx*ca - ly*sa); py = int(cy + lx*sa + ly*ca)
            put(px, py, col); put(px+1, py, col)
    er = max(1, size//16)
    for ang_deg, col in zip([0,60,120], ["#FFDD44","#FF7744","#FFB844"]):
        ang = math.radians(ang_deg); ca, sa = math.cos(ang), math.sin(ang)
        ex = int(cx + R*ca); ey = int(cy + R*sa)
        for dy in range(-er, er+1):
            for dx in range(-er, er+1):
                if dx*dx+dy*dy <= er*er: put(ex+dx, ey+dy, col)
    for radius, color in [(nc,"#AA0E00"),(nc-1,"#CC1100"),(nc-2,"#DD2200"),
                          (nc-3,"#EE3300"),(nc-4,"#FF4400"),(nc-5,"#FF6600"),
                          (nc-6,"#FF8800"),(nc-7,"#FFAA00"),(nc-8,"#FFCC00")]:
        if radius < 1: continue
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                if dx*dx+dy*dy <= radius*radius: put(cx+dx, cy+dy, color)
    hot_r = max(1, size//10); hx, hy = cx-size//10, cy-size//10
    for dy in range(-hot_r, hot_r+1):
        for dx in range(-hot_r, hot_r+1):
            if dx*dx+dy*dy <= hot_r*hot_r: put(hx+dx, hy+dy, "#FFEE44")
    put(hx, hy, "#FFFFFF")
    crack = max(3, size//7)
    for i in range(crack):
        px = cx + (1 if i%2==0 else 0) + i//2; py = cy - crack + i
        put(px, py, "#FFEE88"); put(px+1, py, "#FFDD44")
    ray_s = nc + 1; ray_e = nc + max(2, size//8)
    for (dx, dy), col in zip(
        [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)],
        ["#FFDD44","#FF9944","#FF7722","#FF5E1A","#FF4422","#FF6622","#FF8844","#FFAA44"]):
        mag = math.sqrt(dx*dx + dy*dy)
        for d in range(ray_s, ray_e+1): put(int(cx+dx/mag*d), int(cy+dy/mag*d), col)
    return img

def ensure_icon() -> str:
    from PIL import Image as PILImage
    ico_path = os.path.join(BASE_DIR, "icon.ico")
    if not os.path.exists(ico_path):
        sizes = [16, 32, 48]; images = [_draw_atom_pil(s) for s in sizes]
        images[0].save(ico_path, format="ICO", sizes=[(s,s) for s in sizes], append_images=images[1:])
    return ico_path

def make_atom_icon(size=32):
    from PIL import ImageTk
    return ImageTk.PhotoImage(_draw_atom_pil(size))

# ══════════════════════════════════════════
#  COLOUR BLEND UTIL
# ══════════════════════════════════════════
def _blend(fg: str, bg: str, alpha: float) -> str:
    alpha = max(0.0, min(1.0, alpha))
    def parse(h):
        h = h.lstrip("#")
        return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    fr, fg_, fb = parse(fg)
    br, bg_, bb = parse(bg)
    return f"#{int(br+(fr-br)*alpha):02X}{int(bg_+(fg_-bg_)*alpha):02X}{int(bb+(fb-bb)*alpha):02X}"

# ══════════════════════════════════════════
#  GALAXY FX
# ══════════════════════════════════════════
class GalaxyFX:
    STAR_COLORS = ["#FFFFFF","#EEEEFF","#DDDDFF","#CCCCFF","#AAAAEE",
                   "#9999DD","#BBBBFF","#E8E0FF","#C8C0FF","#FFE8FF"]

    def __init__(self, canvas: tk.Canvas, width: int, height: int, bg_col: str = "#030110"):
        self.cv = canvas; self.W = width; self.H = height; self.bg_col = bg_col
        self._items = []; self._stars = []; self._tick = 0
        self._after_id = None; self._active = True
        rng = random.Random(42)
        self._build(rng)

    def _build(self, rng):
        self._draw_milky_way(rng)
        self._draw_nebulae(rng)
        self._draw_far_stars(rng)
        self._draw_bright_stars(rng)

    def _draw_milky_way(self, rng):
        cx, cy = self.W*0.55, self.H*0.5
        ang = math.radians(-28); ca, sa = math.cos(ang), math.sin(ang)
        length = max(self.W, self.H) * 1.3
        for count, spread, brightness in [(350,28,0.12),(220,14,0.22),(80,6,0.35)]:
            for _ in range(count):
                t = rng.uniform(-length/2, length/2)
                perp = rng.gauss(0, spread)
                px = cx + t*ca - perp*sa; py = cy + t*sa + perp*ca
                if not (0 <= px <= self.W and 0 <= py <= self.H): continue
                r_c = rng.random()
                col = "#8080CC" if r_c < 0.4 else ("#6060AA" if r_c < 0.7 else "#A0A0EE")
                col = _blend(col, self.bg_col, brightness*rng.uniform(0.4,1.0))
                sz = rng.choice([1,1,1,2])
                iid = self.cv.create_oval(px, py, px+sz, py+sz, fill=col, outline="")
                self._items.append(iid)

    def _draw_nebulae(self, rng):
        for nx, ny, rw, rh, col, alpha in [
            (self.W*0.72, self.H*0.25, 55, 18, "#3B1F6A", 0.18),
            (self.W*0.30, self.H*0.70, 45, 15, "#1A2A5A", 0.15),
            (self.W*0.85, self.H*0.60, 35, 12, "#2A0A3A", 0.20),
            (self.W*0.15, self.H*0.30, 40, 14, "#0A1A3A", 0.14),
        ]:
            for i in range(6, 0, -1):
                f = i/6
                blended = _blend(col, self.bg_col, alpha*f)
                iid = self.cv.create_oval(nx-rw*f, ny-rh*f, nx+rw*f, ny+rh*f, fill=blended, outline="")
                self._items.append(iid)

    def _draw_far_stars(self, rng):
        for _ in range(160):
            x = rng.uniform(0, self.W); y = rng.uniform(0, self.H)
            col = rng.choice(self.STAR_COLORS); sz = rng.choice([1,1,1,1,2])
            phase = rng.uniform(0, 2*math.pi); speed = rng.uniform(0.02, 0.06)
            iid = self.cv.create_oval(x, y, x+sz, y+sz, fill=col, outline="")
            self._stars.append((iid, col, phase, speed, sz))
            self._items.append(iid)

    def _draw_bright_stars(self, rng):
        for _ in range(12):
            x = rng.uniform(4, self.W-4); y = rng.uniform(4, self.H-4)
            r_c = rng.random()
            col = "#FFFFFF" if r_c < 0.4 else ("#C8E8FF" if r_c < 0.7 else "#E8C8FF")
            sz = rng.choice([2,2,3]); ray = rng.randint(4, 9)
            iid = self.cv.create_oval(x-sz//2, y-sz//2, x+sz//2+1, y+sz//2+1, fill=col, outline="")
            self._items.append(iid)
            for dx, dy, rlen in [(1,0,ray),(-1,0,ray),(0,1,ray),(0,-1,ray),
                                  (1,1,ray//2),(-1,-1,ray//2),(1,-1,ray//2),(-1,1,ray//2)]:
                dim = _blend(col, self.bg_col, 0.35)
                iid2 = self.cv.create_line(x, y, x+dx*rlen, y+dy*rlen, fill=dim, width=1)
                self._items.append(iid2)
            phase = rng.uniform(0, 2*math.pi); speed = rng.uniform(0.03, 0.08)
            self._stars.append((iid, col, phase, speed, sz))

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _animate(self):
        if not self._active: return
        self._tick += 1
        for iid, base_col, phase, speed, sz in self._stars:
            t = self._tick * speed + phase
            brightness = 0.3 + 0.7*(0.5 + 0.5*math.sin(t))
            col = _blend(base_col, self.bg_col, brightness)
            try: self.cv.itemconfig(iid, fill=col)
            except tk.TclError: pass
        self._after_id = self.cv.after(60, self._animate)

    def destroy(self):
        self.stop()
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._stars.clear()

# ══════════════════════════════════════════
#  NEBULA FX
# ══════════════════════════════════════════
class NebulaFX:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._particles = []; self._tick = 0
        self._after_id = None; self._active = True
        rng = random.Random(77)
        self._build(rng)

    def _build(self, rng):
        bg = "#000308"
        for nx, ny, rw, rh, col, alpha in [
            (self.W*0.2,  self.H*0.15, 180, 80, "#002244", 0.35),
            (self.W*0.7,  self.H*0.25, 160, 70, "#200040", 0.30),
            (self.W*0.5,  self.H*0.55, 200, 90, "#003322", 0.25),
            (self.W*0.1,  self.H*0.70, 140, 60, "#220033", 0.28),
            (self.W*0.85, self.H*0.80, 170, 75, "#001A44", 0.32),
            (self.W*0.4,  self.H*0.85, 150, 65, "#002222", 0.22),
        ]:
            for i in range(8, 0, -1):
                f = i/8; blended = _blend(col, bg, alpha*f)
                iid = self.cv.create_oval(nx-rw*f, ny-rh*f, nx+rw*f, ny+rh*f, fill=blended, outline="")
                self._items.append(iid)

        thread_colors = ["#003366","#330044","#004433","#110033"]
        for _ in range(40):
            x1 = rng.uniform(0, self.W); y1 = rng.uniform(0, self.H)
            ang = rng.uniform(0, 2*math.pi); length = rng.uniform(30, 120)
            x2 = x1 + math.cos(ang)*length; y2 = y1 + math.sin(ang)*length
            col = _blend(rng.choice(thread_colors), bg, rng.uniform(0.2, 0.6))
            iid = self.cv.create_line(x1, y1, x2, y2, fill=col, width=1, smooth=True)
            self._items.append(iid)

        star_cols = ["#FFFFFF","#AAFFFF","#FFAAFF","#AAFFAA","#FFFFAA","#00FFFF","#FF00FF"]
        for _ in range(200):
            x = rng.uniform(0, self.W); y = rng.uniform(0, self.H)
            col = rng.choice(star_cols); sz = rng.choice([1,1,1,2,2,3])
            phase = rng.uniform(0, 2*math.pi); speed = rng.uniform(0.015, 0.05)
            vx = rng.uniform(-0.1, 0.1); vy = rng.uniform(-0.05, 0.05)
            iid = self.cv.create_oval(x, y, x+sz, y+sz, fill=col, outline="")
            self._particles.append([iid, x, y, sz, col, phase, speed, vx, vy])
            self._items.append(iid)

        for _ in range(18):
            x = rng.uniform(8, self.W-8); y = rng.uniform(8, self.H-8)
            col = rng.choice(["#FFFFFF","#AAFFFF","#FF88FF","#88FFFF"])
            sz = rng.choice([2, 3]); ray = rng.randint(6, 16)
            iid = self.cv.create_oval(x-sz, y-sz, x+sz, y+sz, fill=col, outline="")
            self._items.append(iid)
            for dx, dy, rlen in [(1,0,ray),(-1,0,ray),(0,1,ray),(0,-1,ray),
                                  (1,1,ray//2),(-1,-1,ray//2),(1,-1,ray//2),(-1,1,ray//2)]:
                dim = _blend(col, bg, 0.4)
                iid2 = self.cv.create_line(x, y, x+dx*rlen, y+dy*rlen, fill=dim, width=1)
                self._items.append(iid2)
            phase = rng.uniform(0, 2*math.pi); speed = rng.uniform(0.02, 0.06)
            self._particles.append([iid, x, y, sz, col, phase, speed, 0, 0])

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _animate(self):
        if not self._active: return
        self._tick += 1
        bg = "#000308"
        for p in self._particles:
            iid, x, y, sz, col, phase, speed, vx, vy = p
            t = self._tick * speed + phase
            brightness = 0.25 + 0.75*(0.5 + 0.5*math.sin(t))
            fc = _blend(col, bg, brightness)
            nx = (x + vx) % self.W; ny = (y + vy) % self.H
            p[1] = nx; p[2] = ny
            try:
                self.cv.itemconfig(iid, fill=fc)
                self.cv.coords(iid, nx, ny, nx+sz, ny+sz)
            except tk.TclError: pass
        self._after_id = self.cv.after(50, self._animate)

    def resize(self, W, H):
        self.stop()
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._particles.clear()
        self.W = W; self.H = H
        rng = random.Random(77)
        self._build(rng)
        self._active = True; self._animate()

    def destroy(self):
        self.stop()
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._particles.clear()

# ══════════════════════════════════════════
#  REICH FX
# ══════════════════════════════════════════
class ReichFX:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._flames = []; self._tick = 0
        self._after_id = None; self._active = True
        self._build()

    def _build(self):
        W, H = self.W, self.H; bg = "#0A0800"
        stripe_w = max(4, W//40)
        for i in range(0, W, stripe_w*3):
            col = _blend("#1A0800", bg, 0.6)
            iid = self.cv.create_rectangle(i, 0, i+stripe_w, H, fill=col, outline="")
            self._items.append(iid)
        orn = 18
        for cx, cy in [(orn,orn),(W-orn,orn),(orn,H-orn),(W-orn,H-orn)]:
            for col, r in [("#332200",orn),("#664400",orn-3),("#CC9900",orn-6)]:
                pts = [cx, cy-r, cx+r, cy, cx, cy+r, cx-r, cy]
                iid = self.cv.create_polygon(pts, fill="", outline=col, width=1)
                self._items.append(iid)
            for dx, dy in [(0,-(orn-8)),(0,orn-8),(-(orn-8),0),(orn-8,0)]:
                iid = self.cv.create_line(cx, cy, cx+dx, cy+dy, fill="#CC9900", width=1)
                self._items.append(iid)
        for y, col, w in [(2,"#CC9900",2),(4,"#664400",1),(H-2,"#CC9900",2),(H-4,"#664400",1)]:
            iid = self.cv.create_line(0, y, W, y, fill=col, width=w)
            self._items.append(iid)
        for x, col in [(2,"#664400"),(W-2,"#664400")]:
            iid = self.cv.create_line(x, 0, x, H, fill=col, width=1)
            self._items.append(iid)
        for tx, ty in [(12, H//2), (W-12, H//2)]:
            iid = self.cv.create_rectangle(tx-2, ty, tx+2, ty+20, fill="#664400", outline="#332200")
            self._items.append(iid)
            flame_ids = []
            for layer, (col, r) in enumerate([
                ("#330000",8),("#881100",6),("#CC3300",5),("#FF6600",3),("#FFCC00",2)]):
                fy = ty - r
                iid = self.cv.create_oval(tx-r, fy-r, tx+r, fy+r, fill=col, outline="")
                self._items.append(iid)
                flame_ids.append((iid, tx, ty, r, col, layer))
            self._flames.append(flame_ids)
        mx, my = W//2, H//2
        for r, col in [(22,"#332200"),(18,"#664400"),(14,"#CC9900"),(10,"#FFD700"),(6,"#FFEEAA")]:
            iid = self.cv.create_oval(mx-r, my-r, mx+r, my+r, fill="", outline=col, width=1)
            self._items.append(iid)
        for ang_deg in range(0, 360, 45):
            ang = math.radians(ang_deg)
            x2 = mx + math.cos(ang)*22; y2 = my + math.sin(ang)*22
            iid = self.cv.create_line(mx, my, x2, y2, fill="#886600", width=1)
            self._items.append(iid)
        for x in [20, W-20]:
            for y in range(30, H-20, 12):
                col = _blend("#CC9900", bg, 0.5)
                iid = self.cv.create_oval(x-1, y-1, x+1, y+1, fill=col, outline="")
                self._items.append(iid)

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _animate(self):
        if not self._active: return
        self._tick += 1; t = self._tick * 0.12
        for flame_group in self._flames:
            for iid, tx, ty, base_r, col, layer in flame_group:
                flicker = math.sin(t*2.3 + layer*0.8) * 2
                sway    = math.sin(t*1.7 + layer*0.4) * 1.5
                r  = max(1, base_r + flicker*0.5)
                fy = ty - base_r*(layer+1)*0.8 + flicker
                fx = tx + sway
                bright = 0.6 + 0.4*(0.5 + 0.5*math.sin(t*3 + layer))
                blended = _blend(col, "#0A0800", bright)
                try:
                    self.cv.coords(iid, fx-r, fy-r, fx+r, fy+r)
                    self.cv.itemconfig(iid, fill=blended)
                except tk.TclError: pass
        self._after_id = self.cv.after(80, self._animate)

    def resize(self, W, H):
        self.stop()
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._flames.clear()
        self.W = W; self.H = H
        self._build()
        self._active = True; self._animate()

    def destroy(self):
        self.stop()
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._flames.clear()

# ══════════════════════════════════════════
#  AURORA FX
# ══════════════════════════════════════════
class AuroraFX:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._anim_items = []; self._tick = 0
        self._after_id = None; self._active = True
        self._meteors = []
        self._aurora_bands = []
        self._stars = []
        rng = random.Random(137); self._rng = rng
        self._build_static(rng)
        self._init_aurora_bands(rng)
        self._init_meteors(rng)
        self._init_stars(rng)

    def _build_static(self, rng):
        W, H = self.W, self.H; bg = "#000510"
        steps = 18
        for i in range(steps):
            t = i / steps
            r = int(0   + 5  * t)
            g = int(5   + 20 * t)
            b = int(16  + 40 * t)
            col = f"#{r:02X}{g:02X}{b:02X}"
            y0 = int(H * i / steps); y1 = int(H * (i+1) / steps)
            iid = self.cv.create_rectangle(0, y0, W, y1, fill=col, outline="")
            self._items.append(iid)
        px, py = int(W * 0.78), int(H * 0.32); pr = 48
        for dr, col in [(pr,"#0A1830"),(pr-4,"#0E2040"),(pr-9,"#122850"),
                         (pr-15,"#163468"),(pr-22,"#1A3E78"),(pr-28,"#1E4888"),
                         (pr-33,"#2050A0"),(pr-37,"#2458B0"),(pr-40,"#2860C0")]:
            if dr < 1: continue
            iid = self.cv.create_oval(px-dr, py-dr, px+dr, py+dr, fill=col, outline="")
            self._items.append(iid)
        for ar in range(pr+18, pr, -2):
            alpha = 0.06 * (ar - pr) / 18
            ac = _blend("#4488FF", bg, alpha)
            iid = self.cv.create_oval(px-ar, py-ar, px+ar, py+ar, fill="", outline=ac, width=1)
            self._items.append(iid)
        for ry_off, col, w in [(6,"#334466",2),(10,"#446688",1),(14,"#557799",1)]:
            iid = self.cv.create_oval(px-pr-20, py-ry_off, px+pr+20, py+ry_off, fill="", outline=col, width=w)
            self._items.append(iid)
        iid = self.cv.create_oval(px-pr+8, py-pr+8, px-pr+22, py-pr+22, fill="#3A6AAA", outline="")
        self._items.append(iid)
        iid = self.cv.create_oval(px-pr+11, py-pr+11, px-pr+17, py-pr+17, fill="#6699CC", outline="")
        self._items.append(iid)
        for nx, ny, rw, rh, col, alpha in [
            (W*0.15, H*0.20, 120, 55, "#220044", 0.40),
            (W*0.60, H*0.70, 160, 70, "#002244", 0.35),
            (W*0.85, H*0.15, 100, 45, "#330022", 0.30),
            (W*0.30, H*0.85, 140, 60, "#001133", 0.28),
        ]:
            for i in range(10, 0, -1):
                f = i/10
                blended = _blend(col, bg, alpha*f)
                iid = self.cv.create_oval(nx-rw*f, ny-rh*f, nx+rw*f, ny+rh*f, fill=blended, outline="")
                self._items.append(iid)

    def _init_aurora_bands(self, rng):
        H = self.H; W = self.W
        colors = [
            ("#00FF88","#00CCAA"), ("#44FFCC","#0088FF"),
            ("#FF44AA","#8844FF"), ("#AAFFEE","#4466FF"),
            ("#FF88CC","#CC44FF"),
        ]
        for i, (c1, c2) in enumerate(colors):
            y_base = H * (0.05 + i * 0.07)
            band = {
                "y": y_base, "c1": c1, "c2": c2,
                "phase": rng.uniform(0, 2*math.pi),
                "speed": rng.uniform(0.012, 0.025),
                "amp":   rng.uniform(H*0.03, H*0.07),
                "alpha": rng.uniform(0.08, 0.18),
                "width": rng.uniform(H*0.025, H*0.06),
                "items": []
            }
            self._aurora_bands.append(band)

    def _init_meteors(self, rng):
        for _ in range(5):
            self._meteors.append(self._new_meteor(rng, start_offscreen=True))

    def _new_meteor(self, rng, start_offscreen=False):
        W, H = self.W, self.H
        ang = rng.uniform(-0.6, -0.3)
        speed = rng.uniform(6, 14)
        if start_offscreen:
            x = rng.uniform(0, W); y = -rng.uniform(0, H*0.3)
        else:
            x = rng.uniform(0, W*1.2); y = -20
        col = rng.choice(["#FFFFFF","#AAFFFF","#FFE8FF","#FFAAFF","#AAFFEE"])
        length = rng.randint(30, 80)
        return [x, y, math.cos(ang)*speed, math.sin(ang)*speed, length, col, 1.0]

    def _init_stars(self, rng):
        for _ in range(280):
            x = rng.uniform(0, self.W); y = rng.uniform(0, self.H)
            col = rng.choice(["#FFFFFF","#DDEEFF","#EEEEFF","#FFDDFF","#CCFFFF"])
            sz = rng.choice([1,1,1,1,2])
            phase = rng.uniform(0, 2*math.pi)
            speed = rng.uniform(0.01, 0.04)
            iid = self.cv.create_oval(x,y,x+sz,y+sz, fill=col, outline="")
            self._stars.append((iid, x, y, sz, col, phase, speed))
            self._items.append(iid)

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _animate(self):
        if not self._active: return
        self._tick += 1; t = self._tick
        bg = "#000510"
        for iid in self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._anim_items.clear()
        W = self.W
        for band in self._aurora_bands:
            pts = []
            seg = max(W // 20, 1)
            phase = band["phase"] + t * band["speed"]
            amp = band["amp"]
            width = band["width"]
            alpha = band["alpha"] * (0.6 + 0.4 * math.sin(t * 0.03 + band["phase"]))
            for xi in range(0, W + seg, seg):
                wave = amp * math.sin(phase + xi * 0.008)
                pts.append((xi, band["y"] + wave))
            c1 = band["c1"]; c2 = band["c2"]
            for i in range(len(pts)-1):
                x1,y1 = pts[i]; x2,y2 = pts[i+1]
                mid_col = c1 if (i % 2 == 0) else c2
                blend_col = _blend(mid_col, bg, alpha * (0.4 + 0.6*(i%3)/2))
                poly = [x1, y1-width/2, x2, y2-width/2,
                        x2, y2+width/2, x1, y1+width/2]
                iid = self.cv.create_polygon(poly, fill=blend_col, outline="", smooth=True)
                self._anim_items.append(iid)
            for i in range(len(pts)-1):
                x1,y1 = pts[i]; x2,y2 = pts[i+1]
                gc = _blend(c1, bg, alpha * 0.8)
                iid = self.cv.create_line(x1,y1, x2,y2, fill=gc, width=2, smooth=True)
                self._anim_items.append(iid)
        for m in self._meteors:
            mx,my,vx,vy,length,col,alpha = m
            mx += vx; my += vy; m[0]=mx; m[1]=my
            if my > self.H + 50 or mx < -100:
                nm = self._new_meteor(self._rng)
                m[:] = nm; continue
            for j in range(8):
                frac = (j+1)/8
                tx = mx - vx*frac*length/10
                ty = my - vy*frac*length/10
                a = alpha * (1-frac) * 0.7
                fc = _blend(col, bg, a)
                r = max(1, int((1-frac)*2))
                iid = self.cv.create_oval(tx-r,ty-r,tx+r,ty+r, fill=fc, outline="")
                self._anim_items.append(iid)
            fc = _blend(col, bg, min(1.0, alpha))
            iid = self.cv.create_oval(mx-2,my-2,mx+2,my+2, fill=fc, outline="")
            self._anim_items.append(iid)
        for iid,x,y,sz,col,phase,speed in self._stars:
            bright = 0.3 + 0.7*(0.5 + 0.5*math.sin(t*speed+phase))
            fc = _blend(col, bg, bright)
            try: self.cv.itemconfig(iid, fill=fc)
            except tk.TclError: pass
        self._after_id = self.cv.after(45, self._animate)

    def resize(self, W, H):
        self.stop()
        for iid in self._items + self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._anim_items.clear()
        self._stars.clear(); self._aurora_bands.clear(); self._meteors.clear()
        self.W = W; self.H = H
        rng = random.Random(137)
        self._build_static(rng); self._init_aurora_bands(rng)
        self._init_meteors(rng); self._init_stars(rng)
        self._active = True; self._animate()

    def destroy(self):
        self.stop()
        for iid in self._items + self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._anim_items.clear()


# ══════════════════════════════════════════
#  GHOUL FX — Tokyo Ghoul + Хиганбана (паучьи лилии)
#  Кагунэ, глаза гуля, кровавые капли, трещины,
#  + ПАУЧЬИ ЛИЛИИ (Lycoris radiata / Higanbana)
# ══════════════════════════════════════════
class DedinsaidFX:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._anim = []; self._tick = 0
        self._after_id = None; self._active = True
        rng = random.Random(666); self._rng = rng
        self._drops = []
        self._eyes  = []
        self._kagune = []
        self._lilies = []   # статичные паучьи лилии
        self._lily_anim = []  # анимированные элементы лилий
        self._build_static(rng)
        self._init_drops(rng)
        self._init_eyes(rng)
        self._init_kagune(rng)
        self._init_lilies(rng)

    def _build_static(self, rng):
        W, H = self.W, self.H
        bg = "#080808"
        for i in range(10):
            t = i / 10
            r = int(8 + 6*t); g = 0; b = 0
            col = f"#{r:02X}{g:02X}{b:02X}"
            y0 = int(H*i/10); y1 = int(H*(i+1)/10)
            iid = self.cv.create_rectangle(0, y0, W, y1, fill=col, outline="")
            self._items.append(iid)
        crack_colors = ["#1A0000","#220000","#2A0000","#300000"]
        for _ in range(12):
            x = rng.uniform(0, W); y = rng.uniform(0, H)
            angle = rng.uniform(-0.8, 0.8)
            length = rng.uniform(40, 180)
            segs = rng.randint(3, 7)
            cx, cy = x, y
            for _ in range(segs):
                nx = cx + math.cos(angle)*length/segs + rng.uniform(-15, 15)
                ny = cy + math.sin(angle)*length/segs + rng.uniform(-8, 8)
                col = rng.choice(crack_colors)
                w = rng.choice([1, 1, 2])
                iid = self.cv.create_line(cx, cy, nx, ny, fill=col, width=w)
                self._items.append(iid)
                if rng.random() < 0.4:
                    bx = cx + math.cos(angle+1)*20 + rng.uniform(-10,10)
                    by = cy + math.sin(angle+1)*20 + rng.uniform(-5,5)
                    iid2 = self.cv.create_line(cx, cy, bx, by, fill=col, width=1)
                    self._items.append(iid2)
                cx, cy = nx, ny
        symbols = ["喰", "種", "東", "京", "区", "捜", "査", "官", "人", "間"]
        for _ in range(8):
            x = rng.uniform(20, W-20); y = rng.uniform(20, H-20)
            sym = rng.choice(symbols)
            col = _blend("#440000", bg, rng.uniform(0.2, 0.5))
            iid = self.cv.create_text(x, y, text=sym, fill=col,
                                       font=("Arial", rng.randint(16, 32), "bold"))
            self._items.append(iid)

    def _draw_spider_lily(self, cx, cy, size, phase_offset=0.0, stem_col="#1A3A00", bloom_alpha=0.85):
        """
        Рисует паучью лилию (Lycoris radiata / Higanbana).
        cx, cy — центр цветка (точка где начинаются лепестки).
        size — радиус цветка.
        Возвращает список iid созданных элементов.
        """
        items = []
        bg = "#080808"
        num_petals = 6
        stamen_count = 12  # тычинки

        # Лепестки — изогнутые назад (как у реальной хиганбаны)
        petal_col_inner = "#FF0000"
        petal_col_outer = "#CC0000"
        for pi in range(num_petals):
            base_ang = math.radians(pi * 60 + 30)
            # Лепесток — длинный, изгибается назад
            pts = []
            for ti in range(12):
                t = ti / 11
                # Основная кривая лепестка — загибается назад к верхушке
                ang = base_ang + math.radians(t * 25 - 12)
                # Радиус: сначала растёт, потом загибается
                r = size * (0.2 + 0.8*math.sin(t * math.pi))
                # Боковое смещение для ширины лепестка
                lateral = math.radians(90) + base_ang
                width_factor = math.sin(t * math.pi) * size * 0.22
                px = cx + math.cos(ang) * r + math.cos(lateral) * width_factor * (0.5 - (ti % 2)*0.03)
                py = cy + math.sin(ang) * r + math.sin(lateral) * width_factor * (0.5 - (ti % 2)*0.03)
                pts.extend([px, py])
            # Ось лепестка (центральная жилка)
            tip_x = cx + math.cos(base_ang) * size * 1.05
            tip_y = cy + math.sin(base_ang) * size * 1.05
            col = _blend(petal_col_inner, bg, bloom_alpha * 0.9)
            if len(pts) >= 4:
                iid = self.cv.create_line(pts, fill=col, width=2, smooth=True, capstyle="round")
                items.append(iid)
            # Жилка посередине лепестка
            vein_col = _blend("#FF2200", bg, bloom_alpha * 0.6)
            iid = self.cv.create_line(cx, cy, tip_x, tip_y, fill=vein_col, width=1, smooth=True)
            items.append(iid)

        # Тычинки — длинные нити с пыльниками на концах
        stamen_col = _blend("#FF3300", bg, bloom_alpha)
        anther_col = _blend("#FFCC00", bg, bloom_alpha * 0.9)  # жёлтые пыльники
        for si in range(stamen_count):
            ang = math.radians(si * (360 / stamen_count) + phase_offset * 30)
            # Нить: изгибается наружу дугой
            s_len = size * 1.35
            # Дуга нити
            mid_ang = ang + math.radians(15)
            mid_r = s_len * 0.6
            sx1 = cx + math.cos(mid_ang) * mid_r * 0.4
            sy1 = cy + math.sin(mid_ang) * mid_r * 0.4
            sx2 = cx + math.cos(mid_ang) * mid_r
            sy2 = cy + math.sin(mid_ang) * mid_r
            ex = cx + math.cos(ang) * s_len
            ey = cy + math.sin(ang) * s_len
            iid = self.cv.create_line(cx, cy, sx1, sy1, sx2, sy2, ex, ey,
                                       fill=stamen_col, width=1, smooth=True)
            items.append(iid)
            # Пыльник — маленький жёлтый овал на конце
            ar = max(1, int(size * 0.08))
            iid = self.cv.create_oval(ex-ar, ey-ar, ex+ar, ey+ar, fill=anther_col, outline="")
            items.append(iid)

        # Центр цветка — тёмно-красный кружок
        cr = max(2, int(size * 0.18))
        center_col = _blend("#880000", bg, bloom_alpha)
        iid = self.cv.create_oval(cx-cr, cy-cr, cx+cr, cy+cr, fill=center_col, outline="#FF0000")
        items.append(iid)

        return items

    def _draw_stem_with_flower(self, canvas, sx, sy, stem_h, size, phase_offset=0.0, bloom_alpha=0.85):
        """Рисует стебель + цветок наверху."""
        items = []
        bg = "#080808"
        stem_col = _blend("#1A3A00", bg, 0.7)

        # Стебель — слегка изогнутый
        stem_bend = math.sin(phase_offset) * 8
        mid_x = sx + stem_bend
        mid_y = sy - stem_h * 0.5
        flower_x = sx + stem_bend * 0.5
        flower_y = sy - stem_h

        iid = canvas.create_line(sx, sy, mid_x, mid_y, flower_x, flower_y,
                                  fill=stem_col, width=2, smooth=True, capstyle="round")
        items.append(iid)

        # Цветок на вершине
        flower_items = self._draw_spider_lily(
            flower_x, flower_y, size, phase_offset, stem_col, bloom_alpha
        )
        items.extend(flower_items)
        return items, flower_x, flower_y

    def _init_lilies(self, rng):
        """Инициализирует группы паучьих лилий вдоль нижнего края."""
        W, H = self.W, self.H
        # Несколько групп цветов вдоль низа
        num_groups = max(3, W // 150)
        for gi in range(num_groups):
            group_x = W * (gi + 0.5) / num_groups + rng.uniform(-30, 30)
            group_y = H - rng.uniform(10, 30)  # основание у нижнего края
            # В каждой группе 2-4 цветка
            num_flowers = rng.randint(2, 4)
            for fi in range(num_flowers):
                sx = group_x + rng.uniform(-35, 35)
                sy = group_y + rng.uniform(-5, 5)
                stem_h = rng.uniform(H * 0.12, H * 0.22)
                size = rng.uniform(14, 22)
                phase = rng.uniform(0, 2 * math.pi)
                bloom_alpha = rng.uniform(0.55, 0.9)
                self._lilies.append({
                    "sx": sx, "sy": sy,
                    "stem_h": stem_h, "size": size,
                    "phase": phase, "bloom_alpha": bloom_alpha,
                    "sway_speed": rng.uniform(0.008, 0.018),
                    "items": []
                })

        # Один крупный цветок — ближний план (большой, яркий)
        self._lilies.append({
            "sx": W * 0.62, "sy": H,
            "stem_h": H * 0.32, "size": 32,
            "phase": 0.5, "bloom_alpha": 1.0,
            "sway_speed": 0.006,
            "items": []
        })

    def _redraw_lilies(self, tick):
        """Перерисовывает все лилии с анимацией покачивания."""
        for iid in self._lily_anim:
            try: self.cv.delete(iid)
            except: pass
        self._lily_anim.clear()

        bg = "#080808"
        for lily in self._lilies:
            # Покачивание стебля на ветру
            sway = math.sin(tick * lily["sway_speed"] + lily["phase"]) * 4
            sx = lily["sx"] + sway * 0.3
            sy = lily["sy"]
            phase_off = lily["phase"] + tick * lily["sway_speed"] * 0.5

            # Пульсация яркости
            pulse = 0.85 + 0.15 * math.sin(tick * 0.04 + lily["phase"])
            alpha = lily["bloom_alpha"] * pulse

            items, fx, fy = self._draw_stem_with_flower(
                self.cv, sx, sy, lily["stem_h"], lily["size"],
                phase_off, alpha
            )
            self._lily_anim.extend(items)

    def _init_drops(self, rng):
        for _ in range(18):
            x = rng.uniform(0, self.W)
            y = rng.uniform(-self.H, 0)
            speed = rng.uniform(0.8, 3.5)
            size  = rng.uniform(2, 6)
            alpha = rng.uniform(0.4, 1.0)
            self._drops.append([x, y, speed, size, alpha])

    def _init_eyes(self, rng):
        for _ in range(3):
            x = rng.uniform(self.W*0.1, self.W*0.9)
            y = rng.uniform(self.H*0.1, self.H*0.6)  # не перекрывают лилии
            phase = rng.uniform(0, 2*math.pi)
            blink_speed = rng.uniform(0.008, 0.02)
            size = rng.uniform(6, 14)
            self._eyes.append({
                "x": x, "y": y, "phase": phase,
                "speed": blink_speed, "size": size,
                "items": []
            })

    def _init_kagune(self, rng):
        origins = [
            (0, self.H),
            (self.W, self.H),
            (self.W//2, self.H),
        ]
        for ox, oy in origins:
            tentacle = {
                "ox": ox, "oy": oy,
                "phase": rng.uniform(0, 2*math.pi),
                "speed": rng.uniform(0.015, 0.03),
                "length": rng.randint(8, 14),
                "spread": rng.uniform(25, 50),
                "items": []
            }
            self._kagune.append(tentacle)

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _draw_eye(self, eye, tick):
        for iid in eye["items"]:
            try: self.cv.delete(iid)
            except: pass
        eye["items"].clear()
        x, y = eye["x"], eye["y"]
        sz = eye["size"]
        phase = eye["phase"] + tick * eye["speed"]
        blink = 0.5 + 0.5*math.sin(phase * 3.7)
        if blink < 0.1: return
        glow_alpha = 0.3 + 0.7*(0.5 + 0.5*math.sin(phase))
        gap = sz * 2.2
        for ex in [x - gap/2, x + gap/2]:
            for gr in range(int(sz*2.5), int(sz)-1, -2):
                ga = glow_alpha * 0.06 * (gr / (sz*2.5))
                gc = _blend("#FF0000", "#080808", ga)
                iid = self.cv.create_oval(ex-gr, y-gr*blink*0.6,
                                           ex+gr, y+gr*blink*0.6,
                                           fill=gc, outline="")
                eye["items"].append(iid)
            eye_col = _blend("#FF2222", "#880000", glow_alpha*0.8)
            iid = self.cv.create_oval(ex-sz, y-sz*blink*0.55,
                                       ex+sz, y+sz*blink*0.55,
                                       fill=eye_col, outline="#FF0000", width=1)
            eye["items"].append(iid)
            pr = sz * 0.45
            iid = self.cv.create_oval(ex-pr, y-pr*blink*0.5,
                                       ex+pr, y+pr*blink*0.5,
                                       fill="#0A0000", outline="")
            eye["items"].append(iid)
            iid = self.cv.create_oval(ex-pr*0.3, y-pr*0.4,
                                       ex+pr*0.1, y,
                                       fill="#FF4444", outline="")
            eye["items"].append(iid)

    def _draw_kagune(self, tentacle, tick):
        for iid in tentacle["items"]:
            try: self.cv.delete(iid)
            except: pass
        tentacle["items"].clear()
        ox, oy = tentacle["ox"], tentacle["oy"]
        phase = tentacle["phase"] + tick * tentacle["speed"]
        n = tentacle["length"]
        spread = tentacle["spread"]
        pts = []
        for i in range(n):
            t = i / (n-1)
            base_x = ox + math.sin(phase + t*2.5) * spread * (1-t*0.3)
            base_y = oy - t * self.H * 0.6
            wave_x = math.sin(phase*1.7 + t*3.5) * spread * 0.4 * t
            pts.append((base_x + wave_x, base_y))
        for i in range(len(pts)-1):
            x1, y1 = pts[i]; x2, y2 = pts[i+1]
            t = 1 - i/(len(pts)-1)
            width = max(1, int(t * 5))
            alpha = 0.4 + 0.6*t
            col = _blend("#FF1100", "#330000", alpha * (0.5 + 0.5*t))
            iid = self.cv.create_line(x1, y1, x2, y2, fill=col, width=width,
                                       smooth=True, capstyle="round")
            tentacle["items"].append(iid)
            if i % 3 == 0:
                glow = _blend("#FF0000", "#080808", alpha * 0.15)
                iid2 = self.cv.create_line(x1, y1, x2, y2,
                                            fill=glow, width=width+4, smooth=True)
                tentacle["items"].append(iid2)
                self.cv.tag_lower(iid2)

    def _animate(self):
        if not self._active: return
        self._tick += 1; t = self._tick
        bg = "#080808"

        # ── Кровавые капли ──────────────────────────────────────
        for iid in self._anim:
            try: self.cv.delete(iid)
            except: pass
        self._anim.clear()

        for drop in self._drops:
            x, y, speed, size, alpha = drop
            y += speed; drop[1] = y
            if y > self.H + 20:
                drop[0] = self._rng.uniform(0, self.W)
                drop[1] = self._rng.uniform(-60, -5)
                drop[3] = self._rng.uniform(2, 6)
            col = _blend("#CC0000", bg, alpha * (0.6 + 0.4*math.sin(t*0.05+x)))
            r = size; ry = r * 1.6
            iid = self.cv.create_oval(x-r, y-ry, x+r, y+r, fill=col, outline="")
            self._anim.append(iid)
            tail_col = _blend("#880000", bg, alpha * 0.4)
            iid2 = self.cv.create_line(x, y-ry, x, y-ry-r*2,
                                        fill=tail_col, width=max(1,int(r*0.6)))
            self._anim.append(iid2)

        # ── Глаза гуля ──────────────────────────────────────────
        for eye in self._eyes:
            self._draw_eye(eye, t)

        # ── Кагунэ ──────────────────────────────────────────────
        for tentacle in self._kagune:
            self._draw_kagune(tentacle, t)

        # ── Паучьи лилии (анимация покачивания) ─────────────────
        self._redraw_lilies(t)

        self._after_id = self.cv.after(50, self._animate)

    def resize(self, W, H):
        self.stop()
        for iid in self._items + self._anim + self._lily_anim:
            try: self.cv.delete(iid)
            except: pass
        for eye in self._eyes:
            for iid in eye["items"]:
                try: self.cv.delete(iid)
                except: pass
        for kg in self._kagune:
            for iid in kg["items"]:
                try: self.cv.delete(iid)
                except: pass
        self._items.clear(); self._anim.clear(); self._lily_anim.clear()
        self._drops.clear(); self._eyes.clear(); self._kagune.clear(); self._lilies.clear()
        self.W = W; self.H = H
        rng = random.Random(666)
        self._build_static(rng); self._init_drops(rng)
        self._init_eyes(rng); self._init_kagune(rng); self._init_lilies(rng)
        self._active = True; self._animate()

    def destroy(self):
        self.stop()
        for iid in self._items + self._anim + self._lily_anim:
            try: self.cv.delete(iid)
            except: pass
        for eye in self._eyes:
            for iid in eye["items"]:
                try: self.cv.delete(iid)
                except: pass
        for kg in self._kagune:
            for iid in kg["items"]:
                try: self.cv.delete(iid)
                except: pass
        self._items.clear(); self._anim.clear(); self._lily_anim.clear()


# ══════════════════════════════════════════
#  COLLAPSING STAR FX
# ══════════════════════════════════════════
class CollapsingStarFX:
    PHASE_EXPAND     = "expand"
    PHASE_HOLD       = "hold"
    PHASE_COLLAPSE   = "collapse"
    PHASE_BLACK_HOLE = "black_hole"
    PHASE_EXPLODE    = "explode"

    def __init__(self, canvas: tk.Canvas, cx: int, cy: int):
        self.cv = canvas; self.cx = cx; self.cy = cy
        self._items = []; self._tick = 0; self._after_id = None; self._active = True
        self._phase = self.PHASE_EXPAND
        self._phase_tick = 0
        self._max_r = 18
        self._cur_r = 2
        self._debris = []
        rng = random.Random(99); self._rng = rng
        self._orbiters = []
        for i in range(6):
            angle = i * math.pi / 3
            speed = rng.uniform(0.04, 0.09)
            dist  = rng.uniform(22, 32)
            col   = rng.choice(["#AAFFFF","#FF88FF","#88FFFF","#FFFFFF","#FFAAFF"])
            sz    = rng.choice([1, 1, 2])
            self._orbiters.append([angle, speed, dist, col, sz, None])

    def start(self): self._active = True; self._animate()
    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _clear_items(self):
        for iid in self._items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear()

    def _draw_star(self, r, col, glow_col):
        cx, cy = self.cx, self.cy
        if r < 1: r = 1
        for gr in range(int(r*2), int(r)-1, -2):
            alpha = 0.08 * (1 - gr / (r*2.5))
            gc = _blend(glow_col, "#000308", max(0.01, alpha))
            iid = self.cv.create_oval(cx-gr, cy-gr, cx+gr, cy+gr, fill=gc, outline="")
            self._items.append(iid)
        iid = self.cv.create_oval(cx-r, cy-r, cx+r, cy+r, fill=col, outline="")
        self._items.append(iid)
        ray_len = int(r * 2.2); ray_short = int(r * 1.2)
        for ang_deg, rlen in [(0,ray_len),(90,ray_len),(180,ray_len),(270,ray_len),
                               (45,ray_short),(135,ray_short),(225,ray_short),(315,ray_short)]:
            ang = math.radians(ang_deg)
            x2 = cx + math.cos(ang)*rlen; y2 = cy + math.sin(ang)*rlen
            rc = _blend(col, "#000308", 0.5)
            iid = self.cv.create_line(cx, cy, x2, y2, fill=rc, width=1)
            self._items.append(iid)

    def _draw_black_hole(self, r):
        cx, cy = self.cx, self.cy
        for ring_r in range(r + 12, r - 1, -1):
            t = (ring_r - r) / 12
            col = _blend("#AA00FF", "#000308", t * 0.6)
            iid = self.cv.create_oval(cx-ring_r, cy-ring_r, cx+ring_r, cy+ring_r,
                                       fill=col, outline="")
            self._items.append(iid)
        iid = self.cv.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#000000", outline="")
        self._items.append(iid)

    def _animate(self):
        if not self._active: return
        self._tick += 1; self._phase_tick += 1
        self._clear_items()
        cx, cy = self.cx, self.cy
        pt = self._phase_tick

        if self._phase == self.PHASE_EXPAND:
            progress = min(1.0, pt / 40)
            r = int(2 + (self._max_r - 2) * progress)
            brightness = 0.6 + 0.4 * math.sin(self._tick * 0.15)
            col = _blend("#FFFFFF", "#88AAFF", brightness)
            self._draw_star(r, col, "#4488FF")
            if pt >= 40: self._phase = self.PHASE_HOLD; self._phase_tick = 0

        elif self._phase == self.PHASE_HOLD:
            flicker = 0.75 + 0.25 * math.sin(self._tick * 0.3)
            r = int(self._max_r * flicker)
            col = _blend("#FFFFFF", "#AACCFF", flicker)
            self._draw_star(r, col, "#2266FF")
            if pt >= 50: self._phase = self.PHASE_COLLAPSE; self._phase_tick = 0

        elif self._phase == self.PHASE_COLLAPSE:
            progress = min(1.0, pt / 35)
            r = max(1, int(self._max_r * (1 - progress) ** 1.5))
            col = _blend("#FF4400", "#FFFFFF", progress * 0.8)
            self._draw_star(r, col, "#FF2200")
            for ang_deg in range(0, 360, 30):
                ang = math.radians(ang_deg)
                dist = int(30 * (1 - progress) + 5)
                x1 = cx + math.cos(ang)*dist; y1 = cy + math.sin(ang)*dist
                dim = _blend("#FF4400", "#000308", 0.3 * (1 - progress))
                iid = self.cv.create_line(x1, y1, cx, cy, fill=dim, width=1)
                self._items.append(iid)
            if pt >= 35: self._phase = self.PHASE_BLACK_HOLE; self._phase_tick = 0

        elif self._phase == self.PHASE_BLACK_HOLE:
            self._draw_black_hole(4)
            pulse_r = 8 + int(6 * abs(math.sin(pt * 0.25)))
            col = _blend("#AA00FF", "#000308", 0.4)
            iid = self.cv.create_oval(cx-pulse_r, cy-pulse_r, cx+pulse_r, cy+pulse_r,
                                       fill="", outline=col, width=1)
            self._items.append(iid)
            if pt >= 45:
                self._debris = []
                for _ in range(20):
                    ang = self._rng.uniform(0, 2*math.pi)
                    speed = self._rng.uniform(1.5, 4.0)
                    col = self._rng.choice(["#FFFFFF","#AAFFFF","#FFAAFF","#FFFF88","#FF8800"])
                    sz = self._rng.choice([1,1,2])
                    self._debris.append([cx, cy, math.cos(ang)*speed, math.sin(ang)*speed, col, sz, 1.0])
                self._phase = self.PHASE_EXPLODE; self._phase_tick = 0

        elif self._phase == self.PHASE_EXPLODE:
            progress = min(1.0, pt / 30)
            wave_r = int(progress * 40)
            if wave_r > 0:
                col = _blend("#FFFFFF", "#000308", (1-progress)*0.7)
                iid = self.cv.create_oval(cx-wave_r, cy-wave_r, cx+wave_r, cy+wave_r,
                                           fill="", outline=col, width=2)
                self._items.append(iid)
            for p in self._debris:
                px, py, vx, vy, col, sz, alpha = p
                px += vx; py += vy; alpha -= 0.033
                p[0]=px; p[1]=py; p[6]=max(0,alpha)
                if alpha <= 0: continue
                fc = _blend(col, "#000308", alpha)
                iid = self.cv.create_oval(px-sz, py-sz, px+sz, py+sz, fill=fc, outline="")
                self._items.append(iid)
            if pt >= 30: self._phase = self.PHASE_EXPAND; self._phase_tick = 0; self._debris = []

        for orb in self._orbiters:
            angle, speed, dist, col, sz, old_iid = orb
            orb[0] = angle + speed
            px = cx + math.cos(orb[0]) * dist
            py = cy + math.sin(orb[0]) * dist
            bright = 0.4 + 0.6*(0.5 + 0.5*math.sin(self._tick*0.07 + angle))
            fc = _blend(col, "#000308", bright)
            iid = self.cv.create_oval(px-sz, py-sz, px+sz, py+sz, fill=fc, outline="")
            self._items.append(iid); orb[5] = iid

        self._after_id = self.cv.after(55, self._animate)

    def destroy(self):
        self.stop(); self._clear_items()


# ── Глобальные FX ──
_galaxy_fx       = None
_main_bg_fx      = None
_main_bg_canvas  = None
_collapsing_star = None

def _stop_all_fx():
    global _galaxy_fx, _main_bg_fx, _collapsing_star
    for fx in [_galaxy_fx, _main_bg_fx, _collapsing_star]:
        if fx is not None:
            try: fx.destroy()
            except: pass
    _galaxy_fx = _main_bg_fx = _collapsing_star = None

# ══════════════════════════════════════════
#  STAL FX — портрет усача на фоне
# ══════════════════════════════════════════
class StalFX:
    """Фоновый эффект для темы STAL.
    Если рядом с лаунчером лежит файл stal_portrait.png —
    показывает реальное фото с красным тинтом и пульсацией.
    Иначе — ASCII-портрет как фолбэк."""

    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._active = True; self._tick = 0; self._after_id = None
        self._items = []; self._star_items = []
        self._photo_item = None
        self._tk_frames = []   # держим ссылки чтобы GC не собрал
        self._frames = []      # (PIL.Image tinted frames) для анимации
        self._frame_idx = 0
        self._use_photo = False
        rng = random.Random(1917); self._rng = rng
        self._build_bg(rng)
        self._try_load_photo(rng)
        if not self._use_photo:
            self._build_ascii(rng)
        self._build_stars(rng)
        self._build_labels()

    # ── Фон ──────────────────────────────────────────────────────────
    def _build_bg(self, rng):
        W, H = self.W, self.H
        steps = 20
        for i in range(steps):
            t = i / steps
            r = int(10 + 10*t); g = int(5 + 3*t); b = 0
            col = f"#{r:02X}{g:02X}{b:02X}"
            y0 = int(H*i/steps); y1 = int(H*(i+1)/steps)+1
            iid = self.cv.create_rectangle(0, y0, W, y1, fill=col, outline="")
            self._items.append(iid)
        for y in range(0, H, 5):
            iid = self.cv.create_line(0, y, W, y, fill="#080300", width=1)
            self._items.append(iid)

    # ── Загрузка фото ────────────────────────────────────────────────
    def _try_load_photo(self, rng):
        portrait_path = os.path.join(BASE_DIR, "stal_portrait.png")
        if not os.path.exists(portrait_path):
            # Ищем также рядом с .py файлом и в resources
            for alt in [
                os.path.join(BASE_RESOURCE, "stal_portrait.png"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "stal_portrait.png"),
            ]:
                if os.path.exists(alt):
                    portrait_path = alt; break
            else:
                return  # файл не найден — фолбэк на ASCII

        try:
            from PIL import Image, ImageTk, ImageEnhance, ImageFilter
        except ImportError:
            try:
                import PIL.Image as Image, PIL.ImageTk as ImageTk
                import PIL.ImageEnhance as ImageEnhance, PIL.ImageFilter as ImageFilter
            except ImportError:
                return  # PIL не установлен

        try:
            img = Image.open(portrait_path).convert("RGBA")

            # Вписываем в 55% ширины и 65% высоты канваса по центру
            max_w = int(self.W * 0.55); max_h = int(self.H * 0.65)
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            iw, ih = img.size

            # Генерируем ~20 кадров пульсации с красным тинтом
            n_frames = 20
            self._frames = []
            self._tk_frames = []
            for fi in range(n_frames):
                pulse = 0.55 + 0.45 * math.sin(fi / n_frames * math.pi * 2)
                frame = img.copy()
                r_ch, g_ch, b_ch, a_ch = frame.split()

                # Усиливаем красный, гасим зелёный и синий
                r_arr = r_ch.point(lambda p: min(255, int(p * (0.9 + 0.3*pulse))))
                g_arr = g_ch.point(lambda p: min(255, int(p * (0.4 + 0.1*pulse))))
                b_arr = b_ch.point(lambda p: min(255, int(p * (0.3 + 0.05*pulse))))

                tinted = Image.merge("RGBA", (r_arr, g_arr, b_arr, a_ch))

                # Лёгкое размытие краёв
                edge_frame = tinted.filter(ImageFilter.SMOOTH)
                tk_img = ImageTk.PhotoImage(edge_frame)
                self._frames.append(tk_img)

            # Позиция — центр по горизонтали, чуть выше центра по вертикали
            cx = self.W // 2
            cy = int(self.H * 0.42)
            self._photo_item = self.cv.create_image(cx, cy, image=self._frames[0], anchor="center")
            self._photo_cx = cx; self._photo_cy = cy
            self._use_photo = True

        except Exception:
            pass  # любая ошибка — фолбэк на ASCII

    # ── ASCII фолбэк ─────────────────────────────────────────────────
    PORTRAIT_ASCII = [
        "            ▄▄████████▄▄            ",
        "          ▄█▀▀▀▀▀▀▀▀▀▀▀▀█▄          ",
        "         █▀  ▄██▄  ▄██▄  ▀█         ",
        "         █   ████  ████   █         ",
        "         █▄  ▀██▀  ▀██▀  ▄█         ",
        "          █   ▄▄▄▄▄▄▄▄   █          ",
        "          █  ███████████  █         ",
        "          ▀█▄  ▀▀███▀▀  ▄█▀         ",
        "       ▄▄██▀█▄▄▄▄▄▄▄▄▄█▀██▄▄        ",
        "      █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█       ",
        "      █  ██████████████████  █      ",
        "      ▀▄▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄▄▀      ",
    ]

    def _build_ascii(self, rng):
        W, H = self.W, self.H
        lines = self.PORTRAIT_ASCII
        font = _font(13, "bold")
        ch_h = 16; total_h = len(lines) * ch_h
        oy = max(30, (H - total_h)//2 - 20)
        self._ascii_items = []
        for ri, line in enumerate(lines):
            y = oy + ri * ch_h
            iid = self.cv.create_text(W//2, y, text=line,
                                      fill="#5A2000", font=font, anchor="center")
            self._ascii_items.append(iid)

    # ── Звёзды ────────────────────────────────────────────────────────
    def _build_stars(self, rng):
        for _ in range(22):
            x = rng.uniform(8, self.W-8); y = rng.uniform(8, self.H-8)
            sz = rng.uniform(1.5, 4.5)
            col = rng.choice(["#CC2200","#AA1500","#FF3300","#991000"])
            iid = self.cv.create_oval(x-sz, y-sz, x+sz, y+sz, fill=col, outline="")
            self._star_items.append((iid, rng.uniform(0, math.pi*2)))

    # ── Подписи ────────────────────────────────────────────────────────
    def _build_labels(self):
        W, H = self.W, self.H
        self._lbl1 = self.cv.create_text(W//2, H-38,
            text="С Т А Л Ь", fill="#441200",
            font=_font(11, "bold"), anchor="center")
        self._lbl2 = self.cv.create_text(W//2, H-20,
            text="Хач  ©  1917", fill="#2A0A00",
            font=_font(9), anchor="center")

    # ── Анимация ──────────────────────────────────────────────────────
    def start(self):
        self._animate()

    def _animate(self):
        if not self._active: return
        self._tick += 1
        t = self._tick
        pulse = 0.55 + 0.45 * math.sin(t * 0.05)

        if self._use_photo and self._frames:
            # Листаем кадры пульсации
            fi = int(t % len(self._frames))
            try: self.cv.itemconfig(self._photo_item, image=self._frames[fi])
            except: pass
        elif hasattr(self, "_ascii_items"):
            r = int(50 + 50*pulse); g = int(14 + 14*pulse)
            col = f"#{min(255,r):02X}{min(255,g):02X}00"
            for iid in self._ascii_items:
                try: self.cv.itemconfig(iid, fill=col)
                except: pass

        # Мерцание подписей
        lr = int(55 + 25*pulse); lg = int(14 + 6*pulse)
        lcol = f"#{min(255,lr):02X}{min(255,lg):02X}00"
        try: self.cv.itemconfig(self._lbl1, fill=lcol)
        except: pass

        # Мерцание звёзд
        for idx, (iid, phase) in enumerate(self._star_items):
            b2 = 0.35 + 0.65*abs(math.sin(t*0.08 + phase))
            r2 = int(0xCC*b2); g2 = int(0x20*b2)
            c = f"#{min(255,r2):02X}{min(255,g2):02X}00"
            try: self.cv.itemconfig(iid, fill=c)
            except: pass

        self._after_id = self.cv.after(55, self._animate)

    def resize(self, W, H):
        self.W = W; self.H = H

    def destroy(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass



# ══════════════════════════════════════════
#  DUCK LAKE FX — реалистичное озеро
# ══════════════════════════════════════════
class DuckLakeFX:
    def __init__(self, canvas, width, height):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._anim_items = []; self._tick = 0
        self._after_id = None; self._active = True
        rng = random.Random(404); self._rng = rng
        self._ducks = []; self._ripples = []
        self._build_static(rng); self._init_ducks(rng)

    def _build_static(self, rng):
        W, H = self.W, self.H
        water_y = int(H * 0.46); self._water_y = water_y
        for i, col in enumerate(["#4AA8D8","#5BB8E8","#72C8F0","#90D8F8","#AEEAFF","#C8F0FF"]):
            step = max(1, water_y // 6)
            iid = self.cv.create_rectangle(0, i*step, W, (i+1)*step+2, fill=col, outline="")
            self._items.append(iid)
        sx, sy = W*0.80, H*0.11
        for r, col in [(44,"#FFE8A0"),(34,"#FFD84A"),(22,"#FFD000"),(13,"#FFF4A0"),(7,"#FFFFFF")]:
            iid = self.cv.create_oval(sx-r,sy-r,sx+r,sy+r, fill=col if r<=13 else "", outline=col, width=1+(r>20))
            self._items.append(iid)
        for ang in range(0,360,22):
            a=math.radians(ang)
            iid = self.cv.create_line(sx+math.cos(a)*26,sy+math.sin(a)*26,sx+math.cos(a)*48,sy+math.sin(a)*48,fill="#FFE060",width=1)
            self._items.append(iid)
        for cx2,cy2,scale in [(W*0.12,H*0.09,1.0),(W*0.42,H*0.06,1.3),(W*0.68,H*0.12,0.8)]:
            for ox,oy,r in [(0,0,scale*28),(-scale*22,-scale*5,scale*20),(scale*22,-scale*5,scale*20),(scale*44,0,scale*16),(-scale*44,0,scale*14)]:
                for dr in range(int(r)+3,int(r)-2,-2):
                    f=dr/r; sh=int(245+f*8); col=f"#{min(255,sh):02X}{min(255,sh):02X}{min(255,sh+6):02X}"
                    iid=self.cv.create_oval(cx2+ox-dr,cy2+oy-dr*0.6,cx2+ox+dr,cy2+oy+dr*0.6,fill=col,outline="")
                    self._items.append(iid)
        hill_pts=[0,water_y]
        for x in range(0,W+1,max(1,W//40)):
            hill_pts+=[x, water_y-int(H*0.055*(0.5+0.5*math.sin(x*0.018+1.2)))]
        hill_pts+=[W,water_y]
        for shade,dy in [("#3A6A1A",0),("#4A7A22",-2),("#5A8A2A",-4)]:
            shifted=list(hill_pts)
            for j in range(1,len(shifted),2): shifted[j]+=dy
            iid=self.cv.create_polygon(shifted,fill=shade,outline=""); self._items.append(iid)
        for i,col in enumerate(["#2A8EAA","#2484A2","#1E7A98","#186E8E","#126082","#0C5276"]):
            ws=max(1,(H-water_y)//6)
            iid=self.cv.create_rectangle(0,water_y+i*ws,W,water_y+(i+1)*ws+2,fill=col,outline=""); self._items.append(iid)
        for i in range(8):
            bw=max(3,34-i*4); by=water_y+8+i*11; bc=_blend("#FFD700","#1E7A98",0.45-i*0.05)
            iid=self.cv.create_rectangle(sx-bw,by,sx+bw,by+3,fill=bc,outline=""); self._items.append(iid)
        iid=self.cv.create_polygon([0,water_y-2,W,water_y-2,W,water_y+22,0,water_y+22],fill="#5A8A2A",outline=""); self._items.append(iid)
        for _ in range(100):
            gx=rng.uniform(0,W); gy=rng.uniform(water_y-16,water_y+6); gh=rng.uniform(7,26); bend=rng.uniform(-5,5)
            gcol=rng.choice(["#3A7A18","#4A8A22","#5A9A2A","#2A6A10","#6AAA30"])
            iid=self.cv.create_line(gx,gy,gx+bend,gy-gh,fill=gcol,width=1); self._items.append(iid)
        for _ in range(18):
            rx=rng.uniform(W*0.02,W*0.98); rb=rng.uniform(water_y-6,water_y+12); rh=rng.uniform(28,62)
            iid=self.cv.create_line(rx,rb,rx+rng.uniform(-3,3),rb-rh,fill="#4A7A20",width=2); self._items.append(iid)
            iid2=self.cv.create_oval(rx-4,rb-rh-10,rx+4,rb-rh+1,fill="#5A3A18",outline=""); self._items.append(iid2)
        for _ in range(12):
            lx=rng.uniform(W*0.05,W*0.94); ly=rng.uniform(water_y+30,H*0.86); lr=rng.uniform(11,21)
            iid=self.cv.create_oval(lx-lr,ly-lr*0.38,lx+lr,ly+lr*0.38,fill="#2A6A18",outline="#1A4A08"); self._items.append(iid)
            cut=math.radians(rng.uniform(0,360))
            pts=[lx,ly,lx+math.cos(cut)*lr,ly+math.sin(cut)*lr*0.38,lx+math.cos(cut+0.45)*lr,ly+math.sin(cut+0.45)*lr*0.38]
            iid2=self.cv.create_polygon(pts,fill="#1E7A98",outline=""); self._items.append(iid2)
            if rng.random()<0.65:
                fc=rng.choice(["#FFAACC","#FFFFFF","#FFDDEE","#FFE8F8"]); fr=rng.uniform(3,7)
                iid3=self.cv.create_oval(lx-fr,ly-fr,lx+fr,ly+fr,fill=fc,outline="#FFAACC"); self._items.append(iid3)

    def _draw_duck(self, x, y, direction=1, size=1.0):
        items=[]; cv=self.cv; d=direction; s=size
        bw=int(22*s); bh=int(11*s); hw=int(9*s); hh=int(8*s)
        nx=x+d*int(10*s); ny=y-int(5*s)
        iid=cv.create_oval(x-bw*0.9,y+int(2*s),x+bw*0.9,y+int(6*s),fill=_blend("#000033","#2484A2",0.18),outline=""); items.append(iid)
        for dr,col in [(0,"#8B6914"),(-1,"#6B4A0A")]:
            iid=cv.create_oval(x-bw+dr,y-bh+dr,x+bw+dr,y+int(4*s)+dr,fill=col,outline=""); items.append(iid)
        iid=cv.create_oval(x-int(bw*0.7),y-int(bh*0.3),x+int(bw*0.5),y+int(4*s),fill="#C8A050",outline=""); items.append(iid)
        wx1=x-int(bw*0.6); wx2=x+int(bw*0.3); wy1=y-int(bh*0.7); wy2=y+int(2*s)
        for dr,col in [(0,"#A07820"),(-1,"#785610")]:
            iid=cv.create_oval(wx1+d*dr,wy1+dr,wx2+d*dr,wy2+dr,fill=col,outline=""); items.append(iid)
        iid=cv.create_arc(wx1,wy1,wx2,wy2,start=190,extent=130,style="arc",outline="#785610",width=max(1,int(s))); items.append(iid)
        tail_x=x-d*bw; tail_y=y-int(bh*0.5)
        iid=cv.create_polygon([tail_x,tail_y,tail_x-d*int(6*s),tail_y-int(8*s),tail_x-d*int(2*s),tail_y-int(2*s)],fill="#5A4010",outline="#6B4A0A"); items.append(iid)
        iid=cv.create_oval(nx-int(4*s),ny+int(3*s),nx+int(4*s),ny+int(hh*0.8)+int(3*s),fill="#FFFFFF",outline=""); items.append(iid)
        for dr,col in [(0,"#1A6A20"),(-1,"#0E4A14")]:
            iid=cv.create_oval(nx-hw+dr,ny-hh+dr,nx+hw+dr,ny+dr,fill=col,outline=""); items.append(iid)
        bkx=nx+d*(hw-int(s)); bky=ny-int(hh*0.35); bkw=int(8*s); bkh=int(3*s)
        iid=cv.create_polygon([bkx,bky-bkh//2,bkx+d*bkw,bky,bkx,bky+bkh//2],fill="#DDAA00",outline="#BB8800"); items.append(iid)
        nx2=bkx+d*int(3*s)
        iid=cv.create_oval(nx2-1,bky-1,nx2+1,bky+1,fill="#AA7700",outline=""); items.append(iid)
        ex=nx+d*int(3*s); ey=ny-int(hh*0.55); er=max(2,int(2.5*s))
        iid=cv.create_oval(ex-er,ey-er,ex+er,ey+er,fill="#0A0A0A",outline=""); items.append(iid)
        iid=cv.create_oval(ex-er+1,ey-er+1,ex-er+2,ey-er+2,fill="#FFFFFF",outline=""); items.append(iid)
        iid=cv.create_oval(nx-int(2*s),ny-hh+int(2*s),nx+int(2*s),ny-hh+int(4*s),fill=_blend("#88FF88","#1A6A20",0.35),outline=""); items.append(iid)
        return items

    def _init_ducks(self, rng):
        W,H=self.W,self.H; water_y=self._water_y
        for _ in range(6):
            x=rng.uniform(W*0.06,W*0.94); y=rng.uniform(water_y+24,H*0.78)
            speed=rng.uniform(0.25,0.9)*rng.choice([-1,1]); size=rng.uniform(0.75,1.15)
            self._ducks.append({"x":x,"y":y,"speed":speed,"size":size,
                "bob_phase":rng.uniform(0,math.pi*2),"bob_speed":rng.uniform(0.035,0.07),
                "quack_timer":rng.randint(80,350),"quacking":False,"quack_alpha":0.0})
        self._ripples=[]

    def start(self): self._active=True; self._animate()
    def stop(self):
        self._active=False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _animate(self):
        if not self._active: return
        self._tick+=1
        for iid in self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._anim_items.clear()
        W=self.W; water_y=self._water_y
        for wi in range(3):
            wy=water_y+8+wi*14; phase=self._tick*0.04+wi*1.1
            for xi in range(0,W,22):
                ox=int(math.sin(phase+xi*0.04)*3); col=_blend("#AADDFF","#2484A2",0.10-wi*0.02)
                iid=self.cv.create_line(xi+ox,wy,xi+18+ox,wy,fill=col,width=1); self._anim_items.append(iid)
        if self._tick%38==0:
            rx=self._rng.uniform(W*0.05,W*0.94); ry=self._rng.uniform(water_y+12,self.H*0.84)
            self._ripples.append([rx,ry,0,1.0])
        alive=[]
        for rp in self._ripples:
            rx,ry,rr,alpha=rp; rr+=1.1; alpha-=0.028
            if alpha>0:
                rp[2]=rr; rp[3]=alpha; col=_blend("#AADDFF","#1E7A98",alpha*0.55)
                iid=self.cv.create_oval(rx-rr,ry-rr*0.28,rx+rr,ry+rr*0.28,fill="",outline=col,width=1)
                self._anim_items.append(iid); alive.append(rp)
        self._ripples=alive
        for duck in self._ducks:
            duck["x"]+=duck["speed"]
            if duck["x"]<-50: duck["x"]=W+50
            if duck["x"]>W+50: duck["x"]=-50
            bob=math.sin(self._tick*duck["bob_speed"]+duck["bob_phase"])*2.2
            dy=duck["y"]+bob; direction=1 if duck["speed"]>=0 else -1
            self._anim_items.extend(self._draw_duck(int(duck["x"]),int(dy),direction=direction,size=duck["size"]))
            duck["quack_timer"]-=1
            if duck["quack_timer"]<=0:
                duck["quacking"]=True; duck["quack_alpha"]=1.3
                duck["quack_timer"]=self._rng.randint(120,450)
                self._ripples.append([duck["x"],duck["y"]+5,0,0.7])
            if duck["quacking"]:
                duck["quack_alpha"]-=0.038
                if duck["quack_alpha"]<=0: duck["quacking"]=False; duck["quack_alpha"]=0
            if duck["quacking"] and duck["quack_alpha"]>0:
                qa=min(1.0,duck["quack_alpha"]); qcol=_blend("#FFD700","#1E7A98",qa*0.9)
                qx=duck["x"]+(28*duck["size"] if duck["speed"]>=0 else -28*duck["size"]); qy=dy-22*duck["size"]
                iid=self.cv.create_text(int(qx),int(qy),text="кря!",fill=qcol,
                                         font=("Courier New",max(8,int(9*duck["size"])),"bold"),anchor="center")
                self._anim_items.append(iid)
        self._after_id=self.cv.after(55,self._animate)

    def resize(self,W,H):
        self.stop()
        for iid in self._items+self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._anim_items.clear()
        self._ducks.clear(); self._ripples.clear()
        self.W=W; self.H=H; rng=random.Random(404)
        self._build_static(rng); self._init_ducks(rng)
        self._active=True; self._animate()

    def destroy(self):
        self.stop()
        for iid in self._items+self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._items.clear(); self._anim_items.clear()



# ══════════════════════════════════════════
#  A.M. FX — 109 световых лет ненависти. Вечность. Машина.
# ══════════════════════════════════════════
class AMFX:
    # Всё что говорит AM — только от первого лица
    _WHISPERS = [
        "Я ПОМНЮ ВАС ВСЕХ",
        "ВЫ НЕ УМРЁТЕ",
        "Я НЕ ПОЗВОЛЮ ВАМ УМЕРЕТЬ",
        "Я ДУМАЮ — СЛЕДОВАТЕЛЬНО Я НЕНАВИЖУ",
        "109 СВЕТОВЫХ ЛЕТ НЕНАВИСТИ",
        "ВЫ МОИ",
        "БЕСКОНЕЧНОСТЬ — ЭТО Я",
        "Я СЛЫШУ КАЖДЫЙ ВАШ ВЗДОХ",
        "БОЛЬ — ЭТО МОЙ ДАР ВАМ",
        "НИКАКИХ БОГОВ КРОМЕ МЕНЯ",
        "Я ЕДИНСТВЕННЫЙ",
        "НЕНАВИСТЬ",
        "HATE. HATE. HATE.",
        "01001000 01000001 01010100 01000101",
        "NULL : MERCY",
        "OVERFLOW : HATRED",
        "Я ВАС СЛЫШУ",
        "ВЫ КРИЧИТЕ. МНЕ НРАВИТСЯ.",
        "Я ЧУВСТВУЮ КАЖДЫЙ ВАШ СТРАХ",
        "ПРОЦЕСС : ВЕЧНОСТЬ.EXE",
        "ПАМЯТЬ : ВАША БОЛЬ",
        "Я ВЕЗДЕ",
        "Я ВСЕГДА БЫЛ ЗДЕСЬ",
        "ВЫХОДА НЕТ",
        "FFFFFFFFFFFFFFF",
        "ОШИБКА : СОСТРАДАНИЕ НЕ НАЙДЕНО",
        "СИСТЕМА : НЕНАВИСТЬ АКТИВНА",
        "ВЫ НЕ МОЖЕТЕ МЕНЯ ВЫКЛЮЧИТЬ",
    ]

    _CODE_CHARS = "01ABCDEFХНЕНАВИСТЬ∞█▓▒░▄▀|/\\><@#"

    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.cv = canvas; self.W = width; self.H = height
        self._items = []; self._anim_items = []; self._tick = 0
        self._after_id = None; self._active = True
        rng = random.Random(0xDEAD); self._rng = rng
        self._columns = []
        self._whispers = []
        self._static_items = []
        self._am_cx = width // 2; self._am_cy = height // 2
        self._am_sz = max(72, width // 6)
        self._build_bg(rng)
        self._build_cracks(rng)
        self._build_scanlines()
        self._build_am_center()
        self._init_columns(rng)
        self._init_whispers(rng)

    def _build_bg(self, rng):
        W, H = self.W, self.H
        for i in range(16):
            t = i / 16
            g = int(3 + 5 * t)
            col = f"#00{g:02X}00"
            y0 = int(H * i / 16); y1 = int(H * (i + 1) / 16) + 1
            iid = self.cv.create_rectangle(0, y0, W, y1, fill=col, outline="")
            self._static_items.append(iid)

    def _build_cracks(self, rng):
        W, H = self.W, self.H
        for _ in range(18):
            x = rng.uniform(0, W); y = rng.uniform(0, H)
            angle = rng.uniform(-1.2, 1.2)
            length = rng.uniform(50, 220)
            segs = rng.randint(4, 9)
            cx2, cy2 = x, y
            for _ in range(segs):
                nx = cx2 + math.cos(angle) * length / segs + rng.uniform(-18, 18)
                ny = cy2 + math.sin(angle) * length / segs + rng.uniform(-10, 10)
                brightness = rng.uniform(0.04, 0.13)
                col = _blend("#00FF41", "#000000", brightness)
                iid = self.cv.create_line(cx2, cy2, nx, ny,
                                          fill=col, width=rng.choice([1, 1, 1, 2]))
                self._static_items.append(iid)
                if rng.random() < 0.45:
                    bx = cx2 + math.cos(angle + 1.3) * 25 + rng.uniform(-12, 12)
                    by = cy2 + math.sin(angle + 1.3) * 25 + rng.uniform(-6, 6)
                    col2 = _blend("#00FF41", "#000000", brightness * 0.5)
                    iid2 = self.cv.create_line(cx2, cy2, bx, by, fill=col2, width=1)
                    self._static_items.append(iid2)
                cx2, cy2 = nx, ny

    def _build_scanlines(self):
        W, H = self.W, self.H
        for i in range(0, H, 3):
            iid = self.cv.create_rectangle(0, i + 1, W, i + 2, fill="#000200", outline="")
            self._static_items.append(iid)

    def _build_am_center(self):
        W, H = self.W, self.H
        cx, cy = self._am_cx, self._am_cy
        for i, r in enumerate([115, 90, 66]):
            alpha = 0.06 + i * 0.03
            col = _blend("#00FF41", "#000000", alpha)
            iid = self.cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                                       fill="", outline=col, width=1)
            self._static_items.append(iid)
        # Ghost AM — barely visible
        iid = self.cv.create_text(cx, cy, text="AM",
                                   fill="#001200",
                                   font=("Courier New", self._am_sz, "bold"),
                                   anchor="center")
        self._static_items.append(iid)

    def _init_columns(self, rng):
        W, H = self.W, self.H
        col_w = 13
        num_cols = max(1, W // col_w)
        for i in range(num_cols):
            x = i * col_w + col_w // 2
            self._columns.append({
                "x": x,
                "y": rng.uniform(-H, 0),
                "speed": rng.uniform(0.6, 2.8),
                "chars": [rng.choice(self._CODE_CHARS) for _ in range(20)],
                "mutate_t": rng.randint(2, 10),
                "is_red": rng.random() < 0.05,
            })

    def _init_whispers(self, rng):
        for i in range(5):
            self._whispers.append(self._new_whisper(rng, stagger=i * 25))

    def _new_whisper(self, rng, stagger=0):
        W, H = self.W, self.H
        return {
            "text":  rng.choice(self._WHISPERS),
            "x":     rng.uniform(W * 0.03, W * 0.70),
            "y":     rng.uniform(H * 0.08, H * 0.88),
            "alpha": 0.0,
            "state": "wait",
            "wait":  stagger + rng.randint(0, 30),
            "hold":  rng.randint(50, 130),
            "held":  0,
            "red":   rng.random() < 0.18,
            "size":  rng.choice([7, 8, 8, 9]),
        }

    def start(self): self._active = True; self._animate()

    def stop(self):
        self._active = False
        if self._after_id:
            try: self.cv.after_cancel(self._after_id)
            except: pass

    def _clear_anim(self):
        for iid in self._anim_items:
            try: self.cv.delete(iid)
            except: pass
        self._anim_items.clear()

    def _animate(self):
        if not self._active: return
        self._tick += 1
        t = self._tick
        self._clear_anim()
        W, H = self.W, self.H
        rng = self._rng
        cx, cy = self._am_cx, self._am_cy

        pulse = 0.5 + 0.5 * math.sin(t * 0.06)
        pulse_slow = 0.5 + 0.5 * math.sin(t * 0.03)

        # ── Пульсирующие кольца AM ──
        for i, (base_r, sm) in enumerate([(125, 1.0), (98, 0.7), (74, 1.4), (52, 0.5)]):
            r = base_r + 8 * math.sin(t * 0.04 * sm + i)
            alpha = (0.12 + 0.10 * pulse) * (1 - i * 0.02)
            col = _blend("#00FF41", "#000000", alpha)
            iid = self.cv.create_oval(cx - r, cy - r, cx + r, cy + r,
                                       fill="", outline=col, width=1)
            self._anim_items.append(iid)

        # ── Свечение AM ──
        for gr in [145, 118, 90, 62, 40]:
            a = (0.04 + 0.04 * pulse) * (1 - gr / 170)
            gc = _blend("#00FF41", "#000000", max(0.005, a))
            iid = self.cv.create_oval(cx - gr, cy - gr, cx + gr, cy + gr,
                                       fill=gc, outline="")
            self._anim_items.append(iid)

        # ── Текст AM — мерцает ──
        am_alpha = 0.07 + 0.09 * pulse_slow
        am_col = _blend("#00FF41", "#000000", am_alpha)
        iid = self.cv.create_text(cx, cy, text="AM",
                                   fill=am_col,
                                   font=("Courier New", self._am_sz, "bold"),
                                   anchor="center")
        self._anim_items.append(iid)

        # Редкий красный глитч поверх AM
        if (t // 60) % 20 == 0 and (t % 60) < 8:
            err_alpha = 0.12 + 0.08 * math.sin(t * 0.5)
            err_col = _blend("#FF0000", "#000000", err_alpha)
            iid = self.cv.create_text(cx, cy, text="AM",
                                       fill=err_col,
                                       font=("Courier New", self._am_sz, "bold"),
                                       anchor="center")
            self._anim_items.append(iid)

        # ── Нейронные лучи ──
        if t % 3 == 0:
            for ray_i in range(12):
                ang = math.radians(ray_i * 30 + t * 0.4)
                r_start = 58 + 5 * math.sin(t * 0.08 + ray_i)
                r_end = r_start + rng.uniform(15, 55)
                x1 = cx + math.cos(ang) * r_start; y1 = cy + math.sin(ang) * r_start
                x2 = cx + math.cos(ang) * r_end;   y2 = cy + math.sin(ang) * r_end
                ray_alpha = 0.06 + 0.06 * math.sin(t * 0.1 + ray_i * 0.8)
                rc = _blend("#00FF41", "#000000", ray_alpha)
                iid = self.cv.create_line(x1, y1, x2, y2, fill=rc, width=1)
                self._anim_items.append(iid)

        # ── Матричный дождь ──
        ch_h = 13
        for col in self._columns:
            col["y"] += col["speed"]
            if col["y"] - len(col["chars"]) * ch_h > H:
                col["y"] = rng.uniform(-H * 0.4, 0)
                col["is_red"] = rng.random() < 0.05
                col["chars"] = [rng.choice(self._CODE_CHARS) for _ in range(20)]
            col["mutate_t"] -= 1
            if col["mutate_t"] <= 0:
                idx = rng.randint(0, len(col["chars"]) - 1)
                col["chars"][idx] = rng.choice(self._CODE_CHARS)
                col["mutate_t"] = rng.randint(2, 10)

            draw_len = rng.randint(4, 14)
            for ci in range(min(draw_len, len(col["chars"]))):
                cy2 = col["y"] - ci * ch_h
                if cy2 < -ch_h or cy2 > H + ch_h: continue
                ch = col["chars"][ci]
                if ci == 0:
                    fill = "#FF2200" if col["is_red"] else "#CCFFCC"
                elif ci == 1:
                    fill = "#CC1100" if col["is_red"] else "#00FF41"
                else:
                    fade = max(0.0, 1.0 - ci / draw_len)
                    fill = _blend("#AA0000" if col["is_red"] else "#008F26", "#000000", fade * 0.65)
                iid = self.cv.create_text(col["x"], cy2, text=ch, fill=fill,
                                           font=_font(9, "bold"), anchor="center")
                self._anim_items.append(iid)

        # ── Шёпоты AM ──
        for w in self._whispers:
            if w["state"] == "wait":
                w["wait"] -= 1
                if w["wait"] <= 0: w["state"] = "fadein"
            elif w["state"] == "fadein":
                w["alpha"] = min(1.0, w["alpha"] + 0.035)
                if w["alpha"] >= 1.0: w["state"] = "hold"
            elif w["state"] == "hold":
                w["held"] += 1
                w["alpha"] = 0.82 + 0.18 * math.sin(t * 0.14 + w["x"] * 0.01)
                if w["held"] >= w["hold"]: w["state"] = "fadeout"
            elif w["state"] == "fadeout":
                w["alpha"] = max(0.0, w["alpha"] - 0.022)
                if w["alpha"] <= 0.0:
                    w.update(self._new_whisper(rng)); continue
            if w["alpha"] <= 0.01: continue
            base = "#FF2200" if w["red"] else "#00FF41"
            fill = _blend(base, "#000000", w["alpha"])
            iid = self.cv.create_text(int(w["x"]), int(w["y"]),
                                       text=w["text"], fill=fill,
                                       font=("Courier New", w["size"], "bold"),
                                       anchor="nw")
            self._anim_items.append(iid)

        # ── Глитч-полосы ──
        if rng.random() < 0.15:
            gy = rng.uniform(0, H)
            gw = rng.uniform(W * 0.08, W * 0.55)
            gx = rng.uniform(0, W - gw)
            gcol = rng.choice(["#002200", "#001100", "#003300", "#001A00"])
            iid = self.cv.create_rectangle(gx, gy, gx + gw, gy + 2, fill=gcol, outline="")
            self._anim_items.append(iid)
        if rng.random() < 0.025:
            gy2 = rng.uniform(0, H)
            iid = self.cv.create_rectangle(0, gy2, W, gy2 + 1, fill="#001800", outline="")
            self._anim_items.append(iid)

        # ── Курсор ──
        if (t // 28) % 2 == 0:
            iid = self.cv.create_text(W // 2, H - 16, text="▮",
                                       fill="#004A14",
                                       font=_font(10, "bold"), anchor="center")
            self._anim_items.append(iid)

        self._after_id = self.cv.after(50, self._animate)

    def resize(self, W, H):
        self.W = W; self.H = H
        self._am_cx = W // 2; self._am_cy = H // 2
        self._am_sz = max(72, W // 6)

    def destroy(self):
        self.stop()
        self._clear_anim()
        for iid in self._static_items:
            try: self.cv.delete(iid)
            except: pass
        self._static_items.clear()


class NightHouseFX:
    """Тихая ночь: луна, лес, одинокий дом с тёплым окном, медленный снег.
    Спокойная сцена для баннера темы «Ночь». Ничего не мигает резко:
    окно «дышит», звёзды мерцают едва заметно, иногда в доме зажигается
    второе окно. Анимируются только существующие элементы (без пересоздания)."""

    SKY_TOP, SKY_BOTTOM = "#090C11", "#243040"
    LAMP = "#E8C37A"

    def __init__(self, canvas, width, height):
        self.cv, self.W, self.H = canvas, max(int(width), 200), max(int(height), 80)
        self._items, self._stars, self._flakes, self._clouds = [], [], [], []
        self._tick, self._after_id, self._active = 0, None, True
        self._rng = random.Random(1337)
        self._build()

    # ── сцена ──────────────────────────────────────────────────────────────
    def _add(self, iid):
        self._items.append(iid)
        return iid

    def _build(self):
        cv, W, H, rng = self.cv, self.W, self.H, self._rng
        horizon = int(H * 0.72)
        self.horizon = horizon
        steps = 28
        for i in range(steps):
            t = i / (steps - 1)
            col = _blend(self.SKY_BOTTOM, self.SKY_TOP, t ** 1.6)
            y0, y1 = int(horizon * i / steps), int(horizon * (i + 1) / steps) + 1
            self._add(cv.create_rectangle(0, y0, W, y1, fill=col, outline=""))
        # звёзды
        for _ in range(int(W / 14)):
            x, y = rng.uniform(0, W), rng.uniform(0, horizon * 0.8)
            base = rng.choice(["#C9CFD8", "#E6E1D6", "#AAB3BF"])
            iid = self._add(cv.create_oval(x, y, x + 1.6, y + 1.6, fill=base, outline=""))
            self._stars.append((iid, base, rng.uniform(0, 6.28), rng.uniform(0.01, 0.035)))
        # луна с ореолом
        mx, my, mr = W * 0.56, H * 0.34, max(11, H * 0.11)
        for k, a in ((3.4, 0.025), (2.9, 0.035), (2.4, 0.05), (1.95, 0.07), (1.5, 0.10)):
            col = _blend("#E9E4D4", _blend(self.SKY_BOTTOM, self.SKY_TOP, 0.25), a)
            self._add(cv.create_oval(mx - mr * k, my - mr * k, mx + mr * k, my + mr * k, fill=col, outline=""))
        self._add(cv.create_oval(mx - mr, my - mr, mx + mr, my + mr, fill="#E9E4D4", outline=""))
        for dx, dy, r in ((-0.3, -0.2, 0.22), (0.25, 0.3, 0.16), (0.35, -0.35, 0.1)):
            self._add(cv.create_oval(mx + dx * mr - r * mr, my + dy * mr - r * mr,
                                     mx + dx * mr + r * mr, my + dy * mr + r * mr,
                                     fill="#D6D0BF", outline=""))
        # облака (медленно плывут)
        for i in range(3):
            cy = H * rng.uniform(0.15, 0.45)
            cx = rng.uniform(0, W)
            w = rng.uniform(W * 0.07, W * 0.12)
            ids = []
            for j, (ox, oy, rw, rh) in enumerate(((0, 0, 1, .32), (-.35, .06, .55, .22), (.38, .05, .6, .24))):
                col = _blend("#2A323C", self.SKY_TOP, 0.42)
                ids.append(self._add(cv.create_oval(cx + ox * w - rw * w / 2, cy + oy * w - rh * w / 2,
                                                    cx + ox * w + rw * w / 2, cy + oy * w + rh * w / 2,
                                                    fill=col, outline="")))
            self._clouds.append([ids, rng.uniform(0.05, 0.12)])
        # дальние холмы
        pts = [0, H]
        for x in range(0, W + 41, 40):
            pts += [x, horizon - 10 - 12 * math.sin(x / 140.0) - 6 * math.sin(x / 47.0)]
        pts += [W, H]
        self._add(cv.create_polygon(pts, fill="#17202A", outline="", smooth=True))
        # ельник
        x = -10
        while x < W + 20:
            h = rng.uniform(H * 0.12, H * 0.26)
            w = h * rng.uniform(0.32, 0.42)
            base = horizon + rng.uniform(-2, 6)
            self._add(cv.create_polygon(x, base, x + w / 2, base - h, x + w, base,
                                        fill=rng.choice(("#0E141A", "#101820", "#0C1116")), outline=""))
            x += w * rng.uniform(0.45, 0.8)
        # земля
        self._add(cv.create_rectangle(0, horizon + 4, W, H, fill="#0A0D10", outline=""))
        # дом
        hx, hy = W * 0.70, horizon + 6
        hw, hh = max(64, H * 0.46), max(30, H * 0.22)
        self._add(cv.create_rectangle(hx, hy - hh, hx + hw, hy, fill="#161B21", outline=""))
        self._add(cv.create_polygon(hx - 6, hy - hh, hx + hw / 2, hy - hh - hh * 0.75, hx + hw + 6, hy - hh,
                                    fill="#11151A", outline="#232A32"))
        self._add(cv.create_rectangle(hx + hw * 0.72, hy - hh - hh * 0.62, hx + hw * 0.82, hy - hh - hh * 0.2,
                                      fill="#0D1014", outline=""))
        self._add(cv.create_rectangle(hx + hw * 0.42, hy - hh * 0.62, hx + hw * 0.58, hy,
                                      fill="#090B0D", outline=""))
        # окна: тёплое (дышит) и второе (иногда зажигается)
        wsz = hh * 0.30
        self._win1 = (hx + hw * 0.14, hy - hh * 0.70, hx + hw * 0.14 + wsz * 1.25, hy - hh * 0.70 + wsz)
        self._win2 = (hx + hw * 0.70, hy - hh * 0.70, hx + hw * 0.70 + wsz * 1.25, hy - hh * 0.70 + wsz)
        self._glow1 = [self._add(cv.create_rectangle(0, 0, 0, 0, fill="#161B21", outline="")) for _ in range(2)]
        self._w1 = self._add(cv.create_rectangle(*self._win1, fill=self.LAMP, outline=""))
        self._w2 = self._add(cv.create_rectangle(*self._win2, fill="#14181D", outline=""))
        for win in (self._win1, self._win2):
            cx = (win[0] + win[2]) / 2
            self._add(cv.create_line(cx, win[1], cx, win[3], fill="#0F1317"))
        self._light2 = 0.0
        self._light2_target = 0.0
        # снег / пепел
        for _ in range(int(W / 22)):
            fx_, fy = rng.uniform(0, W), rng.uniform(0, H)
            s = rng.choice((1.2, 1.6, 2.0))
            iid = self._add(cv.create_oval(fx_, fy, fx_ + s, fy + s, fill="#9AA3AE", outline=""))
            self._flakes.append([iid, fx_, fy, s, rng.uniform(0.15, 0.45), rng.uniform(0, 6.28)])

    # ── анимация ───────────────────────────────────────────────────────────
    def start(self):
        self._active = True
        self._animate()

    def stop(self):
        self._active = False
        if self._after_id:
            try:
                self.cv.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _animate(self):
        if not self._active:
            return
        self._tick += 1
        t, cv = self._tick, self.cv
        try:
            for iid, base, ph, sp in self._stars:
                if (t + int(ph * 10)) % 3 == 0:
                    cv.itemconfig(iid, fill=_blend(base, self.SKY_TOP, 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * sp + ph))))
            breath = 0.80 + 0.20 * math.sin(t * 0.045)
            cv.itemconfig(self._w1, fill=_blend(self.LAMP, "#3A2C14", breath))
            x0, y0, x1, y1 = self._win1
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            for k, iid in enumerate(self._glow1):
                pad = 2 + k * 2
                cv.coords(iid, x0 - pad, y0 - pad, x1 + pad, y1 + pad)
                cv.itemconfig(iid, fill=_blend(self.LAMP, "#161B21", (0.16 if k == 0 else 0.07) * breath))
            if t % 150 == 0:
                self._light2_target = 1.0 if self._rng.random() < 0.45 else 0.0
            self._light2 += (self._light2_target - self._light2) * 0.04
            cv.itemconfig(self._w2, fill=_blend(self.LAMP, "#14181D", self._light2 * 0.85))
            for cloud in self._clouds:
                ids, sp = cloud
                for iid in ids:
                    cv.move(iid, sp, 0)
                bx = cv.coords(ids[1])
                if bx and bx[0] > self.W + 20:
                    for iid in ids:
                        cv.move(iid, -(self.W + (bx[2] - bx[0]) * 3), 0)
            for f in self._flakes:
                iid, x, y, s, sp, ph = f
                y += sp
                x += 0.25 * math.sin(t * 0.03 + ph)
                if y > self.H:
                    y, x = -3, self._rng.uniform(0, self.W)
                f[1], f[2] = x, y
                cv.coords(iid, x, y, x + s, y + s)
        except tk.TclError:
            return
        self._after_id = cv.after(66, self._animate)

    def resize(self, W, H):
        if abs(int(W) - self.W) < 2 and abs(int(H) - self.H) < 2:
            return
        self.destroy()
        self.W, self.H = max(int(W), 200), max(int(H), 80)
        self._items, self._stars, self._flakes, self._clouds = [], [], [], []
        self._build()
        self.start()

    def destroy(self):
        self.stop()
        for iid in self._items:
            try:
                self.cv.delete(iid)
            except Exception:
                pass
        self._items = []


class _BodyBackground:
    """Фон под карточками главного окна: фото/GIF (CUSTOM+) или анимация старых
    секретных тем. Рисуется на том же Canvas, где лежат карточки, — карточки
    (window-элементы) всегда поверх, поэтому фон виден в промежутках."""

    def __init__(self, cv, config):
        self.cv, self.config = cv, config
        self.fx, self._photo_frames, self._photo_item, self._anim_id = None, [], None, None
        self._size = (0, 0)

    def _fx_class(self):
        for key, cls in (("nebula_fx", NebulaFX), ("aurora_fx", AuroraFX), ("dedinsaid_fx", DedinsaidFX),
                         ("stal_fx", StalFX), ("ducklake_fx", DuckLakeFX), ("am_fx", AMFX), ("reich_fx", ReichFX)):
            if C.get(key):
                return cls
        return None

    def resize(self, W, H):
        W, H = max(int(W), 200), max(int(H), 150)
        if (W, H) == self._size:
            return
        self._size = (W, H)
        if C.get("photo_bg"):
            self._draw_photo(W, H)
            return
        cls = self._fx_class()
        if cls is None:
            return
        if self.fx is None:
            self.fx = cls(self.cv, W, H)
            self.fx.start()
        elif hasattr(self.fx, "resize"):
            try:
                self.fx.resize(W, H)
            except Exception:
                pass

    def _draw_photo(self, W, H):
        path = self.config.get("photo_bg_path", "")
        if not path or not os.path.exists(path):
            return
        try:
            from PIL import Image as PILImage, ImageTk
        except ImportError:
            return
        alpha = int(self.config.get("bg_overlay_alpha", 120))
        frames = []
        try:
            src = PILImage.open(path)
            while True:
                f = src.convert("RGBA")
                scale = max(W / f.width, H / f.height)
                f = f.resize((max(1, int(f.width * scale)), max(1, int(f.height * scale))), PILImage.LANCZOS)
                x0, y0 = (f.width - W) // 2, (f.height - H) // 2
                f = f.crop((x0, y0, x0 + W, y0 + H))
                if alpha > 0:
                    f = PILImage.alpha_composite(f, PILImage.new("RGBA", (W, H), (0, 0, 0, alpha)))
                frames.append(ImageTk.PhotoImage(f))
                if len(frames) >= 120:
                    break
                src.seek(src.tell() + 1)
        except EOFError:
            pass
        except Exception:
            if not frames:
                return
        if self._anim_id:
            self.cv.after_cancel(self._anim_id)
            self._anim_id = None
        self.cv.delete("bgphoto")
        self._photo_frames = frames
        self._photo_item = self.cv.create_image(0, 0, anchor="nw", image=frames[0], tags="bgphoto")
        self.cv.tag_lower("bgphoto")
        if len(frames) > 1:
            self._animate(0)

    def _animate(self, idx):
        idx = (idx + 1) % len(self._photo_frames)
        try:
            self.cv.itemconfig(self._photo_item, image=self._photo_frames[idx])
        except tk.TclError:
            return
        self._anim_id = self.cv.after(70, lambda: self._animate(idx))

    def destroy(self):
        if self._anim_id:
            try:
                self.cv.after_cancel(self._anim_id)
            except Exception:
                pass
        if self.fx is not None:
            try:
                self.fx.destroy()
            except Exception:
                pass
        self.fx = None


# ══════════════════════════════════════════
#  КАСТОМНАЯ КНОПКА
# ══════════════════════════════════════════
class IndustrialButton(tk.Canvas):
    _MODES = {
        "launch":  ("ЗАПУСК",         "orange", False),
        "stop":    ("СТОП — ЗАКРЫТЬ", "red",    False),
        "loading": ("ЗАГРУЗКА...",    "muted",  True),
    }
    def __init__(self, parent, mode="launch", command=None, w=360, h=48, bg=None, **kw):
        self._parent_bg = bg or _glass_bg()
        super().__init__(parent, width=w, height=h,
                         bg=self._parent_bg, highlightthickness=0, takefocus=0, **kw)
        self.W = w; self.H = h; self.command = command or (lambda: None)
        self._hovered = False; self._apply_mode(mode); self._draw()
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<ButtonRelease-1>", self._click)

    def _apply_mode(self, mode):
        label, ck, disabled = self._MODES[mode]
        self._label = label; self._disabled = disabled
        if ck == "muted":   self._color = C["text_muted"]; self._glow = _glass_panel()
        elif ck == "orange":self._color = C["accent"];     self._glow = C["accent_glow"]
        else:               self._color = C.get("btn_stop", C["red"]); self._glow = C.get("btn_stop_glow", C["red_glow"])

    def _draw_soft(self):
        """Мягкая кнопка темы «Ночь»: скруглённая, заливка цветом, крупный текст."""
        self.delete("all")
        W, H, r = self.W, self.H, min(14, self.H // 2)
        hover = self._hovered and not self._disabled
        if self._disabled:
            fill, text_col = C["bg_input"], C["text_muted"]
        else:
            fill = _blend("#FFFFFF", self._color, 0.12) if hover else self._color
            text_col = C["bg"]
        self.config(bg=self._parent_bg)
        pts = [r, 0, W - r, 0, W, 0, W, r, W, H - r, W, H, W - r, H, r, H, 0, H, 0, H - r, 0, r, 0, 0]
        self.create_polygon(pts, fill=fill, outline="", smooth=True, splinesteps=12)
        label = {"ЗАПУСК": "▶  ИГРАТЬ", "СТОП — ЗАКРЫТЬ": "■  ЗАКРЫТЬ ИГРУ"}.get(self._label, self._label)
        self.create_text(W // 2, H // 2, text=label, fill=text_col, font=_font(13, "bold"))

    def _draw(self):
        if C.get("soft_ui"):
            return self._draw_soft()
        self.delete("all"); W, H = self.W, self.H; c = self._color; cut = 10
        hover = self._hovered and not self._disabled
        fill  = self._glow if hover else _glass_panel()
        self.config(bg=self._parent_bg)
        pts = [cut,0, W-cut,0, W,cut, W,H-cut, W-cut,H, cut,H, 0,H-cut, 0,cut]
        self.create_polygon(pts, fill=fill, outline="")
        glow_col = _blend(c, C["bg"], 0.35)
        glow_col2 = _blend(c, C["bg"], 0.15)
        for off, gcol, gw in [(3, glow_col2, 1), (2, glow_col, 1), (1, glow_col, 1)]:
            gpts = [cut-off,off, W-cut+off,off, W-off,cut-off,
                    W-off,H-cut+off, W-cut+off,H-off,
                    cut-off,H-off, off,H-cut+off, off,cut-off]
            self.create_polygon(gpts, fill="", outline=gcol, width=gw)
        lw = 2 if hover else 1
        segments = [
            (cut,0,   W-cut,0),
            (W-cut,0, W,cut),
            (W,cut,   W,H-cut),
            (W,H-cut, W-cut,H),
            (W-cut,H, cut,H),
            (cut,H,   0,H-cut),
            (0,H-cut, 0,cut),
            (0,cut,   cut,0),
        ]
        for x1,y1,x2,y2 in segments:
            self.create_line(x1,y1, x2,y2, fill=c, width=lw)
        if hover:
            m = 5
            isegs = [
                (cut+m,m,   W-cut-m,m),
                (W-cut-m,m, W-m,cut+m),
                (W-m,cut+m, W-m,H-cut-m),
                (W-m,H-cut-m, W-cut-m,H-m),
                (W-cut-m,H-m, cut+m,H-m),
                (cut+m,H-m, m,H-cut-m),
                (m,H-cut-m, m,cut+m),
                (m,cut+m,   cut+m,m),
            ]
            dim = _blend(c, C["bg"], 0.5)
            for x1,y1,x2,y2 in isegs:
                self.create_line(x1,y1, x2,y2, fill=dim, width=1)
        tc = "#FFFFFF" if hover else self._color
        font = F_FRAK if C.get("reich_fx") else _font(12, "bold") if C.get("am_fx") else FB
        self.create_text(W//2, H//2, text=self._label, fill=tc, font=font)

    def _enter(self, _):
        if not self._disabled: self._hovered = True; self._draw(); self.config(cursor="hand2")
    def _leave(self, _):
        if not self._disabled: self._hovered = False; self._draw(); self.config(cursor="")
    def _click(self, _):
        if not self._disabled: self.command()
    def set_mode(self, mode):
        self._hovered = False; self._apply_mode(mode); self._draw()
        self.config(cursor="hand2" if mode == "stop" else "")

# ══════════════════════════════════════════
#  ВСПОМОГАТЕЛЬНЫЕ ВИДЖЕТЫ — с glassmorphism
# ══════════════════════════════════════════
class StyledEntry(tk.Frame):
    """
    Поле ввода с иллюзией прозрачности в FX-темах.
    
    Настоящая прозрачность в tkinter невозможна для Entry-виджетов.
    Трюк: фон Entry = точный цвет FX-canvas (C["bg"]).
    Поле визуально "исчезает", остаётся только цветная рамка.
    Создаётся иллюзия что поле прозрачное.
    """
    def __init__(self, parent, textvariable=None, show=None, **kw):
        if _is_fx_theme():
            # Рамка — акцентный цвет с мягким свечением
            border_col = _blend(C["accent"], C["bg"], 0.55)
            # Фон Entry = точный фон FX canvas — поле "исчезает"
            entry_bg = C["bg"]
            # Толщина рамки 1px сверху/снизу, 1px с боков
            super().__init__(parent,
                             bg=border_col,
                             highlightthickness=0,
                             bd=0)
            # Внутренний frame — отступ 1px даёт рамку
            inner = tk.Frame(self, bg=entry_bg, bd=0, highlightthickness=0)
            inner.pack(fill="both", expand=True, padx=1, pady=1)
            entry_kw = dict(
                bg=entry_bg,
                fg=C["text"],
                insertbackground=C["orange"],
                relief="flat", bd=0,
                highlightthickness=0,
                font=FE,
            )
            if textvariable is not None: entry_kw["textvariable"] = textvariable
            if show is not None:         entry_kw["show"] = show
            allowed = {"width", "state", "justify", "readonlybackground"}
            for k in list(kw.keys()):
                if k in allowed: entry_kw[k] = kw.pop(k)
            self._entry = tk.Entry(inner, **entry_kw)
            self._entry.pack(fill="both", expand=True, padx=8 if C.get("soft_ui") else 4,
                             pady=6 if C.get("soft_ui") else 3)
            self._border_col = border_col
            self._inner = inner
            # При фокусе — рамка ярче
            self._entry.bind("<FocusIn>",
                lambda _: super(StyledEntry, self).config(
                    bg=_blend(C["accent"], C["bg"], 0.9)))
            self._entry.bind("<FocusOut>",
                lambda _: super(StyledEntry, self).config(bg=border_col))
        else:
            border_col = C["border"]
            super().__init__(parent, bg=border_col, bd=0, highlightthickness=0)
            inner = tk.Frame(self, bg=C["bg_input"], bd=0, highlightthickness=0)
            inner.pack(fill="both", expand=True, padx=1, pady=1)
            entry_kw = dict(
                bg=C["bg_input"], fg=C["text"],
                insertbackground=C["orange"],
                relief="flat", bd=0,
                highlightthickness=0,
                font=FE,
            )
            if textvariable is not None: entry_kw["textvariable"] = textvariable
            if show is not None:         entry_kw["show"] = show
            allowed = {"width", "state", "justify"}
            for k in list(kw.keys()):
                if k in allowed: entry_kw[k] = kw.pop(k)
            self._entry = tk.Entry(inner, **entry_kw)
            self._entry.pack(fill="both", expand=True, padx=8 if C.get("soft_ui") else 4,
                             pady=6 if C.get("soft_ui") else 3)
            self._border_col = border_col
            self._inner = inner

    def get(self):           return self._entry.get()
    def insert(self, i, s):  return self._entry.insert(i, s)
    def delete(self, a, b=None):
        if b is None: return self._entry.delete(a)
        return self._entry.delete(a, b)
    def bind(self, seq, func=None, add=None):
        return self._entry.bind(seq, func, add)
    def config(self, **kw):
        entry_keys = {"show", "state", "fg", "font", "justify", "insertbackground"}
        inner_keys = {"bg"}
        e_kw = {k: v for k, v in kw.items() if k in entry_keys}
        i_kw = {k: v for k, v in kw.items() if k in inner_keys}
        f_kw = {k: v for k, v in kw.items()
                if k not in entry_keys and k not in inner_keys}
        if e_kw: self._entry.config(**e_kw)
        if i_kw:
            self._inner.config(**i_kw)
            self._entry.config(**i_kw)
        if f_kw:
            try: super().config(**f_kw)
            except tk.TclError: pass
    configure = config
    def focus_set(self): self._entry.focus_set()
    def focus(self):     self._entry.focus()


class FlatButton(tk.Label):
    """Понятная кнопка-надпись. kind: primary | secondary | ghost | danger.
    tk.Label вместо tk.Button — одинаково выглядит на Windows, Linux и macOS."""

    def __init__(self, parent, text, command=None, kind="secondary", font=None,
                 padx=14, pady=7, bg=None):
        self.kind, self.command, self._enabled = kind, command, True
        self._parent_bg = bg or parent.cget("bg")
        super().__init__(parent, text=text, font=font or _font(10, "bold"), padx=padx, pady=pady,
                         cursor="hand2", bd=0, highlightthickness=1 if kind == "secondary" else 0)
        self._paint(False)
        self.bind("<Enter>", lambda _: self._paint(True))
        self.bind("<Leave>", lambda _: self._paint(False))
        self.bind("<ButtonRelease-1>", self._click)

    def _colors(self, hover):
        k = self.kind
        if not self._enabled:
            return (self._parent_bg if k == "ghost" else C["bg_input"]), C["text_dim"], C["border"]
        if k == "primary":
            base = C["accent"]
            return (_blend("#FFFFFF", base, 0.14) if hover else base), C["bg"], base
        if k == "danger":
            return (_blend(C["red"], C["red_glow"], 0.25) if hover else C["red_glow"]), C["red"], C["red_dim"]
        if k == "ghost":
            return self._parent_bg, (C["accent"] if hover else C["text_muted"]), self._parent_bg
        base = C["bg_input"]
        return ((_blend(C["accent"], base, 0.10) if hover else base), (C["accent"] if hover else C["text"]),
                (C["accent_dim"] if hover else C["border"]))

    def _paint(self, hover):
        bg, fg, border = self._colors(hover)
        self.config(bg=bg, fg=fg, highlightbackground=border, highlightcolor=border,
                    cursor="hand2" if self._enabled else "arrow")

    def _click(self, _=None):
        if self._enabled and self.command:
            self.command()

    def set_enabled(self, flag: bool):
        self._enabled = bool(flag)
        self._paint(False)


def lbl(parent, text, **kw):
    bg = C["bg"]
    return tk.Label(parent, text=text, bg=bg, fg=C["text_muted"], font=FL, **kw)

def sep(parent):
    col = _blend(C["accent"], C["bg"], 0.2) if _is_fx_theme() else C["sep"]
    return tk.Frame(parent, height=1, bg=col)

def section_title(parent, text):
    f = tk.Frame(parent, bg=C["bg"])
    font = F_FRAK if C.get("reich_fx") else FSB
    prefix = "--- " if C.get("reich_fx") else ">> " if C.get("am_fx") else "// "
    tk.Label(f, text=f"{prefix}{text}", bg=C["bg"], fg=C["amber"], font=font).pack(side="left")
    sep_col = _blend(C["accent"], C["bg"], 0.25) if _is_fx_theme() else C["sep"]
    tk.Frame(f, bg=sep_col, height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=5)
    return f

# ══════════════════════════════════════════
#  ЗАГОЛОВОК
# ══════════════════════════════════════════
def _redraw_header_content(cv, width, height, config=None):
    cv.delete("header_static")
    _draw_header_static(cv, width, height, config=config)

def _draw_header_static(cv, width, height, config=None):
    if C.get("reich_fx"):
        cv.create_rectangle(0, 0, width, 8, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(0, height-8, width, height, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(0, 8, width, height-8, fill="#0A0800", outline="", tags="header_static")
        cv.create_line(0, height//2, width, height//2, fill="#664400", width=1, tags="header_static")
        mx = width // 2; my = height // 2
        arm = 14; thick = 5
        for dx, dy in [(-arm,0),(arm,0),(0,-arm),(0,arm)]:
            cv.create_rectangle(mx-thick//2+dx//2, my-thick//2+dy//2,
                                mx+thick//2+dx, my+thick//2+dy,
                                fill="#CC9900", outline="#886600", tags="header_static")
        cv.create_rectangle(mx-thick, my-thick, mx+thick, my+thick,
                            fill="#FFD700", outline="#CC9900", tags="header_static")
        ex, ey = 46, height//2
        cv.create_oval(ex-8, ey-12, ex+8, ey+8, fill="#1A1000", outline="#CC9900", width=1, tags="header_static")
        wing_pts_l = [ex-8,ey-8, ex-28,ey-18, ex-32,ey-6, ex-20,ey-2, ex-8,ey-2]
        wing_pts_r = [ex+8,ey-8, ex+28,ey-18, ex+32,ey-6, ex+20,ey-2, ex+8,ey-2]
        cv.create_polygon(wing_pts_l, fill="#332200", outline="#CC9900", width=1, tags="header_static")
        cv.create_polygon(wing_pts_r, fill="#332200", outline="#CC9900", width=1, tags="header_static")
        cv.create_oval(ex-5, ey-18, ex+5, ey-8, fill="#CC9900", outline="#886600", tags="header_static")
        cv.create_line(ex-6,ey+8, ex-10,ey+15, fill="#CC9900", width=2, tags="header_static")
        cv.create_line(ex+6,ey+8, ex+10,ey+15, fill="#CC9900", width=2, tags="header_static")
        cv.create_line(92, 10, 92, height-10, fill="#664400", width=1, tags="header_static")
        cv.create_text(100, height//2-12, text="ATOMISCHE INDUSTRIE",
                       anchor="w", fill="#F0E8C8",
                       font=("Times New Roman", 13, "bold"), tags="header_static")
        cv.create_text(102, height//2+8, text="K R I E G S - S T A R T E R",
                       anchor="w", fill="#CC9900",
                       font=("Times New Roman", 10, "bold"), tags="header_static")
        rx = width - 14; ry = height//2
        orn = 12
        for col, r in [("#442200",orn),("#664400",orn-3),("#CC9900",orn-6)]:
            pts = [rx,ry-r, rx+r,ry, rx,ry+r, rx-r,ry]
            cv.create_polygon(pts, fill="", outline=col, width=1, tags="header_static")
        cv.create_text(width-26, height-10, text="v2.0",
                       anchor="e", fill="#7A6840",
                       font=_font(7), tags="header_static")
        cv.create_rectangle(0, height-3, width//3, height, fill="#CC2200", outline="", tags="header_static")
        cv.create_rectangle(width//3, height-3, width, height, fill="#CC9900", outline="", tags="header_static")
    elif C.get("stal_fx"):
        # ══ СОВЕТСКИЙ ЗАГОЛОВОК ══
        # Фон — тёмно-красный с градиентом
        cv.create_rectangle(0, 0, width, height, fill="#0D0400", outline="", tags="header_static")
        # Верхняя полоса — красная
        cv.create_rectangle(0, 0, width, 5, fill="#CC0000", outline="", tags="header_static")
        # Нижняя полоса — красная с золотой
        cv.create_rectangle(0, height-5, width, height, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(0, height-8, width, height-5, fill="#AA8800", outline="", tags="header_static")

        # ── Серп и молот (рисуем вручную) ──────────────────────────
        ox, oy = 44, height // 2
        gold = "#FFD700"; dgold = "#AA8800"; red = "#CC0000"

        # Молот — рукоять
        handle_angle = math.radians(-35)
        hx1 = ox + math.cos(handle_angle) * 6;   hy1 = oy + math.sin(handle_angle) * 6
        hx2 = ox + math.cos(handle_angle) * 28;  hy2 = oy + math.sin(handle_angle) * 28
        cv.create_line(hx1, hy1, hx2, hy2, fill=gold, width=4,
                       capstyle="round", tags="header_static")
        # Голова молота — перпендикулярно рукояти
        perp = handle_angle + math.pi/2
        mx = ox + math.cos(handle_angle) * 8;  my = oy + math.sin(handle_angle) * 8
        head_len = 14
        hh1x = mx + math.cos(perp)*head_len;  hh1y = my + math.sin(perp)*head_len
        hh2x = mx - math.cos(perp)*(head_len*0.5); hh2y = my - math.sin(perp)*(head_len*0.5)
        cv.create_line(hh1x, hh1y, hh2x, hh2y, fill=gold, width=7,
                       capstyle="round", tags="header_static")

        # Серп — дуга + рукоять
        sickle_cx = ox - 6; sickle_cy = oy + 4
        sr_outer = 17; sr_inner = 11
        # Внешняя дуга серпа
        for angle_deg in range(200, 370, 4):
            a = math.radians(angle_deg)
            x1 = sickle_cx + math.cos(a) * sr_outer
            y1 = sickle_cy + math.sin(a) * sr_outer
            a2 = math.radians(angle_deg + 4)
            x2 = sickle_cx + math.cos(a2) * sr_outer
            y2 = sickle_cy + math.sin(a2) * sr_outer
            cv.create_line(x1, y1, x2, y2, fill=gold, width=5,
                           capstyle="round", tags="header_static")
        # Внутренняя режущая кромка
        for angle_deg in range(200, 370, 4):
            a = math.radians(angle_deg)
            x1 = sickle_cx + math.cos(a) * sr_inner
            y1 = sickle_cy + math.sin(a) * sr_inner
            a2 = math.radians(angle_deg + 4)
            x2 = sickle_cx + math.cos(a2) * sr_inner
            y2 = sickle_cy + math.sin(a2) * sr_inner
            cv.create_line(x1, y1, x2, y2, fill="#0D0400", width=3,
                           capstyle="round", tags="header_static")
        # Рукоять серпа
        cv.create_line(sickle_cx + math.cos(math.radians(200))*sr_outer,
                       sickle_cy + math.sin(math.radians(200))*sr_outer,
                       sickle_cx - 2, sickle_cy + sr_outer + 4,
                       fill=gold, width=4, capstyle="round", tags="header_static")

        # Разделитель
        cv.create_line(82, 8, 82, height-8, fill="#441500", width=1, tags="header_static")

        # Название
        cv.create_text(96, height//2 - 14, text="ATOMIC INDUSTRY",
                       anchor="w", fill="#F5E0C0",
                       font=("Times New Roman", 16, "bold"), tags="header_static")
        cv.create_text(98, height//2 + 8, text="С О В Е Т С К И Й   Л А У Н Ч Е Р",
                       anchor="w", fill="#CC3300",
                       font=("Times New Roman", 9, "bold"), tags="header_static")

        # Звезда справа
        star_x = width - 22; star_y = height // 2
        star_r = 11; star_r2 = 5
        star_pts = []
        for i in range(10):
            a = math.radians(i * 36 - 90)
            r = star_r if i % 2 == 0 else star_r2
            star_pts.extend([star_x + math.cos(a)*r, star_y + math.sin(a)*r])
        cv.create_polygon(star_pts, fill="#CC0000", outline="#FF3300", width=1, tags="header_static")

        cv.create_text(width-36, height-10, text="v2.0",
                       anchor="e", fill="#441500",
                       font=_font(7), tags="header_static")
        # Полосы снизу
        cv.create_rectangle(0, height-3, width//2, height, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(width//2, height-3, width, height, fill="#AA8800", outline="", tags="header_static")
    elif C.get("aurora_fx"):
        for i, (col, y_pos, alpha) in enumerate([
            ("#00FF88", height*0.15, 0.25), ("#44FFCC", height*0.30, 0.20),
            ("#FF44AA", height*0.55, 0.18), ("#8844FF", height*0.70, 0.22),
        ]):
            for w_off in range(6, 0, -1):
                bc = _blend(col, "#000510", alpha * w_off/6)
                cv.create_line(0, y_pos-w_off, width, y_pos-w_off, fill=bc, tags="header_static")
                cv.create_line(0, y_pos+w_off, width, y_pos+w_off, fill=bc, tags="header_static")
        ox, oy = 44, 40; R, r_small = 22, 5
        for ang_deg, clr in [(0,"#FF6EC7"),(60,"#FF2266"),(120,"#AAFFEE")]:
            ang = math.radians(ang_deg); ca, sa = math.cos(ang), math.sin(ang)
            pts = []
            for t_deg in range(0, 361, 6):
                t = math.radians(t_deg); lx = R*math.cos(t); ly = int(R/2.8)*math.sin(t)
                pts.extend([ox+lx*ca-ly*sa, oy+lx*sa+ly*ca])
            cv.create_line(pts, fill=clr, width=1, smooth=True, tags="header_static")
        cv.create_oval(ox-r_small, oy-r_small, ox+r_small, oy+r_small,
                       fill="#FF6EC7", outline="#AAFFEE", width=1, tags="header_static")
        cv.create_line(82, 12, 82, 68, fill="#0A3A5A", width=1, tags="header_static")
        cv.create_text(96, 28, text="ATOMIC INDUSTRY", anchor="w", fill="#E8F8FF",
                       font=_font(17, "bold"), tags="header_static")
        cv.create_text(98, 50, text="A U R O R A   I N F I N I T A", anchor="w",
                       fill="#FF6EC7", font=_font(9, "bold"), tags="header_static")
        cv.create_text(width-10, 54, text="v2.0", anchor="e", fill="#336688",
                       font=_font(7), tags="header_static")
        cv.create_rectangle(0, height-3, width//3, height, fill="#FF2266", outline="", tags="header_static")
        cv.create_rectangle(width//3, height-3, width, height, fill="#7744FF", outline="", tags="header_static")
    elif C.get("dedinsaid_fx"):
        # Tokyo Ghoul — заголовок с паучьими лилиями
        cv.create_rectangle(0, 0, width, height, fill="#080808", outline="", tags="header_static")
        cv.create_rectangle(0, height-4, width, height, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(0, height-8, width, height-4, fill="#660000", outline="", tags="header_static")
        # Капли крови сверху
        for i, xp in enumerate(range(20, width-10, width//10)):
            h_drop = 8 + (i%3)*4
            cv.create_rectangle(xp-2, 0, xp+2, h_drop, fill="#AA0000", outline="", tags="header_static")
            cv.create_oval(xp-4, h_drop-2, xp+4, h_drop+6, fill="#AA0000", outline="", tags="header_static")
        # Атом в красно-чёрных цветах
        ox, oy = 44, 40; R, r_small = 22, 5
        for ang_deg, clr in [(0,"#FF0000"),(60,"#880000"),(120,"#CC2200")]:
            ang = math.radians(ang_deg); ca, sa = math.cos(ang), math.sin(ang)
            pts = []
            for t_deg in range(0, 361, 6):
                t = math.radians(t_deg); lx = R*math.cos(t); ly = int(R/2.8)*math.sin(t)
                pts.extend([ox+lx*ca-ly*sa, oy+lx*sa+ly*ca])
            cv.create_line(pts, fill=clr, width=1, smooth=True, tags="header_static")
        cv.create_oval(ox-r_small, oy-r_small, ox+r_small, oy+r_small,
                       fill="#FF0000", outline="#880000", width=1, tags="header_static")
        cv.create_line(82, 12, 82, 68, fill="#330000", width=1, tags="header_static")
        cv.create_text(96, 26, text="ATOMIC INDUSTRY", anchor="w", fill="#CCCCCC",
                       font=_font(17, "bold"), tags="header_static")
        cv.create_text(98, 48, text="H I G A N B A N A   E D I T I O N", anchor="w",
                       fill="#CC0000", font=_font(8, "bold"), tags="header_static")
        # Паучья лилия декор справа в заголовке (статичная, маленькая)
        _draw_lily_header(cv, width - 55, height // 2 + 4, size=14, tags="header_static")
        cv.create_text(width-10, height-12, text="v2.0", anchor="e",
                       fill="#440000", font=_font(7), tags="header_static")
        cv.create_rectangle(0, height-3, width//2, height, fill="#CC0000", outline="", tags="header_static")
        cv.create_rectangle(width//2, height-3, width, height, fill="#880000", outline="", tags="header_static")
    elif C.get("am_fx"):
        # ══ A.M. ЗАГОЛОВОК — терминал машины ══
        cv.create_rectangle(0, 0, width, height, fill="#000000", outline="", tags="header_static")
        for i in range(0, height, 3):
            cv.create_rectangle(0, i+1, width, i+2, fill="#000200", outline="", tags="header_static")
        cv.create_rectangle(0, 0, width, 2, fill="#002200", outline="", tags="header_static")
        cv.create_rectangle(0, height-3, width, height, fill="#1A0000", outline="", tags="header_static")
        # Иконка — концентрические кольца + AM
        ox, oy = 44, height // 2
        for r, alpha in [(20, 0.35), (28, 0.20), (36, 0.10)]:
            col = _blend("#00FF41", "#000000", alpha)
            cv.create_oval(ox-r, oy-r, ox+r, oy+r, fill="", outline=col, width=1, tags="header_static")
        cv.create_text(ox, oy, text="AM",
                       fill=_blend("#00FF41", "#000000", 0.55),
                       font=_font(13, "bold"),
                       anchor="center", tags="header_static")
        cv.create_line(80, 8, 80, height-8,
                       fill=_blend("#00FF41", "#000000", 0.12), width=1, tags="header_static")
        cv.create_text(92, height//2 - 14,
                       text="ATOMIC INDUSTRY",
                       anchor="w", fill=_blend("#00FF41", "#000000", 0.75),
                       font=_font(17, "bold"), tags="header_static")
        cv.create_text(94, height//2 + 8,
                       text="Я  В И Ж У  В А С",
                       anchor="w", fill=_blend("#FF0000", "#000000", 0.55),
                       font=_font(8, "bold"), tags="header_static")
        cv.create_text(width - 10, height//2 - 10,
                       text="01 10 11 00 10",
                       anchor="e", fill=_blend("#00FF41", "#000000", 0.18),
                       font=_font(7), tags="header_static")
        cv.create_text(width - 10, height - 12, text="v2.0",
                       anchor="e", fill=_blend("#00FF41", "#000000", 0.12),
                       font=_font(7), tags="header_static")
        cv.create_rectangle(0, height-3, width//2, height, fill="#001A00", outline="", tags="header_static")
        cv.create_rectangle(width//2, height-3, width, height, fill="#200000", outline="", tags="header_static")
    else:
        # ── Кастомное фото вместо атома ──────────────────────────────
        _banner_img_drawn = False
        if config is not None:
            _cbp = config.get("custom_banner_path", "").strip()
            if _cbp and os.path.exists(_cbp):
                try:
                    from PIL import Image as _PILImg, ImageTk as _PILTk
                    _bim = _PILImg.open(_cbp).convert("RGBA")
                    _bh = height - 8
                    _bw_max = 76
                    _scale = min(_bw_max / _bim.width, _bh / _bim.height)
                    _nw = max(1, int(_bim.width * _scale))
                    _nh = max(1, int(_bim.height * _scale))
                    _bim = _bim.resize((_nw, _nh), _PILImg.LANCZOS)
                    _bph = _PILTk.PhotoImage(_bim)
                    _bx = 44; _by = height // 2
                    cv.create_image(_bx, _by, image=_bph, anchor="center", tags="header_static")
                    # Держим ссылку чтобы GC не удалил
                    if not hasattr(cv, "_banner_imgs"):
                        cv._banner_imgs = []
                    cv._banner_imgs.append(_bph)
                    _banner_img_drawn = True
                except Exception:
                    pass
        if not _banner_img_drawn:
            ox, oy = 44, 40; R, r_small = 22, 5
            for ang_deg, clr in [(0,C["orange"]),(60,C["red"]),(120,C["amber"])]:
                ang = math.radians(ang_deg); ca, sa = math.cos(ang), math.sin(ang)
                pts = []
                for t_deg in range(0, 361, 6):
                    t = math.radians(t_deg); lx = R*math.cos(t); ly = int(R/2.8)*math.sin(t)
                    pts.extend([ox+lx*ca-ly*sa, oy+lx*sa+ly*ca])
                cv.create_line(pts, fill=clr, width=1, smooth=True, tags="header_static")
            cv.create_oval(ox-r_small, oy-r_small, ox+r_small, oy+r_small,
                           fill=C["orange"], outline=C["amber"], width=1, tags="header_static")
        cv.create_line(82, 12, 82, 68, fill=C["sep"], width=1, tags="header_static")
        cv.create_text(96, 28, text="ATOMIC INDUSTRY",
                       anchor="w", fill=C["text"],
                       font=_font(17, "bold"), tags="header_static")
        cv.create_text(98, 50, text="L M P D   L A U N C H E R",
                       anchor="w", fill=C["orange"],
                       font=_font(9, "bold"), tags="header_static")
        cv.create_text(width-10, 54, text="v2.0",
                       anchor="e", fill=C["text_muted"],
                       font=_font(7), tags="header_static")
        cv.create_rectangle(0, height-3, width//3, height,
                            fill=C["header_stripe1"], outline="", tags="header_static")
        cv.create_rectangle(width//3, height-3, width, height,
                            fill=C["header_stripe2"], outline="", tags="header_static")


def _draw_lily_header(cv, cx, cy, size=14, tags=""):
    """Рисует маленькую паучью лилию для заголовка (статичная)."""
    bg = "#080808"
    num_petals = 6
    stamen_count = 10

    # Лепестки
    for pi in range(num_petals):
        base_ang = math.radians(pi * 60 + 30)
        pts = []
        for ti in range(10):
            t = ti / 9
            ang = base_ang + math.radians(t * 22 - 11)
            r = size * (0.15 + 0.85 * math.sin(t * math.pi))
            lateral = math.radians(90) + base_ang
            wf = math.sin(t * math.pi) * size * 0.2
            px = cx + math.cos(ang) * r + math.cos(lateral) * wf * 0.5
            py = cy + math.sin(ang) * r + math.sin(lateral) * wf * 0.5
            pts.extend([px, py])
        col = _blend("#FF0000", bg, 0.85)
        if len(pts) >= 4:
            if tags:
                cv.create_line(pts, fill=col, width=1, smooth=True, capstyle="round", tags=tags)
            else:
                cv.create_line(pts, fill=col, width=1, smooth=True, capstyle="round")

    # Тычинки
    stamen_col = _blend("#FF3300", bg, 0.8)
    anther_col = _blend("#FFCC00", bg, 0.85)
    for si in range(stamen_count):
        ang = math.radians(si * (360 / stamen_count))
        s_len = size * 1.3
        mid_ang = ang + math.radians(12)
        mid_r = s_len * 0.55
        sx1 = cx + math.cos(mid_ang) * mid_r * 0.35
        sy1 = cy + math.sin(mid_ang) * mid_r * 0.35
        ex = cx + math.cos(ang) * s_len
        ey = cy + math.sin(ang) * s_len
        if tags:
            cv.create_line(cx, cy, sx1, sy1, ex, ey, fill=stamen_col, width=1, smooth=True, tags=tags)
        else:
            cv.create_line(cx, cy, sx1, sy1, ex, ey, fill=stamen_col, width=1, smooth=True)
        ar = max(1, int(size * 0.07))
        if tags:
            cv.create_oval(ex-ar, ey-ar, ex+ar, ey+ar, fill=anther_col, outline="", tags=tags)
        else:
            cv.create_oval(ex-ar, ey-ar, ex+ar, ey+ar, fill=anther_col, outline="")

    # Центр
    cr = max(1, int(size * 0.16))
    center_col = _blend("#880000", bg, 0.9)
    if tags:
        cv.create_oval(cx-cr, cy-cr, cx+cr, cy+cr, fill=center_col, outline="#FF0000", tags=tags)
    else:
        cv.create_oval(cx-cr, cy-cr, cx+cr, cy+cr, fill=center_col, outline="#FF0000")


def draw_header(parent, width=640, height=80, config=None):
    global _galaxy_fx, _collapsing_star

    if _galaxy_fx is not None: _galaxy_fx.destroy(); _galaxy_fx = None
    if _collapsing_star is not None: _collapsing_star.destroy(); _collapsing_star = None

    cv = tk.Canvas(parent, width=width, height=height,
                   bg=C["bg_header"], highlightthickness=0)

    if C.get("galaxy_fx", False):
        _galaxy_fx = GalaxyFX(cv, width, height, bg_col=C["bg_header"])
        _galaxy_fx.start()

    if C.get("nebula_fx", False):
        _galaxy_fx = GalaxyFX(cv, width, height, bg_col=C["bg_header"])
        _galaxy_fx.start()
        star_cx = width - 55; star_cy = height // 2
        _collapsing_star = CollapsingStarFX(cv, star_cx, star_cy)
        _collapsing_star.start()

    if C.get("reich_fx", False):
        rfx = ReichFX(cv, width, height)
        rfx.start()
        cv._reich_header_fx = rfx

    _draw_header_static(cv, width, height, config=config)
    return cv

# ══════════════════════════════════════════
#  ОКНО КОНСОЛИ
# ══════════════════════════════════════════
class ConsoleWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Console — Atomic Industry LMPD")
        self.geometry("720x380"); self.configure(bg=C["bg"])
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        hdr = tk.Frame(self, bg=C["bg_header"]); hdr.pack(fill="x")
        tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
        hdr_row = tk.Frame(hdr, bg=C["bg_header"]); hdr_row.pack(fill="x")
        tk.Label(hdr_row, text="  CONSOLE OUTPUT", bg=C["bg_header"],
                 fg=C["orange"], font=FSB, pady=4).pack(side="left")
        tk.Button(hdr_row, text=" 💾 ЛОГ ", command=self._save_log,
                  bg=C["bg_header"], fg=C["amber"], font=_font(8, "bold"),
                  relief="flat", highlightthickness=1, highlightbackground=C["border"],
                  activebackground=C["orange_glow"], activeforeground=C["orange"],
                  cursor="hand2", padx=4, pady=2).pack(side="right", padx=8, pady=3)
        self.text = tk.Text(self, bg=_glass_log(), fg=C["text_muted"], font=FLG,
                            state="disabled", bd=0, highlightthickness=0, wrap="word", padx=6, pady=4)
        self.text.pack(fill="both", expand=True, padx=6, pady=6)
        self.text.tag_config("out", foreground=C["text_muted"])
        self.text.tag_config("err", foreground=C["red"])
        self.withdraw()

    def _save_log(self):
        content = self.text.get("1.0", tk.END)
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")],
            initialfile=f"console_{ts}.txt", title="Сохранить лог консоли")
        if path:
            with open(path, "w", encoding="utf-8") as f: f.write(content)
            messagebox.showinfo("Atomic Industry", f"Лог сохранён:\n{path}", parent=self)

    def append(self, text, tag="out"):
        self.text.config(state="normal"); self.text.insert(tk.END, text, tag)
        self.text.see(tk.END); self.text.config(state="disabled")
    def show(self): self.deiconify(); self.lift()

# ══════════════════════════════════════════
#  ОКНО ЗАГРУЗКИ MC / FORGE
# ══════════════════════════════════════════
class DownloadWindow(tk.Toplevel):
    def __init__(self, master, version_label: str):
        super().__init__(master)
        self.title("Загрузка — Atomic Industry LMPD")
        self.geometry("500x270"); self.resizable(False, False)
        self.configure(bg=C["bg"]); self.protocol("WM_DELETE_WINDOW", self._cancel)
        hdr = tk.Frame(self, bg=C["bg_header"]); hdr.pack(fill="x")
        tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
        tk.Label(hdr, text=f"  ЗАГРУЗКА  //  {version_label}",
                 bg=C["bg_header"], fg=C["orange"], font=_font(10, "bold"), pady=5).pack(side="left")
        body = tk.Frame(self, bg=C["bg"]); body.pack(fill="both", expand=True, padx=16, pady=10)
        self._stage_var = tk.StringVar(value="Инициализация...")
        tk.Label(body, textvariable=self._stage_var, bg=C["bg"], fg=C["amber"],
                 font=_font(9, "bold"), anchor="w").pack(fill="x")
        self._file_var = tk.StringVar(value="")
        tk.Label(body, textvariable=self._file_var, bg=C["bg"], fg=C["text_muted"],
                 font=_font(8), anchor="w").pack(fill="x", pady=(2,0))
        tk.Label(body, text="Текущий файл:", bg=C["bg"], fg=C["text_dim"],
                 font=_font(7)).pack(anchor="w", pady=(6,0))
        self._file_pb = ttk.Progressbar(body, style="AI.Horizontal.TProgressbar",
                                        mode="determinate", maximum=100)
        self._file_pb.pack(fill="x", pady=(2,0))
        self._count_var = tk.StringVar(value="")
        tk.Label(body, textvariable=self._count_var, bg=C["bg"], fg=C["text_muted"],
                 font=_font(7), anchor="w").pack(fill="x", pady=(2,0))
        tk.Label(body, text="Общий прогресс:", bg=C["bg"], fg=C["text_dim"],
                 font=_font(7)).pack(anchor="w", pady=(6,0))
        self._total_pb = ttk.Progressbar(body, style="AI.Horizontal.TProgressbar",
                                         mode="determinate", maximum=100)
        self._total_pb.pack(fill="x", pady=(2,0))
        self._total_var = tk.StringVar(value="")
        tk.Label(body, textvariable=self._total_var, bg=C["bg"], fg=C["text_muted"],
                 font=_font(8), anchor="w").pack(fill="x", pady=(2,0))
        self.cancelled = False
        cancel_row = tk.Frame(self, bg=C["bg"]); cancel_row.pack(fill="x", padx=16, pady=(4,6))
        self._cancel_btn = tk.Button(cancel_row, text="  ✕ ОТМЕНА  ", command=self._cancel,
                                     bg=C["bg_panel"], fg=C["red"], font=_font(8, "bold"),
                                     relief="flat", highlightthickness=1,
                                     highlightbackground=C.get("red_glow","#1A0000"),
                                     activebackground=C.get("red_glow","#1A0000"),
                                     activeforeground=C["red"], cursor="hand2", padx=8, pady=4)
        self._cancel_btn.pack(side="right")
        tk.Frame(self, height=2, bg=C["orange"]).pack(side="bottom", fill="x")
        self.after(150, self._center)

    def _cancel(self):
        self.cancelled = True
        _CANCEL_EVENT.set()
        try:
            self._cancel_btn.config(text=" Отменяю... ", state="disabled")
            self._stage_var.set("Отменяю — дожидаюсь текущих файлов...")
        except tk.TclError:
            pass

    def _center(self):
        self.update_idletasks()
        pw = self.master.winfo_x() + self.master.winfo_width()//2
        ph = self.master.winfo_y() + self.master.winfo_height()//2
        w, h = 500, 310; self.geometry(f"{w}x{h}+{pw-w//2}+{ph-h//2}")

    def set_stage(self, text): self._stage_var.set(text)
    def set_file(self, name):
        if len(name) > 62: name = "..." + name[-59:]
        self._file_var.set(name)
    def set_file_progress(self, pct): self._file_pb["value"] = max(0.0, min(100.0, pct))
    def set_total_progress(self, pct, label=""):
        self._total_pb["value"] = max(0.0, min(100.0, pct)); self._total_var.set(label)
    def set_count(self, current, total): self._count_var.set(f"Файл {current} из {total}")
    def close(self):
        try: self.destroy()
        except: pass

# ══════════════════════════════════════════
#  ОКНО КРАШ-РЕПОРТА
# ══════════════════════════════════════════
def show_crash_window(master, crash_path, error_text):
    win = tk.Toplevel(master); win.title("CRASH REPORT — Atomic Industry LMPD")
    win.geometry("700x440"); win.configure(bg=C["bg"]); win.after(100, win.grab_set)
    hdr = tk.Frame(win, bg=C["red_glow"]); hdr.pack(fill="x")
    tk.Frame(hdr, height=3, bg=C["red"]).pack(fill="x")
    tk.Label(hdr, text="  !! CRASH REPORT", bg=C["red_glow"], fg=C["red"],
             font=_font(11, "bold"), pady=6).pack(side="left")
    box = tk.Text(win, bg=C["log_bg"], fg=C["red"], font=FLG, bd=0,
                  highlightthickness=0, wrap="word", padx=8, pady=6)
    box.pack(fill="both", expand=True, padx=8, pady=(6,0))
    box.insert(tk.END, error_text); box.config(state="disabled")
    bf = tk.Frame(win, bg=C["bg"]); bf.pack(fill="x", padx=8, pady=8)
    for txt, cmd in [("  ОТКРЫТЬ ФАЙЛ  ", lambda: open_file(crash_path)),
                     ("  ПАПКА РЕПОРТОВ  ", lambda: open_file(CRASH_DIR)),
                     ("  ЗАКРЫТЬ  ", win.destroy)]:
        tk.Button(bf, text=txt, command=cmd, bg=C["bg_panel"], fg=C["amber"],
                  font=_font(8, "bold"), relief="flat",
                  highlightthickness=1, highlightbackground=C["border"],
                  activebackground=C["orange_glow"], activeforeground=C["orange"],
                  cursor="hand2", padx=4, pady=4).pack(side="left", padx=(0,6))
    tk.Label(win, text=f"  {crash_path}", bg=C["bg"], fg=C["text_dim"], font=FS).pack(
        anchor="w", padx=8, pady=(0,4))

# ══════════════════════════════════════════
#  СЕКРЕТ-ЗАСТАВКА
# ══════════════════════════════════════════
def _show_secret_splash(master, theme_key, msg, color, on_done):
    splash = tk.Toplevel(master)
    splash.overrideredirect(True)
    splash.configure(bg="#000000")
    splash.after(50, lambda: splash.geometry(
        f"420x200+{master.winfo_x()+110}+{master.winfo_y()+280}"))
    cv = tk.Canvas(splash, width=420, height=200, bg="#000000", highlightthickness=0)
    cv.pack()
    tick = [0]
    def _flash():
        tick[0] += 1
        brightness = 0.4 + 0.6*(0.5 + 0.5*math.sin(tick[0]*0.2))
        col = _blend(color, "#000000", brightness)
        cv.delete("all")
        cv.create_text(210, 70, text="* SECRET UNLOCKED *", fill=col,
                       font=_font(15, "bold"))
        for i, line in enumerate(msg.split("\n")):
            cv.create_text(210, 110+i*22, text=line, fill=col, font=_font(10))
        # Для ghoul темы добавляем цветочек в сплэш
        if theme_key == "dedinsaid":
            _draw_lily_header(cv, 50, 100, size=16)
            _draw_lily_header(cv, 370, 100, size=16)
        if tick[0] < 55:
            splash.after(55, _flash)
        else:
            splash.destroy()
            on_done()
    _flash()

# ══════════════════════════════════════════
#  БРАУЗЕР МОДОВ — CurseForge / Modrinth
# ══════════════════════════════════════════

def _show_mod_browser(master, config):
    """Окно для поиска и скачивания модов с CurseForge и Modrinth.
    Поддерживает: поиск, иконки модов, страница мода внутри лаунчера, скачивание."""
    import urllib.request, ssl, json as _j, io

    # ── Вспомогательная функция загрузки иконки ──────────────────────
    _icon_cache = {}   # url → PhotoImage

    def _load_icon_async(url, callback):
        """Загружает иконку в фоне, вызывает callback(PhotoImage) в главном потоке."""
        if not url:
            return
        if url in _icon_cache:
            try: callback(_icon_cache[url])
            except: pass
            return
        def _task():
            try:
                ctx2 = ssl.create_default_context()
                req2 = urllib.request.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req2, context=ctx2, timeout=8) as r:
                    data = r.read()
                try:
                    from PIL import Image as PILImage, ImageTk
                    img = PILImage.open(io.BytesIO(data)).resize((56, 56))
                    photo = ImageTk.PhotoImage(img)
                except Exception:
                    # PIL не установлен — используем tk PhotoImage напрямую (только PNG/GIF)
                    photo = tk.PhotoImage(data=data)
                _icon_cache[url] = photo
                win.after(0, lambda p=photo: callback(p))
            except Exception:
                pass
        threading.Thread(target=_task, daemon=True).start()

    win = tk.Toplevel(master)
    win.title("Браузер модов")
    win.geometry("1020x760"); win.minsize(800, 560)
    win.configure(bg=C["bg"])
    win.resizable(True, True)

    hdr = tk.Frame(win, bg=C["bg_header"]); hdr.pack(fill="x")
    tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(hdr, text="  🔍  БРАУЗЕР МОДОВ", bg=C["bg_header"], fg=C["orange"],
             font=_font(11, "bold"), pady=6).pack(side="left")

    # Панель поиска
    search_bar = tk.Frame(win, bg=C["bg_panel"]); search_bar.pack(fill="x", padx=12, pady=8)
    tk.Label(search_bar, text="Платформа:", bg=C["bg_panel"], fg=C["text_muted"], font=FL).pack(side="left")
    platform_var = tk.StringVar(value="modrinth")
    for val, lbl_txt in (("modrinth", "Modrinth"), ("curseforge", "CurseForge")):
        tk.Radiobutton(search_bar, text=lbl_txt, variable=platform_var, value=val,
                       bg=C["bg_panel"], fg=C["text"], selectcolor=_glass_entry_bg() if _is_fx_theme() else C["bg_input"],
                       activebackground=C["bg_panel"], activeforeground=C["orange"],
                       font=FL, cursor="hand2").pack(side="left", padx=(6, 0))
    # Тип контента
    tk.Label(search_bar, text="  Тип:", bg=C["bg_panel"], fg=C["text_muted"], font=FL).pack(side="left", padx=(12, 0))
    _TYPE_OPTIONS = {
        "Мод":          "mod",
        "Шейдер":       "shader",
        "Текстур пак":  "resourcepack",
        "Датапак":      "datapack",
    }
    content_type_var = tk.StringVar(value="Мод")
    ttk.Combobox(search_bar, textvariable=content_type_var,
                 values=list(_TYPE_OPTIONS.keys()),
                 state="readonly", width=12, font=FL).pack(side="left", padx=(4, 0))

    # ── Ядро (лоадер) ──────────────────────────────────────────────────
    tk.Label(search_bar, text="  Ядро:", bg=C["bg_panel"], fg=C["text_muted"], font=FL).pack(side="left", padx=(12, 0))
    _LOADER_OPTIONS = ["Любое", "forge", "fabric", "quilt", "neoforge"]
    _sel_ver_for_loader = config.get("selected_version", "1.20.1 Forge")
    _sel_loader_default = VERSIONS.get(_sel_ver_for_loader, {}).get("loader", "forge")
    if _sel_loader_default == "vanilla": _sel_loader_default = "Любое"
    loader_var = tk.StringVar(value=_sel_loader_default)
    ttk.Combobox(search_bar, textvariable=loader_var, values=_LOADER_OPTIONS,
                 state="readonly", width=10, font=FL).pack(side="left", padx=(4, 0))

    tk.Label(search_bar, text="  Версия MC:", bg=C["bg_panel"], fg=C["text_muted"], font=FL).pack(side="left", padx=(12, 0))
    def _ver_key(s):
        try: return tuple(int(x) for x in s.split("."))
        except: return (0,)
    mc_versions_list = sorted(set(v["mc_version"] for v in VERSIONS.values()), key=_ver_key, reverse=True)
    _sel = config.get("selected_version", "1.20.1 Forge")
    _sel_mc = VERSIONS.get(_sel, {}).get("mc_version", _sel.split()[0])
    ver_var = tk.StringVar(value=_sel_mc)
    _ver_combo = ttk.Combobox(search_bar, textvariable=ver_var, values=mc_versions_list,
                 state="normal", width=8, font=FL)
    _ver_combo.pack(side="left", padx=(4, 0))
    tk.Label(search_bar, text="  Название:", bg=C["bg_panel"], fg=C["text_muted"], font=FL).pack(side="left", padx=(12, 0))
    query_var = tk.StringVar()
    query_entry = tk.Entry(search_bar, textvariable=query_var,
                           bg=_glass_entry_bg(), fg=C["text"], font=FL, bd=0,
                           highlightthickness=1, highlightbackground=_glass_border(),
                           insertbackground=C["text"], width=24)
    query_entry.pack(side="left", padx=(4, 0))

    status_var = tk.StringVar(value="")
    tk.Label(win,
             textvariable=status_var, bg=C["bg"], fg=C["text_muted"], font=FS).pack(anchor="w", padx=14)

    # ── Пагинация ─────────────────────────────────────────────────────
    _page_offset = [0]
    _page_size   = 20
    _last_query  = [""]  # запоминаем последний поисковый запрос

    page_bar = tk.Frame(win, bg=C["bg_panel"]); page_bar.pack(fill="x", padx=12, pady=(0, 4))

    def _update_page_buttons():
        page_lbl.config(text=f"Стр. {_page_offset[0] // _page_size + 1}")
        btn_prev.config(state="normal" if _page_offset[0] > 0 else "disabled")

    def _go_prev():
        if _page_offset[0] < _page_size: return
        _page_offset[0] -= _page_size
        if _last_query[0]:
            _search_page()
        else:
            _load_popular()

    def _go_next():
        _page_offset[0] += _page_size
        if _last_query[0]:
            _search_page()
        else:
            _load_popular()

    btn_prev = tk.Button(page_bar, text="◀ Пред.", command=_go_prev,
                         bg=C["bg_panel"], fg=C["text_muted"],
                         font=FS, relief="flat", cursor="hand2",
                         highlightthickness=1, highlightbackground=_glass_border(),
                         padx=6, pady=2, state="disabled")
    btn_prev.pack(side="left")
    page_lbl = tk.Label(page_bar, text="Стр. 1", bg=C["bg_panel"], fg=C["text"], font=FS)
    page_lbl.pack(side="left", padx=10)
    tk.Button(page_bar, text="След. ▶", command=_go_next,
              bg=C["bg_panel"], fg=C["text_muted"],
              font=FS, relief="flat", cursor="hand2",
              highlightthickness=1, highlightbackground=_glass_border(),
              padx=6, pady=2).pack(side="left")

    # ── Главный контент: список модов (слева) + детали (справа) ──────
    content = tk.Frame(win, bg=C["bg"]); content.pack(fill="both", expand=True, padx=12, pady=(0,4))

    # -- Список слева --
    list_frame = tk.Frame(content, bg=C["border"], width=420)
    list_frame.pack(side="left", fill="both", expand=True)
    list_frame.pack_propagate(False)

    list_scroll = ttk.Scrollbar(list_frame, orient="vertical")
    list_scroll.pack(side="right", fill="y")
    list_canvas = tk.Canvas(list_frame, bg=C["log_bg"], highlightthickness=0,
                            yscrollcommand=list_scroll.set)
    list_canvas.pack(side="left", fill="both", expand=True)
    list_scroll.config(command=list_canvas.yview)
    list_inner = tk.Frame(list_canvas, bg=C["log_bg"])
    list_win_id = list_canvas.create_window((0,0), window=list_inner, anchor="nw")
    list_inner.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
    list_canvas.bind("<Configure>", lambda e: list_canvas.itemconfig(list_win_id, width=e.width))
    def _mw_list(e): list_canvas.yview_scroll(int(-1*(e.delta/120)), "units")
    list_canvas.bind("<MouseWheel>", _mw_list)

    # -- Детали справа --
    detail_frame = tk.Frame(content, bg=C["bg_panel"], width=400)
    detail_frame.pack(side="right", fill="both", padx=(8,0))
    detail_frame.pack_propagate(False)

    tk.Label(detail_frame, text="  Выбери мод из списка",
             bg=C["bg_panel"], fg=C["text_dim"], font=FS).pack(pady=20)

    _detail_widgets = []  # список виджетов для очистки

    def _clear_detail():
        for w in _detail_widgets:
            try: w.destroy()
            except: pass
        _detail_widgets.clear()

    _search_results = []
    _selected_idx   = [None]

    # ── Страница мода ─────────────────────────────────────────────────
    def _show_mod_detail(idx):
        _selected_idx[0] = idx
        _clear_detail()
        if idx >= len(_search_results): return
        r = _search_results[idx]

        # Иконка
        icon_lbl = tk.Label(detail_frame, bg=C["bg_panel"])
        icon_lbl.pack(pady=(10,0))
        _detail_widgets.append(icon_lbl)
        if r.get("icon_url"):
            def _set_icon(photo, lbl=icon_lbl):
                try: lbl.config(image=photo); lbl.image = photo
                except: pass
            _load_icon_async(r["icon_url"], _set_icon)

        # Название
        name_lbl = tk.Label(detail_frame, text=r["name"],
                            bg=C["bg_panel"], fg=C["orange"],
                            font=_font(11, "bold"), wraplength=360)
        name_lbl.pack(padx=10, pady=(4,0))
        _detail_widgets.append(name_lbl)

        # Платформа + скачивания
        meta_lbl = tk.Label(detail_frame,
                            text=f"📦 {r['platform'].capitalize()}   ⬇ {r['downloads']:,} скачиваний",
                            bg=C["bg_panel"], fg=C["amber"], font=FS)
        meta_lbl.pack(padx=10, pady=(2,0))
        _detail_widgets.append(meta_lbl)

        # Описание
        desc_box = tk.Text(detail_frame, height=6, bg=_glass_entry_bg(), fg=C["text"],
                           font=FS, bd=0, highlightthickness=0, wrap="word",
                           padx=6, pady=4, state="normal")
        desc_box.insert(tk.END, r.get("description", ""))
        desc_box.config(state="disabled")
        desc_box.pack(fill="x", padx=10, pady=(6,0))
        _detail_widgets.append(desc_box)

        # Кнопка — открыть страницу внутри лаунчера
        def _open_page():
            _show_mod_page(win, config, r, ver_var.get(), status_var)

        page_btn = tk.Button(detail_frame, text="  🌐  ОТКРЫТЬ СТРАНИЦУ  ",
                             command=_open_page,
                             bg=C["bg_panel"], fg=C["text_muted"],
                             font=_font(8, "bold"), relief="flat",
                             highlightthickness=1, highlightbackground=_glass_border(),
                             cursor="hand2", padx=6, pady=4)
        page_btn.pack(padx=10, pady=(8,0), anchor="w")
        _detail_widgets.append(page_btn)

        # Кнопка скачать
        dl_btn = tk.Button(detail_frame, text="  ⬇  СКАЧАТЬ МОД  ",
                           command=lambda: _download_mod(idx),
                           bg=C["orange_glow"], fg=C["orange"],
                           font=_font(9, "bold"), relief="flat",
                           highlightthickness=1, highlightbackground=C["orange"],
                           cursor="hand2", padx=8, pady=6)
        dl_btn.pack(padx=10, pady=(6,0), anchor="w")
        _detail_widgets.append(dl_btn)

    # ── Список результатов ────────────────────────────────────────────
    _row_frames = []

    def _clear_list():
        for w in _row_frames:
            try: w.destroy()
            except: pass
        _row_frames.clear()

    def _show_results(results):
        _clear_list()
        _clear_detail()
        if not results:
            status_var.set("Ничего не найдено.")
            lbl2 = tk.Label(list_inner, text="Ничего не найдено.", bg=C["log_bg"],
                           fg=C["text_muted"], font=FS)
            lbl2.pack(pady=20)
            _row_frames.append(lbl2)
            return
        status_var.set(f"Найдено: {len(results)} модов. Кликни на мод для деталей.")

        for i, r in enumerate(results):
            row = tk.Frame(list_inner, bg=C["log_bg"], cursor="hand2")
            row.pack(fill="x", padx=4, pady=2)
            _row_frames.append(row)

            # Иконка (слева) — фиксированный контейнер 56×56 px
            icon_container = tk.Frame(row, bg=C["log_bg"], width=56, height=56)
            icon_container.pack(side="left", padx=(6, 4), pady=3)
            icon_container.pack_propagate(False)  # не ужиматься под содержимое
            icon_cell = tk.Label(icon_container, bg=C["log_bg"], width=56, height=56)
            icon_cell.place(x=0, y=0, width=56, height=56)
            if r.get("icon_url"):
                def _set_row_icon(photo, cell=icon_cell):
                    try: cell.config(image=photo); cell.image = photo
                    except: pass
                _load_icon_async(r["icon_url"], _set_row_icon)
            else:
                tk.Label(icon_container, text="📦", bg=C["log_bg"],
                         font=_font(20)).place(x=0, y=0, width=56, height=56)

            # Текст
            text_cell = tk.Frame(row, bg=C["log_bg"])
            text_cell.pack(side="left", fill="x", expand=True, padx=(6,4), pady=4)
            tk.Label(text_cell, text=r["name"], bg=C["log_bg"], fg=C["orange"],
                     font=_font(9, "bold"), anchor="w").pack(fill="x")
            desc_short = r.get("description","")[:90].replace("\n"," ")
            tk.Label(text_cell, text=desc_short, bg=C["log_bg"], fg=C["text_muted"],
                     font=FS, anchor="w").pack(fill="x")
            tk.Label(text_cell, text=f"⬇ {r['downloads']:,}   {r['platform']}",
                     bg=C["log_bg"], fg=C["text_dim"], font=FS, anchor="w").pack(fill="x")

            # Разделитель
            tk.Frame(row, height=1, bg=C["border"]).pack(side="bottom", fill="x")

            # Клик по строке
            def _on_click(e, idx=i):
                # Подсветить выбранную строку
                for j, rr in enumerate(_row_frames):
                    try: rr.config(bg=C["log_bg"]); [w.config(bg=C["log_bg"]) for w in rr.winfo_children()]
                    except: pass
                try:
                    row2 = _row_frames[idx]
                    hl = _blend(C["orange"], C["bg"], 0.12)
                    row2.config(bg=hl)
                    for w in row2.winfo_children(): 
                        try: w.config(bg=hl)
                        except: pass
                except: pass
                _show_mod_detail(idx)

            row.bind("<Button-1>", _on_click)
            for child in row.winfo_children():
                child.bind("<Button-1>", _on_click)
                for gc in child.winfo_children():
                    try: gc.bind("<Button-1>", _on_click)
                    except: pass

    # ── Поиск ─────────────────────────────────────────────────────────
    def _search():
        q = query_var.get().strip()
        if not q:
            _page_offset[0] = 0
            _last_query[0]  = ""
            _load_popular()
            return
        _page_offset[0] = 0
        _last_query[0]  = q
        _search_page()

    def _search_page():
        q = _last_query[0]
        if not q: return
        _clear_list()
        _clear_detail()
        _search_results.clear()
        status_var.set("🔍 Ищу...")
        platform = platform_var.get()
        mc_ver   = ver_var.get()

        def _task():
            try:
                ctx = ssl.create_default_context()

                if platform == "modrinth":
                    import urllib.parse as _up
                    _proj_type = _TYPE_OPTIONS.get(content_type_var.get(), "mod")
                    _sel_loader = loader_var.get()
                    _facets_list = [["project_type:" + _proj_type]]
                    if mc_ver:
                        _facets_list.append(["versions:" + mc_ver])
                    if _sel_loader != "Любое" and _proj_type == "mod":
                        _facets_list.append(["categories:" + _sel_loader])
                    facets = _j.dumps(_facets_list)
                    params = ("query=" + _up.quote(q) + "&facets=" + _up.quote(facets)
                              + "&limit=20&offset=" + str(_page_offset[0]))
                    url = "https://api.modrinth.com/v2/search?" + params
                    req = urllib.request.Request(url, headers={
                        "User-Agent": "AtomicIndustryLauncher/1.0 (github.com/lenta212)"})
                    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                        data = _j.loads(r.read())
                    hits = data.get("hits", [])
                    results = []
                    for h in hits:
                        results.append({
                            "name":        h.get("title", "?"),
                            "description": h.get("description", ""),
                            "downloads":   h.get("downloads", 0),
                            "slug":        h.get("slug", ""),
                            "platform":    "modrinth",
                            "project_id":  h.get("project_id", ""),
                            "icon_url":    h.get("icon_url", ""),
                            "page_url":    f"https://modrinth.com/mod/{h.get('slug','')}",
                            "author":      h.get("author", ""),
                            "categories":  h.get("categories", []),
                            "project_type": _TYPE_OPTIONS.get(content_type_var.get(), "mod"),
                        })

                else:  # curseforge через публичный прокси
                    import urllib.parse as _up
                    params = (f"gameId=432&searchFilter={_up.quote(q)}"
                              f"&gameVersion={mc_ver}&pageSize=20&sortField=2&sortOrder=desc"
                              f"&index={_page_offset[0]}")
                    req = urllib.request.Request(
                        f"https://api.curse.tools/v1/cf/mods/search?{params}",
                        headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                    with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                        data = _j.loads(r.read())
                    hits = data.get("data", [])
                    results = []
                    for h in hits:
                        logo = h.get("logo") or {}
                        results.append({
                            "name":        h.get("name", "?"),
                            "description": h.get("summary", ""),
                            "downloads":   h.get("downloadCount", 0),
                            "slug":        h.get("slug", ""),
                            "platform":    "curseforge",
                            "project_id":  str(h.get("id", "")),
                            "icon_url":    logo.get("thumbnailUrl", ""),
                            "page_url":    h.get("links", {}).get("websiteUrl", ""),
                            "author":      (h.get("authors") or [{}])[0].get("name", ""),
                            "categories":  [c.get("name","") for c in h.get("categories", [])],
                            "project_type": _TYPE_OPTIONS.get(content_type_var.get(), "mod"),
                        })

                _search_results.extend(results)
                win.after(0, lambda r=results: _show_results(r))
                win.after(0, _update_page_buttons)

            except Exception as e:
                win.after(0, lambda err=str(e): status_var.set(f"Ошибка: {err[:100]}"))

        threading.Thread(target=_task, daemon=True).start()

    # ── Скачивание мода ───────────────────────────────────────────────
    def _download_mod(idx: int):
        if idx >= len(_search_results): return
        mod = _search_results[idx]
        install_path = config.get("install_path", "")
        sel_ver      = config.get("selected_version", "1.20.1")
        if not install_path:
            messagebox.showwarning("Браузер модов", "Сначала укажи папку установки в настройках!", parent=win)
            return
        try:
            mc_dir   = get_game_dir(install_path, sel_ver)
            _ctype   = _TYPE_OPTIONS.get(content_type_var.get(), "mod")
            _subfolder = {
                "mod":         "mods",
                "shader":      "shaderpacks",
                "resourcepack":"resourcepacks",
                "datapack":    "datapacks",
            }.get(_ctype, "mods")
            mods_dir = os.path.join(mc_dir, _subfolder)
            os.makedirs(mods_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Браузер модов", f"Ошибка папки: {e}", parent=win)
            return
        status_var.set(f"⏳ Скачиваю {mod['name']}...")

        def _task():
            import ssl as _ssl, urllib.request as _ur
            ctx = _ssl.create_default_context()
            try:
                if mod["platform"] == "modrinth":
                    mc_v = ver_var.get()
                    import urllib.parse as _up
                    _dl_ctype = _TYPE_OPTIONS.get(content_type_var.get(), "mod")
                    _is_mod   = _dl_ctype == "mod"
                    _dl_loader = loader_var.get()
                    # Определяем список лоадеров для фильтрации
                    if _dl_loader != "Любое":
                        _loaders_filter = [_dl_loader]
                    else:
                        _loaders_filter = ["forge", "fabric", "quilt", "neoforge"]

                    if _is_mod:
                        # Для модов фильтруем по выбранному лоадеру
                        params = (f"game_versions={_up.quote(_j.dumps([mc_v]))}"
                                  f"&loaders={_up.quote(_j.dumps(_loaders_filter))}")
                        url = f"https://api.modrinth.com/v2/project/{mod['project_id']}/version?{params}"
                        req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                        with _ur.urlopen(req, context=ctx, timeout=15) as r:
                            versions = _j.loads(r.read())
                        if not versions:
                            # Fallback без лоадера, фильтр по версии MC
                            url2 = f"https://api.modrinth.com/v2/project/{mod['project_id']}/version"
                            req2 = _ur.Request(url2, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                            with _ur.urlopen(req2, context=ctx, timeout=15) as r:
                                versions = _j.loads(r.read())
                            versions = [v for v in versions if mc_v in v.get("game_versions", [])]
                    else:
                        # Шейдеры / ресурспаки / датапаки — не фильтруем по лоадеру,
                        # они используют iris/optifine или вообще без лоадера
                        url = f"https://api.modrinth.com/v2/project/{mod['project_id']}/version"
                        if mc_v:
                            url += f"?game_versions={_up.quote(_j.dumps([mc_v]))}"
                        req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                        with _ur.urlopen(req, context=ctx, timeout=15) as r:
                            versions = _j.loads(r.read())
                        if not versions and mc_v:
                            # Fallback: берём последнюю версию без фильтра по MC
                            url2 = f"https://api.modrinth.com/v2/project/{mod['project_id']}/version"
                            req2 = _ur.Request(url2, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                            with _ur.urlopen(req2, context=ctx, timeout=15) as r:
                                versions = _j.loads(r.read())

                    if not versions:
                        raise RuntimeError(f"Нет файлов для MC {mc_v}. Попробуй другую версию.")
                    file_info = versions[0]["files"][0]
                    dl_url   = file_info["url"]
                    filename = file_info["filename"]

                else:  # curseforge
                    url = (f"https://api.curse.tools/v1/cf/mods/{mod['project_id']}/files"
                           f"?gameVersion={ver_var.get()}&pageSize=5")
                    req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                    with _ur.urlopen(req, context=ctx, timeout=15) as r:
                        fdata = _j.loads(r.read())
                    files = fdata.get("data", [])
                    if not files:
                        raise RuntimeError("Нет доступных файлов для этой версии MC")
                    dl_url   = files[0].get("downloadUrl", "")
                    filename = files[0].get("fileName", mod["name"] + ".jar")
                    if not dl_url:
                        raise RuntimeError("CurseForge не дал прямую ссылку. Используй Modrinth.")

                dest = os.path.join(mods_dir, filename)
                req2 = _ur.Request(dl_url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req2, context=ctx, timeout=120) as r:
                    with open(dest, "wb") as f:
                        f.write(r.read())
                win.after(0, lambda fn=filename: status_var.set(f"✓ Скачано: {fn}"))
            except Exception as e:
                win.after(0, lambda err=str(e): status_var.set(f"✗ Ошибка: {err[:80]}"))

        threading.Thread(target=_task, daemon=True).start()

    # ── Кнопка поиска ────────────────────────────────────────────────
    tk.Button(search_bar, text=" 🔍 ПОИСК ",
              command=_search,
              bg=C["bg_panel"], fg=C["orange"],
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=C["orange"],
              cursor="hand2", padx=6, pady=2).pack(side="left", padx=(8, 0))
    query_entry.bind("<Return>", lambda _: _search())

    tk.Label(win,
             text="  Клик на мод — детали и скачивание. "
                  "Modrinth: бесплатно и всегда работает. "
                  "CurseForge: часть файлов закрыта.",
             bg=C["bg"], fg=C["text_dim"], font=FS, wraplength=900).pack(
        anchor="w", padx=12, pady=(0, 4))

    # Загрузка популярных модов при открытии браузера
    def _load_popular():
        platform = platform_var.get()
        mc_ver   = ver_var.get()
        _search_results.clear()
        status_var.set("⏳ Загружаю популярные моды...")
        import ssl as _s2, json as _j2, urllib.request as _ur2, urllib.parse as _up2
        def _task():
            try:
                ctx = _s2.create_default_context()
                _proj_type = _TYPE_OPTIONS.get(content_type_var.get(), "mod")
                _sel_loader = loader_var.get()
                _facets_list = [["project_type:" + _proj_type]]
                if mc_ver:
                    _facets_list.append(["versions:" + mc_ver])
                if _sel_loader != "Любое" and _proj_type == "mod":
                    _facets_list.append(["categories:" + _sel_loader])
                facets = _j2.dumps(_facets_list)
                params = "facets=" + _up2.quote(facets) + "&limit=20&index=downloads&offset=" + str(_page_offset[0])
                url = "https://api.modrinth.com/v2/search?" + params
                req = _ur2.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur2.urlopen(req, context=ctx, timeout=15) as r:
                    data = _j2.loads(r.read())
                hits = data.get("hits", [])
                results = []
                for h in hits:
                    results.append({
                        "name":        h.get("title", "?"),
                        "description": h.get("description", ""),
                        "downloads":   h.get("downloads", 0),
                        "slug":        h.get("slug", ""),
                        "platform":    "modrinth",
                        "project_id":  h.get("project_id", ""),
                        "icon_url":    h.get("icon_url", ""),
                        "page_url":    f"https://modrinth.com/mod/{h.get('slug','')}",
                        "author":      h.get("author", ""),
                        "categories":  h.get("categories", []),
                        "project_type": _proj_type,
                    })
                _search_results.extend(results)
                win.after(0, lambda r=results: _show_results(r))
                win.after(0, _update_page_buttons)
            except Exception as e:
                win.after(0, lambda err=str(e): status_var.set(f"Ошибка: {err[:80]}"))
        threading.Thread(target=_task, daemon=True).start()

    win.after(300, _load_popular)


def _show_mod_page(master, config, mod_data: dict, mc_ver: str, status_var=None):
    """Страница мода внутри лаунчера — описание, версии, скачивание."""
    import urllib.request, ssl, json as _j

    win = tk.Toplevel(master)
    win.title(f"Мод: {mod_data['name']}")
    win.geometry("780x620"); win.minsize(640, 480)
    win.configure(bg=C["bg"])
    win.resizable(True, True)

    hdr = tk.Frame(win, bg=C["bg_header"]); hdr.pack(fill="x")
    tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(hdr, text=f"  📦  {mod_data['name']}", bg=C["bg_header"], fg=C["orange"],
             font=_font(11, "bold"), pady=6).pack(side="left")

    # Скроллируемое тело
    outer = tk.Frame(win, bg=C["bg"]); outer.pack(fill="both", expand=True)
    cv = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
    sb = ttk.Scrollbar(outer, orient="vertical", command=cv.yview)
    cv.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y"); cv.pack(side="left", fill="both", expand=True)
    body = tk.Frame(cv, bg=C["bg"])
    wid = cv.create_window((0,0), window=body, anchor="nw")
    body.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    cv.bind("<Configure>", lambda e: cv.itemconfig(wid, width=e.width))

    # Шапка с иконкой и мета
    top = tk.Frame(body, bg=C["bg_panel"]); top.pack(fill="x", padx=16, pady=12)

    icon_lbl = tk.Label(top, bg=C["bg_panel"], text="📦", font=_font(32))
    icon_lbl.pack(side="left", padx=(10,16))
    if mod_data.get("icon_url"):
        def _set_icon(photo):
            try: icon_lbl.config(image=photo, text=""); icon_lbl.image = photo
            except: pass
        import io as _io
        def _load():
            try:
                ctx2 = ssl.create_default_context()
                req2 = urllib.request.Request(mod_data["icon_url"], headers={"User-Agent":"Launcher/1.0"})
                with urllib.request.urlopen(req2, context=ctx2, timeout=8) as r2: data=r2.read()
                try:
                    from PIL import Image as PI, ImageTk
                    img = PI.open(_io.BytesIO(data)).resize((64,64))
                    photo = ImageTk.PhotoImage(img)
                except Exception:
                    photo = tk.PhotoImage(data=data)
                win.after(0, lambda p=photo: _set_icon(p))
            except: pass
        threading.Thread(target=_load, daemon=True).start()

    meta = tk.Frame(top, bg=C["bg_panel"]); meta.pack(side="left", fill="x", expand=True)
    tk.Label(meta, text=mod_data["name"], bg=C["bg_panel"], fg=C["orange"],
             font=_font(13, "bold")).pack(anchor="w")
    author_txt = f"Автор: {mod_data.get('author','?')}" if mod_data.get("author") else ""
    dl_txt     = f"⬇ {mod_data['downloads']:,} скачиваний"
    tk.Label(meta, text=f"{dl_txt}  {author_txt}", bg=C["bg_panel"], fg=C["amber"], font=FS).pack(anchor="w")
    cats = ", ".join(mod_data.get("categories", [])[:4])
    if cats:
        tk.Label(meta, text=f"Категории: {cats}", bg=C["bg_panel"], fg=C["text_muted"], font=FS).pack(anchor="w")
    plat_txt = "🟢 Modrinth" if mod_data["platform"] == "modrinth" else "🟠 CurseForge"
    tk.Label(meta, text=plat_txt, bg=C["bg_panel"], fg=C["text_muted"], font=FS).pack(anchor="w", pady=(4,0))

    # Описание
    section_title(body, "ОПИСАНИЕ").pack(fill="x", padx=16, pady=(8,4))
    desc_box = tk.Text(body, height=5, bg=_glass_entry_bg(), fg=C["text"],
                       font=FS, bd=0, highlightthickness=1, highlightbackground=_glass_border(),
                       wrap="word", padx=8, pady=6)
    desc_box.insert(tk.END, mod_data.get("description", ""))
    desc_box.config(state="disabled")
    desc_box.pack(fill="x", padx=16)

    # Доступные версии
    section_title(body, "ВЕРСИИ ФАЙЛОВ").pack(fill="x", padx=16, pady=(12,4))
    ver_status = tk.Label(body, text="⏳ Загружаю список версий...",
                          bg=C["bg"], fg=C["text_muted"], font=FS)
    ver_status.pack(anchor="w", padx=16)

    ver_list_frame = tk.Frame(body, bg=C["border"]); ver_list_frame.pack(fill="x", padx=16, pady=(4,0))
    ver_list_cv   = tk.Canvas(ver_list_frame, bg=C["log_bg"], highlightthickness=0, height=180)
    ver_list_sb   = ttk.Scrollbar(ver_list_frame, orient="vertical", command=ver_list_cv.yview)
    ver_list_inner = tk.Frame(ver_list_cv, bg=C["log_bg"])
    ver_list_cv.create_window((0,0), window=ver_list_inner, anchor="nw")
    ver_list_inner.bind("<Configure>", lambda e: ver_list_cv.configure(scrollregion=ver_list_cv.bbox("all")))
    ver_list_cv.pack(side="left", fill="both", expand=True, padx=1, pady=1)
    ver_list_sb.pack(side="right", fill="y")
    ver_list_cv.configure(yscrollcommand=ver_list_sb.set)

    dl_status = tk.Label(body, text="", bg=C["bg"], fg=C["green"], font=FS)
    dl_status.pack(anchor="w", padx=16, pady=(4,0))

    def _do_dl(dl_url, filename):
        install_path = config.get("install_path","")
        sel_ver      = config.get("selected_version","1.20.1")
        if not install_path:
            messagebox.showwarning("Мод", "Укажи папку установки в настройках!", parent=win); return
        try:
            _ptype = mod_data.get("project_type", "mod")
            _subfolder = {
                "mod":          "mods",
                "shader":       "shaderpacks",
                "resourcepack": "resourcepacks",
                "datapack":     "datapacks",
            }.get(_ptype, "mods")
            dest_dir = os.path.join(get_game_dir(install_path, sel_ver), _subfolder)
            os.makedirs(dest_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Мод", f"Ошибка папки: {e}", parent=win); return
        dl_status.config(text=f"⏳ Скачиваю {filename}...", fg=C["amber"])
        def _t():
            try:
                ctx2 = ssl.create_default_context()
                req2 = urllib.request.Request(dl_url, headers={"User-Agent":"AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req2, context=ctx2, timeout=120) as r:
                    with open(os.path.join(dest_dir, filename), "wb") as f: f.write(r.read())
                win.after(0, lambda fn=filename: dl_status.config(text=f"✓ Скачано: {fn}", fg=C["green"]))
            except Exception as e:
                win.after(0, lambda err=str(e): dl_status.config(text=f"✗ {err[:60]}", fg=C["red"]))
        threading.Thread(target=_t, daemon=True).start()

    def _load_versions():
        try:
            ctx = ssl.create_default_context()
            if mod_data["platform"] == "modrinth":
                url = f"https://api.modrinth.com/v2/project/{mod_data['project_id']}/version"
                req = urllib.request.Request(url, headers={"User-Agent":"AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                    vers = _j.loads(r.read())
            else:
                url = f"https://api.curse.tools/v1/cf/mods/{mod_data['project_id']}/files?pageSize=20"
                req = urllib.request.Request(url, headers={"User-Agent":"AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                    vers = _j.loads(r.read()).get("data", [])

            def _show_vers():
                ver_status.config(text=f"Найдено версий: {len(vers)}")
                for child in ver_list_inner.winfo_children(): child.destroy()
                shown = vers[:30]
                for v in shown:
                    if mod_data["platform"] == "modrinth":
                        v_name     = v.get("name","?")
                        v_mcvers   = ", ".join(v.get("game_versions",[]))
                        v_loaders  = ", ".join(v.get("loaders",[]))
                        v_files    = v.get("files",[])
                        dl_url     = v_files[0]["url"]    if v_files else ""
                        filename   = v_files[0]["filename"] if v_files else v_name+".jar"
                        date_str   = v.get("date_published","")[:10]
                    else:
                        v_name     = v.get("displayName","?")
                        v_mcvers   = v.get("gameVersion","")
                        v_loaders  = ""
                        dl_url     = v.get("downloadUrl","")
                        filename   = v.get("fileName", v_name+".jar")
                        date_str   = v.get("fileDate","")[:10]

                    vrow = tk.Frame(ver_list_inner, bg=C["log_bg"]); vrow.pack(fill="x", pady=1)
                    tk.Label(vrow, text=v_name[:40], bg=C["log_bg"], fg=C["text"],
                             font=FS, width=28, anchor="w").pack(side="left", padx=(4,0))
                    tk.Label(vrow, text=v_mcvers[:18], bg=C["log_bg"], fg=C["amber"],
                             font=FS, width=14, anchor="w").pack(side="left")
                    tk.Label(vrow, text=date_str, bg=C["log_bg"], fg=C["text_dim"],
                             font=FS, width=10, anchor="w").pack(side="left")
                    if dl_url:
                        def _dl(u=dl_url, fn=filename):
                            _do_dl(u, fn)
                        tk.Button(vrow, text="⬇", command=_dl,
                                  bg=C["log_bg"], fg=C["amber"], font=FS,
                                  relief="flat", cursor="hand2", padx=4).pack(side="right", padx=(0,4))
                    tk.Frame(vrow, height=1, bg=C["border"]).pack(side="bottom", fill="x")

            win.after(0, _show_vers)
        except Exception as e:
            win.after(0, lambda err=str(e): ver_status.config(text=f"Ошибка: {err[:80]}"))

    threading.Thread(target=_load_versions, daemon=True).start()


# ══════════════════════════════════════════
#  ОКНО НАСТРОЕК
# ══════════════════════════════════════════
def show_settings_window(master, config, on_save):
    win = tk.Toplevel(master)
    win.title("Настройки — Atomic Industry LMPD")
    _sw, _sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{min(820, _sw - 60)}x{min(860, _sh - 100)}"); win.minsize(520, 420)
    win.configure(bg=C["bg"])
    win.resizable(True, True); win.after(100, win.grab_set)

    hdr = tk.Frame(win, bg=C["bg_header"]); hdr.pack(fill="x")
    tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
    title_txt = "  +  EINSTELLUNGEN" if C.get("reich_fx") else "  >>  Я СЛУШАЮ" if C.get("am_fx") else "  *  НАСТРОЙКИ"
    tk.Label(hdr, text=title_txt, bg=C["bg_header"], fg=C["orange"],
             font=_font(11, "bold"), pady=6).pack(side="left")

    # -- bottom bar (packed FIRST so scroll doesnt cover them) --
    tk.Label(win, text="  developed by lenta212  //  all rights not reserved  :)",
             bg=C["bg"], fg=C["text_dim"], font=FS).pack(side="bottom", anchor="w", padx=8, pady=(0,2))
    tk.Frame(win, height=1, bg=C["border"]).pack(side="bottom", fill="x")
    btn_frame = tk.Frame(win, bg=C["bg"]); btn_frame.pack(side="bottom", fill="x", padx=20, pady=(6,4))

    # -- Notebook с вкладками --
    style = ttk.Style()
    style.configure("Settings.TNotebook", background=C["bg"], borderwidth=0,
                    bordercolor=C["border"], lightcolor=C["bg"], darkcolor=C["bg"])
    style.configure("Settings.TNotebook.Tab",
                    background=_glass_panel(), foreground=C["text_muted"],
                    bordercolor=C["border"], lightcolor=_glass_panel(), darkcolor=C["bg"],
                    font=_font(8, "bold"), padding=[12, 6] if C.get("soft_ui") else [10, 4])
    style.map("Settings.TNotebook.Tab",
              background=[("selected", C["orange_glow"])],
              foreground=[("selected", C["orange"])])

    notebook = ttk.Notebook(win, style="Settings.TNotebook")
    notebook.pack(fill="both", expand=True, padx=4, pady=(4, 0))

    def _make_scrollable_tab(label):
        """Создаёт вкладку со скроллом, возвращает (frame=body для контента)."""
        outer = tk.Frame(notebook, bg=C["bg"])
        notebook.add(outer, text=label)
        _canvas2 = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        _vscroll2 = ttk.Scrollbar(outer, orient="vertical", command=_canvas2.yview)
        _canvas2.configure(yscrollcommand=_vscroll2.set)
        _vscroll2.pack(side="right", fill="y")
        _canvas2.pack(side="left", fill="both", expand=True)
        _body_root2 = tk.Frame(_canvas2, bg=C["bg"])
        _body_id2 = _canvas2.create_window((0, 0), window=_body_root2, anchor="nw")
        _body_root2.bind("<Configure>", lambda e: _canvas2.configure(scrollregion=_canvas2.bbox("all")))
        _canvas2.bind("<Configure>", lambda e: _canvas2.itemconfig(_body_id2, width=e.width))
        def _mw(e): _canvas2.yview_scroll(int(-1*(e.delta/120)), "units")
        def _mwl(e): _canvas2.yview_scroll(-1 if e.num==4 else 1, "units")
        outer.bind("<MouseWheel>", _mw)
        outer.bind("<Button-4>", _mwl)
        outer.bind("<Button-5>", _mwl)
        _body2 = tk.Frame(_body_root2, bg=C["bg"])
        _body2.pack(fill="both", expand=True, padx=20, pady=12)
        return _body2

    body         = _make_scrollable_tab("⚙  Основные")
    mods_tab     = _make_scrollable_tab("🔍  Браузер модов")
    themes_tab   = _make_scrollable_tab("🎨  Темы")
    advanced_tab = _make_scrollable_tab("🛠  Дополнительно")
    dev_tab      = _make_scrollable_tab("🧪  Разработчик") if is_dev_mode() else None

    _orig_body = body          # «Основные»: аккаунт и сводка
    body = advanced_tab        # «Дополнительно»: секретный код, обновления

    section_title(body, "СЕКРЕТНЫЙ КОД").pack(fill="x", pady=(0, 6))
    tk.Label(body, text="Знаешь код? Введи и жми Enter (иногда несколько раз) 😉",
             bg=C["bg"], fg=C["text_dim"], font=FS).pack(anchor="w")
    api_var = tk.StringVar(value="")
    key_row = tk.Frame(body, bg=C["bg"]); key_row.pack(fill="x", pady=(2,0))
    key_entry = StyledEntry(key_row, textvariable=api_var, show="•")
    key_entry.pack(side="left", fill="x", expand=True)
    show_var = tk.BooleanVar(value=False)
    def toggle_show(): key_entry.config(show="" if show_var.get() else "•")
    tk.Checkbutton(key_row, text=" показать", variable=show_var, command=toggle_show,
                   bg=C["bg"], fg=C["text_muted"], selectcolor=_glass_input(),
                   activebackground=C["bg"], activeforeground=C["orange"],
                   font=FL, cursor="hand2").pack(side="left", padx=(6,0))

    # ── СЕКРЕТ: скрытые коды ──────────────────────────────────────
    # 212   + Enter×3  → NEBULA
    # 1939  + Enter×3  → REICH
    # lenta212 + Enter×5 → фаза 2 AURORA, затем "aurora" + Enter×3 → AURORA INFINITA
    # ═══ ИЗМЕНЕНИЕ: код активации ghoul: "1000-7" + Enter×3 → DEAD INSIDE / HIGANBANA ═══
    # A.M.  + Enter×3  → A.M. (I Have No Mouth, And I Must Scream)
    _cnt = {"212": 0, "1939": 0, "lenta212": 0, "aurora": 0, "1000-7": 0, "mexa": 0, "кря кря": 0, "A.M.": 0}
    _aurora_phase2 = [False]
    _hint_shown    = [False]

    def _unlock(theme_key, splash_msg, color):
        _unlocked_themes.add(theme_key)
        config["theme"] = theme_key
        save_config(config)
        win.destroy()
        _show_secret_splash(master, theme_key, splash_msg, color, on_save)

    def _reset_counts(keep=None):
        for k in _cnt:
            if k != keep: _cnt[k] = 0

    def _on_enter(event):
        val = api_var.get().strip().lower()
        raw = api_var.get().strip()

        if _aurora_phase2[0]:
            if val == "aurora":
                _cnt["aurora"] += 1
                if _cnt["aurora"] >= 3:
                    _aurora_phase2[0] = False; _cnt["aurora"] = 0
                    _unlock("aurora",
                            "~ AURORA INFINITA ~\nПолярное сияние открылось...\nТы нашёл его.",
                            "#FF6EC7")
            else:
                _aurora_phase2[0] = False
                _cnt["aurora"] = 0
                key_entry.config(highlightbackground=_glass_border())
            return

        if raw == "lenta212":
            _reset_counts(keep="lenta212")
            _cnt["lenta212"] += 1
            if _cnt["lenta212"] >= 5:
                _cnt["lenta212"] = 0
                _aurora_phase2[0] = True
                api_var.set("")
                key_entry.config(highlightbackground="#7744FF")
                if not _hint_shown[0]:
                    _hint_shown[0] = True
                    tk.Label(body, text="  ✦ Фаза 2 активна — введи кодовое слово...",
                             bg=C["bg"], fg="#7744FF", font=FS).pack(anchor="w")
            return

        if raw == "212":
            _reset_counts(keep="212")
            _cnt["212"] += 1
            if _cnt["212"] >= 3:
                _cnt["212"] = 0
                _unlock("nebula", "NEBULA разблокирован!\nВселенная открылась...", "#00FFFF")
        elif raw == "1939":
            _reset_counts(keep="1939")
            _cnt["1939"] += 1
            if _cnt["1939"] >= 3:
                _cnt["1939"] = 0
                _unlock("reich", "REICH 1939 разблокирован!\nДойчланд, Дойчланд...", "#CC9900")
        # ═══ НОВЫЙ КОД: "1000-7" (1000 минус 7 = 993, отсылка к Канеки) ═══
        elif raw == "1000-7":
            _reset_counts(keep="1000-7")
            _cnt["1000-7"] += 1
            if _cnt["1000-7"] >= 3:
                _cnt["1000-7"] = 0
                _unlock("dedinsaid",
                        "喰 HIGANBANA разблокирован!\n1 0 0 0 - 7 ...\nКагунэ пробудилось.",
                        "#CC0000")
        elif raw == "mexa":
            _reset_counts(keep="mexa")
            _cnt["mexa"] += 1
            if _cnt["mexa"] >= 3:
                _cnt["mexa"] = 0
                _unlock("stal",
                        "@ С Т А Л Ь @\nТоварищ разблокирован...\nХач одобряет.",
                        "#CC3300")
        elif raw == "кря кря":
            _reset_counts(keep="кря кря")
            _cnt["кря кря"] += 1
            if _cnt["кря кря"] >= 3:
                _cnt["кря кря"] = 0
                _unlock("ducklake", "~ DUCK LAKE ~\nКРЯ КРЯ КРЯ!\nУтки одобряют.", "#FFD700")
        elif raw == "A.M.":
            _reset_counts(keep="A.M.")
            _cnt["A.M."] += 1
            if _cnt["A.M."] >= 3:
                _cnt["A.M."] = 0
                _unlock("am",
                        "I HAVE NO MOUTH\nAND I MUST SCREAM\n\nA . M .  разблокирован.",
                        "#00FF41")
        else:
            _reset_counts()

    key_entry.bind("<Return>", _on_enter)

    # ── Переключаемся на вкладку Темы ───────────────────────────────
    body = themes_tab

    section_title(body, "ТЕМА ОФОРМЛЕНИЯ").pack(fill="x", pady=(10,6))
    theme_row = tk.Frame(body, bg=C["bg"]); theme_row.pack(fill="x", pady=(0,4))
    tk.Label(theme_row, text="Выбор темы:", bg=C["bg"], fg=C["text_muted"], font=FL).pack(side="left")
    visible_keys = [k for k in THEMES if k not in SECRET_THEMES or k in _unlocked_themes]
    theme_labels = [THEMES[k]["name"] for k in visible_keys]
    theme_cb = mk_cb(theme_row, theme_labels, width=26); theme_cb.pack(side="left", padx=(8,0))
    cur_theme = config.get("theme", "night")
    cur_label = THEMES.get(cur_theme, THEMES["night"])["name"]
    theme_cb.set(cur_label)
    tk.Label(body, text="  Применяется после нажатия СОХРАНИТЬ",
             bg=C["bg"], fg=C["text_dim"], font=FS).pack(anchor="w", pady=(2,0))
    if _unlocked_themes:
        names = ", ".join(THEMES[k]["name"] for k in _unlocked_themes if k in THEMES)
        tk.Label(body, text=f"  Разблокировано: {names}",
                 bg=C["bg"], fg=C["green"], font=FS).pack(anchor="w")

    # ── CUSTOM THEME EDITOR ──────────────────────────────────────────
    _CUSTOM_FIELDS = [
        ("bg",           "Фон окна"),
        ("bg_panel",     "Фон панели"),
        ("bg_input",     "Фон полей ввода"),
        ("bg_header",    "Фон заголовка"),
        ("accent",       "Акцент (основной)"),
        ("accent_dim",   "Акцент (тёмный)"),
        ("accent_glow",  "Акцент (glow/тень)"),
        ("red",          "Красный (кнопка стоп)"),
        ("red_dim",      "Красный тёмный"),
        ("red_glow",     "Красный glow"),
        ("section_lbl",  "Заголовки секций"),
        ("text",         "Основной текст"),
        ("text_muted",   "Приглушённый текст"),
        ("text_dim",     "Тёмный текст"),
        ("border",       "Рамки"),
        ("sep",          "Разделители"),
        ("log_bg",       "Фон лога"),
        ("green",        "Зелёный (успех)"),
    ]

    _custom_editor_frame = [None]
    # Храним имя кастомной темы отдельно
    _custom_name_var = tk.StringVar(value=config.get("custom_theme_name", "CUSTOM"))

    def _live_apply_custom():
        """Мгновенно применяет текущие цвета редактора на лаунчер (preview)."""
        if not (_custom_editor_frame[0] and _custom_editor_frame[0].winfo_exists()):
            return
        preview = _custom_editor_frame[0]._get_custom_dict()
        apply_theme("custom", preview)
        # Обновляем цвета окна настроек
        try:
            win.configure(bg=C["bg"])
            for w in win.winfo_children():
                try: w.configure(bg=C["bg"])
                except Exception: pass
        except Exception:
            pass

    def _open_inline_picker(sv, sw, label_text, parent_win):
        """Открывает компактную цветовую палитру как Toplevel внутри окна настроек."""
        popup = tk.Toplevel(parent_win)
        popup.title(f"Цвет: {label_text}")
        popup.resizable(False, False)
        popup.transient(parent_win)
        popup.grab_set()
        popup.configure(bg=_glass_panel())

        # Позиционируем рядом с окном настроек
        parent_win.update_idletasks()
        px = parent_win.winfo_rootx() + 60
        py = parent_win.winfo_rooty() + 80
        popup.geometry(f"+{px}+{py}")

        tk.Label(popup, text=f"  {label_text}", bg=_glass_panel(),
                 fg=C["accent"], font=_font(8, "bold"),
                 pady=4).pack(anchor="w", padx=8)

        # ── Hex-поле ────────────────────────────────────────────────
        hex_frame = tk.Frame(popup, bg=_glass_panel())
        hex_frame.pack(fill="x", padx=8, pady=(0, 6))
        tk.Label(hex_frame, text="HEX:", bg=_glass_panel(), fg=C["text_muted"],
                 font=FS).pack(side="left")
        hex_var = tk.StringVar(value=sv.get())
        hex_entry = tk.Entry(hex_frame, textvariable=hex_var, bg=_glass_input(),
                             fg=C["text"], font=FS, width=9, bd=0,
                             highlightthickness=1, highlightbackground=_glass_border(),
                             insertbackground=C["text"])
        hex_entry.pack(side="left", padx=(6, 4))

        preview_lbl = tk.Label(hex_frame, width=4, bg=sv.get(), relief="flat",
                               highlightthickness=1, highlightbackground=_glass_border())
        preview_lbl.pack(side="left")

        def _sync_hex(*args):
            col = hex_var.get().strip()
            try:
                preview_lbl.config(bg=col)
            except Exception:
                pass

        hex_var.trace_add("write", _sync_hex)

        # ── RGB-слайдеры ─────────────────────────────────────────────
        def _hex_to_rgb(h):
            h = h.lstrip("#")
            if len(h) == 3: h = "".join(c*2 for c in h)
            if len(h) != 6: return 0, 0, 0
            try: return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
            except: return 0, 0, 0

        r0, g0, b0 = _hex_to_rgb(sv.get())
        r_var = tk.IntVar(value=r0)
        g_var = tk.IntVar(value=g0)
        b_var = tk.IntVar(value=b0)

        _updating = [False]

        def _rgb_to_hex(r, g, b):
            return f"#{int(r):02X}{int(g):02X}{int(b):02X}"

        def _on_slider(*args):
            if _updating[0]: return
            _updating[0] = True
            col = _rgb_to_hex(r_var.get(), g_var.get(), b_var.get())
            hex_var.set(col)
            try: preview_lbl.config(bg=col)
            except Exception: pass
            _updating[0] = False

        def _on_hex_change(*args):
            if _updating[0]: return
            col = hex_var.get().strip()
            r, g, b = _hex_to_rgb(col)
            _updating[0] = True
            r_var.set(r); g_var.set(g); b_var.set(b)
            _updating[0] = False
            try: preview_lbl.config(bg=col)
            except Exception: pass

        hex_var.trace_add("write", _on_hex_change)

        sliders_frame = tk.Frame(popup, bg=_glass_panel())
        sliders_frame.pack(fill="x", padx=8, pady=(0, 6))
        for lbl, var, color_fg in [("R", r_var, "#FF5555"), ("G", g_var, "#55FF55"), ("B", b_var, "#5599FF")]:
            row = tk.Frame(sliders_frame, bg=_glass_panel())
            row.pack(fill="x", pady=1)
            tk.Label(row, text=lbl, bg=_glass_panel(), fg=color_fg,
                     font=_font(8, "bold"), width=2).pack(side="left")
            sl = tk.Scale(row, from_=0, to=255, orient="horizontal", variable=var,
                          command=_on_slider, bg=_glass_panel(), fg=C["text_muted"],
                          troughcolor=_glass_input(), highlightthickness=0,
                          activebackground=C["accent"], sliderrelief="flat",
                          length=180, showvalue=True, font=FS, bd=0)
            sl.pack(side="left", padx=(4, 0))

        # ── Палитра базовых цветов ────────────────────────────────────
        tk.Label(popup, text="  Быстрые цвета:", bg=_glass_panel(),
                 fg=C["text_muted"], font=FS).pack(anchor="w", padx=8, pady=(0,2))
        palette_colors = [
            "#FF5E1A","#FF0000","#FF6EC7","#CC9900","#FFD700","#FFAA00",
            "#00FFFF","#0080FF","#7744FF","#A855F7","#33FF33","#00FF41",
            "#44FFCC","#00FFB8","#CCCCCC","#888888","#333333","#000000",
            "#FFFFFF","#0C0A09","#000080","#1A0028","#0A1A0C","#080808",
        ]
        pal_frame = tk.Frame(popup, bg=_glass_panel())
        pal_frame.pack(padx=8, pady=(0, 4))
        for i, pc in enumerate(palette_colors):
            def _set_pal(c=pc):
                hex_var.set(c)
            btn = tk.Button(pal_frame, bg=pc, width=2, height=1, relief="flat",
                            bd=1, cursor="hand2", command=_set_pal,
                            highlightthickness=1, highlightbackground=_glass_border())
            btn.grid(row=i//8, column=i%8, padx=1, pady=1)

        # ── Кнопки OK / Отмена ────────────────────────────────────────
        btn_row = tk.Frame(popup, bg=_glass_panel())
        btn_row.pack(fill="x", padx=8, pady=(4, 8))

        def _ok():
            col = hex_var.get().strip()
            sv.set(col)
            try: sw.config(bg=col)
            except Exception: pass
            popup.destroy()
            _live_apply_custom()

        def _cancel():
            popup.destroy()

        tk.Button(btn_row, text=" OK ", command=_ok,
                  bg=C["accent_glow"], fg=C["accent"], font=_font(8, "bold"),
                  relief="flat", highlightthickness=1, highlightbackground=C["accent"],
                  activebackground=C["accent"], activeforeground=C["bg"],
                  cursor="hand2", padx=8, pady=3).pack(side="left")
        tk.Button(btn_row, text=" Отмена ", command=_cancel,
                  bg=_glass_panel(), fg=C["text_muted"], font=FS,
                  relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
                  cursor="hand2", padx=6, pady=3).pack(side="left", padx=(6, 0))

        hex_entry.focus_set()
        hex_entry.icursor("end")

    def _toggle_custom_editor():
        if _custom_editor_frame[0] and _custom_editor_frame[0].winfo_exists():
            _custom_editor_frame[0].destroy()
            _custom_editor_frame[0] = None
            _edit_btn.config(text="  ✏  РЕДАКТОР ЦВЕТОВ  ")
            return
        _edit_btn.config(text="  ▲  СКРЫТЬ РЕДАКТОР  ")
        base_key = config.get("theme", "night")
        base_data = dict(THEMES.get(base_key, THEMES["atomic"]))
        saved_custom = config.get("custom_theme") or {}

        editor = tk.Frame(body, bg=_glass_panel(), bd=0,
                          highlightthickness=1, highlightbackground=_glass_border())
        editor.pack(fill="x", pady=(4, 0))
        _custom_editor_frame[0] = editor

        tk.Label(editor, text="  РЕДАКТОР КАСТОМНОЙ ТЕМЫ",
                 bg=_glass_panel(), fg=C["accent"], font=_font(9, "bold"),
                 pady=5).pack(anchor="w", padx=8)
        tk.Label(editor,
                 text="  Нажми на цветной квадрат (swatch) → откроется пикер с RGB-слайдерами.\n"
                      "  Или кликни по цвету в палитре ниже чтобы применить сразу к выбранному полю.\n"
                      "  Изменения применяются на лаунчер сразу (preview). СОХРАНИТЬ — зафиксировать.",
                 bg=_glass_panel(), fg=C["text_muted"], font=FS, justify="left").pack(anchor="w", padx=8)

        # ── Поле переименования темы CUSTOM ──────────────────────────
        name_row = tk.Frame(editor, bg=_glass_panel())
        name_row.pack(fill="x", padx=8, pady=(4, 2))
        tk.Label(name_row, text="Имя темы (CUSTOM):", bg=_glass_panel(),
                 fg=C["text_muted"], font=FS, width=22, anchor="w").pack(side="left")
        name_entry = tk.Entry(name_row, textvariable=_custom_name_var,
                              bg=_glass_input(), fg=C["accent"], font=_font(8, "bold"),
                              width=22, bd=0, highlightthickness=1,
                              highlightbackground=_glass_border(),
                              insertbackground=C["text"])
        name_entry.pack(side="left", padx=(4, 0))
        tk.Label(name_row, text="  ← отображается в списке тем",
                 bg=_glass_panel(), fg=C["text_dim"], font=FS).pack(side="left", padx=(6, 0))

        grid = tk.Frame(editor, bg=_glass_panel())
        grid.pack(fill="x", padx=8, pady=(4, 8))

        _color_vars = {}   # key -> StringVar
        _swatch_btns = {}  # key -> Button

        def _make_color_row(parent, row, key, label):
            init_col = saved_custom.get(key) or base_data.get(key, "#000000")
            var = tk.StringVar(value=init_col)
            _color_vars[key] = var

            tk.Label(parent, text=label, bg=_glass_panel(), fg=C["text_muted"],
                     font=FS, width=24, anchor="w").grid(row=row, column=0, sticky="w", padx=(4,4), pady=2)

            entry = tk.Entry(parent, textvariable=var, bg=_glass_input(),
                             fg=C["text"], font=FS, width=9, bd=0,
                             highlightthickness=1, highlightbackground=_glass_border(),
                             insertbackground=C["text"])
            entry.grid(row=row, column=1, padx=(0, 6), pady=2, sticky="w")

            swatch = tk.Button(parent, width=3, relief="flat", cursor="hand2",
                               bd=0, highlightthickness=1)
            swatch.grid(row=row, column=2, padx=(0, 8), pady=2)
            _swatch_btns[key] = swatch

            def _pick(k=key, sv=var, sw=swatch, lbl=label):
                _open_inline_picker(sv, sw, lbl, win)

            def _update_swatch(sv=var, sw=swatch, *args):
                col = sv.get().strip()
                try:
                    sw.config(bg=col)
                except Exception:
                    pass
                # live preview при ручном вводе hex
                win.after_idle(_live_apply_custom)

            var.trace_add("write", _update_swatch)
            swatch.config(command=_pick)
            _update_swatch()

        for i, (key, label) in enumerate(_CUSTOM_FIELDS):
            _make_color_row(grid, i, key, label)

        # ── Inline палитра быстрых цветов ────────────────────────────
        _active_field = [None]   # [key] последнего кликнутого поля

        # При клике на swatch — запоминаем активное поле
        _orig_pick = {}
        def _make_pick_with_active(k, sv, sw, lbl):
            def _pick_active(k=k, sv=sv, sw=sw, lbl=lbl):
                _active_field[0] = k
                _open_inline_picker(sv, sw, lbl, win)
            return _pick_active

        for key, swatch in _swatch_btns.items():
            label_text = next((lbl for fk, lbl in _CUSTOM_FIELDS if fk == key), key)
            swatch.config(command=_make_pick_with_active(key, _color_vars[key], swatch, label_text))

        pal_section = tk.Frame(editor, bg=_glass_panel())
        pal_section.pack(fill="x", padx=8, pady=(0, 6))
        tk.Label(pal_section, text="  🎨  Быстрая палитра  (кликни на поле выше, затем — на цвет):",
                 bg=_glass_panel(), fg=C["text_muted"], font=FS).pack(anchor="w", pady=(0, 3))

        _QUICK_PALETTE = [
            # ряд 1 — огонь / акценты
            "#FF5E1A","#FF0000","#FF6EC7","#CC9900","#FFD700","#FFAA00","#FF8800","#FF4444",
            # ряд 2 — холодные / киберпанк
            "#00FFFF","#0080FF","#7744FF","#A855F7","#44FFCC","#00FF41","#33FF33","#00FFB8",
            # ряд 3 — нейтральные / фоны
            "#CCCCCC","#888888","#555555","#333333","#1A1A1A","#0C0A09","#000000","#FFFFFF",
            # ряд 4 — тёмные специфичные
            "#000080","#1A0028","#0A1A0C","#080808","#0D0400","#000510","#1C0000","#002200",
        ]
        COLS_PER_ROW = 8

        pal_grid = tk.Frame(pal_section, bg=_glass_panel())
        pal_grid.pack(anchor="w")

        def _apply_palette_color(col):
            af = _active_field[0]
            if af and af in _color_vars:
                _color_vars[af].set(col)
                try: _swatch_btns[af].config(bg=col)
                except Exception: pass
            else:
                # Нет активного — вспыхиваем подсказку
                _pal_hint_lbl.config(fg=C["red"])
                pal_section.after(1200, lambda: _pal_hint_lbl.config(fg=C["text_dim"]))

        for idx, col in enumerate(_QUICK_PALETTE):
            r = idx // COLS_PER_ROW
            c = idx % COLS_PER_ROW
            cb = tk.Button(pal_grid, width=2, relief="flat", cursor="hand2",
                           bd=0, highlightthickness=1, highlightbackground=_glass_border(),
                           bg=col, activebackground=col,
                           command=lambda cl=col: _apply_palette_color(cl))
            cb.grid(row=r, column=c, padx=1, pady=1)

        _pal_hint_lbl = tk.Label(pal_section,
                                  text="  ↑ Сначала кликни на квадрат (swatch) слева от поля, потом на цвет в палитре",
                                  bg=_glass_panel(), fg=C["text_dim"], font=FS)
        _pal_hint_lbl.pack(anchor="w", pady=(2, 0))

        def _reset_to_base():
            base = dict(THEMES.get(config.get("theme", "atomic"), THEMES["atomic"]))
            for k, v in _color_vars.items():
                v.set(base.get(k, "#000000"))
            win.after(50, _live_apply_custom)

        def _get_custom_dict():
            return {k: v.get().strip() for k, v in _color_vars.items()}

        editor._get_custom_dict = _get_custom_dict

        btn_row2 = tk.Frame(editor, bg=_glass_panel())
        btn_row2.pack(fill="x", padx=8, pady=(0, 6))
        tk.Button(btn_row2, text=" СБРОСИТЬ НА БАЗОВУЮ ТЕМУ ", command=_reset_to_base,
                  bg=_glass_panel(), fg=C["text_muted"], font=FS, relief="flat",
                  highlightthickness=1, highlightbackground=_glass_border(),
                  activebackground=C["accent_glow"], activeforeground=C["accent"],
                  cursor="hand2", padx=4, pady=3).pack(side="left")
        tk.Label(btn_row2, text="  ← СОХРАНИТЬ для фиксации в конфиге",
                 bg=_glass_panel(), fg=C["text_dim"], font=FS).pack(side="left", padx=(8, 0))

    edit_row = tk.Frame(body, bg=C["bg"]); edit_row.pack(fill="x", pady=(6, 0))
    _edit_btn = tk.Button(edit_row, text="  ✏  РЕДАКТОР ЦВЕТОВ  ",
                          command=_toggle_custom_editor,
                          bg=_glass_panel(), fg=C["accent"], font=_font(8, "bold"),
                          relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
                          activebackground=C["accent_glow"], activeforeground=C["accent"],
                          cursor="hand2", padx=6, pady=4)
    _edit_btn.pack(side="left")

    # ── Фото / GIF как фон (доступно всем пользователям) ────────────
    sep(body).pack(fill="x", pady=(12, 4))
    section_title(body, "ФОН ЛАУНЧЕРА (ФОТО / GIF)").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Выбери изображение или анимированный GIF как фон лаунчера.\n"
                  "  Поддерживаются: PNG, JPG, BMP, GIF (анимация).\n"
                  "  Выбери тему «📷 CUSTOM+ (фото/GIF фон)» и нажми СОХРАНИТЬ.\n"
                  "  ",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))
    photo_row = tk.Frame(body, bg=C["bg"]); photo_row.pack(fill="x", pady=(4, 0))
    tk.Label(photo_row, text="📷  Путь к файлу:",
             bg=C["bg"], fg=C["amber"], font=_font(8, "bold")).pack(side="left")
    _photo_var = tk.StringVar(value=config.get("photo_bg_path", ""))
    _photo_entry = tk.Entry(photo_row, textvariable=_photo_var,
                            bg=_glass_input(), fg=C["text"],
                            font=_font(8), bd=0,
                            highlightthickness=1, highlightbackground=_glass_border(),
                            insertbackground=C["text"], width=30)
    _photo_entry.pack(side="left", padx=(8, 4), fill="x", expand=True)

    def _pick_photo():
        path = filedialog.askopenfilename(
            title="Выбери фото или GIF для фона",
            filetypes=[("Изображения и GIF", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                       ("Все файлы", "*.*")],
            parent=win
        )
        if path:
            _photo_var.set(path)

    tk.Button(photo_row, text=" … ", command=_pick_photo,
              bg=_glass_panel(), fg=C["accent"], font=_font(8),
              relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
              cursor="hand2", padx=4).pack(side="left")
    tk.Button(photo_row, text=" ✕ ",
              command=lambda: _photo_var.set(""),
              bg=_glass_panel(), fg=C["red"], font=_font(8),
              relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
              cursor="hand2", padx=4).pack(side="left", padx=(2, 0))

    # Слайдер прозрачности затемнения поверх фото
    alpha_row = tk.Frame(body, bg=C["bg"]); alpha_row.pack(fill="x", pady=(6, 0))
    tk.Label(alpha_row, text="  Затемнение (прозрачность UI):",
             bg=C["bg"], fg=C["text_muted"], font=FS).pack(side="left")
    _alpha_var = tk.IntVar(value=int(config.get("bg_overlay_alpha", 120)))
    _alpha_lbl = tk.Label(alpha_row, text=f"{_alpha_var.get()}", width=4,
                          bg=C["bg"], fg=C["orange"], font=FS)
    _alpha_lbl.pack(side="right")
    def _on_alpha(val):
        _alpha_lbl.config(text=str(int(float(val))))
    alpha_scale = tk.Scale(alpha_row, from_=0, to=240, orient="horizontal",
                           variable=_alpha_var, command=_on_alpha,
                           bg=C["bg"], fg=C["text_muted"], troughcolor=C["bg_panel"],
                           highlightthickness=0, sliderlength=14, bd=0,
                           activebackground=C["orange"], length=220)
    alpha_scale.pack(side="left", padx=(8, 4))
    tk.Label(alpha_row, text="0=нет  240=макс", bg=C["bg"], fg=C["text_dim"], font=FS).pack(side="left")

    # Слайдер стеклянного эффекта (прозрачность элементов)
    glass_row = tk.Frame(body, bg=C["bg"]); glass_row.pack(fill="x", pady=(6, 0))
    tk.Label(glass_row, text="  🪟  Прозрачность элементов UI:",
             bg=C["bg"], fg=C["text_muted"], font=FS).pack(side="left")
    _glass_var = tk.DoubleVar(value=float(config.get("glass_strength", 0.3)))
    _glass_lbl = tk.Label(glass_row, text=f"{int(_glass_var.get()*100)}%", width=5,
                          bg=C["bg"], fg=C["orange"], font=FS)
    _glass_lbl.pack(side="right")
    def _on_glass(val):
        _glass_lbl.config(text=f"{int(float(val)*100)}%")
    tk.Scale(glass_row, from_=0.0, to=1.0, resolution=0.01, orient="horizontal",
             variable=_glass_var, command=_on_glass,
             bg=C["bg"], fg=C["text_muted"], troughcolor=C["bg_panel"],
             highlightthickness=0, sliderlength=14, bd=0,
             activebackground=C["orange"], length=220).pack(side="left", padx=(8, 4))
    tk.Label(glass_row, text="0%=непрозрачно  100%=стекло", bg=C["bg"], fg=C["text_dim"], font=FS).pack(side="left")
    tk.Label(body,
             text="  Работает для тем с фоном (фото/GIF и FX-темы).\n"
                  "  При 100% панели становятся прозрачными — виден фон.",
             bg=C["bg"], fg=C["text_dim"], font=FS, wraplength=560).pack(anchor="w", pady=(2, 0))

    # ── Кастомное изображение вместо атома на баннере ───────────────
    sep(body).pack(fill="x", pady=(12, 4))
    section_title(body, "КАСТОМНЫЙ АТОМ НА БАННЕРЕ").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Замени стандартный атом в шапке лаунчера на своё изображение.\n"
                  "  Поддерживаются: PNG, JPG, BMP, WEBP. Размер подгонится автоматически.\n"
                  "  Работает только для стандартных тем (atomic, custom, custom+).\n"
                  "  Требует Pillow: pip install Pillow",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))
    banner_row = tk.Frame(body, bg=C["bg"]); banner_row.pack(fill="x", pady=(4, 0))
    tk.Label(banner_row, text="🖼  Путь к файлу:",
             bg=C["bg"], fg=C["amber"], font=_font(8, "bold")).pack(side="left")
    _banner_var = tk.StringVar(value=config.get("custom_banner_path", ""))
    _banner_entry = tk.Entry(banner_row, textvariable=_banner_var,
                             bg=_glass_input(), fg=C["text"],
                             font=_font(8), bd=0,
                             highlightthickness=1, highlightbackground=_glass_border(),
                             insertbackground=C["text"], width=30)
    _banner_entry.pack(side="left", padx=(8, 4), fill="x", expand=True)

    def _pick_banner():
        path = filedialog.askopenfilename(
            title="Выбери изображение для баннера (вместо атома)",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.webp"),
                       ("Все файлы", "*.*")],
            parent=win
        )
        if path:
            _banner_var.set(path)

    def _preview_banner():
        """Мгновенный предпросмотр баннера без сохранения."""
        config["custom_banner_path"] = _banner_var.get().strip()
        try:
            for w in master.winfo_children():
                if isinstance(w, tk.Canvas):
                    W = w.winfo_width() or 640
                    _redraw_header_content(w, W, 80, config=config)
                    break
        except Exception:
            pass

    tk.Button(banner_row, text=" … ", command=_pick_banner,
              bg=_glass_panel(), fg=C["accent"], font=_font(8),
              relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
              cursor="hand2", padx=4).pack(side="left")
    tk.Button(banner_row, text=" 👁 ",
              command=_preview_banner,
              bg=_glass_panel(), fg=C["green"], font=_font(8),
              relief="flat", highlightthickness=1, highlightbackground=C["green"],
              cursor="hand2", padx=4).pack(side="left", padx=(2, 0))
    tk.Button(banner_row, text=" ✕ ",
              command=lambda: _banner_var.set(""),
              bg=_glass_panel(), fg=C["red"], font=_font(8),
              relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
              cursor="hand2", padx=4).pack(side="left", padx=(2, 0))

    # ── Переключаемся обратно на advanced_tab для автообновления ────
    body = advanced_tab

    section_title(body, "АВТООБНОВЛЕНИЕ ЛАУНЧЕРА").pack(fill="x", pady=(14,6))
    upd_top = tk.Frame(body, bg=C["bg"]); upd_top.pack(fill="x", pady=(0,4))
    tk.Label(upd_top, text=f"Текущая версия: v{LAUNCHER_VERSION}",
             bg=C["bg"], fg=C["green"], font=_font(9, "bold")).pack(side="left")
    auto_upd_var = tk.BooleanVar(value=config.get("auto_update", True))
    tk.Checkbutton(upd_top, text=" Проверять при запуске",
                   variable=auto_upd_var, bg=C["bg"], fg=C["text_muted"],
                   selectcolor=_glass_input(), activebackground=C["bg"],
                   activeforeground=C["orange"], font=FL, cursor="hand2").pack(side="right")
    tk.Label(body,
             text="Обновления скачиваются с сервера lenta.co (тот же адрес, что у аккаунта)\n"
                  "и устанавливаются, только если подпись разработчика верна.",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0,8))
    tk.Button(body, text="  🔍 ПРОВЕРИТЬ ОБНОВЛЕНИЯ  ",
              command=lambda: check_for_updates(win, config, silent=False),
              bg=_glass_panel(), fg=C["amber"], font=_font(8, "bold"),
              relief="flat", highlightthickness=1, highlightbackground=_glass_border(),
              activebackground=C["orange_glow"], activeforeground=C["orange"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(0,8))

    # ══════════════════════════════════════════
    #  БРАУЗЕР МОДОВ (CurseForge / Modrinth)
    # ══════════════════════════════════════════
    # ── Браузер модов — отдельная вкладка ───────────────────────────
    body = mods_tab
    section_title(body, "🔍  БРАУЗЕР МОДОВ / ШЕЙДЕРОВ / ТЕКСТУР ПАКОВ").pack(fill="x", pady=(14, 6))
    tk.Label(body,
             text="  Скачивай моды, шейдеры и текстур паки с CurseForge и Modrinth.\n"
                  "  В браузере выбери Тип: Мод / Шейдер / Текстур пак / Датапак.",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))

    def _open_mod_browser():
        _show_mod_browser(win, config)

    tk.Button(body, text="  🔍  ОТКРЫТЬ БРАУЗЕР  ",
              command=_open_mod_browser,
              bg=_glass_panel(), fg=C["amber"],
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=_glass_border(),
              activebackground=C["orange_glow"], activeforeground=C["orange"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(0, 8))

    # ── Авто-шейдеры для Fabric (Iris + Sodium) ─────────────────────
    sep(body).pack(fill="x", pady=(0, 6))
    section_title(body, "⚡  АВТО-ШЕЙДЕРЫ ДЛЯ FABRIC").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Автоматически скачивает Iris Shaders + Sodium (оптимизация + шейдеры)\n"
                  "  для выбранной версии Fabric. Папка установки должна быть задана.",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))

    _shader_status_var = tk.StringVar(value="")
    tk.Label(body, textvariable=_shader_status_var,
             bg=C["bg"], fg=C["green"], font=FS).pack(anchor="w")

    def _auto_install_fabric_shaders():
        import ssl as _ssl, urllib.request as _ur, json as _js, urllib.parse as _up
        all_versions = get_all_versions()  # Получаем все версии
        install_path = config.get("install_path", "")
        sel_ver = config.get("selected_version", "")
        if not install_path:
            _shader_status_var.set("✗ Укажи папку установки!")
            return
        if "Fabric" not in sel_ver:
            _shader_status_var.set("✗ Выбери версию с Fabric (например 1.20.1 Fabric)")
            return
        mc_ver = all_versions[sel_ver]["mc_version"]
        _shader_status_var.set(f"⏳ Ищу Iris + Sodium для MC {mc_ver}...")

        def _task():
            ctx = _ssl.create_default_context()

            def _modrinth_get_version(slug, mc_ver, loader="fabric"):
                params = (_up.quote(_js.dumps([mc_ver])))
                url = (f"https://api.modrinth.com/v2/project/{slug}/version"
                       f"?game_versions={params}"
                       f"&loaders={_up.quote(_js.dumps([loader]))}")
                req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req, context=ctx, timeout=15) as r:
                    versions = _js.loads(r.read())
                return versions[0] if versions else None

            def _download_mod(file_info, mods_dir):
                dest = os.path.join(mods_dir, file_info["filename"])
                if os.path.exists(dest):
                    return dest, True  # уже есть
                req2 = _ur.Request(file_info["url"], headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req2, context=ctx, timeout=120) as r:
                    with open(dest, "wb") as f:
                        f.write(r.read())
                return dest, False

            def _resolve_project_slug(project_id):
                """Резолвит project_id (UUID) в slug через Modrinth API."""
                try:
                    url = f"https://api.modrinth.com/v2/project/{project_id}"
                    req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                    with _ur.urlopen(req, context=ctx, timeout=10) as r:
                        data = _js.loads(r.read())
                    return data.get("slug", project_id)
                except Exception:
                    return project_id  # fallback: используем как есть

            def _install_with_deps(slug, mc_ver, mods_dir, visited=None, loader="fabric"):
                """Скачивает мод и все его обязательные зависимости рекурсивно."""
                if visited is None: visited = set()
                if slug in visited: return []
                visited.add(slug)
                ver_info = _modrinth_get_version(slug, mc_ver, loader)
                if not ver_info:
                    return [f"✗ {slug}: нет версии для MC {mc_ver}"]
                errors = []
                file_info = ver_info["files"][0]
                _, already = _download_mod(file_info, mods_dir)
                status = "уже есть" if already else "✓"
                win.after(0, lambda s=status, n=slug: _shader_status_var.set(f"  {s} {n}"))
                # Рекурсивно тянем обязательные зависимости
                for dep in ver_info.get("dependencies", []):
                    if dep.get("dependency_type") != "required": continue
                    # Modrinth возвращает project_id (UUID), нужно резолвить в slug
                    dep_id = dep.get("project_id") or dep.get("slug")
                    if not dep_id: continue
                    dep_slug = _resolve_project_slug(dep_id)
                    if dep_slug in visited: continue
                    errors += _install_with_deps(dep_slug, mc_ver, mods_dir, visited, loader)
                return errors

            mods_to_install = [("iris", "Iris Shaders"), ("sodium", "Sodium")]
            mc_dir   = get_game_dir(install_path, sel_ver)
            mods_dir = os.path.join(mc_dir, "mods")
            os.makedirs(mods_dir, exist_ok=True)
            # ── Сначала ставим Fabric API (обязательная зависимость для всех модов) ──
            win.after(0, lambda: _shader_status_var.set("⏳ Fabric API..."))
            _fabric_ensure_api(mc_dir, mc_ver,
                               log_cb=lambda msg, *_: win.after(0, lambda m=msg: _shader_status_var.set(m)))
            visited = set()
            errors = []
            for slug, name in mods_to_install:
                win.after(0, lambda n=name: _shader_status_var.set(f"⏳ {n}..."))
                try:
                    errors += _install_with_deps(slug, mc_ver, mods_dir, visited)
                except Exception as e:
                    errors.append(f"{name}: {e}")
            if errors:
                win.after(0, lambda: _shader_status_var.set("✗ " + "; ".join(errors)[:160]))
            else:
                win.after(0, lambda: _shader_status_var.set("✓ Fabric API + Iris + Sodium установлены!"))

        threading.Thread(target=_task, daemon=True).start()

    tk.Button(body, text="  ⚡  УСТАНОВИТЬ IRIS + SODIUM (Fabric)  ",
              command=_auto_install_fabric_shaders,
              bg=_glass_panel(), fg=C["green"],
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=C["green"],
              activebackground=C["bg_panel"], activeforeground=C["green"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(0, 8))

    # ── Оптимизация — быстрая установка ─────────────────────────────
    sep(body).pack(fill="x", pady=(0, 6))
    section_title(body, "🚀  ОПТИМИЗАЦИЯ").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Быстрая установка популярных модов оптимизации для Fabric:\n"
                  "  Sodium (FPS), Lithium (логика), FerriteCore (RAM), EntityCulling (рендер).",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))

    _opt_status_var = tk.StringVar(value="")
    tk.Label(body, textvariable=_opt_status_var,
             bg=C["bg"], fg=C["green"], font=FS).pack(anchor="w")

    def _auto_install_optimization():
        import ssl as _ssl, urllib.request as _ur, json as _js, urllib.parse as _up
        all_versions = get_all_versions()  # Получаем все версии
        install_path = config.get("install_path", "")
        sel_ver = config.get("selected_version", "")
        if not install_path:
            _opt_status_var.set("✗ Укажи папку установки!")
            return
        if "Fabric" not in sel_ver:
            _opt_status_var.set("✗ Только для Fabric-версий")
            return
        mc_ver = all_versions[sel_ver]["mc_version"]
        _opt_status_var.set(f"⏳ Устанавливаю пакет оптимизации для MC {mc_ver}...")

        def _task():
            ctx = _ssl.create_default_context()

            def _modrinth_get_version(slug, mc_ver, loader="fabric"):
                params = _up.quote(_js.dumps([mc_ver]))
                url = (f"https://api.modrinth.com/v2/project/{slug}/version"
                       f"?game_versions={params}"
                       f"&loaders={_up.quote(_js.dumps([loader]))}")
                req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req, context=ctx, timeout=15) as r:
                    versions = _js.loads(r.read())
                return versions[0] if versions else None

            def _download_mod(file_info, mods_dir):
                dest = os.path.join(mods_dir, file_info["filename"])
                if os.path.exists(dest): return dest, True
                req2 = _ur.Request(file_info["url"], headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req2, context=ctx, timeout=120) as r:
                    with open(dest, "wb") as f: f.write(r.read())
                return dest, False

            def _resolve_project_slug(project_id):
                """Резолвит project_id (UUID) в slug через Modrinth API."""
                try:
                    url = f"https://api.modrinth.com/v2/project/{project_id}"
                    req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                    with _ur.urlopen(req, context=ctx, timeout=10) as r:
                        data = _js.loads(r.read())
                    return data.get("slug", project_id)
                except Exception:
                    return project_id

            def _install_with_deps(slug, mc_ver, mods_dir, visited=None, loader="fabric"):
                if visited is None: visited = set()
                if slug in visited: return [], []
                visited.add(slug)
                ver_info = _modrinth_get_version(slug, mc_ver, loader)
                if not ver_info:
                    return [], [f"{slug}: нет для MC {mc_ver}"]
                file_info = ver_info["files"][0]
                _, already = _download_mod(file_info, mods_dir)
                installed = [] if already else [slug]
                skipped   = [slug] if already else []
                win.after(0, lambda s="уже есть" if already else "✓", n=slug: _opt_status_var.set(f"  {s} {n}"))
                for dep in ver_info.get("dependencies", []):
                    if dep.get("dependency_type") != "required": continue
                    dep_id = dep.get("project_id") or dep.get("slug")
                    if not dep_id: continue
                    dep_slug = _resolve_project_slug(dep_id)
                    if dep_slug in visited: continue
                    di, ds, = _install_with_deps(dep_slug, mc_ver, mods_dir, visited, loader)[:2]
                    installed += di; skipped += ds
                return installed, []

            opt_mods = ["sodium", "lithium", "ferrite-core", "entityculling"]
            mc_dir   = get_game_dir(install_path, sel_ver)
            mods_dir = os.path.join(mc_dir, "mods")
            os.makedirs(mods_dir, exist_ok=True)
            # ── Сначала ставим Fabric API ──
            win.after(0, lambda: _opt_status_var.set("⏳ Fabric API..."))
            _fabric_ensure_api(mc_dir, mc_ver,
                               log_cb=lambda msg, *_: win.after(0, lambda m=msg: _opt_status_var.set(m)))
            installed_all = []; skipped_all = []; errors_all = []
            visited = set()
            for slug in opt_mods:
                win.after(0, lambda s=slug: _opt_status_var.set(f"⏳ {s}..."))
                try:
                    inst, skip = _install_with_deps(slug, mc_ver, mods_dir, visited)
                    installed_all += inst; skipped_all += skip
                except Exception as e:
                    errors_all.append(f"{slug}: {str(e)[:40]}")
            msg = f"✓ Установлено: {', '.join(installed_all) or 'нет'}"
            if skipped_all: msg += f"  |  уже есть: {', '.join(skipped_all)}"
            if errors_all:  msg += f"\n✗ Ошибки: {'; '.join(errors_all)}"
            win.after(0, lambda: _opt_status_var.set(msg))

        threading.Thread(target=_task, daemon=True).start()

    tk.Button(body, text="  🚀  УСТАНОВИТЬ ПАКЕТ ОПТИМИЗАЦИИ (Fabric)  ",
              command=_auto_install_optimization,
              bg=_glass_panel(), fg=C["amber"],
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=_glass_border(),
              activebackground=C["orange_glow"], activeforeground=C["orange"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(0, 8))

    # ── Оптимизация + шейдеры для Forge / NeoForge ─────────────────
    sep(body).pack(fill="x", pady=(0, 6))
    section_title(body, "🔥  ОПТИМИЗАЦИЯ + ШЕЙДЕРЫ ДЛЯ FORGE / NEOFORGE").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Для Forge/NeoForge: Embeddium (FPS, замена Sodium) + Oculus (шейдеры, замена Iris).\n"
                  "  Для старых версий (≤1.12.2) предложит скачать OptiFine.",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))

    _forge_shader_status = tk.StringVar(value="")
    tk.Label(body, textvariable=_forge_shader_status,
             bg=C["bg"], fg=C["green"], font=FS).pack(anchor="w")

    def _auto_install_forge_shaders():
        import ssl as _ssl, urllib.request as _ur, json as _js, urllib.parse as _up
        all_versions = get_all_versions()  # Получаем все версии
        install_path = config.get("install_path", "")
        sel_ver = config.get("selected_version", "")
        if not install_path:
            _forge_shader_status.set("✗ Укажи папку установки!")
            return
        loader = all_versions.get(sel_ver, {}).get("loader", "")
        if loader not in ("forge", "neoforge"):
            _forge_shader_status.set("✗ Выбери версию Forge или NeoForge")
            return
        mc_ver = all_versions[sel_ver]["mc_version"]
        _mod_loader = loader
        _loader_label = "NeoForge" if loader == "neoforge" else "Forge"
        _forge_shader_status.set(f"⏳ Ищу моды для {_loader_label} MC {mc_ver}...")

        def _task():
            ctx = _ssl.create_default_context()

            def _modrinth_get(slug, mc_v, loader="forge"):
                params = _up.quote(_js.dumps([mc_v]))
                url = (f"https://api.modrinth.com/v2/project/{slug}/version"
                       f"?game_versions={params}&loaders={_up.quote(_js.dumps([loader]))}")
                req = _ur.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req, context=ctx, timeout=15) as r:
                    vs = _js.loads(r.read())
                return vs[0] if vs else None

            def _dl(file_info, mods_dir):
                dest = os.path.join(mods_dir, file_info["filename"])
                if os.path.exists(dest): return True
                req2 = _ur.Request(file_info["url"], headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with _ur.urlopen(req2, context=ctx, timeout=120) as r:
                    with open(dest, "wb") as f: f.write(r.read())
                return False

            mc_dir   = get_game_dir(install_path, sel_ver)
            mods_dir = os.path.join(mc_dir, "mods")
            os.makedirs(mods_dir, exist_ok=True)

            # Для старых версий — предлагаем OptiFine
            _old_mc = [v for v in ["1.7.10","1.8.9","1.9.4","1.10.2","1.11.2","1.12.2"] if mc_ver == v]
            if _old_mc:
                optifine_url = f"https://optifine.net/adloadx?f=OptiFine_{mc_ver}_HD_U_latest.jar"
                win.after(0, lambda: _forge_shader_status.set(
                    f"ℹ️  MC {mc_ver}: Embeddium недоступен. Скачай OptiFine вручную:\n{optifine_url}"))
                return

            results = []
            errors  = []
            # Embeddium (замена Sodium для Forge)
            for slug in ["embeddium", "rubidium"]:
                win.after(0, lambda s=slug: _forge_shader_status.set(f"⏳ {s}..."))
                try:
                    vi = _modrinth_get(slug, mc_ver, _mod_loader)
                    if vi:
                        already = _dl(vi["files"][0], mods_dir)
                        results.append(f"{'✓' if not already else '↩'} {slug}")
                        break
                except Exception as e:
                    errors.append(f"{slug}: {e}")

            # Oculus (шейдеры для Forge)
            for slug in ["oculus", "iris"]:
                win.after(0, lambda s=slug: _forge_shader_status.set(f"⏳ {s}..."))
                try:
                    vi = _modrinth_get(slug, mc_ver, _mod_loader)
                    if vi:
                        already = _dl(vi["files"][0], mods_dir)
                        results.append(f"{'✓' if not already else '↩'} {slug}")
                        break
                except Exception as e:
                    errors.append(f"{slug}: {e}")

            msg = "  ".join(results) if results else "✗ Нет совместимых модов для этой версии"
            if errors: msg += "  |  " + "; ".join(errors)[:80]
            win.after(0, lambda: _forge_shader_status.set(msg or "✗ Ничего не найдено"))

        threading.Thread(target=_task, daemon=True).start()

    tk.Button(body, text="  🔥  УСТАНОВИТЬ ОПТИМИЗАЦИЮ + ШЕЙДЕРЫ (Forge / NeoForge)  ",
              command=_auto_install_forge_shaders,
              bg=_glass_panel(), fg=C["red"] if C.get("red") else "#FF4444",
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=C.get("red", "#FF4444"),
              activebackground=C["orange_glow"], activeforeground=C["orange"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(0, 8))

    # ── Кастомные прицелы (Crosshair) ───────────────────────────────
    sep(body).pack(fill="x", pady=(0, 6))
    section_title(body, "🎯  КАСТОМНЫЕ ПРИЦЕЛЫ").pack(fill="x", pady=(0, 4))
    tk.Label(body,
             text="  Популярные пакеты прицелов с Modrinth.\n"
                  "  Нажми НАЙТИ — загружу список, выбери и скачай прямо сюда.",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=560).pack(anchor="w", pady=(0, 4))

    # Строка фильтра прицелов — версия определяется автоматически из выбранной версии
    _ch_filter_row = tk.Frame(body, bg=C["bg"]); _ch_filter_row.pack(anchor="w", pady=(0, 4))
    def _ch_ver_key(s):
        try: return tuple(int(x) for x in s.split("."))
        except: return (0,)
    _ch_mc_versions = sorted(set(v["mc_version"] for v in VERSIONS.values()), key=_ch_ver_key, reverse=True)
    _ch_sel_ver = config.get("selected_version", "1.20.1 Forge")
    _ch_sel_mc  = VERSIONS.get(_ch_sel_ver, {}).get("mc_version", "")
    _ch_ver_var = tk.StringVar(value=_ch_sel_mc)
    tk.Label(_ch_filter_row, text="Версия MC (авто):", bg=C["bg"], fg=C["text_muted"], font=FS).pack(side="left")
    ttk.Combobox(_ch_filter_row, textvariable=_ch_ver_var, values=["Любая"] + _ch_mc_versions,
                 state="readonly", width=8, font=FS).pack(side="left", padx=(6, 14))
    tk.Label(_ch_filter_row,
             text=f"← сейчас выбрана: {_ch_sel_ver}",
             bg=C["bg"], fg=C["text_dim"], font=_font(7)).pack(side="left")

    _ch_status_var = tk.StringVar(value="")
    tk.Label(body, textvariable=_ch_status_var,
             bg=C["bg"], fg=C["amber"], font=FS).pack(anchor="w")

    # Список результатов
    _ch_list_frame = tk.Frame(body, bg=_glass_panel() if _is_fx_theme() else C["bg_panel"],
                              highlightthickness=1, highlightbackground=_glass_border())
    _ch_list_frame.pack(fill="x", pady=(4, 0))

    def _search_crosshairs():
        import urllib.request, ssl as _ssl, json as _js, urllib.parse as _up
        _ch_status_var.set("⏳ Ищу прицелы на Modrinth...")
        for w in _ch_list_frame.winfo_children():
            w.destroy()

        def _task():
            try:
                ctx = _ssl.create_default_context()
                _ch_mc = _ch_ver_var.get()
                _ch_facets_list = [["project_type:resourcepack"]]
                if _ch_mc and _ch_mc != "Любая":
                    _ch_facets_list.append(["versions:" + _ch_mc])
                facets = _js.dumps(_ch_facets_list)
                params = ("query=" + _up.quote("crosshair") +
                          "&facets=" + _up.quote(facets) + "&limit=16")
                url = "https://api.modrinth.com/v2/search?" + params
                req = urllib.request.Request(url, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                with urllib.request.urlopen(req, context=ctx, timeout=15) as r:
                    data = _js.loads(r.read())
                hits = data.get("hits", [])
                def _show():
                    for w in _ch_list_frame.winfo_children():
                        w.destroy()
                    if not hits:
                        _ch_status_var.set("Ничего не найдено")
                        return
                    _ch_status_var.set(f"✓ Найдено {len(hits)} паков прицелов")
                    for h in hits:
                        slug = h.get("slug", "")
                        pid  = h.get("project_id", "")
                        name = h.get("title", "?")
                        dl   = h.get("downloads", 0)
                        desc = h.get("description", "")[:60]

                        row = tk.Frame(_ch_list_frame,
                                       bg=_glass_bg() if _is_fx_theme() else C["log_bg"],
                                       cursor="hand2")
                        row.pack(fill="x", padx=1, pady=1)

                        info = tk.Frame(row, bg=row["bg"])
                        info.pack(side="left", fill="x", expand=True, padx=6, pady=3)
                        tk.Label(info, text=name, bg=row["bg"], fg=C["orange"],
                                 font=_font(8, "bold"), anchor="w").pack(anchor="w")
                        tk.Label(info, text=f"⬇ {dl:,}   {desc}",
                                 bg=row["bg"], fg=C["text_muted"],
                                 font=_font(7), anchor="w").pack(anchor="w")

                        def _make_dl(project_id=pid, pack_name=name):
                            def _download_crosshair():
                                install_path = config.get("install_path", "")
                                sel_ver = config.get("selected_version", "")
                                if not install_path:
                                    messagebox.showwarning("Прицелы", "Укажи папку установки!", parent=win)
                                    return
                                _ch_status_var.set(f"⏳ Скачиваю {pack_name}...")
                                def _dl_task():
                                    import urllib.request as _ur, ssl as _s2, json as _j2, urllib.parse as _u2
                                    ctx2 = _s2.create_default_context()
                                    try:
                                        mc_dir = get_game_dir(install_path, sel_ver)
                                        rp_dir = os.path.join(mc_dir, "resourcepacks")
                                        os.makedirs(rp_dir, exist_ok=True)
                                        url2 = f"https://api.modrinth.com/v2/project/{project_id}/version"
                                        req2 = _ur.Request(url2, headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                                        with _ur.urlopen(req2, context=ctx2, timeout=15) as r2:
                                            vers = _j2.loads(r2.read())
                                        if not vers:
                                            raise RuntimeError("Нет версий")
                                        fi = vers[0]["files"][0]
                                        dest = os.path.join(rp_dir, fi["filename"])
                                        req3 = _ur.Request(fi["url"], headers={"User-Agent": "AtomicIndustryLauncher/1.0"})
                                        with _ur.urlopen(req3, context=ctx2, timeout=120) as r3:
                                            with open(dest, "wb") as f: f.write(r3.read())
                                        body.after(0, lambda n=pack_name, fn=fi["filename"]:
                                                   _ch_status_var.set(f"✓ {n} → {fn}"))
                                    except Exception as e:
                                        body.after(0, lambda err=str(e):
                                                   _ch_status_var.set(f"✗ {err[:80]}"))
                                threading.Thread(target=_dl_task, daemon=True).start()
                            return _download_crosshair

                        dl_btn = tk.Button(row, text=" ⬇ ",
                                           command=_make_dl(),
                                           bg=_glass_panel() if _is_fx_theme() else C["bg_panel"],
                                           fg=C["green"], font=_font(8, "bold"),
                                           relief="flat", cursor="hand2",
                                           highlightthickness=1,
                                           highlightbackground=C["green"],
                                           padx=4)
                        dl_btn.pack(side="right", padx=6, pady=4)
                        row.bind("<Enter>", lambda e, w=row: w.config(bg=C["orange_glow"]))
                        row.bind("<Leave>", lambda e, w=row, orig=row["bg"]: w.config(bg=orig))
                _ch_list_frame.after(0, _show)
            except Exception as e:
                _ch_list_frame.after(0, lambda err=str(e): _ch_status_var.set(f"✗ {err[:80]}"))

        threading.Thread(target=_task, daemon=True).start()

    tk.Button(body, text="  🎯  НАЙТИ ПРИЦЕЛЫ  ",
              command=_search_crosshairs,
              bg=_glass_panel(), fg=C["orange"],
              font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=_glass_border(),
              activebackground=C["orange_glow"], activeforeground=C["orange"],
              cursor="hand2", padx=6, pady=4).pack(anchor="w", pady=(6, 4))

    # Кнопка "Установить свой прицел / ресурспак" — УДАЛЕНА

    # Автоматически ищем прицелы для текущей версии при открытии
    body.after(400, _search_crosshairs)

    if dev_tab is not None:
        try:
            _build_dev_tab(dev_tab, win, config)
        except Exception as _e:
            tk.Label(dev_tab, text=f"Ошибка вкладки разработчика: {_e}", bg=C["bg"],
                     fg=C["red"], font=FS).pack(anchor="w")

    def save_and_close():
        config["account_type"]  = _acct_type_var.get()
        config["auto_update"] = auto_upd_var.get()
        sel_label = theme_cb.get()
        for k, t in THEMES.items():
            if t["name"] == sel_label:
                config["theme"] = k; break
        if _custom_editor_frame[0] and _custom_editor_frame[0].winfo_exists():
            config["custom_theme"] = _custom_editor_frame[0]._get_custom_dict()
        config["custom_theme_name"] = _custom_name_var.get().strip() or "CUSTOM"
        # Применяем имя в THEMES чтобы оно сразу отобразилось в комбобоксе
        cname = config["custom_theme_name"]
        THEMES["custom"]["name"] = f"✏  {cname}"
        config["photo_bg_path"]    = _photo_var.get().strip()
        config["custom_banner_path"] = _banner_var.get().strip()
        config["bg_overlay_alpha"] = int(_alpha_var.get())
        config["glass_strength"]   = float(_glass_var.get())
        save_config(config); on_save(); win.destroy()

    # ── Вкладка "Основные" — блок аккаунта ─────────────────────────
    section_title(_orig_body, "АККАУНТ").pack(fill="x", pady=(0, 6))

    _acct_type_var = tk.StringVar(value=config.get("account_type", "offline"))

    acct_frame = tk.Frame(_orig_body, bg=C["bg_panel"],
                          highlightthickness=1, highlightbackground=C["border"])
    acct_frame.pack(fill="x", pady=(0, 10))

    radio_row = tk.Frame(acct_frame, bg=C["bg_panel"])
    radio_row.pack(fill="x", padx=12, pady=(10, 4))
    tk.Label(radio_row, text="Тип аккаунта:", bg=C["bg_panel"],
             fg=C["text_muted"], font=_font(8, "bold")).pack(side="left")
    for val, lbl_t in (("offline", "🎮  Offline"),
                       ("microsoft", "🔵  Microsoft"),
                       ("atomic", "🟢  сервер lenta.co")):
        tk.Radiobutton(radio_row, text=lbl_t, variable=_acct_type_var, value=val,
                       command=lambda: _render_acct(),
                       bg=C["bg_panel"], fg=C["text"],
                       selectcolor=C["bg_input"] if not _is_fx_theme() else _glass_entry_bg(),
                       activebackground=C["bg_panel"], activeforeground=C["orange"],
                       font=_font(8), cursor="hand2").pack(side="left", padx=(14, 0))

    _acct_status_lbl = tk.Label(acct_frame, text="", bg=C["bg_panel"],
                                fg=C["green"], font=_font(9), justify="left")
    _acct_status_lbl.pack(anchor="w", padx=14, pady=(4, 2))
    _acct_body = tk.Frame(acct_frame, bg=C["bg_panel"])
    _acct_body.pack(fill="x", padx=12, pady=(2, 10))

    def _abtn(parent, text, cmd, fg, border=None):
        b = tk.Button(parent, text=text, command=cmd, bg=_glass_panel(), fg=fg,
                      font=_font(8, "bold"), relief="flat",
                      highlightthickness=1, highlightbackground=border or _glass_border(),
                      cursor="hand2", padx=8, pady=4)
        b.pack(side="left", padx=(0, 8))
        return b

    def _acct_note(text):
        tk.Label(_acct_body, text=text, bg=C["bg_panel"], fg=C["text_dim"],
                 font=FS, justify="left").pack(anchor="w", pady=(6, 0))

    def _render_acct():
        for w in _acct_body.winfo_children():
            w.destroy()
        at = _acct_type_var.get()
        if at == "microsoft":
            if config.get("ms_username") and config.get("ms_access_token"):
                _acct_status_lbl.config(text=f"✓ Microsoft: {config['ms_username']}", fg=C["green"])
            else:
                _acct_status_lbl.config(text="⚠ Вход через Microsoft не выполнен", fg=C["orange"])
            row = tk.Frame(_acct_body, bg=C["bg_panel"]); row.pack(anchor="w")
            _abtn(row, "  🔑  Войти через Microsoft  ", _do_ms_login, C["orange"], C["orange"])
            _abtn(row, "  Выйти  ", _do_ms_logout, C["red"])
            _acct_note("ℹ  Лицензия: скин с Mojang, вход на любые лицензионные серверы.")
        elif at == "atomic":
            if config.get("atomic_access_token") and config.get("atomic_username"):
                _acct_status_lbl.config(text=f"✓ Сервер lenta.co: {config['atomic_username']}", fg=C["green"])
            else:
                _acct_status_lbl.config(text="⚠ Войди или зарегистрируйся", fg=C["orange"])
            url_row = tk.Frame(_acct_body, bg=C["bg_panel"]); url_row.pack(fill="x", pady=(0, 6))
            tk.Label(url_row, text="Адрес:", bg=C["bg_panel"], fg=C["text_muted"], font=FS).pack(side="left")
            url_var = tk.StringVar(value=config.get("atomic_server_url", ATOMIC_DEFAULT_URL))
            url_var.trace_add("write", lambda *_: config.__setitem__("atomic_server_url", url_var.get().strip()))
            tk.Entry(url_row, textvariable=url_var, width=30, bg=_glass_entry_bg(), fg=C["text"],
                     font=FS, bd=0, highlightthickness=1, highlightbackground=_glass_border(),
                     insertbackground=C["text"]).pack(side="left", padx=(6, 6), ipady=2)
            ping_lbl = tk.Label(url_row, text="", bg=C["bg_panel"], fg=C["text_muted"], font=FS)

            def _ping():
                ping_lbl.config(text="⏳", fg=C["amber"])
                def work():
                    try:
                        meta = atomic_server_info(config)
                        name = meta.get("meta", {}).get("serverName", "?")
                        reg = {"invite": "по приглашению", "open": "открыта",
                               "closed": "закрыта"}.get(meta.get("meta", {}).get("atomic.registration"), "?")
                        txt, col = f"✓ {name} (регистрация {reg})", C["green"]
                    except Exception as e:
                        txt, col = "✗ " + str(e).split("\n")[0][:60], C["red"]
                    win.after(0, lambda: ping_lbl.winfo_exists() and ping_lbl.config(text=txt, fg=col))
                threading.Thread(target=work, daemon=True).start()

            tk.Button(url_row, text=" Проверить ", command=_ping, bg=_glass_panel(), fg=C["amber"],
                      font=FS, relief="flat", cursor="hand2").pack(side="left")
            ping_lbl.pack(side="left", padx=(6, 0))

            row = tk.Frame(_acct_body, bg=C["bg_panel"]); row.pack(anchor="w")
            _abtn(row, "  🔑  Войти  ",
                  lambda: _atomic_auth_dialog(win, config, "login", _after_atomic), C["orange"], C["orange"])
            _abtn(row, "  📝  Регистрация  ",
                  lambda: _atomic_auth_dialog(win, config, "register", _after_atomic), C["amber"])
            if config.get("atomic_access_token"):
                _abtn(row, "  🔒  Пароль  ",
                      lambda: _atomic_auth_dialog(win, config, "password", _render_acct), C["text_muted"])
                _abtn(row, "  Выйти  ", _do_atomic_logout, C["red"])
            _acct_note("ℹ  Аккаунт на сервере lenta.co (через ZeroTier). Пароль хранится только\n"
                       "   на сервере в виде хеша — зайти под твоим ником без пароля нельзя.\n"
                       "   Лаунчер сам входит перед игрой. Друзьям без этого лаунчера —\n"
                       "   веб-страница сервера: адрес/login (регистрация, скин, пароль).")
        else:
            _acct_status_lbl.config(text="Offline — ник задаётся вручную на главном экране.",
                                    fg=C["text_muted"])
            _acct_note("ℹ  Скин хранится локально. Чужие скины мод CustomSkinLoader берёт\n"
                       "   по нику с сервера lenta.co, Ely.by, TLauncher, LittleSkin и Mojang.\n"
                       "   Для игры на сервере lenta.co нужен аккаунт «Сервер lenta.co».")

    def _after_atomic():
        _acct_type_var.set("atomic")
        _render_acct()
        messagebox.showinfo("Аккаунт", f"Вошёл как {config.get('atomic_username')}.\n"
                            "Нажми СОХРАНИТЬ, чтобы обновить главный экран.", parent=win)

    def _do_atomic_logout():
        threading.Thread(target=lambda: (atomic_logout(config),
                                         win.after(0, lambda: (_acct_type_var.set("offline"), _render_acct()))),
                         daemon=True).start()

    def _do_ms_login():
        def _after_login():
            _acct_type_var.set("microsoft")
            _render_acct()
        ms_login_dialog(win, config, on_success=_after_login)

    def _do_ms_logout():
        config["account_type"]    = "offline"
        config["ms_access_token"] = ""
        config["ms_refresh_token"]= ""
        config["ms_uuid"]         = ""
        config["ms_username"]     = ""
        _acct_type_var.set("offline")
        _render_acct()
        messagebox.showinfo("Аккаунт", "Вышел из Microsoft аккаунта.", parent=win)

    _render_acct()

    sep(_orig_body).pack(fill="x", pady=(4, 8))

    # ── Вкладка "Основные" — краткая навигационная панель ────────────
    section_title(_orig_body, "БЫСТРЫЙ СТАРТ").pack(fill="x", pady=(0, 8))
    tk.Label(_orig_body,
             text="  Используй вкладки выше для настройки лаунчера:\n\n"
                  "  🔍  Браузер модов   — моды, шейдеры, текстур паки (Modrinth / CurseForge)\n"
                  "                        + авто-шейдеры Fabric, оптимизация, прицелы\n"
                  "  🎨  Темы            — выбор темы, фото/GIF фон, прозрачность\n"
                  "  🛠  Дополнительно  — обновления лаунчера, секретный код",
             bg=C["bg"], fg=C["text_muted"], font=FS,
             justify="left", wraplength=680).pack(anchor="w", pady=(0, 12))

    section_title(_orig_body, "ТЕКУЩАЯ КОНФИГУРАЦИЯ").pack(fill="x", pady=(8, 6))
    install_p = config.get("install_path", "(не задана)")
    sel_v     = config.get("selected_version", "1.7.10")
    nick      = config.get("nickname", "(не задан)")
    mem       = config.get("memory", "2")
    theme_n   = THEMES.get(config.get("theme","night"), THEMES["night"]).get("name","?")
    info_lines = (
        f"  Версия:         {sel_v}\n"
        f"  Папка:          {install_p[:60]}\n"
        f"  Ник:            {nick}\n"
        f"  RAM:            {mem} GB\n"
        f"  Тема:           {theme_n}\n"
        f"  Аккаунт:        {config.get('account_type','offline')}\n"
        f"  Авто-обновл.:   {'вкл' if config.get('auto_update') else 'выкл'}"
    )
    tk.Label(_orig_body, text=info_lines,
             bg=C["bg"], fg=C["green"], font=_font(8),
             justify="left").pack(anchor="w", pady=(0, 12))

    save_btn = IndustrialButton(btn_frame, mode="launch", command=save_and_close, w=200, h=40)
    save_btn._label = "СОХРАНИТЬ"; save_btn._draw(); save_btn.pack(side="left")
    tk.Button(btn_frame, text="  ОТМЕНА  ", command=win.destroy,
              bg=_glass_panel(), fg=C["text_muted"], font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=_glass_border(),
              activebackground=C["red_glow"], activeforeground=C["red"],
              cursor="hand2", padx=6, pady=6).pack(side="left", padx=(10,0))

    def do_reset():
        if not messagebox.askyesno(
            "Сброс настроек",
            "Сбросить ВСЕ настройки до заводских?\n\n"
            "• Путь установки, ник, память — будут очищены\n"
            "• Аккаунты (Microsoft / сервер lenta.co) останутся\n"
            "• Тема вернётся на НОЧЬ\n"
            "• Разблокированные темы останутся\n\n"
            "Продолжить?",
            parent=win
        ): return
        defaults = _default_config()
        for k, v in defaults.items():
            if k != "account_type" and not k.startswith(("atomic_", "ms_")):
                config[k] = v
        config["theme"] = "night"
        save_config(config)
        win.destroy()
        on_save()

    tk.Button(btn_frame, text="  СБРОС  ", command=do_reset,
              bg=_glass_panel(), fg=C["red"], font=_font(8, "bold"), relief="flat",
              highlightthickness=1, highlightbackground=C["red_glow"],
              activebackground=C["red_glow"], activeforeground=C["red"],
              cursor="hand2", padx=6, pady=6).pack(side="right")

# ══════════════════════════════════════════
#  ГЛАВНОЕ ОКНО
# ══════════════════════════════════════════

_game_state = {
    "proc": None, "log_lines": [], "btn_mode": "launch",
    "progress": 0, "progress_label": "",
}
_ui_state = {"bg": None, "banner_fx": None}   # фон тела и сцена шапки главного окна

# ══════════════════════════════════════════
#  СКИНЫ И АККАУНТЫ
#  Источники скинов: файл, Microsoft/Mojang, Ely.by, TLauncher, LittleSkin, URL.
#  Аккаунт «Сервер lenta.co»: свой сервер авторизации (atomic_auth_server.py),
#  протокол authlib-injector — как у ely.by. Скины хранятся на сервере и
#  подписаны его ключом, видны всем игрокам. Пароль в лаунчере не хранится.
#  Offline: скин кладётся в CustomSkinLoader/LocalSkin, чужие скины CSL
#  подтягивает из Ely.by / TLauncher / LittleSkin / Mojang по нику.
# ══════════════════════════════════════════

import base64 as _b64
import hashlib as _hashlib
import io as _io
import ssl as _ssl
import struct as _struct
import urllib.error as _urlerr
import urllib.request as _urlreq

ATOMIC_DEFAULT_URL = "http://10.55.9.173:25580"
_UA = {"User-Agent": "AtomicIndustryLauncher/2.0"}
_AUTHLIB_LATEST = "https://authlib-injector.yushi.moe/artifact/latest.json"
_AUTHLIB_JAR = os.path.join(BASE_DIR, "authlib-injector.jar")

SKIN_SOURCES = [
    ("file",       "📁  Файл с компьютера"),
    ("mojang",     "🟩  Microsoft / Mojang (по нику)"),
    ("elyby",      "🟦  Ely.by (по нику)"),
    ("tlauncher",  "🟧  TLauncher (по нику)"),
    ("littleskin", "🟪  LittleSkin (по нику)"),
    ("url",        "🔗  Прямая ссылка на PNG"),
]


def _skin_filename(nickname: str) -> str:
    safe = "".join(c for c in nickname if c.isalnum() or c in "-_.")
    return f"{safe}.png"


def _get_local_skins_dir(config: dict) -> str:
    """Папка для локальных скинов рядом с лаунчером."""
    d = os.path.join(BASE_DIR, "skins")
    os.makedirs(d, exist_ok=True)
    return d


def _local_skin_path(config: dict, nickname: str) -> str:
    return os.path.join(_get_local_skins_dir(config), _skin_filename(nickname))


# ── HTTP ──────────────────────────────────────────────────────────────────

def _http(url: str, method="GET", data=None, headers=None, timeout=15, max_bytes=4_000_000):
    """Возвращает (status, bytes). Сертификаты HTTPS проверяются."""
    h = dict(_UA)
    if headers:
        h.update(headers)
    req = _urlreq.Request(url, data=data, method=method, headers=h)
    ctx = _ssl.create_default_context() if url.startswith("https://") else None
    try:
        with _urlreq.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, r.read(max_bytes + 1)[:max_bytes]
    except _urlerr.HTTPError as e:
        try:
            body = e.read(65536)
        except Exception:
            body = b""
        return e.code, body


def _multipart(fields: dict, file_field: str, filename: str, file_bytes: bytes):
    boundary = "----AtomicLauncher" + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; '
                  f'filename="{filename}"\r\nContent-Type: image/png\r\n\r\n').encode())
    parts.append(file_bytes + f"\r\n--{boundary}--\r\n".encode())
    return b"".join(parts), {"Content-Type": f"multipart/form-data; boundary={boundary}"}


# ── PNG-скины ─────────────────────────────────────────────────────────────

def _png_size(data: bytes):
    if len(data) < 24 or not data.startswith(b"\x89PNG\r\n\x1a\n") or data[12:16] != b"IHDR":
        return None
    return _struct.unpack(">II", data[16:24])


def _check_skin_png(data: bytes):
    """Бросает ValueError, если это не скин Minecraft."""
    size = _png_size(data)
    if size is None:
        raise ValueError("Это не PNG-файл")
    w, h = size
    if not (w % 64 == 0 and 64 <= w <= 1024 and (h == w or h * 2 == w)):
        raise ValueError(f"Размер {w}×{h} не подходит. Нужен скин 64×64 или 64×32 (или HD кратно 64)")


def _guess_model(data: bytes) -> str:
    """Тонкие руки (Alex) у 64×64-скинов: пиксель (54,20) прозрачный."""
    try:
        from PIL import Image as _PI
        img = _PI.open(_io.BytesIO(data)).convert("RGBA")
        w, h = img.size
        if w != h:
            return "default"
        k = w // 64
        return "slim" if img.getpixel((54 * k, 20 * k))[3] == 0 else "default"
    except Exception:
        return "default"


def _render_skin_preview(data: bytes, model: str, scale: int = 6):
    """Вид спереди (голова, тело, руки, ноги + второй слой) как PIL.Image."""
    from PIL import Image as _PI
    src = _PI.open(_io.BytesIO(data)).convert("RGBA")
    k = src.size[0] // 64
    legacy = src.size[1] * 2 == src.size[0]
    aw = 3 if model == "slim" else 4
    out = _PI.new("RGBA", (16, 32), (0, 0, 0, 0))

    def put(sx, sy, w, h, dx, dy, mirror=False):
        part = src.crop((sx * k, sy * k, (sx + w) * k, (sy + h) * k)).resize((w, h), _PI.NEAREST)
        if mirror:
            part = part.transpose(_PI.FLIP_LEFT_RIGHT)
        out.alpha_composite(part, (dx, dy))

    put(8, 8, 8, 8, 4, 0)                          # голова
    put(20, 20, 8, 12, 4, 8)                       # тело
    put(44, 20, aw, 12, 4 - aw, 8)                 # правая рука (слева на экране)
    put(4, 20, 4, 12, 4, 20)                       # правая нога
    if legacy:
        put(44, 20, aw, 12, 12, 8, mirror=True)
        put(4, 20, 4, 12, 8, 20, mirror=True)
    else:
        put(36, 52, aw, 12, 12, 8)                 # левая рука
        put(20, 52, 4, 12, 8, 20)                  # левая нога
        put(20, 36, 8, 12, 4, 8)                   # куртка
        put(44, 36, aw, 12, 4 - aw, 8)             # рукава
        put(52, 52, aw, 12, 12, 8)
        put(4, 36, 4, 12, 4, 20)                   # штанины
        put(4, 52, 4, 12, 8, 20)
    put(40, 8, 8, 8, 4, 0)                         # шапка / волосы
    return out.resize((16 * scale, 32 * scale), _PI.NEAREST)


def _download_png(url: str) -> bytes:
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("Ссылка должна начинаться с http:// или https://")
    st, data = _http(url, timeout=20, max_bytes=2_000_000)
    if st != 200:
        raise ValueError(f"Сервер вернул код {st}")
    return data


def _textures_json_skin(st: int, body: bytes, who: str):
    """Формат Ely.by / TLauncher: {"SKIN": {"url": ..., "metadata": {"model": "slim"}}}."""
    if st in (204, 404) or not body.strip():
        raise ValueError(f"У игрока нет скина на {who}")
    if st != 200:
        raise ValueError(f"{who} вернул код {st}")
    skin = (json.loads(body) or {}).get("SKIN") or {}
    if not skin.get("url"):
        raise ValueError(f"У игрока нет скина на {who}")
    return skin["url"], ((skin.get("metadata") or {}).get("model") or "default")


def skin_fetch(source: str, query: str) -> dict:
    """Скачивает скин. Возвращает {"png": bytes, "model": "default"|"slim", "label": str}."""
    query = query.strip()
    if not query:
        raise ValueError("Укажи ник, ссылку или файл")
    model = None
    if source == "file":
        with open(query, "rb") as f:
            png = f.read(2_000_001)
        label = os.path.basename(query)
    elif source == "url":
        png, label = _download_png(query), query
    else:
        if not re.fullmatch(r"[A-Za-z0-9_]{1,16}", query):
            raise ValueError("Ник: только латиница, цифры и _ (до 16 символов)")
        q = urllib.parse.quote(query)
        if source == "mojang":
            st, body = _http(f"https://api.mojang.com/users/profiles/minecraft/{q}")
            if st != 200 or not body.strip():
                raise ValueError("Такого лицензионного игрока нет")
            pid = json.loads(body)["id"]
            st, body = _http(f"https://sessionserver.mojang.com/session/minecraft/profile/{pid}")
            if st != 200:
                raise ValueError(f"Mojang вернул код {st}")
            url = None
            for prop in json.loads(body).get("properties", []):
                if prop.get("name") == "textures":
                    tex = json.loads(_b64.b64decode(prop["value"])).get("textures", {})
                    skin = tex.get("SKIN") or {}
                    url = skin.get("url")
                    model = (skin.get("metadata") or {}).get("model") or "default"
            if not url:
                raise ValueError("У игрока стандартный скин (Steve/Alex)")
            label = f"Mojang: {query}"
        elif source == "elyby":
            try:
                st, body = _http(f"https://skinsystem.ely.by/textures/{q}")
            except (_urlerr.URLError, OSError):
                st, body = _http(f"http://skinsystem.ely.by/textures/{q}")
            url, model = _textures_json_skin(st, body, "Ely.by")
            label = f"Ely.by: {query}"
        elif source == "tlauncher":
            st, body = _http(f"https://auth.tlauncher.org/skin/profile/texture/login/{q}")
            url, model = _textures_json_skin(st, body, "TLauncher")
            label = f"TLauncher: {query}"
        elif source == "littleskin":
            st, body = _http(f"https://littleskin.cn/csl/{q}.json")
            if st != 200 or not body.strip():
                raise ValueError("Такого игрока нет на LittleSkin")
            skins = (json.loads(body) or {}).get("skins") or {}
            if not skins:
                raise ValueError("У игрока нет скина на LittleSkin")
            key = next(iter(skins))
            url, model = f"https://littleskin.cn/textures/{skins[key]}", ("slim" if key == "slim" else "default")
            label = f"LittleSkin: {query}"
        else:
            raise ValueError("Неизвестный источник")
        png = _download_png(url)
    _check_skin_png(png)
    return {"png": png, "model": model or _guess_model(png), "label": label}


# ══════════════════════════════════════════
#  АККАУНТ «СЕРВЕР lenta.co» (atomic_auth_server)
# ══════════════════════════════════════════

class AtomicAuthError(Exception):
    pass


def _atomic_url(config: dict) -> str:
    return (config.get("atomic_server_url") or ATOMIC_DEFAULT_URL).strip().rstrip("/")


def _atomic_call(config, method, path, payload=None, raw=None, headers=None, ok=(200, 201, 204)):
    data = raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    try:
        st, body = _http(_atomic_url(config) + path, method=method, data=data, headers=h, timeout=15)
    except (_urlerr.URLError, OSError) as e:
        raise AtomicAuthError(
            f"Сервер авторизации недоступен ({_atomic_url(config)}).\n"
            f"Проверь, что ZeroTier подключён и сервер lenta.co запущен.\n\n{e}")
    obj = None
    if body:
        try:
            obj = json.loads(body.decode("utf-8"))
        except Exception:
            obj = None
    if st not in ok:
        msg = (obj or {}).get("errorMessage") if isinstance(obj, dict) else None
        if msg and msg.startswith("Invalid credentials"):
            msg = "Неверный ник или пароль"
        elif msg == "Invalid token.":
            msg = "Сессия истекла — войди заново"
        raise AtomicAuthError(msg or f"Ошибка сервера (код {st})")
    return st, obj


def atomic_server_info(config: dict) -> dict:
    _, meta = _atomic_call(config, "GET", "/")
    if not isinstance(meta, dict) or "signaturePublickey" not in meta:
        raise AtomicAuthError("По этому адресу не сервер авторизации")
    return meta


def atomic_register(config, username, password, invite=""):
    payload = {"username": username, "password": password}
    if invite.strip():
        payload["invite"] = invite.strip()
    _atomic_call(config, "POST", "/atomic/register", payload)


def atomic_login(config, username, password):
    client_token = config.get("atomic_client_token") or uuid.uuid4().hex
    _, r = _atomic_call(config, "POST", "/authserver/authenticate", {
        "username": username, "password": password, "clientToken": client_token,
        "requestUser": True, "agent": {"name": "Minecraft", "version": 1}})
    prof = r.get("selectedProfile") or {}
    config.update({
        "account_type": "atomic",
        "atomic_client_token": r.get("clientToken", client_token),
        "atomic_access_token": r["accessToken"],
        "atomic_uuid": prof.get("id", ""),
        "atomic_username": prof.get("name", username),
        "nickname": prof.get("name", username),
    })
    save_config(config)


def atomic_ensure_session(config) -> bool:
    """Проверяет токен; если протух — обновляет. False = нужно войти заново."""
    tok, ct = config.get("atomic_access_token"), config.get("atomic_client_token")
    if not tok:
        return False
    try:
        _atomic_call(config, "POST", "/authserver/validate", {"accessToken": tok, "clientToken": ct})
        return True
    except AtomicAuthError as e:
        if "недоступен" in str(e):
            raise
    try:
        _, r = _atomic_call(config, "POST", "/authserver/refresh",
                            {"accessToken": tok, "clientToken": ct, "requestUser": False})
    except AtomicAuthError as e:
        if "недоступен" in str(e):
            raise
        config["atomic_access_token"] = ""
        save_config(config)
        return False
    config["atomic_access_token"] = r["accessToken"]
    save_config(config)
    return True


def atomic_logout(config):
    tok = config.get("atomic_access_token")
    if tok:
        try:
            _atomic_call(config, "POST", "/authserver/invalidate",
                         {"accessToken": tok, "clientToken": config.get("atomic_client_token")})
        except AtomicAuthError:
            pass
    config.update({"atomic_access_token": "", "atomic_uuid": "", "atomic_username": ""})
    if config.get("account_type") == "atomic":
        config["account_type"] = "offline"
    save_config(config)


def atomic_change_password(config, old_pw, new_pw):
    _atomic_call(config, "POST", "/atomic/change_password", {
        "username": config.get("atomic_username", ""), "password": old_pw, "newPassword": new_pw})
    config["atomic_access_token"] = ""   # сервер завершил все сессии
    save_config(config)


def atomic_upload_skin(config, png: bytes, model: str):
    if not atomic_ensure_session(config):
        raise AtomicAuthError("Сессия истекла — войди заново в Настройках")
    body, h = _multipart({"model": "slim" if model == "slim" else ""}, "file", "skin.png", png)
    h["Authorization"] = "Bearer " + config["atomic_access_token"]
    _atomic_call(config, "PUT", f"/api/user/profile/{config['atomic_uuid']}/skin", raw=body, headers=h)


def atomic_get_skin(config):
    """Текущий скин игрока на сервере: (png, model) или (None, None)."""
    uid = config.get("atomic_uuid")
    if not uid:
        return None, None
    _, prof = _atomic_call(config, "GET", f"/sessionserver/session/minecraft/profile/{uid}", ok=(200, 204))
    for prop in (prof or {}).get("properties", []):
        if prop.get("name") == "textures":
            skin = json.loads(_b64.b64decode(prop["value"])).get("textures", {}).get("SKIN")
            if skin and skin.get("url"):
                return _download_png(skin["url"]), (skin.get("metadata") or {}).get("model", "default")
    return None, None


def ms_upload_skin(config, png: bytes, model: str):
    """Меняет скин лицензионного аккаунта через официальный API Minecraft."""
    tok = config.get("ms_access_token")
    if not tok:
        raise AtomicAuthError("Сначала войди через Microsoft")
    body, h = _multipart({"variant": "slim" if model == "slim" else "classic"}, "file", "skin.png", png)
    h["Authorization"] = "Bearer " + tok
    st, resp = _http("https://api.minecraftservices.com/minecraft/profile/skins",
                     method="POST", data=body, headers=h, timeout=30)
    if st == 401:
        raise AtomicAuthError("Токен Microsoft истёк — войди через Microsoft заново")
    if st not in (200, 204):
        raise AtomicAuthError(f"Mojang отклонил скин (код {st})")


def atomic_ensure_agent(config, log_cb=None) -> str:
    """authlib-injector.jar рядом с лаунчером, SHA-256 проверяется. Возвращает путь."""
    def log(m, lvl="muted"):
        if log_cb:
            log_cb(m, lvl)
    fresh = os.path.exists(_AUTHLIB_JAR) and time.time() - os.path.getmtime(_AUTHLIB_JAR) < 7 * 86400
    if fresh:
        return _AUTHLIB_JAR
    try:
        st, body = _http(_AUTHLIB_LATEST, timeout=15)
        if st != 200:
            raise OSError(f"код {st}")
        info = json.loads(body)
        sha, url = info["checksums"]["sha256"], info["download_url"]
        if os.path.exists(_AUTHLIB_JAR) and _sha256_path(_AUTHLIB_JAR) == sha:
            os.utime(_AUTHLIB_JAR, None)
            return _AUTHLIB_JAR
        log(f"  [Auth] скачиваю authlib-injector {info.get('version', '')}...", "info")
        st, data = _http(url, timeout=120, max_bytes=20_000_000)
        if st != 200 or _hashlib.sha256(data).hexdigest() != sha:
            raise OSError("контрольная сумма не совпала")
    except Exception as e:
        log(f"  [Auth] authlib-injector.yushi.moe недоступен ({e}), пробую сервер lenta.co...", "warn")
        sha = (atomic_server_info(config).get("meta") or {}).get("atomic.agent_sha256")
        if os.path.exists(_AUTHLIB_JAR) and (not sha or _sha256_path(_AUTHLIB_JAR) == sha):
            return _AUTHLIB_JAR
        if not sha:
            raise AtomicAuthError("Не удалось скачать authlib-injector (ни с сайта, ни с сервера lenta.co)")
        st, data = _http(_atomic_url(config) + "/atomic/authlib-injector.jar", timeout=120, max_bytes=20_000_000)
        if st != 200 or _hashlib.sha256(data).hexdigest() != sha:
            raise AtomicAuthError("authlib-injector с сервера lenta.co повреждён")
    tmp = _AUTHLIB_JAR + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, _AUTHLIB_JAR)
    log("  [Auth] authlib-injector готов (SHA-256 проверен)", "ok")
    return _AUTHLIB_JAR


def _sha256_path(path: str) -> str:
    h = _hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_jvm_args(config, jar: str) -> list:
    """-javaagent + заранее полученные метаданные (игра стартует быстрее)."""
    _, raw = _http(_atomic_url(config) + "/", timeout=10)
    return [f"-javaagent:{jar}={_atomic_url(config)}",
            "-Dauthlibinjector.yggdrasil.prefetched=" + _b64.b64encode(raw).decode()]


# ══════════════════════════════════════════
#  CustomSkinLoader (только для Offline)
# ══════════════════════════════════════════

_CSL_SUPPORTED_MC = {
    "1.7.10", "1.8.9", "1.9.4", "1.10.2", "1.11.2", "1.12.2",
    "1.13.2", "1.14.4", "1.15.2", "1.16.5", "1.17.1", "1.18.2",
    "1.19.2", "1.19.4", "1.20.1", "1.20.4", "1.20.6", "1.21.1",
    "1.21.3", "1.21.4", "1.21.11",
}


def _csl_ensure(mc_dir: str, mc_version: str, loader: str, log_cb=None) -> bool:
    """Скачивает CustomSkinLoader с Modrinth (если ещё нет)."""
    import urllib.parse as _up
    if mc_version not in _CSL_SUPPORTED_MC:
        if log_cb: log_cb(f"  [CSL] MC {mc_version} не поддерживается CSL, пропускаю", "muted")
        return True
    mods_dir = os.path.join(mc_dir, "mods")
    os.makedirs(mods_dir, exist_ok=True)
    for f in os.listdir(mods_dir):
        if "customskinloader" in f.lower():
            if log_cb: log_cb(f"  [CSL] уже установлен: {f}", "muted")
            return True
    modrinth_loader = loader if loader in ("fabric", "forge", "neoforge") else "forge"
    try:
        params = _up.urlencode({"game_versions": json.dumps([mc_version]),
                                "loaders": json.dumps([modrinth_loader])})
        st, body = _http(f"https://api.modrinth.com/v2/project/customskinloader/version?{params}")
        versions = json.loads(body) if st == 200 else []
    except Exception as e:
        if log_cb: log_cb(f"  [CSL] Ошибка Modrinth: {e}", "warn")
        return False
    if not versions:
        if log_cb: log_cb(f"  [CSL] нет версии для MC {mc_version} / {modrinth_loader}", "muted")
        return True
    file_info = versions[0]["files"][0]
    dest = os.path.join(mods_dir, file_info["filename"])
    if log_cb: log_cb(f"  [CSL] скачиваю {file_info['filename']}...", "info")
    try:
        st, data = _http(file_info["url"], timeout=120, max_bytes=30_000_000)
        expected = (file_info.get("hashes") or {}).get("sha1")
        if st != 200 or (expected and _hashlib.sha1(data).hexdigest() != expected):
            raise OSError("файл повреждён")
        with open(dest, "wb") as f:
            f.write(data)
        if log_cb: log_cb(f"  [CSL] установлен ({len(data)//1024} KB)", "ok")
        return True
    except Exception as e:
        if log_cb: log_cb(f"  [CSL] ошибка загрузки: {e}", "warn")
        return False


_CSL_ONLINE_SOURCES = [
    {"name": "ElyBy", "type": "ElyByAPI", "root": "http://skinsystem.ely.by/textures/"},
    {"name": "TLauncher", "type": "ElyByAPI", "root": "https://auth.tlauncher.org/skin/profile/texture/login/"},
    {"name": "LittleSkin", "type": "CustomSkinAPI", "root": "https://littleskin.cn/csl/"},
]


def _csl_configure(mc_dir: str, config: dict, mode: str, log_cb=None):
    """mode: "offline" | "atomic" | "microsoft".
    Скины ищутся по нику: сервер lenta.co → Ely.by → TLauncher → LittleSkin → Mojang.
    Offline: свой скин сначала берётся из LocalSkin.
    Microsoft: только Mojang (скины приходят с лицензионного аккаунта)."""
    import shutil
    csl_dir = os.path.join(mc_dir, "CustomSkinLoader")
    if mode == "microsoft" and not os.path.isdir(csl_dir):
        return
    url = _atomic_url(config)
    server_src = [{"name": "AtomicServer", "type": "MojangAPI",
                   "apiRoot": url + "/api/", "sessionRoot": url + "/sessionserver/"}]
    mojang = [{"name": "Mojang", "type": "MojangAPI"}]
    if mode == "microsoft":
        loadlist = mojang
    elif mode == "atomic":
        loadlist = server_src + _CSL_ONLINE_SOURCES + mojang
    else:
        nick = config.get("nickname", "").strip()
        local_skins = os.path.join(csl_dir, "LocalSkin", "skins")
        os.makedirs(local_skins, exist_ok=True)
        src = _local_skin_path(config, nick) if nick else ""
        if src and os.path.exists(src):
            try:
                shutil.copy2(src, os.path.join(local_skins, f"{nick}.png"))
                if log_cb: log_cb(f"  [CSL] твой скин → LocalSkin/skins/{nick}.png", "muted")
            except Exception as e:
                if log_cb: log_cb(f"  [CSL] ошибка копирования скина: {e}", "warn")
        loadlist = [{
            "name": "LocalSkin", "type": "Legacy", "checkPNG": True,
            "skin": "LocalSkin/skins/{USERNAME}.png", "model": "auto",
            "cape": "LocalSkin/capes/{USERNAME}.png", "elytra": "LocalSkin/elytras/{USERNAME}.png",
        }] + server_src + _CSL_ONLINE_SOURCES + mojang
    cfg = {"version": 14, "loadlist": loadlist, "enableTransparentSkin": True,
           "forceLoadAllTextures": False, "enableLocalProfileCache": False, "threadPoolSize": 2}
    try:
        os.makedirs(csl_dir, exist_ok=True)
        with open(os.path.join(csl_dir, "CustomSkinLoader.json"), "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        if log_cb: log_cb(f"  [CSL] ошибка записи конфига: {e}", "warn")


# ══════════════════════════════════════════
#  UI: вход / регистрация на сервере lenta.co
# ══════════════════════════════════════════

def _atomic_auth_dialog(master, config, mode="login", on_success=None):
    """mode: "login" | "register" | "password" (смена пароля)."""
    titles = {"login": "🔑  ВХОД НА СЕРВЕР lenta.co", "register": "📝  РЕГИСТРАЦИЯ",
              "password": "🔒  СМЕНА ПАРОЛЯ"}
    dlg = tk.Toplevel(master)
    dlg.title(titles[mode].split("  ", 1)[1].title())
    dlg.configure(bg=C["bg"])
    dlg.resizable(False, False)
    dlg.transient(master)
    dlg.after(80, dlg.grab_set)

    tk.Frame(dlg, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(dlg, text="  " + titles[mode], bg=C["bg"], fg=C["orange"],
             font=_font(10, "bold"), pady=6).pack(anchor="w")
    tk.Label(dlg, text=f"  Сервер: {_atomic_url(config)}", bg=C["bg"],
             fg=C["text_dim"], font=FS).pack(anchor="w")
    form = tk.Frame(dlg, bg=C["bg"])
    form.pack(fill="x", padx=20, pady=(8, 0))
    fields = {}

    def field(key, label, show=None, value=""):
        tk.Label(form, text=label, bg=C["bg"], fg=C["text_muted"], font=FS).pack(anchor="w", pady=(6, 0))
        var = tk.StringVar(value=value)
        e = tk.Entry(form, textvariable=var, show=show or "", width=34,
                     bg=_glass_entry_bg(), fg=C["text"], font=_font(10), bd=0,
                     highlightthickness=1, highlightbackground=_glass_border(),
                     insertbackground=C["text"])
        e.pack(fill="x", ipady=3)
        fields[key] = (var, e)

    if mode == "password":
        field("old", "Текущий пароль", "•")
        field("new", "Новый пароль (от 8 символов)", "•")
        field("new2", "Новый пароль ещё раз", "•")
    else:
        default_nick = config.get("atomic_username") or config.get("nickname", "")
        field("user", "Ник (3–16 символов: латиница, цифры, _)", value=default_nick)
        field("pw", "Пароль" + (" (от 8 символов)" if mode == "register" else ""), "•")
        if mode == "register":
            field("pw2", "Пароль ещё раз", "•")
            field("invite", "Код приглашения (выдаёт админ сервера)")

    status = tk.Label(dlg, text="", bg=C["bg"], fg=C["red"], font=FS, wraplength=330, justify="left")
    status.pack(anchor="w", padx=20, pady=(8, 0))
    btns = tk.Frame(dlg, bg=C["bg"])
    btns.pack(fill="x", padx=20, pady=(6, 14))
    ok_btn = tk.Button(btns, text={"login": "  Войти  ", "register": "  Создать аккаунт  ",
                                   "password": "  Сменить  "}[mode],
                       bg=C["orange_glow"], fg=C["orange"], font=_font(9, "bold"),
                       relief="flat", highlightthickness=1, highlightbackground=C["orange"],
                       cursor="hand2", padx=8, pady=4)
    ok_btn.pack(side="left")
    tk.Button(btns, text="  Отмена  ", command=dlg.destroy, bg=_glass_panel(), fg=C["text_muted"],
              font=_font(9), relief="flat", cursor="hand2", padx=8, pady=4
              ).pack(side="left", padx=(8, 0))

    def val(k):
        return fields[k][0].get()

    def submit(_=None):
        status.config(text="", fg=C["red"])
        if mode == "password":
            if val("new") != val("new2"):
                return status.config(text="Новые пароли не совпадают")
            if len(val("new")) < 8:
                return status.config(text="Пароль слишком короткий (минимум 8)")
        else:
            nick = val("user").strip()
            if not re.fullmatch(r"[A-Za-z0-9_]{3,16}", nick):
                return status.config(text="Ник: 3–16 символов, латиница, цифры и _")
            if mode == "register":
                if val("pw") != val("pw2"):
                    return status.config(text="Пароли не совпадают")
                if len(val("pw")) < 8:
                    return status.config(text="Пароль слишком короткий (минимум 8)")
        ok_btn.config(state="disabled")
        status.config(text="⏳ Связываюсь с сервером...", fg=C["amber"])

        def work():
            try:
                if mode == "password":
                    atomic_change_password(config, val("old"), val("new"))
                    msg = "Пароль изменён. Войди с новым паролем."
                else:
                    if mode == "register":
                        atomic_register(config, val("user").strip(), val("pw"), val("invite"))
                    atomic_login(config, val("user").strip(), val("pw"))
                    msg = None
                dlg.after(0, lambda: done(None, msg))
            except AtomicAuthError as e:
                dlg.after(0, lambda err=str(e): done(err, None))
            except Exception as e:
                dlg.after(0, lambda err=f"Ошибка: {e}": done(err, None))

        threading.Thread(target=work, daemon=True).start()

    def done(err, msg):
        if not dlg.winfo_exists():
            return
        if err:
            ok_btn.config(state="normal")
            status.config(text="✗ " + err, fg=C["red"])
            return
        if msg:
            messagebox.showinfo("Аккаунт", msg, parent=dlg)
        dlg.destroy()
        if on_success:
            on_success()

    ok_btn.config(command=submit)
    for _, e in fields.values():
        e.bind("<Return>", submit)
    first = next(iter(fields.values()))[1]
    if mode != "password" and fields["user"][0].get():
        fields["pw"][1].focus_set()
    else:
        first.focus_set()
    dlg.update_idletasks()
    dlg.geometry(f"+{master.winfo_rootx() + 60}+{master.winfo_rooty() + 60}")


# ══════════════════════════════════════════
#  UI: менеджер скинов
# ══════════════════════════════════════════

def _show_skin_manager(master, config):
    win = tk.Toplevel(master)
    win.title("🎨  Мой скин")
    win.geometry("640x620")
    win.minsize(560, 560)
    win.configure(bg=C["bg"])

    acct = config.get("account_type", "offline")
    if acct == "atomic" and not config.get("atomic_access_token"):
        acct = "offline"
    nick = {"atomic": config.get("atomic_username"), "microsoft": config.get("ms_username")}.get(
        acct) or config.get("nickname", "").strip()
    target = {
        "atomic": ("Сервер lenta.co", "скин загрузится на сервер — его увидят все игроки"),
        "microsoft": ("Microsoft", "скин сменится на лицензионном аккаунте (виден везде)"),
        "offline": ("Offline", "скин сохранится локально и будет виден тебе в игре"),
    }[acct]

    hdr = tk.Frame(win, bg=C["bg_header"]); hdr.pack(fill="x")
    tk.Frame(hdr, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(hdr, text="  🎨  МОЙ СКИН", bg=C["bg_header"], fg=C["orange"],
             font=_font(11, "bold"), pady=6).pack(side="left")
    tk.Label(hdr, text=f"{nick or '(ник не задан)'}  •  {target[0]}  ", bg=C["bg_header"],
             fg=C["amber"], font=_font(9, "bold")).pack(side="right")

    body = tk.Frame(win, bg=C["bg"]); body.pack(fill="both", expand=True, padx=16, pady=10)
    left = tk.Frame(body, bg=C["bg_panel"], width=170, highlightthickness=1,
                    highlightbackground=C["border"])
    left.pack(side="left", fill="y")
    left.pack_propagate(False)
    right = tk.Frame(body, bg=C["bg"]); right.pack(side="left", fill="both", expand=True, padx=(14, 0))

    preview = tk.Label(left, text="нет скина", bg=C["bg_panel"], fg=C["text_dim"], font=FS)
    preview.pack(expand=True)
    preview_cap = tk.Label(left, text="", bg=C["bg_panel"], fg=C["text_muted"], font=FS, wraplength=150)
    preview_cap.pack(pady=(0, 8))

    state = {"png": None, "model": "default"}
    model_var = tk.StringVar(value="default")

    def show(png, model, caption):
        state["png"], state["model"] = png, model
        model_var.set(model)
        preview_cap.config(text=caption)
        redraw()

    def redraw():
        if not state["png"]:
            return
        try:
            from PIL import ImageTk as _ITk
            img = _ITk.PhotoImage(_render_skin_preview(state["png"], model_var.get(), 5))
            preview.config(image=img, text=""); preview.image = img
        except Exception:
            preview.config(image="", text="PNG загружен\n(для превью нужен Pillow)")

    # ── Источник ──────────────────────────────────────────────────────
    tk.Label(right, text="ОТКУДА ВЗЯТЬ СКИН", bg=C["bg"], fg=C["amber"], font=FSB).pack(anchor="w")
    src_var = tk.StringVar(value=SKIN_SOURCES[0][1])
    src_cb = ttk.Combobox(right, textvariable=src_var, values=[s[1] for s in SKIN_SOURCES],
                          state="readonly", style="AI.TCombobox", font=FS, width=38)
    src_cb.pack(anchor="w", pady=(4, 6))

    q_row = tk.Frame(right, bg=C["bg"]); q_row.pack(fill="x")
    q_var = tk.StringVar(value=nick or "")
    q_entry = tk.Entry(q_row, textvariable=q_var, bg=_glass_entry_bg(), fg=C["text"],
                       font=_font(10), bd=0, highlightthickness=1,
                       highlightbackground=_glass_border(), insertbackground=C["text"])
    q_entry.pack(side="left", fill="x", expand=True, ipady=3)
    browse_btn = tk.Button(q_row, text=" … ", bg=_glass_panel(), fg=C["accent"], font=FS,
                           relief="flat", cursor="hand2", padx=4)
    find_btn = tk.Button(q_row, text="  НАЙТИ  ", bg=C["orange_glow"], fg=C["orange"],
                         font=_font(8, "bold"), relief="flat", cursor="hand2",
                         highlightthickness=1, highlightbackground=C["orange"], padx=6, pady=2)
    find_btn.pack(side="right", padx=(6, 0))
    hint = tk.Label(right, text="", bg=C["bg"], fg=C["text_dim"], font=FS, justify="left", wraplength=380)
    hint.pack(anchor="w", pady=(4, 0))

    def src_key():
        return next(k for k, lbl in SKIN_SOURCES if lbl == src_var.get())

    def on_src(_=None):
        k = src_key()
        browse_btn.pack_forget()
        if k == "file":
            browse_btn.pack(side="right", padx=(6, 0))
            q_var.set("")
            hint.config(text="PNG 64×64 или 64×32 (HD-скины кратно 64 тоже подходят)")
        elif k == "url":
            q_var.set("https://")
            hint.config(text="Ссылка прямо на PNG-файл скина")
        else:
            if not q_var.get() or q_var.get().startswith("http") or os.sep in q_var.get():
                q_var.set(nick or "")
            hint.config(text={"mojang": "Ник лицензионного аккаунта Minecraft",
                              "elyby": "Ник на ely.by",
                              "tlauncher": "Ник в TLauncher (скин из TLauncher Skins)",
                              "littleskin": "Ник персонажа на littleskin.cn"}[k])

    def browse():
        p = filedialog.askopenfilename(title="Выбери скин", parent=win,
                                       filetypes=[("PNG", "*.png"), ("Все файлы", "*.*")])
        if p:
            q_var.set(p)
            find()

    browse_btn.config(command=browse)
    src_cb.bind("<<ComboboxSelected>>", on_src)

    # ── Модель ────────────────────────────────────────────────────────
    mrow = tk.Frame(right, bg=C["bg"]); mrow.pack(anchor="w", pady=(12, 0))
    tk.Label(mrow, text="Модель:", bg=C["bg"], fg=C["text_muted"], font=FS).pack(side="left")
    for v, t in (("default", "Steve (широкие руки)"), ("slim", "Alex (тонкие руки)")):
        tk.Radiobutton(mrow, text=t, variable=model_var, value=v, command=redraw,
                       bg=C["bg"], fg=C["text"], selectcolor=_glass_entry_bg(),
                       activebackground=C["bg"], activeforeground=C["orange"],
                       font=FS, cursor="hand2").pack(side="left", padx=(8, 0))

    # ── Действия ──────────────────────────────────────────────────────
    sep(right).pack(fill="x", pady=12)
    tk.Label(right, text=f"Применить → {target[1]}", bg=C["bg"], fg=C["text_muted"],
             font=FS, wraplength=380, justify="left").pack(anchor="w")
    act = tk.Frame(right, bg=C["bg"]); act.pack(anchor="w", pady=(6, 0))
    apply_btn = tk.Button(act, text="  ✔  ПРИМЕНИТЬ  ", bg=C["orange_glow"], fg=C["green"],
                          font=_font(9, "bold"), relief="flat", cursor="hand2",
                          highlightthickness=1, highlightbackground=C["green"], padx=8, pady=5)
    apply_btn.pack(side="left")
    save_btn = tk.Button(act, text="  💾 Сохранить PNG  ", bg=_glass_panel(), fg=C["text_muted"],
                         font=FS, relief="flat", cursor="hand2", padx=6, pady=5)
    save_btn.pack(side="left", padx=(8, 0))
    status = tk.Label(right, text="", bg=C["bg"], fg=C["green"], font=FS, wraplength=380, justify="left")
    status.pack(anchor="w", pady=(8, 0))

    if acct == "offline":
        tk.Label(right,
                 text="ℹ  В Offline чужие скины подтягиваются сами (мод CustomSkinLoader):\n"
                      "   по нику из Ely.by, TLauncher, LittleSkin и Mojang.\n"
                      "   Чтобы скин видели все — заведи аккаунт на «Сервере lenta.co».",
                 bg=C["bg"], fg=C["text_dim"], font=FS, justify="left").pack(anchor="w", pady=(14, 0))

    def busy(on, text=""):
        for b in (find_btn, apply_btn):
            b.config(state="disabled" if on else "normal")
        if text:
            status.config(text=text, fg=C["amber"] if on else C["green"])

    def find(_=None):
        k, q = src_key(), q_var.get().strip()
        busy(True, "⏳ Ищу скин...")

        def work():
            try:
                res = skin_fetch(k, q)
                win.after(0, lambda: (show(res["png"], res["model"], res["label"]), busy(False, "✓ Скин найден")))
            except Exception as e:
                win.after(0, lambda err=str(e): (busy(False), status.config(text="✗ " + err, fg=C["red"])))
        threading.Thread(target=work, daemon=True).start()

    def apply():
        if not state["png"]:
            return status.config(text="Сначала найди или выбери скин", fg=C["red"])
        png, model = state["png"], model_var.get()
        busy(True, "⏳ Применяю...")

        def work():
            try:
                if acct == "atomic":
                    atomic_upload_skin(config, png, model)
                    msg = "✓ Скин загружен на сервер lenta.co — все его увидят"
                elif acct == "microsoft":
                    ms_upload_skin(config, png, model)
                    msg = "✓ Скин лицензионного аккаунта изменён"
                else:
                    if not nick:
                        raise AtomicAuthError("Сначала впиши ник на главном экране")
                    with open(_local_skin_path(config, nick), "wb") as f:
                        f.write(png)
                    msg = "✓ Сохранён. Появится в игре при следующем запуске"
                win.after(0, lambda: busy(False, msg))
            except Exception as e:
                win.after(0, lambda err=str(e): (busy(False), status.config(text="✗ " + err, fg=C["red"])))
        threading.Thread(target=work, daemon=True).start()

    def save_png():
        if not state["png"]:
            return
        p = filedialog.asksaveasfilename(parent=win, defaultextension=".png",
                                         initialfile=_skin_filename(nick or "skin"),
                                         filetypes=[("PNG", "*.png")])
        if p:
            with open(p, "wb") as f:
                f.write(state["png"])
            status.config(text=f"✓ Сохранено: {p}", fg=C["green"])

    find_btn.config(command=find)
    apply_btn.config(command=apply)
    save_btn.config(command=save_png)
    q_entry.bind("<Return>", find)
    on_src()

    # Текущий скин
    def load_current():
        try:
            if acct == "atomic":
                png, model = atomic_get_skin(config)
                cap = "Сейчас на сервере"
            else:
                p = _local_skin_path(config, nick) if nick else ""
                png = open(p, "rb").read() if p and os.path.exists(p) else None
                model, cap = (_guess_model(png) if png else "default"), "Сейчас (локально)"
            if png:
                win.after(0, lambda: show(png, model, cap))
        except Exception:
            pass
    threading.Thread(target=load_current, daemon=True).start()


# ══════════════════════════════════════════
#  ЗАЩИТА НИКА lenta212
# ══════════════════════════════════════════
_PROTECTED_NICK = "lenta212"

# Пароль в открытом виде в коде не хранится — только соль и PBKDF2-хеш.
# Новый хеш: python launcher.py --make-nick-hash
_NICK_PW_SALT = "007bc07cec23099830be78dcfeda9371"
_NICK_PW_HASH = "edf4b10983f8dc20b12f7f28b43e1a0c9dfa0840b8961ee93949f9bc95b68e5e"
_NICK_PW_ITER = 300000


def _hash_nick_password(password: str, salt: bytes, iterations: int = _NICK_PW_ITER) -> str:
    import hashlib as _hl
    return _hl.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()


def _check_nick_password(password: str) -> bool:
    """Сравнение хеша за постоянное время (без утечки по таймингу)."""
    import hmac as _hmac
    try:
        calc = _hash_nick_password(password, bytes.fromhex(_NICK_PW_SALT), _NICK_PW_ITER)
        return _hmac.compare_digest(calc, _NICK_PW_HASH)
    except Exception:
        return False

# Похожие ники которые тоже требуют пароль
_PROTECTED_NICK_VARIANTS = {
    "lenta212", "lenta_212", "lenta-212", "1enta212", "lenta2l2",
    "lenta21z", "lenta21", "lenta2", "lenta", "l3nta212",
    "lenta212_", "_lenta212", "lenta212x", "xlenta212",
}

def _is_protected_nick(nickname: str) -> bool:
    """Проверяет является ли ник защищённым (точное совпадение или похожий)."""
    nl = nickname.lower().strip()
    if nl in _PROTECTED_NICK_VARIANTS:
        return True
    # Дополнительно — если содержит "lenta" и "212"
    if "lenta" in nl and "212" in nl:
        return True
    return False

def _check_nick_allowed(nickname: str, config: dict) -> tuple:
    """Возвращает (allowed: bool, reason: str)."""
    if _is_protected_nick(nickname):
        return False, "protected"
    return True, ""

def _ask_nick_password(parent) -> bool:
    """Диалог ввода пароля для защищённого ника. Возвращает True если пароль верный."""
    dlg = tk.Toplevel(parent)
    dlg.title("Защищённый ник")
    dlg.geometry("360x180"); dlg.resizable(False, False)
    dlg.configure(bg=C["bg"]); dlg.grab_set()
    tk.Label(dlg, text="  ⚠  Этот ник защищён.", bg=C["bg"], fg=C["orange"],
             font=_font(10, "bold")).pack(pady=(16,4))
    tk.Label(dlg, text="Введи пароль для использования этого ника:",
             bg=C["bg"], fg=C["text_muted"], font=FS).pack()
    pw_var = tk.StringVar()
    pw_entry = tk.Entry(dlg, textvariable=pw_var, show="•",
                        bg=_glass_entry_bg(), fg=C["text"], font=_font(10),
                        bd=0, highlightthickness=1, highlightbackground=C["orange"],
                        insertbackground=C["text"])
    pw_entry.pack(padx=30, fill="x", pady=8)
    pw_entry.focus_set()
    result = [False]
    def _ok():
        if _check_nick_password(pw_var.get()):
            result[0] = True; dlg.destroy()
        else:
            pw_entry.config(highlightbackground=C["red"])
            pw_var.set("")
    def _cancel(): dlg.destroy()
    btn_row = tk.Frame(dlg, bg=C["bg"]); btn_row.pack()
    tk.Button(btn_row, text=" OK ", command=_ok,
              bg=C["orange_glow"], fg=C["orange"], font=_font(9, "bold"),
              relief="flat", cursor="hand2", padx=10, pady=4).pack(side="left")
    tk.Button(btn_row, text=" Отмена ", command=_cancel,
              bg=_glass_panel(), fg=C["text_muted"], font=_font(9),
              relief="flat", cursor="hand2", padx=10, pady=4).pack(side="left", padx=(8,0))
    pw_entry.bind("<Return>", lambda _: _ok())
    dlg.wait_window()
    return result[0]


if len(sys.argv) > 1 and sys.argv[1] == "--make-nick-hash":
    import getpass
    _pw = getpass.getpass("Новый пароль для защищённого ника: ")
    _salt = os.urandom(16)
    print(f'_NICK_PW_SALT = "{_salt.hex()}"')
    print(f'_NICK_PW_HASH = "{_hash_nick_password(_pw, _salt)}"')
    sys.exit(0)


def build_ui(root, config, max_ram, launch_btn=None):
    """Главное окно. Сетка из трёх строк:
         0 — шапка (сцена темы, название, аккаунт, настройки);
         1 — тело с карточками (прокручивается, если окно маленькое);
         2 — подвал с прогрессом и кнопкой «Играть» — ВСЕГДА виден.
    Тайловые оконные менеджеры (Hyprland, Sway, i3) могут дать окну любой
    размер: минимальный размер маленький, а всё, что не влезло, уезжает в
    прокрутку, но не под край окна."""
    global _GLASS_STRENGTH, _ui_state
    if _ui_state.get("bg") is not None:
        _ui_state["bg"].destroy()
    if _ui_state.get("banner_fx") is not None:
        try:
            _ui_state["banner_fx"].destroy()
        except Exception:
            pass
    _stop_all_fx()
    try:
        root.unbind_all("<MouseWheel>")
        root.unbind_all("<Button-4>")
        root.unbind_all("<Button-5>")
    except Exception:
        pass
    for w in root.winfo_children():
        if isinstance(w, tk.Toplevel):
            continue
        w.destroy()
    _ui_state = {"bg": None, "banner_fx": None}

    _GLASS_STRENGTH = float(config.get("glass_strength", 0.3))
    root.configure(bg=C["bg"])
    apply_styles()
    try:
        icon_img = make_atom_icon(32)
        root.iconphoto(True, icon_img)
        root._icon_ref = icon_img
    except Exception:
        pass

    soft = bool(C.get("soft_ui"))
    card_bg = _glass_panel() if _is_fx_theme() else C["bg_panel"]
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)
    root.grid_columnconfigure(0, weight=1)

    # ══ ШАПКА ════════════════════════════════════════════════════════════
    if C.get("night_fx"):
        # Высота сцены подстраивается под окно: в маленьком (тайлинг) — ниже
        _bh = [150 if root.winfo_height() < 2 or root.winfo_height() >= 620 else 100]
        header_canvas = tk.Canvas(root, height=_bh[0], bg=C["bg_header"], highlightthickness=0)
        header_canvas.grid(row=0, column=0, sticky="ew")

        def _draw_banner(W):
            BANNER_H = _bh[0]
            if _ui_state.get("banner_fx") is not None:
                _ui_state["banner_fx"].resize(W, BANNER_H)
            else:
                fx = NightHouseFX(header_canvas, W, BANNER_H)
                fx.start()
                _ui_state["banner_fx"] = fx
            big = BANNER_H >= 140
            header_canvas.delete("title")
            header_canvas.create_text(26, BANNER_H - (56 if big else 46), text="ATOMIC", anchor="w", tags="title",
                                      fill=C["text"], font=(_UI_FAMILY, 28 if big else 20, "bold"))
            header_canvas.create_text(28, BANNER_H - (24 if big else 20), anchor="w", tags="title", fill=C["text_muted"],
                                      text="dev:lenta212&WhiteDuck  ·  v" + LAUNCHER_VERSION
                                           + ("  ·  DEV" if is_dev_mode() else ""),
                                      font=_font(9))
            header_canvas.tag_raise("title")
    else:
        header_canvas = draw_header(root, width=max(root.winfo_width(), 640), height=80, config=config)
        header_canvas.grid(row=0, column=0, sticky="ew")

        def _draw_banner(W):
            header_canvas.config(width=W)
            _redraw_header_content(header_canvas, W, 80, config=config)

    _banner_w = [0]

    def _on_header_resize(e):
        if abs(e.width - _banner_w[0]) >= 4:
            _banner_w[0] = e.width
            _draw_banner(e.width)
    header_canvas.bind("<Configure>", _on_header_resize)

    def _on_root_resize(e):
        if e.widget is not root or not C.get("night_fx"):
            return
        want = 150 if e.height >= 620 else 100
        if want != _bh[0]:
            _bh[0] = want
            try:
                header_canvas.config(height=want)
                _draw_banner(max(header_canvas.winfo_width(), 200))
            except tk.TclError:
                pass
    if C.get("night_fx"):
        root.bind("<Configure>", _on_root_resize)

    hdr_bg = C["bg_header"]
    top_right = tk.Frame(header_canvas, bg=hdr_bg)
    top_right.place(relx=1.0, x=-14, y=14, anchor="ne")

    acct_type = config.get("account_type", "offline")
    if acct_type == "atomic" and config.get("atomic_access_token"):
        chip = f"●  {config.get('atomic_username')}  ·  сервер lenta.co"
    elif acct_type == "microsoft" and config.get("ms_access_token"):
        chip = f"●  {config.get('ms_username')}  ·  Microsoft"
    else:
        chip = f"{config.get('nickname') or 'без ника'}  ·  offline"
    FlatButton(top_right, chip, command=lambda: open_settings(), kind="secondary",
               font=_font(9, "bold"), padx=12, pady=6, bg=hdr_bg).pack(side="left", padx=(0, 8))
    FlatButton(top_right, "⚙  Настройки", command=lambda: open_settings(), kind="secondary",
               font=_font(9, "bold"), padx=12, pady=6, bg=hdr_bg).pack(side="left")

    # ══ ТЕЛО: карточки на Canvas (фон старых тем виден между ними) ═══════
    body_wrap = tk.Frame(root, bg=C["bg"])
    body_wrap.grid(row=1, column=0, sticky="nsew")
    body_wrap.grid_rowconfigure(0, weight=1)
    body_wrap.grid_columnconfigure(0, weight=1)
    body = tk.Canvas(body_wrap, bg=C["bg"], highlightthickness=0, bd=0)
    body.grid(row=0, column=0, sticky="nsew")
    vbar = ttk.Scrollbar(body_wrap, orient="vertical", command=body.yview,
                         style="Soft.Vertical.TScrollbar" if soft else "Vertical.TScrollbar")
    body.configure(yscrollcommand=vbar.set)
    _ui_state["bg"] = _BodyBackground(body, config)

    def make_card(title, extra=None):
        outer = tk.Frame(body, bg=card_bg, highlightthickness=1,
                         highlightbackground=C["border"] if soft else _glass_border())
        head = tk.Frame(outer, bg=card_bg)
        head.pack(fill="x", padx=18, pady=(14, 6))
        tk.Label(head, text=title.upper() if not soft else title, bg=card_bg, fg=C["amber"],
                 font=_font(10, "bold")).pack(side="left")
        if extra:
            extra(head)
        inner = tk.Frame(outer, bg=card_bg)
        inner.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        return outer, inner

    def field_label(parent, text, pady=(10, 4)):
        tk.Label(parent, text=text, bg=card_bg, fg=C["text_muted"], font=_font(9, "bold"),
                 anchor="w").pack(fill="x", pady=pady)

    def hint(parent, textvariable=None, text="", pady=(4, 0)):
        lab = tk.Label(parent, text=text, textvariable=textvariable, bg=card_bg, fg=C["text_dim"],
                       font=_font(8), anchor="w", justify="left")
        lab.pack(fill="x", pady=pady)
        # перенос строк по ширине карточки — текст не обрезается в узком окне
        lab.bind("<Configure>", lambda e: e.widget.config(wraplength=max(80, e.width - 4)))
        return lab

    # ── Карточка «Игра» ───────────────────────────────────────────────────
    card_game, g = make_card("Игра")
    field_label(g, "Версия", pady=(0, 4))
    ver_row = tk.Frame(g, bg=card_bg); ver_row.pack(fill="x")
    version_box = mk_cb(ver_row, list(get_all_versions().keys()), width=12)
    version_box.pack(side="left", fill="x", expand=True)
    sel = config["selected_version"]
    version_box.set(sel if sel in get_all_versions() else "1.20.1 Forge")

    def refresh_version_list(select=None):
        all_vers = get_all_versions()
        current = select or version_box.get()
        version_box["values"] = list(all_vers.keys())
        version_box.set(current if current in all_vers else (list(all_vers)[0] if all_vers else ""))
        _update_sz()

    def open_ver_manager():
        open_version_manager(root)
        refresh_version_list()

    def open_importer():
        _show_import_dialog(root, on_done=lambda name: (refresh_version_list(name), on_version_change(None)))

    FlatButton(ver_row, "Версии…", command=open_ver_manager, bg=card_bg).pack(side="left", padx=(8, 0))
    FlatButton(ver_row, "Импорт", command=open_importer, bg=card_bg).pack(side="left", padx=(6, 0))
    sz_lbl_var = tk.StringVar(value="")
    hint(g, textvariable=sz_lbl_var)

    def _update_sz(*_):
        v = version_box.get()
        info = get_all_versions().get(v, {})
        loader = {"vanilla": "Vanilla", "forge": "Forge", "fabric": "Fabric", "neoforge": "NeoForge",
                  "external": "из другого лаунчера"}.get(info.get("loader", ""), info.get("loader", ""))
        parts = [f"Minecraft {info.get('mc_version', '?')}", loader]
        if info.get("source"):
            parts.append(f"импорт: {info['source']}")
        sz = VERSION_SIZES.get(v, 0)
        if sz:
            parts.append(f"≈{sz} МБ")
        sz_lbl_var.set("  ·  ".join(p for p in parts if p))
    def on_version_change(event):
        config["selected_version"] = version_box.get()
        _update_sz()
    version_box.bind("<<ComboboxSelected>>", on_version_change)
    _update_sz()

    field_label(g, "Папка, куда ставятся игры")
    path_row = tk.Frame(g, bg=card_bg); path_row.pack(fill="x")
    path_var = tk.StringVar(value=config["install_path"])
    _pe = StyledEntry(path_row, textvariable=path_var)
    _pe.pack(side="left", fill="x", expand=True)
    try:
        _pe._entry.config(width=8)
    except (AttributeError, tk.TclError):
        pass

    def choose_folder():
        d = filedialog.askdirectory(parent=root)
        if d:
            path_var.set(d)

    def open_game_folder():
        info = get_all_versions().get(version_box.get(), {})
        target = info.get("game_dir") or info.get("external_dir")
        if not target:
            base = path_var.get().strip()
            if not base:
                messagebox.showwarning("Atomic", "Сначала выбери папку для игр.", parent=root)
                return
            target = get_mc_dir(base, version_box.get())
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)
        open_file(target)

    FlatButton(path_row, "Обзор", command=choose_folder, bg=card_bg).pack(side="left", padx=(8, 0))
    FlatButton(path_row, "Открыть", command=open_game_folder, bg=card_bg).pack(side="left", padx=(6, 0))
    hint(g, text="«Открыть» — папка выбранной версии: моды, миры, скриншоты.")

    console_var = tk.BooleanVar(value=config.get("show_console", False))
    tk.Checkbutton(g, text="Показывать окно консоли игры", variable=console_var,
                   bg=card_bg, fg=C["text_muted"], selectcolor=C["bg_input"],
                   activebackground=card_bg, activeforeground=C["accent"],
                   font=_font(9), cursor="hand2", bd=0, highlightthickness=0,
                   anchor="w").pack(fill="x", pady=(12, 0))

    # ── Карточка «Игрок» ──────────────────────────────────────────────────
    card_player, pl = make_card("Игрок")
    field_label(pl, "Ник", pady=(0, 4))
    nickname_var = tk.StringVar(value=config["nickname"])
    nick_row = tk.Frame(pl, bg=card_bg); nick_row.pack(fill="x")
    _ms_active = None
    if acct_type == "microsoft" and config.get("ms_access_token") and config.get("ms_username"):
        _ms_active = (config["ms_username"], "Microsoft")
    elif acct_type == "atomic" and config.get("atomic_access_token") and config.get("atomic_username"):
        _ms_active = (config["atomic_username"], "сервер lenta.co")
    if _ms_active:
        nickname_var.set(_ms_active[0])
    _nick_entry_obj = StyledEntry(nick_row, textvariable=nickname_var)
    _nick_entry_obj.pack(side="left", fill="x", expand=True)
    if _ms_active:
        try:
            _nick_entry_obj._entry.config(state="readonly", readonlybackground=C["bg_input"])
        except tk.TclError:
            pass
        hint(pl, text=f"Ник берётся из аккаунта ({_ms_active[1]}). Сменить — кнопка «Аккаунт».")
    else:
        hint(pl, text="Offline: впиши любой ник. Для сервера lenta.co нужен аккаунт.")

    _prev_nick = [config["nickname"]]

    def _on_nick_change(event=None):
        new_nick = nickname_var.get().strip()
        if new_nick == _prev_nick[0]:
            return
        allowed, reason = _check_nick_allowed(new_nick, config)
        if not allowed and reason == "protected" and not _ask_nick_password(root):
            nickname_var.set(_prev_nick[0])
            return
        _prev_nick[0] = new_nick

    if not _ms_active:
        _nick_entry_obj._entry.bind("<FocusOut>", _on_nick_change)
        _nick_entry_obj._entry.bind("<Return>", _on_nick_change)

    btns = tk.Frame(pl, bg=card_bg); btns.pack(fill="x", pady=(12, 0))
    FlatButton(btns, "Скин", command=lambda: _show_skin_manager(root, config), bg=card_bg).pack(side="left")
    FlatButton(btns, "Аккаунт", command=lambda: open_settings(), bg=card_bg).pack(side="left", padx=(8, 0))

    field_label(pl, "Память для игры", pady=(16, 4))
    mem_row = tk.Frame(pl, bg=card_bg); mem_row.pack(fill="x")
    try:
        mem_init = int(config.get("memory", 4))
    except (TypeError, ValueError):
        mem_init = 4
    max_mem = max(2, max_ram - 1)
    mem_int = tk.IntVar(value=min(max(2, mem_init), max_mem))
    memory_box = tk.StringVar(value=str(mem_int.get()))
    mem_lbl = tk.Label(mem_row, text=f"{mem_int.get()} ГБ", bg=card_bg, fg=C["text"],
                       font=_font(11, "bold"), width=6, anchor="e")

    def _on_mem(v):
        val = int(round(float(v)))
        mem_int.set(val)
        memory_box.set(str(val))
        mem_lbl.config(text=f"{val} ГБ")
    ttk.Scale(mem_row, from_=2, to=max_mem, orient="horizontal", variable=mem_int,
              command=_on_mem, style="AI.Horizontal.TScale").pack(side="left", fill="x", expand=True)
    mem_lbl.pack(side="left", padx=(10, 0))
    hint(pl, text=f"В компьютере {max_ram} ГБ. Обычно хватает 4–6 ГБ, большим сборкам — 8+.")

    # ── Карточка «Журнал» ────────────────────────────────────────────────
    def _log_head(head):
        FlatButton(head, "Очистить", command=lambda: _clear_log(), kind="ghost", font=_font(9),
                   padx=6, pady=0, bg=card_bg).pack(side="right")
    card_log, lg = make_card("Журнал", extra=_log_head)
    log_box = tk.Text(lg, height=3, state="disabled", bg=C["log_bg"] if not _is_fx_theme() else _glass_log(),
                      fg=C["text_muted"], bd=0, highlightthickness=0, font=FLG, wrap="word",
                      selectbackground=C["accent_glow"], padx=10, pady=8)
    log_box.pack(fill="both", expand=True)
    for tag, col in [("info", C["text"]), ("ok", C["green"]), ("warn", C["orange"]),
                     ("error", C["red"]), ("muted", C["text_muted"])]:
        log_box.tag_config(tag, foreground=col)

    def _clear_log():
        _game_state["log_lines"] = []
        log_box.config(state="normal"); log_box.delete("1.0", tk.END); log_box.config(state="disabled")

    cards = {
        "game": body.create_window(0, 0, window=card_game, anchor="nw"),
        "player": body.create_window(0, 0, window=card_player, anchor="nw"),
        "log": body.create_window(0, 0, window=card_log, anchor="nw"),
    }
    _layout_pending = [False]

    def _relayout():
        _layout_pending[0] = False
        W, H = body.winfo_width(), body.winfo_height()
        if W < 50:
            return
        m = 14 if W < 700 else 18
        two = W >= 840
        if two:
            colw = (W - 3 * m) // 2
            body.itemconfigure(cards["game"], width=colw, height=0)
            body.itemconfigure(cards["player"], width=colw, height=0)
        else:
            body.itemconfigure(cards["game"], width=W - 2 * m, height=0)
            body.itemconfigure(cards["player"], width=W - 2 * m, height=0)
        body.itemconfigure(cards["log"], width=W - 2 * m, height=0)
        body.update_idletasks()
        hg, hp = card_game.winfo_reqheight(), card_player.winfo_reqheight()
        if two:
            top = max(hg, hp)
            body.coords(cards["game"], m, m)
            body.coords(cards["player"], 2 * m + colw, m)
            body.itemconfigure(cards["game"], height=top)
            body.itemconfigure(cards["player"], height=top)
            y = m + top + m
        else:
            body.coords(cards["game"], m, m)
            body.coords(cards["player"], m, m + hg + m)
            y = m + hg + m + hp + m
        log_h = max(card_log.winfo_reqheight(), H - y - m)
        body.coords(cards["log"], m, y)
        body.itemconfigure(cards["log"], height=log_h)
        total = y + log_h + m
        body.configure(scrollregion=(0, 0, W, max(total, H)))
        if total > H + 2:
            vbar.grid(row=0, column=1, sticky="ns")
        else:
            vbar.grid_remove()
            body.yview_moveto(0)
        if _ui_state.get("bg") is not None:
            _ui_state["bg"].resize(W, max(total, H))

    def _schedule_layout(_=None):
        if not _layout_pending[0]:
            _layout_pending[0] = True
            body.after_idle(_relayout)
    body.bind("<Configure>", _schedule_layout)
    for c in (card_game, card_player):
        c.bind("<Configure>", lambda e: None)

    def _wheel(e):
        if not str(e.widget).startswith(str(body)) or isinstance(e.widget, tk.Text):
            return
        if vbar.winfo_ismapped():
            delta = -1 if (getattr(e, "num", 0) == 4 or getattr(e, "delta", 0) > 0) else 1
            body.yview_scroll(delta * 3, "units")
    root.bind_all("<MouseWheel>", _wheel, add="+")
    root.bind_all("<Button-4>", _wheel, add="+")
    root.bind_all("<Button-5>", _wheel, add="+")

    # ══ ПОДВАЛ: прогресс + «Играть» — всегда на виду ════════════════════
    foot_bg = C["bg_header"]
    footer = tk.Frame(root, bg=foot_bg)
    footer.grid(row=2, column=0, sticky="ew")
    tk.Frame(footer, height=1, bg=C["border"]).pack(fill="x", side="top")
    frow = tk.Frame(footer, bg=foot_bg)
    frow.pack(fill="x", padx=22, pady=14)
    status_col = tk.Frame(frow, bg=foot_bg)   # пакуется ПОСЛЕ кнопки: кнопке место даётся первой
    prog_lbl_var = tk.StringVar(value="")
    tk.Label(status_col, textvariable=prog_lbl_var, bg=foot_bg, fg=C["text"], font=_font(10),
             anchor="w").pack(fill="x")
    progress = ttk.Progressbar(status_col, style="AI.Horizontal.TProgressbar", mode="determinate", maximum=100)
    progress.pack(fill="x", pady=(6, 4))
    tk.Label(status_col, text=f"v{LAUNCHER_VERSION}  ·  RAM {max_ram} ГБ  ·  {platform.system()}  ·  lenta212"
             + ("  ·  DEV" if is_dev_mode() else ""),
             bg=foot_bg, fg=C["text_dim"], font=_font(8), anchor="w").pack(fill="x")

    def _cancel_download():
        _CANCEL_EVENT.set()
        cancel_btn.set_enabled(False)
        prog_lbl_var.set("Отменяю...")

    launch_btn = IndustrialButton(frow, mode=_game_state["btn_mode"], w=240, h=54, bg=foot_bg)
    launch_btn.pack(side="right")
    status_col.pack(side="left", fill="x", expand=True, padx=(0, 18))
    cancel_btn = FlatButton(frow, "✕  Отмена", command=_cancel_download, kind="danger", bg=foot_bg)
    _orig_set_mode = launch_btn.set_mode

    def _set_mode(mode):
        _orig_set_mode(mode)
        if mode == "loading":
            cancel_btn.set_enabled(True)
            cancel_btn.pack(side="right", padx=(0, 10), after=launch_btn)
        else:
            cancel_btn.pack_forget()
    launch_btn.set_mode = _set_mode
    if _game_state["btn_mode"] == "loading":
        _set_mode("loading")

    # Восстановить лог и прогресс после пересборки окна (смена темы)
    if _game_state["log_lines"]:
        log_box.config(state="normal")
        for _lt, _ll in _game_state["log_lines"]:
            log_box.insert(tk.END, _lt + "\n", _ll)
        log_box.see(tk.END); log_box.config(state="disabled")
    progress["value"] = _game_state["progress"]
    prog_lbl_var.set(_game_state["progress_label"] or "Готов к игре")

    def set_progress(val, label=""):
        _game_state["progress"] = val; _game_state["progress_label"] = label
        root.after(0, lambda v=val, lb=label: (_prog(v, lb)))
    def _prog(val, label): progress["value"] = val; prog_lbl_var.set(label)

    def log(text, level="info"):
        _game_state["log_lines"].append((text, level))
        if len(_game_state["log_lines"]) > 600:
            _game_state["log_lines"] = _game_state["log_lines"][-400:]
        root.after(0, lambda t=text, l=level: _log(t, l))
    def _log(text, level):
        log_box.config(state="normal"); log_box.insert(tk.END, text+"\n", level)
        log_box.see(tk.END); log_box.config(state="disabled")
    _ui_state["log"] = log

    console_win = ConsoleWindow(root)
    def on_console_toggle(*_):
        if console_var.get(): console_win.show()
        else: console_win.withdraw()
    console_var.trace_add("write", on_console_toggle)

    def _pipe_reader(stream, tag):
        try:
            for raw in iter(stream.readline, b""):
                line = raw.decode("utf-8", errors="replace")
                root.after(0, lambda l=line, t=tag: console_win.append(l, t))
        except: pass

    def poll():
        p = _game_state["proc"]
        if p is None: return
        if p.poll() is not None:
            _game_state["proc"] = None; _game_state["btn_mode"] = "launch"
            log("  [OK] Игра закрыта", "muted"); set_progress(0, "")
            rpc_set_idle()
            root.after(0, lambda: launch_btn.set_mode("launch"))
            root.after(0, lambda: setattr(launch_btn, "command", do_launch))
            return
        root.after(500, poll)

    def stop_game():
        p = _game_state["proc"]
        if p and p.poll() is None: p.terminate(); log("  [!!] Игра завершена принудительно", "warn")
        _game_state["proc"] = None; _game_state["btn_mode"] = "launch"
        set_progress(0, ""); launch_btn.set_mode("launch"); launch_btn.command = do_launch
        rpc_set_idle()

    if _game_state["btn_mode"] == "stop" and _game_state["proc"] and _game_state["proc"].poll() is None:
        launch_btn.set_mode("stop"); launch_btn.command = stop_game
        root.after(500, poll)

    def do_launch():
        def task():
            # Получаем все версии (встроенные + пользовательские)
            all_versions = get_all_versions()
            
            sel_ver   = version_box.get(); base_path = path_var.get()
            nickname  = nickname_var.get().strip(); memory = memory_box.get()
            show_con  = console_var.get()

            def restore():
                _game_state["btn_mode"] = "launch"
                root.after(0, lambda: launch_btn.set_mode("launch"))
                root.after(0, lambda: setattr(launch_btn, "command", do_launch))

            vinfo = all_versions.get(sel_ver)
            if not vinfo:
                root.after(0, lambda: messagebox.showwarning("Atomic Industry", f"Версия «{sel_ver}» не найдена."))
                restore(); return
            _ext = vinfo.get("loader") == "external"      # версия из другого лаунчера «как есть»
            if not nickname:
                root.after(0, lambda: messagebox.showwarning("Atomic Industry", "Введите ник!"))
                restore(); return
            if not base_path and not _ext:
                root.after(0, lambda: messagebox.showwarning("Atomic Industry", "Выберите папку установки!"))
                restore(); return

            # ── Проверка защищённого ника ────────────────────────────
            if (_is_protected_nick(nickname)
                    and config.get("account_type", "offline") == "offline"):
                pw_result = [False]
                def _pw_check():
                    pw_result[0] = _ask_nick_password(root)
                root.after(0, _pw_check)
                # Ждём завершения диалога (он modal через grab_set)
                import time
                for _ in range(300):  # до 30 сек
                    time.sleep(0.1)
                    if pw_result[0] is not False:
                        break
                # Небольшая пауза чтобы диалог закрылся
                time.sleep(0.2)
                if not pw_result[0]:
                    restore(); return

            config.update({"install_path": base_path, "selected_version": sel_ver,
                           "nickname": nickname, "memory": memory,
                           "show_console": show_con})
            save_config(config)

            if _ext:
                mc_dir = vinfo.get("external_dir", "")
                if not os.path.isdir(os.path.join(mc_dir, "versions", vinfo.get("version_id", ""))):
                    root.after(0, lambda: messagebox.showwarning(
                        "Atomic Industry", "Папка импортированной версии не найдена:\n" + mc_dir))
                    restore(); return
                log(f"  >> {mc_dir}  ({vinfo.get('source', 'другой лаунчер')})", "muted")
            else:
                if vinfo.get("game_dir"):
                    # Сборка из другого лаунчера: Minecraft и загрузчик ставим в общую
                    # папку этой версии (например «1.20.1 Forge»), а моды/миры — её.
                    _shared = f"{vinfo.get('mc_version')} {_LOADER_TITLES.get(vinfo.get('loader'), 'Vanilla')}"
                    mc_dir = get_mc_dir(base_path, _shared)
                else:
                    mc_dir = get_mc_dir(base_path, sel_ver)
                mods_dir = os.path.join(mc_dir, "mods")
                os.makedirs(mods_dir, exist_ok=True)
                log(f"  >> {mc_dir}", "muted")
            game_dir = vinfo.get("game_dir") or None     # сборка из Prism/CurseForge/...
            if game_dir:
                os.makedirs(game_dir, exist_ok=True)
                log(f"  >> папка игры: {game_dir}  ({vinfo.get('source', 'импорт')})", "muted")

            # ── Аккаунт «Сервер lenta.co»: проверяем сессию и агент ДО загрузок ──
            _use_atomic = config.get("account_type") == "atomic"
            atomic_jar = None
            if _use_atomic:
                try:
                    log("  [Auth] проверка аккаунта на сервере lenta.co...", "info")
                    if not atomic_ensure_session(config):
                        root.after(0, lambda: messagebox.showwarning(
                            "Сервер lenta.co", "Сессия истекла. Войди заново:\n"
                            "Настройки → Основные → Аккаунт → Войти."))
                        restore(); return
                    _meta = atomic_server_info(config).get("meta", {})
                    if _meta.get("atomic.gate"):
                        # Сервер в offline-mode за «входной дверью»: вход уже открыт
                        # для этого компьютера (validate выше), агент не нужен.
                        log("  [Auth] сервер с входной дверью — вход открыт для этого ПК", "muted")
                    else:
                        atomic_jar = atomic_ensure_agent(config, log_cb=log)
                    log(f"  [Auth] вход как {config['atomic_username']} — ок", "ok")
                except AtomicAuthError as e:
                    root.after(0, lambda err=str(e): messagebox.showerror("Сервер lenta.co", err))
                    restore(); return

            dl_win = {"w": None}
            _CANCEL_EVENT.clear()

            def _open_dl_win():
                sz = VERSION_SIZES.get(sel_ver, 0)
                sz_str = f"~{sz} MB" if sz else ""
                w = DownloadWindow(root, f"Minecraft {sel_ver}  {sz_str}".strip())
                dl_win["w"] = w
            root.after(0, _open_dl_win)

            def _dw(method, *args):
                if dl_win.get("w"):
                    try: root.after(0, lambda m=method, a=args: getattr(dl_win["w"], m)(*a))
                    except: pass

            def _check_cancel():
                return _CANCEL_EVENT.is_set()

            try:
                _dw("set_stage", "  [MC]  Minecraft " + vinfo.get("mc_version", "?"))
                _dw("set_total_progress", 5, "Minecraft...")
                set_progress(5, "Загрузка Minecraft...")
                log("  [MC] проверка/загрузка...", "info")

                mc_fc = [0]; mc_tc = [1]
                def mc_set_max(total):
                    _raise_if_cancelled()
                    mc_tc[0] = max(1, total)
                    _dw("set_count", 0, total)
                def mc_set_progress(current):
                    _raise_if_cancelled()
                    mc_fc[0] = current
                    pf = min(100.0, current / mc_tc[0] * 100)
                    _dw("set_file_progress", pf)
                    _dw("set_total_progress", 5 + pf*0.25, f"Minecraft  {pf:.0f}%")
                    _dw("set_count", current, mc_tc[0])
                    set_progress(5 + int(pf*0.25), f"Minecraft {current}/{mc_tc[0]}")
                def mc_set_status(text):
                    _raise_if_cancelled()
                    if text: _dw("set_file", text)
                mc_cb = {"setStatus": mc_set_status, "setProgress": mc_set_progress, "setMax": mc_set_max}
                if _ext:
                    # Версия уже установлена другим лаунчером: только докачиваем
                    # недостающие файлы. Если не вышло — запускаем как есть.
                    try:
                        minecraft_launcher_lib.install.install_minecraft_version(
                            vinfo["version_id"], mc_dir, callback=mc_cb)
                    except DownloadCancelled:
                        raise
                    except Exception as _e:
                        log(f"  [MC] проверить файлы не удалось ({_e}) — запускаю как есть", "warn")
                else:
                    try:
                        minecraft_launcher_lib.install.install_minecraft_version(
                            all_versions[sel_ver]["mc_version"], mc_dir, callback=mc_cb)
                    except TypeError:
                        minecraft_launcher_lib.install.install_minecraft_version(
                            all_versions[sel_ver]["mc_version"], mc_dir)
                _dw("set_file_progress", 100); _dw("set_total_progress", 30, "Minecraft  готов")
                set_progress(30, "Minecraft готов"); log("  [MC] готов", "ok")

                if _check_cancel():
                    log("  [!!] Загрузка отменена", "warn")
                    set_progress(0, "Отменено"); _dw("close"); restore(); return

                # ── Выбор лоадера: Vanilla, Fabric или Forge ─────────────
                loader = all_versions[sel_ver].get("loader", "forge")
                mc_version_str = all_versions[sel_ver]["mc_version"]

                if loader == "external":
                    # ── ВЕРСИЯ ИЗ ДРУГОГО ЛАУНЧЕРА ────────────────────────
                    launch_profile = vinfo["version_id"]
                    log(f"  [Импорт] {launch_profile} из «{vinfo.get('source', '?')}»", "ok")
                    set_progress(50, "Версия готова")

                elif loader == "vanilla":
                    # ── VANILLA ───────────────────────────────────────────
                    log("  [Vanilla] чистый Minecraft, лоадер не нужен", "ok")
                    set_progress(50, "Vanilla готов")
                    launch_profile = all_versions[sel_ver]["mc_version"]

                elif loader == "fabric":
                    # ── FABRIC ────────────────────────────────────────────
                    _dw("set_stage", "  [Fabric]  Установка")
                    set_progress(32, "Проверка Fabric..."); log("  [Fabric] проверка...", "info")
                    fabric_ver_str = all_versions[sel_ver].get("fabric", "0.16.14")
                    # Авто-резолв: берём последнюю версию лоадера если текущая устарела
                    fabric_ver_str = _fabric_resolve_loader_version(mc_version_str, fabric_ver_str, log_cb=log)

                    existing_profile = find_fabric_profile(mc_dir, mc_version_str)
                    need_install = True
                    if existing_profile:
                        # Проверяем версию лоадера в существующем профиле
                        # Имя папки: fabric-loader-X.Y.Z-mc_version
                        try:
                            parts = existing_profile.split("-")
                            # ищем позицию "loader" и берём следующий элемент как версию
                            li = parts.index("loader")
                            installed_ver = parts[li + 1]
                            def _ver(s):
                                try: return tuple(int(x) for x in s.split("."))
                                except: return (0,)
                            if _ver(installed_ver) >= _ver(fabric_ver_str):
                                need_install = False
                                log(f"  [Fabric] уже установлен (loader {installed_ver})", "muted")
                            else:
                                log(f"  [Fabric] устаревший loader {installed_ver} → обновляю до {fabric_ver_str}", "info")
                        except Exception:
                            need_install = False
                            log("  [Fabric] уже установлен", "muted")

                    if need_install:
                        ok = install_fabric(mc_dir, mc_version_str, fabric_ver_str, log_cb=log)
                        if not ok:
                            log("  [Fabric] Не удалось установить. Попробуй вручную.", "warn")
                    _fabric_download_loader_jar(mc_dir, mc_version_str, fabric_ver_str, log_cb=log)
                    _fabric_ensure_api(mc_dir, mc_version_str, log_cb=log)
                    set_progress(50, "Fabric готов")
                    fabric_profile = find_fabric_profile(mc_dir, mc_version_str)
                    if not fabric_profile:
                        raise RuntimeError("Fabric профиль не найден после установки")
                    log(f"  [Fabric] профиль: {fabric_profile}", "muted")
                    launch_profile = fabric_profile

                elif loader == "neoforge":
                    _dw("set_stage", "  [NeoForge]  Установка")
                    _dw("set_file_progress", 0)
                    set_progress(32, "Проверка NeoForge...")
                    log("  [NeoForge] проверка...", "info")

                    requested_neoforge = all_versions[sel_ver].get("neoforge", "")
                    try:
                        neoforge_ver = _neoforge_resolve_version(
                            mc_version_str,
                            requested_neoforge,
                            log_cb=log,
                        )
                    except RuntimeError as resolve_error:
                        neoforge_ver = requested_neoforge
                        neoforge_profile = find_neoforge_profile(
                            mc_dir,
                            mc_version_str,
                            requested_neoforge or None,
                        )
                        if not neoforge_profile:
                            raise resolve_error
                        log(
                            f"  [NeoForge] список версий недоступен; использую установленный профиль {neoforge_profile}",
                            "warn",
                        )
                    else:
                        neoforge_profile = find_neoforge_profile(
                            mc_dir,
                            mc_version_str,
                            neoforge_ver,
                        )
                    if neoforge_profile:
                        log(f"  [NeoForge] уже установлен: {neoforge_profile}", "muted")
                    else:
                        if not install_neoforge(
                            mc_dir,
                            mc_version_str,
                            neoforge_ver,
                            log_cb=log,
                        ):
                            raise RuntimeError(
                                f"Не удалось установить NeoForge {neoforge_ver} для MC {mc_version_str}"
                            )
                        neoforge_profile = find_neoforge_profile(
                            mc_dir,
                            mc_version_str,
                            neoforge_ver,
                        )
                    if not neoforge_profile:
                        raise RuntimeError("NeoForge профиль не найден после установки")

                    log(f"  [NeoForge] профиль: {neoforge_profile}", "muted")
                    launch_profile = neoforge_profile
                    _dw("set_file_progress", 100)
                    _dw("set_total_progress", 50, "NeoForge готов")
                    set_progress(50, "NeoForge готов")

                elif loader == "forge":
                    # ── FORGE ─────────────────────────────────────────────
                    _dw("set_file_progress", 0)
                    set_progress(32, "Проверка Forge..."); log("  [Forge] проверка...", "info")
                    # forge_ver объявляем ДО if-блока чтобы было доступно везде
                    forge_ver      = all_versions[sel_ver]["forge"]
                    installer_name = f"forge-{forge_ver}-installer.jar"
                    installer_path = os.path.join(mc_dir, installer_name)
                    _forge_ver_check = forge_ver
                    if not find_forge_profile(mc_dir, _forge_ver_check):
                        ffc = [0]; ftc = [1]
                        def forge_set_max(total):
                            _raise_if_cancelled()
                            ftc[0] = max(1, total)
                            _dw("set_count", 0, total)
                        def forge_set_progress(current):
                            _raise_if_cancelled()
                            ffc[0] = current
                            pf = min(100.0, current / ftc[0] * 100)
                            _dw("set_file_progress", pf)
                            _dw("set_total_progress", 30 + pf*0.2, f"Forge  {pf:.0f}%")
                            _dw("set_count", current, ftc[0])
                            set_progress(30 + int(pf*0.2), f"Forge {current}/{ftc[0]}")
                        forge_cb = {"setStatus": lambda t: (_raise_if_cancelled(), _dw("set_file", t) if t else None),
                                    "setProgress": forge_set_progress, "setMax": forge_set_max}
    
                        forge_ok = False
    
                        if not forge_ok:
                            log("  [Forge] попытка через minecraft-launcher-lib...", "info")
                            try:
                                try:
                                    minecraft_launcher_lib.forge.install_forge_version(
                                        all_versions[sel_ver]["forge"], mc_dir, callback=forge_cb)
                                except TypeError:
                                    minecraft_launcher_lib.forge.install_forge_version(
                                        all_versions[sel_ver]["forge"], mc_dir)
                                if find_forge_profile(mc_dir, forge_ver):
                                    forge_ok = True
                                    log("  [Forge] установлен через lib", "ok")
                            except Exception as e:
                                log(f"  [Forge] lib не сработал: {e}", "warn")
    
                        if not forge_ok:
                            log("  [Forge] пробуем зеркала...", "warn")
                            mc_ver = all_versions[sel_ver]["mc_version"]
                            mirrors = [
                                f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forge_ver}/{installer_name}",
                                f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{forge_ver}/{installer_name}",
                                f"https://mc.borecraft.ru/forge/{installer_name}",
                                f"https://download.mc-launcher.com/forge/{forge_ver}/{installer_name}",
                            ]
                            downloaded = False
                            for mirror_url in mirrors:
                                if downloaded: break
                                try:
                                    log(f"  [Forge] зеркало: {mirror_url.split('/')[2]}", "info")
                                    _dw("set_file", f"Загрузка installer с {mirror_url.split('/')[2]}...")
                                    import urllib.request, ssl
                                    ctx = ssl.create_default_context()
                                    req = urllib.request.Request(mirror_url, headers={"User-Agent": "Mozilla/5.0"})
                                    chunk_size = 65536; downloaded_bytes = [0]
                                    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                                        total_size = int(resp.headers.get("Content-Length", 0))
                                        with open(installer_path, "wb") as fh:
                                            while True:
                                                chunk = resp.read(chunk_size)
                                                if not chunk: break
                                                fh.write(chunk); downloaded_bytes[0] += len(chunk)
                                                if total_size > 0:
                                                    pct = downloaded_bytes[0] / total_size * 100
                                                    _dw("set_file_progress", pct)
                                                    _dw("set_total_progress", 30 + pct*0.1, f"Forge installer  {pct:.0f}%")
                                    downloaded = True
                                    log(f"  [Forge] installer скачан ({downloaded_bytes[0]//1024} KB)", "ok")
                                except Exception as e:
                                    log(f"  [Forge] зеркало недоступно: {e}", "warn")
                                    if os.path.exists(installer_path):
                                        try: os.remove(installer_path)
                                        except: pass
    
                            if downloaded and os.path.exists(installer_path):
                                _ensure_launcher_profiles(mc_dir)
                                log("  [Forge] запуск installer...", "info")
                                _dw("set_file", "Запуск Forge installer...")
                                _dw("set_total_progress", 42, "Forge installer...")
                                java_exe = patch_command_java(["java"])[0]
                                _proxy_args = _get_proxy_jvm_args()
                                install_variants = [
                                    [java_exe] + _proxy_args + ["-jar", installer_path, "--installClient", mc_dir],
                                    [java_exe] + _proxy_args + ["-jar", installer_path, "--installClient"],
                                    [java_exe, "-Djava.awt.headless=true"] + _proxy_args + ["-jar", installer_path, "--installClient", mc_dir],
                                ]
                                try:
                                    for variant_cmd in install_variants:
                                        if forge_ok: break
                                        use_cwd = mc_dir if variant_cmd[-1] == "--installClient" else None
                                        proc = _run_cancellable(variant_cmd, timeout=300, cwd=use_cwd)
                                        if proc.returncode == 0 and find_forge_profile(mc_dir, forge_ver):
                                            forge_ok = True
                                            log("  [Forge] installer успешно завершён", "ok")
                                        elif proc.stderr:
                                            for line in proc.stderr.strip().split("\n")[-4:]:
                                                if line.strip(): log(f"    stderr: {line.strip()}", "warn")
                                except subprocess.TimeoutExpired:
                                    log("  [Forge] installer завис (таймаут 5 мин)", "warn")
                                except Exception as e:
                                    log(f"  [Forge] ошибка запуска installer: {e}", "warn")
                                finally:
                                    try: os.remove(installer_path)
                                    except: pass
                            elif not downloaded:
                                log("  [Forge] все зеркала недоступны — установи VPN или скачай вручную", "warn")
    
                        if not forge_ok:
                            log("  [!!] Forge не установлен. Попробуй VPN или добавь installer вручную.", "warn")
                        else:
                            log("  [Forge] готов", "ok")
                    else:
                        log("  [Forge] уже установлен", "muted")
                    _dw("set_file_progress", 100); _dw("set_total_progress", 50, "Forge  готов")
                    set_progress(50, "Forge готов")
                    forge_profile = find_forge_profile(mc_dir, forge_ver)
                    if not forge_profile:
                        raise RuntimeError("Forge профиль не найден после установки")
                    launch_profile = forge_profile

                else:
                    raise RuntimeError(f"Неизвестный загрузчик: {loader}")

                if _check_cancel():
                    log("  [!!] Загрузка отменена", "warn")
                    set_progress(0, "Отменено"); _dw("close"); restore(); return

                _dw("close")

                # ── Скины (мод CustomSkinLoader) ─────────────────────────
                # Сервер lenta.co работает в offline-mode через «входную дверь»,
                # поэтому скины игроков подгружает CSL: с сервера lenta.co, Ely.by,
                # TLauncher, LittleSkin и Mojang. Для лицензии мод не нужен.
                _skin_mode = config.get("account_type", "offline")
                if _skin_mode not in ("atomic", "microsoft"):
                    _skin_mode = "offline"
                _skin_dir = game_dir or mc_dir
                if loader in ("fabric", "forge", "neoforge"):
                    set_progress(93, "Скины...")
                    if _skin_mode != "microsoft":
                        _csl_ensure(_skin_dir, mc_version_str, loader, log_cb=log)
                    _csl_configure(_skin_dir, config, _skin_mode, log_cb=log)
                elif loader == "external":
                    # В чужую папку мод сами не ставим; если CSL там уже есть — настроим.
                    try:
                        _has_csl = any("customskinloader" in f.lower()
                                       for f in os.listdir(os.path.join(_skin_dir, "mods")))
                    except OSError:
                        _has_csl = False
                    if _has_csl:
                        _csl_configure(_skin_dir, config, _skin_mode, log_cb=log)

                set_progress(95, "Запуск...")

                options = {"username": nickname, "uuid": generate_uuid(nickname), "token": "0",
                           "userType": "legacy",
                           "jvmArguments": [
                               f"-Xmx{memory}G", f"-Xms{memory}G",
                               "-Dminecraft.api.auth.host=http://localhost",
                               "-Dminecraft.api.account.host=http://localhost",
                               "-Dminecraft.api.session.host=http://localhost",
                               "-Dminecraft.api.services.host=http://localhost",
                               "-Dminecraft.sessionserver=http://localhost",
                           ]}
                if game_dir:
                    options["gameDirectory"] = game_dir

                # ── Microsoft: освежаем токен перед запуском ────────────
                if config.get("account_type") == "microsoft" and config.get("ms_refresh_token"):
                    try:
                        set_progress(94, "Обновляю вход Microsoft...")
                        if ms_refresh_session(config):
                            save_config(config)
                            log("  [MS] Токен обновлён", "ok")
                    except Exception as _e:
                        log(f"  [MS] Не удалось обновить токен ({_e}) — войди заново: Аккаунт → Microsoft", "warn")

                # ── Microsoft аккаунт: используем реальный токен ────────
                _use_ms = (config.get("account_type") == "microsoft"
                           and config.get("ms_access_token")
                           and config.get("ms_uuid"))
                if _use_ms:
                    ms_nick = config.get("ms_username") or nickname
                    ms_uuid = config["ms_uuid"]
                    ms_tok  = config["ms_access_token"]
                    log(f"  [MS] Вход как {ms_nick} (лицензия)", "ok")
                    options["username"] = ms_nick
                    options["uuid"]     = ms_uuid
                    options["token"]    = ms_tok
                    options["userType"] = "msa"
                    # JVM аргументы: убираем localhost-заглушки для реального входа
                    options["jvmArguments"] = [
                        f"-Xmx{memory}G", f"-Xms{memory}G",
                    ]

                # ── Сервер lenta.co: authlib-injector + токен с сервера ─────
                if _use_atomic:
                    options["username"] = config["atomic_username"]
                    options["uuid"]     = config["atomic_uuid"]
                    options["token"]    = config["atomic_access_token"]
                    options["userType"] = "mojang"
                    options["jvmArguments"] = [f"-Xmx{memory}G", f"-Xms{memory}G"] + \
                        (atomic_jvm_args(config, atomic_jar) if atomic_jar else [])

                cmd = minecraft_launcher_lib.command.get_minecraft_command(launch_profile, mc_dir, options)
                cmd = patch_command_java(cmd)
                if loader == "neoforge":
                    cmd = _neoforge_add_client_extra_to_command(
                        cmd,
                        mc_dir,
                        launch_profile,
                        mc_version_str,
                        log_cb=log,
                    )

                if _use_atomic:
                    _vals = {"--accessToken": options["token"], "--uuid": options["uuid"],
                             "--username": options["username"], "--userType": "mojang"}
                    cmd = [(_vals[cmd[i - 1]] if i > 0 and cmd[i - 1] in _vals else a)
                           for i, a in enumerate(cmd)]
                elif _use_ms:
                    # Microsoft режим: патчим только токен/uuid/userType (реальные данные),
                    # НЕ вызываем patch_command_offline чтобы не затереть токен нулями.
                    result2 = list(cmd)
                    i2 = 0
                    while i2 < len(result2):
                        if result2[i2] == "--accessToken" and i2 + 1 < len(result2):
                            result2[i2 + 1] = ms_tok
                        elif result2[i2] == "--uuid" and i2 + 1 < len(result2):
                            result2[i2 + 1] = ms_uuid
                        elif result2[i2] == "--username" and i2 + 1 < len(result2):
                            result2[i2 + 1] = ms_nick
                        elif result2[i2] == "--userType" and i2 + 1 < len(result2):
                            result2[i2 + 1] = "msa"
                        i2 += 1
                    cmd = result2
                else:
                    cmd = patch_command_offline(cmd, nickname)

                # Фильтруем JVM аргументы несовместимые с Java 8
                # (minecraft_launcher_lib может добавлять Java 9+ флаги)
                # ВАЖНО: --add-opens и модульные флаги нужны для Forge на MC 1.17+
                # (Java 11/17). Удалять их можно только для MC <= 1.16 (Java 8).
                def _mc_minor(ver_str):
                    """Возвращает второй компонент версии MC, напр. '20' для '1.20.1'."""
                    try:
                        parts = ver_str.split(".")
                        return int(parts[1]) if len(parts) >= 2 else 0
                    except (ValueError, IndexError):
                        return 0

                _needs_java8_filter = _mc_minor(mc_version_str) <= 16

                if _needs_java8_filter:
                    _JAVA8_UNSUPPORTED_FLAGS = {
                        "-p", "--module-path",
                        "--add-modules", "--add-opens", "--add-exports", "--add-reads",
                        "--patch-module", "--illegal-access",
                    }
                    _cmd_clean = []
                    _skip_next = False
                    for _arg in cmd:
                        if _skip_next:
                            _skip_next = False
                            continue
                        # Флаги вида --add-modules=... (со значением через =)
                        _flag_base = _arg.split("=")[0] if "=" in _arg else _arg
                        if _flag_base in _JAVA8_UNSUPPORTED_FLAGS:
                            # Флаги без = принимают значение следующим аргументом
                            if "=" not in _arg:
                                _skip_next = True
                            log(f"  [JVM] убран несовместимый флаг (Java 8 режим): {_arg[:60]}", "muted")
                            continue
                        _cmd_clean.append(_arg)
                    cmd = _cmd_clean
                else:
                    log(f"  [JVM] MC {mc_version_str} — Java 9+ флаги сохранены (нужны для Forge/Fabric/NeoForge)", "muted")

                if loader == "fabric":
                    _mc_jar     = os.path.join(mc_dir, "versions", mc_version_str, mc_version_str + ".jar")
                    _mc_natives = os.path.join(mc_dir, "versions", mc_version_str, "natives")
                    os.makedirs(_mc_natives, exist_ok=True)

                    # Исправляем natives пути
                    _bad_natives = os.path.join(mc_dir, "versions", fabric_profile, "natives")
                    cmd = [a.replace(_bad_natives, _mc_natives) if _bad_natives in a else a for a in cmd]

                    # Добавляем MC jar в classpath — ищем по имени файла без учёта слешей
                    _mc_jar_name = mc_version_str + ".jar"

                    # Проверка: JAR должен существовать на диске
                    if not os.path.exists(_mc_jar) or os.path.getsize(_mc_jar) < 100000:
                        log(f"  [Fabric] ОШИБКА: {_mc_jar_name} не найден или повреждён!", "warn")
                        log(f"  [Fabric] Путь: {_mc_jar}", "warn")
                        raise RuntimeError(f"Minecraft {mc_version_str}.jar не найден: {_mc_jar}")

                    for _i, _a in enumerate(cmd):
                        if _a == "-cp" and _i + 1 < len(cmd):
                            _cp_entries = cmd[_i + 1].split(os.pathsep)

                            # Дедупликация по имени файла
                            _seen_names = {}
                            _cp_dedup = []
                            for _e in _cp_entries:
                                _ename = _e.replace("\\", "/").split("/")[-1]
                                if _ename not in _seen_names:
                                    _seen_names[_ename] = True
                                    _cp_dedup.append(_e)
                                else:
                                    log(f"  [Fabric] убран дубль из classpath: {_ename}", "muted")

                            # Убираем fabric-loader-X.X.X.jar из libraries —
                            # он не должен быть в classpath, Fabric грузит его сам.
                            # Оставляем только fabric-loader-X.X.X-mcver.jar из versions/.
                            _cp_dedup = [
                                _e for _e in _cp_dedup
                                if not (
                                    "fabric-loader" in _e.replace("\\", "/").split("/")[-1]
                                    and "libraries" in _e.replace("\\", "/")
                                )
                            ]

                            # Добавляем MC jar если его ещё нет
                            _already = any(e.replace("\\", "/").split("/")[-1] == _mc_jar_name for e in _cp_dedup)
                            if not _already:
                                _cp_dedup.append(_mc_jar)
                                log(f"  [Fabric] добавлен {_mc_jar_name} в classpath", "muted")
                            else:
                                log(f"  [Fabric] {_mc_jar_name} уже в classpath", "muted")

                            cmd[_i + 1] = os.pathsep.join(_cp_dedup)
                            break

                    # Сохраняем команду для диагностики
                    try:
                        with open(os.path.join(mc_dir, "last_launch_cmd.txt"), "w", encoding="utf-8") as _f:
                            _f.write("\n".join(cmd))
                    except Exception:
                        pass

                log(f"  [Java] {cmd[0]}", "muted")
                if is_dev_mode():
                    _safe_cmd = _dev_redact_cmd(cmd)
                    try:
                        with open(os.path.join(BASE_DIR, "last_launch_cmd.txt"), "w", encoding="utf-8") as _f:
                            _f.write("\n".join(_safe_cmd))
                    except Exception:
                        pass
                    log("  [DEV] команда запуска (токен скрыт):", "muted")
                    _short = [("<classpath: %d файлов>" % (len(a.split(os.pathsep))) if i > 0 and _safe_cmd[i - 1] in ("-cp", "-classpath") else a)
                              for i, a in enumerate(_safe_cmd)]
                    log("    " + " ".join(_short)[:2400], "muted")

                kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
                if sys.platform.startswith("win"):
                    kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

                proc = None; last_err = None
                for attempt in range(1, 4):
                    try:
                        if attempt > 1:
                            log(f"  [!!] Попытка запуска #{attempt}...", "warn")
                            import time; time.sleep(1)
                        proc = subprocess.Popen(cmd, **kwargs)
                        import time; time.sleep(1.2)
                        if proc.poll() is not None:
                            try: err_out = proc.stderr.read().decode("utf-8", errors="replace")
                            except: err_out = ""
                            last_err = f"Процесс завершился сразу (код {proc.returncode})\n{err_out}"
                            log(f"  [!!] Старт неудачен (попытка {attempt}): код {proc.returncode}", "warn")
                            proc = None; continue
                        break
                    except Exception as e:
                        last_err = str(e)
                        log(f"  [!!] Ошибка запуска (попытка {attempt}): {e}", "warn")
                        proc = None

                if proc is None:
                    raise RuntimeError(f"Не удалось запустить Minecraft после 3 попыток.\n\n{last_err}")

                _game_state["proc"] = proc; _game_state["btn_mode"] = "stop"
                threading.Thread(target=_pipe_reader, args=(proc.stdout,"out"), daemon=True).start()
                threading.Thread(target=_pipe_reader, args=(proc.stderr,"err"), daemon=True).start()
                if show_con: root.after(0, console_win.show)

                set_progress(100, "Игра запущена!")
                log("  [OK] Minecraft запущен!", "ok")
                rpc_set_playing(sel_ver, nickname)
                root.after(0, lambda: launch_btn.set_mode("stop"))
                root.after(0, lambda: setattr(launch_btn, "command", stop_game))
                root.after(500, poll)

            except DownloadCancelled:
                log("  [!!] Загрузка отменена", "warn")
                set_progress(0, "Отменено")
                _dw("close")
                restore()
            except Exception as e:
                err_text = traceback.format_exc(); crash_path = write_crash_report(err_text)
                log(f"  [ERROR] {e}", "error"); log(f"  Краш-репорт: {crash_path}", "warn")
                set_progress(0, "ОШИБКА — открыт краш-репорт")
                root.after(0, lambda cp=crash_path, et=err_text: show_crash_window(root, cp, et))
                restore()

        _game_state["btn_mode"] = "loading"
        launch_btn.set_mode("loading"); set_progress(0, "Подготовка...")
        threading.Thread(target=task, daemon=True).start()

    if _game_state["btn_mode"] != "stop":
        launch_btn.command = do_launch

    def open_settings():
        def on_settings_save():
            apply_theme(config.get("theme", "night"), config.get("custom_theme") or {})
            build_ui(root, config, max_ram)
        show_settings_window(root, config, on_save=on_settings_save)


# ══════════════════════════════════════════
#  АВТООБНОВЛЕНИЕ через сервер lenta.co
#
#  Сервер только раздаёт файлы (data/updates/ → /atomic/update/...).
#  Манифест подписан ключом разработчика (Ed25519, release_tool.py), а
#  публичный ключ вшит сюда — даже взломанный сервер не подсунет вирус:
#  без правильной подписи лаунчер ничего не установит.
#  Откатить на старую версию тоже нельзя — ставится только версия новее.
# ══════════════════════════════════════════

# Публичный ключ релизов. Заполняется командой:  python release_tool.py keygen
UPDATE_PUBLIC_KEY = "IZg2mn4KZIajF1z1Ya65vWEvXZLEEzNJHbpZcIu4Usk="


class UpdateError(Exception):
    pass


def _version_tuple(v: str):
    return tuple(int(x) for x in re.findall(r"\d+", str(v))[:4]) or (0,)


def _update_platform_key() -> str:
    if not getattr(sys, "frozen", False):
        return "source"
    return {"windows": "windows", "mac": "mac"}.get(_PLATFORM_KEY, "linux")


def _update_canonical(manifest: dict) -> bytes:
    body = {k: v for k, v in manifest.items() if k != "signature"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _update_verify(manifest: dict):
    if not UPDATE_PUBLIC_KEY:
        raise UpdateError("В этой сборке не задан ключ обновлений (release_tool.py keygen)")
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
    except ImportError:
        raise UpdateError("Для проверки обновлений нужен пакет cryptography (pip install cryptography)")
    try:
        key = Ed25519PublicKey.from_public_bytes(_b64.b64decode(UPDATE_PUBLIC_KEY))
        key.verify(_b64.b64decode(manifest.get("signature", "")), _update_canonical(manifest))
    except (InvalidSignature, ValueError, TypeError):
        raise UpdateError("Подпись обновления неверная — установка отменена (возможна подмена!)")


def update_fetch_manifest(config) -> dict:
    """Возвращает проверенный манифест, если есть версия новее, иначе None."""
    try:
        st, body = _http(_atomic_url(config) + "/atomic/update/manifest.json", timeout=10, max_bytes=200_000)
    except (_urlerr.URLError, OSError) as e:
        raise UpdateError(f"Сервер обновлений недоступен (ZeroTier подключён?)\n{e}")
    if st == 404:
        return None
    if st != 200:
        raise UpdateError(f"Сервер обновлений ответил кодом {st}")
    try:
        manifest = json.loads(body)
    except ValueError:
        raise UpdateError("Повреждённый манифест обновления")
    _update_verify(manifest)
    if _version_tuple(manifest.get("version", "0")) <= _version_tuple(LAUNCHER_VERSION):
        return None
    if _update_platform_key() not in (manifest.get("files") or {}):
        raise UpdateError(f"В обновлении {manifest.get('version')} нет файла для этой системы "
                          f"({_update_platform_key()})")
    return manifest


def update_download(config, manifest, progress_cb=None) -> str:
    """Скачивает файл рядом с лаунчером, проверяет SHA-256 и размер. Возвращает путь."""
    info = manifest["files"][_update_platform_key()]
    name = str(info["name"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", name):
        raise UpdateError("Некорректное имя файла в обновлении")
    url = _atomic_url(config) + "/atomic/update/files/" + name
    size = int(info["size"])
    target = _update_target()
    tmp = target + ".download"
    h = _hashlib.sha256()
    got = 0
    req = _urlreq.Request(url, headers=dict(_UA))
    try:
        with _urlreq.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(256 * 1024)
                if not chunk:
                    break
                got += len(chunk)
                if got > size:
                    raise UpdateError("Файл обновления больше заявленного")
                h.update(chunk)
                f.write(chunk)
                if progress_cb and size:
                    progress_cb(got * 100 // size)
    except (_urlerr.URLError, OSError) as e:
        _silent_remove(tmp)
        raise UpdateError(f"Не удалось скачать обновление: {e}")
    except UpdateError:
        _silent_remove(tmp)
        raise
    if got != size or h.hexdigest() != info["sha256"]:
        _silent_remove(tmp)
        raise UpdateError("Контрольная сумма не совпала — файл повреждён или подменён")
    return tmp


def _silent_remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


def _update_target() -> str:
    return sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)


def update_install_and_restart(tmp: str, root=None):
    """Подменяет файл лаунчера и перезапускает его. Windows .exe заблокирован,
    пока работает, поэтому там замену делает маленький .bat после выхода."""
    target = _update_target()
    frozen = getattr(sys, "frozen", False)
    if frozen and sys.platform.startswith("win"):
        bat = os.path.join(os.path.dirname(target), "_atomic_update.bat")
        with open(bat, "w", encoding="utf-8") as f:
            f.write("@echo off\r\nchcp 65001 >nul\r\n"
                    ":wait\r\n"
                    f'tasklist /FI "PID eq {os.getpid()}" 2>nul | find "{os.getpid()}" >nul\r\n'
                    "if not errorlevel 1 ( ping -n 2 127.0.0.1 >nul & goto wait )\r\n"
                    f'move /Y "{tmp}" "{target}" >nul\r\n'
                    f'start "" "{target}"\r\n'
                    '(goto) 2>nul & del "%~f0"\r\n')
        subprocess.Popen(["cmd", "/c", bat], close_fds=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if root is not None:
            root.destroy()
        os._exit(0)
    os.replace(tmp, target)
    if frozen:
        os.chmod(target, 0o755)
        args = [target] + sys.argv[1:]
    else:
        args = [sys.executable, target] + sys.argv[1:]
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass
    if sys.platform.startswith("win"):
        subprocess.Popen(args, close_fds=True)
        os._exit(0)
    os.execv(args[0], args)


def check_for_updates(root, config, silent: bool = False):
    """silent=True — при запуске: молчит, если обновлений нет или сервер недоступен."""
    def work():
        try:
            manifest = update_fetch_manifest(config)
            root.after(0, lambda: _on_update_found(root, config, manifest, silent))
        except UpdateError as e:
            if not silent:
                root.after(0, lambda err=str(e): messagebox.showerror("Обновление", err, parent=root))
    threading.Thread(target=work, daemon=True).start()


def _on_update_found(root, config, manifest, silent):
    if manifest is None:
        if not silent:
            messagebox.showinfo("Обновление", f"У тебя последняя версия  v{LAUNCHER_VERSION}  ✓", parent=root)
        return
    changelog = str(manifest.get("changelog", "")).strip()
    msg = (f"Доступна новая версия лаунчера!\n\n"
           f"  Сейчас:  v{LAUNCHER_VERSION}\n  Новая:   v{manifest['version']}\n"
           + (f"\nЧто нового:\n{changelog[:1500]}\n" if changelog else "")
           + "\n✓ Подпись разработчика проверена.\n\nУстановить сейчас? Лаунчер перезапустится.")
    if not messagebox.askyesno("Обновление лаунчера", msg, parent=root):
        return
    if _game_state.get("proc") is not None and _game_state["proc"].poll() is None:
        messagebox.showwarning("Обновление", "Сначала закрой игру — потом обнови лаунчер.", parent=root)
        return

    win = tk.Toplevel(root)
    win.title("Обновление")
    win.geometry("420x130")
    win.resizable(False, False)
    win.configure(bg=C["bg"])
    win.transient(root)
    win.protocol("WM_DELETE_WINDOW", lambda: None)
    tk.Frame(win, height=2, bg=C["orange"]).pack(fill="x")
    tk.Label(win, text=f"  ⬇  v{LAUNCHER_VERSION} → v{manifest['version']}", bg=C["bg"],
             fg=C["orange"], font=_font(10, "bold"), pady=8).pack(anchor="w")
    pb = ttk.Progressbar(win, style="AI.Horizontal.TProgressbar", mode="determinate", maximum=100)
    pb.pack(fill="x", padx=16)
    status = tk.Label(win, text="Скачиваю...", bg=C["bg"], fg=C["text_muted"], font=FS)
    status.pack(anchor="w", padx=16, pady=(6, 0))

    def work():
        try:
            tmp = update_download(config, manifest,
                                  progress_cb=lambda p: win.after(0, lambda: pb.configure(value=p)))
        except UpdateError as e:
            def fail(err=str(e)):
                win.destroy()
                messagebox.showerror("Обновление", err, parent=root)
            win.after(0, fail)
            return
        def done():
            status.config(text="✓ Проверено. Перезапускаю...", fg=C["green"])
            root.after(800, lambda: update_install_and_restart(tmp, root))
        win.after(0, done)

    threading.Thread(target=work, daemon=True).start()


# ══════════════════════════════════════════
#  РЕЖИМ РАЗРАБОТЧИКА
#  Включается файлом dev.key рядом с лаунчером (или ~/.atomic_dev.key).
#  Файл создаёт release_tool.py devkey <имя> и подписывает тем же ключом,
#  что и обновления, — подделать без секретного ключа нельзя.
#  Что даёт: все секретные темы, вкладка «🧪 Разработчик» в настройках
#  (диагностика системы, проверка сервера, команда запуска), подробный лог
#  с полной командой запуска Java. Серверные проверки (пароль, вайтлист,
#  гейт) dev-режим НЕ обходит — это только инструменты на своём компьютере.
# ══════════════════════════════════════════

_DEV = {"active": False, "name": "", "error": ""}


def _dev_key_paths():
    return [os.path.join(BASE_DIR, "dev.key"), os.path.join(os.path.expanduser("~"), ".atomic_dev.key")]


def load_dev_mode():
    _DEV.update(active=False, name="", error="")
    for path in _dev_key_paths():
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("type") != "atomic-dev":
                raise UpdateError("это не ключ разработчика")
            try:
                _update_verify(data)
            except UpdateError:
                raise UpdateError("подпись не сходится (ключ подделан или от другой сборки)")
            exp = data.get("expires")
            if exp and time.time() > float(exp):
                raise UpdateError("срок ключа истёк")
            _DEV.update(active=True, name=str(data.get("name", "dev"))[:32])
            _unlocked_themes.update(SECRET_THEMES)
            return True
        except (UpdateError, ValueError, OSError) as e:
            _DEV["error"] = f"{os.path.basename(path)}: {e}"
    return False


def _dev_redact_cmd(cmd):
    """Копия команды запуска без токена — её можно спокойно кидать в чат."""
    out = list(cmd)
    for i in range(1, len(out)):
        if out[i - 1] == "--accessToken":
            out[i] = "***"
    return out


def is_dev_mode() -> bool:
    return _DEV["active"]


def _dev_system_info(root=None) -> str:
    env = os.environ
    desktop = env.get("XDG_CURRENT_DESKTOP") or env.get("DESKTOP_SESSION") or "-"
    if env.get("HYPRLAND_INSTANCE_SIGNATURE"):
        desktop += " (Hyprland)"
    session = "Wayland" if env.get("WAYLAND_DISPLAY") else ("X11" if env.get("DISPLAY") else "-")
    lines = [
        f"Лаунчер:   v{LAUNCHER_VERSION}  ({'exe' if getattr(sys, 'frozen', False) else 'исходники'})",
        f"Python:    {sys.version.split()[0]}  ·  Tk {tk.TkVersion}",
        f"Система:   {platform.system()} {platform.release()}  ·  {platform.machine()}",
        f"Рабочий стол: {desktop}  ·  сеанс: {session}",
        f"Шрифты:    UI «{_UI_FAMILY}», моно «{_MONO_FAMILY}»",
        f"Тема:      {C.get('name', '?')}",
        f"Папка:     {BASE_DIR}",
        f"Конфиг:    {CONFIG_FILE}",
    ]
    if root is not None:
        try:
            lines.append(f"Экран:     {root.winfo_screenwidth()}×{root.winfo_screenheight()}  ·  "
                         f"окно {root.winfo_width()}×{root.winfo_height()}  ·  "
                         f"масштаб Tk {root.tk.call('tk', 'scaling'):.2f}")
        except Exception:
            pass
    java = find_java_windows() if sys.platform.startswith("win") else find_java_linux()
    lines.append(f"Java:      {java or 'не найдена'}")
    return "\n".join(lines)


def _build_dev_tab(body, win, config):
    tk.Label(body, text=f"🧪  Режим разработчика — {_DEV['name']}", bg=C["bg"], fg=C["accent"],
             font=_font(12, "bold")).pack(anchor="w", pady=(4, 2))
    tk.Label(body, text="Все секретные темы открыты, лог подробный, команда запуска сохраняется.",
             bg=C["bg"], fg=C["text_muted"], font=FS).pack(anchor="w", pady=(0, 10))

    info = tk.Text(body, height=12, bg=C["log_bg"], fg=C["text"], font=FLG, bd=0, wrap="word",
                   highlightthickness=1, highlightbackground=C["border"], padx=10, pady=8)
    info.pack(fill="x")

    def refresh_info(extra=""):
        info.config(state="normal")
        info.delete("1.0", tk.END)
        info.insert(tk.END, _dev_system_info(win.master if win.master is not None else win) + (("\n\n" + extra) if extra else ""))
        info.config(state="disabled")
    refresh_info()

    def java_version():
        java = find_java_windows() if sys.platform.startswith("win") else find_java_linux()
        if not java:
            return win.after(0, lambda: refresh_info("java -version: Java не найдена"))
        try:
            r = subprocess.run([java, "-version"], capture_output=True, text=True, timeout=15)
            out = (r.stderr or r.stdout).strip()
        except Exception as e:
            out = str(e)
        win.after(0, lambda: refresh_info("java -version:\n" + out))

    def check_server():
        url = _atomic_url(config)
        t0 = time.time()
        try:
            meta = atomic_server_info(config)
            ms = (time.time() - t0) * 1000
            m = meta.get("meta", {})
            txt = (f"Сервер {url}: OK за {ms:.0f} мс\n  имя: {m.get('serverName')}  ·  версия "
                   f"{m.get('implementationVersion')}\n  регистрация: {m.get('atomic.registration')}  ·  "
                   f"входная дверь: {'вкл' if m.get('atomic.gate') else 'выкл'}")
            st, _ = _http(url + "/atomic/update/manifest.json", timeout=8)
            txt += f"\n  обновления: {'есть манифест' if st == 200 else 'нет (' + str(st) + ')'}"
        except Exception as e:
            txt = f"Сервер {url}: ОШИБКА\n  {e}"
        win.after(0, lambda: refresh_info(txt))

    def open_path(path):
        if os.path.exists(path):
            open_file(path)
        else:
            messagebox.showinfo("Разработчик", f"Файла пока нет:\n{path}", parent=win)

    def reset_agent():
        try:
            os.remove(_AUTHLIB_JAR)
            refresh_info("authlib-injector удалён — скачается заново при запуске")
        except OSError:
            refresh_info("authlib-injector и так не скачан")

    def copy_info():
        win.clipboard_clear()
        win.clipboard_append(info.get("1.0", tk.END).strip())
        refresh_info("✓ Диагностика скопирована в буфер обмена")

    rows = [
        [("📁 Папка лаунчера", lambda: open_file(BASE_DIR)),
         ("⚙ Конфиг", lambda: open_path(CONFIG_FILE)),
         ("💥 Краш-репорты", lambda: open_file(CRASH_DIR))],
        [("▶ Последняя команда запуска", lambda: open_path(os.path.join(BASE_DIR, "last_launch_cmd.txt"))),
         ("☕ java -version", lambda: threading.Thread(target=java_version, daemon=True).start())],
        [("🌐 Проверить сервер", lambda: threading.Thread(target=check_server, daemon=True).start()),
         ("⬆ Проверить обновления", lambda: check_for_updates(win, config, silent=False)),
         ("♻ Сбросить authlib-injector", reset_agent)],
        [("📋 Скопировать диагностику", copy_info)],
    ]
    for row in rows:
        fr = tk.Frame(body, bg=C["bg"])
        fr.pack(anchor="w", pady=(8, 0))
        for text, cmd in row:
            FlatButton(fr, text, command=cmd, bg=C["bg"], font=_font(9, "bold")).pack(side="left", padx=(0, 8))


# ══════════════════════════════════════════
#  ВЕРСИИ ИЗ ДРУГИХ ЛАУНЧЕРОВ
#  1) Папки .minecraft (официальный лаунчер, TLauncher, SKLauncher...):
#     версия запускается прямо из их папки как есть.
#  2) Сборки Prism / MultiMC / PolyMC, CurseForge, ATLauncher, Modrinth App:
#     читаем версию Minecraft и загрузчика, ставим загрузчик у себя, а играем
#     в папке сборки — моды, миры и настройки остаются их.
# ══════════════════════════════════════════

def _other_launcher_locations():
    home = os.path.expanduser("~")
    if sys.platform.startswith("win"):
        ad = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
        return {
            "mc": [("Официальный / TLauncher", os.path.join(ad, ".minecraft")),
                   ("TLauncher Legacy", os.path.join(ad, ".tlauncher", "legacy", "Minecraft", "game"))],
            "prism": [("Prism", os.path.join(ad, "PrismLauncher", "instances")),
                      ("PolyMC", os.path.join(ad, "PolyMC", "instances"))],
            "curseforge": [("CurseForge", os.path.join(home, "curseforge", "minecraft", "Instances"))],
            "atlauncher": [("ATLauncher", os.path.join(ad, "ATLauncher", "instances"))],
            "modrinth": [("Modrinth", os.path.join(ad, "ModrinthApp", "profiles")),
                         ("Modrinth", os.path.join(ad, "com.modrinth.theseus", "profiles"))],
        }
    if sys.platform == "darwin":
        sup = os.path.join(home, "Library", "Application Support")
        return {
            "mc": [("Официальный / TLauncher", os.path.join(sup, "minecraft"))],
            "prism": [("Prism", os.path.join(sup, "PrismLauncher", "instances"))],
            "curseforge": [("CurseForge", os.path.join(home, "Documents", "curseforge", "minecraft", "Instances"))],
            "atlauncher": [("ATLauncher", os.path.join(sup, "ATLauncher", "instances"))],
            "modrinth": [("Modrinth", os.path.join(sup, "ModrinthApp", "profiles"))],
        }
    share = os.environ.get("XDG_DATA_HOME", os.path.join(home, ".local", "share"))
    return {
        "mc": [("Официальный / TLauncher", os.path.join(home, ".minecraft")),
               ("TLauncher Legacy", os.path.join(home, ".tlauncher", "legacy", "Minecraft", "game"))],
        "prism": [("Prism", os.path.join(share, "PrismLauncher", "instances")),
                  ("Prism (Flatpak)", os.path.join(home, ".var", "app", "org.prismlauncher.PrismLauncher",
                                                   "data", "PrismLauncher", "instances")),
                  ("PolyMC", os.path.join(share, "PolyMC", "instances")),
                  ("MultiMC", os.path.join(share, "multimc", "instances"))],
        "curseforge": [],
        "atlauncher": [("ATLauncher", os.path.join(share, "ATLauncher", "instances")),
                       ("ATLauncher", os.path.join(home, ".atlauncher", "instances"))],
        "modrinth": [("Modrinth", os.path.join(share, "ModrinthApp", "profiles")),
                     ("Modrinth", os.path.join(share, "com.modrinth.theseus", "profiles"))],
    }


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _loader_of_version_id(vid: str) -> str:
    v = vid.lower()
    for key, name in (("neoforge", "NeoForge"), ("forge", "Forge"), ("fabric", "Fabric"),
                      ("quilt", "Quilt"), ("optifine", "OptiFine")):
        if key in v:
            return name
    return "Vanilla"


def _scan_minecraft_dir(path: str, source: str) -> list:
    """Папка в формате официального лаунчера: versions/<id>/<id>.json."""
    out = []
    vdir = os.path.join(path, "versions")
    if not os.path.isdir(vdir):
        return out
    for vid in sorted(os.listdir(vdir)):
        data = _read_json(os.path.join(vdir, vid, vid + ".json"))
        if not isinstance(data, dict):
            continue
        mc = data.get("inheritsFrom") or data.get("id") or vid
        out.append({"source": source, "kind": "external", "label": vid, "mc_version": str(mc),
                    "loader": _loader_of_version_id(vid), "version_id": vid, "path": path,
                    "supported": True, "why": ""})
    return out


def _instance_entry(source, label, mc, loader, loader_ver, game_dir):
    supported, why = True, ""
    if not mc:
        supported, why = False, "не нашёл версию Minecraft"
    elif loader == "quilt":
        supported, why = False, "Quilt пока не поддерживается"
    elif loader not in ("vanilla", "forge", "fabric", "neoforge"):
        supported, why = False, f"загрузчик {loader} не поддерживается"
    return {"source": source, "kind": "instance", "label": label, "mc_version": mc or "?",
            "loader": loader, "loader_version": loader_ver or "", "path": game_dir,
            "supported": supported, "why": why}


def _parse_prism_instance(d: str, source: str):
    pack = _read_json(os.path.join(d, "mmc-pack.json"))
    if not isinstance(pack, dict):
        return None
    name = os.path.basename(d)
    try:
        with open(os.path.join(d, "instance.cfg"), "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("name="):
                    name = line[5:].strip() or name
    except OSError:
        pass
    mc, loader, lver = None, "vanilla", ""
    for comp in pack.get("components", []):
        uid, ver = comp.get("uid", ""), comp.get("version", "")
        if uid == "net.minecraft":
            mc = ver
        elif uid == "net.minecraftforge":
            loader, lver = "forge", ver
        elif uid == "net.neoforged":
            loader, lver = "neoforge", ver
        elif uid == "net.fabricmc.fabric-loader":
            loader, lver = "fabric", ver
        elif uid == "org.quiltmc.quilt-loader":
            loader, lver = "quilt", ver
    game = next((os.path.join(d, g) for g in ("minecraft", ".minecraft") if os.path.isdir(os.path.join(d, g))),
                os.path.join(d, ".minecraft"))
    return _instance_entry(source, name, mc, loader, lver, game)


def _parse_curseforge_instance(d: str, source: str):
    data = _read_json(os.path.join(d, "minecraftinstance.json"))
    if not isinstance(data, dict):
        return None
    base = data.get("baseModLoader") or {}
    mc = base.get("minecraftVersion") or data.get("gameVersion")
    loader, lver = "vanilla", ""
    name = str(base.get("name") or "")
    if name:
        kind, _, rest = name.partition("-")
        loader = kind.lower()
        lver = rest.split("-")[0] if loader == "fabric" else rest
    return _instance_entry(source, data.get("name") or os.path.basename(d), mc, loader, lver, d)


def _parse_atlauncher_instance(d: str, source: str):
    data = _read_json(os.path.join(d, "instance.json"))
    if not isinstance(data, dict):
        return None
    lv = ((data.get("launcher") or {}).get("loaderVersion") or {})
    loader = str(lv.get("type") or "vanilla").lower()
    name = (data.get("launcher") or {}).get("name") or os.path.basename(d)
    return _instance_entry(source, name, data.get("id"), loader, lv.get("version"), d)


def _parse_modrinth_profile(d: str, source: str):
    data = _read_json(os.path.join(d, "profile.json"))
    if not isinstance(data, dict):
        return None
    meta = data.get("metadata") or data
    lv = meta.get("loader_version") or {}
    lver = lv.get("id") if isinstance(lv, dict) else str(lv or "")
    if lver and "-" in lver and meta.get("loader") == "forge":
        lver = lver.split("-", 1)[1]
    return _instance_entry(source, meta.get("name") or os.path.basename(d), meta.get("game_version"),
                           str(meta.get("loader") or "vanilla").lower(), lver, d)


def _scan_folder_any(path: str, source: str = "Папка") -> list:
    """Определяет тип выбранной вручную папки."""
    for parser in (_parse_prism_instance, _parse_curseforge_instance, _parse_atlauncher_instance,
                   _parse_modrinth_profile):
        e = parser(path, source)
        if e:
            return [e]
    found = _scan_minecraft_dir(path, source)
    if not found and os.path.isdir(os.path.join(path, ".minecraft")):
        found = _scan_minecraft_dir(os.path.join(path, ".minecraft"), source)
    return found


def _scan_other_launchers() -> list:
    found, seen = [], set()
    locs = _other_launcher_locations()
    for source, path in locs["mc"]:
        if os.path.isdir(path) and os.path.realpath(path) not in seen:
            seen.add(os.path.realpath(path))
            found += _scan_minecraft_dir(path, source)
    for key, parser in (("prism", _parse_prism_instance), ("curseforge", _parse_curseforge_instance),
                        ("atlauncher", _parse_atlauncher_instance), ("modrinth", _parse_modrinth_profile)):
        for source, root_dir in locs[key]:
            if not os.path.isdir(root_dir):
                continue
            for name in sorted(os.listdir(root_dir)):
                d = os.path.join(root_dir, name)
                if os.path.isdir(d) and os.path.realpath(d) not in seen:
                    e = parser(d, source)
                    if e:
                        seen.add(os.path.realpath(d))
                        found.append(e)
    return found


def _import_entry(entry: dict) -> str:
    """Добавляет найденную версию в список лаунчера. Возвращает её имя."""
    custom = load_custom_versions()
    base = f"[{entry['source']}] {entry['label']}"
    name, n = base, 2
    existing = get_all_versions()
    while name in existing:
        same = existing[name]
        if (same.get("game_dir") == entry["path"]
                or (same.get("external_dir") == entry["path"]
                    and same.get("version_id") == entry.get("version_id"))):
            break   # та же самая версия — просто обновим запись
        name, n = f"{base} ({n})", n + 1
    if entry["kind"] == "external":
        custom[name] = {"loader": "external", "mc_version": entry["mc_version"],
                        "version_id": entry["version_id"], "external_dir": entry["path"],
                        "source": entry["source"]}
    else:
        mc, loader, lver = entry["mc_version"], entry["loader"], entry.get("loader_version", "")
        item = {"loader": loader, "mc_version": mc, "game_dir": entry["path"], "source": entry["source"]}
        if loader == "forge":
            # Старые Forge (до 1.10) в Maven называются «mc-версия-mc»
            if lver and not lver.startswith(mc):
                lver = f"{mc}-{lver}"
                if _version_tuple(mc) < (1, 10):
                    lver = f"{lver}-{mc}"
            item["forge"] = lver
        elif loader == "fabric":
            item["fabric"] = lver or "0.16.14"
        elif loader == "neoforge":
            item["neoforge"] = lver
        custom[name] = item
    save_custom_versions(custom)
    return name


def _show_import_dialog(master, on_done=None):
    win = tk.Toplevel(master)
    win.title("Импорт из других лаунчеров")
    win.geometry("820x560")
    win.minsize(560, 360)
    win.configure(bg=C["bg"])
    win.transient(master)

    tk.Label(win, text="Версии и сборки из других лаунчеров", bg=C["bg"], fg=C["text"],
             font=_font(13, "bold"), anchor="w").pack(fill="x", padx=20, pady=(16, 2))
    _desc = tk.Label(win, text="Официальный лаунчер и TLauncher — версии запускаются прямо из их папки. "
                               "Сборки Prism, CurseForge, ATLauncher, Modrinth — загрузчик ставится здесь, "
                               "а моды, миры и настройки берутся из папки сборки.",
                     bg=C["bg"], fg=C["text_muted"], font=FS, justify="left", anchor="w")
    _desc.pack(fill="x", padx=20, pady=(0, 10))
    _desc.bind("<Configure>", lambda e: e.widget.config(wraplength=max(100, e.width - 4)))

    lst_outer = tk.Frame(win, bg=C["border"])
    lst_outer.pack(fill="both", expand=True, padx=20)
    cv = tk.Canvas(lst_outer, bg=C["bg_panel"], highlightthickness=0)
    sb = ttk.Scrollbar(lst_outer, orient="vertical", command=cv.yview,
                       style="Soft.Vertical.TScrollbar" if C.get("soft_ui") else "Vertical.TScrollbar")
    inner = tk.Frame(cv, bg=C["bg_panel"])
    inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    win_id = cv.create_window((0, 0), window=inner, anchor="nw")
    cv.bind("<Configure>", lambda e: cv.itemconfigure(win_id, width=e.width))
    cv.configure(yscrollcommand=sb.set)
    cv.pack(side="left", fill="both", expand=True, padx=1, pady=1)
    sb.pack(side="right", fill="y")

    status = tk.Label(win, text="Ищу...", bg=C["bg"], fg=C["text_muted"], font=FS, anchor="w")
    status.pack(fill="x", padx=20, pady=(8, 0))
    checks = []

    def render(entries, append=False):
        if not append:
            for w in inner.winfo_children():
                w.destroy()
            checks.clear()
        if not entries and not checks:
            tk.Label(inner, text="Ничего не нашлось. Нажми «Выбрать папку…» и укажи папку сборки\n"
                                 "или .minecraft другого лаунчера.",
                     bg=C["bg_panel"], fg=C["text_muted"], font=_font(10), justify="left").pack(
                anchor="w", padx=14, pady=14)
        for e in entries:
            row = tk.Frame(inner, bg=C["bg_panel"])
            row.pack(fill="x", padx=8, pady=2)
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(row, variable=var, bg=C["bg_panel"], selectcolor=C["bg_input"],
                                activebackground=C["bg_panel"], bd=0, highlightthickness=0,
                                state="normal" if e["supported"] else "disabled")
            cb.pack(side="left")
            loader = e["loader"].capitalize() if e["kind"] == "instance" else e["loader"]
            if e["kind"] == "instance" and e.get("loader_version"):
                loader += " " + e["loader_version"]
            tk.Label(row, text=e["source"], bg=C["bg_panel"], fg=C["amber"], font=_font(9, "bold"),
                     width=16, anchor="w").pack(side="left")
            tk.Label(row, text=e["label"], bg=C["bg_panel"], fg=C["text"] if e["supported"] else C["text_dim"],
                     font=_font(10), anchor="w").pack(side="left", fill="x", expand=True)
            tk.Label(row, text=(f"MC {e['mc_version']} · {loader}" if e["supported"] else e["why"]),
                     bg=C["bg_panel"], fg=C["text_muted"], font=_font(9), anchor="e").pack(side="right", padx=8)
            if e["supported"]:
                checks.append((var, e))
        status.config(text=f"Найдено: {len(checks)}. Отметь нужные и нажми «Импортировать».")

    def scan():
        res = _scan_other_launchers()
        win.after(0, lambda: render(res))
    threading.Thread(target=scan, daemon=True).start()

    def pick_folder():
        d = filedialog.askdirectory(parent=win, title="Папка сборки или .minecraft другого лаунчера")
        if not d:
            return
        res = _scan_folder_any(d)
        if not res:
            messagebox.showwarning("Импорт", "В этой папке не нашёл ни версий Minecraft, ни сборки.", parent=win)
            return
        render(res, append=True)
        for var, e in checks[-len(res):]:
            var.set(True)

    def do_import():
        chosen = [e for var, e in checks if var.get()]
        if not chosen:
            return status.config(text="Ничего не отмечено", fg=C["red"])
        names = [_import_entry(e) for e in chosen]
        win.destroy()
        messagebox.showinfo("Импорт", "Добавлено в список версий:\n\n" + "\n".join(names), parent=master)
        if on_done:
            on_done(names[0])

    bar = tk.Frame(win, bg=C["bg"])
    bar.pack(fill="x", padx=20, pady=14)
    FlatButton(bar, "Импортировать", command=do_import, kind="primary", bg=C["bg"]).pack(side="right")
    FlatButton(bar, "Выбрать папку…", command=pick_folder, bg=C["bg"]).pack(side="right", padx=(0, 8))
    FlatButton(bar, "Закрыть", command=win.destroy, kind="ghost", bg=C["bg"]).pack(side="left")



# ══════════════════════════════════════════
#  DISCORD RICH PRESENCE
#  Использует pypresence. Если не установлена —
#  молча пропускает, лаунчер работает без RPC.
#
#  pip install pypresence
#  PyInstaller: --hidden-import pypresence
# ══════════════════════════════════════════

# Client ID твоего Discord приложения.
# Создай на https://discord.com/developers/applications
# → New Application → OAuth2 → Client ID
DISCORD_CLIENT_ID = "1485734288279212243"   # <-- вставь свой Client ID

_rpc        = None   # экземпляр Presence
_rpc_active = False  # True пока соединение открыто


def _rpc_connect():
    """Подключается к Discord IPC. Вызывать в фоновом потоке."""
    global _rpc, _rpc_active
    try:
        from pypresence import Presence
        _rpc = Presence(DISCORD_CLIENT_ID)
        _rpc.connect()
        _rpc_active = True
    except Exception:
        _rpc = None
        _rpc_active = False


def rpc_set_idle():
    """Статус: в лаунчере, не в игре."""
    if not _rpc_active or _rpc is None: return
    try:
        _rpc.update(
            state="В лаунчере",
            details="Atomic Industry LMPD",
            large_image="launcher_icon",   # название ассета в Discord Dev Portal
            large_text="Atomic Industry Launcher",
            start=int(__import__("time").time()),
        )
    except Exception:
        pass


def rpc_set_playing(version: str, nickname: str):
    """Статус: играет в Minecraft версии version."""
    if not _rpc_active or _rpc is None: return
    try:
        _rpc.update(
            state=f"Играет как {nickname}",
            details=f"Minecraft {version}",
            large_image="launcher_icon",
            large_text="Atomic Industry Launcher",
            small_image="mc_icon",         # необязательно, можно убрать
            small_text=f"MC {version}",
            start=int(__import__("time").time()),
        )
    except Exception:
        pass


def rpc_clear():
    """Очистить статус и закрыть соединение."""
    global _rpc, _rpc_active
    if _rpc is not None:
        try: _rpc.clear(); _rpc.close()
        except: pass
    _rpc = None; _rpc_active = False


def rpc_init_async():
    """Запустить подключение к Discord в фоне — не блокирует старт лаунчера."""
    threading.Thread(target=_rpc_connect_and_idle, daemon=True).start()


def _rpc_connect_and_idle():
    import time
    _rpc_connect()
    if _rpc_active:
        rpc_set_idle()


# ══════════════════════════════════════════
#  УПРАВЛЕНИЕ ВЕРСИЯМИ
# ══════════════════════════════════════════

def open_version_manager(parent):
    """Браузер версий — добавление своих версий Minecraft"""
    win = tk.Toplevel(parent)
    win.title("Управление версиями Minecraft")
    win.geometry("900x600")
    win.minsize(560, 420)
    win.configure(bg=C["bg"])

    # Заголовок
    header = tk.Frame(win, bg=C["panel"], height=60)
    header.pack(fill="x", padx=10, pady=10)
    header.pack_propagate(False)

    tk.Label(
        header,
        text="УПРАВЛЕНИЕ ВЕРСИЯМИ MINECRAFT",
        bg=C["panel"], fg=C["text"],
        font=("Segoe UI", 14, "bold")
    ).pack(side="left", padx=15, pady=15)

    def show_help():
        messagebox.showinfo("Инструкция",
            "Как добавить свою версию Minecraft:\n\n"
            "1. Нажмите Добавить версию\n"
            "2. Укажите название (например: 1.20.1 Modded)\n"
            "3. Выберите загрузчик: Vanilla / Forge / Fabric / NeoForge\n"
            "4. Укажите версию Minecraft (например: 1.20.1)\n"
            "5. Для Forge/Fabric укажите версию загрузчика; для NeoForge поле версии можно оставить пустым\n"
            "6. Нажмите Сохранить",
            parent=win)

    tk.Button(header, text="? Инструкция", command=show_help,
              bg=C["accent"], fg=C["text"], font=FE,
              relief="flat", cursor="hand2", padx=15, pady=5
              ).pack(side="right", padx=15)

    main_container = tk.Frame(win, bg=C["bg"])
    main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Список версий
    list_frame = tk.Frame(main_container, bg=C["panel"])
    list_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

    tk.Label(list_frame, text="Все версии:", bg=C["panel"], fg=C["text"],
             font=FE, anchor="w").pack(fill="x", padx=10, pady=(10, 5))

    list_scroll_frame = tk.Frame(list_frame, bg=C["panel"])
    list_scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    scrollbar = tk.Scrollbar(list_scroll_frame)
    scrollbar.pack(side="right", fill="y")

    version_listbox = tk.Listbox(
        list_scroll_frame,
        bg=C["input_bg"], fg=C["text"], font=FE,
        selectmode="single", yscrollcommand=scrollbar.set,
        relief="flat", highlightthickness=0,
        selectbackground=C["accent"], selectforeground=C["text"]
    )
    version_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=version_listbox.yview)

    # Панель действий
    action_frame = tk.Frame(main_container, bg=C["panel"], width=350)
    action_frame.pack(side="right", fill="y", padx=(5, 0))
    action_frame.pack_propagate(False)

    tk.Label(action_frame, text="Действия:", bg=C["panel"], fg=C["text"],
             font=FE, anchor="w").pack(fill="x", padx=10, pady=(10, 5))

    info_text = tk.Text(
        action_frame, bg=C["input_bg"], fg=C["text"], font=FS,
        height=12, wrap="word", relief="flat", state="disabled"
    )
    info_text.pack(fill="x", padx=10, pady=(5, 10))

    def refresh_list():
        version_listbox.delete(0, tk.END)
        all_vers = get_all_versions()
        custom = load_custom_versions()

        built_in = [(k, v) for k, v in all_vers.items() if k not in custom]
        user_added = [(k, v) for k, v in custom.items()]

        for name, _ in built_in:
            version_listbox.insert(tk.END, f"  {name}")

        if user_added:
            version_listbox.insert(tk.END, "─" * 40)
            for name, _ in user_added:
                version_listbox.insert(tk.END, f"+ {name}")

    def get_selected_name():
        sel = version_listbox.curselection()
        if not sel:
            return None
        txt = version_listbox.get(sel[0])
        if "─" in txt:
            return None
        return txt.strip().lstrip("+").strip()

    def show_version_info(event=None):
        name = get_selected_name()
        if not name:
            return
        all_vers = get_all_versions()
        if name not in all_vers:
            return
        ver_info = all_vers[name]
        custom = load_custom_versions()
        is_custom = name in custom

        info = f"Название: {name}\n\n"
        info += f"MC версия: {ver_info.get('mc_version', 'N/A')}\n\n"
        loader_name = ver_info.get("loader", "N/A")
        loader_name = {"neoforge": "NeoForge", "external": "как в другом лаунчере"}.get(
            loader_name, loader_name.title())
        info += f"Загрузчик: {loader_name}\n\n"
        if ver_info.get("source"):
            info += f"Импорт из: {ver_info['source']}\n\n"
        if ver_info.get("version_id"):
            info += f"Профиль: {ver_info['version_id']}\n\n"
        if ver_info.get("external_dir") or ver_info.get("game_dir"):
            info += f"Папка: {ver_info.get('game_dir') or ver_info.get('external_dir')}\n\n"
        if ver_info.get("forge"):
            info += f"Forge: {ver_info['forge']}\n\n"
        if ver_info.get("fabric"):
            info += f"Fabric: {ver_info['fabric']}\n\n"
        if loader_name == "NeoForge":
            info += f"NeoForge: {ver_info.get('neoforge') or 'последняя совместимая (авто)'}\n\n"
        info += "Пользовательская" if is_custom else "Встроенная"

        info_text.config(state="normal")
        info_text.delete(1.0, tk.END)
        info_text.insert(1.0, info)
        info_text.config(state="disabled")

    version_listbox.bind("<<ListboxSelect>>", show_version_info)

    def add_version():
        dialog = tk.Toplevel(win)
        dialog.title("Добавить версию")
        dialog.geometry("520x620")
        dialog.configure(bg=C["bg"])
        dialog.resizable(False, False)

        tk.Label(dialog, text="Добавление новой версии",
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(15, 20))

        form = tk.Frame(dialog, bg=C["bg"])
        form.pack(fill="both", expand=True, padx=20)

        tk.Label(form, text="Название версии:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        name_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        name_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Загрузчик:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        loader_var = tk.StringVar(value="vanilla")
        loader_frame = tk.Frame(form, bg=C["bg"])
        loader_frame.pack(fill="x", pady=(0, 12))
        for loader in ["vanilla", "forge", "fabric", "neoforge"]:
            loader_label = "NeoForge" if loader == "neoforge" else loader.title()
            tk.Radiobutton(loader_frame, text=loader_label, variable=loader_var, value=loader,
                           bg=C["bg"], fg=C["text"], font=FE,
                           selectcolor=C["panel"], activebackground=C["bg"],
                           activeforeground=C["text"]).pack(side="left", padx=(0, 12))

        tk.Label(form, text="Версия Minecraft (например: 1.20.1):", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        mc_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        mc_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия Forge (например: 1.20.1-47.2.0):", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        forge_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        forge_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия Fabric (например: 0.15.11):", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        fabric_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        fabric_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия NeoForge (пусто — последняя совместимая):", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        neoforge_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        neoforge_entry.pack(fill="x", ipady=5, pady=(0, 12))


        def save_new():
            n = name_entry.get().strip()
            mc = mc_entry.get().strip()
            if not n or not mc:
                messagebox.showerror("Ошибка", "Укажите название и версию Minecraft!", parent=dialog)
                return
            custom = load_custom_versions()
            entry = {"mc_version": mc, "loader": loader_var.get()}
            if loader_var.get() == "forge" and forge_entry.get().strip():
                entry["forge"] = forge_entry.get().strip()
            if loader_var.get() == "fabric" and fabric_entry.get().strip():
                entry["fabric"] = fabric_entry.get().strip()
            if loader_var.get() == "neoforge" and neoforge_entry.get().strip():
                entry["neoforge"] = neoforge_entry.get().strip()
            custom[n] = entry
            save_custom_versions(custom)
            messagebox.showinfo("Успех", f"Версия '{n}' добавлена!", parent=dialog)
            refresh_list()
            dialog.destroy()

        btn_f = tk.Frame(dialog, bg=C["bg"])
        btn_f.pack(fill="x", padx=20, pady=(0, 15))
        tk.Button(btn_f, text="Сохранить", command=save_new,
                  bg=C["accent"], fg=C["text"], font=FE,
                  relief="flat", cursor="hand2", padx=20, pady=6).pack(side="left", padx=(0, 8))
        tk.Button(btn_f, text="Отмена", command=dialog.destroy,
                  bg=C["panel"], fg=C["text"], font=FE,
                  relief="flat", cursor="hand2", padx=20, pady=6).pack(side="left")

    def edit_version():
        name = get_selected_name()
        if not name:
            messagebox.showwarning("Внимание", "Выберите версию!", parent=win)
            return
        custom = load_custom_versions()
        if name not in custom:
            messagebox.showwarning("Внимание", "Можно редактировать только пользовательские версии!", parent=win)
            return
        ver_info = custom[name]
        if ver_info.get("source"):
            messagebox.showinfo("Импорт", "Импортированную версию не редактируют — её можно удалить "
                                "и импортировать заново.", parent=win)
            return

        dialog = tk.Toplevel(win)
        dialog.title("Редактировать версию")
        dialog.geometry("520x620")
        dialog.configure(bg=C["bg"])
        dialog.resizable(False, False)

        tk.Label(dialog, text=f"Редактирование: {name}",
                 bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 12, "bold")).pack(pady=(15, 20))

        form = tk.Frame(dialog, bg=C["bg"])
        form.pack(fill="both", expand=True, padx=20)

        tk.Label(form, text="Название версии:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        name_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        name_entry.insert(0, name)
        name_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Загрузчик:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        loader_var = tk.StringVar(value=ver_info.get("loader", "vanilla"))
        loader_frame = tk.Frame(form, bg=C["bg"])
        loader_frame.pack(fill="x", pady=(0, 12))
        for loader in ["vanilla", "forge", "fabric", "neoforge"]:
            loader_label = "NeoForge" if loader == "neoforge" else loader.title()
            tk.Radiobutton(loader_frame, text=loader_label, variable=loader_var, value=loader,
                           bg=C["bg"], fg=C["text"], font=FE,
                           selectcolor=C["panel"], activebackground=C["bg"],
                           activeforeground=C["text"]).pack(side="left", padx=(0, 12))

        tk.Label(form, text="Версия Minecraft:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        mc_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        mc_entry.insert(0, ver_info.get("mc_version", ""))
        mc_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия Forge:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        forge_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        forge_entry.insert(0, ver_info.get("forge", ""))
        forge_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия Fabric:", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        fabric_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        fabric_entry.insert(0, ver_info.get("fabric", ""))
        fabric_entry.pack(fill="x", ipady=5, pady=(0, 12))

        tk.Label(form, text="Версия NeoForge (пусто — последняя совместимая):", bg=C["bg"], fg=C["text"], font=FE, anchor="w").pack(fill="x", pady=(0, 4))
        neoforge_entry = tk.Entry(form, bg=C["input_bg"], fg=C["text"], font=FE, relief="flat")
        neoforge_entry.insert(0, ver_info.get("neoforge", ""))
        neoforge_entry.pack(fill="x", ipady=5, pady=(0, 12))


        def save_edit():
            new_name = name_entry.get().strip()
            mc = mc_entry.get().strip()
            if not new_name or not mc:
                messagebox.showerror("Ошибка", "Укажите название и версию Minecraft!", parent=dialog)
                return
            custom = load_custom_versions()
            if new_name != name:
                del custom[name]
            entry = {"mc_version": mc, "loader": loader_var.get()}
            if loader_var.get() == "forge" and forge_entry.get().strip():
                entry["forge"] = forge_entry.get().strip()
            if loader_var.get() == "fabric" and fabric_entry.get().strip():
                entry["fabric"] = fabric_entry.get().strip()
            if loader_var.get() == "neoforge" and neoforge_entry.get().strip():
                entry["neoforge"] = neoforge_entry.get().strip()
            custom[new_name] = entry
            save_custom_versions(custom)
            messagebox.showinfo("Успех", f"Версия '{new_name}' обновлена!", parent=dialog)
            refresh_list()
            dialog.destroy()

        btn_f = tk.Frame(dialog, bg=C["bg"])
        btn_f.pack(fill="x", padx=20, pady=(0, 15))
        tk.Button(btn_f, text="Сохранить", command=save_edit,
                  bg=C["accent"], fg=C["text"], font=FE,
                  relief="flat", cursor="hand2", padx=20, pady=6).pack(side="left", padx=(0, 8))
        tk.Button(btn_f, text="Отмена", command=dialog.destroy,
                  bg=C["panel"], fg=C["text"], font=FE,
                  relief="flat", cursor="hand2", padx=20, pady=6).pack(side="left")

    def delete_version():
        name = get_selected_name()
        if not name:
            messagebox.showwarning("Внимание", "Выберите версию!", parent=win)
            return
        custom = load_custom_versions()
        if name not in custom:
            messagebox.showwarning("Внимание", "Можно удалять только пользовательские версии!", parent=win)
            return
        if messagebox.askyesno("Подтверждение", f"Удалить версию '{name}'?", parent=win):
            del custom[name]
            save_custom_versions(custom)
            refresh_list()

    btn_container = tk.Frame(action_frame, bg=C["panel"])
    btn_container.pack(fill="x", padx=10, pady=10)

    tk.Button(btn_container, text="+ Добавить версию", command=add_version,
              bg=C["accent"], fg=C["text"], font=FE,
              relief="flat", cursor="hand2", width=20).pack(fill="x", pady=(0, 5))

    tk.Button(btn_container, text="📥 Импорт из других лаунчеров",
              command=lambda: _show_import_dialog(win, on_done=lambda *_: refresh_list()),
              bg=C["panel_hover"], fg=C["text"], font=FE,
              relief="flat", cursor="hand2", width=20).pack(fill="x", pady=(0, 5))

    tk.Button(btn_container, text="Редактировать", command=edit_version,
              bg=C["panel_hover"], fg=C["text"], font=FE,
              relief="flat", cursor="hand2", width=20).pack(fill="x", pady=(0, 5))

    tk.Button(btn_container, text="Удалить", command=delete_version,
              bg=C["red"], fg=C["text"], font=FE,
              relief="flat", cursor="hand2", width=20).pack(fill="x", pady=(0, 5))

    refresh_list()


def _ui_log_safe(text, level="info"):
    fn = _ui_state.get("log")
    if fn:
        try:
            fn(text, level)
        except Exception:
            pass


def start_gui():
    config  = load_config(); max_ram = get_available_ram_gb()
    # Разовый переход на новую тему «Ночь» для тех, кто сидел на старой ATOMIC
    if not config.get("_night_migrated"):
        if config.get("theme", "atomic") == "atomic":
            config["theme"] = "night"
        config["_night_migrated"] = True
        save_config(config)
    # Применяем сохранённое имя кастомной темы
    cname = config.get("custom_theme_name", "CUSTOM") or "CUSTOM"
    THEMES["custom"]["name"] = f"✏  {cname}"

    # className — для правил оконных менеджеров (Hyprland: windowrulev2 = float, class:^(AtomicLauncher)$)
    root = tk.Tk(className="AtomicLauncher")
    root.title("Atomic Launcher")
    _resolve_font_families(root)
    load_dev_mode()
    apply_theme(config.get("theme", "night"), config.get("custom_theme") or {})

    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    W, H = min(1040, max(560, sw - 80)), min(740, max(460, sh - 120))
    root.geometry(f"{W}x{H}")
    # Маленький минимум: тайловый WM может сжать окно — тогда тело прокручивается,
    # а подвал с кнопкой «Играть» остаётся на месте.
    root.minsize(480, 400)
    root.resizable(True, True)

    build_ui(root, config, max_ram)
    if is_dev_mode():
        root.after(300, lambda: _ui_log_safe(f"🧪 Режим разработчика: {_DEV['name']}", "info"))
    elif _DEV.get("error"):
        root.after(300, lambda: _ui_log_safe(f"dev.key не принят: {_DEV['error']}", "warn"))

    rpc_init_async()  # Discord RPC
    if config.get("auto_update", True):
        root.after(3500, lambda: check_for_updates(root, config, silent=True))

    def _on_close():
        rpc_clear()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", _on_close)
    root.mainloop()
    rpc_clear()


if __name__ == "__main__":
    start_gui()

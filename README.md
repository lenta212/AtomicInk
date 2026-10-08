# Atomic Launcher

**Atomic Launcher** is an unofficial desktop launcher for Minecraft: Java Edition. This repository contains the launcher source in `launcher.py`.

## English

### Features

- Launch configured Minecraft Java Edition versions with Vanilla, Forge, Fabric, or NeoForge profiles where available.
- Install and manage mods and related content using Modrinth and CurseForge APIs.
- Configure the game directory, memory allocation, themes, and launcher preferences.
- Choose between Microsoft sign-in, the launcher's separate Atomic server account mode, and an offline nickname mode.
- Optionally check for signed launcher updates.

### Microsoft sign-in and local data

Microsoft sign-in uses the device-code flow. The user completes authentication on Microsoft's website; the launcher then exchanges tokens with Microsoft, Xbox Live/XSTS, and Minecraft Services to retrieve the Minecraft profile.

The launcher stores its configuration and account tokens in `launcher_config.json` next to the launcher. This file is JSON and is **not encrypted by the launcher**. Keep it private and do not upload or share it. Tokens used for Microsoft sign-in are sent to Microsoft's authentication services as required by the sign-in flow.

The offline nickname mode is separate from Microsoft authentication and does not verify ownership of Minecraft. The Atomic account mode uses a separately configured custom authentication server; only use a server you trust and use HTTPS when transmitting account credentials. Plain HTTP does not encrypt credentials in transit. These modes are not part of Microsoft sign-in.

### Launcher updates

When automatic updates are enabled, the launcher checks the configured Atomic server for `/atomic/update/manifest.json`. It verifies the Ed25519 signature on the manifest and checks the downloaded file's declared size and SHA-256 hash. It offers an update only when a newer version is available and asks the user before installing and restarting.

Publishing signed updates requires the matching private signing key and release tooling. **Never commit the private signing key, account tokens, or `launcher_config.json` to this repository.**

### Run from source

Requirements:

- Python 3.12 is recommended.
- Tkinter, included with many Python installations (some Linux distributions package it separately).
- A Java runtime compatible with the selected Minecraft version.

Create and activate a virtual environment, then install the Python dependencies:

```text
Windows:  py -3.12 -m venv .venv
Linux:    python3 -m venv .venv
```

Activate it:

```text
Windows PowerShell:  .\.venv\Scripts\Activate.ps1
Windows Git Bash:    source .venv/Scripts/activate
Linux:               source .venv/bin/activate
```

Install dependencies and run the launcher:

```bash
python -m pip install --upgrade pip
python -m pip install minecraft-launcher-lib psutil pillow cryptography pypresence
python launcher.py
```

### Build with PyInstaller

Build on the operating system you intend to distribute for; PyInstaller does not make a Windows executable when run on Linux, or vice versa.

Install PyInstaller in the activated virtual environment:

```bash
python -m pip install pyinstaller
```

**Windows** — run in PowerShell:

```powershell
python -m PyInstaller --noconfirm --clean --onefile `
  --name AtomicLauncher `
  --hidden-import=pypresence `
  --collect-all minecraft_launcher_lib `
  --collect-all PIL `
  --collect-all cryptography `
  launcher.py
```

The executable is created at `dist/AtomicLauncher.exe`.

**Linux** — run in a desktop environment with Tkinter installed:

```bash
python -m PyInstaller --noconfirm --clean --onefile \
  --name AtomicLauncher \
  --hidden-import=pypresence \
  --collect-all minecraft_launcher_lib \
  --collect-all PIL \
  --collect-all cryptography \
  launcher.py
chmod +x dist/AtomicLauncher
```

The result, `dist/AtomicLauncher`, is a native Linux executable, **not** a shell script. If you specifically need a `.sh` file to run the Python source, create `run_launcher.sh` beside `launcher.py`:

```bash
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
exec .venv/bin/python launcher.py "$@"
```

Make it executable with `chmod +x run_launcher.sh`. This wrapper uses the virtual environment prepared above; it still requires Tkinter, Java, and the Python dependencies to be installed.

## По-русски

### Что это

Atomic Launcher — неофициальный настольный лаунчер для Minecraft: Java Edition. В репозитории находится исходный код `launcher.py`.

Возможности:

- запуск настроенных версий Minecraft с Vanilla, Forge, Fabric или NeoForge, если профиль доступен;
- установка и управление модами и связанным контентом через API Modrinth и CurseForge;
- настройка папки игры, выделенной памяти, темы и параметров лаунчера;
- отдельные режимы входа: Microsoft, аккаунт собственного Atomic-сервера и офлайн-ник;
- проверка подписанных обновлений лаунчера, если она включена.

### Microsoft-вход и данные на компьютере

Вход Microsoft работает через Device Code Flow: пользователь подтверждает вход на сайте Microsoft, после чего лаунчер обращается к Microsoft, Xbox Live/XSTS и Minecraft Services, чтобы получить профиль Minecraft.

Конфигурация и токены аккаунтов сохраняются в `launcher_config.json` рядом с лаунчером. Это обычный JSON-файл — **лаунчер не шифрует его содержимое**. Не выкладывай и не отправляй этот файл другим людям. Токены Microsoft передаются сервисам Microsoft, необходимым для авторизации.

Офлайн-режим с ником — отдельный режим, который не проверяет владение Minecraft. Режим Atomic использует отдельно настроенный сервер авторизации; используй только сервер, которому доверяешь, и HTTPS для передачи учётных данных. Обычный HTTP не шифрует логин и пароль при передаче. Эти два режима не являются частью входа через Microsoft.

### Обновления

Если автообновление включено, лаунчер проверяет на настроенном Atomic-сервере `/atomic/update/manifest.json`. Он проверяет подпись Ed25519 у манифеста, а также заявленный размер скачанного файла и его SHA-256. Обновление предлагается только для более новой версии; перед установкой лаунчер спрашивает пользователя и затем перезапускается.

Для публикации обновлений необходимы соответствующий закрытый ключ подписи и инструменты сборки релизов. **Не добавляй закрытый ключ, токены или `launcher_config.json` в этот репозиторий.**

### Запуск из исходников

Рекомендуется Python 3.12. Для интерфейса нужен Tkinter, а для запуска Minecraft — совместимая версия Java. На некоторых Linux-дистрибутивах Tkinter устанавливается отдельным системным пакетом.

Создай виртуальное окружение:

```text
Windows:  py -3.12 -m venv .venv
Linux:    python3 -m venv .venv
```

Активируй его:

```text
Windows PowerShell:  .\.venv\Scripts\Activate.ps1
Windows Git Bash:    source .venv/Scripts/activate
Linux:               source .venv/bin/activate
```

Установи зависимости и запусти программу:

```bash
python -m pip install --upgrade pip
python -m pip install minecraft-launcher-lib psutil pillow cryptography pypresence
python launcher.py
```

### Сборка

Собирать нужно на целевой системе: запуск PyInstaller в Linux не создаст `.exe` для Windows, и наоборот. Команды для Windows и Linux выше создают файл в папке `dist`.

В Linux PyInstaller создаёт исполняемый бинарный файл `dist/AtomicLauncher`, а не `.sh`. Shell-скрипт `run_launcher.sh` из примера выше лишь запускает исходный `launcher.py` через подготовленное виртуальное окружение `.venv` и требует установленного Tkinter, Java и зависимостей.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Mojang Studios or Microsoft. Minecraft is a trademark of Microsoft.

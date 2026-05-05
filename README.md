# QK — Quick Kit

A multi-OS CLI Swiss army knife for daily computer tasks. One command, nine modules.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-macOS%20|%20Linux%20|%20Windows-lightgrey?style=flat-square)

<img width="1555" height="828" alt="demo" src="https://github.com/user-attachments/assets/52a57e17-c540-42ad-b642-4c3466674e26" />

## Install

```bash
pip install qk-tool
```

## First Run

On first run, QK launches a setup wizard where you pick which modules to enable:

```
$ qk
🔧 QK Setup — Welcome!
Select which modules to enable...
```

Re-run anytime with `qk setup`.

## Modules

### save — Command Saver

```bash
qk save add "list containers" "docker ps -a" --tag docker
qk save list --tag docker
qk save search "container"
qk save copy <id>
qk save remove <id>
```

### system — System Actions

```bash
qk system port 8080
qk system kill-port 8080
qk system ip
qk system flush-dns
qk system trash
qk system info
```

### organize — File Organizer

```bash
qk organize run ~/Downloads --dry
qk organize run ~/Downloads
qk organize list-rules
qk organize add-rule .pdf Documents
qk organize remove-rule <id>
```

### convert — Converter

```bash
qk convert unit 100 kg lb
qk convert color "#ff5733"
qk convert base64 "hello world"
qk convert base64 "aGVsbG8=" --decode
qk convert json-fmt '{"a":1}'
qk convert json-fmt '{"a": 1}' --mini
```

### note — Quick Notes

```bash
qk note add "meeting at 3pm" --tag work
qk note list --tag work
qk note search "meeting"
qk note remove <id>
qk note export
```

### security — Password & Security

```bash
qk security pass
qk security pass --length 24 --symbols
qk security hash "some text"
qk security hash-file document.pdf
qk security checksum file.txt <expected-hash>
```

### clean — System Cleaner

```bash
qk clean temp --dry
qk clean temp
qk clean big ~/Documents --top 20
qk clean duplicates ~/Photos --dry
```

### text — Text Processing

```bash
qk text count file.txt
qk text case "helloWorld" --to snake
qk text case "hello_world" --to camel
qk text case "hello world" --to kebab
qk text lorem 3
qk text regex "\d+" file.txt
```

### net — Network Tools

```bash
qk net speed
qk net ip
qk net dns google.com
qk net ping google.com --count 5
qk net check github.com
```

## Data

All data is stored locally in `~/.qk/` as human-readable JSON files. No cloud, no tracking, no database.

```
~/.qk/
├── config.json
├── saves.json
├── notes.json
└── organize_rules.json
```

## License

MIT

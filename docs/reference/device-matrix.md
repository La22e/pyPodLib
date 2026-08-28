# Device matrix

Supported iPod models and their checksum families.

| Model number | Generation | Family | Checksum | Notes |
|---|---|---|---|---|
| MA146 | Mini 1G 4GB | iPod Mini | NONE | |
| MA188 | Mini 1G 4GB | iPod Mini | NONE | |
| MA205 | Mini 1G 4GB | iPod Mini | NONE | |
| MA206 | Mini 1G 4GB | iPod Mini | NONE | |
| MA214 | Mini 1G 4GB | iPod Mini | NONE | |
| MA215 | Mini 1G 4GB | iPod Mini | NONE | |
| MA216 | Mini 1G 4GB | iPod Mini | NONE | |
| MA217 | Mini 1G 4GB | iPod Mini | NONE | |
| MA233 | Mini 2G 4GB | iPod Mini | NONE | |
| MA234 | Mini 2G 4GB | iPod Mini | NONE | |
| MA235 | Mini 2G 6GB | iPod Mini | NONE | |
| MA236 | Mini 2G 6GB | iPod Mini | NONE | |
| MA350 | Classic 5G 30GB | iPod Classic | NONE | |
| MA444 | Classic 5G 30GB | iPod Classic | NONE | |
| MA445 | Classic 5G 60GB | iPod Classic | NONE | |
| MA446 | Classic 5G 60GB | iPod Classic | NONE | |
| MB029 | Classic 5.5G 30GB | iPod Classic | HASH58 | |
| MB147 | Classic 5.5G 30GB | iPod Classic | HASH58 | |
| MB148 | Classic 5.5G 80GB | iPod Classic | HASH58 | |
| MB149 | Classic 5.5G 80GB | iPod Classic | HASH58 | |
| MB150 | Classic 5.5G 30GB | iPod Classic | HASH58 | |
| MB562 | Classic 5.5G 80GB | iPod Classic | HASH58 | |
| MA632 | Classic 6G 80GB | iPod Classic | HASH58 | |
| MA633 | Classic 6G 160GB | iPod Classic | HASH58 | |
| MC297 | Classic 7G 160GB | iPod Classic | HASH58 | |
| MC293 | Classic 6G 120GB | iPod Classic | HASH58 | |
| MA978 | Nano 3G 4GB | iPod Nano | HASH58 | |
| MA979 | Nano 3G 8GB | iPod Nano | HASH58 | |
| MB754 | Nano 4G 8GB | iPod Nano | HASH58 | |
| MB755 | Nano 4G 16GB | iPod Nano | HASH58 | |
| MC027 | Nano 5G 8GB | iPod Nano | HASH72 | SQLite |
| MC028 | Nano 5G 16GB | iPod Nano | HASH72 | SQLite |
| MC059 | Nano 5G 8GB | iPod Nano | HASH72 | SQLite |
| MC060 | Nano 5G 4GB | iPod Nano | HASH72 | SQLite |
| MC112 | Nano 5G 16GB | iPod Nano | HASH72 | SQLite |
| MC275 | Nano 5G 8GB | iPod Nano | HASH72 | SQLite |
| MC525 | Nano 6G 8GB | iPod Nano | HASHAB | SQLite |
| MC526 | Nano 6G 16GB | iPod Nano | HASHAB | SQLite |
| MKMX2 | Nano 7G 16GB | iPod Nano | HASHAB | SQLite |

## Checksum types

| Type | Technology | Devices |
|---|---|---|
| NONE | No signature | Pre-2007 iPods (Mini, 5G Classic, early Nano) |
| HASH58 | FireWire GUID | Classic 5.5G/6G/7G, Nano 3G/4G |
| HASH72 | AES via pycryptodome | Nano 5G |
| HASHAB | WebAssembly via wasmtime | Nano 6G/7G |

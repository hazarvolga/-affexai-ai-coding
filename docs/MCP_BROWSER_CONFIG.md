# MCP Tarayıcıdan Yapılandırma Rehberi

## 🎯 Özet

Node.js sunucuda hazır! Artık sadece tarayıcıdan OpenHands'de MCP sunucularını yapılandırmanız yeterli.

## 📋 Adım Adım Yapılandırma

### 1️⃣ OpenHands'i Açın

Tarayıcınızda:
```
https://ai.fpvlovers.com.tr
```

### 2️⃣ Settings'e Gidin

- Sağ üst köşede **⚙️ Settings** simgesine tıklayın
- Sol menüden **MCP Settings** seçin

### 3️⃣ MCP Sunucularını Ekleyin

**"Add MCP Server"** veya **"+"** butonuna tıklayın ve aşağıdaki yapılandırmaları ekleyin:

---

## 🔧 Yapılandırmalar (Kopyala-Yapıştır)

### 1. 📁 Filesystem (Token Gerektirmez) ✅

**En önemli MCP - Mutlaka ekleyin!**

```json
{
  "name": "filesystem",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/opt/workspace"
  ],
  "env": {}
}
```

**Test:**
```
"Workspace'deki tüm dosyaları listele"
```

---

### 2. 🐙 GitHub (Token Gerekli) ⚡

**GitHub işlemleri için**

```json
{
  "name": "github",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "BURAYA_TOKEN_YAZIN"
  }
}
```

**Token nasıl alınır:**
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scope: `repo`, `workflow`
4. Token'ı kopyala ve yukarıdaki `BURAYA_TOKEN_YAZIN` yerine yapıştır

**Test:**
```
"GitHub repository'lerimi listele"
```

---

### 3. 🔍 Brave Search (API Key Gerekli) ⚡

**Web araması için**

```json
{
  "name": "brave-search",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-brave-search"
  ],
  "env": {
    "BRAVE_API_KEY": "BURAYA_API_KEY_YAZIN"
  }
}
```

**API Key nasıl alınır:**
1. https://brave.com/search/api/
2. Ücretsiz plan: 2000 sorgu/ay
3. API key'i kopyala ve yukarıdaki `BURAYA_API_KEY_YAZIN` yerine yapıştır

**Test:**
```
"Python async/await best practices araştır"
```

---

### 4. 🐳 Docker (Token Gerektirmez) ✅

**Container yönetimi için**

```json
{
  "name": "docker",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-docker"
  ],
  "env": {}
}
```

**Test:**
```
"Çalışan Docker container'ları listele"
```

---

### 5. 🐘 PostgreSQL (Connection String Gerekli) 🔧

**Veritabanı sorguları için**

```json
{
  "name": "postgres",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-postgres"
  ],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@host:5432/db"
  }
}
```

**Test:**
```
"users tablosundaki tüm kayıtları göster"
```

---

### 6. 💾 SQLite (Database Path Gerekli) 🔧

**Hafif veritabanı için**

```json
{
  "name": "sqlite",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-sqlite",
    "/opt/workspace/database.db"
  ],
  "env": {}
}
```

**Test:**
```
"SQLite veritabanındaki tabloları listele"
```

---

## 🎨 Kullanım

### MCP Durumunu Görme

Settings → MCP Settings'de:
- ✅ **Yeşil**: Çalışıyor
- ❌ **Kırmızı**: Hata var
- ⚪ **Gri**: Devre dışı

### Sohbette Kullanma

Normal şekilde sohbet edin, OpenHands otomatik olarak MCP'leri kullanır:

```
Sen: "Workspace'deki Python dosyalarını listele"
OpenHands: 🔧 Using tool: filesystem_list
         [Dosyaları listeler]

Sen: "test-app adında GitHub repo oluştur"
OpenHands: 🔧 Using tool: github_create_repository
         [Repo oluşturur]

Sen: "FastAPI authentication araştır"
OpenHands: 🔧 Using tool: brave_web_search
         [Arama yapar ve özetler]
```

---

## 🚀 Önerilen Başlangıç Seti

**Minimum (Token gerektirmez):**
```
✅ Filesystem
✅ Docker
```

**Tam Özellikli (Token gerekli):**
```
✅ Filesystem
✅ GitHub (token)
✅ Brave Search (API key)
✅ Docker
```

---

## 🐛 Sorun Giderme

### MCP Sunucusu Kırmızı Görünüyor

1. **Token/API key kontrolü:**
   - Doğru girilmiş mi?
   - Expire olmamış mı?
   - Doğru scope'lar var mı?

2. **Yapılandırma kontrolü:**
   - JSON syntax doğru mu?
   - Tırnak işaretleri doğru mu?
   - Virgüller yerinde mi?

3. **OpenHands'i yenile:**
   - Tarayıcıyı yenile (Ctrl+Shift+R)
   - Veya OpenHands container'ı restart et

### İlk Kullanımda Yavaş

- Normal! `npx` ilk seferde paketi indiriyor
- Sonraki kullanımlarda cache'den çalışır (hızlı)
- 5-10 saniye bekleyin

### MCP Aracı Kullanılmıyor

- Daha açık komut verin:
  - ❌ "Dosyaları göster"
  - ✅ "Workspace'deki tüm dosyaları listele"

---

## 💡 İpuçları

1. **Sadece ihtiyacınız olanları ekleyin** - Gereksiz MCP'ler performansı etkilemez ama karışıklık yaratır

2. **Token'ları güvenli tutun** - Asla GitHub'a commit etmeyin

3. **API limitlerine dikkat** - Brave Search: 2000/ay ücretsiz

4. **MCP loglarını takip edin** - Hangi aracın ne zaman kullanıldığını görün

---

## ✅ Kurulum Tamamlandı!

Artık OpenHands'iniz MCP sunucularıyla güçlendirildi! 🎉

**Sonraki adımlar:**
- Filesystem MCP'yi test edin
- GitHub token ekleyin (opsiyonel)
- Brave Search API key ekleyin (opsiyonel)
- Projelerinizde kullanmaya başlayın!

---

**Sunucu:** instance-hulyaekiz (161.118.171.201)  
**OpenHands:** https://ai.fpvlovers.com.tr  
**Node.js:** v20.19.6 ✅

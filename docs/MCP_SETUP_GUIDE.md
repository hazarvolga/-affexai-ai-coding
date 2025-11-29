# MCP (Model Context Protocol) Kurulum Rehberi

## 🎯 Genel Bakış

MCP sunucularını SSH ile sunucuya kurduktan sonra, OpenHands web arayüzünden (tarayıcıdan) bunları yapılandırıp kullanabilirsiniz.

## 📋 Adım Adım Kurulum

### Adım 1: Sunucuya Bağlanın ve MCP'yi Kurun

```bash
# SSH ile sunucuya bağlanın
ssh -i AffexAI-Oracle-Servers/instance-hulya/ssh-key-2025-09-20.key ubuntu@161.118.171.201

# Kurulum scriptini çalıştırın
bash ~/setup-mcp-servers.sh
```

**Veya manuel kurulum:**

```bash
# Node.js kurulumu
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Versiyonları kontrol edin
node --version  # v20.x.x olmalı
npm --version   # 10.x.x olmalı
```

### Adım 2: OpenHands Web Arayüzünde MCP'yi Yapılandırın

1. **Tarayıcınızda OpenHands'i açın:**
   ```
   https://ai.fpvlovers.com.tr
   ```

2. **Settings'e gidin:**
   - Sağ üst köşedeki ⚙️ (Settings) simgesine tıklayın

3. **MCP Settings sekmesini açın:**
   - Sol menüden "MCP Settings" veya "Model Context Protocol" seçin

4. **MCP Sunucusu ekleyin:**
   - "Add MCP Server" veya "+" butonuna tıklayın

### Adım 3: MCP Sunucularını Ekleyin

Aşağıdaki yapılandırmaları kullanarak MCP sunucularını ekleyin:

---

## 🔧 MCP Sunucu Yapılandırmaları

### 1. 📁 Filesystem Server (Dosya Sistemi Erişimi)

**Ne yapar:** OpenHands'in workspace'deki dosyaları okuyup yazmasını sağlar.

**Yapılandırma:**
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

**Kullanım örneği:**
- "Workspace'deki tüm Python dosyalarını listele"
- "config.json dosyasını oku"
- "README.md dosyasına yeni bir bölüm ekle"

---

### 2. 🐙 GitHub Server (GitHub Entegrasyonu)

**Ne yapar:** GitHub repository'leri ile etkileşim kurmanızı sağlar.

**Yapılandırma:**
```json
{
  "name": "github",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-github"
  ],
  "env": {
    "GITHUB_TOKEN": "ghp_your_github_token_here"
  }
}
```

**⚠️ Önemli:** `GITHUB_TOKEN` yerine kendi GitHub token'ınızı yazın!

**Token nasıl alınır:**
1. https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Scope seçin: `repo`, `workflow`
4. Token'ı kopyalayın

**Kullanım örneği:**
- "Benim GitHub repository'lerimi listele"
- "test-repo adında yeni bir repository oluştur"
- "README.md dosyasını güncelle ve commit yap"

---

### 3. 🔍 Brave Search Server (Web Araması)

**Ne yapar:** OpenHands'in web'de arama yapmasını sağlar.

**Yapılandırma:**
```json
{
  "name": "brave-search",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-brave-search"
  ],
  "env": {
    "BRAVE_API_KEY": "your_brave_api_key_here"
  }
}
```

**API Key nasıl alınır:**
1. https://brave.com/search/api/ adresine gidin
2. Ücretsiz API key alın (aylık 2000 sorgu)
3. API key'i kopyalayın

**Kullanım örneği:**
- "Python'da async/await nasıl kullanılır, araştır"
- "En son React best practices'leri neler?"
- "PostgreSQL performans optimizasyonu hakkında bilgi bul"

---

### 4. 🗄️ PostgreSQL Server (Veritabanı Erişimi)

**Ne yapar:** PostgreSQL veritabanına bağlanıp sorgu çalıştırmanızı sağlar.

**Yapılandırma:**
```json
{
  "name": "postgres",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-postgres"
  ],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user:password@host:5432/database"
  }
}
```

**Kullanım örneği:**
- "users tablosundaki tüm kayıtları göster"
- "Son 10 siparişi listele"
- "Yeni bir tablo oluştur"

---

### 5. 🐳 Docker Server (Docker Yönetimi)

**Ne yapar:** Docker container'larını yönetmenizi sağlar.

**Yapılandırma:**
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

**Kullanım örneği:**
- "Çalışan container'ları listele"
- "Nginx container'ı başlat"
- "Container loglarını göster"

---

### 6. 📊 Google Drive Server (Drive Erişimi)

**Ne yapar:** Google Drive dosyalarına erişim sağlar.

**Yapılandırma:**
```json
{
  "name": "gdrive",
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-gdrive"
  ],
  "env": {
    "GDRIVE_CLIENT_ID": "your_client_id",
    "GDRIVE_CLIENT_SECRET": "your_client_secret"
  }
}
```

---

## 🎨 Tarayıcıdan Kullanım

### MCP Sunucularını Görüntüleme

1. OpenHands'de yeni bir sohbet başlatın
2. Settings → MCP Settings'e gidin
3. Eklediğiniz tüm MCP sunucularını göreceksiniz:
   - ✅ Yeşil işaret: Aktif ve çalışıyor
   - ❌ Kırmızı işaret: Hata var
   - ⚪ Gri: Devre dışı

### MCP Araçlarını Kullanma

OpenHands otomatik olarak MCP araçlarını kullanır. Sadece normal şekilde sohbet edin:

**Örnek 1: Dosya Sistemi**
```
Sen: "Workspace'deki tüm Python dosyalarını listele"
OpenHands: [filesystem MCP kullanarak dosyaları listeler]
```

**Örnek 2: GitHub**
```
Sen: "test-app adında yeni bir GitHub repository oluştur"
OpenHands: [github MCP kullanarak repository oluşturur]
```

**Örnek 3: Web Araması**
```
Sen: "FastAPI ile authentication nasıl yapılır, araştır"
OpenHands: [brave-search MCP kullanarak arama yapar ve sonuçları özetler]
```

### Hangi MCP Aracının Kullanıldığını Görme

OpenHands sohbet sırasında hangi MCP aracını kullandığını gösterir:
- 🔧 "Using tool: filesystem_read"
- 🔧 "Using tool: github_create_repo"
- 🔧 "Using tool: brave_search"

---

## 🔍 MCP Sunucularını Test Etme

### Tarayıcıdan Test:

1. OpenHands'de yeni sohbet başlatın
2. Test komutları verin:

```
# Filesystem test
"Workspace'deki dosyaları listele"

# GitHub test (token gerekli)
"GitHub repository'lerimi göster"

# Brave Search test (API key gerekli)
"Python best practices araştır"
```

### SSH'dan Test:

```bash
# Filesystem MCP test
npx -y @modelcontextprotocol/server-filesystem /tmp

# GitHub MCP test (token ile)
GITHUB_TOKEN=ghp_xxx npx -y @modelcontextprotocol/server-github

# Brave Search test (API key ile)
BRAVE_API_KEY=xxx npx -y @modelcontextprotocol/server-brave-search
```

---

## 🐛 Sorun Giderme

### MCP Sunucusu Çalışmıyor

**1. Node.js versiyonunu kontrol edin:**
```bash
ssh ubuntu@161.118.171.201
node --version  # v20.x.x olmalı
```

**2. MCP sunucusunu manuel test edin:**
```bash
npx -y @modelcontextprotocol/server-filesystem /tmp
```

**3. OpenHands loglarını kontrol edin:**
```bash
sudo docker logs openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 | grep -i mcp
```

### Token/API Key Hataları

**GitHub Token:**
- Token'ın doğru scope'lara sahip olduğundan emin olun (`repo`, `workflow`)
- Token'ın expire olmadığını kontrol edin
- https://github.com/settings/tokens adresinden yeni token oluşturun

**Brave API Key:**
- API key'in aktif olduğundan emin olun
- Aylık limit aşılmadığını kontrol edin
- https://brave.com/search/api/ adresinden kontrol edin

### MCP Sunucusu Listede Görünmüyor

1. OpenHands'i yeniden başlatın:
```bash
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

2. Tarayıcı cache'ini temizleyin (Ctrl+Shift+R)

3. Settings → MCP Settings'i yeniden açın

---

## 📚 Popüler MCP Kombinasyonları

### Web Development Stack
```json
[
  {"name": "filesystem", ...},
  {"name": "github", ...},
  {"name": "brave-search", ...}
]
```

### Data Science Stack
```json
[
  {"name": "filesystem", ...},
  {"name": "postgres", ...},
  {"name": "brave-search", ...}
]
```

### DevOps Stack
```json
[
  {"name": "filesystem", ...},
  {"name": "docker", ...},
  {"name": "github", ...}
]
```

---

## 🎯 Best Practices

### 1. Güvenlik
- ✅ Token'ları güvenli saklayın
- ✅ Minimum gerekli scope'ları kullanın
- ✅ Token'ları düzenli olarak rotate edin
- ❌ Token'ları kod içinde hardcode etmeyin

### 2. Performans
- ✅ Sadece ihtiyacınız olan MCP sunucularını ekleyin
- ✅ Kullanılmayan sunucuları devre dışı bırakın
- ✅ API rate limit'lerini göz önünde bulundurun

### 3. Kullanım
- ✅ MCP araçlarını açık ve net komutlarla kullanın
- ✅ Hangi aracın kullanıldığını takip edin
- ✅ Hata mesajlarını okuyun ve anlayın

---

## 🚀 Hızlı Başlangıç Checklist

- [ ] SSH ile sunucuya bağlan
- [ ] Node.js kur (`bash ~/setup-mcp-servers.sh`)
- [ ] Tarayıcıda https://ai.fpvlovers.com.tr aç
- [ ] Settings → MCP Settings'e git
- [ ] Filesystem MCP ekle (token gerektirmez)
- [ ] Test et: "Workspace'deki dosyaları listele"
- [ ] GitHub token al (opsiyonel)
- [ ] GitHub MCP ekle (opsiyonel)
- [ ] Test et: "GitHub repository'lerimi göster"
- [ ] Brave API key al (opsiyonel)
- [ ] Brave Search MCP ekle (opsiyonel)
- [ ] Test et: "Python best practices araştır"

---

## 📞 Yardım

Sorun yaşarsanız:
1. [Troubleshooting Guide](TROUBLESHOOTING.md) kontrol edin
2. OpenHands loglarını inceleyin
3. MCP sunucusunu manuel test edin

---

**Son Güncelleme**: 2025-11-29
**Sunucu**: instance-hulyaekiz (161.118.171.201)

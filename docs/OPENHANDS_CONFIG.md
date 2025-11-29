# OpenHands Konfigürasyon Rehberi

## Genel Bakış
Bu rehber, Oracle Cloud sunucunuzdaki OpenHands'i nasıl yapılandıracağınızı, AI model seçimini, MCP sunucularını ve gelişmiş ayarları açıklar.

## İçindekiler
1. [OpenHands'e Erişim](#openhands-erişim)
2. [AI Model Yapılandırması](#ai-model-yapılandırması)
3. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
4. [GitHub Entegrasyonu](#github-entegrasyonu)
5. [Gelişmiş Ayarlar](#gelişmiş-ayarlar)

---

## OpenHands'e Erişim

### Web Arayüzü
- **URL**: https://ai.fpvlovers.com.tr
- **Yerel Erişim**: http://161.118.171.201:3000 (dahili)

### İlk Kurulum
1. Tarayıcınızda https://ai.fpvlovers.com.tr adresini açın
2. OpenHands arayüzünü göreceksiniz
3. Yapılandırma için ayarlar simgesine (⚙️) tıklayın

---

## AI Model Yapılandırması

### Mevcut Kurulum
Sunucunuzda Ollama üzerinden iki AI modeli yüklü:

#### 1. DeepSeek Coder V2 16B (Birincil)
- **Model ID**: `deepseek-coder-v2:16b`
- **En iyi**: Karmaşık kodlama görevleri, büyük projeler
- **Hız**: Daha yavaş ama daha doğru
- **Bellek**: ~16GB RAM gerekli

#### 2. Qwen2.5-Coder 7B (İkincil)
- **Model ID**: `qwen2.5-coder:7b`
- **En iyi**: Hızlı görevler, basit kod üretimi
- **Hız**: Hızlı ve verimli
- **Bellek**: ~7GB RAM gerekli

### Model Değiştirme

#### OpenHands UI Üzerinden:
1. **Settings** (⚙️ simgesi) tıklayın
2. **LLM Settings** bölümüne gidin
3. **Provider** seçin: `Ollama`
4. **Base URL** ayarlayın: `http://ollama:11434`
5. **Model** seçin:
   - Kapsamlı görevler için: `deepseek-coder-v2:16b`
   - Hızlı görevler için: `qwen2.5-coder:7b`
6. **Save** tıklayın

#### Coolify Environment Variables Üzerinden:
1. https://coolify.fpvlovers.com.tr adresine giriş yapın
2. AI Coding Platform uygulamasına gidin
3. **Environment Variables** sekmesine gidin
4. Güncelleyin:
   ```
   LLM_MODEL=ollama/qwen2.5-coder:7b
   ```
5. Uygulamayı yeniden başlatın

#### SSH Üzerinden (İleri Seviye):
```bash
# Sunucuya SSH ile bağlanın
ssh ubuntu@161.118.171.201

# Environment dosyasını düzenleyin
nano ~/.env

# Modeli güncelleyin
LLM_MODEL=ollama/qwen2.5-coder:7b

# OpenHands'i yeniden başlatın
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

### Model Karşılaştırması

| Özellik | DeepSeek Coder V2 16B | Qwen2.5-Coder 7B |
|---------|----------------------|------------------|
| Kod Kalitesi | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Hız | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Bellek Kullanımı | 16GB | 7GB |
| Bağlam Penceresi | Büyük | Orta |
| En İyi Kullanım | Karmaşık projeler | Hızlı düzeltmeler |

### Yeni Model Ekleme

Ollama'dan daha fazla model eklemek için:

```bash
# Sunucuya SSH ile bağlanın
ssh ubuntu@161.118.171.201

# Mevcut modelleri listeleyin
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list

# Yeni model çekin (örnek: CodeLlama)
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama pull codellama:13b

# Doğrulayın
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list
```

Popüler kodlama modelleri:
- `codellama:13b` - Meta'nın CodeLlama'sı
- `starcoder2:15b` - StarCoder2
- `mistral:7b` - Genel amaçlı
- `llama3:8b` - Meta'nın Llama 3'ü

---

## Model Context Protocol (MCP)

MCP, OpenHands'in harici araçlar ve servisler kullanmasını sağlayan açık bir standarttır. [modelcontextprotocol.io](https://modelcontextprotocol.io) standardına dayanır.

### MCP Nedir?

Model Context Protocol şunları sağlar:
- **Dosya Sistemi Erişimi**: Dosya okuma/yazma
- **Veritabanı Bağlantıları**: Veritabanı sorguları
- **API Entegrasyonları**: Harici API çağrıları
- **Özel Araçlar**: Kendi araçlarınızı ekleyin

### MCP Nasıl Çalışır?

OpenHands başladığında:
1. MCP yapılandırmasını okur
2. Yapılandırılmış sunuculara bağlanır (SSE, SHTTP veya stdio)
3. Bu sunucular tarafından sağlanan araçları agent'a kaydeder
4. Çalışma sırasında araç çağrılarını uygun MCP sunucularına yönlendirir

### MCP Destek Matrisi

| Platform | Destek Seviyesi | Yapılandırma Yöntemi |
|----------|----------------|---------------------|
| **CLI** | ✅ Tam Destek | `~/.openhands/mcp.json` dosyası |
| **SDK** | ✅ Tam Destek | Programatik yapılandırma |
| **Local GUI** | ✅ Tam Destek | Settings UI + config dosyaları |
| **OpenHands Cloud** | ✅ Tam Destek | Cloud UI ayarları |

### MCP Sunucularını Yapılandırma

#### OpenHands UI Üzerinden (Local GUI):

1. **Settings** (⚙️) → **MCP Settings** gidin
2. **Add MCP Server** tıklayın
3. Sunucu detaylarını yapılandırın
4. **Save** tıklayın

#### CLI Üzerinden:

MCP yapılandırması `~/.openhands/mcp.json` dosyasında saklanır:

```bash
# Sunucuda MCP config dosyası oluşturun
ssh ubuntu@161.118.171.201

# MCP dizini oluşturun
mkdir -p ~/.openhands

# MCP config dosyası oluşturun
nano ~/.openhands/mcp.json
```

**Örnek mcp.json:**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/workspace"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Yaygın MCP Sunucuları:

**1. Dosya Sistemi Sunucusu**
```json
{
  "name": "filesystem",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/workspace"],
  "env": {}
}
```

**2. GitHub Sunucusu**
```json
{
  "name": "github",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_TOKEN": "github_tokeniniz_buraya"
  }
}
```

**3. PostgreSQL Sunucusu**
```json
{
  "name": "postgres",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-postgres"],
  "env": {
    "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@host:5432/db"
  }
}
```

**4. Brave Search Sunucusu**
```json
{
  "name": "brave-search",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-brave-search"],
  "env": {
    "BRAVE_API_KEY": "brave_api_keyiniz"
  }
}
```

### Sunucuya MCP Sunucularını Kurma

MCP sunucuları ayrı süreçler olarak çalışır. Kurmak için:

```bash
# Sunucuya SSH ile bağlanın
ssh ubuntu@161.118.171.201

# Node.js yoksa kurun
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Kurulumu doğrulayın
node --version
npm --version

# MCP sunucusunu test edin
npx -y @modelcontextprotocol/server-filesystem /tmp
```

---

## GitHub Entegrasyonu

### GitHub Token Kurulumu

#### 1. Personal Access Token Oluşturma

1. https://github.com/settings/tokens adresine gidin
2. **Generate new token** → **Generate new token (classic)** tıklayın
3. **Expiration** ayarlayın: 90 gün
4. **Scopes** seçin:
   - ✅ `repo` (Özel depoların tam kontrolü)
   - ✅ `workflow` (GitHub Action workflow'larını güncelleme)
5. **Generate token** tıklayın
6. **Token'ı hemen kopyalayın!**

#### 2. OpenHands'de Yapılandırma

**UI Üzerinden:**
1. OpenHands Settings açın
2. **Integrations Settings** gidin
3. **GitHub** bölümünü bulun
4. Token'ınızı yapıştırın
5. **Save** tıklayın

**Coolify Üzerinden:**
1. https://coolify.fpvlovers.com.tr adresine giriş yapın
2. AI Coding Platform'a gidin
3. **Environment Variables** gidin
4. Ekleyin/Güncelleyin:
   ```
   GITHUB_TOKEN=ghp_tokeniniz_buraya
   ```
5. Uygulamayı yeniden başlatın

**SSH Üzerinden:**
```bash
# Sunucuya SSH ile bağlanın
ssh ubuntu@161.118.171.201

# Environment düzenleyin
nano ~/.env

# Token ekleyin
GITHUB_TOKEN=ghp_tokeniniz_buraya

# OpenHands'i yeniden başlatın
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

---

## Gelişmiş Ayarlar

### Uygulama Ayarları

#### 1. Güvenlik Modu
- **Confirmation Mode**: Komutları çalıştırmadan önce onay ister
- **Safe Mode**: Tehlikeli işlemleri kısıtlar
- **Full Access**: Kısıtlama yok (dikkatli kullanın)

**Yapılandırma:**
1. Settings → **Application Settings**
2. **Security Mode** seçin
3. Tercihinizi seçin

#### 2. Agent Yapılandırması

**Agent Tipi:**
- `CodeActAgent` (Varsayılan): Kodlama görevleri için en iyi
- `PlannerAgent`: Karmaşık çok adımlı görevler için daha iyi

**Maksimum İterasyon:**
- Varsayılan: 100
- Aralık: 10 - 500
- Amaç: Agent'ın atabileceği maksimum adım

**Yapılandırma:**
```bash
# Environment variables üzerinden
AGENT_TYPE=CodeActAgent
MAX_ITERATIONS=100
```

---

## Hızlı Referans

### Temel Komutlar

```bash
# Sistem sağlığını kontrol et
bash ~/health-check-system.sh

# OpenHands loglarını görüntüle
sudo docker logs -f openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# OpenHands'i yeniden başlat
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Mevcut modelleri kontrol et
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list

# Ollama'yı test et
curl http://localhost:11434/api/tags
```

### Önemli URL'ler

- **OpenHands UI**: https://ai.fpvlovers.com.tr
- **Coolify Dashboard**: https://coolify.fpvlovers.com.tr
- **GitHub Tokens**: https://github.com/settings/tokens
- **OpenHands Docs**: https://docs.openhands.dev

---

## Sonraki Adımlar

1. **Tercih ettiğiniz AI modelini yapılandırın**
2. **GitHub entegrasyonunu kurun** (gerekirse)
3. **Ek yetenekler için MCP sunucuları ekleyin**
4. **OpenHands ile ilk projenizi başlatın**
5. **Rahat ettikçe gelişmiş özellikleri keşfedin**

Daha fazla yardım için:
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Configuration Reference](CONFIGURATION_REFERENCE.md)
- [Maintenance Procedures](MAINTENANCE.md)

---
**Son Güncelleme**: 2025-11-29
**Sunucu**: instance-hulyaekiz (161.118.171.201)

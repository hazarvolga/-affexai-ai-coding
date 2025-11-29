# Mevcut Durum - OpenHands & MCP Kurulumu

**Tarih:** 2025-11-29  
**Sunucu:** instance-hulyaekiz (161.118.171.201)  
**OpenHands URL:** https://ai-code.affexai.tr

---

## ✅ Tamamlanan İşlemler

### 1. Node.js Kurulumu
- ✅ Node.js v20.19.6 sunucuda kurulu
- ✅ npm v10.8.2 çalışıyor
- ✅ npx v10.8.2 çalışıyor

### 2. MCP Spec Güncellemesi
- ✅ Requirements.md'ye Requirement 11 eklendi (MCP entegrasyonu)
- ✅ Design.md'ye MCP mimarisi ve yapılandırmaları eklendi
- ✅ Tasks.md'ye Task 11 eklendi (8 alt görev)
- ✅ MCP_BROWSER_CONFIG.md oluşturuldu (tarayıcıdan yapılandırma rehberi)

### 3. MCP Kurulum Scripti
- ✅ scripts/setup-mcp-servers.sh güncellendi
- ✅ 6 modern MCP sunucusu için kurulum desteği eklendi:
  - Filesystem
  - GitHub
  - Brave Search
  - Docker
  - PostgreSQL
  - SQLite

### 4. OpenHands Yapılandırması
- ✅ OpenHands redeploy edildi (Coolify üzerinden)
- ✅ LLM Provider yapılandırması tamamlandı:
  - Provider: Ollama
  - Base URL: `http://ollama:11434`
  - Model: `qwen2.5-coder:7b-instruct`
  - API Key: Boş (gerekmiyor)

---

## ⚠️ Devam Eden Sorunlar

### 1. Runtime Başlatma Sorunu
**Durum:** OpenHands runtime container'ı başlatamıyor

**Hata:**
```
httpx.ConnectError: [Errno -2] Name or service not known
```

**Sebep:** OpenHands ve Runtime container'ları farklı Docker network'lerde olabilir

**Çözüm Adımları:**
1. Container network'lerini kontrol et
2. Her iki container'ı da aynı network'e ekle
3. Veya Coolify'da OpenHands yapılandırmasını düzenle

### 2. MCP Yapılandırması Beklemede
**Durum:** MCP sunucuları henüz OpenHands'e eklenmedi

**Sebep:** Önce runtime sorununu çözmemiz gerekiyor

**Yapılacaklar:**
1. Runtime sorunu çözüldükten sonra
2. Settings → MCP Settings'e git
3. Filesystem MCP'yi ekle:
   ```json
   {
     "name": "filesystem",
     "command": "npx",
     "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
     "env": {}
   }
   ```
4. Test et: "Workspace'deki dosyaları listele"

---

## 🔧 Sonraki Adımlar

### Öncelik 1: Runtime Sorununu Çöz
```bash
# Container'ları kontrol et
ssh ubuntu@161.118.171.201
sudo docker ps | grep openhands
sudo docker network ls
sudo docker inspect <openhands-container-id> | grep Networks
sudo docker inspect <runtime-container-id> | grep Networks

# Aynı network'e ekle (gerekirse)
sudo docker network connect <network-name> <container-id>
```

### Öncelik 2: MCP Entegrasyonu
1. Filesystem MCP'yi ekle (token gerektirmez)
2. Test et
3. GitHub MCP ekle (token gerekli)
4. Brave Search MCP ekle (API key gerekli)

### Öncelik 3: Dokümantasyon
1. Çözülen sorunları dokümante et
2. MCP kullanım örnekleri ekle
3. Troubleshooting guide güncelle

---

## 📋 Önemli Bilgiler

### Container İsimleri
- **OpenHands:** `openhands-kogccog8g0ok80w0kgcoc4ck-112840198537`
- **Runtime:** `openhands-runtime-<dynamic-id>` (her conversation için yeni)
- **Ollama:** `ollama-kogccog8g0ok80w0kgcoc4ck-112840189768`

### Network Bilgileri
- **Docker Network:** `ai-coding-network` (veya Coolify default network)
- **Ollama Internal URL:** `http://ollama:11434`
- **Workspace Path (Runtime içinde):** `/workspace`

### Yapılandırma Dosyaları
- **MCP Rehberi:** `docs/MCP_BROWSER_CONFIG.md`
- **Setup Script:** `scripts/setup-mcp-servers.sh`
- **Spec Dosyaları:** `.kiro/specs/self-hosted-ai-coding-platform/`

---

## 🐛 Bilinen Hatalar

### 1. Session Metadata Hatası (Çözüldü)
**Hata:** `No such file or directory: /.openhands/sessions/.../metadata.json`  
**Çözüm:** Session dizini temizlendi: `rm -rf /.openhands/sessions/*`

### 2. Gateway Timeout (Çözüldü)
**Hata:** 504 Gateway Timeout  
**Çözüm:** OpenHands container restart edildi

### 3. 500 Internal Server Error (Çözüldü)
**Hata:** Request failed with status code 500  
**Çözüm:** Session cache temizlendi ve container restart edildi

---

## 📞 Yardım

**Logları Kontrol Et:**
```bash
# OpenHands logs
sudo docker logs --tail 100 openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Runtime logs
sudo docker logs --tail 100 <runtime-container-id>

# Ollama logs
sudo docker logs --tail 100 ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
```

**Container Durumu:**
```bash
sudo docker ps | grep openhands
sudo docker stats --no-stream
```

**Coolify Dashboard:**
- URL: https://coolify.fpvlovers.com.tr
- Project: affexai-ai-coding
- Service: openhands

---

**Son Güncelleme:** 2025-11-29 20:45 UTC

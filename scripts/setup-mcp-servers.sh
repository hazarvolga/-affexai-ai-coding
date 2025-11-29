#!/bin/bash
# MCP Servers Setup Script
# This script installs Node.js and modern MCP servers for OpenHands

set -e

echo "🚀 Modern MCP Sunucuları Kurulum Scripti"
echo "========================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "📦 Node.js 20.x LTS kuruluyor..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
    echo "✅ Node.js kuruldu: $(node --version)"
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js zaten kurulu: $NODE_VERSION"
fi

echo ""
echo "📋 NPM versiyonu: $(npm --version)"
echo "📋 NPX versiyonu: $(npx --version)"
echo ""

# Install MCP servers globally for better performance
echo "📦 Modern MCP Sunucularını Global Olarak Kuruyoruz..."
echo ""

MCP_SERVERS=(
    "@modelcontextprotocol/server-filesystem"
    "@modelcontextprotocol/server-github"
    "@modelcontextprotocol/server-brave-search"
    "@modelcontextprotocol/server-docker"
    "@modelcontextprotocol/server-postgres"
    "@modelcontextprotocol/server-sqlite"
)

for server in "${MCP_SERVERS[@]}"; do
    echo "Installing $server..."
    npm install -g "$server" --silent || echo "⚠️  $server kurulumunda sorun oldu"
done

echo ""
echo "🧪 MCP Sunucularını Test Ediyoruz..."
echo ""

echo "1. 📁 Filesystem MCP Server:"
if npx -y @modelcontextprotocol/server-filesystem --help &> /dev/null; then
    echo "   ✅ Dosya okuma/yazma işlemleri hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "2. 🐙 GitHub MCP Server:"
if npx -y @modelcontextprotocol/server-github --help &> /dev/null; then
    echo "   ✅ GitHub işlemleri hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "3. 🔍 Brave Search MCP Server:"
if npx -y @modelcontextprotocol/server-brave-search --help &> /dev/null; then
    echo "   ✅ Web araması hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "4. 🐳 Docker MCP Server:"
if npx -y @modelcontextprotocol/server-docker --help &> /dev/null; then
    echo "   ✅ Container yönetimi hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "5. 🐘 PostgreSQL MCP Server:"
if npx -y @modelcontextprotocol/server-postgres --help &> /dev/null; then
    echo "   ✅ PostgreSQL sorguları hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "6. 💾 SQLite MCP Server:"
if npx -y @modelcontextprotocol/server-sqlite --help &> /dev/null; then
    echo "   ✅ SQLite sorguları hazır"
else
    echo "   ⚠️  Test edilemedi"
fi

echo ""
echo "========================================="
echo "✅ MCP Sunucuları Kurulumu Tamamlandı!"
echo ""
echo "🎯 Kurulu MCP Sunucuları:"
echo "   📁 Filesystem - Dosya işlemleri"
echo "   🐙 GitHub - Repo yönetimi"
echo "   🔍 Brave Search - Web araması"
echo "   🐳 Docker - Container yönetimi"
echo "   🐘 PostgreSQL - Veritabanı sorguları"
echo "   💾 SQLite - Hafif veritabanı"
echo ""
echo "📝 Sonraki Adımlar:"
echo "1. Tarayıcıdan OpenHands'i açın: https://ai.fpvlovers.com.tr"
echo "2. Settings (⚙️) → MCP Settings tıklayın"
echo "3. 'Add MCP Server' ile sunucuları ekleyin"
echo ""
echo "💡 Örnek Yapılandırmalar için: docs/MCP_SETUP_GUIDE.md"
echo ""

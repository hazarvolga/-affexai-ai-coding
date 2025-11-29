# DNS Configuration for OpenHands

## Overview

This document provides step-by-step instructions for configuring DNS records to point the OpenHands subdomain to your Oracle Cloud instance.

## Prerequisites

- Access to your DNS provider's control panel
- Domain: fpvlovers.com.tr
- Oracle Cloud instance IP: 161.118.171.201

## DNS Configuration Steps

### Step 1: Access Your DNS Provider

1. Log in to your DNS provider's control panel (e.g., GoDaddy, Cloudflare, Namecheap, etc.)
2. Navigate to the DNS management section for fpvlovers.com.tr

### Step 2: Create A Record for OpenHands Subdomain

Create a new DNS A record with the following configuration:

| Field | Value |
|-------|-------|
| Type | A |
| Name/Host | ai |
| Value/Points to | 161.118.171.201 |
| TTL | 3600 (or Auto) |

**Example configurations for common DNS providers:**

**Cloudflare:**
- Type: A
- Name: ai
- IPv4 address: 161.118.171.201
- Proxy status: DNS only (gray cloud)
- TTL: Auto

**GoDaddy:**
- Type: A
- Host: ai
- Points to: 161.118.171.201
- TTL: 1 Hour

**Namecheap:**
- Type: A Record
- Host: ai
- Value: 161.118.171.201
- TTL: Automatic

### Step 3: Verify DNS Record

After creating the A record, verify it was added correctly in your DNS provider's interface. The record should show:

```
ai.fpvlovers.com.tr → 161.118.171.201
```

### Step 4: Wait for DNS Propagation

DNS changes can take time to propagate across the internet:

- **Minimum wait time:** 5-10 minutes
- **Typical propagation time:** 1-4 hours
- **Maximum propagation time:** 24-48 hours (rare)

The TTL (Time To Live) value affects how quickly changes propagate. Lower TTL values (e.g., 300 seconds) propagate faster.

### Step 5: Check DNS Propagation

Use the following methods to verify DNS propagation:

**Method 1: Using dig command (Linux/Mac)**
```bash
dig ai.fpvlovers.com.tr

# Expected output should include:
# ai.fpvlovers.com.tr.    3600    IN    A    161.118.171.201
```

**Method 2: Using nslookup command (Windows/Linux/Mac)**
```bash
nslookup ai.fpvlovers.com.tr

# Expected output:
# Name:    ai.fpvlovers.com.tr
# Address: 161.118.171.201
```

**Method 3: Using online DNS checker**
- Visit: https://dnschecker.org/
- Enter: ai.fpvlovers.com.tr
- Check that multiple locations resolve to 161.118.171.201

**Method 4: Using ping command**
```bash
ping ai.fpvlovers.com.tr

# Should show: PING ai.fpvlovers.com.tr (161.118.171.201)
```

### Step 6: Verify from Oracle Instance

SSH into your Oracle Cloud instance and verify the DNS resolution:

```bash
ssh ubuntu@161.118.171.201

# Once connected, test DNS resolution
nslookup ai.fpvlovers.com.tr
dig ai.fpvlovers.com.tr
```

## Troubleshooting

### DNS Not Resolving

**Problem:** DNS lookup fails or returns wrong IP

**Solutions:**
1. Double-check the A record configuration in your DNS provider
2. Ensure you saved the changes in your DNS control panel
3. Wait longer for propagation (up to 24 hours)
4. Clear your local DNS cache:
   - **Linux:** `sudo systemd-resolve --flush-caches`
   - **Mac:** `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
   - **Windows:** `ipconfig /flushdns`

### Partial Propagation

**Problem:** DNS resolves in some locations but not others

**Solutions:**
1. This is normal during propagation - wait longer
2. Use https://dnschecker.org/ to monitor global propagation
3. Check that your DNS provider's nameservers are responding

### Wrong IP Address

**Problem:** DNS resolves to incorrect IP address

**Solutions:**
1. Verify the A record points to 161.118.171.201
2. Check for conflicting DNS records (CNAME, other A records)
3. Remove any old/incorrect records
4. Wait for DNS cache to expire (based on TTL)

## Next Steps

Once DNS propagation is complete and verified:

1. Proceed to configure Coolify to route the subdomain to OpenHands
2. Set up SSL certificate with Let's Encrypt
3. Test HTTPS access to ai.fpvlovers.com.tr

## Security Considerations

- **DNS Security:** Consider enabling DNSSEC if your provider supports it
- **DDoS Protection:** If using Cloudflare, you can enable proxy (orange cloud) after initial setup
- **Monitoring:** Set up DNS monitoring to alert on changes or failures

## References

- [DNS Propagation Checker](https://dnschecker.org/)
- [What is DNS?](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [Understanding DNS Records](https://www.cloudflare.com/learning/dns/dns-records/)

# EVOLUTION API — ORACLE CLOUD INSTALL GUIDE
# One-time setup on the Always Free instance

## STEP 1 — Provision Oracle Cloud (Always Free)
1. Go to cloud.oracle.com → Create Free Account
2. Spin up: VM.Standard.A1.Flex
   - 4 OCPUs, 24GB RAM (max Always Free allocation)
   - OS: Ubuntu 22.04 (Canonical)
   - Shape: ARM (Ampere)
3. Open ports in Security List:
   - 8080 (Evolution API)
   - 5432 (Postgres — internal only, keep closed to internet)
   - 6379 (Redis — internal only)
   - 22 (SSH)

## STEP 2 — SSH Into the Box
ssh ubuntu@YOUR_ORACLE_IP

## STEP 3 — Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
newgrp docker

## STEP 4 — Deploy Evolution API
git clone https://github.com/kevinleestites2-dev/evolution-deploy
cd evolution-deploy
cp .env.example .env
nano .env
# Set POSTGRES_PASSWORD and REDIS_PASSWORD to strong values
# Set EVOLUTION_API_KEY to your secret key
# Set SERVER_URL to http://YOUR_ORACLE_IP:8080

docker compose up -d

## STEP 5 — Connect WhatsApp Number
# Get QR code:
python3 pantheon_messenger.py qr

# OR hit the API directly:
curl http://YOUR_ORACLE_IP:8080/instance/connect/pantheon \
  -H "apikey: YOUR_API_KEY"

# Scan the QR with WhatsApp on the number you want to connect
# Check connection:
python3 pantheon_messenger.py status

## STEP 6 — Wire All Primes
# Add to every Prime's .env:
EVOLUTION_URL=http://YOUR_ORACLE_IP:8080
EVOLUTION_API_KEY=YOUR_API_KEY
EVOLUTION_INSTANCE=pantheon
FORGEMASTER_NUMBER=19189007206

# Then import in any Prime:
from pantheon_messenger import alert_forgemaster, scout_deal_alert

## FIREWALL (OCI Security List)
# Only open 8080 to your IP or keep it internal
# All Primes on same Oracle box talk via localhost — no public exposure needed

## HEALTH CHECK
curl http://localhost:8080/
# Should return: {"status":"Server is running","version":"x.x.x"}

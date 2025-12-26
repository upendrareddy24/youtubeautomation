# Oracle Cloud Deployment Guide

This guide will help you move your **Viral YouTube Shorts Automator** to an **Oracle Cloud Always Free** instance.

## 1. Create VM Instance
1.  Log in to Oracle Cloud.
2.  Go to **Compute > Instances > Create Instance**.
3.  **Image**: Canonical Ubuntu 22.04 (or 24.04).
4.  **Shape**: VM.Standard.A1.Flex (Ampere ARM) - *Highly recommended as it's free and powerful (4 OCPU, 24GB RAM).*
5.  **SSH Keys**: Save your Private Key (`.key`)! You need this to log in.

## 2. Ingress Rules (Enable Port 5000)
By default, the firewall blocks everything.
1.  Go to your Instance details.
2.  Click the **Subnet** link.
3.  Click the **Security List** (e.g., Default Security List).
4.  **Add Ingress Rule**:
    - Source CIDR: `0.0.0.0/0`
    - Destination Port Range: `5000` (for the Dashboard)
    - Protocol: TCP

## 3. Transfer Files
You need to move your code to the server. You can use an SFTP client (like FileZilla) or `scp`.

**Using SCP (Terminal):**
```bash
# Run this from your local folder containing the code
scp -i path/to/your/private.key -r . ubuntu@<YOUR_VM_IP>:/home/ubuntu/youtube_shorts_automator
```

## 4. Install & Setup
SSH into your server:
```bash
ssh -i path/to/your/private.key ubuntu@<YOUR_VM_IP>
```

Go to the folder and run the installer:
```bash
cd youtube_shorts_automator
chmod +x oracle_install.sh
./oracle_install.sh
```
*This will install Python, FFmpeg, ImageMagick, and all dependencies.*

## 5. Start the Dashboard (Background Service)
To keep the web dashboard running even when you disconnect:

1.  **Edit the service file** (if needed):
    `nano youtube_bot.service`
    *Check that the paths `/home/ubuntu/youtube_shorts_automator` match where you uploaded files.*

2.  **Enable the service**:
    ```bash
    sudo cp youtube_bot.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable youtube_bot
    sudo systemctl start youtube_bot
    ```

3.  Access your dashboard at: `http://<YOUR_VM_IP>:5000`

## 6. Automate Daily Videos (Cron)
Your bot needs to run automatically every day.

1.  Open crontab:
    ```bash
    crontab -e
    ```

2.  Add this line to run everyday at 10:00 AM:
    ```bash
    0 10 * * * cd /home/ubuntu/youtube_shorts_automator && ./venv/bin/python main_pipeline.py >> pipeline_cron.log 2>&1
    ```

## Troubleshooting
- **Logs**: Check `pipeline_log.txt` or `pipeline_cron.log`.
- **Permissions**: Ensure `chmod +x` is run on scripts.
- **Firewall (Internal)**: You might need to open the port on Ubuntu itself:
    ```bash
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
    sudo netfilter-persistent save
    ```

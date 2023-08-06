import subprocess
import urllib.parse
import urllib.request
import time
from socket import gethostname,gethostbyname
import smtplib
from email.message import EmailMessage

# You can find the bot token and chat id on: https://bluenickel.sharepoint.com/:x:/r/_layouts/15/Doc.aspx?sourcedoc=%7B4B85D1DB-87C0-472F-91C9-27EA70195A71%7D&file=BNS_Telegram_Bots_and_Groups.xlsx&action=default&mobileredirect=true
class QuickMonitorTelegram:
    def __init__(self,telegram_bot_token,telegram_chat_id,service_list,freq):
        # Telegram Bot token and chat ID
        self.token = telegram_bot_token
        self.chat_id = telegram_chat_id
        # Service names to monitor
        self.services = service_list        
        self.machine_ip = gethostbyname(gethostname())
        # Command to check if the service is running
        while True:
            stopped = self.check_services()
            if len(stopped) > 0:
               service_str = ", ".join(str(x) for x in stopped)
               message = f"The following services have stopped on machine {self.machine_ip}:\n" + service_str
               self.send_telegram_message(message)
            time.sleep(freq)  # Execute the task every freq seconds  

    # Send message to Telegram
    def send_telegram_message(self,message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        data = urllib.parse.urlencode(data)
        data = data.encode("utf-8")
        urllib.request.Request(url, data)        

    def check_services(self):
        stopped_services = []        
        for service in self.services:
            try:
                CHECK_COMMAND = f"systemctl is-active {service}"
                # Run the command to check if the service is running
                result = subprocess.check_output(f'sc query "{service}"', shell=True, text=True)
                # If the service is not active, append it to the list
                if not "RUNNING" in result:
                    stopped_services.append(service)                
            except:
                pass
        return stopped_services
    
class QuickMonitorTeams:
    def __init__(self,smtp_server, smtp_port, smtp_user, smtp_password,service_list,freq):
        # SMTP server details
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smptp_user = smtp_user
        self.smtp_password = smtp_password
        #user with power automate flow
        self.to = "james@bluenickel.co.za"
        #subject that tirggers outlook rule
        self.subject = "Power Automate Service Monitor Mail"
        # Service names to monitor
        self.services = service_list        
        self.machine_ip = gethostbyname(gethostname())
        # Command to check if the service is running
        while True:
            stopped = self.check_services()
            if len(stopped) > 0:
               service_str = ", ".join(str(x) for x in stopped)
               body = f"The following services have stopped on machine {self.machine_ip}:\n" + service_str
               self.send_email(body)
            time.sleep(freq)  # Execute the task every freq seconds  

    def send_email(self,body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = self.subject
        msg['From'] = self.smptp_user
        msg['To'] = self.to
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)            
        except Exception as e:
            #maybe write the error to a log??
            pass
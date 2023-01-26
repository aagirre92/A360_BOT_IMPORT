# INTRODUCTION
This script allows you to import bots from certain folder to your A360 Control Room
# USAGE (powershell)
You must provide 4 parameters:
* **cr_url**: Full Control Room URL, e.g. https://aa1-app2019.iacc.epam.com
* **username**: Username from Control Room
* **api_key**: API key for authenticating with that user
* **folder_path**: Full path of the folder where the bot exports are located
```
.\main.py --cr_url="https://aa1-app2019.iacc.epam.com" --username="andoni_aguirre_aranguren" --api_key="123456" --folder_path="C:\Users\Andoni_Aguirre_Arang\Desktop\BOT EXPORT FOLDER"

```
# LOGS
This script will create a log file under users's Documents folder named _A360_BOT_IMPORT_LOGS_dd-MMM-yyyy.log_
from tobrot.sample_config import Config

#Fill your all data, read readme for reference

#FOR CUSTOM COMMANDS READ REAME AND FILL THEM...

class Config(Config):
    TG_BOT_TOKEN= "1268fill---your----data"
    APP_ID = 1373938
    API_HASH = "fill--your--data"
    OWNER_ID = 12537936
    AUTH_CHANNEL = [-10082786282972]
    DESTINATION_FOLDER = "TorrentLeech-Gdrive" #Name of your folder read readme(not id of the folder)
    #fill your rclone config like this(Your config may have some extra value or less. so Don't worry)
    # Do not delete [DRIVE] #do not delete [DRIVE] but replace remaining part
    RCLONE_CONFIG = """
[DRIVE]
type = drive
client_id = 28dslkgjsdl-fill-your-details-apps.googleusercontent.com
client_secret = 6Tib48-fill-your-details-KuXXDX-eWgnRBYc
scope = drive
root_folder_id =
token = {"access_token":"ya29.a-fill-your-details-af4ychuHswBt8X0nf2oWmczsHg6MYPSE6hXo-PJ-fill-your-details-s06KAecfw_H-tYThBtbs:20:25.430920315Z"}
team_drive = 0AB0q-fill-your-details-sdrgsgsdUk9PVA
"""
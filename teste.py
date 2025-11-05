import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SERVICE_ACCOUNT_FILE = r"credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_ID = "17G-oV9e6PMOsV6RyEZn5k6aWMTFxAjjR"

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    return service


def sobe_arquivo(local_path, name=None, folder_id=FOLDER_ID):
    """
    Envia um arquivo local para o Google Drive na pasta especificada
    e retorna o link público e o id do arquivo.
    """
    service = get_drive_service()
    mime_type = mimetypes.guess_type(local_path)[0] or "application/octet-stream"

    file_metadata = {
        "name": name or local_path.split("/")[-1],
        "parents": [folder_id],
    }

    media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, name, webViewLink")
        .execute()
    )

    # Tornar o arquivo público (opcional, ver abaixo)
    #service.permissions().create(
    #    fileId=file["id"],
    #    body={"role": "reader", "type": "anyone"},
    #).execute()

    # Pegar link de visualização
    file = (
        service.files()
        .get(fileId=file["id"], fields="id, name, webViewLink, webContentLink")
        .execute()
    )

    return {
        "id": file["id"],
        "name": file["name"],
        "view_link": file.get("webViewLink"),
        "download_link": file.get("webContentLink"),
    }

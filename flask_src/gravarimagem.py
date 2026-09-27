import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


def upload_imagem(arquivo, pasta="patatino/animais"):
    """Faz upload de uma imagem para o Cloudinary.
    Retorna (url, public_id) ou (None, None) em caso de erro.
    """
    try:
        resultado = cloudinary.uploader.upload(
            arquivo,
            folder=pasta,
            resource_type="image",
        )
        return resultado["secure_url"], resultado["public_id"]
    except Exception as e:
        print(f"❌ Erro no upload Cloudinary: {e}")
        return None, None


def excluir_imagem(public_id):
    """Remove uma imagem do Cloudinary pelo public_id."""
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print(f"❌ Erro ao excluir imagem Cloudinary: {e}")

"""
ImagemService — encapsula toda comunicação com o Cloudinary.
Nenhuma outra classe importa cloudinary diretamente.
"""
import os
from typing import Tuple, Optional
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


class ImagemService:
    """Responsável por upload e exclusão de imagens no Cloudinary."""

    def upload(
        self, arquivo, pasta: str = "patatino"
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Faz upload de uma imagem.
        Retorna (url_segura, public_id) ou (None, None) em caso de erro.
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

    def excluir(self, public_id: str) -> bool:
        """
        Remove uma imagem pelo public_id.
        Retorna True se bem-sucedido.
        """
        try:
            cloudinary.uploader.destroy(public_id)
            return True
        except Exception as e:
            print(f"❌ Erro ao excluir imagem Cloudinary: {e}")
            return False

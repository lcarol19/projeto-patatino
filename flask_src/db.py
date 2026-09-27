import os
import tempfile
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def _get_ssl_path():
    """
    Retorna o caminho do certificado SSL.
    Prioridade:
    1. Variável CA_CERT_CONTENT (Render) — cria arquivo temporário
    2. Arquivo ca.pem local (desenvolvimento)
    """
    # Render: conteúdo do certificado como variável de ambiente
    ca_content = os.getenv("CA_CERT_CONTENT")
    if ca_content:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".pem", delete=False
        )
        tmp.write(ca_content)
        tmp.close()
        return tmp.name

    # Local: arquivo ca.pem na mesma pasta
    ssl_ca = os.getenv("SSL_CA")
    if ssl_ca:
        ssl_path = Path(__file__).parent / ssl_ca
        if ssl_path.exists():
            return str(ssl_path)

    return None


def conectar():
    """Abre e retorna uma conexão com o banco MySQL (Aiven)."""
    try:
        ssl_path = _get_ssl_path()

        params = dict(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            connection_timeout=30,
            autocommit=False,
        )

        if ssl_path:
            params["ssl_disabled"] = False
            params["ssl_ca"] = ssl_path

        conn = mysql.connector.connect(**params)
        conn.ping(reconnect=True, attempts=3, delay=2)
        return conn

    except mysql.connector.Error as erro:
        print(f"❌ Erro ao conectar ao banco: {erro}")
        return None


if __name__ == "__main__":
    conn = conectar()
    if conn:
        print("✅ Conectado com sucesso!")
        conn.close()

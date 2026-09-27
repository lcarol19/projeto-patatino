"""
criar_banco.py — cria as tabelas no banco defaultdb do Aiven
Execute: python criar_banco.py
"""
from db import conectar

conn   = conectar()
cursor = conn.cursor()

# Verifica em qual banco estamos
cursor.execute("SELECT DATABASE()")
banco_atual = cursor.fetchone()[0]
print(f"✅ Conectado ao banco: {banco_atual}")

# Lista de comandos SQL separados
comandos = [
    # Espécies
    """CREATE TABLE IF NOT EXISTS especies (
        id_especie INT AUTO_INCREMENT PRIMARY KEY,
        descricao  VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO especies (id_especie, descricao) VALUES (1,'Cachorro'),(2,'Gato'),(3,'Outro')",

    # Portes
    """CREATE TABLE IF NOT EXISTS portes (
        id_porte  INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO portes (id_porte, descricao) VALUES (1,'Pequeno'),(2,'Médio'),(3,'Grande')",

    # Status animal
    """CREATE TABLE IF NOT EXISTS status_animal (
        id_status INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO status_animal (id_status, descricao) VALUES (1,'Para adoção'),(2,'Adotado'),(3,'Em tratamento'),(4,'Óbito')",

    # Status adoção
    """CREATE TABLE IF NOT EXISTS status_adocao (
        id_status INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO status_adocao (id_status, descricao) VALUES (1,'Em análise'),(2,'Aprovada'),(3,'Recusada'),(4,'Cancelada'),(5,'Concluída')",

    # Tipos de moradia
    """CREATE TABLE IF NOT EXISTS tipos_moradia (
        id_tipo   INT AUTO_INCREMENT PRIMARY KEY,
        descricao VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO tipos_moradia (id_tipo, descricao) VALUES (1,'Casa'),(2,'Apartamento'),(3,'Sítio'),(4,'Comércio'),(5,'Outros')",

    # Resultado visita
    """CREATE TABLE IF NOT EXISTS resultado_visita (
        id_resultado INT AUTO_INCREMENT PRIMARY KEY,
        descricao    VARCHAR(50) NOT NULL
    ) ENGINE=InnoDB""",

    "INSERT IGNORE INTO resultado_visita (id_resultado, descricao) VALUES (1,'Ok'),(2,'Preocupante'),(3,'Retorno necessário')",

    # Animais
    """CREATE TABLE IF NOT EXISTS animais (
        id_animal        INT AUTO_INCREMENT PRIMARY KEY,
        nome             VARCHAR(100) NOT NULL,
        id_especie       INT NOT NULL,
        id_porte         INT NOT NULL,
        id_status        INT NOT NULL DEFAULT 1,
        sexo             ENUM('Macho','Fêmea','Não informado') NOT NULL DEFAULT 'Não informado',
        idade_aproximada INT NULL,
        codigo_chip      VARCHAR(50) NULL,
        temperamento     VARCHAR(255) NULL,
        descricao        TEXT NULL,
        observacoes      TEXT NULL,
        data_cadastro    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_atualizacao DATETIME NULL ON UPDATE CURRENT_TIMESTAMP,
        CONSTRAINT fk_animal_especie FOREIGN KEY (id_especie) REFERENCES especies(id_especie),
        CONSTRAINT fk_animal_porte   FOREIGN KEY (id_porte)   REFERENCES portes(id_porte),
        CONSTRAINT fk_animal_status  FOREIGN KEY (id_status)  REFERENCES status_animal(id_status)
    ) ENGINE=InnoDB""",

    # Fotos animais
    """CREATE TABLE IF NOT EXISTS fotos_animais (
        id_foto       INT AUTO_INCREMENT PRIMARY KEY,
        id_animal     INT NOT NULL,
        url_foto      VARCHAR(500) NOT NULL,
        id_cloudinary VARCHAR(255) NULL,
        ordem         INT NOT NULL DEFAULT 1,
        data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_foto_animal FOREIGN KEY (id_animal)
            REFERENCES animais(id_animal) ON DELETE CASCADE
    ) ENGINE=InnoDB""",

    # Tutores
    """CREATE TABLE IF NOT EXISTS tutores (
        id_tutor            INT AUTO_INCREMENT PRIMARY KEY,
        nome                VARCHAR(150) NOT NULL,
        rg                  VARCHAR(20) NULL,
        cpf                 CHAR(11) NOT NULL,
        cep                 CHAR(8) NULL,
        endereco            VARCHAR(255) NULL,
        numero              VARCHAR(20) NULL,
        complemento         VARCHAR(100) NULL,
        bairro              VARCHAR(100) NULL,
        cidade              VARCHAR(100) NULL,
        estado              CHAR(2) NULL,
        telefone            VARCHAR(20) NOT NULL,
        email               VARCHAR(150) NULL,
        horas_fora_casa     DECIMAL(4,1) NULL,
        id_tipo_moradia     INT NULL,
        casa_telada         ENUM('Sim','Não','Não se aplica') NULL,
        acesso_quintal      ENUM('Sim','Não','Não se aplica') NULL,
        acesso_rua          ENUM('Sim','Não','Não se aplica') NULL,
        autoriza_visita_ong ENUM('Sim','Não') NOT NULL DEFAULT 'Sim',
        autoriza_foto_mural ENUM('Sim','Não') NOT NULL DEFAULT 'Sim',
        observacoes         TEXT NULL,
        data_cadastro       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_tutor_moradia FOREIGN KEY (id_tipo_moradia)
            REFERENCES tipos_moradia(id_tipo)
    ) ENGINE=InnoDB""",

    # Adoções
    """CREATE TABLE IF NOT EXISTS adocoes (
        id_adocao        INT AUTO_INCREMENT PRIMARY KEY,
        id_animal        INT NOT NULL,
        id_tutor         INT NOT NULL,
        id_status        INT NOT NULL DEFAULT 1,
        data_interesse   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        data_solicitacao DATETIME NULL,
        data_adocao      DATETIME NULL,
        termo_gerado     BOOLEAN NOT NULL DEFAULT FALSE,
        observacoes      TEXT NULL,
        CONSTRAINT fk_adocao_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal),
        CONSTRAINT fk_adocao_tutor  FOREIGN KEY (id_tutor)  REFERENCES tutores(id_tutor),
        CONSTRAINT fk_adocao_status FOREIGN KEY (id_status) REFERENCES status_adocao(id_status)
    ) ENGINE=InnoDB""",

    # Visitas
    """CREATE TABLE IF NOT EXISTS visitas (
        id_visita    INT AUTO_INCREMENT PRIMARY KEY,
        id_adocao    INT NOT NULL,
        id_resultado INT NULL,
        data_visita  DATETIME NOT NULL,
        observacoes  TEXT NULL,
        data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_visita_adocao    FOREIGN KEY (id_adocao)    REFERENCES adocoes(id_adocao),
        CONSTRAINT fk_visita_resultado FOREIGN KEY (id_resultado) REFERENCES resultado_visita(id_resultado)
    ) ENGINE=InnoDB""",

    # Fotos adoções
    """CREATE TABLE IF NOT EXISTS fotos_adocoes (
        id_foto_adocao        INT AUTO_INCREMENT PRIMARY KEY,
        id_visita             INT NOT NULL,
        url_foto              VARCHAR(500) NOT NULL,
        id_cloudinary         VARCHAR(255) NULL,
        autorizada_divulgacao BOOLEAN NOT NULL DEFAULT FALSE,
        data_cadastro         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_foto_visita FOREIGN KEY (id_visita)
            REFERENCES visitas(id_visita) ON DELETE CASCADE
    ) ENGINE=InnoDB""",
]

for cmd in comandos:
    try:
        cursor.execute(cmd)
        conn.commit()
    except Exception as e:
        print(f"Aviso: {e}")

# Verifica tabelas criadas
cursor.execute("SHOW TABLES")
tabelas = [row[0] for row in cursor.fetchall()]
print(f"\n✅ Tabelas criadas: {', '.join(tabelas)}")

conn.close()
print("\n🐾 Banco PATATINO pronto!")

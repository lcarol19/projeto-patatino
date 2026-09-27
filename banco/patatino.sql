-- ============================================================
-- PATATINO - Plataforma Web para Adoção Responsável de Animais
-- Banco de dados: patatino_pets
-- ============================================================

CREATE DATABASE IF NOT EXISTS patatino_pets
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE patatino_pets;

-- ============================================================
-- TABELAS DE DOMÍNIO (listas fixas)
-- ============================================================

CREATE TABLE IF NOT EXISTS especies (
    id_especie      INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO especies (descricao) VALUES
    ('Cachorro'),
    ('Gato'),
    ('Outro');

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS portes (
    id_porte        INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO portes (descricao) VALUES
    ('Pequeno'),
    ('Médio'),
    ('Grande');

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS status_animal (
    id_status       INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO status_animal (descricao) VALUES
    ('Para adoção'),
    ('Adotado'),
    ('Em tratamento'),
    ('Óbito');

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS status_adocao (
    id_status       INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO status_adocao (descricao) VALUES
    ('Em análise'),
    ('Aprovada'),
    ('Recusada'),
    ('Cancelada'),
    ('Concluída');

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tipos_moradia (
    id_tipo         INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO tipos_moradia (descricao) VALUES
    ('Casa'),
    ('Apartamento'),
    ('Sítio'),
    ('Comércio'),
    ('Outros');

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS resultado_visita (
    id_resultado    INT AUTO_INCREMENT PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

INSERT INTO resultado_visita (descricao) VALUES
    ('Ok'),
    ('Preocupante'),
    ('Retorno necessário');

-- ============================================================
-- TABELAS PRINCIPAIS
-- ============================================================

CREATE TABLE IF NOT EXISTS animais (
    id_animal           INT AUTO_INCREMENT PRIMARY KEY,
    nome                VARCHAR(100)    NOT NULL,
    id_especie          INT             NOT NULL,
    id_porte            INT             NOT NULL,
    id_status           INT             NOT NULL DEFAULT 1,
    sexo                ENUM('Macho','Fêmea','Não informado') NOT NULL DEFAULT 'Não informado',
    idade_aproximada    INT             NULL COMMENT 'Idade em meses',
    codigo_chip         VARCHAR(50)     NULL,
    temperamento        VARCHAR(255)    NULL,
    descricao           TEXT            NULL,
    observacoes         TEXT            NULL,
    data_cadastro       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao    DATETIME        NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_animal_especie FOREIGN KEY (id_especie) REFERENCES especies(id_especie),
    CONSTRAINT fk_animal_porte   FOREIGN KEY (id_porte)   REFERENCES portes(id_porte),
    CONSTRAINT fk_animal_status  FOREIGN KEY (id_status)  REFERENCES status_animal(id_status)
) ENGINE=InnoDB;

CREATE INDEX idx_animal_status  ON animais(id_status);
CREATE INDEX idx_animal_especie ON animais(id_especie);
CREATE INDEX idx_animal_nome    ON animais(nome);

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fotos_animais (
    id_foto         INT AUTO_INCREMENT PRIMARY KEY,
    id_animal       INT             NOT NULL,
    url_foto        VARCHAR(500)    NOT NULL COMMENT 'URL Cloudinary',
    id_cloudinary   VARCHAR(255)    NULL     COMMENT 'Public ID Cloudinary para exclusão',
    ordem           INT             NOT NULL DEFAULT 1,
    data_cadastro   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_foto_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_fotos_animal ON fotos_animais(id_animal);

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tutores (
    id_tutor            INT AUTO_INCREMENT PRIMARY KEY,
    nome                VARCHAR(150)    NOT NULL,
    rg                  VARCHAR(20)     NULL,
    cpf                 CHAR(11)        NOT NULL COMMENT 'Apenas números',
    cep                 CHAR(8)         NULL,
    endereco            VARCHAR(255)    NULL,
    numero              VARCHAR(20)     NULL,
    complemento         VARCHAR(100)    NULL,
    bairro              VARCHAR(100)    NULL,
    cidade              VARCHAR(100)    NULL,
    estado              CHAR(2)         NULL,
    telefone            VARCHAR(20)     NOT NULL,
    email               VARCHAR(150)    NULL,
    horas_fora_casa     DECIMAL(4,1)    NULL,
    id_tipo_moradia     INT             NULL,
    casa_telada         ENUM('Sim','Não','Não se aplica') NULL,
    acesso_quintal      ENUM('Sim','Não','Não se aplica') NULL,
    acesso_rua          ENUM('Sim','Não','Não se aplica') NULL,
    autoriza_visita_ong ENUM('Sim','Não')                 NOT NULL DEFAULT 'Sim',
    autoriza_foto_mural ENUM('Sim','Não')                 NOT NULL DEFAULT 'Sim',
    observacoes         TEXT            NULL,
    data_cadastro       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tutor_moradia FOREIGN KEY (id_tipo_moradia) REFERENCES tipos_moradia(id_tipo)
) ENGINE=InnoDB;

CREATE INDEX idx_tutor_cpf  ON tutores(cpf);
CREATE INDEX idx_tutor_nome ON tutores(nome);

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS adocoes (
    id_adocao           INT AUTO_INCREMENT PRIMARY KEY,
    id_animal           INT             NOT NULL,
    id_tutor            INT             NOT NULL,
    id_status           INT             NOT NULL DEFAULT 1,
    data_interesse      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_solicitacao    DATETIME        NULL,
    data_adocao         DATETIME        NULL,
    termo_gerado        BOOLEAN         NOT NULL DEFAULT FALSE,
    observacoes         TEXT            NULL,
    CONSTRAINT fk_adocao_animal FOREIGN KEY (id_animal) REFERENCES animais(id_animal),
    CONSTRAINT fk_adocao_tutor  FOREIGN KEY (id_tutor)  REFERENCES tutores(id_tutor),
    CONSTRAINT fk_adocao_status FOREIGN KEY (id_status) REFERENCES status_adocao(id_status)
) ENGINE=InnoDB;

CREATE INDEX idx_adocao_animal ON adocoes(id_animal);
CREATE INDEX idx_adocao_tutor  ON adocoes(id_tutor);
CREATE INDEX idx_adocao_status ON adocoes(id_status);

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS visitas (
    id_visita       INT AUTO_INCREMENT PRIMARY KEY,
    id_adocao       INT             NOT NULL,
    id_resultado    INT             NULL,
    data_visita     DATETIME        NOT NULL,
    observacoes     TEXT            NULL,
    data_cadastro   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_visita_adocao    FOREIGN KEY (id_adocao)    REFERENCES adocoes(id_adocao),
    CONSTRAINT fk_visita_resultado FOREIGN KEY (id_resultado) REFERENCES resultado_visita(id_resultado)
) ENGINE=InnoDB;

CREATE INDEX idx_visita_adocao ON visitas(id_adocao);

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fotos_adocoes (
    id_foto_adocao      INT AUTO_INCREMENT PRIMARY KEY,
    id_visita           INT             NOT NULL,
    url_foto            VARCHAR(500)    NOT NULL COMMENT 'URL Cloudinary',
    id_cloudinary       VARCHAR(255)    NULL,
    autorizada_divulgacao BOOLEAN       NOT NULL DEFAULT FALSE,
    data_cadastro       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_foto_visita FOREIGN KEY (id_visita) REFERENCES visitas(id_visita)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_foto_visita ON fotos_adocoes(id_visita);

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "structscan.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabela 1: Catálogo Normativo de Patologias (Civil e Elétrica)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS catalogo_patologias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        area TEXT NOT NULL,
        sistema TEXT NOT NULL,
        titulo TEXT NOT NULL,
        risco TEXT NOT NULL,
        tipo_manutencao TEXT NOT NULL,
        prazo_sugerido TEXT NOT NULL,
        norma_referencia TEXT NOT NULL,
        requer_laudo_especifico INTEGER DEFAULT 0,
        diagnostico_padrao TEXT NOT NULL,
        recomendacao_padrao TEXT NOT NULL
    )
    """)

    # Tabela 2: Vistorias / Edificações (Lei Municipal 9.913/2012 - Fortaleza)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vistorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edificacao TEXT NOT NULL,
        endereco TEXT NOT NULL,
        uso_edificacao TEXT NOT NULL,
        idade_imovel INTEGER NOT NULL,
        periodicidade_cip TEXT NOT NULL,
        data_vistoria TEXT NOT NULL,
        engenheiro TEXT NOT NULL,
        crea_art TEXT NOT NULL,
        estado_geral TEXT NOT NULL
    )
    """)

    # Tabela 3: Anomalias Registradas na Vistoria
    cur.execute("""
    CREATE TABLE IF NOT EXISTS anomalias_registradas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vistoria_id INTEGER NOT NULL,
        area TEXT NOT NULL,
        sistema TEXT NOT NULL,
        titulo TEXT NOT NULL,
        local TEXT NOT NULL,
        risco TEXT NOT NULL,
        tipo_manutencao TEXT NOT NULL,
        prazo_conclusao TEXT NOT NULL,
        requer_laudo_especifico INTEGER DEFAULT 0,
        diagnostico TEXT NOT NULL,
        recomendacao TEXT NOT NULL,
        foto_base64 TEXT,
        FOREIGN KEY (vistoria_id) REFERENCES vistorias(id) ON DELETE CASCADE
    )
    """)

    # Seed Catálogo se vazio
    cur.execute("SELECT COUNT(*) FROM catalogo_patologias")
    if cur.fetchone()[0] == 0:
        patologias_seed = [
            # ENGENHARIA CIVIL (10)
            ("CIV-01", "Civil", "Estrutura de Concreto", "Corrosão de armadura com desplacamento", "Crítico", "Corretiva Imediata", "30 dias (Art. 10 Lei 9.913/12)", "ABNT NBR 6118 / NBR 16747", 0,
             "Carbonatação do concreto e ataque de cloretos por cobrimento insuficiente, provocando oxidação da armadura longitudinal, expansão e desplacamento do cobrimento.",
             "Escarificação do concreto degradado, limpeza mecânica das armaduras, aplicação de primer inibidor de corrosão e recomposição com graute estrutural."),
            ("CIV-02", "Civil", "Estrutura de Concreto", "Fissura inclinada a 45° em alvenaria estrutural / vedação", "Regular", "Corretiva Programada", "60 dias", "ABNT NBR 16868 / NBR 16747", 0,
             "Tensões de cisalhamento ocasionadas por recalque diferencial de apoio ou deformação excessiva da viga superior.",
             "Instalação de selos de gesso/fissurômetros por 30 dias para verificar estabilização; posterior abertura em 'V' e tratamento com selante elastomérico."),
            ("CIV-03", "Civil", "Estrutura de Concreto", "Flecha excessiva / deformação visível em viga ou laje", "Crítico", "Corretiva Imediata", "15 dias (Escoramento imediato)", "ABNT NBR 6118", 0,
             "Sobrecarga não prevista em projeto ou perda de rigidez à flexão, ocasionando fissuração na face tracionada e esmagamento de alvenarias inferiores.",
             "Escoramento imediato da região afetada, levantamento geométrico e reforço estrutural com perfis metálicos ou fibra de carbono."),
            ("CIV-04", "Civil", "Impermeabilização e Cobertura", "Infiltração ativa com eflorescência e estalactites em laje", "Regular", "Corretiva Programada", "90 dias", "ABNT NBR 9575", 0,
             "Falha na estanqueidade da laje superior permitindo percolação de água pluvial, lixiviação de hidróxido de cálcio e formação de estalactites.",
             "Remoção do piso e proteção mecânica no trecho afetado, refazimento da impermeabilização conforme NBR 9575 e teste de lâmina d'água de 72h."),
            ("CIV-05", "Civil", "Impermeabilização e Cobertura", "Ressecamento e falha de manta asfáltica na cobertura", "Regular", "Corretiva Programada", "90 dias", "ABNT NBR 9575", 0,
             "Degradação térmica por exposição solar sem proteção mecânica adequada, com bolhas, fissuras e descolamento nas emendas.",
             "Substituição da manta asfáltica danificada com regularização do caimento (mín. 1%), execução de meia-cana nos rodapés e proteção mecânica."),
            ("CIV-06", "Civil", "Fachadas e Revestimentos", "Descolamento de revestimento cerâmico em fachada", "Crítico", "Corretiva Imediata", "20 dias (Isolamento imediato)", "ABNT NBR 13755", 0,
             "Perda de aderência da argamassa colante por ausência de juntas de movimentação horizontal/vertical, com som cavo à percussão e risco de queda sobre pedestres.",
             "Isolamento imediato da área térrea sob projeção da fachada, ensaio de percussão 100%, apicoamento das placas soltas e reassentamento conforme NBR 13755."),
            ("CIV-07", "Civil", "Fachadas e Revestimentos", "Falta de vedação / colmatação em junta de dilatação", "Regular", "Preventiva Periódica (Anual)", "120 dias", "ABNT NBR 13755 / NBR 16747", 0,
             "Ressecamento e ruptura do selante poliuretano da junta estrutural, permitindo ingresso de água entre blocos e deterioração da armadura.",
             "Remoção completa do selante antigo, limpeza das bordas, inserção de corpo de apoio (tarugo de polietileno) e aplicação de selante PU de baixo módulo."),
            ("CIV-08", "Civil", "Estrutura de Concreto", "Recalque diferencial / afundamento de piso no térreo", "Regular", "Corretiva Programada", "90 dias", "ABNT NBR 6122 / NBR 16747", 0,
             "Adensamento de aterro mal compactado ou carreamento de finos por vazamento subterrâneo em rede pluvial/esgoto.",
             "Inspeção com câmera nas redes enterradas próximas, recomposição da base granular compactada e reconstrução da placa de concreto armado."),
            ("CIV-09", "Civil", "Instalações Hidrossanitárias", "Vazamento em prumada hidrossanitária com umidade ascendente", "Regular", "Corretiva Programada", "60 dias", "ABNT NBR 5626 / NBR 8160", 0,
             "Ruptura de junta soldável/elástica em shaft hidráulico ocasionando saturação da alvenaria, bolor e descascamento de pintura.",
             "Abertura do shaft, substituição do trecho danificado da tubulação, teste de estanqueidade e recomposição do fechamento."),
            ("CIV-10", "Civil", "Prevenção e Combate a Incêndio", "Sistema de hidrantes / iluminação de emergência inoperante", "Crítico", "Corretiva Imediata", "15 dias (Exigência CBMCE)", "ABNT NBR 13714 / Lei 9.913 Art. 6º § único", 1,
             "Bomba de incêndio em modo manual com pressostato desregulado e luminárias de emergência sem autonomia de bateria nas rotas de fuga.",
             "Revisão completa do sistema preventivo, substituição das baterias e emissão de laudo específico de segurança contra incêndio (Art. 6º, Parágrafo Único)."),

            # ENGENHARIA ELÉTRICA (8)
            ("ELE-01", "Elétrica", "Instalações Elétricas (BT)", "Quadro elétrico sem barramento isolado e sem IDR", "Crítico", "Corretiva Imediata", "15 dias (Risco choque/incêndio)", "ABNT NBR 5410 / Lei 9.913 Art. 6º § único", 1,
             "Ausência de dispositivo diferencial residual (IDR 30mA) em circuitos de áreas molhadas e conexões diretas sem barramento isolado, gerando pontos quentes.",
             "Adequação imediata do quadro de distribuição com instalação de IDR 30mA, DPS, disjuntores padrão DIN e barramentos isolados conforme NBR 5410."),
            ("ELE-02", "Elétrica", "Instalações Elétricas (BT)", "Disjuntores padrão NEMA obsoletos / superaquecimento de bornes", "Crítico", "Corretiva Imediata", "20 dias (Anomalia térmica)", "ABNT NBR 5410 / NR-10", 1,
             "Disjuntores termomagnéticos antigos (padrão NEMA) com perda de curva de atuação e oxidação nos terminais, elevando a temperatura acima de 70°C.",
             "Retrofit completo do quadro elétrico substituindo disjuntores NEMA por padrão DIN, reapertando conexões com torquímetro e realizando termografia."),
            ("ELE-03", "Elétrica", "Aterramento e SPDA", "Descontinuidade na malha de aterramento e SPDA", "Crítico", "Corretiva Imediata", "30 dias (Risco atmosférico)", "ABNT NBR 5419", 1,
             "Cabos de descida rompidos/oxidados e ausência de equipotencialização (BEP) entre massas metálicas, comprometendo a proteção contra descargas atmosféricas.",
             "Restabelecimento da continuidade elétrica das descidas, medição com miliohmímetro (< 0,2 Ω) e emissão de laudo específico de SPDA conforme NBR 5419."),
            ("ELE-04", "Elétrica", "Instalações Elétricas (BT)", "Ausência de DPS (Proteção contra Surtos) no QGBT", "Regular", "Corretiva Programada", "60 dias", "ABNT NBR 5410 / NBR 5419", 0,
             "Quadro Geral de Baixa Tensão desprovido de Dispositivos de Proteção contra Surtos (Classe I/II), expondo elevadores, bombas e centrais eletrônicas à queima.",
             "Instalação de conjunto de DPS coordenados entre fases/neutro e barra de equipotencialização (PE) conforme NBR 5410 e NBR 5419."),
            ("ELE-05", "Elétrica", "Subestação / Média Tensão", "Subestação abrigada sem tapete isolante, EPI ou análise de óleo", "Crítico", "Corretiva Imediata", "15 dias (Risco grave NR-10)", "ABNT NBR 14039 / NR-10 / Art. 6º § único", 1,
             "Subestação de média tensão (13,8 kV) com iluminação deficiente, ausência de tapete isolante, vara de manobra e vencimento do ensaio físico-químico do óleo.",
             "Adequação imediata às exigências da NR-10 e NBR 14039, fornecimento de kit de segurança e emissão de laudo técnico específico por engenheiro eletricista."),
            ("ELE-06", "Elétrica", "Eficiência Energética", "Banco de capacitores inoperante / baixo fator de potência", "Regular", "Corretiva Programada", "60 dias", "PRODIST ANEEL / NBR 5410", 0,
             "Células capacitivas estufadas e controlador automático de fator de potência desarmado, gerando cobrança de energia reativa excedente na fatura.",
             "Substituição das células capacitivas defeituosas, revisão dos contatores de manobra e parametrização do controlador para manter FP >= 0,92."),
            ("ELE-07", "Elétrica", "Instalações Elétricas (BT)", "Condutores expostos sem eletroduto / emendas irregulares", "Crítico", "Corretiva Imediata", "15 dias (Risco curto-circuito)", "ABNT NBR 5410 / NBR 15465", 0,
             "Circuitos alimentadores lançados diretamente sobre forro combustível sem proteção mecânica e com emendas isoladas precariamente.",
             "Lançamento de eletrodutos metálicos ou PVC antichama, instalação de caixas de passagem com tampa e substituição de condutores danificados."),
            ("ELE-08", "Elétrica", "Geração de Emergência", "Grupo motogerador sem teste de transferência automática (ATS)", "Regular", "Preventiva Periódica (Semestral)", "45 dias (Art. 6º § único)", "ABNT NBR 13523 / Lei 9.913 Art. 6º § único", 1,
             "Baterias de partida sulfatadas e quadro de transferência automática (QTA) em modo manual, impedindo o acionamento de emergência dos elevadores e bombas.",
             "Substituição do banco de baterias, revisão do carregador flutuador, teste de partida com carga e emissão de laudo específico (Art. 6º, Parágrafo Único).")
        ]
        cur.executemany("""
            INSERT INTO catalogo_patologias
            (codigo, area, sistema, titulo, risco, tipo_manutencao, prazo_sugerido, norma_referencia, requer_laudo_especifico, diagnostico_padrao, recomendacao_padrao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, patologias_seed)

    # Seed Vistoria Exemplo se vazio
    cur.execute("SELECT COUNT(*) FROM vistorias")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO vistorias (edificacao, endereco, uso_edificacao, idade_imovel, periodicidade_cip, data_vistoria, engenheiro, crea_art, estado_geral)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Condomínio Residencial Jardins do Atlântico",
            "Av. Beira Mar, 2450 - Meireles, Fortaleza - CE",
            "multirresidencial_3plus",
            18,
            "A cada 5 anos (Art. 3º, IV e Art. 9º)",
            "2026-11-26",
            "Eng. Edvaldo Queiroz",
            "CREA-CE 123456-D | ART nº 2026987412",
            "Edificação em concreto armado com 12 pavimentos, apresentando condições gerais satisfatórias de habitabilidade, porém com pontos críticos localizados na estrutura do subsolo e nos quadros elétricos que demandam intervenção saneadora imediata."
        ))
        vistoria_id = cur.lastrowid
        anomalias_seed = [
            (vistoria_id, "Civil", "Estrutura de Concreto", "Corrosão de armadura com desplacamento", "Garagem Subsolo 1 - Pilar P04", "Crítico", "Corretiva Imediata", "30 dias (Art. 10 Lei 9.913/12)", 0,
             "Carbonatação do concreto por cobrimento insuficiente, provocando oxidação da armadura longitudinal e desplacamento.",
             "Escarificação, limpeza da armadura, primer anticorrosivo e recomposição com graute estrutural (NBR 6118).", None),
            (vistoria_id, "Elétrica", "Instalações Elétricas (BT)", "Quadro elétrico sem barramento isolado e sem IDR", "Hall Técnico - 3º Pavimento", "Crítico", "Corretiva Imediata", "15 dias (Risco choque/incêndio)", 1,
             "Circuito de bombas sem proteção diferencial residual (IDR 30mA) e emendas frouxas com aquecimento anormal.",
             "Substituição de disjuntores padrão NEMA por DIN, instalação de IDR 30mA e barramentos isolados (NBR 5410).", None),
            (vistoria_id, "Civil", "Impermeabilização e Cobertura", "Infiltração ativa com eflorescência e estalactites em laje", "Cobertura / Casa de Máquinas", "Regular", "Corretiva Programada", "90 dias", 0,
             "Fissuração na proteção mecânica e falha na manta asfáltica junto ao ralo pluvial.",
             "Refazimento localizado da impermeabilização conforme NBR 9575 e teste de lâmina d'água por 72h.", None)
        ]
        cur.executemany("""
            INSERT INTO anomalias_registradas
            (vistoria_id, area, sistema, titulo, local, risco, tipo_manutencao, prazo_conclusao, requer_laudo_especifico, diagnostico, recomendacao, foto_base64)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, anomalias_seed)

    conn.commit()
    conn.close()

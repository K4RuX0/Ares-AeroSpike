# Changelog - ARES-SPACE TRANSPORT

Todas as atualizações notáveis da arquitetura conceitual do veículo de transporte e suas missões logísticas integradas serão documentadas neste arquivo.

## [4.0.0-commercial] - 2030-05-24

### Adicionado
- **Arquitetura Verde de Baixo Custo (Horizonte 2030)**: Substituição completa do sistema nuclear (NTR) por Propulsão Térmica Solar (STP) altamente econômica, eliminando burocracias regulatórias, seguros abusivos e riscos radiológicos em Alcântara.
- **Transição para Metano Líquido ($LCH_4$)**: Combustível alterado de hidrogênio molecular para metano líquido. O metano é 6 vezes mais denso, reduzindo o volume dos tanques estruturais na fuselagem de 9 metros e barateando os insumos logísticos.
- **Logística Modular em Duas Fases**:
  * **Fase I (Missão Lunar)**: Circuito cislunar autônomo de ida e volta sem reabastecimento com capacidade para **55 toneladas** de carga útil.
  * **Fase II (Missão Marte - Prometheus I)**: Manobra de Injeção Trans-Marte (TMI) de alta energia levando **71 toneladas** de carga útil pura.
- **Engenharia de Corrosão Zero**: Câmara de expansão construída em liga refratária de **Carboneto de Tântalo-Háfnio ($Ta_4HfC_5$)** blindada internamente com película protetora de **Irídio**, anulando a fadiga química em altas temperaturas.
- **Tecnologia Ativa Zero Boil-Off (ZBO)**: Integração de isolamento térmico de múltiplas camadas (MLI) e crio-resfriadores de tubo de pulso operados por hélio para anular a evaporação térmica do metano no vácuo espacial profundo.

### Alterado
- **Contagem de Motores**: 4 reatores nucleares → Cluster dinâmico redundante de **2 motores térmicos solares (STP)**.
- **Empuxo Combinado (LEO)**: 740 kN → **370 kN** (calibrado dinamicamente com base no fluxo solar em 1.0 AU).
- **Impulso Específico Real ($I_{sp}$)**: 920s (alvo teórico de fissão com hidrogênio) → **620s** (calculado via expansão isentrópica termodinâmica real de metano superaquecido a 3200 K).
- **Massa Seca Estrutural (Dry Mass)**: 185.0t → **120.0t** (redução drástica pelo alívio de peso de blindagens de chumbo e do núcleo do reator).
- **Massa de Tanques**: 95.0t → **75.0t** (tanques de Al-Li compactados devido à maior densidade do metano líquido).
- **Capacidade de Propelente**: 1127.0t ($LH_2$) → **1130.0t** ($LCH_4$).
- **Massa Total em LEO**: 1407.0t → **1325.0t** (veículo mais leve e ágil).

### Corrigido
- **Física de Expansão Gasosa**: O algoritmo agora computa o comportamento real do fluido usando as propriedades térmicas moleculares específicas do metano ($\gamma = 1.32$, $R = 518.3 \text{ J/kg·K}$).
- **Vazamento Térmico**: Substituídas as estimativas genéricas por perdas baseadas na transmitância MLI real de $0.001$ e no Coeficiente de Performance (COP) dos compressores a 110 K.
- **Bug de Renderização do Front-End**: Removidos os escudos dinâmicos externos quebrados do README e substituídos por tabelas nativas estáveis em Markdown.

---

## [3.1.0-heavy] - 2026-05-22

### Adicionado
- **Configuração Pesada de 740kN**: Cluster de 4 motores NTR de 185kN cada (antigos 680kN).
- **Base de Lançamento de Alcântara**: Introdução do bônus equatorial de +463 m/s e conformidade com CNEN/AEB.
- **Relatório Engine-Out**: `e_out_tw = 0.31` explícito para aborto com 3 reatores ativos.

### Alterado
- **Massa Seca**: Reduzida para 185.0t após correção de erro de 25.8t na densidade estrutural do bocal de Carbono-Carbono (8190 → 1950 kg/m³).
- **Temperatura do Núcleo**: Elevada para 3100 K na matriz UC-ZrC-NbC para tentar sustentar o alvo teórico de 920s de Isp.

---

## - 2026-05-15

### Adicionado
- Projeto conceitual inicial V3.0: 4x motores NTR químicos de 170kN, Isp linear de 780s.
- Módulo habitacional ATHENA com 380m³ para suporte de vida de 6 tripulantes em 776 dias.

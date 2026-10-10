# Alerta Perda 🥦🥩

Sistema de monitoramento preditivo de validades e prevenção de perdas no varejo alimentar (Hortifrúti e Carnes).

## Funcionalidades
- Painel de controle de shelf-life e alertas dinâmicos de validade.
- Registro de baixas e quebras com histórico auditável.
- Monitoramento e inspeção preventiva de temperatura dos balcões refrigerados.
- Gestão de equipe e fiscais de prevenção.
- API REST para integração com sistemas de PDV (`/api/produtos/alertas`).
- Integração meteorológica com Open-Meteo (`/api/clima`) para apoiar a rotina operacional.

## Como Executar

1. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # ou source venv/bin/activate.fish

2. Instale as dependências:
    ```bash
    pip install -r requirements.txt

3. Inicie o servidor:
    ```bash
    python app.py

Acesse em: http://127.0.0.1:5000

## Configuração do clima

Por padrão, a integração consulta Pitangueiras-SP. Para configurar a localização do supermercado, defina as variáveis de ambiente abaixo antes de iniciar a aplicação:

```text
WEATHER_LOCATION=Nome da cidade, UF
WEATHER_LATITUDE=-21.0094
WEATHER_LONGITUDE=-48.2217
```

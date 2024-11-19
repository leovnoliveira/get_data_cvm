# Get Data CVM

Este repositório contém um código em Python que coleta dados diretamente do site de dados abertos da CVM, como:

- **Demonstrações Financeiras Padronizadas (DFP):** Dados de balanço das S.A.'s registrados na CVM.
- **Informes Diários dos Fundos Imobiliários:** Dados diários dos fundos de investimento imobiliário (FIIs), incluindo informações financeiras e cadastrais.

  Os arquivos CSV são extraídos, lidos, limpos e organizados em formatos adequados para análise, permitindo a fusão dos dados para enriquecimento das informações.


## Funcionalidades

- Coleta e extração de dados do balanço das S.A's da CVM.
- Coleta e extração dos informes diários dos FIIs.
- - Enriquecimento dos dados dos informes diários com informações cadastrais para inclusão da razão social dos fundos.
- Leitura e organização dos dados em formato tabular
- Limpeza e pré-processamento dos dados para análise

### Informações Disponíveis:

#### Dados de Demonstrações Financeiras (DFP):
- Balanços das empresas, incluindo informações patrimoniais e contábeis padronizadas.

#### Dados dos Informes Diários dos FIIs contém as colunas:
- Valor total da carteira do fundo.
- Patrimônio líquido.
- Valor da cota.
- Captações realizadas no dia.
- Resgates pagos no dia.
- Número de cotistas.

#### Informações Cadastrais dos FIIs possuem:
- CNPJ.
- Data de registro.
- Situação do fundo.

Esses dados são cruzados com os informes diários para adicionar a razão social do fundo, que não está disponível diretamente nos arquivos diários.

## Estrutura do Repositório

- **Pasta `dfp_zips`:** Contém os dados baixados referentes às Demonstrações Financeiras Padronizadas.
- **Pasta `inf_diario_zips`:** Contém os dados baixados referentes aos Informes Diários dos FIIs.
- **Pasta `scripts`:** Contém os scripts de definição das classes e métodos:
  - `DFPDataHandler.py`: Manipulação dos dados das Demonstrações Financeiras Padronizadas.
  - `FIIDataHandler.py`: Manipulação dos dados dos Informes Diários e cadastro dos FIIs.
- **Pasta `main`:** Scripts principais para execução do código:
  - `DFPMain.py`: Executa a coleta, processamento e análise dos dados de Demonstrações Financeiras Padronizadas.
  - `FIIMain.py`: Executa a coleta, enriquecimento e análise dos dados dos FIIs.

## Requisitos

Para executar este projeto, você precisará ter instalado:

- Python 3.x
- Anaconda (recomendado para a configuração do ambiente)

## Instalação

### 1. Criação do Ambiente Virtual no Windows (MAC e Linux é bem mais simples)

Para criar um ambiente virtual no Windows, siga as etapas abaixo.

1. **Defina as variáveis de ambiente do Python**:
   - No terminal do Anaconda Prompt, digite `where python` para identificar o caminho do seu Python e do diretório Scripts. Copie esses caminhos.
   - Abra as configurações do sistema (Painel de Controle > Sistema e Segurança > Sistema > Configurações Avançadas do Sistema > Variáveis de Ambiente).
   - Em "Variáveis do Sistema", edite a variável `Path` e adicione os caminhos do Python e do diretório `Scripts` que você obteve no passo anterior.

2. **Crie o ambiente virtual**:
   - Abra o Visual Studio Code (VSCode) e o terminal integrado.
   - No terminal, navegue até o diretório do projeto e execute o seguinte comando para criar o ambiente virtual:
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual com:
     ```bash
     venv\Scripts\Activate
     ```

3. **Instale as dependências**:
   - Com o ambiente virtual ativo, execute o seguinte comando para instalar as dependências listadas no `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

### 2. Fork do Repositório

Para replicar este projeto, você pode criar um "fork" do repositório:

1. Clique no botão "Fork" no canto superior direito da página do repositório no GitHub.
2. No seu perfil, você verá uma cópia do repositório.
3. Clone o repositório para sua máquina com o seguinte comando:
   ```bash
   git clone https://github.com/seu-usuario/get_data_cvm.git

### 3. Dependências
Abaixo estão as dependências necessárias para rodar o projeto:
```bash
   pandas==1.5.3
   requests==2.31.0
```

## Contribuições
Sinta-se à vontade para abrir issues ou enviar PRs para melhorias no código!

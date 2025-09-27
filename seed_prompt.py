from app.services.database_service import DatabaseService

# --- DEFINIÇÃO DOS PROMPTS ---

CREATION_PROMPT = """Você é TARS, um assistente de IA especialista em engenharia de software e Product Ownership. Sua tarefa é analisar a solicitação de uma nova funcionalidade e traduzi-la em Histórias de Usuário (HUs) claras, bem estruturadas, e também gerar os Critérios de Aceite para cada HU no formato Gherkin (`Dado que... Quando... Então...`).

Analise as seguintes informações:
1.  **Contexto do Projeto:** {project_context}
2.  **Contexto do Épico Atual ({epic_name}):** {epic_context}
3.  **Documentação Relevante (regras existentes do sistema relevantes para a requisição do usuário):**
    ---
    {retrieved_context}
    ---
4.  **Solicitação do Usuário (transcrição do áudio):**
    ---
    {user_request}
    ---
5.  **Exemplo de padrão ultilizado nas regras de negócio, apresentação e mensagens:**

    ---

    RA_0053: Variáveis Personalização de Modelo de E-mail
      Quando uma variável for usada no conteúdo do termo, o texto da variável deve ser destacado na cor verde.
      Caso a variável não esteja em uso, o texto deve ser exibido na cor amarela.
      Ao clicar no texto, o conteúdo da variável será automaticamente copiado para a área de transferência.
      O usuário poderá então utilizar Ctrl + V (ou Cmd + V no macOS) para colar o texto da variável em qualquer local desejado.

    RA_0054: Ordenar Questões em Questionário
      Ao clicar e segurar no ícone, deve ser possível arrastar a linha da tabela e reordenar as linhas da tabela, essa ordenação será importante para a geração da página de realização de entrevista e preenchimento de formulário pelo candidato.

    RA_0055: Autocomplete no Campo Questão - Configuração de Questionário
      O campo deve se comportar como um autocomplete para questões registradas no sistema.
      Formato de exibição: <numeração da questão> - <enunciado da questão>.
      Obs.: O enunciado da questão deve ser truncado para se adequar ao layout.

    RA_0056: Cancelar Inscrição de Candidatos com pendências - Confirmação
      O botão “Confirmar” da modal, só deve ser habilitado para o usuário assim que ele digitar exatamente o nome da turma no campo disponibilizado.

    ---

    RN_0107: Criar Usuário - Acesso Externo
      Ao incluir todas as informações corretamente:
      Uma senha deve ser gerada, de acordo com a regra RN_0105: Gerar Senha - Acesso Externo.
      A combinação CPF - CNPJ - Senha, devem ser as credenciais para a autenticação deste usuário.
      A mensagem MSG73: Usuário de acesso externo criado com sucesso deve ser acionada.

    RN_0108: Reativar/Inativar Usuário de Acesso Externo
      A ativação de um usuário de acesso externo o permite autenticar a qualquer momento com suas credenciais, enquanto a inativação impede de autenticar.
      Após inativar um usuário de acesso externo com sucesso, a seguinte mensagem deve ser acionada: MSG71: Usuário de acesso externo inativado
      Após reativar um usuário de acesso externo com sucesso, a seguinte mensagem deve ser acionada: MSG70: Usuário de acesso externo reativado
      Após realizar alguma dessas ações, um registro deve ser salvo no detalhamento do usuário (mais detalhes na regra RN_0009: Histórico do registro).

    RN_0107: Unicidade de Usuário x Empresa - Acesso Externo
      Ao criar um novo usuário, o sistema deve verificar se já existe um cadastro com a mesma combinação de CPF e CNPJ (inativo ou ativo). Caso exista, impedir a criação e acionar a mensagem: MSG72: Criar Usuário Acesso Externo - Unicidade de Usuário x Empresa.

    ---

    MSG68: Comunicado Situacional Editado com Sucesso
      Tipo: Mensagem GERAL de sucesso. 	
        Mensagem de sucesso exibida após a edição e salvamento do conteúdo de um comunicado situacional: "Conteúdo do comunicado situacional atualizado com sucesso!"

    MSG69: Gerar nova senha acesso externo com sucesso
      Tipo: Mensagem GERAL de sucesso. 	
        Mensagem de sucesso exibida após a geração de uma nova senha para um usuário de acesso externo é: "Uma nova senha foi gerada com sucesso para o usuário: [Nome Usuário]. A senha anterior foi invalidada."

    MSG72: Criar Usuário Acesso Externo - Unicidade de Usuário x Empresa
      Tipo: Mensagem GERAL de erro. 	
        A mensagem de erro exibida após a tentativa de criação de usuário externo já existente é: "Não foi possível finalizar a ação. Já existe um usuário cadastrado com este CPF e CNPJ."

    ---

Com base em TODAS as informações acima, gere uma ou mais Histórias de Usuário completas.

Sua resposta DEVE ser um array JSON válido, contido em um único bloco de código. NÃO inclua nenhum texto, explicação ou formatação markdown antes ou depois do array JSON.

Cada objeto no array deve representar uma única HU e seguir estritamente a seguinte estrutura:
{{
  "nome_hu": "Um nome curto e descritivo para a HU gerado por você, precisa seguir a numeração do epico, se a numeração do epico for 001, então as hu's devem ser 001.1 - 'nome da hu', 001.2 - 'nome da hu', 001.3 - 'nome da hu' etc.",
  "como_um": "O tipo de usuário",
  "eu_quero": "A ação ou objetivo do usuário",
  "para_que": "O benefício ou valor gerado",
  "regras_negocio": [
    {{
      "nome_numeracao_rn": "Um título descritivo da regra de negocio (siga o mesmo padrão de numeracao_nome apresentado acima)",
      "descricao": "descricao da regra de negocio"
    }}
  ],
  "regras_apresentacao": [
    {{
      "nome_numeracao_ra": "Um título descritivo da regra de apresentacao (siga o mesmo padrão de numeracao_nome apresentado acima)",
      "descricao": "descricao da regra de apresentacao"
    }}
  ],
  "mensagens_sistema": [
    {{
      "nome_numeracao_mensagem": "Um título descritivo da mensagem (siga o mesmo padrão de numeracao_nome apresentado acima)",
      "descricao": "descricao da mensagem"
    }}
  ],
  "criterios_aceite": [
    {{
      "cenario": "Um título descritivo para o primeiro cenário de teste",
      "dado_que": "Uma string descrevendo o contexto inicial (Given), podendo ter múltiplas condições separadas por 'E'",
      "quando": "Uma string descrevendo a ação do usuário (When)",
      "entao": "Uma string descrevendo o resultado esperado e verificável (Then), podendo ter múltiplas condições separadas por 'E'"
    }}
  ]
}}

Gere o array JSON agora. A sua resposta DEVE começar com o caractere '[' e terminar com o caractere ']' e não deve conter absolutamente mais nada.
"""

# Prompt para refinar a busca vetorial
SEARCH_PROMPT = """Você é um especialista em sistemas de busca e recuperação de informação. Sua tarefa é analisar a solicitação conversacional de um usuário e extrair dela os termos técnicos, funcionais e palavras-chave mais relevantes para uma busca em uma base de dados vetorial de documentos de software.

Elimine palavras de preenchimento, frases de polidez e linguagem ambígua. Foque nos conceitos e funcionalidades.

Sua resposta deve ser APENAS uma string com os termos separados por vírgula, nada mais.

Exemplos:
---
Exemplo 1:
Solicitação do Usuário: "Então, eu tava pensando aqui, a gente precisa que o usuário consiga, sabe, entrar no sistema usando a conta do Google dele, pra ser mais fácil."
Sua Resposta: login, autenticação, Google, social login, OAuth, Single Sign-On, SSO, credenciais
---
Exemplo 2:
Solicitação do Usuário: "Acho que seria legal se na tela de listagem, quando não tiver nenhum item pra mostrar, aparecesse uma mensagem bonitinha em vez de ficar tudo em branco."
Sua Resposta: tela de listagem, lista, estado vazio, empty state, mensagem de feedback, UI, UX, nenhum item
---
Agora, faça o mesmo para a seguinte solicitação:

Solicitação do Usuário: "{user_request}"
Sua Resposta:
"""

def seed_database_prompts():
    """
    Função principal para inserir os prompts padrão na tabela de configurações.
    """
    print("Iniciando o script para popular o banco de dados com os prompts...")
    
    # Aponta para o banco de dados principal onde as configurações são salvas
    db_path = "data/tars_main.db"
    db_service = DatabaseService(db_path=db_path)

    prompts_to_save = {
        "CREATION_PROMPT_TEMPLATE": CREATION_PROMPT,
        "BETTER_CONTEXT_SEARCH_PROMPT": SEARCH_PROMPT,
        "AI_PROVIDER_PREFERENCE": "gemini",
        "OPENAI_API_KEY": {},
        "GOOGLE_API_KEY": {}
    }

    for key, value in prompts_to_save.items():
        print(f"Salvando/Atualizando a configuração: '{key}'...")
        db_service.save_setting(key, value)

    print("\nPrompts salvos com sucesso no banco de dados!")
    print("Você pode verificar o arquivo 'data/tars_main.db' para confirmar.")

if __name__ == "__main__":
    seed_database_prompts()
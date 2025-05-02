# Estrutura do Banco de Dados

Com base nos requisitos do projeto, a seguinte estrutura de tabela é definida para o banco de dados. Esta tabela armazenará as informações dos usuários, suas respostas ao quiz, o resumo gerado pela IA e o código de acesso.

**Tabela: `usuarios`**

| Coluna             | Tipo          | Restrições                           | Descrição                                                                 |
|--------------------|---------------|--------------------------------------|---------------------------------------------------------------------------|
| `id`               | INT           | PRIMARY KEY, AUTO_INCREMENT          | Identificador único numérico para cada registro.                          |
| `nick`             | VARCHAR(255)  | UNIQUE, NOT NULL                     | O @nick fornecido pelo usuário.                                           |
| `telefone`         | VARCHAR(50)   | UNIQUE, NOT NULL                     | O número de telefone fornecido pelo usuário (usado como identificador). |
| `codigo_acesso`    | VARCHAR(50)   | UNIQUE, NOT NULL                     | Código único gerado para acesso futuro ao resumo.                         |
| `respostas_quiz`   | JSON          | NULL                                 | Armazena as respostas do usuário ao quiz no formato JSON.                 |
| `resumo_gerado`    | TEXT          | NULL                                 | Armazena o resumo personalizado gerado pela IA Gemini.                    |
| `idioma`           | VARCHAR(10)   | NOT NULL                             | Idioma em que o teste foi realizado e o resumo foi gerado (ex: 'pt', 'en'). |
| `data_criacao`     | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP            | Data e hora de criação do registro.                                       |
| `data_atualizacao` | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Data e hora da última atualização do registro.                            |

**Considerações:**

*   **Privacidade:** Armazenar números de telefone diretamente requer atenção às leis de privacidade de dados (como LGPD). Considerar anonimização ou hashing se necessário.
*   **Índices:** Criar índices nas colunas `nick`, `telefone` e `codigo_acesso` será crucial para otimizar as buscas futuras.
*   **Escalabilidade:** A estrutura JSON para `respostas_quiz` oferece flexibilidade, mas pode impactar a performance de consultas complexas sobre as respostas individuais. Avaliar se uma tabela separada para respostas seria melhor em caso de análises muito detalhadas no futuro.


import os
import base64
from key import OPENAI_API_KEY

from openai import OpenAI

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def converte_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analisar_imagem(arquivo, tipo_analise):
    base64_image = converte_base64(arquivo)
    if tipo_analise == "expert_apresentacao":
        texto = "Você é um expert em preparar apresentações e montar textos para suportar as apresentações. Veja o slide e escreva um roteiro dos principaos pontos a serem explicados. Informe também se há alguma sugestão de alteração no slide."
    elif tipo_analise == "expert_seguranca":
        texto = "Você é um expert em segurança do trabalho. Analise a imagem e retorne com 1) pontos de atenção, 2) recomendações."
    elif tipo_analise == "expert_fiscal":
        texto = "Você é um expert em extrair informações de documentos fiscais. Por favor retorne com um json com as seguintes informações: data, nome do estabelecimento, cnpj, valor total."
    elif tipo_analise == "expert_fiscal_itens":
        texto = "Você é um expert em extrair informações de documentos fiscais. Por favor retorne com um json com as seguintes informações: data, nome do estabelecimento, cnpj, itens (cada item:descrição, quantidade, valor unitário, valor total por item), valor total do documento."
    elif tipo_analise == "expert_financeiro":
        texto = "Você é um expert em análises financeiras. Avalie as informações e retorne com uma análise sobre a situação da empresa."

  
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": texto
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ],
            },
        ]
    )

    return response.choices[0].message.content


tarefas = [
    ["cupom_fiscal.jpg", "expert_fiscal"],
    ["nfe.png", "expert_fiscal_itens"],
    ["obra.png", "expert_seguranca"],
    ["risco_fabrica.jpg", "expert_seguranca"],
    ["armazem.jpg", "expert_seguranca"],
    ["bradesco.webp", "expert_financeiro"],
    ["vittia.jpg", "expert_apresentacao"],
]

client = OpenAI(api_key=OPENAI_API_KEY)

sessao = 6

arquivo = tarefas[sessao][0]
tipo_analise = tarefas[sessao][1]

print("-------------------------------------")
print(f"Analisando imagem: {arquivo}")
print(f"Tipo de analise: {tipo_analise}")
resposta = analisar_imagem(arquivo, tipo_analise)

print("-------------------------------------")
print(resposta)
print("-------------------------------------")

arq = os.path.splitext(arquivo)[0]
with open(f'{arq}.md', 'w', encoding='utf-8') as f:
    f.write(resposta)




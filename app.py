"""
AdotaIA: protótipo local (Gradio)

Carrega o modelo treinado no notebook (modelo/modelo_adocao.joblib) e abre um formulário
para estimar a chance de um animal ser adotado em até 30 dias.

Como executar:
    pip install -r requirements.txt
    python app.py
Depois abra no navegador o endereço mostrado no terminal (normalmente http://127.0.0.1:7860).

ATENÇÃO: o modelo foi treinado com DADOS FICTÍCIOS. Uso apenas acadêmico/demonstrativo.
"""

import os
import sys

import gradio as gr
import joblib
import pandas as pd

# Caminho do modelo salvo pelo notebook (relativo a este arquivo)
PASTA = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MODELO = os.path.join(PASTA, "modelo", "modelo_adocao.joblib")

if not os.path.exists(CAMINHO_MODELO):
    sys.exit(f"Modelo não encontrado em {CAMINHO_MODELO}.\n"
             "Execute o notebook AdotaIA.ipynb até o fim para gerar o arquivo.")

modelo = joblib.load(CAMINHO_MODELO)


# ---------------------------------------------------------------------------
# Mesmas regras do notebook (Etapa 4)
# ---------------------------------------------------------------------------
def classificar_chance(prob):
    """Converte a probabilidade em uma faixa fácil de entender."""
    if prob >= 0.6:
        return "Alta chance"
    elif prob >= 0.4:
        return "Média chance"
    return "Baixa chance"


def gerar_recomendacoes(animal, limite=3):
    """Gera recomendações por regras simples, a partir dos dados digitados."""
    dicas = []
    if animal["castrado"] == "não":
        dicas.append("Castrar o animal: animais castrados costumam ser adotados mais rápido.")
    if animal["foto_boa_qualidade"] == "não":
        dicas.append("Fazer fotos novas, com boa luz e mostrando o rosto e a personalidade do animal.")
    if animal["qtd_divulgacoes"] < 3:
        dicas.append("Priorizar este animal nas redes sociais (ele teve poucas divulgações).")
    if animal["vacinado"] == "não":
        dicas.append("Atualizar a vacinação e destacar isso na divulgação.")
    if animal["temperamento"] == "tímido":
        dicas.append("Investir em socialização e descrever o jeito do animal no post (ex.: 'carinhoso depois que confia').")
    if animal["possui_deficiencia"] == "sim":
        dicas.append("Contar a história do animal e mostrar que a deficiência não impede uma vida feliz.")
    if animal["idade_meses"] > 96 or animal["porte"] == "grande" or animal["cor_pelagem"] == "preta":
        dicas.append("Incluir em campanhas específicas (ex.: 'Adote um idoso', 'Adote um pretinho', 'Adote um grandão').")
    if animal["vermifugado"] == "não":
        dicas.append("Vermifugar o animal antes das feiras de adoção.")
    if animal["tempo_abrigo_dias"] > 90:
        dicas.append("Dar destaque especial: ele já está há mais de 3 meses esperando um lar.")
    if not dicas:
        dicas.append("O perfil é favorável: manter a divulgação atual e levar às feiras de adoção.")
    return dicas[:limite]


def interface_prever(especie, idade_anos, idade_meses, porte, sexo, cor_pelagem, vacinado, castrado,
                     vermifugado, possui_deficiencia, temperamento, tempo_abrigo_dias,
                     qtd_divulgacoes, foto_boa_qualidade):
    """Função chamada quando o usuário clica em 'Prever chance'.

    Devolve dois valores:
      1. um texto em Markdown, mostrado na própria página;
      2. um dicionário com os resultados, que o JavaScript usa para montar a janela.
    """
    # A idade é digitada em anos + meses e convertida para meses (o modelo usa meses)
    total_meses = int(idade_anos or 0) * 12 + int(idade_meses or 0)
    if total_meses < 1 or total_meses > 180:
        aviso = "A idade deve ficar entre 1 mês e 15 anos."
        return f"⚠️ {aviso}", {"erro": aviso}

    # Gatos no cadastro são sempre pequenos ou médios
    if especie == "gato" and porte == "grande":
        aviso = "Para gatos, escolha porte pequeno ou médio."
        return f"⚠️ {aviso}", {"erro": aviso}

    animal = {
        "especie": especie, "idade_meses": total_meses, "porte": porte, "sexo": sexo,
        "cor_pelagem": cor_pelagem, "vacinado": vacinado, "castrado": castrado,
        "vermifugado": vermifugado, "possui_deficiencia": possui_deficiencia,
        "temperamento": temperamento, "tempo_abrigo_dias": int(tempo_abrigo_dias or 0),
        "qtd_divulgacoes": int(qtd_divulgacoes or 0), "foto_boa_qualidade": foto_boa_qualidade,
    }
    prob = modelo.predict_proba(pd.DataFrame([animal]))[0, 1]
    faixa = classificar_chance(prob)
    dicas = gerar_recomendacoes(animal)

    texto = f"## {faixa}\n**Probabilidade de adoção em até 30 dias:** {prob:.0%}\n\n### Recomendações\n"
    texto += "\n".join(f"- {d}" for d in dicas)
    dados = {"probabilidade": round(float(prob) * 100), "faixa": faixa, "dicas": dicas}
    return texto, dados


# ---------------------------------------------------------------------------
# Janela de resultado em JavaScript
# Esta função roda no navegador (não no Python). Ela recebe o dicionário devolvido
# por interface_prever e monta uma janela por cima da página.
# ---------------------------------------------------------------------------
JS_JANELA = """
(dados) => {
    if (!dados) return;
    const antiga = document.getElementById("adotaia-janela");
    if (antiga) antiga.remove();

    // Cor de acordo com a faixa de chance
    const cores = {"Alta chance": "#2e7d32", "Média chance": "#ef8f00", "Baixa chance": "#c62828"};
    const cor = cores[dados.faixa] || "#555";

    // Fundo escurecido que cobre a página
    const fundo = document.createElement("div");
    fundo.id = "adotaia-janela";
    fundo.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.55);display:flex;" +
        "align-items:center;justify-content:center;z-index:9999;padding:16px;";

    // Caixa branca com o resultado
    const caixa = document.createElement("div");
    caixa.setAttribute("role", "dialog");
    caixa.style.cssText = "background:#fff;color:#222;border-radius:16px;max-width:440px;width:100%;" +
        "padding:28px;box-shadow:0 10px 40px rgba(0,0,0,.3);font-family:system-ui,sans-serif;" +
        "border-top:8px solid " + cor + ";";

    if (dados.erro) {
        caixa.innerHTML = "<h2 style='margin:0 0 12px'>⚠️ Atenção</h2><p class='msg'></p>";
        caixa.querySelector(".msg").textContent = dados.erro;
    } else {
        caixa.innerHTML =
            "<div style='font-size:14px;color:#666'>🐾 AdotaIA: chance de adoção em 30 dias</div>" +
            "<div style='font-size:56px;font-weight:700;color:" + cor + ";margin:8px 0 0'>" +
                dados.probabilidade + "%</div>" +
            "<div style='font-size:20px;font-weight:600;color:" + cor + "'>" + dados.faixa + "</div>" +
            "<div style='background:#eee;border-radius:8px;height:12px;margin:14px 0 20px;overflow:hidden'>" +
                "<div style='height:100%;width:" + dados.probabilidade + "%;background:" + cor + "'></div></div>" +
            "<div style='font-weight:600;margin-bottom:6px'>Recomendações</div><ul class='dicas' " +
                "style='margin:0 0 16px;padding-left:20px;line-height:1.5'></ul>" +
            "<div style='font-size:12px;color:#888'>⚠️ Modelo treinado com dados fictícios.</div>";
        // textContent evita que o texto seja interpretado como HTML
        const lista = caixa.querySelector(".dicas");
        dados.dicas.forEach((d) => {
            const item = document.createElement("li");
            item.textContent = d;
            lista.appendChild(item);
        });
    }

    // Botão de fechar
    const botao = document.createElement("button");
    botao.textContent = "Fechar";
    botao.style.cssText = "margin-top:20px;width:100%;padding:12px;border:0;border-radius:10px;" +
        "background:" + cor + ";color:#fff;font-size:16px;cursor:pointer;";
    caixa.appendChild(botao);

    const fechar = () => { fundo.remove(); document.removeEventListener("keydown", teclaEsc); };
    const teclaEsc = (e) => { if (e.key === "Escape") fechar(); };
    botao.onclick = fechar;
    fundo.onclick = (e) => { if (e.target === fundo) fechar(); };   // clique fora da caixa fecha
    document.addEventListener("keydown", teclaEsc);

    fundo.appendChild(caixa);
    document.body.appendChild(fundo);
    botao.focus();
}
"""

SIM_NAO = ["sim", "não"]

with gr.Blocks(title="AdotaIA") as demo:
    gr.Markdown("# 🐾 AdotaIA: chance de adoção em 30 dias\n"
                "⚠️ **Protótipo acadêmico.** O modelo foi treinado com **dados fictícios** e serve apenas "
                "para demonstração. Não use o resultado como decisão definitiva sobre um animal.")

    with gr.Row():
        with gr.Column():
            especie = gr.Radio(["cão", "gato"], value="cão", label="Espécie")
            with gr.Row():   # idade separada em anos e meses (mais fácil de preencher)
                campo_anos = gr.Number(value=2, precision=0, minimum=0, maximum=15, label="Idade: anos")
                campo_meses = gr.Number(value=0, precision=0, minimum=0, maximum=11, label="Idade: meses")
            porte = gr.Radio(["pequeno", "médio", "grande"], value="médio", label="Porte (gatos: pequeno ou médio)")
            sexo = gr.Radio(["macho", "fêmea"], value="macho", label="Sexo")
            cor_pelagem = gr.Radio(["preta", "clara", "mista"], value="mista", label="Cor da pelagem")
            temperamento = gr.Radio(["dócil", "tímido", "agitado"], value="dócil", label="Temperamento")
            tempo_abrigo = gr.Number(value=30, precision=0, minimum=0, label="Tempo no abrigo (dias)")
        with gr.Column():
            vacinado = gr.Radio(SIM_NAO, value="sim", label="Vacinado?")
            castrado = gr.Radio(SIM_NAO, value="não", label="Castrado?")
            vermifugado = gr.Radio(SIM_NAO, value="sim", label="Vermifugado?")
            deficiencia = gr.Radio(SIM_NAO, value="não", label="Possui deficiência?")
            foto = gr.Radio(SIM_NAO, value="não", label="Tem foto de boa qualidade?")
            divulgacoes = gr.Number(value=2, precision=0, minimum=0, label="Quantidade de divulgações nas redes")

    with gr.Row():
        botao_limpar = gr.Button("Limpar", variant="secondary")
        botao = gr.Button("Prever chance", variant="primary")
    resultado = gr.Markdown()                  # resultado também fica escrito na página
    dados_janela = gr.JSON(visible=False)      # dados que o JavaScript vai ler

    # 1º) o Python calcula a previsão; 2º) o JavaScript abre a janela com o resultado
    botao.click(
        fn=interface_prever,
        inputs=[especie, campo_anos, campo_meses, porte, sexo, cor_pelagem, vacinado, castrado, vermifugado,
                deficiencia, temperamento, tempo_abrigo, divulgacoes, foto],
        outputs=[resultado, dados_janela],
    ).then(fn=None, inputs=dados_janela, js=JS_JANELA)

    # Botão "Limpar": volta todos os campos para os valores iniciais e apaga o resultado
    def limpar_campos():
        return ("cão", 2, 0, "médio", "macho", "mista", "dócil", 30,      # coluna da esquerda
                "sim", "não", "sim", "não", "não", 2,                    # coluna da direita
                "", None)                                                # resultado e dados da janela

    botao_limpar.click(
        fn=limpar_campos,
        inputs=None,
        outputs=[especie, campo_anos, campo_meses, porte, sexo, cor_pelagem, temperamento, tempo_abrigo,
                 vacinado, castrado, vermifugado, deficiencia, foto, divulgacoes,
                 resultado, dados_janela],
    )


if __name__ == "__main__":
    demo.launch()

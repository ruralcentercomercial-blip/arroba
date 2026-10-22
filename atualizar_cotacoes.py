import json
import urllib.request
from datetime import datetime, timezone

UFS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

NOMES = {
    "AC":"Acre", "AL":"Alagoas", "AP":"Amapá", "AM":"Amazonas",
    "BA":"Bahia", "CE":"Ceará", "DF":"Distrito Federal",
    "ES":"Espírito Santo", "GO":"Goiás", "MA":"Maranhão",
    "MT":"Mato Grosso", "MS":"Mato Grosso do Sul",
    "MG":"Minas Gerais", "PA":"Pará", "PB":"Paraíba",
    "PR":"Paraná", "PE":"Pernambuco", "PI":"Piauí",
    "RJ":"Rio de Janeiro", "RN":"Rio Grande do Norte",
    "RS":"Rio Grande do Sul", "RO":"Rondônia",
    "RR":"Roraima", "SC":"Santa Catarina", "SP":"São Paulo",
    "SE":"Sergipe", "TO":"Tocantins"
}

def consultar(uf):
    url = f"https://agrodocai.com.br/api/v1/cotacao?uf={uf}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "RuralCenterCotacao/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))

    # Preço estadual vem dentro de boi_gordo_uf.preco
    estadual = dados.get("boi_gordo_uf") or {}
    valor = estadual.get("preco")

    # Para SP, se não houver preço estadual, usa a referência CEPEA/SP
    if valor is None and uf == "SP":
        valor = dados.get("boi_gordo_cepea_sp")

    if valor is not None:
        return {
            "uf": uf,
            "estado": NOMES[uf],
            "valor": float(valor),
            "data_cotacao": dados.get("atualizado"),
            "fonte": "AgroDoc AI"
        }

    return None

def main():
    arquivo = "cotacoes.json"

    try:
        with open(arquivo, encoding="utf-8") as f:
            anterior = json.load(f)
    except (OSError, ValueError):
        anterior = {"cotacoes": []}

    antigos = {
        item["uf"]: item
        for item in anterior.get("cotacoes", [])
    }

    cotacoes = []
    sucessos = 0

    for uf in UFS:
        try:
            item = consultar(uf)
            if item:
                cotacoes.append(item)
                sucessos += 1
            else:
                cotacoes.append(antigos.get(uf, {
                    "uf": uf,
                    "estado": NOMES[uf],
                    "valor": None,
                    "data_cotacao": None
                }))
        except Exception as erro:
            print(f"Falha em {uf}: {erro}")
            cotacoes.append(antigos.get(uf, {
                "uf": uf,
                "estado": NOMES[uf],
                "valor": None,
                "data_cotacao": None
            }))

    if sucessos == 0:
        raise RuntimeError(
            "Nenhuma cotação válida recebida. Arquivo não atualizado."
        )

    resultado = {
        "atualizado_em": datetime.now(timezone.utc).isoformat(),
        "fonte": "AgroDoc AI",
        "cotacoes": cotacoes
    }

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"Cotações recebidas com sucesso: {sucessos}")

if __name__ == "__main__":
    main()

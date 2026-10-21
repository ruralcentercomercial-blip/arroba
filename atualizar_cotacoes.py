#!/usr/bin/env python3
"""Atualiza uma vez ao dia as cotações por UF usando a API pública AgroDoc."""
import json, os, urllib.request, urllib.error
from datetime import datetime, timezone

URL = "https://agrodocai.com.br/api/v1/cotacao?uf={uf}"
UFS = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]
NOMES = {"AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas","BA":"Bahia","CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás","MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul","MG":"Minas Gerais","PA":"Pará","PB":"Paraíba","PR":"Paraná","PE":"Pernambuco","PI":"Piauí","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte","RS":"Rio Grande do Sul","RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina","SP":"São Paulo","SE":"Sergipe","TO":"Tocantins"}

def get_json(url):
    req=urllib.request.Request(url, headers={"User-Agent":"RuralCenterCotacao/1.0","Accept":"application/json"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))

def main():
    path="cotacoes.json"
    try:
        with open(path,encoding="utf-8") as f:
            previous=json.load(f)
    except (OSError, ValueError):
        previous={"cotacoes":[]}
    old={x.get("uf"):x for x in previous.get("cotacoes",[])}
    out=[]
    success=0
    for uf in UFS:
        try:
            data=get_json(URL.format(uf=uf))
            # A API documenta campos valor/uf/data_cotacao para consulta por UF.
            valor=data.get("valor")
            if valor is None:
                # Algumas respostas podem devolver o valor no campo geral.
                valor=data.get("boi_gordo_cepea_sp") if uf=="SP" else None
            if isinstance(valor,(int,float)) and valor>0:
                out.append({"uf":uf,"estado":NOMES[uf],"valor":float(valor),
                            "data_cotacao":data.get("data_cotacao") or data.get("atualizado") or data.get("atualizado_em"),
                            "fonte":data.get("fonte","AgroDoc AI")})
                success+=1
            else:
                out.append(old.get(uf,{"uf":uf,"estado":NOMES[uf],"valor":None,"data_cotacao":None}))
        except Exception as exc:
            print(f"Falha em {uf}: {exc}")
            out.append(old.get(uf,{"uf":uf,"estado":NOMES[uf],"valor":None,"data_cotacao":None}))
    # Se a API falhar por completo, preserva o último arquivo válido.
    if success == 0:
        raise SystemExit("Nenhuma cotação válida retornada; arquivo anterior preservado.")
    result={"atualizado_em":datetime.now(timezone.utc).isoformat(),"fonte":"AgroDoc AI","cotacoes":out}
    with open(path,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(f"Atualizadas {success} cotações de UF.")

if __name__=="__main__":
    main()

# Rural Center — cotação do boi gordo por estado

Esta pasta contém uma página para publicar no GitHub Pages e incorporar na Loja Integrada por iframe. A tabela lê o arquivo estático `cotacoes.json`; o navegador do visitante NÃO consulta a API de cotação.

## Como funciona o limite gratuito

O fluxo agendado executa uma vez ao dia e consulta a API uma vez por UF (27 chamadas máximas por execução). O limite informado pela AgroDoc é 100 chamadas por dia por IP. A consulta ocorre pelos servidores do GitHub Actions, não por cada visitante. Se a API não retornar valor válido para um estado, o script preserva o último valor salvo para aquele estado.

> Importante: a disponibilidade real das cotações por UF depende da API. A documentação menciona 18 UFs; os demais estados podem ficar sem preço. Não invente nem preencha manualmente valores ausentes.

## Publicar gratuitamente

1. Entre em https://github.com e crie um repositório público, por exemplo `cotacao-boi-ruralcenter`.
2. Envie todos os arquivos desta pasta mantendo a estrutura, inclusive a pasta `.github/workflows/`.
3. Abra a aba **Actions** do repositório e, se solicitado, habilite os workflows.
4. Abra **Settings → Pages**. Em **Build and deployment**, selecione **Deploy from a branch**, branch `main` e pasta `/(root)`. Salve.
5. Na aba **Actions**, execute manualmente **Atualizar cotação do boi** uma vez (Run workflow). Confira o log e se `cotacoes.json` foi atualizado. O agendamento diário roda às 10:15 UTC (07:15 no horário de Brasília, normalmente).
6. Depois que o Pages publicar o site, abra a URL indicada em **Settings → Pages**. Teste se a tabela mostra os valores e a data.

## Incorporar na Loja Integrada

Quando a página estiver publicada, troque `URL-DO-SEU-GITHUB-PAGES` pela URL real no código abaixo:

```html
<div style="width:100%;max-width:1000px;margin:0 auto;">
  <iframe
    src="URL-DO-SEU-GITHUB-PAGES"
    title="Cotação do boi gordo por estado - Rural Center"
    width="100%"
    height="900"
    style="display:block;width:100%;height:900px;border:0;border-radius:10px;"
    loading="lazy">
  </iframe>
</div>
```

## Observações

- A API é de terceiros. Confira os termos atuais de uso comercial e mantenha a atribuição "AgroDoc AI".
- Os preços são indicativos e podem não representar todas as praças ou condições comerciais.
- O script foi preparado com base na estrutura descrita publicamente pela API; confirme a primeira execução no GitHub Actions antes de divulgar a tabela. Se a API alterar campos ou o formato de resposta, o script precisará ser ajustado.
- Não coloque chaves ou senhas em arquivos públicos. Esta integração não precisa de chave segundo a documentação da versão v1.

# Teste de Saúde Mental e Emocional (N/A)

App gratuito (PWA) com o questionário de autoavaliação e a curva do livro
*A Etiologia da Doença e da Saúde Mental e Emocional*, de Neuróticos Anônimos.

**Endereço do app:** https://app-n-a.github.io

Funciona no navegador de qualquer celular ou computador, pode ser instalado na
tela inicial (Android e iPhone) e funciona sem internet depois do primeiro acesso.

> App independente, feito por membros a serviço da irmandade. Não é uma
> publicação oficial de Neuróticos Anônimos nem do ENABRA.
> As 50 frases foram reescritas com outras palavras, mantendo o sentido de cada
> item do livro; a contagem dos pontos (Sim = 2, Às vezes = 1, Não = 0) e a
> curva seguem o original.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `index.html` | O app inteiro (telas, estilos e lógica) |
| `cofre.js` | O conteúdo do teste **cifrado** e a lista de acessos (login e senha) |
| `sw.js` | Faz o app funcionar sem internet |
| `manifest.json` | Nome, cores e ícones usados na instalação |
| `icons/` | Ícones (tela inicial, aba do navegador) |
| `fonts/` | Fontes Atkinson Hyperlegible e Literata (licença OFL) |
| `ferramentas/gerar_cofre.py` | Gera um `cofre.js` novo a partir do conteúdo e dos acessos |

## Segurança e privacidade

- O conteúdo do teste fica cifrado (AES-256-GCM). A chave só é liberada com um
  login e senha válidos (PBKDF2-SHA256, 310.000 iterações). Quem abrir o
  `cofre.js` no GitHub não consegue ler as frases.
- As respostas, os resultados e as anotações ficam **somente no aparelho** de
  cada pessoa (armazenamento local do navegador). Nada é enviado a servidores.
- O site pede aos buscadores para não ser indexado (`robots.txt` e `noindex`).

## Como criar um login novo (sem programar)

1. Entre no app e abra **Mais > Administrar acessos**.
2. Preencha identificação, login e senha e toque em **Gerar linha do acesso**.
3. Toque em **Copiar linha** e em **Abrir cofre.js no GitHub**.
4. Cole a linha logo abaixo de `"acessos": [` e salve (**Commit changes**).

Para trocar a senha de um login, gere a linha de novo com o mesmo login e
substitua a linha antiga (o campo `"id"` será o mesmo). Para remover um acesso,
apague a linha dele.

## Como mudar as frases ou refazer todos os acessos

Use `ferramentas/gerar_cofre.py` com os arquivos `conteudo.json` (frases) e
`acessos.json` (logins e senhas). **Esses dois arquivos não devem ser
publicados** neste repositório.

```bash
pip install cryptography
python3 ferramentas/gerar_cofre.py --conteudo conteudo.json --acessos acessos.json --saida cofre.js
```

Depois de alterar `index.html` ou `cofre.js`, aumente o número de `VERSAO` em
`sw.js` para que os aparelhos recebam a atualização (o app mostra o aviso
"Há uma versão nova do app").

## Fontes de apoio citadas no app

- CVV — Centro de Valorização da Vida: 188 (gratuito, 24 horas) — https://cvv.org.br
- Neuróticos Anônimos no Brasil — https://neuroticosanonimos.org.br

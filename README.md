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

## Privacidade: nada sai do celular

- **Não existe cadastro, servidor nem conta central.** Quem mantém este
  repositório não tem acesso a logins, senhas ou resultados de ninguém.
- Na primeira vez, cada pessoa cria **o próprio login e senha no próprio
  aparelho**. A senha não é guardada: dela se deriva uma chave
  (PBKDF2-SHA256, 310.000 iterações) que cifra os resultados e as anotações
  (AES-256-GCM) no armazenamento local do navegador.
- Se a senha for esquecida, não há recuperação: a pessoa apaga o acesso no
  próprio app e começa de novo. A cópia de segurança (Mais > Meus dados) é
  opcional e fica com a própria pessoa.
- O app não usa contadores de visita, anúncios nem chamadas a outros sites, e
  pede aos buscadores para não ser indexado (`robots.txt` e `noindex`).

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `index.html` | O app inteiro (telas, estilos e lógica) |
| `conteudo.js` | As 50 frases e as áreas de reflexão |
| `sw.js` | Faz o app funcionar sem internet |
| `manifest.json` | Nome, cores e ícones usados na instalação |
| `icons/` | Ícones (tela inicial, aba do navegador) |
| `fonts/` | Fontes Atkinson Hyperlegible e Literata (licença OFL) |

## Para publicar uma alteração

Depois de alterar qualquer arquivo, aumente o número de `VERSAO` em `sw.js`.
Assim os aparelhos que já usam o app recebem o aviso "Há uma versão nova do app".

## Fontes de apoio citadas no app

- CVV — Centro de Valorização da Vida: 188 (gratuito, 24 horas) — https://cvv.org.br
- Neuróticos Anônimos no Brasil — https://neuroticosanonimos.org.br

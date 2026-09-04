# Proposta: perfil github.com/Esl1h

## Diagnóstico do README atual

| Problema | Impacto |
|---|---|
| Conteúdo em `<details>` aninhado ("Expand for more" → "About") | Dois cliques até qualquer informação real |
| Nenhum repositório ou artigo citado | 63 repos, 32 gists e ~200 posts sem curadoria |
| H1 em Unicode estilizado (`𝙷𝚎𝚕𝚕𝚘`) | Não indexa na busca do GitHub, quebra leitor de tela |
| Bloco PGP completo inline | ~20 linhas de ruído; já linkado em keys.openpgp.org |
| Ícones StackShare / Anchor / Medium / Steam | Anchor virou Spotify for Creators e contas inativas foram deletadas em 17/abr/2026; os demais estão sem uso. Link morto sinaliza abandono |
| `HASHNODE:START/END` órfão | Blog migrou para Astro; workflow morto |
| `blog: esli.cafe` no perfil, `esli.blog.br` no README | O endereço correto é **esli.blog**: inconsistente nos dois lugares |
| Links de artigos apontando para `esli.blog.br/<slug>` | Estrutura do Astro é `esli.blog/posts/<slug>/` |

## Decisões

1. **Conteúdo antes de decoração.** Projetos, gists e séries no topo; `<details>` só para o detalhamento de cada série, background e chaves.
2. **Séries como unidade editorial.** O blog tem ~200 posts; o valor está nas séries (YubiKey 6 partes, SDR/ADS-B 8 partes, DNS criptografado 4, age 4, SRE 12+). A tabela lista série + ponto de entrada; o `<details>` traz a sequência completa.
3. **Gists como diferencial.** Poucos perfis os expõem, e os seus têm valor operacional real (CMDB Steampipe, hardening `sysctl`, prompt SRE).
4. **Painel gerado por Actions, commitado no repo.** Nada de `*.vercel.app` em tempo de renderização.

## Visualização: banner

`assets/hero-dark.svg` + `assets/hero-light.svg`, trocados via `<picture>` + `prefers-color-scheme`.

- Motivo gráfico: campo de barras tipo espectro/perfil de latência: vocabulário do DNSbench e do easy1090.
- Paleta: base tinta `#0E1620`, âmbar `#E8A33D`, ciano `#57A6B8`.
- Tipografia monoespaçada do sistema (`ui-monospace`): SVG carregado via `<img>` no GitHub não busca webfont.
- Estático, sem SMIL/CSS animation: o camo (proxy de imagem do GitHub) é imprevisível com animação.
- ~7 KB cada, versionado no repo.

## Visualização: painel de métricas

Duas actions, ambas commitando SVG no próprio repositório. Nenhuma depende de serviço externo em tempo de leitura do README: se a action parar, o painel congela, mas não quebra.

| Workflow | Action | Gera |
|---|---|---|
| `.github/workflows/metrics.yml` | `lowlighter/metrics@latest` | `metrics/overview.svg` (header, atividade, comunidade, repos, calendário isométrico, linhas alteradas, topics), `metrics/languages.svg` (bytes e commits recentes), `metrics/habits.svg` (horários, dias, indentação, follow-up de PRs/issues) |
| `.github/workflows/summary-cards.yml` | `vn7n24fzkq/github-profile-summary-cards@release` | `profile-summary-card-output/<tema>/{0-profile-details,1-repos-per-language,2-most-commit-language,3-stats,4-productive-time}.svg` |

Divisão de papéis: o `metrics` cobre commits, PRs, issues, calendário e hábitos; os `summary-cards` cobrem a distribuição de linguagens e o horário produtivo, com layout de card que fica bem em duas colunas.

### Tokens

Nenhuma das duas funciona bem com o `GITHUB_TOKEN` padrão: ambas precisam de PAT clássico:

```
Settings → Developer settings → Personal access tokens (classic)

METRICS_TOKEN          scopes: public_repo, read:user, read:org
SUMMARY_GITHUB_TOKEN   scopes: read:user, repo   (repo só se quiser contar privados)
```

Cadastre os dois em `Settings → Secrets and variables → Actions` do repo `Esl1h/Esl1h`.

### Primeira execução

```bash
# os diretórios são criados pelas próprias actions, mas o README referencia
# os caminhos antes disso: rode manualmente para não ficar com imagem quebrada
gh workflow run metrics.yml       -R Esl1h/Esl1h
gh workflow run summary-cards.yml -R Esl1h/Esl1h
gh run watch -R Esl1h/Esl1h
```

### Notas

- Os `cron` estão em UTC: `17 6` e `42 6` = 03:17 e 03:42 em America/Sao_Paulo. Evite `0 0`: é o horário de pico da fila de agendamento do GitHub e atrasa (ou pula) execuções.
- O tema `github_dark` está fixo no README. A action gera vários temas por execução; para trocar, basta mudar o diretório no `<img src>`.
- O `raw.githubusercontent` tem cache; o painel pode levar alguns minutos para refletir uma execução nova.
- Se quiser dark/light também nos cards, o mesmo padrão `<picture>` do banner funciona apontando para `github_dark/` e `github/`.

## Ações fora do README

```
# 1. Estrutura do repo de perfil
Esl1h/Esl1h
├── README.md
├── assets/
│   ├── hero-dark.svg
│   ├── hero-light.svg
│   └── dock/                     # 9 tiles + 2 separadores
├── metrics/                      # gerado pela action
├── profile-summary-card-output/  # gerado pela action
├── .github/workflows/
│   ├── metrics.yml
│   └── summary-cards.yml
└── github-header-image.png       # legado, pode remover

# 2. Pinned repos (Settings → Customize your pins): 6 slots
DNSbench · yubikey-shell-toolkit · easy1090 · vBackups · climabr.app · UAI-FAI

# 3. Topics nos repos (a busca do GitHub indexa topic, não descrição)
gh repo edit Esl1h/DNSbench --add-topic dns,benchmark,vlang,cli,sre
gh repo edit Esl1h/yubikey-shell-toolkit --add-topic yubikey,security,shell,gpg
gh repo edit Esl1h/easy1090 --add-topic adsb,rtl-sdr,archlinux,readsb
gh repo edit Esl1h/vBackups --add-topic backup,encryption,vlang
gh repo edit Esl1h/UAI-FAI --add-topic fedora,ubuntu,post-install,bash

# 4. Perfil (Settings → Public profile)
blog: https://esli.blog             # hoje aponta para esli.cafe
social accounts: blog, LinkedIn, Bluesky, Matrix

# 5. Higiene
gh repo archive Esl1h/go_learning Esl1h/r_learning Esl1h/lua_learning \
                Esl1h/python_learning Esl1h/HenryApp Esl1h/esli-nux_k8s
```

## Automação do feed do blog (opcional)

Se quiser que a seção Writing atualize sozinha, o padrão sem serviço externo é um workflow
agendado reescrevendo um bloco delimitado: o mesmo mecanismo do `HASHNODE:START/END` que
já existia, agora apontando para o Astro:

```yaml
# .github/workflows/blog.yml
on:
  schedule: [{ cron: "0 9 * * 1" }]
  workflow_dispatch:
permissions:
  contents: write
jobs:
  feed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gautamkrishnar/blog-post-workflow@v1
        with:
          feed_list: "https://esli.blog/rss.xml"
          max_post_count: 5
          comment_tag_name: "BLOG"
```

Só adicione os marcadores `<!-- BLOG:START -->` / `<!-- BLOG:END -->` se for ativar o
workflow. Marcador sem workflow é exatamente o que está no README hoje.

---

## Links recuperados do histórico

O `README.md` tem 253 commits desde 2020-07-06. Rodando `git log -p` (ou lendo os blobs
em `raw.githubusercontent.com/Esl1h/Esl1h/<sha>/README.md`) dá para ver o que foi caindo:

```bash
git log --format='%h %ad %s' --date=short -- README.md
git show 10077437:README.md | grep -oP 'href="\K[^"]+'
```

| Link | Último SHA em que aparece | Situação | Decisão |
|---|---|---|---|
| stackoverflow.com/users/4122311/esli-silva | `34c98afd` (2022-08) | ativo | **volta** (dock) |
| stackexchange.com/users/4974728 | `fd5507f2` (2021-09) | ativo | volta (dock + flair opcional) |
| t.me/Esl1h | `10077437` (2020-12) | ativo | fica fora: canal privado |
| reddit.com/user/Esl1h | `10077437` | ativo | fica fora |
| youtube.com/@eslih | `b578bae8` (2022-11) | ativo | volta |
| x.com/esl1h | `0c3b7f66` (2025-06) | ativo | volta |
| bsky.app/profile/esli.blog.br | nunca esteve no README | ativo (está no blog) | fica fora |
| esli.blog/posts/git/ (GitLab, Codeberg, Radicle) | nunca | ativo | entra como `mirrors` |
| instagram.com/eslihs90 | `10077437` | ativo | fica fora: canal pessoal |
| steamcommunity.com/id/esl1h | `10077437` | ativo | fica fora: dilui perfil técnico |
| medium.com/@esl1h | `10077437` | sem publicação | fora |
| anchor.fm/esl1h | `10077437` | plataforma virou Spotify for Creators; contas inativas deletadas em 17/abr/2026 | fora |
| stackshare.io/Esl1h | `34c98afd` | perfil existe, sem manutenção | fora |
| cloudacademy.com/profile/… | `10077437` | perfil de aluno | fora |
| flowcrypt.com/me/esli | `10077437` | redundante com keys.openpgp.org | fora |
| esli-nux.com | `10077437` | domínio antigo | fora |
| twitter.com/esli_nux | `10077437` | handle antigo | fora |
| visitor-badge.glitch.me | `10077437` | Glitch encerrou o serviço | fora |

Os 9 que voltam ficam no dock. Os que ficam de fora seguem existindo: só não competem por
atenção no topo da página.

---

## Visualização: dock

`assets/dock/*.svg`: 9 tiles + 2 separadores, gerados por `gen_dock.py`.

### Como funciona

O GitHub não aplica CSS no README e não executa link dentro de SVG carregado via `<img>`.
Então o dock não pode ser um SVG único: cada tile é um arquivo, embrulhado em seu próprio
`<a href title>`.

A prateleira contínua vem de um truque: **os 14 px inferiores de cada tile são uma faixa
que ocupa a largura inteira do arquivo**. Quando os `<a>` são escritos colados, sem espaço
nem quebra de linha entre eles, o navegador não insere gap entre inline elements e as faixas
se emendam numa prateleira só. Uma quebra de linha no meio do bloco quebra o efeito: é o
único cuidado de manutenção.

```html
<!-- certo -->
<a href="..."><img src="./assets/dock/01-blog.svg" height="46"></a><a href="..."><img ...></a>

<!-- errado: o espaço vira um buraco na prateleira -->
<a href="..."><img ...></a>
<a href="..."><img ...></a>
```

### Decisões de desenho

- **Sem logotipo de marca.** Monogramas em monoespaçada (`blog`, `s.o.`, `bsky`, `pgp`) em vez
  de ícones. Evita reproduzir marca registrada, dispensa CDN de ícones (o `simple-icons` via
  jsDelivr do README antigo é dependência externa em tempo de renderização) e combina com a
  tipografia do banner.
- **Um único arquivo por tile, sem `<picture>`.** As cores são neutras com opacidade baixa
  (`#7F8D9B` a 10-30%) mais um âmbar de acento, então os mesmos SVGs funcionam no tema claro
  e no escuro sem duplicar os arquivos.
- **Ponto âmbar sob blog, s.o. e LinkedIn**: o indicador de "app aberto" de dock de verdade,
  usado aqui para marcar os canais principais. Sem legenda: quem conhece dock entende.
- **Separadores** dividem publicação / social / chaves, como a divisória entre apps fixados e
  bandeja do sistema.
- **Tooltip** vem do atributo `title` do `<a>`; `alt` no `<img>` cobre leitor de tela. Os
  separadores têm `alt=""` para não serem anunciados.
- Altura de 46 px no README (os arquivos são 76×92, então renderizam em 2x: nítido em tela
  Retina).

### Manutenção

```bash
python3 gen_dock.py          # regenera os SVGs e imprime dock-snippet.html
```

Para adicionar ou remover um canal, edite a lista `ITEMS` no script e cole o
`dock-snippet.html` gerado no lugar do bloco atual do README. A numeração dos arquivos é
recalculada, então rode `git status` para remover órfãos.

### Alternativa: menu de aplicativos

Se preferir um menu tipo lançador de aplicativos (KDE/GNOME) em vez de dock, o mesmo conjunto
de tiles funciona numa grade: só troca o wrapper por uma tabela e some a prateleira:

```html
<table align="center"><tr>
  <td align="center"><a href="..."><img src="./assets/dock/01-blog.svg" height="52"></a><br><sub>blog</sub></td>
  <td align="center"><a href="..."><img src="./assets/dock/02-so.svg" height="52"></a><br><sub>stack overflow</sub></td>
</tr><tr>
  ...
</tr></table>
```

Para isso, gere os tiles com `SHELF_TOP = H` (elimina a faixa) e use rótulo em `<sub>` embaixo
de cada célula. Ocupa mais altura vertical, ganha em legibilidade dos nomes. O dock é mais
compacto e cabe logo abaixo do banner sem empurrar os projetos para baixo da dobra.

---

## Validação e correções (segunda passada)

Este documento e o README foram redigidos numa sessão anterior do Claude Code (CLI), cujos
arquivos ficaram como artefatos soltos em `~/Área de trabalho/files/` (README.md, PROPOSTA.md,
gen_dock.py, dock-preview.png e três `.zip` de rodadas intermediárias), sem nunca terem sido
copiados para o repositório `~/GIT/Esl1h` nem commitados. Antes de usar esse material como base
definitiva, validei tudo de novo com acesso real a `gh api`, `curl` e ao histórico git local:

- **61 links de posts** citados no README (`grep -oE` sobre todas as URLs `esli.blog/posts/...`):
  todos retornam 200.
- **16 repositórios** citados: todos existem via `gh api repos/Esl1h/<nome>`, incluindo
  `sysz-ng`, que é um fork (`joehillen/sysz`) mas com desenvolvimento próprio substancial (9 PRs
  do autor, rebrand para v2.1.0, filtragem por tiers), então a escolha de incluí-lo no
  README apesar de ser fork está correta.
- **7 gists** citados: todos existem via `gh api gists/<id>`.
- **5 SHAs** citados na tabela "Links recuperados do histórico" (`34c98afd`, `fd5507f2`,
  `10077437`, `0c3b7f66`, `b578bae8`): todos existem no histórico real do `README.md` do repo.
- **Domínio do blog**: confirmado, `esli.blog` está no ar, `esli.blog.br` responde 301 para lá, e
  `esli.cafe` (valor atual do campo "Website" do perfil GitHub) é uma landing page separada.

Duas correções feitas nesta passada, por serem erros reais e não escolhas de estilo:

1. **`metrics.yml` tinha um gatilho `on: push: branches: [main]` além do `schedule`.** As três
   jobs commitam com um PAT real (não o `GITHUB_TOKEN` padrão), e pelo menos uma delas
   (`plugin_isocalendar`, que muda todo dia por só existir) tende a gerar um SVG diferente a cada
   execução. Push de uma job aciona a própria action de novo pelo gatilho `push`, o que é loop
   potencial. Removido; sobra `schedule` + `workflow_dispatch`.
2. **`summary-cards.yml` original (da primeira tentativa desta sessão, antes de eu achar os
   arquivos da sessão anterior) usava inputs inventados (`template`, `card`) que não existem na
   action `vn7n24fzkq/github-profile-summary-cards`.** Os inputs reais (`USERNAME`,
   `BRANCH_NAME`, `UTC_OFFSET`, `EXCLUDE`, `AUTO_PUSH`, `THEME`) foram confirmados lendo o
   `action.yml` publicado no repositório da action. A versão da sessão anterior já usava os
   inputs corretos; adicionei apenas `THEME: github_dark` para não gerar todos os temas
   (o README só exibe um).

Também refeitos, por exigência do `~/.claude/CLAUDE.md` do usuário (proibição de travessão como
pontuação): todo travessão em `README.md` e neste arquivo foi reescrito com vírgula, dois-pontos
ou reestruturação de frase. Os SVGs do hero na sessão anterior vieram com um manifesto C2PA de
proveniência de conteúdo embutido (~14 KB de metadado, quase o dobro do tamanho do arquivo) e
`aria-label` com travessão; regenerei o mesmo desenho (curva de sino, grade, chips de stack, cores
`#0E1620`/`#E8A33D`/`#57A6B8`) via `scripts/gen_assets.py`, sem esse metadado e sem travessão.

O `dock-snippet.html` e os nomes de arquivo em `assets/dock/*.svg` da sessão anterior batem
exatamente com o que `scripts/gen_assets.py` (que incorporou a lógica de `gen_dock.py`) gera
agora, então o bloco de dock no README não precisou de nenhum ajuste além dos travessões.

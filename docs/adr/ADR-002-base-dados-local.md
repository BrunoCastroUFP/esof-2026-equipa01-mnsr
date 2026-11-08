# ADR-002: Base de dados local no telemóvel com IndexedDB e Service Worker
- **Estado:** Aceite
- **Data:** 2026-11-08
- **Decisores:** Equipa 01

## Contexto
- ADR-001 escolheu uma PWA que funciona sem rede
- Sem rede, o visitante tem de ver os roteiros já gerados, as obras e o mapa, e continuar a caça ao tesouro (RNF-02)
- Não podemos guardar dados pessoais de menores (RNF-03)
- Acervo muda pouco, mas muda: uma obra pode ir para restauro ou mudar de sala

## Alternativas consideradas
1. **localStorage:** guarda pares chave–valor só em texto. Rejeitada: tem pouco espaço (cerca de 5 MB) e é síncrono, por isso bloqueia o ecrã enquanto lê ou escreve.
2. **IndexedDB:** base de dados do browser que guarda objetos, com índices para pesquisar e sem bloquear o ecrã.
Escolhida para os dados, que a app pesquisa e altera durante a visita.
3. **Cache Storage do Service Worker:** guarda cópias dos ficheiros pedidos à rede e devolve-as quando não há ligação.
Escolhida para os ficheiros (a app, as imagens das obras e o mapa). Não serve para os dados, porque não permite pesquisar.
4. **SQLite no telemóvel:** só existe numa app nativa, que a ADR-001 rejeitou. Rejeitada.

## Decisão
- IndexedDB guarda: obras, roteiros gerados, progresso da caça ao tesouro (anónimo) e o perfil escolhido (criança, jovem ou perito)
- o Service Worker guarda na Cache Storage: a própria app, as imagens das obras e o mapa
- os dados descarregam-se quando há rede, com um número de versão do acervo; só se descarregam de novo quando a versão muda
- nunca se guarda no telemóvel: nome, email, idade, data de nascimento, tokens, chaves

## Consequências
- Positivas: funciona sem rede; os dados ficam no telemóvel e não identificam ninguém
- Negativas: é preciso gerir a versão do acervo e atualizar a cópia local
- Riscos:
   - o browser pode apagar os dados se o telemóvel ficar sem espaço: pedir armazenamento persistente e voltar a descarregar quando faltarem
   - qualquer script que corra na página consegue ler o IndexedDB: uma falha de XSS expõe tudo o que lá estiver, por isso nunca se guardam segredos

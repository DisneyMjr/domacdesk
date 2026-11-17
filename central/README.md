# Central DomacDesk

Página de downloads e configuração pública da rede própria, em um Worker gratuito separado. Não é cliente web de acesso remoto e não executa `hbbs`/`hbbr`.

Publicação: https://domacdesk-central.disneymjr.workers.dev. Servidor de conexão/relay e teste entre dois dispositivos continuam pendentes.

```sh
npm ci
npm test
npm run dev
npm run deploy
```

`npm run deploy` exige autorização Wrangler da conta correta. Não habilitar plano pago nem alterar o Worker da agência. O nome do Worker é `domacdesk-central`.

A página não coleta dados de contato, senhas ou certificados e não usa analytics/fontes externas. Sem as variáveis `ID_SERVER`, `RELAY_SERVER`, `SERVER_PUBLIC_KEY`, mostra o servidor como pendente e desabilita copiar configuração. Variáveis incompletas são recusadas, sem fallback público na API da central. A chave privada nunca deve entrar na configuração do Worker.

`GET /api/health` verifica apenas a central; `GET /api/config` informa configuração, sem garantir disponibilidade de sessões. Todos os endpoints da central são somente leitura. A origem dos downloads é a pré-release própria já distribuída; não houve nova compilação dos clientes nesta etapa.

Para ativação real, seguir [servidor próprio](../deploy/server/README.md). O cliente já instalado não migra automaticamente ao visitar a página. Concluir somente após uma sessão direta e por relay testada em duas redes distintas.

# DomacDesk

Software de acesso remoto, derivado de um projeto livre sob licença **GNU AGPL-3.0**.

## Licença
Este projeto mantém a licença **GNU AGPL-3.0** (arquivo `LICENCE`) e os avisos de copyright
originais presentes nos arquivos-fonte. Quem usar a versão modificada por rede tem direito
ao código-fonte correspondente.

## Servidor próprio
Por padrão o app ainda aponta para servidores públicos de terceiros
(`libs/hbb_common/src/config.rs`: `RENDEZVOUS_SERVERS` e `RS_PUB_KEY`).
Para usar uma rede própria, suba os serviços `hbbs`/`hbbr` e troque esses valores.

## Build
Veja `build.py` e a pasta `docs/`.

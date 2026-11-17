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

Consulte [configuração, preservação de dados e testes](docs/DOMACDESK-SETUP.md)
para preparar o servidor, assinaturas, dependências nativas e atualizações.

## Distribuição (Windows, Android e Linux)
Os instaladores são gerados pelo GitHub Actions e publicados em **Releases**.

1. Em *Settings > Actions > General > Workflow permissions*, marque **Read and write permissions**.
2. Gere uma release criando uma tag:
   ```bash
   git tag v1.5.3
   git push origin v1.5.3
   ```
   Ou use *Actions > Release DomacDesk > Run workflow*.
3. Ao terminar (leva de 1 a 2 horas), a release terá:
   - **Windows:** `.exe` e `.msi` para x64 e ARM64
   - **Android:** APKs por arquitetura e APK universal
   - **Linux:** pacotes `.deb` e AppImage

Para assinar o APK, cadastre em *Settings > Secrets and variables > Actions* os segredos
`ANDROID_SIGNING_KEY`, `ANDROID_ALIAS`, `ANDROID_KEY_STORE_PASSWORD` e `ANDROID_KEY_PASSWORD`.
Sem eles, o APK sai sem a sua assinatura.

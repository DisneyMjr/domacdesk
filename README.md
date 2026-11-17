# DomacDesk

Software de acesso remoto, derivado de um projeto livre sob licença **GNU AGPL-3.0**.

## Licença
Este projeto mantém a licença **GNU AGPL-3.0** (arquivo `LICENCE`) e os avisos de copyright
originais presentes nos arquivos-fonte. Quem usar a versão modificada por rede tem direito
ao código-fonte correspondente.

## Servidor próprio
Por padrão o app ainda aponta para servidores públicos de terceiros
(`libs/hbb_common/src/config.rs`: `RENDEZVOUS_SERVERS` e `RS_PUB_KEY`).
Para usar uma rede própria, suba os serviços `hbbs`/`hbbr` e configure servidor ID,
relay e chave pública nas configurações de rede dos dois clientes, sem recompilar.

## Build
Veja `build.py` e a pasta `docs/`.

Consulte [configuração, preservação de dados e testes](docs/DOMACDESK-SETUP.md)
para preparar o servidor, assinaturas, dependências nativas e atualizações.

## Distribuição (Windows, Android e Linux)
Os instaladores são gerados pelo GitHub Actions e publicados em **Releases**.

1. Os workflows de publicação já declaram `contents: write`; eventuais políticas da organização precisam permitir essa publicação.
2. Gere uma release criando uma **tag nova**, compatível com a versão do código. Nunca reutilize uma tag já distribuída. Por exemplo, para a próxima revisão de `1.5.3`:
   ```bash
   git tag v1.5.3-2
   git push origin v1.5.3-2
   ```
   Ou use *Actions > Release DomacDesk > Run workflow*.
3. Ao terminar (leva de 1 a 2 horas), a release terá:
   - **Windows:** `.exe` e `.msi` para x64 e ARM64
   - **Android:** APKs por arquitetura e APK universal, quando o keystore definitivo estiver configurado
   - **Linux:** pacotes `.deb` e AppImage

Para assinar o APK, cadastre em *Settings > Secrets and variables > Actions* os segredos
`ANDROID_SIGNING_KEY`, `ANDROID_ALIAS`, `ANDROID_KEY_STORE_PASSWORD` e `ANDROID_KEY_PASSWORD`.
Sem eles, APKs com a chave de depuração do runner ficam somente como artefatos
`diagnostic-debug-signed-android-*` no Actions, sem publicação em Releases.
Esses artefatos não oferecem uma identidade estável para atualizar instalações
existentes. Preserve o keystore original e não desinstale para contornar uma
incompatibilidade de assinatura.

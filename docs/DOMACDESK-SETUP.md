# Configuração e validação do DomacDesk

O cliente deriva de [rustdesk/rustdesk](https://github.com/rustdesk/rustdesk).
A interface atual é Flutter; captura, entrada, áudio, transferência e rede são
implementados em Rust. Este repositório contém o cliente, não os serviços `hbbs`
e `hbbr`. A interface web completa depende de código JavaScript que não está
versionado; este checkout não fornece um cliente web funcional.

## Dados existentes

As correções não alteram os diretórios de configuração, IDs, senhas, contatos,
identificadores Android, formatos persistidos ou rotinas de migração. Não apague
configurações para instalar uma atualização. Antes de atualizar uma instalação
real, faça backup da pasta de configuração do DomacDesk e mantenha o instalador
anterior. Não execute testes de configuração contra os dados de produção.

Mantenha o mesmo `applicationId` e o mesmo keystore Android para atualizar uma
instalação existente. Trocar a assinatura impede a atualização; desinstalar para
contornar isso pode apagar os dados do aplicativo.

## Servidor para acesso remoto

Para operar uma infraestrutura própria, disponibilize `hbbs` (registro e
conexões) e `hbbr` (relay) em um servidor acessível pelos dois computadores.
Nos dois clientes, abra as configurações de rede e informe o mesmo servidor ID,
o relay e a chave pública `id_ed25519.pub` do seu servidor. Não distribua a chave
privada. Não é necessário recompilar para configurar esses campos.

As portas padrão são TCP 21115–21117 e UDP 21116. TCP 21118–21119 só é necessário
para clientes web; API/console dependem da edição do servidor. Configure firewall,
DNS e encaminhamento de portas conforme a [documentação do servidor](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/install/).
Preserve o banco e o par de chaves do servidor em armazenamento persistente.
O fallback atual do código continua sendo o servidor público do RustDesk;
disponibilidade e autorização desse serviço não são controladas pelo DomacDesk.

Permissões do sistema também são necessárias: captura de tela e acessibilidade
no macOS; autorização de captura/acessibilidade no Android; serviço e elevação
no Windows para controlar telas elevadas. No Linux, captura depende da sessão,
do compositor e das permissões disponíveis.

## Compilação e testes

Os workflows `CI` e `Full Flutter CI` acompanham `main` e pull requests. O primeiro
compila o cliente e testa `hbb_common` e `base`; o segundo gera a ponte Rust/Dart,
compila as plataformas e executa os testes Windows Rust e Linux Flutter.
`Validate update tooling` executa a suíte Python, inclusive a validação dos
fixtures criptográficos Rust, sem precisar compilar o cliente inteiro.

```sh
cargo metadata --locked --format-version 1
DOMACDESK_TEST_CONFIG_DIR=/tmp/domacdesk-tests cargo test --locked -p hbb_common -p base --lib
python -m pip install --only-binary=:all: --require-hashes -r res/update/update_metadata_requirements.txt
python -m unittest discover -s res/update -p 'test_*.py'
```

No PowerShell, defina `$env:DOMACDESK_TEST_CONFIG_DIR` para uma pasta temporária
antes dos testes de configuração. Esse override só é compilado na suíte
de testes do `hbb_common`; não muda o armazenamento do aplicativo distribuído.

O arquivo de requisitos Python com hashes é específico para o runner Linux
x86_64/Python 3.12. Em outra plataforma, use um ambiente separado com uma versão
compatível de `cryptography`; não reutilize esses hashes de wheels Linux.

Para compilar a interface nativa, use as versões e etapas dos workflows:
Flutter 3.24.5 nos destinos padrão; Flutter 3.44 nos destinos ARM64 indicados;
ponte `flutter_rust_bridge` 1.80.1; bibliotecas nativas pelo vcpkg no commit
definido em `vcpkg.json`; SDKs da plataforma e compilador C/C++.
No Windows, execute em um Developer Command Prompt com Visual C++ e Windows SDK.
Os arquivos da ponte são gerados pelo CI e não estão versionados. Apenas executar
`flutter test` em um clone novo, sem preparar a ponte, não valida o aplicativo.

## Distribuição e assinaturas

O workflow `Release DomacDesk` publica instaladores e requer permissão
`contents: write`. Tags estáveis são releases normais; `nightly` e tags com
sufixo são pré-releases. Use uma tag nova e compatível com a versão do código;
não reutilize tags de versões já distribuídas.

Para Android, configure os secrets `ANDROID_SIGNING_KEY` (keystore em base64),
`ANDROID_ALIAS`, `ANDROID_KEY_STORE_PASSWORD` e `ANDROID_KEY_PASSWORD`.
Sem esses secrets, o APK de release é publicado sem assinatura de distribuição
e precisa ser assinado antes de ser instalado. Preserve o keystore existente.
Assinatura de executáveis Windows depende de certificado/serviço externo;
o workflow usa `SIGN_BASE_URL` e `SIGN_SECRET_KEY` quando configurados.

Os componentes binários externos mantêm seus identificadores técnicos RustDesk:
classe da janela de privacidade, nome do arquivo INF e nome do driver de impressão.
A marca exibida e o diretório de empacotamento continuam DomacDesk. Renomear
esses identificadores sem reconstruir os componentes quebra a integração.

## Atualização automática assinada

A descoberta consulta as releases estáveis de `DisneyMjr/domacdesk` pelo GitHub.
Downloads e metadados ficam restritos a esse repositório; não há fallback para
instalar uma release do RustDesk. A instalação continua exigindo metadados
Ed25519 válidos e verificação de hash.

O workflow de release está configurado com `publish-update-metadata: false`.
Ele não gera atualmente os arquivos assinados de atualização. Para ativar a
instalação automática, primeiro estabeleça uma chave Ed25519 própria, substitua
a chave pública herdada em `src/update_metadata.rs` e distribua essa versão do
cliente. Armazene a seed privada de 32 bytes em base64 no secret
`DOMACDESK_UPDATE_ED25519_SEED` e a chave pública correspondente em base64 na
variável `DOMACDESK_UPDATE_ED25519_PUBLIC_KEY`. Nunca publique a seed privada.

Use `res/update/generate_update_metadata.py check-key` para conferir as chaves.
Os subcomandos `sign --help` e `verify --help` documentam a criação e a verificação
de `domacdesk-update.json` e `domacdesk-update.json.sig`. Gere os metadados dos
instaladores finais e publique os dois arquivos na mesma release, com a base
`https://github.com/DisneyMjr/domacdesk/releases/download` e package ID
`domacdesk`. O input existente de publicação apenas valida a chave; sozinho
não publica esses arquivos. Até concluir essa configuração, instale atualizações
manualmente pelas Releases; não desative a verificação de assinatura.

## Verificação operacional pendente

Compilar e passar testes não comprova uma sessão remota real. Depois de configurar
o servidor, valide em duas máquinas: conexão por ID, senha/aprovação, teclado,
mouse, vídeo, áudio, transferência de arquivos, relay forçado, reconexão e
persistência das configurações após reiniciar. Valide separadamente impressão,
modo de privacidade e instalação por cima da versão anterior com backup.

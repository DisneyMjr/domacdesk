# Rede própria DomacDesk — ativação pendente

Esta pasta prepara os serviços OSS de registro (`hbbs`) e retransmissão (`hbbr`) em infraestrutura controlada pelo responsável. Ela **não cria uma VM, não altera clientes e não abre portas automaticamente**. Ainda é necessário instalar e testar os serviços em um servidor real. O cliente e o servidor preservam os créditos e licenças dos projetos livres de origem; independência do serviço público não significa reescrever todo o software.

## Infraestrutura gratuita a avaliar

O responsável informou não possuir computador/servidor disponível e aceitou criar uma conta gratuita Oracle Cloud. O cadastro e a verificação são feitos diretamente pelo titular no [site oficial](https://signup.cloud.oracle.com/); nunca enviar senha, cartão, códigos ou chaves privadas pelo chat ou GitHub.

Use exclusivamente uma VM e imagem marcadas **Always Free elegíveis**, na região home, respeitando as cotas de computação e armazenamento. Não converter a conta para Pay As You Go, nem usar recursos pagos cobertos apenas por crédito temporário. Capacidade pode estar indisponível e instâncias ociosas podem ser recuperadas pelo provedor; mantenha backup independente. Veja os [limites oficiais vigentes](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm). Não há garantia de disponibilidade contínua ou obtenção de uma VM gratuita.

## Preparar a VM

1. Após o cadastro, selecionar uma VM Linux elegível, com IP público e acesso SSH por chave do responsável. Conferir elegibilidade gratuita também do disco e da imagem. Nenhuma VM foi criada nesta entrega.
2. Instalar Docker Engine e Docker Compose pelo [procedimento oficial da distribuição](https://docs.docker.com/engine/install/). Não executar instalação como parte de um comando copiado do portal sem conferir o destino.
3. Copiar `compose.yml` e `.env.example` para uma pasta dedicada. Criar `.env` a partir do exemplo e definir somente o IP público ou hostname da VM em `DOMACDESK_PUBLIC_HOST`, sem protocolo e sem porta. Não usar o endereço `workers.dev` nesse campo. Se houver DNS Cloudflare, o registro do servidor TCP/UDP deve ficar **DNS only**; proxy HTTP comum não encaminha essas portas.
4. Preparar o diretório persistente com permissões restritas, **preservando qualquer conteúdo existente**. Nunca apagar `data` para resolver erro de configuração. Os comandos abaixo assumem uma instalação nova, na pasta dedicada:

   ```sh
   umask 077
   mkdir -p data
   docker compose config --quiet
   docker compose pull
   docker compose up -d hbbs
   ```

5. Confirmar que `data/id_ed25519` e `data/id_ed25519.pub` foram gerados e que `hbbs` iniciou sem erro, antes de iniciar o relay:

   ```sh
   test -s data/id_ed25519.pub && docker compose up -d hbbr
   docker compose ps
   ```

   A imagem oficial 1.1.16 foi fixada por digest do registro. `-k _` exige a chave do servidor nos dois serviços; ambos compartilham o mesmo diretório persistente. Não use a chave privada como variável da central.
6. Abrir no firewall da VM e na rede OCI **TCP 21115, 21116, 21117 e UDP 21116**. Manter SSH restrito ao IP administrativo. Não expor 21114 (console Pro), 21118 e 21119 (WebSocket), que não são necessários neste cenário. O Compose publica somente as quatro portas necessárias; não desative o firewall inteiro.
7. Fazer backup protegido de `data`, que contém banco e chave privada. Não versionar esse diretório. Atualizações devem preservar as mesmas chaves; a substituição da chave exige redistribuição consciente aos clientes.

## Ligar a central Cloudflare

A central em `central/` está separada do servidor de sessão e do site Agência Ilustre. Não recebe tela, senhas de sessão nem chaves privadas. Seu endpoint `/api/config` publica apenas endereço ID, relay e chave **pública**, depois de configurados pelo responsável.

No painel Cloudflare do Worker `domacdesk-central`, cadastrar estas variáveis públicas:

- `ID_SERVER`: IP/hostname da VM, com porta `21116`.
- `RELAY_SERVER`: IP/hostname da VM, com porta `21117`.
- `SERVER_PUBLIC_KEY`: conteúdo de `data/id_ed25519.pub`, sem espaços/quebras de linha.

Não definir os valores antes de verificar o servidor. A central indica **configuração cadastrada, não verificada**; isso não equivale a uma sessão funcional. Ela não testa UDP nem valida o tráfego do cliente.

Nos dois aplicativos DomacDesk, preencher os mesmos campos em Configurações → Rede → Servidor ID/Relay. Deixar Servidor API vazio para OSS sem API. Preservar ID, senhas e contatos existentes; não importar arquivos genéricos sobre a configuração inteira. O cliente distribuído mantém o fallback público quando nenhum servidor próprio é definido; publicar a central não muda o aplicativo instalado automaticamente.

## Critério de conclusão

A rede só pode ser considerada ativa depois de: registro de dois dispositivos em redes diferentes, confirmação da chave, sessão autorizada com visualização/controle, teste de conexão forçada por relay e reinício dos serviços preservando a chave/banco. Até lá, declarar o acesso remoto como **pendente**, mesmo que a página carregue ou apareça “Pronto” no aplicativo.

Referências: [implantação OSS](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/), [limitação TCP dos Workers](https://developers.cloudflare.com/workers/runtime-apis/tcp-sockets/). Workers serve a página; os processos de sessão executam na VM. Não foi contratado serviço pago.

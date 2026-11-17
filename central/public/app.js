let config;
const node = (id) => document.getElementById(id);
async function load() {
  try {
    const response = await fetch("/api/config", { cache: "no-store" });
    if (!response.ok) throw Error("config");
    config = await response.json();
    if (!config.configured) {
      node("status-title").textContent =
        "Servidor de conexão ainda não configurado";
      node("status-detail").textContent =
        "A central está disponível. O acesso remoto próprio depende da instalação dos serviços de conexão e relay.";
      return;
    }
    node("status-title").textContent =
      "Configuração cadastrada · conexão ainda precisa ser testada";
    node("status-detail").textContent =
      "Estes dados não comprovam que as portas estão acessíveis. Configure os dois aplicativos e valide uma sessão real.";
    node("network-state").textContent =
      "Configuração cadastrada, sem teste de sessão";
    node("config-note").textContent =
      "Use os mesmos dados nos dois aplicativos. Confira a chave pública antes de conectar.";
    node("id-server").textContent = config.idServer;
    node("relay-server").textContent = config.relayServer;
    node("public-key").textContent = config.publicKey;
    node("copy-config").disabled = false;
  } catch {
    node("status-title").textContent =
      "Não foi possível consultar a configuração";
    node("status-detail").textContent =
      "Nenhum servidor alternativo foi selecionado. O responsável precisa conferir a configuração da central.";
  }
}
node("copy-config").addEventListener("click", async () => {
  if (!config?.configured) return;
  try {
    await navigator.clipboard.writeText(
      `Servidor ID: ${config.idServer}\nServidor relay: ${config.relayServer}\nChave pública: ${config.publicKey}\nServidor API: deixe vazio (OSS sem API)`,
    );
    node("copy-result").textContent =
      "Dados copiados. Cole cada valor no campo correspondente do aplicativo.";
  } catch {
    node("copy-result").textContent =
      "Selecione e copie os campos manualmente; o navegador não permitiu acessar a área de transferência.";
  }
});
void load();

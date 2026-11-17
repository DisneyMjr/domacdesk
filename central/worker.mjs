function endpoint(value) {
  if (typeof value !== "string" || !value || value.includes("://"))
    throw Error("endpoint");
  const url = new URL("http://" + value);
  if (
    !url.hostname ||
    url.username ||
    url.password ||
    url.pathname !== "/" ||
    url.search ||
    url.hash ||
    /\s/.test(value)
  )
    throw Error("endpoint");
  return value;
}
export function connectionConfig(env) {
  const values = [env.ID_SERVER, env.RELAY_SERVER, env.SERVER_PUBLIC_KEY];
  if (values.every((v) => !v))
    return {
      configured: false,
      state: "awaiting_server",
      idServer: null,
      relayServer: null,
      publicKey: null,
    };
  const idServer = endpoint(env.ID_SERVER),
    relayServer = endpoint(env.RELAY_SERVER);
  if (
    typeof env.SERVER_PUBLIC_KEY !== "string" ||
    !/^[A-Za-z0-9+/]{43}=$/.test(env.SERVER_PUBLIC_KEY) ||
    atob(env.SERVER_PUBLIC_KEY).length !== 32
  )
    throw Error("key");
  return {
    configured: true,
    state: "configured_unverified",
    idServer,
    relayServer,
    publicKey: env.SERVER_PUBLIC_KEY,
  };
}
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    },
  });
export default {
  async fetch(req, env) {
    const path = new URL(req.url).pathname;
    if (path.startsWith("/api/")) {
      if (req.method !== "GET")
        return json({ error: "Método não permitido." }, 405);
      if (path === "/api/health")
        return json({
          ok: true,
          service: "central",
          connectionState: "not_checked",
        });
      if (path === "/api/config") {
        try {
          return json(connectionConfig(env));
        } catch {
          return json(
            {
              error: "A configuração do servidor está incompleta ou inválida.",
            },
            503,
          );
        }
      }
      return json({ error: "Rota não encontrada." }, 404);
    }
    return env.ASSETS.fetch(req);
  },
};

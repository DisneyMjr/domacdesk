import { test } from "node:test";
import assert from "node:assert/strict";
import worker from "./worker.mjs";
const get = (env) =>
  worker.fetch(new Request("https://central.example/api/config"), env);
test("unconfigured central never advertises a working remote server", async () => {
  const response = await get({});
  assert.equal(response.status, 200);
  const data = await response.json();
  assert.equal(data.configured, false);
  assert.equal(data.state, "awaiting_server");
  assert.equal(data.idServer, null);
  assert.equal(response.headers.get("Cache-Control"), "no-store");
});
test("publishes only explicit public connection settings without claiming health", async () => {
  const key = Buffer.alloc(32, 7).toString("base64");
  const response = await get({
    ID_SERVER: "id.example.com:21116",
    RELAY_SERVER: "relay.example.com:21117",
    SERVER_PUBLIC_KEY: key,
    PRIVATE_KEY: "never-public",
  });
  assert.equal(response.status, 200);
  const data = await response.json();
  assert.equal(data.state, "configured_unverified");
  assert.equal(data.publicKey, key);
  assert.equal(JSON.stringify(data).includes("never-public"), false);
});
test("rejects incomplete settings and URL credentials without a public fallback", async () => {
  for (const env of [
    { ID_SERVER: "id.example.com" },
    {
      ID_SERVER: "user:password@host.example",
      RELAY_SERVER: "host.example",
      SERVER_PUBLIC_KEY: "invalid",
    },
  ])
    assert.equal((await get(env)).status, 503);
  assert.equal(
    (
      await worker.fetch(
        new Request("https://central.example/api/config", { method: "POST" }),
        {},
      )
    ).status,
    405,
  );
});

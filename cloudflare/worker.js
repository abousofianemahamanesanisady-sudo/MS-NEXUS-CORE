// MS NEXUS PRIME — Cloudflare Workers gateway (deployed snapshot)
// This gateway currently uses Cloudflare Workers AI for text inference.
// It is not a proprietary model trained by MS NEXUS.
// Keep secrets in Worker bindings; never place API keys in this file.

const MODEL = "@cf/zai-org/glm-4.7-flash";
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Authorization, Content-Type"
};

const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status,
  headers: { "Content-Type": "application/json; charset=utf-8", ...cors }
});

function authorized(request, env) {
  return Boolean(env.NEXUS_API_KEY) &&
    request.headers.get("Authorization") === "Bearer " + env.NEXUS_API_KEY;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    if (url.pathname === "/health" && request.method === "GET") {
      return json({
        ok: true,
        service: "MS NEXUS AI",
        stage: "gateway-bootstrap",
        runtime: "Cloudflare Workers",
        model: MODEL,
        api_key_configured: Boolean(env.NEXUS_API_KEY)
      });
    }

    if (url.pathname === "/" && request.method === "GET") {
      return new Response("MS NEXUS AI gateway is online. See /health.", {
        headers: { "Content-Type": "text/plain; charset=utf-8" }
      });
    }

    if (url.pathname.startsWith("/v1/") && !authorized(request, env)) {
      return json({ error: { message: "Clé API manquante ou invalide." } }, 401);
    }

    if (url.pathname === "/v1/models" && request.method === "GET") {
      return json({
        object: "list",
        data: [{ id: MODEL, object: "model", owned_by: "cloudflare-workers-ai" }]
      });
    }

    if (url.pathname === "/v1/chat/completions" && request.method === "POST") {
      if (!env.AI) {
        return json({ error: { message: "Moteur IA non configuré." } }, 503);
      }

      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: { message: "JSON invalide." } }, 400);
      }

      if (!Array.isArray(body.messages) || !body.messages.length) {
        return json({ error: { message: "messages est obligatoire." } }, 400);
      }

      const messages = body.messages.slice(-20).map((message) => ({
        role: ["system", "user", "assistant"].includes(message.role)
          ? message.role
          : "user",
        content: typeof message.content === "string"
          ? message.content
          : JSON.stringify(message.content ?? "")
      }));

      try {
        const result = await env.AI.run(MODEL, {
          messages,
          max_tokens: Math.min(Math.max(Number(body.max_tokens) || 512, 1), 2048)
        });

        return json({
          id: "msnexus-" + crypto.randomUUID(),
          object: "chat.completion",
          created: Math.floor(Date.now() / 1000),
          model: MODEL,
          choices: [{
            index: 0,
            message: { role: "assistant", content: result.response ?? "" },
            finish_reason: "stop"
          }]
        });
      } catch (error) {
        return json({
          error: {
            message: "Échec du moteur IA.",
            detail: String(error).slice(0, 240)
          }
        }, 502);
      }
    }

    return json({ error: { message: "Route introuvable." } }, 404);
  }
};

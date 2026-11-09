export default {
  async fetch(request, env) {
    const backend = env.NEXUS_BACKEND_URL;
    if (!backend) {
      return Response.json(
        { error: "NEXUS_BACKEND_URL is not configured. Deploy the model server first." },
        { status: 503 }
      );
    }

    const incoming = new URL(request.url);
    const target = new URL(incoming.pathname + incoming.search, backend);
    const headers = new Headers(request.headers);
    headers.delete("host");

    // The backend validates the user's bearer API key. Never put model/admin secrets here.
    return fetch(new Request(target, {
      method: request.method,
      headers,
      body: ["GET", "HEAD"].includes(request.method) ? undefined : request.body,
      redirect: "manual"
    }));
  }
};

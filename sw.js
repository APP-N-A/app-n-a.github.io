/* Service worker: guarda o app no aparelho para funcionar sem internet.
   Ao publicar uma versão nova, aumente o número em VERSAO. */
const VERSAO = "teste-na-v2.0.0";
const ARQUIVOS = [
  "./", "index.html", "conteudo.js", "manifest.json",
  "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-192.png", "icons/icon-maskable-512.png",
  "icons/apple-touch-icon.png", "icons/favicon-32.png",
  "fonts/atkinson-hyperlegible-latin-400-normal.woff2", "fonts/atkinson-hyperlegible-latin-700-normal.woff2",
  "fonts/atkinson-hyperlegible-latin-400-italic.woff2", "fonts/literata-latin-wght-normal.woff2", "fonts/literata-latin-wght-italic.woff2"
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSAO).then(c => c.addAll(ARQUIVOS.map(u => new Request(u, {cache: "reload"})))));
});

self.addEventListener("activate", e => {
  e.waitUntil((async () => {
    const nomes = await caches.keys();
    await Promise.all(nomes.filter(n => n.startsWith("teste-na-") && n !== VERSAO).map(n => caches.delete(n)));
    await self.clients.claim();
  })());
});

self.addEventListener("message", e => { if (e.data === "atualizar") self.skipWaiting(); });

/* Páginas, scripts e manifesto: tenta a rede primeiro (para receber novos acessos e
   correções) e usa a cópia guardada quando estiver sem internet.
   Fontes e imagens: usa a cópia guardada primeiro. */
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  const dinamico = req.mode === "navigate" || /\.(html|js|json)$/.test(url.pathname) || url.pathname.endsWith("/");
  if (dinamico) {
    e.respondWith((async () => {
      const cache = await caches.open(VERSAO);
      try {
        const controle = new AbortController();
        const prazo = setTimeout(() => controle.abort(), 6000);
        const resp = await fetch(req, {signal: controle.signal, cache: "no-cache"});
        clearTimeout(prazo);
        if (resp && resp.ok && resp.type === "basic") cache.put(req, resp.clone());
        return resp;
      } catch (err) {
        const guardado = await cache.match(req, {ignoreSearch: true});
        if (guardado) return guardado;
        if (req.mode === "navigate") return (await cache.match("index.html")) || Response.error();
        return Response.error();
      }
    })());
  } else {
    e.respondWith((async () => {
      const guardado = await caches.match(req, {ignoreSearch: true});
      if (guardado) return guardado;
      const resp = await fetch(req);
      if (resp && resp.ok && resp.type === "basic") {
        const cache = await caches.open(VERSAO);
        cache.put(req, resp.clone());
      }
      return resp;
    })());
  }
});

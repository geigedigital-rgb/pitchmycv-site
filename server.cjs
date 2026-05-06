'use strict';

/**
 * Static site + SEO redirects for Railway.
 * Seobility expects https://www.pitchcv.app/path → 301 → https://pitchcv.app/path (same path).
 * Plain `serve` ignores Host, so both hostnames returned 200 (duplicate content).
 */

const http = require('http');
const path = require('path');
const fs = require('fs');
const handler = require('serve-handler');

const PORT = Number(process.env.PORT) || 3000;
const ROOT = process.cwd();

const rawCanonical = (process.env.CANONICAL_HOST || 'pitchcv.app').trim().toLowerCase();
const CANONICAL_HOST = rawCanonical.replace(/^https?:\/\//, '').split(':')[0];

function hostHeader(req) {
  const raw = req.headers['x-forwarded-host'] || req.headers.host || '';
  return raw.split(':')[0].toLowerCase();
}

function forwardedProto(req) {
  const raw = req.headers['x-forwarded-proto'] || 'http';
  return String(raw).split(',')[0].trim().toLowerCase();
}

function loadServeJson() {
  const p = path.join(ROOT, 'serve.json');
  try {
    const txt = fs.readFileSync(p, 'utf8');
    return JSON.parse(txt);
  } catch {
    return {};
  }
}

const serveConfig = {
  cleanUrls: true,
  ...loadServeJson(),
  public: ROOT
};

const server = http.createServer(async (req, res) => {
  const host = hostHeader(req);
  const proto = forwardedProto(req);

  const isLocal =
    host === 'localhost' ||
    host === '127.0.0.1' ||
    host === '[::1]' ||
    host.endsWith('.railway.internal');

  if (!isLocal && host === `www.${CANONICAL_HOST}`) {
    const loc = `https://${CANONICAL_HOST}${req.url || '/'}`;
    res.writeHead(301, { Location: loc });
    res.end();
    return;
  }

  if (!isLocal && host === CANONICAL_HOST && proto === 'http') {
    const loc = `https://${CANONICAL_HOST}${req.url || '/'}`;
    res.writeHead(301, { Location: loc });
    res.end();
    return;
  }

  await handler(req, res, serveConfig);
});

server.listen(PORT, () => {
  console.log(`pitchcv-site listening on ${PORT}, canonical https://${CANONICAL_HOST}`);
});

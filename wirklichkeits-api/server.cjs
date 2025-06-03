const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
let lastTrigger = null;

function sendJSON(res, code, data) {
  res.writeHead(code, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(data));
}

function sendFile(res, filePath, contentType) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      sendJSON(res, 404, { error: 'Not found' });
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(data);
    }
  });
}

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/trigger') {
    let body = '';
    req.on('data', chunk => (body += chunk));
    req.on('end', () => {
      try {
        lastTrigger = JSON.parse(body || '{}');
      } catch {
        lastTrigger = null;
      }
      sendJSON(res, 200, { status: 'trigger received' });
    });
    return;
  }

  if (req.method === 'GET' && req.url === '/status') {
    sendJSON(res, 200, { lastTrigger });
    return;
  }

  if (req.method === 'GET' && req.url === '/init/anchors/ankerpunkt.yaml') {
    const filePath = path.join(__dirname, '../../../init/anchors/ankerpunkt.yaml');
    sendFile(res, filePath, 'application/yaml');
    return;
  }

  if (req.method === 'GET' && req.url === '/init/templates/narion_erinnerung_template.yaml') {
    const filePath = path.join(
      __dirname,
      '../../../init/templates/narion_erinnerung_template.yaml'
    );
    sendFile(res, filePath, 'application/yaml');
    return;
  }

  if (req.method === 'GET' && req.url === '/DATENSCHUTZ.md') {
    const filePath = path.join(__dirname, '../../../public/DATENSCHUTZ.md');
    sendFile(res, filePath, 'text/markdown; charset=utf-8');
    return;
  }

  sendJSON(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`Wirklichkeits API running on port ${PORT}`);
});

import { WebSocketServer } from 'ws';
import { spawn } from 'child_process';
import dotenv from 'dotenv';

dotenv.config();

const PORT = process.env.VOICE_PORT || 8080;

const wss = new WebSocketServer({ port: PORT, path: '/speak' });

wss.on('connection', ws => {
  ws.on('message', msg => {
    let data;
    try {
      data = JSON.parse(msg.toString());
    } catch {
      ws.send(JSON.stringify({ error: 'Invalid JSON' }));
      ws.close();
      return;
    }

    const { agent = 'default', text, voice } = data;
    if (!text) {
      ws.send(JSON.stringify({ error: 'Missing text' }));
      ws.close();
      return;
    }

    const args = ['voice_pipeline/pipeline_orchestrator.py', '--agent', agent, '--text', text];
    if (voice) args.push('--voice', voice);

    const proc = spawn('python3', args);
    proc.stdout.on('data', chunk => ws.send(chunk));
    proc.stderr.on('data', err => console.error(err.toString()));
    proc.on('close', () => ws.close());
  });
});

console.log(`🔊 Voice server running on ws://localhost:${PORT}/speak`);

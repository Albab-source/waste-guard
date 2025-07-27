import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { WebSocketServer } from 'ws';

const app = express();
const wss = new WebSocketServer({ port: 8080 });

import webhook from './routes/webhook.js';
import dataSensor from './routes/data_sensor.js';
import alertLogs from './routes/alert_logs.js';
import devices from './routes/devices.js';

app.use(cors());
app.use(express.json()); // untuk menerima JSON
app.use('/webhook', webhook);
app.use('/api/data-sensor', dataSensor);
app.use('/api/alert', alertLogs);
app.use('/api/devices', devices);

// Menyimpan client dashboard yang tersambung
const clients = new Set();

wss.on('connection', (ws) => {
  console.log('WebSocket client connected');
  clients.add(ws);

  ws.on('message', (msg) => {
    // Pesan dari Python Listener diteruskan ke semua client dashboard
    console.log("[WS IN]", msg.toString());

    for (let client of clients) {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(msg.toString());
      }
    }
  });

  ws.on('close', () => {
    clients.delete(ws);
    console.log('Client disconnected');
  });
});

const PORT = process.env.PORT || 9000;
app.listen(PORT, () => {
  console.log(`Server running in http://localhost:${PORT}`);
});


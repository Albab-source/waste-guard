import express from 'express';
import fetch from 'node-fetch';
import db from '../database/db.js'; 
const router = express.Router();

// ----------- KONFIGURASI -----------

const ULTRAMSG_INSTANCE = "instance133324";
const ULTRAMSG_TOKEN = "sqrhgrf580rmam3j";
const ULTRAMSG_PHONE = "+6289630145676";


const send_whatsapp = async (message) => {
  const url = `https://api.ultramsg.com/${ULTRAMSG_INSTANCE}/messages/chat`;
  const payload = {
    token: ULTRAMSG_TOKEN,
    to: ULTRAMSG_PHONE,
    body: message
  };
  try {
    const response = await fetch(url, {
      method: 'POST',
      body: new URLSearchParams(payload)
    });
    const text = await response.text();
    console.log("[WA]", text);
  } catch (e) {
    console.error("[WA ERROR]", e);
  }
};

// POST /webhook
router.post('/', async (req, res) => {
  const token = req.headers['authorization'];
  if (token !== 'Bearer your-secret-token') {
    return res.status(403).send('Unauthorized');
  }

  const { sensorId, topic, value, status } = req.body;

  const query = `
    INSERT INTO alert_logs (sensorId, topic, value, message, status)
    VALUES (?, ?, ?, ?, ?)
  `;
  const values = [sensorId, topic, value, status, 'unread'];
  await send_whatsapp(values[status]);

  try {
    await db.execute(query, values);
    console.log('Data inserted successfully');
    res.status(200).json({ message: 'OK' });
  } catch (err) {
    console.error('DB Error:', err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

export default router;

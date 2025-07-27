import express from 'express';
const router = express.Router();
import db from '../database/db.js';

router.get('/', async(req,res) => {
    try {
        const [rows] = await db.query('SELECT * FROM alert_logs ORDER BY timestamp DESC LIMIT 20');
        res.json(rows); // Kirim data ke client
      } catch (err) {
        res.status(500).json({ error: err.message });
      }
});

router.get('/notif', async(req,res) => {
  try {
      const { limit } = req.query;
      const params = ['unread', Number(limit)]
      const [rows] = await db.query("SELECT * FROM alert_logs WHERE status = ? ORDER BY timestamp DESC LIMIT ? ", params);
      const [counts] = await db.query("SELECT COUNT(*) AS total FROM alert_logs WHERE status = ? ORDER BY timestamp DESC ", params[0]);
      res.json({
        meta : {
          source: 'alert_logs',
          count: counts[0]['total'],
          countType : typeof(rows.length)
        },
        data : rows
      }); // Kirim data ke client
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
});

router.put('/status', async(req, res) => {
  const { status } = req.body;
    try {
      const query = "UPDATE alert_logs SET status = ? Where status = ?"
      const params = [status, 'unread']

      const [rows] = await db.query(query, params);
      console.log('alert status has been updated succesfully! ')

      res.status(201).json(rows);
    }
    catch (err) {
      res.status(500).json({err: err.message})
    }
})

export default router;
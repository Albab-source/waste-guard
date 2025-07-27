import express from 'express';
const router = express.Router();
import db from '../database/db.js';

router.get('/', async(req,res) => {
    try {
        const [rows] = await db.query('SELECT * FROM devices');
        res.json(rows); 
      } catch (err) {
        res.status(500).json({ error: err.message });
      }
});

export default router;
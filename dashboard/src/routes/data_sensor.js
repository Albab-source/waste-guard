import express from 'express';
const router = express.Router();
import db from '../database/db.js';

router.get('/history', async (req, res) => {
  const topic = req.query.topic || 'ph'; // Default topik
  const startDate = req.query.startDate ? `${req.query.startDate} 00:00:00` : '';
  const endDate = req.query.endDate ? `${req.query.endDate} 23:59:59` : '';
  const startTime = req.query.startTime ? req.query.startTime : '00:00:00';
  const endTime = req.query.endTime ? req.query.endTime : '23:59:59';
  const device = req.query.device || '';
  const location = req.query.location || '';
  const page = parseInt(req.query.page) || 1;

  // Validasi topik (hindari SQL injection via nama tabel)
  const allowedTopics = ['ph', 'temperature', 'volume', 'cod'];
  if (!allowedTopics.includes(topic)) {
    return res.status(400).json({ error: 'Topik sensor tidak valid' });
  }

  try {
    let whereClause = 'WHERE 1=1';
    let params = [];

    // Filter tanggal
    if (startDate) {
      whereClause += ' AND ds.timestamp >= ?';
      params.push(startDate);
    }
    if (endDate) {
      whereClause += ' AND ds.timestamp <= ?';
      params.push(endDate);
    }
    
    // Filter Waktu
    if (startTime) {
      whereClause += ' AND TIME(ds.timestamp) >= ?';
      params.push(startTime);
    }
    if (endTime) {
      whereClause += ' AND TIME(ds.timestamp) <= ?';
      params.push(endTime);
    }

    // Filter deviceId
    if (device) {
      whereClause += ' AND d.deviceId LIKE ?';
      params.push(`%${device}%`);
    }

    // Filter lokasi
    if (location) {
      whereClause += ' AND d.location LIKE ?';
      params.push(`%${location}%`);
    }

    // Nama kolom data tergantung topik
    const dataField = topic;

    const query = `
      SELECT 
        d.deviceId,
        d.name,
        d.location,
        ds.timestamp,
        ds.${dataField} AS value
      FROM data_${topic} ds
      JOIN devices d ON d.deviceId = ds.sensorId
      ${whereClause}
      ORDER BY ds.timestamp DESC
    `;

    const [rows] = await db.query(query, [...params]);
    const queryString = [...params];

    res.status(200).json({
      meta: {
        topic,
        count: rows.length,
        query: queryString
      },
      data: rows
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


router.get('/real-time', async (req, res) => {
  // Ambil parameter dari query string
  const device = req.query.device || 'device-001';
  const topic = req.query.topic || 'ph';
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 12;

  const offset = (page - 1) * limit;

  try {
    // Query data
    const query = `SELECT * FROM data_${topic} WHERE sensorId = ? LIMIT ? OFFSET ?`;
    const [results] = await db.query(query, [device, limit, offset]);

    // Query total data
    const queryCount = `SELECT COUNT(*) AS total FROM data_${topic} WHERE sensorId = ?`;
    const [countResult] = await db.query(queryCount, [device]);
    const totalData = countResult[0].total;
    const totalPages = Math.ceil(totalData / limit);

    // Kirim response
    res.status(200).json({
      meta: {
        totalData,
        currentPage: page,
        totalPages
      },
      data: results
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

export default router;
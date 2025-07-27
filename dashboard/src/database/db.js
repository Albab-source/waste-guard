import mysql from'mysql2/promise';

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '', // sesuaikan dengan XAMPP kamu
  database: 'dbpcn'
});

export default pool;

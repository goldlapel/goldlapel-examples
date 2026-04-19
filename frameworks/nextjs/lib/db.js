import goldlapel from 'goldlapel';
import pg from 'pg';

let _instance = null;
let _pool = null;

export async function getGl() {
  if (!_instance) {
    _instance = await goldlapel.start(process.env.DATABASE_URL);
  }
  return _instance;
}

export async function getPool() {
  if (!_pool) {
    const gl = await getGl();
    _pool = new pg.Pool({ connectionString: gl.url });
  }
  return _pool;
}

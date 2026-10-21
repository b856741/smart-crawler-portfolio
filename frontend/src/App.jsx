import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [stats, setStats] = useState({ total_books: 0, rating_distribution: {} });
  const [loading, setLoading] = useState(true);

  // 串接 FastAPI 後端 API
  useEffect(() => {
    // 自動適應 Codespaces 雲端環境或本地環境的後端網址
    const getBackendUrl = () => {
      const hostname = window.location.hostname;
      if (hostname.includes('app.github.dev')) {
        return `https://${hostname.replace('-5173', '-8000')}`;
      }
      return 'http://localhost:8000';
    };

    const backendUrl = getBackendUrl();

    const fetchData = async () => {
      try {
        const booksRes = await axios.get(`${backendUrl}/api/books`);
        const statsRes = await axios.get(`${backendUrl}/api/stats`);
        setBooks(booksRes.data);
        setStats(statsRes.data);
      } catch (error) {
        console.error('無法取得後端資料:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}>資料載入中...</div>;
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ textAlign: 'center', marginBottom: '30px' }}>
        <h1>📚 Smart Crawler Portfolio </h1>
        <p>基於 Requests, BeautifulSoup, SQLModel 與 FastAPI 的全端爬蟲與數據展示系統</p>
      </header>

      {/* 數據統計儀表板 */}
      <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
        <div style={{ flex: 1, background: '#f4f6f8', padding: '20px', borderRadius: '8px', textAlign: 'center' }}>
          <h3>總爬取書籍數量</h3>
          <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#2563eb' }}>{stats.total_books}</p>
        </div>
        <div style={{ flex: 2, background: '#f4f6f8', padding: '20px', borderRadius: '8px' }}>
          <h3>評分分佈 (Rating Distribution)</h3>
          <div style={{ display: 'flex', gap: '15px', marginTop: '10px' }}>
            {Object.entries(stats.rating_distribution || {}).map(([rating, count]) => (
              <div key={rating} style={{ textAlign: 'center' }}>
                <span style={{ display: 'block', fontSize: '12px', color: '#666' }}>{rating} 星</span>
                <span style={{ fontSize: '18px', fontWeight: 'bold' }}>{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 書籍資料表格 */}
      <h2>📖 書籍清單資料表</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        <thead>
          <tr style={{ background: '#2563eb', color: '#fff', textAlign: 'left' }}>
            <th style={{ padding: '12px' }}>#</th>
            <th style={{ padding: '12px' }}>書名 (Title)</th>
            <th style={{ padding: '12px' }}>價格 (Price)</th>
            <th style={{ padding: '12px' }}>評分 (Rating)</th>
          </tr>
        </thead>
        <tbody>
          {books.map((book, index) => (
            <tr key={book.id} style={{ borderBottom: '1px solid #e5e7eb' }}>
              <td style={{ padding: '12px' }}>{index + 1}</td>
              <td style={{ padding: '12px' }}>{book.title}</td>
              <td style={{ padding: '12px', color: '#16a34a', fontWeight: 'bold' }}>{book.price}</td>
              <td style={{ padding: '12px' }}>⭐ {book.rating}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
import Navbar from './Navbar'

export default function Layout({ children }) {
  return (
    <div className="app-wrapper">
      <Navbar />
      <main className="main-content">
        {children}
      </main>
      <footer className="footer">
        <p>FitTrack &copy; 2024</p>
      </footer>
    </div>
  )
}

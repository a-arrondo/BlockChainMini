import { useState, useEffect, useCallback } from "react"
import "./App.css"

const api = (path, opts) =>
  fetch(path, opts).then(r => {
    if (!r.ok) return r.json().then(b => Promise.reject(b.detail ?? `HTTP ${r.status}`))
    return r.status === 204 ? null : r.json()
  })

// ── Sidebar status widget ─────────────────────────────────────────────────────
function SidebarStatus() {
  const [status, setStatus] = useState(null)
  const [nPeers, setNPeers] = useState(null)

  const load = useCallback(() => {
    api("/blockchain/status").then(d => setStatus(d)).catch(() => {})
    api("/blockchain/neighbours").then(d => setNPeers(d.n_peers)).catch(() => {})
  }, [])

  useEffect(() => {
    load()
    const t = setInterval(load, 5000)
    return () => clearInterval(t)
  }, [load])

  return (
    <div className="sidebar-status">
      <div className="sidebar-stat">
        <span className="sidebar-stat-value">{status ? status.length : "—"}</span>
        <span className="sidebar-stat-label">Blocks</span>
      </div>
      <div className="sidebar-stat">
        <span className={`sidebar-stat-value ${status ? (status.is_valid ? "valid" : "invalid") : ""}`}>
          {status ? (status.is_valid ? "valid" : "invalid") : "—"}
        </span>
        <span className="sidebar-stat-label">Integrity</span>
      </div>
      <div className="sidebar-stat">
        <span className="sidebar-stat-value">{nPeers !== null ? nPeers : "—"}</span>
        <span className="sidebar-stat-label">Neighbours</span>
      </div>
    </div>
  )
}

// ── History ──────────────────────────────────────────────────────────────────
function HistoryPane() {
  const [history, setHistory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    api("/blockchain/history")
      .then(d => { setHistory(d); setLoading(false) })
      .catch(e => { setError(String(e)); setLoading(false) })
  }, [])

  return (
    <>
      <div className="pane-label">Chain History</div>
      {loading && <p className="muted-text">Fetching…</p>}
      {error   && <p className="error">{error}</p>}
      {history && (
        <table className="data-table">
          <colgroup>
            <col /><col /><col /><col />
          </colgroup>
          <thead>
            <tr>
              <th>#</th>
              <th>Hash</th>
              <th>Txns</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {[...history.history].reverse().map(block => (
              <tr key={block.index}>
                <td>{block.index}</td>
                <td><span className="hash">{block.hash.slice(0, 45)}…</span></td>
                <td>{block.transactions.length}</td>
                <td><span className="hash">{block.timestamp}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  )
}

// ── Transactions ─────────────────────────────────────────────────────────────
function TransactionsPane() {
  const [form, setForm]         = useState({ sender: "", receiver: "", amount: "" })
  const [loading, setLoading]   = useState(false)
  const [feedback, setFeedback] = useState(null)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const submit = () => {
    const amount = parseFloat(form.amount)
    if (!form.sender || !form.receiver || isNaN(amount)) {
      setFeedback({ ok: false, msg: "All fields are required." }); return
    }
    setLoading(true); setFeedback(null)
    api("/blockchain/append", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender: form.sender, receiver: form.receiver, amount })
    })
      .then(() => { setFeedback({ ok: true, msg: "Transaction submitted." }); setForm({ sender: "", receiver: "", amount: "" }); setLoading(false) })
      .catch(e => { setFeedback({ ok: false, msg: String(e) }); setLoading(false) })
  }

  return (
    <>
      <div className="pane-label">Add Transaction</div>
      <div className="form">
        <div className="form-row">
          <div className="field">
            <label>Sender</label>
            <input placeholder="alice" value={form.sender} onChange={set("sender")} />
          </div>
          <div className="field">
            <label>Receiver</label>
            <input placeholder="bob" value={form.receiver} onChange={set("receiver")} />
          </div>
        </div>
        <div className="field">
          <label>Amount</label>
          <input placeholder="0.00" type="number" min="0" step="any" value={form.amount} onChange={set("amount")} />
        </div>
        {feedback && <p className={`form-feedback ${feedback.ok ? "ok" : "err"}`}>{feedback.msg}</p>}
        <button className="btn-primary" onClick={submit} disabled={loading}>
          {loading ? "Submitting…" : "Submit"}
        </button>
      </div>
    </>
  )
}

// ── Neighbours ───────────────────────────────────────────────────────────────
function NeighboursPane() {
  const [peers, setPeers]       = useState([])
  const [form, setForm]         = useState({ ip: "", port: "" })
  const [loading, setLoading]   = useState(true)
  const [feedback, setFeedback] = useState(null)

  const load = useCallback(() => {
    api("/blockchain/neighbours")
      .then(d => { setPeers(d.peers); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  useEffect(() => { load() }, [load])

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const add = () => {
    const port = parseInt(form.port)
    if (!form.ip || isNaN(port)) { setFeedback({ ok: false, msg: "IP and port required." }); return }
    setFeedback(null)
    api("/blockchain/neighbours", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify([{ ip: form.ip, port }])
    }).then(() => { setForm({ ip: "", port: "" }); load() })
      .catch(e => setFeedback({ ok: false, msg: String(e) }))
  }

  const reset = () => {
    api("/blockchain/neighbours", { method: "DELETE" })
      .then(() => { setPeers([]); setFeedback({ ok: true, msg: "Neighbours cleared." }) })
      .catch(e => setFeedback({ ok: false, msg: String(e) }))
  }

  return (
    <>
      <div className="pane-label">Neighbours</div>
      {loading ? <p className="muted-text">Fetching…</p> : (
        <div className="peer-list">
          {peers.length === 0
            ? <p className="empty">No neighbours connected.</p>
            : peers.map(p => (
              <div className="peer-item" key={`${p.ip}:${p.port}`}>
                <span>{p.ip}:{p.port}</span>
              </div>
            ))}
        </div>
      )}
      <div className="form">
        <div className="pane-label" style={{ border: "none", paddingBottom: 0 }}>Add Neighbour</div>
        <div className="form-row">
          <div className="field">
            <label>IP</label>
            <input placeholder="127.0.0.1" value={form.ip} onChange={set("ip")} />
          </div>
          <div className="field">
            <label>Port</label>
            <input placeholder="8001" type="number" value={form.port} onChange={set("port")} />
          </div>
        </div>
        {feedback && <p className={`form-feedback ${feedback.ok ? "ok" : "err"}`}>{feedback.msg}</p>}
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <button className="btn-primary" onClick={add}>Add</button>
          <button className="btn-ghost" onClick={reset}>Clear all</button>
        </div>
      </div>
    </>
  )
}

function SidebarFooter() {
  const [countdown, setCountdown] = useState(5)

  useEffect(() => {
    const t = setInterval(() => {
      setCountdown(c => c <= 1 ? 5 : c - 1)
    }, 1000)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="sidebar-footer">
      Refresh in {countdown}s<br />v1.0<br />
      <span style={{ opacity: 0.6 }}>@a-arrondo</span>
    </div>
  )
}


const TABS = [
  { id: "history",      label: "History" },
  { id: "transactions", label: "Transactions" },
  { id: "neighbours",   label: "Neighbours" },
]

export default function App() {
  const [active, setActive] = useState("history")

  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-name">
          BlockChain<span className="brand-accent">Mini</span>
          </div>
          <div className="brand-sub">Explorer</div>
        </div>

        <SidebarStatus />

        <nav>
          {TABS.map(t => (
            <button
              key={t.id}
              className={`nav-item ${active === t.id ? "active" : ""}`}
              onClick={() => setActive(t.id)}
            >
              {t.label}
            </button>
          ))}
        </nav>

        <SidebarFooter />
      </aside>

      <main className="content">
        {active === "history"      && <HistoryPane />}
        {active === "transactions" && <TransactionsPane />}
        {active === "neighbours"   && <NeighboursPane />}
      </main>
    </div>
  )
}
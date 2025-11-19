import React, { useState } from "react";

/**
 * Minimal Chat UI that calls the backend /chat endpoint.
 * Drop this file into a React app (e.g., Vite / Create React App) under frontend/src/
 *
 * Usage:
 *  - Ensure your frontend dev server proxies /chat to the backend (or set the full URL)
 *  - Import and render <ChatBox /> in App.jsx
 */

export default function ChatBox({ apiUrl = "/chat" }) {
  const [query, setQuery] = useState("");
  const [resp, setResp] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function send() {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const r = await fetch(apiUrl, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!r.ok) {
        const text = await r.text();
        throw new Error(`HTTP ${r.status}: ${text}`);
      }
      const j = await r.json();
      setResp(j);
    } catch (e) {
      setError(e.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  function exampleQuestion(txn) {
    setQuery(`Is txn ${txn} fraudulent? Explain and recommend action.`);
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="mb-3">
        <label className="block mb-1 font-medium">Ask the fraud assistant</label>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Is txn 12345 fraudulent?"
          className="w-full p-2 border rounded"
        />
      </div>

      <div className="flex gap-2">
        <button
          onClick={send}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-60"
        >
          {loading ? "Thinking..." : "Ask"}
        </button>
        <button
          onClick={() => exampleQuestion(12345)}
          className="px-4 py-2 bg-gray-200 rounded"
        >
          Example
        </button>
        <button
          onClick={() => {
            setQuery("");
            setResp(null);
            setError(null);
          }}
          className="px-4 py-2 bg-red-100 rounded"
        >
          Clear
        </button>
      </div>

      {error && (
        <div className="mt-3 text-red-600">
          <strong>Error:</strong> {error}
        </div>
      )}

      {resp && (
        <div className="mt-4 p-3 border rounded bg-white shadow-sm">
          <div className="font-bold mb-2">Assistant</div>
          <pre className="whitespace-pre-wrap">{resp.answer}</pre>

          <details className="mt-3">
            <summary className="cursor-pointer">Raw retrieved evidence</summary>
            <pre className="mt-2 text-sm">{JSON.stringify(resp.retrieved, null, 2)}</pre>
          </details>

          <details className="mt-3">
            <summary className="cursor-pointer">Raw API response</summary>
            <pre className="mt-2 text-sm">{JSON.stringify(resp, null, 2)}</pre>
          </details>
        </div>
      )}
    </div>
  );
}

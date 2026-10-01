import React from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BriefcaseBusiness, Search, Sparkles } from "lucide-react";
import "./styles.css";

type Job = { id: string; title: string; company: string; location: string | null; remote_type: string | null; skills: string[]; source: string; freshness: string };
type JobPage = { items: Job[]; total: number };
const api = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

function App() {
  const [query, setQuery] = React.useState("");
  const [jobs, setJobs] = React.useState<JobPage>({ items: [], total: 0 });
  const [error, setError] = React.useState<string | null>(null);
  const search = async (value = query) => {
    setError(null);
    try { const response = await fetch(`${api}/jobs?q=${encodeURIComponent(value)}`); if (!response.ok) throw new Error("Search is temporarily unavailable."); setJobs(await response.json() as JobPage); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Search failed."); }
  };
  React.useEffect(() => { void search(""); }, []);
  return <main><nav><span className="brand"><BriefcaseBusiness size={20}/> Job Pull</span><span>Find Jobs</span><span>Fresh Jobs</span><span>Applications</span><button className="ghost">Sign in</button></nav>
    <section className="hero"><p className="eyebrow"><Sparkles size={15}/> REAL-TIME JOB INTELLIGENCE</p><h1>Find the right job.<br/><em>Before everyone else does.</em></h1><p className="lede">Search fresh opportunities from trusted, publicly available job sources in one calm workspace.</p>
      <form onSubmit={(event) => { event.preventDefault(); void search(); }}><Search size={20}/><input aria-label="Search jobs" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Machine Learning Engineer, Python, or company"/><button>Search jobs</button></form></section>
    <section className="results"><div className="section-head"><div><p className="eyebrow green">● LIVE INDEX</p><h2>Fresh opportunities</h2><p>{jobs.total} jobs available in demo mode</p></div><button className="ghost">Filters</button></div>{error && <p className="error">{error}</p>}<div className="grid">{jobs.items.map((job) => <article key={job.id}><div className="card-top"><div><h3>{job.title}</h3><strong>{job.company}</strong></div><span className="fresh">{job.freshness}</span></div><p className="meta">{job.location} · {job.remote_type}</p><div className="skills">{job.skills.map((skill) => <span key={skill}>{skill}</span>)}</div><footer><small>Found via {job.source}</small><button className="ghost">View job →</button></footer></article>)}</div></section></main>;
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><QueryClientProvider client={new QueryClient()}><App/></QueryClientProvider></React.StrictMode>);

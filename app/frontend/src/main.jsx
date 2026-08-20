import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

import { api } from './api.js';

function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  const [tone, setTone] = useState('info');
  const [busy, setBusy] = useState(false);

  function changeMode(next) {
    setMode(next);
    setMessage('');
    setForm((current) => ({ ...current, password: '' }));
  }

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setMessage('');
    try {
      if (mode === 'register') {
        await api('/api/auth/register', { method: 'POST', body: JSON.stringify(form) });
        setTone('success');
        setMessage('Account created. Please sign in with your new credentials.');
        setMode('login');
        setForm((current) => ({ ...current, name: '', password: '' }));
      } else {
        const result = await api('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({ email: form.email, password: form.password }),
        });
        localStorage.setItem('token', result.access_token);
        localStorage.setItem('role', result.role);
        onAuthenticated(result.access_token, result.role);
      }
    } catch (error) {
      setTone('error');
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-showcase">
        <a className="brand" href="#" aria-label="ServiceHub home"><span>SH</span> ServiceHub</a>
        <div className="showcase-copy">
          <p className="eyebrow">APPOINTMENTS, SIMPLIFIED</p>
          <h1>Great service starts with an easy booking.</h1>
          <p>Discover trusted professionals, compare services, and reserve a time that works for you.</p>
          <div className="benefits">
            <span>✓ Verified providers</span><span>✓ Real-time availability</span><span>✓ Easy cancellation</span>
          </div>
        </div>
        <p className="showcase-note">ServiceHub QA Lab · Portfolio application</p>
      </section>

      <section className="auth-side">
        <div className="auth-card">
          <div className="auth-heading">
            <p className="eyebrow">WELCOME TO SERVICEHUB</p>
            <h2>{mode === 'login' ? 'Sign in to continue' : 'Create your account'}</h2>
            <p>{mode === 'login' ? 'Manage bookings and discover your next service.' : 'It takes less than a minute to get started.'}</p>
          </div>
          <div className="auth-tabs" role="tablist">
            <button className={mode === 'login' ? 'active' : ''} onClick={() => changeMode('login')} type="button">Sign in</button>
            <button className={mode === 'register' ? 'active' : ''} onClick={() => changeMode('register')} type="button">Register</button>
          </div>
          {message && <div className={`feedback ${tone}`} role="alert">{message}</div>}
          <form onSubmit={submit} className="auth-form">
            {mode === 'register' && (
              <label>Full name<input data-testid="name" autoComplete="name" placeholder="Your full name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></label>
            )}
            <label>Email address<input data-testid="email" type="email" autoComplete="email" placeholder="you@example.com" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required /></label>
            <label>Password<input data-testid="password" type="password" autoComplete={mode === 'login' ? 'current-password' : 'new-password'} placeholder="At least 8 characters" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required /></label>
            {mode === 'register' && <p className="password-hint">Use at least 8 characters with a letter and number.</p>}
            <button data-testid="auth-submit" className="primary auth-submit" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'}</button>
          </form>
          <p className="auth-switch">{mode === 'login' ? 'New to ServiceHub?' : 'Already have an account?'} <button type="button" onClick={() => changeMode(mode === 'login' ? 'register' : 'login')}>{mode === 'login' ? 'Create account' : 'Sign in'}</button></p>
        </div>
      </section>
    </main>
  );
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [role, setRole] = useState(localStorage.getItem('role'));
  const [view, setView] = useState(token ? 'services' : 'login');
  const [services, setServices] = useState([]);
  const [providers, setProviders] = useState([]);
  const [slots, setSlots] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [search, setSearch] = useState('');
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const [selected, setSelected] = useState({ service_id: '', provider_id: '', appointment_time: '' });

  const selectedService = useMemo(() => services.find((item) => item.id === Number(selected.service_id)), [services, selected.service_id]);
  const selectedProvider = useMemo(() => providers.find((item) => item.id === Number(selected.provider_id)), [providers, selected.provider_id]);
  const currentStep = selected.service_id ? (selected.provider_id ? (selected.appointment_time ? 4 : 3) : 2) : 1;

  async function loadCatalog(term = search) {
    setBusy(true);
    try {
      const query = term ? `?search=${encodeURIComponent(term)}` : '';
      const [serviceData, providerData] = await Promise.all([api(`/api/services${query}`), api('/api/providers')]);
      setServices(serviceData);
      setProviders(providerData);
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }

  useEffect(() => { if (token) loadCatalog(''); }, [token]);

  function selectService(id) {
    setSelected({ service_id: id, provider_id: '', appointment_time: '' });
    setSlots([]);
    setMessage('Service selected. Now choose your provider.');
    setTimeout(() => document.getElementById('booking-flow')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
  }

  async function selectProvider(id) {
    setBusy(true);
    try {
      const data = await api(`/api/providers/${id}/availability`);
      setSelected((current) => ({ ...current, provider_id: id, appointment_time: '' }));
      setSlots(data);
      setMessage(data.length ? 'Provider selected. Choose an available time.' : 'This provider currently has no open slots.');
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }

  async function book() {
    setBusy(true);
    try {
      await api('/api/bookings', { method: 'POST', body: JSON.stringify({ ...selected, service_id: Number(selected.service_id), provider_id: Number(selected.provider_id) }) });
      setMessage('Appointment booked successfully.');
      setSelected({ service_id: '', provider_id: '', appointment_time: '' });
      setSlots([]);
      await showBookings();
    } catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }

  async function showBookings() {
    try { setBookings(await api('/api/bookings/me')); setView('appointments'); }
    catch (error) { setMessage(error.message); }
  }

  async function cancel(id) {
    if (!window.confirm('Cancel this appointment? The time will become available again.')) return;
    try { await api(`/api/bookings/${id}`, { method: 'DELETE' }); setMessage('Appointment cancelled.'); await showBookings(); }
    catch (error) { setMessage(error.message); }
  }

  function logout() {
    localStorage.removeItem('token'); localStorage.removeItem('role');
    setToken(null); setRole(null); setView('login'); setMessage('');
  }

  if (!token) return <AuthScreen onAuthenticated={(newToken, newRole) => { setToken(newToken); setRole(newRole); setView('services'); setMessage(`Welcome back. You are signed in as ${newRole}.`); }} />;

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand brand-button" onClick={() => { setView('services'); loadCatalog(''); }}><span>SH</span> ServiceHub</button>
        <nav>
          <button className={view === 'services' ? 'nav-active' : ''} onClick={() => { setView('services'); loadCatalog(''); }}>Explore</button>
          <button data-testid="appointments-nav" className={view === 'appointments' ? 'nav-active' : ''} onClick={showBookings}>My appointments</button>
        </nav>
        <div className="account"><span className="role-pill">{role}</span><button className="ghost" onClick={logout}>Log out</button></div>
      </header>

      <main className="content">
        {message && <div className="toast" role="status"><span>{message}</span><button onClick={() => setMessage('')} aria-label="Dismiss">×</button></div>}
        {view === 'services' && (
          <>
            <section className="hero">
              <div><p className="eyebrow">TRUSTED LOCAL PROFESSIONALS</p><h1>What can we help you with?</h1><p>Choose a service, find a provider, and book your preferred time.</p></div>
              <form className="search-box" onSubmit={(e) => { e.preventDefault(); loadCatalog(); }}>
                <span>⌕</span><input aria-label="Search services" placeholder="Search massage, repair, consultation…" value={search} onChange={(e) => setSearch(e.target.value)} /><button className="primary">Search</button>
              </form>
            </section>

            <section className="section-heading"><div><p className="eyebrow">OUR SERVICES</p><h2>Popular services</h2></div><span>{services.length} available</span></section>
            <section className="service-grid" aria-busy={busy}>
              {services.map((service) => {
                const active = selected.service_id === service.id;
                return <article className={`service-card ${active ? 'selected' : ''}`} key={service.id}>
                  <div className="service-icon">{service.category === 'Technology' ? '⌁' : '✦'}</div>
                  <span className="category">{service.category}</span>
                  <h3>{service.name}</h3><p>{service.description}</p>
                  <div className="service-meta"><strong>${Number(service.price).toFixed(2)}</strong><span>{service.duration_minutes} min</span></div>
                  <button data-testid={`select-service-${service.id}`} className={active ? 'selected-button' : 'secondary'} onClick={() => selectService(service.id)}>{active ? '✓ Selected' : 'Select service'} <span>→</span></button>
                </article>;
              })}
              {!busy && services.length === 0 && <div className="empty-state"><h3>No services found</h3><p>Try a broader search term.</p></div>}
            </section>

            <section id="booking-flow" className="booking-panel">
              <div className="booking-head"><div><p className="eyebrow">BOOK AN APPOINTMENT</p><h2>{selectedService ? selectedService.name : 'Start by selecting a service'}</h2></div><div className="steps">{['Service', 'Provider', 'Time', 'Confirm'].map((label, index) => <div className={currentStep >= index + 1 ? 'done' : ''} key={label}><span>{currentStep > index + 1 ? '✓' : index + 1}</span><small>{label}</small></div>)}</div></div>
              {!selectedService ? <div className="booking-empty">Choose one of the service cards above to continue.</div> : <>
                <div className="selection-summary"><div><small>Selected service</small><strong>{selectedService.name}</strong></div><div><small>Duration</small><strong>{selectedService.duration_minutes} minutes</strong></div><div><small>Price</small><strong>${Number(selectedService.price).toFixed(2)}</strong></div></div>
                <div className="booking-section"><h3>1. Choose your provider</h3><div className="provider-list">{providers.map((provider) => <button data-testid={`provider-${provider.id}`} className={selected.provider_id === provider.id ? 'active' : ''} onClick={() => selectProvider(provider.id)} key={provider.id}><span className="avatar">{provider.name.split(' ').map((part) => part[0]).join('').slice(0, 2)}</span><span><strong>{provider.name}</strong><small>{provider.bio}</small></span><b>{selected.provider_id === provider.id ? '✓' : '›'}</b></button>)}</div></div>
                {selectedProvider && <div className="booking-section"><h3>2. Choose an available time</h3>{slots.length ? <div className="slot-grid">{slots.map((slot) => <button data-testid="slot" className={selected.appointment_time === slot.start_time ? 'active' : ''} onClick={() => setSelected((current) => ({ ...current, appointment_time: slot.start_time }))} key={slot.id}><span>{new Date(slot.start_time).toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' })}</span><strong>{new Date(slot.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong></button>)}</div> : <p className="muted">No future slots are currently available.</p>}</div>}
                <div className="booking-action"><div>{selected.appointment_time ? <><small>Ready to book</small><strong>{selectedService.name} with {selectedProvider?.name}</strong></> : <span>Select a provider and time to continue.</span>}</div><button data-testid="book" className="primary" disabled={!selected.appointment_time || busy} onClick={book}>{busy ? 'Booking…' : 'Confirm booking →'}</button></div>
              </>}
            </section>
          </>
        )}

        {view === 'appointments' && <section className="appointments-page"><div className="section-heading"><div><p className="eyebrow">YOUR SCHEDULE</p><h1>My appointments</h1></div><button className="primary" onClick={() => setView('services')}>+ Book another</button></div>{bookings.length === 0 ? <div className="empty-state large"><div>◷</div><h2>No appointments yet</h2><p>Your upcoming bookings will appear here.</p><button className="secondary" onClick={() => setView('services')}>Explore services</button></div> : <div className="appointment-list">{bookings.map((booking) => <article className="appointment" key={booking.id}><div className="date-block"><strong>{new Date(booking.appointment_time).getDate()}</strong><span>{new Date(booking.appointment_time).toLocaleString([], { month: 'short' })}</span></div><div className="appointment-info"><span className={`status ${booking.status}`}>{booking.status}</span><h3>Booking #{booking.id}</h3><p>{new Date(booking.appointment_time).toLocaleString()}</p></div>{booking.status === 'confirmed' && <button className="danger-ghost" onClick={() => cancel(booking.id)}>Cancel</button>}</article>)}</div>}</section>}
      </main>
      <footer><span>ServiceHub QA Lab</span><span>Personal quality engineering portfolio</span></footer>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);

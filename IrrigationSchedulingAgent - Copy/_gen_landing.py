
# -*- coding: utf-8 -*-
"""Generate landing page files for AgroMind."""
import pathlib

BASE = pathlib.Path(__file__).parent

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """\
/* ===========================
   DESIGN TOKENS
=========================== */
:root {
  --green:        #2F6F5E;
  --green-dark:   #1E4D40;
  --green-light:  #3D8F74;
  --green-xlight: #E8F5F0;
  --green-glow:   rgba(47, 111, 94, 0.18);
  --blue:         #2E5F8A;
  --blue-dark:    #1C3F5E;
  --blue-light:   #4A7FAD;
  --blue-xlight:  #EAF1F8;
  --blue-glow:    rgba(46, 95, 138, 0.18);
  --cream:        #FAF8F3;
  --cream-dark:   #F0ECE3;
  --text-dark:    #1A2B24;
  --text-mid:     #3D5248;
  --text-muted:   #7A9186;
  --white:        #FFFFFF;
  --shadow-sm:    0 2px 12px rgba(30, 77, 64, 0.08);
  --shadow-md:    0 8px 30px rgba(30, 77, 64, 0.12);
  --shadow-lg:    0 16px 50px rgba(30, 77, 64, 0.16);
  --radius-sm:    10px;
  --radius-md:    16px;
  --radius-lg:    24px;
  --radius-xl:    36px;
  --transition:   all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  --font-head:    'Outfit', sans-serif;
  --font-body:    'Inter', sans-serif;
}

/* ===========================
   RESET & BASE
=========================== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 16px; }
body {
  font-family: var(--font-body);
  background-color: var(--cream);
  color: var(--text-dark);
  line-height: 1.65;
  overflow-x: hidden;
}
img { max-width: 100%; display: block; }
a   { text-decoration: none; color: inherit; }
ul  { list-style: none; }
h1,h2,h3,h4,h5 {
  font-family: var(--font-head);
  line-height: 1.2;
  color: var(--text-dark);
}
section { padding: 90px 0; }

.container {
  width: 90%;
  max-width: 1160px;
  margin: 0 auto;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--green-xlight);
  color: var(--green);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 6px 16px;
  border-radius: 50px;
  margin-bottom: 16px;
}
.section-badge.blue { background: var(--blue-xlight); color: var(--blue); }

.section-title {
  font-size: clamp(28px, 4vw, 42px);
  font-weight: 800;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 17px;
  color: var(--text-muted);
  max-width: 580px;
  line-height: 1.7;
}

/* ===========================
   SCROLL REVEAL ANIMATIONS
=========================== */
.reveal {
  opacity: 0;
  transform: translateY(36px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.reveal.visible { opacity: 1; transform: translateY(0); }
.reveal-delay-1 { transition-delay: 0.1s; }
.reveal-delay-2 { transition-delay: 0.2s; }
.reveal-delay-3 { transition-delay: 0.3s; }
.reveal-delay-4 { transition-delay: 0.4s; }
.reveal-delay-5 { transition-delay: 0.5s; }
.reveal-delay-6 { transition-delay: 0.6s; }

/* ===========================
   NAVBAR
=========================== */
#navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 1000;
  padding: 18px 0;
  transition: var(--transition);
}
#navbar.scrolled {
  background: rgba(250,248,243,0.93);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: var(--shadow-sm);
  padding: 12px 0;
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 90%;
  max-width: 1160px;
  margin: 0 auto;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-head);
  font-size: 22px;
  font-weight: 800;
  color: var(--white);
  transition: var(--transition);
}
#navbar.scrolled .nav-logo { color: var(--text-dark); }
.nav-logo-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--green-light), var(--green-dark));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; color: var(--white);
  box-shadow: 0 4px 16px var(--green-glow);
  flex-shrink: 0;
}
.nav-links { display: flex; align-items: center; gap: 32px; }
.nav-links a {
  font-size: 14px;
  font-weight: 500;
  color: rgba(255,255,255,0.85);
  transition: var(--transition);
}
#navbar.scrolled .nav-links a { color: var(--text-mid); }
.nav-links a:hover { color: var(--green); }
.nav-cta {
  background: var(--white) !important;
  color: var(--green-dark) !important;
  font-weight: 700 !important;
  padding: 9px 22px !important;
  border-radius: 50px !important;
  box-shadow: var(--shadow-sm) !important;
}
#navbar.scrolled .nav-cta { background: var(--green) !important; color: var(--white) !important; }
.nav-cta:hover { transform: translateY(-2px); box-shadow: var(--shadow-md) !important; }
.nav-hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  cursor: pointer;
  padding: 4px;
  background: none;
  border: none;
}
.nav-hamburger span {
  display: block; width: 24px; height: 2px;
  background: var(--white); border-radius: 2px;
  transition: var(--transition);
}
#navbar.scrolled .nav-hamburger span { background: var(--text-dark); }

/* ===========================
   MOBILE NAV
=========================== */
.mobile-nav {
  display: none;
  position: fixed;
  inset: 0;
  background: var(--green-dark);
  z-index: 999;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 36px;
}
.mobile-nav.open { display: flex; }
.mobile-nav a {
  font-family: var(--font-head);
  font-size: 28px;
  font-weight: 700;
  color: var(--white);
  transition: var(--transition);
}
.mobile-nav a:hover { color: #A8F0D8; }
.mobile-nav-close {
  position: absolute; top: 24px; right: 24px;
  font-size: 28px; color: white;
  cursor: pointer; background: none; border: none;
}

/* ===========================
   HERO
=========================== */
#hero {
  min-height: 100vh;
  background: linear-gradient(145deg, var(--green-dark) 0%, var(--green) 45%, var(--blue) 100%);
  display: flex; align-items: center;
  position: relative; overflow: hidden;
  padding: 120px 0 80px;
}
.hero-bg-circle {
  position: absolute; border-radius: 50%; opacity: 0.07;
}
.hero-bg-circle-1 { width:700px;height:700px;background:var(--white);top:-200px;right:-200px; }
.hero-bg-circle-2 { width:400px;height:400px;background:var(--white);bottom:-150px;left:-100px; }
.hero-bg-circle-3 { width:200px;height:200px;background:var(--blue-light);top:50%;left:60%;opacity:0.12; }
.hero-dots {
  position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.12) 1px, transparent 1px);
  background-size: 40px 40px;
}
.hero-content {
  position: relative; z-index: 2;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 60px; align-items: center;
  width: 90%; max-width: 1160px; margin: 0 auto;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(8px);
  color: var(--white); font-size: 12px; font-weight: 600;
  letter-spacing: 1px; text-transform: uppercase;
  padding: 7px 18px; border-radius: 50px;
  border: 1px solid rgba(255,255,255,0.25);
  margin-bottom: 24px;
}
.hero-badge i { font-size: 10px; color: #A8F0D8; }
.hero-h1 {
  font-family: var(--font-head);
  font-size: clamp(40px, 5.5vw, 68px);
  font-weight: 900; color: var(--white);
  line-height: 1.05; margin-bottom: 22px;
  letter-spacing: -1px;
}
.hero-h1 .accent { color: #A8F0D8; }
.hero-sub {
  font-size: 17px; color: rgba(255,255,255,0.78);
  line-height: 1.7; margin-bottom: 40px; max-width: 480px;
}
.hero-btns { display: flex; gap: 16px; flex-wrap: wrap; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 10px;
  background: var(--white); color: var(--green-dark);
  font-family: var(--font-head); font-size: 15px; font-weight: 700;
  padding: 15px 30px; border-radius: 50px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.2);
  transition: var(--transition); border: none; cursor: pointer;
}
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 36px rgba(0,0,0,0.25); background: #EDFDF6; }
.btn-outline {
  display: inline-flex; align-items: center; gap: 10px;
  background: transparent; color: var(--white);
  font-family: var(--font-head); font-size: 15px; font-weight: 600;
  padding: 14px 28px; border-radius: 50px;
  border: 2px solid rgba(255,255,255,0.4);
  transition: var(--transition); cursor: pointer;
}
.btn-outline:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.7); transform: translateY(-3px); }
.hero-stats {
  display: flex; gap: 28px; margin-top: 48px;
  padding-top: 32px; border-top: 1px solid rgba(255,255,255,0.15);
}
.hero-stat-num { font-family: var(--font-head); font-size: 30px; font-weight: 800; color: #A8F0D8; line-height: 1; }
.hero-stat-label { font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px; }

/* Hero visual card */
.hero-visual { position: relative; }
.hero-mock-card {
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.22);
  border-radius: var(--radius-lg); padding: 28px;
  animation: floatCard 5s ease-in-out infinite;
}
@keyframes floatCard {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-12px); }
}
.mock-header { display: flex; align-items: center; gap: 10px; margin-bottom: 22px; }
.mock-header-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #A8F0D8, #2F6F5E);
  border-radius: 10px; display: flex; align-items: center; justify-content: center;
  font-size: 18px; color: white;
}
.mock-header-text h4 { font-family: var(--font-head); font-size: 14px; font-weight: 700; color: white; }
.mock-header-text p  { font-size: 11px; color: rgba(255,255,255,0.6); }
.mock-live-badge {
  margin-left: auto;
  display: inline-flex; align-items: center; gap: 5px;
  background: rgba(168,240,216,0.2); color: #A8F0D8;
  font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 50px;
}
.mock-live-dot {
  width: 6px; height: 6px; background: #A8F0D8; border-radius: 50%;
  animation: pulseDot 1.4s ease-in-out infinite;
}
@keyframes pulseDot {
  0%,100% { opacity:1; transform:scale(1); }
  50%      { opacity:0.4; transform:scale(0.8); }
}
.mock-sensor-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 18px; }
.mock-sensor-cell { background: rgba(255,255,255,0.08); border-radius: var(--radius-sm); padding: 14px; }
.mock-sensor-lbl { font-size: 10px; color: rgba(255,255,255,0.55); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.mock-sensor-val { font-family: var(--font-head); font-size: 22px; font-weight: 800; color: var(--white); }
.mock-sensor-unit { font-size: 12px; font-weight: 400; }
.mock-bar-row { margin-bottom: 12px; }
.mock-bar-lbl { display: flex; justify-content: space-between; font-size: 11px; color: rgba(255,255,255,0.6); margin-bottom: 5px; }
.mock-bar-track { height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; }
.mock-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #A8F0D8, #2F6F5E); }
.mock-recommendation {
  background: rgba(168,240,216,0.15); border: 1px solid rgba(168,240,216,0.3);
  border-radius: var(--radius-sm); padding: 14px;
  display: flex; align-items: flex-start; gap: 10px;
}
.mock-rec-icon { font-size: 18px; flex-shrink: 0; margin-top: 2px; }
.mock-rec-text { font-size: 12px; color: rgba(255,255,255,0.85); line-height: 1.5; }
.mock-rec-text strong { display: block; font-family: var(--font-head); font-size: 13px; color: #A8F0D8; margin-bottom: 2px; }

/* Floating badges */
.hero-float-badge {
  position: absolute; background: var(--white);
  border-radius: var(--radius-md); padding: 12px 16px;
  box-shadow: var(--shadow-lg);
  display: flex; align-items: center; gap: 10px;
  animation: floatBadge 6s ease-in-out infinite;
}
.hero-float-badge.badge-top    { top: -18px; left: -30px; animation-delay: -2s; }
.hero-float-badge.badge-bottom { bottom: -16px; right: -24px; animation-delay: -4s; }
@keyframes floatBadge {
  0%,100% { transform: translateY(0); }
  50%      { transform: translateY(-8px); }
}
.float-badge-icon {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; font-size: 14px;
}
.float-badge-icon.green { background: var(--green-xlight); color: var(--green); }
.float-badge-icon.blue  { background: var(--blue-xlight);  color: var(--blue); }
.float-badge-text strong { font-family: var(--font-head); font-size: 13px; font-weight: 700; color: var(--text-dark); display: block; }
.float-badge-text span   { font-size: 11px; color: var(--text-muted); }

/* ===========================
   PROBLEM STATEMENT
=========================== */
#problem { background: var(--white); }
.problem-header { margin-bottom: 56px; }
.problem-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }
.problem-card {
  background: var(--cream); border: 1px solid var(--cream-dark);
  border-radius: var(--radius-md); padding: 32px 24px;
  text-align: center; transition: var(--transition);
  position: relative; overflow: hidden;
}
.problem-card::before {
  content: ''; position: absolute;
  bottom: 0; left: 0; right: 0; height: 3px;
}
.problem-card.p1::before { background: #EF4444; }
.problem-card.p2::before { background: #F59E0B; }
.problem-card.p3::before { background: var(--blue); }
.problem-card.p4::before { background: var(--green); }
.problem-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-md); background: var(--white); }
.problem-icon-wrap {
  width: 68px; height: 68px; border-radius: 18px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; margin: 0 auto 20px;
}
.p1 .problem-icon-wrap { background: #FEF2F2; color: #EF4444; }
.p2 .problem-icon-wrap { background: #FFFBEB; color: #F59E0B; }
.p3 .problem-icon-wrap { background: var(--blue-xlight); color: var(--blue); }
.p4 .problem-icon-wrap { background: var(--green-xlight); color: var(--green); }
.problem-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
.problem-card p  { font-size: 14px; color: var(--text-muted); line-height: 1.65; }

/* ===========================
   HOW IT WORKS
=========================== */
#how-it-works { background: var(--cream); }
.how-header { margin-bottom: 60px; }
.steps-flow { display: grid; grid-template-columns: 1fr 64px 1fr 64px 1fr; align-items: center; }
.step-card {
  background: var(--white); border-radius: var(--radius-lg);
  padding: 36px 28px; text-align: center;
  box-shadow: var(--shadow-md); border: 1px solid var(--cream-dark);
  position: relative; transition: var(--transition);
}
.step-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-lg); }
.step-num {
  position: absolute; top: -16px; left: 50%; transform: translateX(-50%);
  width: 32px; height: 32px; background: var(--green); color: white;
  font-family: var(--font-head); font-weight: 800; font-size: 14px;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 14px var(--green-glow);
}
.step-icon-wrap {
  width: 80px; height: 80px; border-radius: 20px;
  background: linear-gradient(135deg, var(--green-xlight), var(--blue-xlight));
  display: flex; align-items: center; justify-content: center;
  font-size: 32px; margin: 0 auto 20px; color: var(--green);
}
.step-3 .step-icon-wrap { color: var(--blue); }
.step-card h3 { font-size: 19px; font-weight: 700; margin-bottom: 12px; }
.step-card p  { font-size: 14px; color: var(--text-muted); line-height: 1.65; }
.step-tags { display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 16px; }
.step-tag {
  background: var(--green-xlight); color: var(--green);
  font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 50px;
}
.step-tag.blue { background: var(--blue-xlight); color: var(--blue); }
.flow-arrow { display: flex; align-items: center; justify-content: center; color: var(--green); font-size: 26px; }

/* ===========================
   SYSTEM ARCHITECTURE
=========================== */
#architecture { background: var(--white); }
.arch-header { margin-bottom: 56px; }
.arch-diagram { display: flex; align-items: stretch; gap: 0; overflow-x: auto; padding-bottom: 8px; }
.arch-layer {
  flex: 1; min-width: 160px;
  background: var(--cream); border: 1.5px solid var(--cream-dark);
  border-radius: var(--radius-md); padding: 24px 16px;
  text-align: center; transition: var(--transition);
}
.arch-layer:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.arch-layer-title {
  font-family: var(--font-head); font-size: 13px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.8px;
  margin-bottom: 18px; padding: 6px 14px; border-radius: 50px; display: inline-block;
}
.layer-input .arch-layer-title { background: var(--green-xlight); color: var(--green); }
.layer-proc  .arch-layer-title { background: var(--blue-xlight);  color: var(--blue); }
.layer-ai    .arch-layer-title { background: #FFF7ED; color: #C2410C; }
.layer-rec   .arch-layer-title { background: #F0FDF4; color: #166534; }
.layer-app   .arch-layer-title { background: #F5F3FF; color: #6D28D9; }
.arch-item {
  display: flex; align-items: center; gap: 8px;
  background: var(--white); border-radius: var(--radius-sm);
  padding: 10px 12px; margin-bottom: 8px;
  font-size: 13px; font-weight: 500;
  box-shadow: var(--shadow-sm); text-align: left;
}
.arch-item i { font-size: 14px; width: 18px; text-align: center; }
.layer-input .arch-item i { color: var(--green); }
.layer-proc  .arch-item i { color: var(--blue); }
.layer-ai    .arch-item i { color: #C2410C; }
.layer-rec   .arch-item i { color: #166534; }
.layer-app   .arch-item i { color: #6D28D9; }
.arch-connector { display: flex; align-items: center; padding: 0 4px; color: var(--text-muted); font-size: 22px; flex-shrink: 0; }

/* ===========================
   FEATURES
=========================== */
#features { background: var(--cream); }
.features-header { margin-bottom: 56px; }
.features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.feature-card {
  background: var(--white); border-radius: var(--radius-md);
  padding: 32px; border: 1px solid var(--cream-dark);
  transition: var(--transition); position: relative; overflow: hidden;
}
.feature-card::after {
  content: ''; position: absolute; top: 0; left: 0;
  width: 100%; height: 3px;
  background: linear-gradient(90deg, var(--green), var(--blue));
  transform: scaleX(0); transform-origin: left; transition: transform 0.4s ease;
}
.feature-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-md); }
.feature-card:hover::after { transform: scaleX(1); }
.feature-icon {
  width: 56px; height: 56px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; margin-bottom: 20px;
}
.fi-1 { background:#ECFDF5;color:#059669; }
.fi-2 { background:#EFF6FF;color:#2563EB; }
.fi-3 { background:#FFF7ED;color:#EA580C; }
.fi-4 { background:#F0FDF4;color:#16A34A; }
.fi-5 { background:#EEF2FF;color:#4F46E5; }
.fi-6 { background:#FEF2F2;color:#DC2626; }
.feature-card h3 { font-size: 18px; font-weight: 700; margin-bottom: 10px; }
.feature-card p  { font-size: 14px; color: var(--text-muted); line-height: 1.65; }

/* ===========================
   SAMPLE RECOMMENDATION
=========================== */
#sample {
  background: linear-gradient(135deg, var(--green-dark) 0%, var(--green) 50%, var(--blue) 100%);
  position: relative; overflow: hidden;
}
#sample::before {
  content: ''; position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px);
  background-size: 36px 36px;
}
.sample-inner {
  position: relative; z-index: 2;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 64px; align-items: center;
}
.sample-text .section-title   { color: var(--white); }
.sample-text .section-subtitle { color: rgba(255,255,255,0.7); max-width: 420px; }
.sample-quotes { display: flex; flex-direction: column; gap: 16px; margin-top: 32px; }
.sample-quote-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
  border-radius: 50px; padding: 8px 16px;
  font-size: 13px; color: rgba(255,255,255,0.85); width: fit-content;
}
.sample-quote-pill i { color: #A8F0D8; }
.phone-mockup {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: var(--radius-xl); padding: 28px;
  max-width: 360px; margin: 0 auto;
  animation: floatCard 6s ease-in-out infinite;
}
.phone-status-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.phone-status-bar > span { font-size: 11px; color: rgba(255,255,255,0.6); font-weight: 600; }
.phone-status-icons { display: flex; gap: 6px; }
.phone-status-icons i { font-size: 11px; color: rgba(255,255,255,0.6); }
.notif-card {
  background: var(--white); border-radius: var(--radius-md);
  padding: 20px; margin-bottom: 14px;
  box-shadow: var(--shadow-md); position: relative; overflow: hidden;
}
.notif-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; }
.notif-card.skip::before  { background: #F59E0B; }
.notif-card.water::before { background: var(--blue); }
.notif-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.notif-app-icon {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, var(--green-light), var(--green-dark));
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: white;
}
.notif-app-name { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.notif-time { margin-left: auto; font-size: 10px; color: var(--text-muted); }
.notif-body h4 { font-size: 13px; font-weight: 700; color: var(--text-dark); margin-bottom: 4px; }
.notif-body p  { font-size: 12px; color: var(--text-muted); line-height: 1.5; }
.phone-sensors { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-top: 14px; }
.phone-sensor-cell { background: rgba(255,255,255,0.08); border-radius: var(--radius-sm); padding: 10px 8px; text-align: center; }
.psc-icon { font-size: 16px; margin-bottom: 4px; }
.psc-val  { font-family: var(--font-head); font-size: 14px; font-weight: 700; color: white; }
.psc-lbl  { font-size: 9px; color: rgba(255,255,255,0.55); margin-top: 2px; }

/* ===========================
   BENEFITS
=========================== */
#benefits { background: var(--white); }
.benefits-header { margin-bottom: 56px; }
.benefits-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; }
.benefit-column { border-radius: var(--radius-lg); padding: 40px 36px; border: 1.5px solid; }
.benefit-column.for-farmers {
  background: linear-gradient(135deg, var(--green-xlight), rgba(255,255,255,0.5));
  border-color: rgba(47,111,94,0.2);
}
.benefit-column.for-env {
  background: linear-gradient(135deg, var(--blue-xlight), rgba(255,255,255,0.5));
  border-color: rgba(46,95,138,0.2);
}
.benefit-col-header {
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 28px; padding-bottom: 20px;
  border-bottom: 1px solid rgba(0,0,0,0.07);
}
.benefit-col-icon {
  width: 52px; height: 52px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center; font-size: 22px;
}
.for-farmers .benefit-col-icon { background: var(--green-xlight); color: var(--green); }
.for-env     .benefit-col-icon { background: var(--blue-xlight);  color: var(--blue); }
.benefit-col-header h3 { font-size: 22px; font-weight: 800; }
.benefit-list { display: flex; flex-direction: column; gap: 14px; }
.benefit-item { display: flex; align-items: flex-start; gap: 14px; }
.benefit-check {
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; flex-shrink: 0; margin-top: 2px;
}
.for-farmers .benefit-check { background: var(--green); color: white; }
.for-env     .benefit-check { background: var(--blue);  color: white; }
.benefit-item-text strong { display: block; font-size: 15px; font-weight: 700; margin-bottom: 2px; }
.benefit-item-text span   { font-size: 13px; color: var(--text-muted); }

/* ===========================
   TECH STACK
=========================== */
#tech-stack { background: var(--cream); }
.tech-inner { text-align: center; }
.tech-inner .section-subtitle { margin: 0 auto 48px; text-align: center; }
.tech-badges { display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; }
.tech-badge {
  display: flex; align-items: center; gap: 12px;
  background: var(--white); border: 1.5px solid var(--cream-dark);
  border-radius: var(--radius-md); padding: 16px 24px;
  box-shadow: var(--shadow-sm); transition: var(--transition); cursor: default;
}
.tech-badge:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--green); }
.tech-badge-icon {
  width: 44px; height: 44px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center; font-size: 20px;
}
.tb-1{background:#ECFDF5;color:#059669;}
.tb-2{background:#FFF7ED;color:#C2410C;}
.tb-3{background:#EFF6FF;color:#2563EB;}
.tb-4{background:#F5F3FF;color:#6D28D9;}
.tb-5{background:#F0FDF4;color:#16A34A;}
.tb-6{background:#FEF2F2;color:#DC2626;}
.tech-badge-text strong { display: block; font-family: var(--font-head); font-size: 15px; font-weight: 700; color: var(--text-dark); }
.tech-badge-text span   { font-size: 12px; color: var(--text-muted); }

/* ===========================
   CONTACT / FOOTER
=========================== */
#contact {
  background: var(--green-dark);
  padding: 90px 0 0;
  position: relative; overflow: hidden;
}
#contact::before {
  content: ''; position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}
.contact-inner {
  position: relative; z-index: 2;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 72px; align-items: start; padding-bottom: 80px;
}
.contact-left .section-badge { background: rgba(168,240,216,0.2); color: #A8F0D8; }
.contact-left .section-title    { color: var(--white); }
.contact-left .section-subtitle { color: rgba(255,255,255,0.65); }
.contact-tagline { margin-top: 32px; display: flex; flex-direction: column; gap: 14px; }
.contact-tagline-item { display: flex; align-items: center; gap: 12px; font-size: 14px; color: rgba(255,255,255,0.75); }
.contact-tagline-item i { color: #A8F0D8; font-size: 16px; }
.contact-form {
  background: var(--white); border-radius: var(--radius-lg);
  padding: 40px; box-shadow: var(--shadow-lg);
}
.contact-form h3 { font-size: 22px; font-weight: 800; margin-bottom: 24px; color: var(--text-dark); }
.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 18px; }
.form-group label {
  font-size: 12px; font-weight: 700; color: var(--text-muted);
  text-transform: uppercase; letter-spacing: 0.6px;
}
.form-group input, .form-group textarea {
  background: var(--cream); border: 1.5px solid var(--cream-dark);
  color: var(--text-dark); padding: 13px 16px;
  border-radius: var(--radius-sm); font-family: var(--font-body);
  font-size: 14px; outline: none; transition: var(--transition);
  width: 100%; resize: none;
}
.form-group input:focus, .form-group textarea:focus {
  border-color: var(--green); background: var(--white);
  box-shadow: 0 0 0 3px var(--green-glow);
}
.form-group textarea { height: 110px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.btn-submit {
  width: 100%;
  background: linear-gradient(135deg, var(--green), var(--green-dark));
  color: white; font-family: var(--font-head); font-size: 15px; font-weight: 700;
  padding: 15px; border-radius: var(--radius-sm); border: none;
  cursor: pointer; transition: var(--transition);
  display: flex; align-items: center; justify-content: center; gap: 10px;
  margin-top: 6px;
}
.btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 24px var(--green-glow); }
.footer-bottom { background: rgba(0,0,0,0.2); padding: 24px 0; position: relative; z-index: 2; }
.footer-bottom-inner {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 16px;
  width: 90%; max-width: 1160px; margin: 0 auto;
}
.footer-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-head); font-size: 18px; font-weight: 800; color: var(--white);
}
.footer-logo-icon {
  width: 32px; height: 32px; background: var(--green);
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-size: 15px; color: white;
}
.footer-links { display: flex; gap: 24px; }
.footer-links a { font-size: 13px; color: rgba(255,255,255,0.5); transition: var(--transition); }
.footer-links a:hover { color: var(--white); }
.footer-copy { font-size: 12px; color: rgba(255,255,255,0.4); }

/* ===========================
   RESPONSIVE
=========================== */
@media (max-width: 1024px) {
  .problem-grid  { grid-template-columns: repeat(2,1fr); }
  .features-grid { grid-template-columns: repeat(2,1fr); }
  .steps-flow    { grid-template-columns: 1fr; gap: 20px; }
  .flow-arrow    { transform: rotate(90deg); }
  .arch-diagram  { flex-direction: column; }
  .arch-connector{ transform: rotate(90deg); height: 40px; width: auto; justify-content: center; }
}
@media (max-width: 860px) {
  .hero-content     { grid-template-columns: 1fr; gap: 40px; }
  .hero-visual      { display: none; }
  .sample-inner     { grid-template-columns: 1fr; }
  .benefits-columns { grid-template-columns: 1fr; }
  .contact-inner    { grid-template-columns: 1fr; gap: 40px; }
  .nav-links        { display: none; }
  .nav-hamburger    { display: flex; }
}
@media (max-width: 640px) {
  section                 { padding: 64px 0; }
  .problem-grid           { grid-template-columns: 1fr; }
  .features-grid          { grid-template-columns: 1fr; }
  .tech-badges            { flex-direction: column; align-items: center; }
  .form-row               { grid-template-columns: 1fr; }
  .footer-bottom-inner    { flex-direction: column; align-items: flex-start; }
  .hero-stats             { flex-wrap: wrap; gap: 20px; }
}
"""

# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AgroMind - AI-Based Irrigation Scheduling Agent</title>
  <meta name="description" content="AgroMind uses soil moisture sensors, weather forecasts, and crop intelligence to tell farmers exactly when, how long, and how much to irrigate - eliminating waste and maximising yield." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="stylesheet" href="landing.css" />
</head>
<body>

<!-- MOBILE NAV -->
<nav class="mobile-nav" id="mobileNav" role="navigation" aria-label="Mobile navigation">
  <button class="mobile-nav-close" id="mobileNavClose" aria-label="Close menu"><i class="fa-solid fa-xmark"></i></button>
  <a href="#hero"         onclick="closeMobileNav()">Home</a>
  <a href="#problem"      onclick="closeMobileNav()">Problem</a>
  <a href="#how-it-works" onclick="closeMobileNav()">How It Works</a>
  <a href="#architecture" onclick="closeMobileNav()">Architecture</a>
  <a href="#features"     onclick="closeMobileNav()">Features</a>
  <a href="#benefits"     onclick="closeMobileNav()">Benefits</a>
  <a href="#contact"      onclick="closeMobileNav()">Contact</a>
</nav>

<!-- NAVBAR -->
<nav id="navbar" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a class="nav-logo" href="#hero" aria-label="AgroMind Home">
      <div class="nav-logo-icon" aria-hidden="true"><i class="fa-solid fa-seedling"></i></div>
      AgroMind
    </a>
    <ul class="nav-links" role="list">
      <li><a href="#problem">Problem</a></li>
      <li><a href="#how-it-works">How It Works</a></li>
      <li><a href="#architecture">Architecture</a></li>
      <li><a href="#features">Features</a></li>
      <li><a href="#benefits">Benefits</a></li>
      <li><a href="#tech-stack">Tech Stack</a></li>
      <li><a href="#contact" class="nav-cta">Contact Us</a></li>
    </ul>
    <button class="nav-hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- 1. HERO -->
<section id="hero" aria-label="Hero section">
  <div class="hero-bg-circle hero-bg-circle-1" aria-hidden="true"></div>
  <div class="hero-bg-circle hero-bg-circle-2" aria-hidden="true"></div>
  <div class="hero-bg-circle hero-bg-circle-3" aria-hidden="true"></div>
  <div class="hero-dots" aria-hidden="true"></div>
  <div class="hero-content">
    <div class="hero-text-block">
      <div class="hero-badge"><i class="fa-solid fa-circle-check"></i> AI-Powered Agriculture</div>
      <h1 class="hero-h1">Irrigate <span class="accent">Smarter</span>,<br />Waste Less.</h1>
      <p class="hero-sub">Over-irrigation and under-irrigation cost farmers billions every year. AgroMind's AI engine reads your soil, checks the sky, and tells you exactly when and how much to water &mdash; so you never guess again.</p>
      <div class="hero-btns">
        <a href="#how-it-works" class="btn-primary" id="hero-cta-primary"><i class="fa-solid fa-circle-play"></i> See How It Works</a>
        <a href="#contact" class="btn-outline" id="hero-cta-secondary"><i class="fa-solid fa-envelope"></i> Get In Touch</a>
      </div>
      <div class="hero-stats" aria-label="Key statistics">
        <div class="hero-stat-item"><div class="hero-stat-num">40%</div><div class="hero-stat-label">Water Saved</div></div>
        <div class="hero-stat-item"><div class="hero-stat-num">28%</div><div class="hero-stat-label">Yield Increase</div></div>
        <div class="hero-stat-item"><div class="hero-stat-num">Real-Time</div><div class="hero-stat-label">AI Decisions</div></div>
      </div>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <div class="hero-float-badge badge-top">
        <div class="float-badge-icon green"><i class="fa-solid fa-droplet"></i></div>
        <div class="float-badge-text"><strong>Soil Moisture</strong><span>68% &mdash; Optimal</span></div>
      </div>
      <div class="hero-mock-card">
        <div class="mock-header">
          <div class="mock-header-icon"><i class="fa-solid fa-seedling"></i></div>
          <div class="mock-header-text"><h4>AgroMind Dashboard</h4><p>Field A &mdash; Rice Crop</p></div>
          <div class="mock-live-badge"><div class="mock-live-dot"></div> LIVE</div>
        </div>
        <div class="mock-sensor-grid">
          <div class="mock-sensor-cell"><div class="mock-sensor-lbl">Soil Moisture</div><div class="mock-sensor-val">68<span class="mock-sensor-unit">%</span></div></div>
          <div class="mock-sensor-cell"><div class="mock-sensor-lbl">Temperature</div><div class="mock-sensor-val">31<span class="mock-sensor-unit">&deg;C</span></div></div>
          <div class="mock-sensor-cell"><div class="mock-sensor-lbl">Rain Chance</div><div class="mock-sensor-val">82<span class="mock-sensor-unit">%</span></div></div>
          <div class="mock-sensor-cell"><div class="mock-sensor-lbl">Crop Stage</div><div class="mock-sensor-val" style="font-size:16px">Tillering</div></div>
        </div>
        <div class="mock-bar-row">
          <div class="mock-bar-lbl"><span>Weekly Water Usage</span><span>3.2 / 8 L</span></div>
          <div class="mock-bar-track"><div class="mock-bar-fill" style="width:40%"></div></div>
        </div>
        <div class="mock-bar-row">
          <div class="mock-bar-lbl"><span>AI Confidence</span><span>94%</span></div>
          <div class="mock-bar-track"><div class="mock-bar-fill" style="width:94%;background:linear-gradient(90deg,#A8F0D8,#2E5F8A)"></div></div>
        </div>
        <div class="mock-recommendation">
          <div class="mock-rec-icon">&#x1F6AB;</div>
          <div class="mock-rec-text"><strong>Skip Irrigation Today</strong>Soil moisture adequate (68%) and rain expected within 24 hours. No irrigation needed.</div>
        </div>
      </div>
      <div class="hero-float-badge badge-bottom">
        <div class="float-badge-icon blue"><i class="fa-solid fa-cloud-rain"></i></div>
        <div class="float-badge-text"><strong>Rain Incoming</strong><span>Within 24 hours</span></div>
      </div>
    </div>
  </div>
</section>

<!-- 2. PROBLEM STATEMENT -->
<section id="problem" aria-labelledby="problem-title">
  <div class="container">
    <div class="problem-header reveal">
      <div class="section-badge"><i class="fa-solid fa-triangle-exclamation"></i> The Problem</div>
      <h2 class="section-title" id="problem-title">Why Traditional Irrigation Fails</h2>
      <p class="section-subtitle">Farmers across the globe lose crops and water to outdated irrigation methods. The cost is enormous &mdash; for them and for the planet.</p>
    </div>
    <div class="problem-grid">
      <div class="problem-card p1 reveal reveal-delay-1">
        <div class="problem-icon-wrap"><i class="fa-solid fa-faucet-drip"></i></div>
        <h3>Water Wastage</h3>
        <p>Over-irrigation wastes up to 70% of fresh water used in agriculture, depleting groundwater tables and increasing costs.</p>
      </div>
      <div class="problem-card p2 reveal reveal-delay-2">
        <div class="problem-icon-wrap"><i class="fa-solid fa-wheat-awn"></i></div>
        <h3>Crop Yield Loss</h3>
        <p>Under-irrigation stresses crops at critical growth stages, reducing harvest yield by 20&ndash;40% and threatening food security.</p>
      </div>
      <div class="problem-card p3 reveal reveal-delay-3">
        <div class="problem-icon-wrap"><i class="fa-solid fa-cloud-bolt"></i></div>
        <h3>Unpredictable Weather</h3>
        <p>Climate variability makes manual irrigation scheduling unreliable. Farmers relying on intuition often irrigate just before rain.</p>
      </div>
      <div class="problem-card p4 reveal reveal-delay-4">
        <div class="problem-icon-wrap"><i class="fa-solid fa-signal"></i></div>
        <h3>No Real-Time Data</h3>
        <p>Without live soil and weather data, decisions are made blindly &mdash; leading to inefficient water use and unnecessary expenses.</p>
      </div>
    </div>
  </div>
</section>

<!-- 3. HOW IT WORKS -->
<section id="how-it-works" aria-labelledby="how-title">
  <div class="container">
    <div class="how-header reveal" style="text-align:center">
      <div class="section-badge blue"><i class="fa-solid fa-gears"></i> Process</div>
      <h2 class="section-title" id="how-title">How AgroMind Works</h2>
      <p class="section-subtitle" style="margin:0 auto">Three intelligent steps transform raw data into actionable irrigation decisions &mdash; delivered straight to the farmer.</p>
    </div>
    <div class="steps-flow">
      <div class="step-card reveal reveal-delay-1">
        <div class="step-num">1</div>
        <div class="step-icon-wrap"><i class="fa-solid fa-satellite-dish"></i></div>
        <h3>Data Collection</h3>
        <p>IoT soil sensors, live weather APIs, and crop profile inputs are gathered continuously from the field.</p>
        <div class="step-tags">
          <span class="step-tag"><i class="fa-solid fa-microchip"></i> Soil Sensors</span>
          <span class="step-tag blue"><i class="fa-solid fa-cloud-sun"></i> Weather API</span>
          <span class="step-tag"><i class="fa-solid fa-user"></i> Farmer Input</span>
        </div>
      </div>
      <div class="flow-arrow reveal reveal-delay-2"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="step-card reveal reveal-delay-2">
        <div class="step-num">2</div>
        <div class="step-icon-wrap"><i class="fa-solid fa-brain"></i></div>
        <h3>AI Decision Engine</h3>
        <p>A hybrid rule-based &amp; machine learning model analyses all inputs and calculates an optimal irrigation decision.</p>
        <div class="step-tags">
          <span class="step-tag"><i class="fa-solid fa-robot"></i> ML Model</span>
          <span class="step-tag blue"><i class="fa-solid fa-scale-balanced"></i> Rule Engine</span>
        </div>
      </div>
      <div class="flow-arrow reveal reveal-delay-3"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="step-card step-3 reveal reveal-delay-3">
        <div class="step-num">3</div>
        <div class="step-icon-wrap"><i class="fa-solid fa-mobile-screen-button"></i></div>
        <h3>Smart Recommendation</h3>
        <p>Farmers receive a clear, explainable recommendation &mdash; when to irrigate, for how long, and exactly why the AI decided so.</p>
        <div class="step-tags">
          <span class="step-tag blue"><i class="fa-solid fa-bell"></i> Push Alert</span>
          <span class="step-tag"><i class="fa-solid fa-comment-dots"></i> Explanation</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 4. SYSTEM ARCHITECTURE -->
<section id="architecture" aria-labelledby="arch-title">
  <div class="container">
    <div class="arch-header reveal" style="text-align:center">
      <div class="section-badge"><i class="fa-solid fa-diagram-project"></i> Architecture</div>
      <h2 class="section-title" id="arch-title">System Architecture</h2>
      <p class="section-subtitle" style="margin:0 auto">A layered pipeline from raw sensor data to actionable recommendation &mdash; built for reliability and scalability.</p>
    </div>
    <div class="arch-diagram reveal reveal-delay-1">
      <div class="arch-layer layer-input">
        <div class="arch-layer-title">Input Layer</div>
        <div class="arch-item"><i class="fa-solid fa-microchip"></i> Soil Sensors</div>
        <div class="arch-item"><i class="fa-solid fa-cloud-sun"></i> Weather API</div>
        <div class="arch-item"><i class="fa-solid fa-user-pen"></i> Farmer Inputs</div>
        <div class="arch-item"><i class="fa-solid fa-seedling"></i> Crop Profiles</div>
      </div>
      <div class="arch-connector"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="arch-layer layer-proc">
        <div class="arch-layer-title">Data Processing</div>
        <div class="arch-item"><i class="fa-solid fa-filter"></i> Data Cleaning</div>
        <div class="arch-item"><i class="fa-solid fa-chart-line"></i> Feature Eng.</div>
        <div class="arch-item"><i class="fa-solid fa-database"></i> Cloud Storage</div>
        <div class="arch-item"><i class="fa-solid fa-rotate"></i> Real-time ETL</div>
      </div>
      <div class="arch-connector"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="arch-layer layer-ai">
        <div class="arch-layer-title">AI Engine</div>
        <div class="arch-item"><i class="fa-solid fa-robot"></i> ML Classifier</div>
        <div class="arch-item"><i class="fa-solid fa-scale-balanced"></i> Rule Engine</div>
        <div class="arch-item"><i class="fa-solid fa-brain"></i> XAI Module</div>
        <div class="arch-item"><i class="fa-solid fa-arrows-spin"></i> Feedback Loop</div>
      </div>
      <div class="arch-connector"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="arch-layer layer-rec">
        <div class="arch-layer-title">Recommendation</div>
        <div class="arch-item"><i class="fa-solid fa-circle-check"></i> Irrigate / Skip</div>
        <div class="arch-item"><i class="fa-solid fa-clock"></i> Duration &amp; Time</div>
        <div class="arch-item"><i class="fa-solid fa-droplet"></i> Volume Calc.</div>
        <div class="arch-item"><i class="fa-solid fa-comment-dots"></i> Explanation</div>
      </div>
      <div class="arch-connector"><i class="fa-solid fa-arrow-right"></i></div>
      <div class="arch-layer layer-app">
        <div class="arch-layer-title">Farmer App</div>
        <div class="arch-item"><i class="fa-solid fa-mobile-screen"></i> Mobile App</div>
        <div class="arch-item"><i class="fa-solid fa-gauge-high"></i> Dashboard</div>
        <div class="arch-item"><i class="fa-solid fa-bell"></i> Push Alerts</div>
        <div class="arch-item"><i class="fa-solid fa-file-lines"></i> History &amp; Logs</div>
      </div>
    </div>
  </div>
</section>

<!-- 5. KEY FEATURES -->
<section id="features" aria-labelledby="features-title">
  <div class="container">
    <div class="features-header reveal" style="text-align:center">
      <div class="section-badge blue"><i class="fa-solid fa-star"></i> Features</div>
      <h2 class="section-title" id="features-title">Everything You Need</h2>
      <p class="section-subtitle" style="margin:0 auto">Six core capabilities that make AgroMind the most intelligent irrigation assistant available for modern farming.</p>
    </div>
    <div class="features-grid">
      <div class="feature-card reveal reveal-delay-1">
        <div class="feature-icon fi-1"><i class="fa-solid fa-gauge"></i></div>
        <h3>Real-Time Soil Monitoring</h3>
        <p>Continuous readings from IoT sensors track soil moisture, temperature, and EC levels &mdash; updated every 15 minutes for live insight.</p>
      </div>
      <div class="feature-card reveal reveal-delay-2">
        <div class="feature-icon fi-2"><i class="fa-solid fa-cloud-sun-rain"></i></div>
        <h3>Weather-Aware Scheduling</h3>
        <p>Integrates 72-hour weather forecasts to prevent redundant irrigation before rain &mdash; saving water and reducing energy costs.</p>
      </div>
      <div class="feature-card reveal reveal-delay-3">
        <div class="feature-icon fi-3"><i class="fa-solid fa-wheat-awn"></i></div>
        <h3>Crop-Specific Water Needs</h3>
        <p>Each crop profile contains growth-stage water requirements. The AI adapts its recommendations to your specific crop and season.</p>
      </div>
      <div class="feature-card reveal reveal-delay-1">
        <div class="feature-icon fi-4"><i class="fa-solid fa-magnifying-glass-chart"></i></div>
        <h3>Explainable AI (XAI)</h3>
        <p>Every recommendation comes with a plain-language explanation &mdash; &ldquo;Why should I skip irrigation today?&rdquo; is always answered.</p>
      </div>
      <div class="feature-card reveal reveal-delay-2">
        <div class="feature-icon fi-5"><i class="fa-solid fa-mobile-screen-button"></i></div>
        <h3>Mobile Dashboard</h3>
        <p>Farmers access recommendations, live sensor data, and field history from a clean, simple mobile-first dashboard &mdash; no tech expertise needed.</p>
      </div>
      <div class="feature-card reveal reveal-delay-3">
        <div class="feature-icon fi-6"><i class="fa-solid fa-clock-rotate-left"></i></div>
        <h3>Usage History &amp; Logs</h3>
        <p>Full audit trail of every irrigation event &mdash; including AI rationale, sensor state, and outcomes &mdash; for post-season analysis and reporting.</p>
      </div>
    </div>
  </div>
</section>

<!-- 6. SAMPLE RECOMMENDATION -->
<section id="sample" aria-labelledby="sample-title">
  <div class="container">
    <div class="sample-inner">
      <div class="sample-text reveal">
        <div class="section-badge"><i class="fa-solid fa-bell"></i> Live Demo</div>
        <h2 class="section-title" id="sample-title">What a Real Recommendation Looks Like</h2>
        <p class="section-subtitle">AgroMind sends simple, actionable alerts &mdash; not confusing data dumps. Here&rsquo;s what a farmer sees on their phone.</p>
        <div class="sample-quotes">
          <div class="sample-quote-pill"><i class="fa-solid fa-circle-check"></i> Clear reason &mdash; no guesswork required</div>
          <div class="sample-quote-pill"><i class="fa-solid fa-circle-check"></i> Delivered via push notification instantly</div>
          <div class="sample-quote-pill"><i class="fa-solid fa-circle-check"></i> Works offline &mdash; cached on-device</div>
          <div class="sample-quote-pill"><i class="fa-solid fa-circle-check"></i> Available in local languages</div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <div class="phone-mockup">
          <div class="phone-status-bar">
            <span>09:47 AM</span>
            <div class="phone-status-icons">
              <i class="fa-solid fa-signal"></i>
              <i class="fa-solid fa-wifi"></i>
              <i class="fa-solid fa-battery-three-quarters"></i>
            </div>
          </div>
          <div class="notif-card skip">
            <div class="notif-header">
              <div class="notif-app-icon"><i class="fa-solid fa-seedling"></i></div>
              <div class="notif-app-name">AgroMind</div>
              <div class="notif-time">Just now</div>
            </div>
            <div class="notif-body">
              <h4>&#x1F6AB; Skip Irrigation Today</h4>
              <p>Soil moisture is adequate (68%) and rain is expected within 24 hours. No irrigation needed.</p>
            </div>
          </div>
          <div class="notif-card water">
            <div class="notif-header">
              <div class="notif-app-icon"><i class="fa-solid fa-seedling"></i></div>
              <div class="notif-app-name">AgroMind &middot; Yesterday</div>
              <div class="notif-time">6:00 AM</div>
            </div>
            <div class="notif-body">
              <h4>&#x1F4A7; Irrigate Field B &mdash; 40 min</h4>
              <p>Soil moisture dropped to 31%. High evaporation expected. Irrigate for 40 minutes this morning.</p>
            </div>
          </div>
          <div class="phone-sensors">
            <div class="phone-sensor-cell"><div class="psc-icon">&#x1F4A7;</div><div class="psc-val">68%</div><div class="psc-lbl">Soil Moisture</div></div>
            <div class="phone-sensor-cell"><div class="psc-icon">&#x1F321;&#xFE0F;</div><div class="psc-val">31&deg;C</div><div class="psc-lbl">Temperature</div></div>
            <div class="phone-sensor-cell"><div class="psc-icon">&#x1F327;&#xFE0F;</div><div class="psc-val">82%</div><div class="psc-lbl">Rain Chance</div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 7. BENEFITS -->
<section id="benefits" aria-labelledby="benefits-title">
  <div class="container">
    <div class="benefits-header reveal" style="text-align:center">
      <div class="section-badge"><i class="fa-solid fa-leaf"></i> Benefits</div>
      <h2 class="section-title" id="benefits-title">Good for Farmers. Great for the Planet.</h2>
      <p class="section-subtitle" style="margin:0 auto">AgroMind creates measurable value on both sides &mdash; profitability for the farmer, sustainability for the environment.</p>
    </div>
    <div class="benefits-columns">
      <div class="benefit-column for-farmers reveal reveal-delay-1">
        <div class="benefit-col-header">
          <div class="benefit-col-icon"><i class="fa-solid fa-tractor"></i></div>
          <h3>For Farmers</h3>
        </div>
        <ul class="benefit-list">
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Lower Water &amp; Energy Costs</strong><span>Cut irrigation-related electricity and water bills by up to 35% with precision scheduling.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Higher Crop Yield</strong><span>Optimal irrigation at every growth stage means stronger crops and bigger harvests.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Reduced Manual Effort</strong><span>No more constant field checks. The AI monitors 24/7 and alerts you only when action is needed.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Better Decision Confidence</strong><span>Data-backed recommendations with transparent reasoning build trust and certainty in every choice.</span></div>
          </li>
        </ul>
      </div>
      <div class="benefit-column for-env reveal reveal-delay-2">
        <div class="benefit-col-header">
          <div class="benefit-col-icon"><i class="fa-solid fa-earth-asia"></i></div>
          <h3>For the Environment</h3>
        </div>
        <ul class="benefit-list">
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Water Conservation</strong><span>Avoid unnecessary irrigation and prevent runoff that wastes precious fresh-water resources.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Reduced Carbon Footprint</strong><span>Less pumping means less energy consumption &mdash; directly reducing greenhouse gas emissions.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Soil Health Protection</strong><span>Preventing over-saturation protects soil structure, prevents erosion, and reduces nutrient leaching.</span></div>
          </li>
          <li class="benefit-item">
            <div class="benefit-check"><i class="fa-solid fa-check"></i></div>
            <div class="benefit-item-text"><strong>Long-Term Sustainability</strong><span>Responsible water management ensures farmland remains productive for future generations.</span></div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- 8. TECH STACK -->
<section id="tech-stack" aria-labelledby="tech-title">
  <div class="tech-inner container">
    <div class="reveal">
      <div class="section-badge"><i class="fa-solid fa-code"></i> Tech Stack</div>
      <h2 class="section-title" id="tech-title">Built on Modern Technology</h2>
      <p class="section-subtitle">AgroMind is built with a robust, production-ready technology stack designed for performance, reliability, and scale.</p>
    </div>
    <div class="tech-badges reveal reveal-delay-1">
      <div class="tech-badge"><div class="tech-badge-icon tb-1"><i class="fa-solid fa-microchip"></i></div><div class="tech-badge-text"><strong>IoT Sensors</strong><span>Soil &amp; Climate</span></div></div>
      <div class="tech-badge"><div class="tech-badge-icon tb-2"><i class="fa-brands fa-python"></i></div><div class="tech-badge-text"><strong>Python / ML</strong><span>scikit-learn &middot; FastAPI</span></div></div>
      <div class="tech-badge"><div class="tech-badge-icon tb-3"><i class="fa-solid fa-cloud-sun"></i></div><div class="tech-badge-text"><strong>Weather API</strong><span>OpenWeatherMap</span></div></div>
      <div class="tech-badge"><div class="tech-badge-icon tb-4"><i class="fa-solid fa-mobile-screen-button"></i></div><div class="tech-badge-text"><strong>Mobile App</strong><span>React Native</span></div></div>
      <div class="tech-badge"><div class="tech-badge-icon tb-5"><i class="fa-solid fa-database"></i></div><div class="tech-badge-text"><strong>Cloud Database</strong><span>PostgreSQL &middot; Redis</span></div></div>
      <div class="tech-badge"><div class="tech-badge-icon tb-6"><i class="fa-solid fa-server"></i></div><div class="tech-badge-text"><strong>Cloud Infra</strong><span>AWS &middot; Docker</span></div></div>
    </div>
  </div>
</section>

<!-- 9. CONTACT / FOOTER CTA -->
<section id="contact" aria-labelledby="contact-title">
  <div class="container">
    <div class="contact-inner">
      <div class="contact-left reveal">
        <div class="section-badge"><i class="fa-solid fa-envelope"></i> Contact</div>
        <h2 class="section-title" id="contact-title">Join the Future of Sustainable Farming</h2>
        <p class="section-subtitle">Whether you&rsquo;re a farmer, investor, or researcher &mdash; we&rsquo;d love to hear from you. Let&rsquo;s make irrigation smarter together.</p>
        <div class="contact-tagline">
          <div class="contact-tagline-item"><i class="fa-solid fa-users"></i> Open to pilot partnerships with farms of any size</div>
          <div class="contact-tagline-item"><i class="fa-solid fa-hand-holding-dollar"></i> Seeking investors &amp; agri-tech collaborators</div>
          <div class="contact-tagline-item"><i class="fa-solid fa-flask"></i> Research &amp; academic collaborations welcome</div>
          <div class="contact-tagline-item"><i class="fa-solid fa-headset"></i> Demo sessions available on request</div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <form class="contact-form" id="contact-form" onsubmit="handleFormSubmit(event)" novalidate>
          <h3>Send us a Message</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="contact-name">Your Name</label>
              <input type="text" id="contact-name" name="name" placeholder="Ravi Kumar" required autocomplete="name" />
            </div>
            <div class="form-group">
              <label for="contact-email">Email Address</label>
              <input type="email" id="contact-email" name="email" placeholder="ravi@example.com" required autocomplete="email" />
            </div>
          </div>
          <div class="form-group">
            <label for="contact-subject">Subject</label>
            <input type="text" id="contact-subject" name="subject" placeholder="Pilot program enquiry" />
          </div>
          <div class="form-group">
            <label for="contact-message">Message</label>
            <textarea id="contact-message" name="message" placeholder="Tell us about your farm, your goals, or how you'd like to collaborate..."></textarea>
          </div>
          <button type="submit" class="btn-submit" id="contact-submit">
            <i class="fa-solid fa-paper-plane"></i> Send Message
          </button>
          <div id="form-success" style="display:none;margin-top:16px;background:#ECFDF5;color:#166534;border-radius:8px;padding:14px 16px;font-size:14px;font-weight:600;text-align:center;">
            <i class="fa-solid fa-circle-check" style="margin-right:8px;"></i>Thank you! We'll get back to you within 24 hours.
          </div>
        </form>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-bottom-inner">
      <div class="footer-logo"><div class="footer-logo-icon"><i class="fa-solid fa-seedling"></i></div>AgroMind</div>
      <nav class="footer-links">
        <a href="#hero">Home</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#features">Features</a>
        <a href="#contact">Contact</a>
      </nav>
      <p class="footer-copy">&copy; 2026 AgroMind. AI-Based Irrigation Scheduling Agent.</p>
    </div>
  </div>
</section>

<script>
  // Navbar scroll effect
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });

  // Mobile nav
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  const mobileNavClose = document.getElementById('mobileNavClose');
  hamburger.addEventListener('click', () => {
    mobileNav.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  });
  hamburger.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') hamburger.click(); });
  mobileNavClose.addEventListener('click', closeMobileNav);
  function closeMobileNav() {
    mobileNav.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  // Scroll reveal
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // Active nav highlight
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  const secObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const id = e.target.getAttribute('id');
        navLinks.forEach(link => {
          const active = link.getAttribute('href') === '#' + id;
          link.style.fontWeight = active ? '700' : '500';
          if (!link.classList.contains('nav-cta')) {
            link.style.color = active ? 'var(--green)' : '';
          }
        });
      }
    });
  }, { threshold: 0.45 });
  sections.forEach(s => secObserver.observe(s));

  // Contact form
  function handleFormSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('contact-submit');
    const name = document.getElementById('contact-name').value.trim();
    const email = document.getElementById('contact-email').value.trim();
    const msg = document.getElementById('contact-message').value.trim();
    if (!name || !email || !msg) {
      btn.style.background = 'linear-gradient(135deg,#EF4444,#DC2626)';
      btn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Please fill all required fields';
      setTimeout(() => { btn.style.background = ''; btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Message'; }, 2500);
      return;
    }
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
    setTimeout(() => {
      document.getElementById('contact-form').querySelectorAll('input,textarea').forEach(el => el.value = '');
      btn.style.display = 'none';
      document.getElementById('form-success').style.display = 'block';
    }, 1200);
  }
</script>
</body>
</html>"""

with open(str(BASE / 'index.html'), 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"index.html written: {len(HTML)} chars")

with open(str(BASE / 'landing.css'), 'w', encoding='utf-8') as f:
    f.write(CSS)
print(f"landing.css written: {len(CSS)} chars")

import os

from flask import Flask, jsonify, render_template_string


app = Flask(__name__)


PAGE = """<!doctype html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta id="page-description" name="description" content="Irada is an accessible remote hiring platform for Sudanese talent.">
    <title>Irada | إرادة</title>
    <style>
      :root {
        color-scheme: light;
        --ink: #17324d;
        --ink-soft: #38566f;
        --muted: #5f7181;
        --accent: #0e7c86;
        --accent-dark: #07545d;
        --accent-pale: #e4f4f1;
        --surface: #ffffff;
        --background: #f4faf8;
        --line: #d4e7e3;
        --warning: #9b4c18;
        --error: #a83b42;
        --shadow: 0 22px 65px rgba(22, 70, 82, .12);
      }
      * { box-sizing: border-box; }
      html { scroll-behavior: smooth; }
      body {
        margin: 0;
        min-width: 320px;
        background:
          radial-gradient(circle at 88% 0%, #d9f2ed 0, transparent 28rem),
          var(--background);
        color: var(--ink);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          Tahoma, Arial, sans-serif;
      }
      a { color: inherit; }
      button, input, select { font: inherit; }
      button, a { -webkit-tap-highlight-color: transparent; }
      :focus-visible {
        outline: 3px solid #e66f3d;
        outline-offset: 4px;
      }
      .skip-link {
        position: fixed;
        z-index: 10;
        top: 10px;
        inset-inline-start: 10px;
        padding: 10px 14px;
        border-radius: 8px;
        background: var(--ink);
        color: white;
        transform: translateY(-150%);
        transition: transform .2s ease;
      }
      .skip-link:focus { transform: translateY(0); }
      .shell { width: min(1160px, calc(100% - 40px)); margin: 0 auto; }
      header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        padding: 24px 0;
      }
      .brand {
        display: inline-flex;
        align-items: center;
        gap: 11px;
        color: var(--ink);
        font-size: 1.22rem;
        font-weight: 800;
        text-decoration: none;
        white-space: nowrap;
      }
      .mark {
        display: grid;
        width: 42px;
        height: 42px;
        place-items: center;
        border-radius: 13px;
        background: var(--accent);
        color: white;
        font-size: 1.28rem;
      }
      nav { display: flex; align-items: center; gap: 24px; }
      nav a {
        color: var(--ink-soft);
        font-size: .92rem;
        font-weight: 650;
        text-decoration: none;
      }
      nav a:hover { color: var(--accent-dark); text-decoration: underline; text-underline-offset: 4px; }
      .language-switcher {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        padding: 3px;
        border: 1px solid var(--line);
        border-radius: 10px;
        background: var(--surface);
      }
      .language-switcher button {
        min-width: 44px;
        padding: 7px 9px;
        border: 0;
        border-radius: 7px;
        background: transparent;
        color: var(--muted);
        cursor: pointer;
        font-size: .82rem;
        font-weight: 750;
      }
      .language-switcher button[aria-pressed="true"] {
        background: var(--ink);
        color: white;
      }
      main { padding-bottom: 86px; scroll-margin-top: 20px; }
      .hero {
        display: grid;
        grid-template-columns: minmax(0, 1.15fr) minmax(300px, .85fr);
        gap: clamp(42px, 7vw, 96px);
        align-items: center;
        min-height: 520px;
        padding: 56px 0 70px;
      }
      .eyebrow {
        margin: 0 0 18px;
        color: var(--accent-dark);
        font-size: .76rem;
        font-weight: 850;
        letter-spacing: .14em;
        text-transform: uppercase;
      }
      h1 {
        max-width: 720px;
        margin: 0 0 22px;
        font-size: clamp(2.75rem, 7vw, 5.8rem);
        line-height: .98;
        letter-spacing: -.06em;
      }
      h1 span { color: var(--accent); }
      .intro {
        max-width: 650px;
        margin: 0;
        color: var(--muted);
        font-size: clamp(1.05rem, 2vw, 1.24rem);
        line-height: 1.75;
      }
      .hero-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
      .button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 46px;
        padding: 11px 18px;
        border: 1px solid transparent;
        border-radius: 10px;
        cursor: pointer;
        font-weight: 750;
        text-decoration: none;
        transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
      }
      .button:hover { transform: translateY(-2px); }
      .button-primary {
        background: var(--accent);
        color: white;
        box-shadow: 0 8px 18px rgba(14, 124, 134, .18);
      }
      .button-primary:hover { background: var(--accent-dark); }
      .button-secondary { border-color: var(--line); background: var(--surface); color: var(--ink); }
      .hero-panel {
        position: relative;
        overflow: hidden;
        padding: 34px;
        border: 1px solid var(--line);
        border-radius: 28px;
        background: var(--surface);
        box-shadow: var(--shadow);
      }
      .hero-panel::before {
        position: absolute;
        top: -90px;
        inset-inline-end: -80px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: #d8f1ec;
        content: "";
      }
      .panel-label, .hero-panel h2, .hero-panel p, .panel-stat { position: relative; }
      .panel-label { color: var(--accent-dark); font-size: .8rem; font-weight: 800; }
      .hero-panel h2 { margin: 12px 0 13px; font-size: 1.65rem; line-height: 1.25; }
      .hero-panel p { margin: 0; color: var(--muted); line-height: 1.7; }
      .panel-stat {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid var(--line);
      }
      .stat-number { color: var(--accent); font-size: 1.75rem; font-weight: 850; }
      .stat-copy { color: var(--ink-soft); font-size: .9rem; line-height: 1.35; }
      .section { padding: 44px 0; }
      .section-heading {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 24px;
        margin-bottom: 24px;
      }
      .section-heading h2 { margin: 0; font-size: clamp(1.8rem, 4vw, 2.5rem); letter-spacing: -.04em; }
      .section-heading p { max-width: 480px; margin: 0; color: var(--muted); line-height: 1.6; }
      .search-box {
        display: grid;
        grid-template-columns: minmax(0, 1fr) minmax(180px, .42fr) auto;
        gap: 14px;
        align-items: end;
        margin-bottom: 12px;
        padding: 18px;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: rgba(255,255,255,.72);
      }
      .field { display: grid; gap: 7px; }
      .field label { color: var(--ink-soft); font-size: .86rem; font-weight: 750; }
      .field input, .field select {
        width: 100%;
        min-height: 44px;
        padding: 9px 12px;
        border: 1px solid #b9d5d1;
        border-radius: 9px;
        background: var(--surface);
        color: var(--ink);
      }
      .field input::placeholder { color: #728795; }
      .field input[aria-invalid="true"], .field select[aria-invalid="true"] { border-color: var(--error); }
      .form-message {
        min-height: 24px;
        margin: 0 0 18px;
        color: var(--ink-soft);
        font-size: .92rem;
      }
      .form-message.error { color: var(--error); font-weight: 650; }
      .jobs {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
      }
      .job-card {
        display: flex;
        flex-direction: column;
        min-height: 290px;
        padding: 24px;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: var(--surface);
        transition: transform .18s ease, box-shadow .18s ease;
      }
      .job-card:hover { transform: translateY(-3px); box-shadow: 0 12px 28px rgba(22,70,82,.09); }
      .job-type {
        align-self: start;
        margin-bottom: 17px;
        padding: 5px 9px;
        border-radius: 999px;
        background: var(--accent-pale);
        color: var(--accent-dark);
        font-size: .72rem;
        font-weight: 800;
      }
      .job-card h3 { margin: 0 0 8px; font-size: 1.23rem; line-height: 1.28; }
      .job-company { margin: 0 0 15px; color: var(--accent-dark); font-size: .9rem; font-weight: 700; }
      .job-description { margin: 0; color: var(--muted); font-size: .92rem; line-height: 1.6; }
      .job-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 14px;
        margin-top: auto;
        padding-top: 22px;
        color: var(--ink-soft);
        font-size: .8rem;
      }
      .job-meta span { display: inline-flex; align-items: center; gap: 5px; }
      .how-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
      .how-card { padding: 24px; border-top: 3px solid var(--accent); background: rgba(255,255,255,.58); }
      .how-number { color: var(--accent); font-size: .84rem; font-weight: 850; }
      .how-card h3 { margin: 13px 0 8px; font-size: 1.12rem; }
      .how-card p { margin: 0; color: var(--muted); line-height: 1.6; }
      footer {
        padding: 24px 0 34px;
        border-top: 1px solid var(--line);
        color: var(--muted);
        font-size: .88rem;
      }
      .footer-content { display: flex; justify-content: space-between; gap: 20px; }
      .footer-content p { margin: 0; }
      .visually-hidden {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
      }
      [dir="rtl"] body { font-family: Tahoma, Arial, "Segoe UI", sans-serif; }
      [dir="rtl"] h1 { letter-spacing: 0; line-height: 1.15; }
      [dir="rtl"] .eyebrow { letter-spacing: 0; }
      @media (max-width: 840px) {
        header { flex-wrap: wrap; row-gap: 14px; }
        nav { gap: 13px; }
        nav a { font-size: .83rem; }
        nav { order: 3; width: 100%; justify-content: space-between; flex-wrap: wrap; }
        .hero { grid-template-columns: 1fr; min-height: auto; }
        .jobs, .how-grid { grid-template-columns: repeat(2, 1fr); }
        .search-box { grid-template-columns: 1fr 1fr; }
        .search-box .button { grid-column: 1 / -1; }
      }
      @media (max-width: 620px) {
        .shell { width: min(100% - 28px, 560px); }
        header {
          display: grid;
          grid-template-columns: minmax(0, 1fr) auto;
          column-gap: 12px;
          row-gap: 10px;
          padding: 18px 0;
        }
        .brand {
          min-width: 0;
          gap: 8px;
          font-size: 1.08rem;
          white-space: normal;
        }
        .language-switcher { justify-self: end; }
        nav {
          grid-column: 1 / -1;
          order: initial;
          justify-content: space-between;
          gap: 8px 13px;
          padding-top: 0;
        }
        nav a { min-width: 0; overflow-wrap: anywhere; }
        .hero { padding: 42px 0 52px; }
        .hero-panel { padding: 27px; }
        .section-heading, .footer-content { display: block; }
        .section-heading p { margin-top: 10px; }
        .jobs, .how-grid, .search-box { grid-template-columns: 1fr; }
        .search-box .button { grid-column: auto; }
        .footer-content p + p { margin-top: 8px; }
      }
      @media (prefers-reduced-motion: reduce) {
        html { scroll-behavior: auto; }
        *, *::before, *::after { transition-duration: .01ms !important; animation-duration: .01ms !important; }
      }
    </style>
  </head>
  <body>
    <a class="skip-link" href="#main-content" data-i18n="skip">Skip to main content</a>
    <div class="shell">
      <header>
        <a class="brand" href="/" aria-label="Irada home" data-i18n-aria-label="homeLabel">
          <span class="mark" aria-hidden="true">إ</span>
          <span>Irada · إرادة</span>
        </a>
        <nav aria-label="Primary navigation" data-i18n-aria-label="navLabel">
          <a href="#jobs" data-i18n="navJobs">Find work</a>
          <a href="#how-it-works" data-i18n="navHow">How it works</a>
          <a href="#about" data-i18n="navAbout">About Irada</a>
        </nav>
        <div class="language-switcher" role="group" aria-label="Language" data-i18n-aria-label="languageLabel" dir="ltr">
          <button type="button" data-language="en" aria-pressed="true">EN</button>
          <button type="button" data-language="ar" aria-pressed="false">العربية</button>
        </div>
      </header>

        <main id="main-content" tabindex="-1">
        <section class="hero" id="about" aria-labelledby="hero-title">
          <div>
            <p class="eyebrow" data-i18n="eyebrow">Remote work · Sudanese talent</p>
            <h1 id="hero-title"><span data-i18n="heroLead">Work with</span> <span data-i18n="heroAccent">purpose.</span></h1>
            <p class="intro" data-i18n="heroIntro">
              Irada connects Sudanese talent with disabilities to accessible remote opportunities and organizations that value every perspective.
            </p>
            <div class="hero-actions">
              <a class="button button-primary" href="#jobs" data-i18n="heroPrimary">Explore opportunities</a>
              <a class="button button-secondary" href="#how-it-works" data-i18n="heroSecondary">See how it works</a>
            </div>
          </div>
          <aside class="hero-panel" aria-labelledby="panel-title">
            <div class="panel-label" data-i18n="panelLabel">A more inclusive future of work</div>
            <h2 id="panel-title" data-i18n="panelTitle">Your ability is your advantage.</h2>
            <p data-i18n="panelCopy">Find work that respects your strengths, your access needs, and the future you want to build.</p>
            <div class="panel-stat">
              <span class="stat-number">100%</span>
              <span class="stat-copy" data-i18n="panelStat">designed around accessible connection</span>
            </div>
          </aside>
        </section>

        <section class="section" id="jobs" aria-labelledby="jobs-title">
          <div class="section-heading">
            <div>
              <p class="eyebrow" data-i18n="jobsEyebrow">Start where you are</p>
              <h2 id="jobs-title" data-i18n="jobsTitle">Opportunities with room to grow</h2>
            </div>
            <p data-i18n="jobsIntro">Browse a few examples of remote roles created with flexibility and clear expectations in mind.</p>
          </div>
          <form class="search-box" id="job-search" aria-labelledby="jobs-title" novalidate>
            <div class="field">
              <label for="keyword" data-i18n="keywordLabel">Search roles</label>
              <input id="keyword" name="keyword" type="search" autocomplete="off" minlength="2" required aria-describedby="search-message" data-i18n-placeholder="keywordPlaceholder" placeholder="Try “customer support”">
            </div>
            <div class="field">
              <label for="work-type" data-i18n="typeLabel">Work type</label>
              <select id="work-type" name="workType">
                <option value="all" data-i18n="allTypes">All types</option>
                <option value="full-time" data-i18n="fullTime">Full time</option>
                <option value="part-time" data-i18n="partTime">Part time</option>
                <option value="contract" data-i18n="contract">Contract</option>
              </select>
            </div>
            <button class="button button-primary" type="submit" data-i18n="searchButton">Search roles</button>
          </form>
          <p class="form-message" id="search-message" role="status" aria-live="polite"></p>
          <div class="jobs" id="job-list" aria-live="polite"></div>
        </section>

        <section class="section" id="how-it-works" aria-labelledby="how-title">
          <div class="section-heading">
            <div>
              <p class="eyebrow" data-i18n="howEyebrow">A clear next step</p>
              <h2 id="how-title" data-i18n="howTitle">Work should meet you halfway</h2>
            </div>
            <p data-i18n="howIntro">Irada is built to make remote work feel more human, accessible, and possible.</p>
          </div>
          <div class="how-grid">
            <article class="how-card">
              <div class="how-number">01</div>
              <h3 data-i18n="stepOneTitle">Discover your fit</h3>
              <p data-i18n="stepOneCopy">Explore roles that match your skills, interests, and preferred way of working.</p>
            </article>
            <article class="how-card">
              <div class="how-number">02</div>
              <h3 data-i18n="stepTwoTitle">Show your strengths</h3>
              <p data-i18n="stepTwoCopy">Share what you do best in a process that values clarity over barriers.</p>
            </article>
            <article class="how-card">
              <div class="how-number">03</div>
              <h3 data-i18n="stepThreeTitle">Build what is next</h3>
              <p data-i18n="stepThreeCopy">Connect with teams ready to make space for your contribution and growth.</p>
            </article>
          </div>
        </section>
      </main>

      <footer>
        <div class="footer-content">
          <p><strong>Irada · إرادة</strong> <span data-i18n="footerTag">— accessible work with purpose.</span></p>
          <p data-i18n="footerStatus">A welcoming starting point for Sudanese talent and organizations.</p>
        </div>
      </footer>
    </div>

    <script>
      const translations = {
        en: {
          skip: "Skip to main content",
          pageTitle: "Irada | Accessible work with purpose",
          pageDescription: "Irada connects Sudanese talent with disabilities to accessible remote opportunities.",
          homeLabel: "Irada home",
          navLabel: "Primary navigation",
          navJobs: "Find work",
          navHow: "How it works",
          navAbout: "About Irada",
          languageLabel: "Language",
          eyebrow: "Remote work · Sudanese talent",
          heroLead: "Work with",
          heroAccent: "purpose.",
          heroIntro: "Irada connects Sudanese talent with disabilities to accessible remote opportunities and organizations that value every perspective.",
          heroPrimary: "Explore opportunities",
          heroSecondary: "See how it works",
          panelLabel: "A more inclusive future of work",
          panelTitle: "Your ability is your advantage.",
          panelCopy: "Find work that respects your strengths, your access needs, and the future you want to build.",
          panelStat: "designed around accessible connection",
          jobsEyebrow: "Start where you are",
          jobsTitle: "Opportunities with room to grow",
          jobsIntro: "Browse a few examples of remote roles created with flexibility and clear expectations in mind.",
          keywordLabel: "Search roles",
          keywordPlaceholder: "Try “customer support”",
          typeLabel: "Work type",
          allTypes: "All types",
          fullTime: "Full time",
          partTime: "Part time",
          contract: "Contract",
          searchButton: "Search roles",
          searchRequired: "Enter at least 2 characters to search roles.",
          searchFoundOne: "{count} roles match “{keyword}”.",
          searchFoundMany: "{count} roles match “{keyword}”.",
          searchNone: "No roles match “{keyword}” yet. Try another search.",
          howEyebrow: "A clear next step",
          howTitle: "Work should meet you halfway",
          howIntro: "Irada is built to make remote work feel more human, accessible, and possible.",
          stepOneTitle: "Discover your fit",
          stepOneCopy: "Explore roles that match your skills, interests, and preferred way of working.",
          stepTwoTitle: "Show your strengths",
          stepTwoCopy: "Share what you do best in a process that values clarity over barriers.",
          stepThreeTitle: "Build what is next",
          stepThreeCopy: "Connect with teams ready to make space for your contribution and growth.",
          footerTag: "— accessible work with purpose.",
          footerStatus: "A welcoming starting point for Sudanese talent and organizations.",
          locationRemote: "Remote",
          typeRoleFullTime: "Full time",
          typeRolePartTime: "Part time",
          typeRoleContract: "Contract",
          jobSupportTitle: "Customer support specialist",
          jobSupportCompany: "Nile Connect",
          jobSupportDescription: "Help customers feel heard through thoughtful chat and email support.",
          jobContentTitle: "Content assistant",
          jobContentCompany: "Saha Studio",
          jobContentDescription: "Turn ideas into clear, useful content for a growing social enterprise.",
          jobDataTitle: "Data entry coordinator",
          jobDataCompany: "Wadi Partners",
          jobDataDescription: "Keep important information organized with care, focus, and flexible hours."
        },
        ar: {
          skip: "انتقل إلى المحتوى الرئيسي",
          pageTitle: "إرادة | عمل ميسّر وهادف",
          pageDescription: "تصل إرادة المواهب السودانية من ذوي الإعاقة بفرص عمل عن بُعد ميسّرة.",
          homeLabel: "الصفحة الرئيسية لإرادة",
          navLabel: "التنقل الرئيسي",
          navJobs: "اكتشف الوظائف",
          navHow: "كيف تعمل المنصة",
          navAbout: "عن إرادة",
          languageLabel: "اللغة",
          eyebrow: "عمل عن بُعد · مواهب سودانية",
          heroLead: "اعمل",
          heroAccent: "بهدف.",
          heroIntro: "تصل إرادة المواهب السودانية من ذوي الإعاقة بفرص عمل عن بُعد ميسّرة، وبمؤسسات تقدّر اختلاف كل شخص.",
          heroPrimary: "استكشف الفرص",
          heroSecondary: "تعرّف على الطريقة",
          panelLabel: "مستقبل أكثر شمولاً للعمل",
          panelTitle: "قدرتك هي مصدر تميّزك.",
          panelCopy: "اعثر على عمل يحترم نقاط قوتك واحتياجاتك المتعلقة بإتاحة الوصول والمستقبل الذي تريد بناءه.",
          panelStat: "مصممة لتسهيل التواصل الميسّر",
          jobsEyebrow: "ابدأ من مكانك",
          jobsTitle: "فرص تمنحك مساحة للنمو",
          jobsIntro: "تصفّح أمثلة على وظائف عن بُعد صُممت بمرونة وتوقعات واضحة.",
          keywordLabel: "ابحث عن وظيفة",
          keywordPlaceholder: "جرّب «خدمة العملاء»",
          typeLabel: "نوع العمل",
          allTypes: "كل الأنواع",
          fullTime: "دوام كامل",
          partTime: "دوام جزئي",
          contract: "تعاقد",
          searchButton: "ابحث عن وظائف",
          searchRequired: "أدخل حرفين على الأقل للبحث عن الوظائف.",
          searchFoundOne: "وجدنا وظيفة واحدة تطابق بحثك عن «{keyword}».",
          searchFoundMany: "وجدنا {count} وظائف تطابق بحثك عن «{keyword}».",
          searchNone: "لا توجد وظائف تطابق بحثك عن «{keyword}» حالياً. جرّب بحثاً آخر.",
          howEyebrow: "خطوة واضحة إلى الأمام",
          howTitle: "العمل يجب أن يلتقي بك في منتصف الطريق",
          howIntro: "صُممت إرادة لتجعل العمل عن بُعد أكثر إنسانية وإتاحة وإمكانية.",
          stepOneTitle: "اكتشف ما يناسبك",
          stepOneCopy: "استكشف الوظائف التي تتوافق مع مهاراتك واهتماماتك وطريقتك المفضلة في العمل.",
          stepTwoTitle: "أظهر نقاط قوتك",
          stepTwoCopy: "شارك أفضل ما لديك من خلال عملية تقدّر الوضوح وتزيل الحواجز.",
          stepThreeTitle: "ابنِ خطوتك القادمة",
          stepThreeCopy: "تواصل مع فرق مستعدة لإفساح المجال لمساهمتك ونموك.",
          footerTag: "— عمل ميسّر وهادف.",
          footerStatus: "بداية مرحّبة بالمواهب السودانية والمؤسسات.",
          locationRemote: "عن بُعد",
          typeRoleFullTime: "دوام كامل",
          typeRolePartTime: "دوام جزئي",
          typeRoleContract: "تعاقد",
          jobSupportTitle: "أخصائي دعم العملاء",
          jobSupportCompany: "نايل كونيكت",
          jobSupportDescription: "ساعد العملاء على الشعور بأنهم مسموعون من خلال دعم لطيف عبر الدردشة والبريد الإلكتروني.",
          jobContentTitle: "مساعد محتوى",
          jobContentCompany: "استوديو صحة",
          jobContentDescription: "حوّل الأفكار إلى محتوى واضح ومفيد لمؤسسة اجتماعية متنامية.",
          jobDataTitle: "منسق إدخال بيانات",
          jobDataCompany: "شركاء وادي",
          jobDataDescription: "حافظ على تنظيم المعلومات المهمة بعناية وتركيز وساعات عمل مرنة."
        }
      };

      const jobs = [
        { type: "full-time", title: "jobSupportTitle", company: "jobSupportCompany", description: "jobSupportDescription", typeLabel: "typeRoleFullTime" },
        { type: "part-time", title: "jobContentTitle", company: "jobContentCompany", description: "jobContentDescription", typeLabel: "typeRolePartTime" },
        { type: "contract", title: "jobDataTitle", company: "jobDataCompany", description: "jobDataDescription", typeLabel: "typeRoleContract" }
      ];

      let currentLanguage = "en";
      const languageButtons = document.querySelectorAll("[data-language]");
      const html = document.documentElement;
      const skipLink = document.querySelector(".skip-link");
      const mainContent = document.getElementById("main-content");
      const searchForm = document.getElementById("job-search");
      const keyword = document.getElementById("keyword");
      const workType = document.getElementById("work-type");
      const searchMessage = document.getElementById("search-message");
      const jobList = document.getElementById("job-list");

      function text(key, language = currentLanguage) {
        const catalog = translations[language];
        if (!catalog || !Object.prototype.hasOwnProperty.call(catalog, key)) {
          throw new Error(`Missing ${language} translation key: ${key}`);
        }
        return catalog[key];
      }

      function applyTranslations() {
        document.querySelectorAll("[data-i18n]").forEach((element) => {
          element.textContent = text(element.dataset.i18n);
        });
        document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
          element.placeholder = text(element.dataset.i18nPlaceholder);
        });
        document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
          element.setAttribute("aria-label", text(element.dataset.i18nAriaLabel));
        });
        document.title = text("pageTitle");
        document.getElementById("page-description").setAttribute("content", text("pageDescription"));
        html.lang = currentLanguage;
        html.dir = currentLanguage === "ar" ? "rtl" : "ltr";
        languageButtons.forEach((button) => {
          button.setAttribute("aria-pressed", String(button.dataset.language === currentLanguage));
        });
      }

      function renderJobs(filteredJobs = jobs) {
        jobList.innerHTML = filteredJobs.map((job) => `
          <article class="job-card">
            <div class="job-type">${text(job.typeLabel)}</div>
            <h3>${text(job.title)}</h3>
            <p class="job-company">${text(job.company)}</p>
            <p class="job-description">${text(job.description)}</p>
            <div class="job-meta">
              <span>${text("locationRemote")}</span>
              <span>${text(job.typeLabel)}</span>
            </div>
          </article>
        `).join("");
      }

      function showSearchMessage(key, values = {}, isError = false) {
        let message = text(key);
        Object.entries(values).forEach(([name, value]) => {
          message = message.replace(`{${name}}`, value);
        });
        searchMessage.textContent = message;
        searchMessage.classList.toggle("error", isError);
      }

      skipLink.addEventListener("click", (event) => {
        event.preventDefault();
        mainContent.focus({ preventScroll: true });
        mainContent.scrollIntoView({ block: "start" });
      });

      function searchJobs(event) {
        event.preventDefault();
        const query = keyword.value.trim();
        keyword.setAttribute("aria-invalid", String(query.length < 2));
        if (query.length < 2) {
          showSearchMessage("searchRequired", {}, true);
          keyword.focus();
          renderJobs([]);
          return;
        }
        const selectedType = workType.value;
        const normalizedQuery = query.toLocaleLowerCase();
        const filteredJobs = jobs.filter((job) => {
          const searchable = ["en", "ar"].flatMap((language) => [
            text(job.title, language),
            text(job.company, language),
            text(job.description, language)
          ]).join(" ").toLocaleLowerCase();
          return searchable.includes(normalizedQuery) && (selectedType === "all" || selectedType === job.type);
        });
        renderJobs(filteredJobs);
        const resultMessageKey = filteredJobs.length === 0
          ? "searchNone"
          : filteredJobs.length === 1
            ? "searchFoundOne"
            : "searchFoundMany";
        showSearchMessage(resultMessageKey, { count: filteredJobs.length, keyword: query });
      }

      languageButtons.forEach((button) => {
        button.addEventListener("click", () => {
          currentLanguage = button.dataset.language;
          try { localStorage.setItem("irada-language", currentLanguage); } catch (error) {}
          applyTranslations();
          renderJobs();
          if (keyword.value.trim()) {
            searchJobs({ preventDefault: () => {} });
          } else {
            searchMessage.textContent = "";
          }
        });
      });

      searchForm.addEventListener("submit", searchJobs);
      try {
        const savedLanguage = localStorage.getItem("irada-language");
        if (savedLanguage === "ar" || savedLanguage === "en") currentLanguage = savedLanguage;
      } catch (error) {}
      applyTranslations();
      renderJobs();
    </script>
  </body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(PAGE)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
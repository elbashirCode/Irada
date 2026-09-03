import os

from flask import Flask, jsonify, render_template_string


app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Irada | إرادة</title>
    <style>
      :root {
        color-scheme: light;
        --ink: #17324d;
        --muted: #5f7181;
        --accent: #0e7c86;
        --accent-dark: #07545d;
        --surface: #ffffff;
        --background: #f2f8f7;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        background: var(--background);
        color: var(--ink);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
          Tahoma, Arial, sans-serif;
      }
      .shell {
        width: min(1100px, calc(100% - 40px));
        margin: 0 auto;
      }
      header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 28px 0;
      }
      .brand {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        color: var(--ink);
        font-size: 1.25rem;
        font-weight: 750;
        text-decoration: none;
      }
      .mark {
        display: grid;
        width: 42px;
        height: 42px;
        place-items: center;
        border-radius: 12px;
        background: var(--accent);
        color: white;
        font-size: 1.25rem;
      }
      .language {
        color: var(--muted);
        font-size: .9rem;
      }
      main {
        display: grid;
        grid-template-columns: 1.1fr .9fr;
        gap: 64px;
        align-items: center;
        min-height: calc(100vh - 108px);
        padding: 28px 0 76px;
      }
      .eyebrow {
        color: var(--accent-dark);
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
      }
      h1 {
        max-width: 680px;
        margin: 16px 0;
        font-size: clamp(2.7rem, 7vw, 5.6rem);
        line-height: .98;
        letter-spacing: -.055em;
      }
      h1 span { color: var(--accent); }
      .intro {
        max-width: 600px;
        margin: 0;
        color: var(--muted);
        font-size: clamp(1.05rem, 2vw, 1.25rem);
        line-height: 1.7;
      }
      .status {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        margin-top: 32px;
        padding: 12px 16px;
        border: 1px solid #bde1db;
        border-radius: 999px;
        background: #e7f6f2;
        color: var(--accent-dark);
        font-weight: 650;
      }
      .dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #22a37d;
        box-shadow: 0 0 0 4px #c4eadf;
      }
      .card {
        position: relative;
        overflow: hidden;
        padding: 38px;
        border: 1px solid #d7e8e5;
        border-radius: 28px;
        background: var(--surface);
        box-shadow: 0 24px 65px rgba(22, 70, 82, .12);
      }
      .card::before {
        position: absolute;
        top: -85px;
        right: -75px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: #d9f1ec;
        content: "";
      }
      .card h2, .card p { position: relative; }
      .card h2 { margin: 0 0 14px; font-size: 1.55rem; }
      .card p { margin: 0; color: var(--muted); line-height: 1.7; }
      .arabic {
        margin-top: 34px !important;
        color: var(--accent) !important;
        font-size: 2.7rem;
        font-weight: 700;
        line-height: 1.25 !important;
        direction: rtl;
      }
      @media (max-width: 760px) {
        .shell { width: min(100% - 28px, 620px); }
        header { padding: 20px 0; }
        main {
          display: block;
          min-height: auto;
          padding: 54px 0 48px;
        }
        .card { margin-top: 42px; padding: 28px; }
      }
    </style>
  </head>
  <body>
    <div class="shell">
      <header>
        <a class="brand" href="/">
          <span class="mark" aria-hidden="true">إ</span>
          <span>Irada · إرادة</span>
        </a>
        <span class="language">Accessible by design</span>
      </header>
      <main>
        <section>
          <div class="eyebrow">Remote work · Sudanese talent</div>
          <h1>Work with <span>purpose.</span></h1>
          <p class="intro">
            Irada is a remote hiring platform empowering Sudanese talents with
            disabilities through accessible online jobs.
          </p>
          <div class="status"><span class="dot" aria-hidden="true"></span> Flask app is running</div>
        </section>
        <aside class="card" aria-label="Project status">
          <h2>A more inclusive future of work</h2>
          <p>
            This starter page confirms that the imported project is connected
            and ready for the next stage of product development.
          </p>
          <p class="arabic" lang="ar">إرادة</p>
        </aside>
      </main>
    </div>
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
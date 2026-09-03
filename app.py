import functools
import hmac
import os
import secrets
import sqlite3
from datetime import datetime

from flask import (
    Flask,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "SESSION_SECRET", "local-development-secret-change-me"
)
app.config["DATABASE"] = os.environ.get(
    "IRADA_DB_PATH", os.path.join(os.path.dirname(__file__), "irada.db")
)

STATUSES = ("submitted", "reviewing", "shortlisted", "declined", "hired")
WORK_TYPES = ("full-time", "part-time", "contract")

TRANSLATIONS = {
    "en": {
        "language_name": "English",
        "other_language": "العربية",
        "home": "Home",
        "find_work": "Find work",
        "how_it_works": "How it works",
        "dashboard": "Dashboard",
        "sign_in": "Sign in",
        "create_account": "Create account",
        "sign_out": "Sign out",
        "profile": "My profile",
        "organization": "Organization",
        "candidate": "Candidate",
        "remote_work": "Remote work · Sudanese talent",
        "hero_title": "Work with <span>purpose.</span>",
        "hero_intro": "Irada connects Sudanese talent with disabilities to accessible remote opportunities and organizations that value every perspective.",
        "explore_jobs": "Explore opportunities",
        "join_irada": "Join Irada",
        "inclusive_future": "A more inclusive future of work",
        "inclusive_copy": "Find work that respects your strengths, your access needs, and the future you want to build.",
        "open_roles": "open roles",
        "roles_heading": "Opportunities with room to grow",
        "roles_intro": "Browse remote roles created with flexibility and clear expectations in mind.",
        "search_roles": "Search roles",
        "search_placeholder": "Try “customer support”",
        "work_type": "Work type",
        "all_types": "All types",
        "full_time": "Full time",
        "part_time": "Part time",
        "contract": "Contract",
        "search": "Search",
        "search_found": "{count} roles match “{query}”.",
        "search_none": "No roles match “{query}” yet. Try another search.",
        "showing_all": "Showing all open roles.",
        "remote": "Remote",
        "apply": "Apply now",
        "view_role": "View role",
        "no_roles": "No open roles yet. Organizations can publish the first opportunity.",
        "how_title": "Work should meet you halfway",
        "how_intro": "Irada is built to make remote work feel more human, accessible, and possible.",
        "discover_fit": "Discover your fit",
        "discover_copy": "Explore roles that match your skills, interests, and preferred way of working.",
        "show_strengths": "Show your strengths",
        "show_copy": "Share what you do best in a process that values clarity over barriers.",
        "build_next": "Build what is next",
        "build_copy": "Connect with teams ready to make space for your contribution and growth.",
        "footer": "Accessible work with purpose.",
        "login_title": "Welcome back",
        "register_title": "Create your Irada account",
        "email": "Email address",
        "password": "Password",
        "full_name": "Full name",
        "account_type": "I am joining as a",
        "candidate_account": "Candidate",
        "organization_account": "Organization",
        "company_name": "Organization name",
        "password_hint": "At least 8 characters",
        "sign_in_action": "Sign in",
        "create_account_action": "Create account",
        "need_account": "New to Irada?",
        "have_account": "Already have an account?",
        "candidate_dashboard": "Candidate dashboard",
        "organization_dashboard": "Organization dashboard",
        "welcome": "Welcome, {name}",
        "applications": "Applications",
        "my_applications": "My applications",
        "no_applications": "You have not applied to a role yet.",
        "browse_roles": "Browse open roles",
        "saved_profile": "Your profile helps organizations understand your strengths.",
        "edit_profile": "Edit profile",
        "bio": "About you",
        "skills": "Skills",
        "access_needs": "Access needs (optional)",
        "access_needs_hint": "Share what would help you do your best work.",
        "save_profile": "Save profile",
        "manage_jobs": "Manage jobs",
        "post_job": "Post a new job",
        "no_jobs": "You have not posted a role yet.",
        "applicants": "applicants",
        "edit": "Edit",
        "close": "Close",
        "closed": "Closed",
        "open": "Open",
        "review_applications": "Review applications",
        "job_title": "Job title",
        "description": "Description",
        "publish_job": "Publish job",
        "save_changes": "Save changes",
        "edit_job": "Edit job",
        "new_job": "Post a new accessible remote job",
        "accessibility": "Accessibility and flexibility",
        "accessibility_hint": "Describe accommodations, schedule flexibility, or tools you provide.",
        "job_details": "Role details",
        "organization_label": "Organization",
        "application_note": "Why are you a good fit?",
        "application_note_hint": "Share a short note about your experience and strengths.",
        "submit_application": "Submit application",
        "application_sent": "Your application was sent.",
        "already_applied": "You already applied to this role.",
        "sign_in_to_apply": "Sign in as a candidate to apply.",
        "status": "Status",
        "status_submitted": "Submitted",
        "status_reviewing": "In review",
        "status_shortlisted": "Shortlisted",
        "status_declined": "Not selected",
        "status_hired": "Hired",
        "update_status": "Update status",
        "candidate_profile": "Candidate profile",
        "member_since": "Member since {date}",
        "back": "Back",
        "required": "Please complete all required fields.",
        "invalid_login": "That email or password is not correct.",
        "email_exists": "An account with that email already exists.",
        "password_short": "Password must be at least 8 characters.",
        "role_required": "Choose whether you are a candidate or organization.",
        "company_required": "Organization name is required for organization accounts.",
        "profile_saved": "Profile saved.",
        "job_saved": "Job published.",
        "job_updated": "Job updated.",
        "job_closed": "Job closed.",
        "not_authorized": "You do not have permission to do that.",
        "invalid_status": "Choose a valid application status.",
        "csrf_error": "This form expired. Please try again.",
        "job_not_found": "That role is no longer available.",
    },
    "ar": {
        "language_name": "العربية",
        "other_language": "English",
        "home": "الرئيسية",
        "find_work": "اكتشف الوظائف",
        "how_it_works": "كيف تعمل المنصة",
        "dashboard": "لوحة التحكم",
        "sign_in": "تسجيل الدخول",
        "create_account": "إنشاء حساب",
        "sign_out": "تسجيل الخروج",
        "profile": "ملفي الشخصي",
        "organization": "مؤسسة",
        "candidate": "متقدم للوظيفة",
        "remote_work": "عمل عن بُعد · مواهب سودانية",
        "hero_title": "اعمل <span>بهدف.</span>",
        "hero_intro": "تصل إرادة المواهب السودانية من ذوي الإعاقة بفرص عمل عن بُعد ميسّرة، وبمؤسسات تقدّر اختلاف كل شخص.",
        "explore_jobs": "استكشف الفرص",
        "join_irada": "انضم إلى إرادة",
        "inclusive_future": "مستقبل أكثر شمولاً للعمل",
        "inclusive_copy": "اعثر على عمل يحترم نقاط قوتك واحتياجاتك المتعلقة بإتاحة الوصول والمستقبل الذي تريد بناءه.",
        "open_roles": "وظائف مفتوحة",
        "roles_heading": "فرص تمنحك مساحة للنمو",
        "roles_intro": "تصفّح وظائف عن بُعد صُممت بمرونة وتوقعات واضحة.",
        "search_roles": "ابحث عن وظيفة",
        "search_placeholder": "جرّب «خدمة العملاء»",
        "work_type": "نوع العمل",
        "all_types": "كل الأنواع",
        "full_time": "دوام كامل",
        "part_time": "دوام جزئي",
        "contract": "تعاقد",
        "search": "بحث",
        "search_found": "تطابق {count} وظائف مع بحث «{query}».",
        "search_none": "لا توجد وظائف تطابق «{query}» حالياً. جرّب بحثاً آخر.",
        "showing_all": "تظهر هنا كل الوظائف المفتوحة.",
        "remote": "عن بُعد",
        "apply": "قدّم الآن",
        "view_role": "عرض الوظيفة",
        "no_roles": "لا توجد وظائف مفتوحة بعد. يمكن للمؤسسات نشر أول فرصة.",
        "how_title": "العمل يجب أن يلتقي بك في منتصف الطريق",
        "how_intro": "صُممت إرادة لتجعل العمل عن بُعد أكثر إنسانية وإتاحة وإمكانية.",
        "discover_fit": "اكتشف ما يناسبك",
        "discover_copy": "استكشف الوظائف التي تتوافق مع مهاراتك واهتماماتك وطريقتك المفضلة في العمل.",
        "show_strengths": "أظهر نقاط قوتك",
        "show_copy": "شارك أفضل ما لديك من خلال عملية تقدّر الوضوح وتزيل الحواجز.",
        "build_next": "ابنِ خطوتك القادمة",
        "build_copy": "تواصل مع فرق مستعدة لإفساح المجال لمساهمتك ونموك.",
        "footer": "عمل ميسّر وهادف.",
        "login_title": "مرحباً بعودتك",
        "register_title": "أنشئ حسابك في إرادة",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "full_name": "الاسم الكامل",
        "account_type": "سأنضم بصفتي",
        "candidate_account": "متقدماً لوظيفة",
        "organization_account": "مؤسسة",
        "company_name": "اسم المؤسسة",
        "password_hint": "8 أحرف على الأقل",
        "sign_in_action": "تسجيل الدخول",
        "create_account_action": "إنشاء الحساب",
        "need_account": "جديد في إرادة؟",
        "have_account": "لديك حساب بالفعل؟",
        "candidate_dashboard": "لوحة المتقدم",
        "organization_dashboard": "لوحة المؤسسة",
        "welcome": "مرحباً، {name}",
        "applications": "الطلبات",
        "my_applications": "طلباتي",
        "no_applications": "لم تتقدم إلى وظيفة بعد.",
        "browse_roles": "تصفح الوظائف المفتوحة",
        "saved_profile": "يساعد ملفك الشخصي المؤسسات على فهم نقاط قوتك.",
        "edit_profile": "تعديل الملف الشخصي",
        "bio": "نبذة عنك",
        "skills": "المهارات",
        "access_needs": "احتياجات الوصول (اختياري)",
        "access_needs_hint": "شارك ما يساعدك على تقديم أفضل ما لديك.",
        "save_profile": "حفظ الملف الشخصي",
        "manage_jobs": "إدارة الوظائف",
        "post_job": "نشر وظيفة جديدة",
        "no_jobs": "لم تنشر وظيفة بعد.",
        "applicants": "متقدمين",
        "edit": "تعديل",
        "close": "إغلاق",
        "closed": "مغلقة",
        "open": "مفتوحة",
        "review_applications": "مراجعة الطلبات",
        "job_title": "المسمى الوظيفي",
        "description": "الوصف",
        "publish_job": "نشر الوظيفة",
        "save_changes": "حفظ التغييرات",
        "edit_job": "تعديل الوظيفة",
        "new_job": "انشر وظيفة عن بُعد ميسّرة",
        "accessibility": "الإتاحة والمرونة",
        "accessibility_hint": "اذكر التسهيلات أو مرونة المواعيد أو الأدوات التي توفرها.",
        "job_details": "تفاصيل الوظيفة",
        "organization_label": "المؤسسة",
        "application_note": "لماذا تناسبك هذه الوظيفة؟",
        "application_note_hint": "شارك نبذة عن خبرتك ونقاط قوتك.",
        "submit_application": "إرسال الطلب",
        "application_sent": "تم إرسال طلبك.",
        "already_applied": "لقد تقدمت إلى هذه الوظيفة بالفعل.",
        "sign_in_to_apply": "سجّل الدخول كمتقدم للتقديم.",
        "status": "الحالة",
        "status_submitted": "تم الإرسال",
        "status_reviewing": "قيد المراجعة",
        "status_shortlisted": "ضمن القائمة المختصرة",
        "status_declined": "لم يتم الاختيار",
        "status_hired": "تم التوظيف",
        "update_status": "تحديث الحالة",
        "candidate_profile": "ملف المتقدم",
        "member_since": "عضو منذ {date}",
        "back": "رجوع",
        "required": "يرجى إكمال الحقول المطلوبة.",
        "invalid_login": "البريد الإلكتروني أو كلمة المرور غير صحيحة.",
        "email_exists": "يوجد حساب بهذا البريد الإلكتروني بالفعل.",
        "password_short": "يجب أن تتكون كلمة المرور من 8 أحرف على الأقل.",
        "role_required": "اختر ما إذا كنت متقدماً أو مؤسسة.",
        "company_required": "اسم المؤسسة مطلوب لحسابات المؤسسات.",
        "profile_saved": "تم حفظ الملف الشخصي.",
        "job_saved": "تم نشر الوظيفة.",
        "job_updated": "تم تحديث الوظيفة.",
        "job_closed": "تم إغلاق الوظيفة.",
        "not_authorized": "ليس لديك صلاحية لتنفيذ ذلك.",
        "invalid_status": "اختر حالة طلب صحيحة.",
        "csrf_error": "انتهت صلاحية هذا النموذج. يرجى المحاولة مجدداً.",
        "job_not_found": "هذه الوظيفة لم تعد متاحة.",
    },
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_db(query, params=(), one=False):
    cursor = get_db().execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    return (rows[0] if rows else None) if one else rows


def init_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('candidate', 'organization')),
            full_name TEXT NOT NULL,
            company_name TEXT,
            bio TEXT NOT NULL DEFAULT '',
            skills TEXT NOT NULL DEFAULT '',
            access_needs TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            work_type TEXT NOT NULL CHECK (work_type IN ('full-time', 'part-time', 'contract')),
            accessibility TEXT NOT NULL DEFAULT '',
            is_open INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (organization_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            cover_note TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'submitted',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (job_id, candidate_id),
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            FOREIGN KEY (candidate_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS jobs_open_idx ON jobs(is_open);
        CREATE INDEX IF NOT EXISTS applications_candidate_idx ON applications(candidate_id);
        """
    )
    seed = db.execute(
        "SELECT id FROM users WHERE email = ?", ("seed@irada.local",)
    ).fetchone()
    if seed is None:
        cursor = db.execute(
            """
            INSERT INTO users (email, password_hash, role, full_name, company_name)
            VALUES (?, ?, 'organization', ?, ?)
            """,
            (
                "seed@irada.local",
                generate_password_hash(secrets.token_urlsafe(24)),
                "Irada partner",
                "Irada partner",
            ),
        )
        seed_id = cursor.lastrowid
        db.executemany(
            """
            INSERT INTO jobs (organization_id, title, description, work_type, accessibility)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    seed_id,
                    "Customer support specialist",
                    "Help customers feel heard through thoughtful chat and email support.",
                    "full-time",
                    "Flexible schedules and written-first communication.",
                ),
                (
                    seed_id,
                    "Content assistant",
                    "Turn ideas into clear, useful content for a growing social enterprise.",
                    "part-time",
                    "Async collaboration and clear written briefs.",
                ),
                (
                    seed_id,
                    "Data entry coordinator",
                    "Keep important information organized with care, focus, and flexible hours.",
                    "contract",
                    "Flexible hours and step-by-step onboarding.",
                ),
            ],
        )
    db.commit()
    db.close()


def current_language():
    language = session.get("language", "en")
    return language if language in TRANSLATIONS else "en"


def translate(key, **values):
    value = TRANSLATIONS[current_language()].get(
        key, TRANSLATIONS["en"].get(key, key)
    )
    return value.format(**values) if values else value


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.context_processor
def inject_template_helpers():
    return {
        "t": translate,
        "csrf_token": csrf_token,
        "current_language": current_language(),
        "current_user": getattr(g, "user", None),
        "job_type_label": job_type_label,
        "status_options": STATUSES,
        "work_types": WORK_TYPES,
    }


@app.before_request
def load_user():
    g.user = None
    user_id = session.get("user_id")
    if user_id:
        g.user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
        if g.user is None:
            session.clear()


@app.before_request
def protect_mutations():
    if request.method == "POST":
        supplied = request.form.get("csrf_token", "")
        expected = session.get("csrf_token", "")
        if not expected or not supplied or not hmac.compare_digest(supplied, expected):
            flash(translate("csrf_error"), "error")
            abort(400)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash(translate("sign_in_to_apply"), "error")
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)

    return wrapped_view


def role_required(role):
    def decorator(view):
        @functools.wraps(view)
        @login_required
        def wrapped_view(**kwargs):
            if g.user["role"] != role:
                flash(translate("not_authorized"), "error")
                return redirect(url_for("dashboard"))
            return view(**kwargs)

        return wrapped_view

    return decorator


def safe_next(default_endpoint="home"):
    destination = request.values.get("next", "")
    if destination.startswith("/") and not destination.startswith("//"):
        return destination
    return url_for(default_endpoint)


def job_type_label(work_type):
    return {
        "full-time": translate("full_time"),
        "part-time": translate("part_time"),
        "contract": translate("contract"),
    }.get(work_type, work_type)


@app.template_filter("date_only")
def date_only(value):
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value).strftime("%d %b %Y")
    except ValueError:
        return value[:10]


@app.get("/")
def home():
    query = request.args.get("q", "").strip()
    work_type = request.args.get("work_type", "all")
    conditions = ["jobs.is_open = 1"]
    params = []
    if query:
        conditions.append(
            "(jobs.title LIKE ? OR jobs.description LIKE ? OR users.company_name LIKE ?)"
        )
        term = f"%{query}%"
        params.extend([term, term, term])
    if work_type in WORK_TYPES:
        conditions.append("jobs.work_type = ?")
        params.append(work_type)
    jobs = query_db(
        f"""
        SELECT jobs.*, users.company_name
        FROM jobs JOIN users ON users.id = jobs.organization_id
        WHERE {" AND ".join(conditions)}
        ORDER BY jobs.created_at DESC, jobs.id DESC
        """,
        params,
    )
    if query:
        search_message = translate(
            "search_found" if jobs else "search_none",
            count=len(jobs),
            query=query,
        )
    else:
        search_message = translate("showing_all")
    open_count = query_db(
        "SELECT COUNT(*) AS count FROM jobs WHERE is_open = 1", one=True
    )["count"]
    return render_template(
        "index.html",
        jobs=jobs,
        query=query,
        work_type=work_type,
        search_message=search_message,
        open_count=open_count,
    )


@app.get("/language/<language>")
def set_language(language):
    if language in TRANSLATIONS:
        session["language"] = language
    return redirect(safe_next())


@app.route("/register", methods=("GET", "POST"))
def register():
    if g.user:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        full_name = request.form.get("full_name", "").strip()
        role = request.form.get("role", "")
        company_name = request.form.get("company_name", "").strip()
        error = None
        if not email or not password or not full_name:
            error = translate("required")
        elif len(password) < 8:
            error = translate("password_short")
        elif role not in ("candidate", "organization"):
            error = translate("role_required")
        elif role == "organization" and not company_name:
            error = translate("company_required")
        if error is None:
            try:
                db = get_db()
                cursor = db.execute(
                    """
                    INSERT INTO users (email, password_hash, role, full_name, company_name)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        email,
                        generate_password_hash(password),
                        role,
                        full_name,
                        company_name or None,
                    ),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = translate("email_exists")
        if error:
            flash(error, "error")
        else:
            session.clear()
            session["user_id"] = cursor.lastrowid
            session["csrf_token"] = secrets.token_urlsafe(32)
            flash(translate("welcome", name=full_name), "success")
            return redirect(safe_next("dashboard"))
    return render_template("auth.html", mode="register")


@app.route("/login", methods=("GET", "POST"))
def login():
    if g.user:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)
        if user is None or not check_password_hash(user["password_hash"], password):
            flash(translate("invalid_login"), "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["csrf_token"] = secrets.token_urlsafe(32)
            return redirect(safe_next("dashboard"))
    return render_template("auth.html", mode="login")


@app.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.get("/dashboard")
@login_required
def dashboard():
    if g.user["role"] == "candidate":
        applications = query_db(
            """
            SELECT applications.*, jobs.title, jobs.work_type, users.company_name
            FROM applications
            JOIN jobs ON jobs.id = applications.job_id
            JOIN users ON users.id = jobs.organization_id
            WHERE applications.candidate_id = ?
            ORDER BY applications.created_at DESC
            """,
            (g.user["id"],),
        )
        return render_template("candidate_dashboard.html", applications=applications)
    jobs = query_db(
        """
        SELECT jobs.*, COUNT(applications.id) AS applicant_count
        FROM jobs LEFT JOIN applications ON applications.job_id = jobs.id
        WHERE jobs.organization_id = ?
        GROUP BY jobs.id
        ORDER BY jobs.created_at DESC
        """,
        (g.user["id"],),
    )
    applications = query_db(
        """
        SELECT applications.*, jobs.title, users.full_name, users.email,
               users.bio, users.skills, users.access_needs
        FROM applications
        JOIN jobs ON jobs.id = applications.job_id
        JOIN users ON users.id = applications.candidate_id
        WHERE jobs.organization_id = ?
        ORDER BY applications.created_at DESC
        """,
        (g.user["id"],),
    )
    return render_template(
        "organization_dashboard.html", jobs=jobs, applications=applications
    )


@app.route("/profile", methods=("GET", "POST"))
@role_required("candidate")
def profile():
    if request.method == "POST":
        db = get_db()
        db.execute(
            """
            UPDATE users SET full_name = ?, bio = ?, skills = ?, access_needs = ?
            WHERE id = ?
            """,
            (
                request.form.get("full_name", "").strip(),
                request.form.get("bio", "").strip(),
                request.form.get("skills", "").strip(),
                request.form.get("access_needs", "").strip(),
                g.user["id"],
            ),
        )
        db.commit()
        flash(translate("profile_saved"), "success")
        return redirect(url_for("profile"))
    return render_template("profile.html")


def read_job_form():
    return {
        "title": request.form.get("title", "").strip(),
        "description": request.form.get("description", "").strip(),
        "work_type": request.form.get("work_type", ""),
        "accessibility": request.form.get("accessibility", "").strip(),
    }


def validate_job_form(form):
    if not form["title"] or not form["description"] or form["work_type"] not in WORK_TYPES:
        return translate("required")
    return None


@app.route("/organization/jobs/new", methods=("GET", "POST"))
@role_required("organization")
def create_job():
    form = read_job_form() if request.method == "POST" else {
        "title": "",
        "description": "",
        "work_type": "full-time",
        "accessibility": "",
    }
    if request.method == "POST":
        error = validate_job_form(form)
        if error:
            flash(error, "error")
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO jobs (organization_id, title, description, work_type, accessibility)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    g.user["id"],
                    form["title"],
                    form["description"],
                    form["work_type"],
                    form["accessibility"],
                ),
            )
            db.commit()
            flash(translate("job_saved"), "success")
            return redirect(url_for("dashboard"))
    return render_template("job_form.html", form=form, editing=False)


@app.route("/organization/jobs/<int:job_id>/edit", methods=("GET", "POST"))
@role_required("organization")
def edit_job(job_id):
    job = query_db(
        "SELECT * FROM jobs WHERE id = ? AND organization_id = ?",
        (job_id, g.user["id"]),
        one=True,
    )
    if job is None:
        abort(404)
    form = read_job_form() if request.method == "POST" else dict(job)
    if request.method == "POST":
        error = validate_job_form(form)
        if error:
            flash(error, "error")
        else:
            db = get_db()
            db.execute(
                """
                UPDATE jobs SET title = ?, description = ?, work_type = ?, accessibility = ?
                WHERE id = ? AND organization_id = ?
                """,
                (
                    form["title"],
                    form["description"],
                    form["work_type"],
                    form["accessibility"],
                    job_id,
                    g.user["id"],
                ),
            )
            db.commit()
            flash(translate("job_updated"), "success")
            return redirect(url_for("dashboard"))
    return render_template("job_form.html", form=form, editing=True)


@app.post("/organization/jobs/<int:job_id>/close")
@role_required("organization")
def close_job(job_id):
    db = get_db()
    result = db.execute(
        "UPDATE jobs SET is_open = 0 WHERE id = ? AND organization_id = ?",
        (job_id, g.user["id"]),
    )
    db.commit()
    if result.rowcount:
        flash(translate("job_closed"), "success")
    else:
        flash(translate("not_authorized"), "error")
    return redirect(url_for("dashboard"))


@app.get("/jobs/<int:job_id>")
def job_detail(job_id):
    job = query_db(
        """
        SELECT jobs.*, users.company_name, users.email AS organization_email
        FROM jobs JOIN users ON users.id = jobs.organization_id
        WHERE jobs.id = ? AND (jobs.is_open = 1 OR jobs.organization_id = ?)
        """,
        (job_id, g.user["id"] if g.user else -1),
        one=True,
    )
    if job is None:
        flash(translate("job_not_found"), "error")
        return redirect(url_for("home"))
    already_applied = False
    if g.user and g.user["role"] == "candidate":
        already_applied = query_db(
            "SELECT id FROM applications WHERE job_id = ? AND candidate_id = ?",
            (job_id, g.user["id"]),
            one=True,
        ) is not None
    return render_template(
        "job_detail.html", job=job, already_applied=already_applied
    )


@app.post("/jobs/<int:job_id>/apply")
@role_required("candidate")
def apply_to_job(job_id):
    job = query_db(
        "SELECT id FROM jobs WHERE id = ? AND is_open = 1", (job_id,), one=True
    )
    if job is None:
        flash(translate("job_not_found"), "error")
        return redirect(url_for("home"))
    try:
        db = get_db()
        db.execute(
            """
            INSERT INTO applications (job_id, candidate_id, cover_note)
            VALUES (?, ?, ?)
            """,
            (job_id, g.user["id"], request.form.get("cover_note", "").strip()),
        )
        db.commit()
        flash(translate("application_sent"), "success")
    except sqlite3.IntegrityError:
        flash(translate("already_applied"), "error")
    return redirect(url_for("job_detail", job_id=job_id))


@app.post("/organization/applications/<int:application_id>/status")
@role_required("organization")
def update_application_status(application_id):
    status = request.form.get("status", "")
    if status not in STATUSES:
        flash(translate("invalid_status"), "error")
        return redirect(url_for("dashboard"))
    db = get_db()
    result = db.execute(
        """
        UPDATE applications SET status = ?
        WHERE id = ? AND job_id IN (
            SELECT id FROM jobs WHERE organization_id = ?
        )
        """,
        (status, application_id, g.user["id"]),
    )
    db.commit()
    if result.rowcount:
        flash(translate("job_updated"), "success")
    else:
        flash(translate("not_authorized"), "error")
    return redirect(url_for("dashboard"))


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/favicon.ico")
def favicon():
    return "", 204


init_db()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
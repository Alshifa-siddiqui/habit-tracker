"""
Vitalis — Premium Habit Tracker
Deep Purple + Gold Theme | Ultra-Modern Desktop UI
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import calendar
from datetime import datetime, date, timedelta

from database import HabitDatabase
from analytics import HabitAnalytics
from medical import (get_medical_insight, get_habit_personality,
                     get_health_score, HEALTH_CONDITIONS, MEDICAL_DISCLAIMER)
from rpg import (get_character_stats, get_current_boss,
                 get_unlocked_gear, get_pet_status, CHARACTERS, PETS,
                 RARITY_COLORS)

P = {
    "bg":          "#0D0D1A",
    "surface":     "#13132B",
    "surface2":    "#1A1A38",
    "surface3":    "#222245",
    "purple":      "#7B2FBE",
    "purple_light":"#9D4EDD",
    "purple_dark": "#4A1A7A",
    "gold":        "#FFD700",
    "gold_dark":   "#B8860B",
    "gold_light":  "#FFE55C",
    "text":        "#F0E6FF",
    "subtext":     "#9B8EC4",
    "danger":      "#FF4757",
    "success":     "#2ED573",
    "warning":     "#FFA502",
    "info":        "#1E90FF",
    "border":      "#2D2D5E",
    "card":        "#16163A",
    "card_hover":  "#1E1E4A",
}

FONT_TITLE = ("Georgia", 22, "bold")
FONT_HEAD  = ("Georgia", 15, "bold")
FONT_SUB   = ("Trebuchet MS", 11, "bold")
FONT_BODY  = ("Trebuchet MS", 10)
FONT_SMALL = ("Trebuchet MS", 9)
FONT_MONO  = ("Courier New", 10)

CATEGORIES = ["General", "Health", "Work", "Personal", "Fitness", "Learning"]
COLORS     = {"Purple":"#9D4EDD","Gold":"#FFD700","Green":"#2ED573",
              "Blue":"#1E90FF","Red":"#FF4757","Teal":"#00CEC9","Pink":"#FD79A8"}

def blend(c1, c2, t):
    def h2r(h):
        h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))
    r1,g1,b1=h2r(c1); r2,g2,b2=h2r(c2)
    return f"#{int(r1+(r2-r1)*t):02x}{int(g1+(g2-g1)*t):02x}{int(b1+(b2-b1)*t):02x}"

class GlowButton(tk.Button):
    def __init__(self, parent, text, command=None, accent=None, **kw):
        accent = accent or P["purple"]
        super().__init__(parent, text=text, command=command,
                         bg=accent, fg=P["text"],
                         activebackground=blend(accent,"#FFFFFF",0.2),
                         activeforeground=P["text"],
                         relief="flat", bd=0, cursor="hand2",
                         font=FONT_SUB, padx=14, pady=7, **kw)
        self.accent=accent
        self.bind("<Enter>", lambda e: self.config(bg=blend(self.accent,"#FFFFFF",0.15)))
        self.bind("<Leave>", lambda e: self.config(bg=self.accent))

class Card(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=P["card"],
                         highlightbackground=P["border"],
                         highlightthickness=1, **kw)

class StatBar(tk.Frame):
    def __init__(self, parent, label, value, max_val=100, color=None):
        super().__init__(parent, bg=P["card"])
        color = color or P["purple_light"]
        tk.Label(self, text=label, bg=P["card"], fg=P["subtext"],
                 font=FONT_SMALL, width=12, anchor="w").pack(side="left")
        bar_bg = tk.Frame(self, bg=P["surface3"], height=8, width=180)
        bar_bg.pack(side="left", padx=6)
        bar_bg.pack_propagate(False)
        pct = min(value/max_val, 1.0)
        if pct > 0:
            tk.Frame(bar_bg, bg=color, height=8,
                     width=int(180*pct)).place(x=0, y=0)
        tk.Label(self, text=str(value), bg=P["card"],
                 fg=P["text"], font=FONT_SMALL, width=4).pack(side="left")

def make_scrollable(parent):
    canvas = tk.Canvas(parent, bg=P["bg"], highlightthickness=0)
    vsb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    inner = tk.Frame(canvas, bg=P["bg"])
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120),"units"))
    return inner

class VitalisApp:
    def __init__(self, root, user_id=1):
        self.root = root
        self.db = HabitDatabase()
        self.analytics = HabitAnalytics(self.db)
        self.user_id = user_id
        self._habits_cache = []
        self.selected_habit = None
        self.selected_char = "warrior"
        self.selected_pet  = "dragon"
        self._reminded = set()  # (habit_id, "YYYY-MM-DD HH:MM") already notified
        self.root.title("Vitalis — Premium Habit Tracker")
        self.root.geometry("1280x800")
        self.root.minsize(1100,700)
        self.root.configure(bg=P["bg"])
        self._setup_styles()
        self._build_ui()
        self._refresh()
        self._start_reminder_loop()

    def _setup_styles(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("Vit.TNotebook", background=P["bg"], borderwidth=0)
        s.configure("Vit.TNotebook.Tab", background=P["surface"],
                    foreground=P["subtext"], padding=[18,8], font=FONT_SUB, borderwidth=0)
        s.map("Vit.TNotebook.Tab",
              background=[("selected",P["purple_dark"])],
              foreground=[("selected",P["gold"])])
        s.configure("Gold.Horizontal.TProgressbar",
                    troughcolor=P["surface3"], background=P["gold"], borderwidth=0, thickness=10)
        s.configure("Purple.Horizontal.TProgressbar",
                    troughcolor=P["surface3"], background=P["purple_light"], borderwidth=0, thickness=8)

    def _build_ui(self):
        self._build_header()
        main = tk.Frame(self.root, bg=P["bg"])
        main.pack(fill="both", expand=True)
        self._build_sidebar(main)
        content = tk.Frame(main, bg=P["bg"])
        content.pack(side="left", fill="both", expand=True)
        self._build_notebook(content)

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=P["surface"], height=64)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        logo = tk.Frame(hdr, bg=P["surface"])
        logo.pack(side="left", padx=24, pady=10)
        tk.Label(logo, text="✦", bg=P["surface"], fg=P["gold"], font=("Georgia",20)).pack(side="left")
        tk.Label(logo, text=" VITALIS", bg=P["surface"], fg=P["text"], font=("Georgia",18,"bold")).pack(side="left")
        self.hdr_user_lbl = tk.Label(hdr, text="", bg=P["surface"], fg=P["subtext"], font=FONT_BODY)
        self.hdr_user_lbl.pack(side="left", padx=30)
        self.hdr_score_lbl = tk.Label(hdr, text="", bg=P["surface"], fg=P["gold"], font=FONT_SUB)
        self.hdr_score_lbl.pack(side="left", padx=10)
        GlowButton(hdr, "👤 Profiles", self._switch_profile_dialog,
                   accent=P["purple_dark"]).pack(side="right", padx=16, pady=14)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=P["surface"], width=260)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        self.dc_card = Card(sb)
        self.dc_card.pack(fill="x", padx=12, pady=(14,6))
        tk.Label(self.dc_card, text="🎯 Today's Challenge", bg=P["card"],
                 fg=P["gold"], font=FONT_SUB).pack(anchor="w", padx=12, pady=(10,4))
        self.dc_label = tk.Label(self.dc_card, text="No challenge set", bg=P["card"],
                                  fg=P["subtext"], font=FONT_BODY, wraplength=210, justify="left")
        self.dc_label.pack(anchor="w", padx=12, pady=(0,10))
        pet_card = Card(sb); pet_card.pack(fill="x", padx=12, pady=6)
        self.pet_emoji_lbl = tk.Label(pet_card, text="🐲", bg=P["card"], font=("Arial",28))
        self.pet_emoji_lbl.pack(pady=(10,4))
        self.pet_name_lbl = tk.Label(pet_card, text="Ember", bg=P["card"], fg=P["text"], font=FONT_SUB)
        self.pet_name_lbl.pack()
        self.pet_mood_lbl = tk.Label(pet_card, text="", bg=P["card"], fg=P["subtext"], font=FONT_SMALL)
        self.pet_mood_lbl.pack(pady=(2,10))
        tk.Label(sb, text="YOUR HABITS", bg=P["surface"], fg=P["subtext"],
                 font=("Trebuchet MS",8,"bold")).pack(anchor="w", padx=14, pady=(14,4))
        lf = tk.Frame(sb, bg=P["surface"])
        lf.pack(fill="both", expand=True, padx=8)
        vsb = ttk.Scrollbar(lf)
        self.habit_lb = tk.Listbox(lf, font=FONT_BODY, bg=P["surface"], fg=P["text"],
                                    selectbackground=P["purple_dark"], selectforeground=P["gold"],
                                    activestyle="none", bd=0, highlightthickness=0, cursor="hand2",
                                    yscrollcommand=vsb.set)
        vsb.config(command=self.habit_lb.yview)
        vsb.pack(side="right", fill="y"); self.habit_lb.pack(fill="both", expand=True)
        self.habit_lb.bind("<<ListboxSelect>>", self._on_habit_select)
        GlowButton(sb, "➕  Add Habit", self._add_dialog, accent=P["purple"]).pack(fill="x", padx=12, pady=10)

    def _build_notebook(self, parent):
        self.nb = ttk.Notebook(parent, style="Vit.TNotebook")
        self.nb.pack(fill="both", expand=True, padx=8, pady=6)
        self.tab_home     = tk.Frame(self.nb, bg=P["bg"])
        self.tab_detail   = tk.Frame(self.nb, bg=P["bg"])
        self.tab_rpg      = tk.Frame(self.nb, bg=P["bg"])
        self.tab_medical  = tk.Frame(self.nb, bg=P["bg"])
        self.tab_calendar = tk.Frame(self.nb, bg=P["bg"])
        self.tab_stats    = tk.Frame(self.nb, bg=P["bg"])
        self.tab_badges   = tk.Frame(self.nb, bg=P["bg"])
        self.nb.add(self.tab_home,     text="🏠  Home")
        self.nb.add(self.tab_detail,   text="📋  Detail")
        self.nb.add(self.tab_rpg,      text="⚔️  RPG")
        self.nb.add(self.tab_medical,  text="🏥  Health")
        self.nb.add(self.tab_calendar, text="📅  Calendar")
        self.nb.add(self.tab_stats,    text="📊  Analytics")
        self.nb.add(self.tab_badges,   text="🏅  Badges")
        self._build_stats_tab()
        self._build_calendar_tab()
        # Lazy refresh: each dynamic tab is rebuilt only when it is the visible
        # tab, instead of rebuilding all tabs on every action.
        self._tab_refreshers = {
            self.tab_home:    self._refresh_home,
            self.tab_detail:  self._refresh_detail,
            self.tab_rpg:     self._refresh_rpg,
            self.tab_medical: self._refresh_medical,
            self.tab_badges:  self._refresh_badges,
        }
        self._dirty = set()
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _current_tab(self):
        try:
            return self.nb.nametowidget(self.nb.select())
        except Exception:
            return None

    def _refresh_current_tab(self):
        """Rebuild the visible tab only if its data is marked stale."""
        tab = self._current_tab()
        fn = self._tab_refreshers.get(tab)
        if fn and tab in self._dirty:
            fn()
            self._dirty.discard(tab)

    def _on_tab_changed(self, event=None):
        self._refresh_current_tab()

    # HOME
    def _refresh_home(self):
        for w in self.tab_home.winfo_children(): w.destroy()
        parent = make_scrollable(self.tab_home)
        habits = self._habits_cache
        user = self.db.get_user_by_id(self.user_id)
        if not user: return
        personality = get_habit_personality(habits)
        banner = tk.Frame(parent, bg=P["surface2"])
        banner.pack(fill="x", padx=16, pady=(14,8))
        tk.Label(banner, text=f"{personality['emoji']}  {personality['type']}",
                 bg=P["surface2"], fg=P["gold"], font=("Georgia",16,"bold")).pack(anchor="w", padx=20, pady=(14,4))
        tk.Label(banner, text=personality["description"], bg=P["surface2"],
                 fg=P["subtext"], font=FONT_BODY).pack(anchor="w", padx=20, pady=(0,14))
        row = tk.Frame(parent, bg=P["bg"]); row.pack(fill="x", padx=16, pady=6)
        hs = get_health_score(habits)
        for label,val,color in [
            ("⭐ Level",str(user["level"]),P["gold"]),
            ("⚡ XP",str(user["xp"]),P["purple_light"]),
            ("🔥 Habits",str(len(habits)),P["success"]),
            ("🏅 Badges",str(len(self.db.get_badges(self.user_id))),P["warning"]),
            ("💚 Health",f"{hs['score']}/100",hs["color"]),
        ]:
            c=Card(row); c.pack(side="left",expand=True,fill="x",padx=5)
            tk.Label(c,text=val,bg=P["card"],fg=color,font=("Georgia",22,"bold")).pack(pady=(12,2))
            tk.Label(c,text=label,bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(pady=(0,10))
        tk.Label(parent,text="YOUR HABITS",bg=P["bg"],fg=P["subtext"],
                 font=("Trebuchet MS",8,"bold")).pack(anchor="w",padx=20,pady=(16,4))
        grid = tk.Frame(parent, bg=P["bg"]); grid.pack(fill="x", padx=16, pady=4)
        if not habits:
            tk.Label(grid,text="No habits yet. Add one! ✨",bg=P["bg"],fg=P["subtext"],font=FONT_BODY).pack(pady=20)
            return
        for i,h in enumerate(habits):
            self._habit_mini_card(grid, h, i//3, i%3)

    def _habit_mini_card(self, parent, habit, row, col):
        color = habit.get("color", P["purple_light"])
        card = tk.Frame(parent, bg=P["card"], highlightbackground=color,
                        highlightthickness=1, cursor="hand2")
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        parent.columnconfigure(col, weight=1)
        tk.Frame(card, bg=color, height=4).pack(fill="x")
        body = tk.Frame(card, bg=P["card"]); body.pack(fill="x", padx=12, pady=10)
        nr = tk.Frame(body, bg=P["card"]); nr.pack(fill="x")
        tk.Label(nr,text=habit["name"],bg=P["card"],fg=P["text"],font=FONT_SUB,anchor="w").pack(side="left")
        if habit["current_streak"]>0:
            tk.Label(nr,text=f"🔥{habit['current_streak']}",bg=P["card"],fg=P["warning"],font=FONT_SMALL).pack(side="right")
        tk.Label(body,text=f"{habit['category']} · {habit['frequency']}",bg=P["card"],
                 fg=P["subtext"],font=FONT_SMALL,anchor="w").pack(fill="x",pady=2)
        goal=max(habit.get("goal_target",30),1); pct=min(habit["completed_count"]/goal,1.0)
        bar_bg=tk.Frame(body,bg=P["surface3"],height=6); bar_bg.pack(fill="x",pady=4)
        bar_bg.update_idletasks()
        if pct>0: tk.Frame(bar_bg,bg=color,height=6,width=int(180*pct)).place(x=0,y=0)
        tk.Label(body,text=f"{habit['completed_count']}/{goal} done",bg=P["card"],
                 fg=P["subtext"],font=FONT_SMALL,anchor="w").pack(fill="x")
        GlowButton(card,"✓ Check In",lambda h=habit: self._quick_checkin(h),accent=color).pack(fill="x",padx=12,pady=(4,10))
        card.bind("<Button-1>", lambda e,h=habit: self._open_detail(h))

    def _quick_checkin(self, habit):
        try:
            xp, new_badges = self.db.check_habit(habit["id"], user_id=self.user_id)
            self._refresh()
            popup=tk.Toplevel(self.root); popup.overrideredirect(True)
            popup.configure(bg=P["surface2"])
            popup.geometry(f"220x90+{self.root.winfo_x()+530}+{self.root.winfo_y()+30}")
            tk.Label(popup,text=f"⚡ +{xp} XP",bg=P["surface2"],fg=P["gold"],font=("Georgia",20,"bold")).pack(pady=10)
            tk.Label(popup,text="Habit completed! 🎉",bg=P["surface2"],fg=P["text"],font=FONT_BODY).pack()
            popup.after(2000, popup.destroy)
            if new_badges:
                messagebox.showinfo("🏅 New Badge!", "\n".join(new_badges), parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    # DETAIL
    def _open_detail(self, habit):
        self.selected_habit = habit
        self._dirty.add(self.tab_detail)
        self.nb.select(self.tab_detail)
        self._refresh_current_tab()  # handles the case where Detail is already open

    def _refresh_detail(self):
        for w in self.tab_detail.winfo_children(): w.destroy()
        if not self.selected_habit:
            tk.Label(self.tab_detail,text="← Select a habit",bg=P["bg"],fg=P["subtext"],font=FONT_HEAD).pack(expand=True)
            return
        h = self.db.get_habit_by_id(self.selected_habit["id"]) or self.selected_habit
        self.selected_habit = h
        color = h.get("color", P["purple_light"])
        parent = make_scrollable(self.tab_detail)
        tk.Frame(parent,bg=color,height=8).pack(fill="x")
        hdr=tk.Frame(parent,bg=color); hdr.pack(fill="x")
        tk.Label(hdr,text=h["name"],bg=color,fg="white",font=("Georgia",20,"bold")).pack(side="left",padx=20,pady=14)
        tk.Label(hdr,text=h["category"],bg=P["surface"],fg=P["gold"],font=FONT_SMALL,padx=8,pady=3).pack(side="left",padx=8)
        bb=tk.Frame(parent,bg=P["bg"]); bb.pack(fill="x",padx=16,pady=10)
        for text,cmd,acc in [
            ("✅ Check In",lambda: self._checkin_dialog(h),P["success"]),
            ("✏️ Edit",lambda: self._edit_dialog(h),P["purple"]),
            ("🧊 Freeze",lambda: self._use_freeze(h),P["info"]),
            ("📈 Plot",lambda: self.analytics.plot_habit_progress(h["id"]),P["purple_dark"]),
            ("🌡️ Heatmap",lambda: self.analytics.plot_heatmap(h["id"]),P["purple_dark"]),
            ("🎯 Challenge",lambda: self._set_challenge(h),P["gold_dark"]),
            ("🔔 Test",lambda: self._fire_reminder(h),P["info"]),
        ]:
            GlowButton(bb,text,cmd,accent=acc).pack(side="left",padx=4)
        GlowButton(bb,"🗑 Delete",lambda: self._delete(h),accent=P["danger"]).pack(side="right",padx=4)
        GlowButton(bb,"🗃 Archive",lambda: self._archive(h),accent=P["surface3"]).pack(side="right",padx=4)
        sr=tk.Frame(parent,bg=P["bg"]); sr.pack(fill="x",padx=16,pady=6)
        for label,val,col in [
            ("Check-ins",str(h["completed_count"]),P["gold"]),
            ("🔥 Streak",str(h["current_streak"]),P["warning"]),
            ("Best Streak",f"{h['longest_streak']}d",P["success"]),
            ("Freezes",f"🧊{h['streak_freeze']}",P["info"]),
            ("Goal",str(h["goal_target"]),P["purple_light"]),
            ("Difficulty","⭐"*h["difficulty"],P["gold"]),
        ]:
            c=Card(sr); c.pack(side="left",expand=True,fill="x",padx=4)
            tk.Label(c,text=val,bg=P["card"],fg=col,font=("Georgia",16,"bold")).pack(pady=(10,2))
            tk.Label(c,text=label,bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(pady=(0,8))
        pc=Card(parent); pc.pack(fill="x",padx=16,pady=6)
        weekly=self.analytics.get_completion_rate(h["id"],"weekly")
        monthly=self.analytics.get_completion_rate(h["id"],"monthly")
        best_day=self.analytics.get_best_day_of_week(h["id"])
        for label,val in [("Weekly Rate",weekly),("Monthly Rate",monthly)]:
            r=tk.Frame(pc,bg=P["card"]); r.pack(fill="x",padx=16,pady=6)
            tk.Label(r,text=f"{label}: {val}%",bg=P["card"],fg=P["subtext"],font=FONT_BODY).pack(anchor="w")
            ttk.Progressbar(r,value=val,maximum=100,length=400,style="Purple.Horizontal.TProgressbar").pack(anchor="w",pady=2)
        tk.Label(pc,text=f"📅 Best Day: {best_day}",bg=P["card"],fg=P["text"],font=FONT_BODY).pack(anchor="w",padx=16,pady=(0,12))
        rate=min(h["completed_count"],100)
        insight=get_medical_insight(h["name"],rate)
        if insight:
            mc=Card(parent); mc.pack(fill="x",padx=16,pady=6)
            tk.Label(mc,text="🏥 Medical Insight",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
            tk.Label(mc,text=f"Status: {insight['status']}",bg=P["card"],fg=insight["status_color"],font=FONT_SUB).pack(anchor="w",padx=16)
            tk.Label(mc,text=insight["headline"],bg=P["card"],fg=P["text"],font=FONT_BODY,wraplength=700,justify="left").pack(anchor="w",padx=16,pady=6)
            for b in insight.get("benefits",[]):
                tk.Label(mc,text=f"  ✅ {b}",bg=P["card"],fg=P["success"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=1)
            for r in insight.get("risks",[]):
                tk.Label(mc,text=f"  {r}",bg=P["card"],fg=P["warning"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=1)
            tk.Label(mc,text="",bg=P["card"]).pack(pady=4)
        hc=Card(parent); hc.pack(fill="x",padx=16,pady=6)
        tk.Label(hc,text="📜 Recent Check-ins",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
        history=self.db.get_habit_history(h["id"])
        if history:
            for entry in reversed(history[-8:]):
                r=tk.Frame(hc,bg=P["card"]); r.pack(fill="x",padx=16,pady=2)
                tk.Label(r,text=f"✦ {entry[3]}",bg=P["card"],fg=P["subtext"],font=FONT_SMALL,width=14,anchor="w").pack(side="left")
                note=entry[4] if len(entry)>4 and entry[4] else "—"
                tk.Label(r,text=note,bg=P["card"],fg=P["text"],font=FONT_SMALL).pack(side="left",padx=8)
        else:
            tk.Label(hc,text="No check-ins yet.",bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=6)
        tk.Label(hc,text="",bg=P["card"]).pack(pady=4)

    # RPG
    def _refresh_rpg(self):
        for w in self.tab_rpg.winfo_children(): w.destroy()
        parent = make_scrollable(self.tab_rpg)
        habits = self._habits_cache
        user = self.db.get_user_by_id(self.user_id)
        cd = get_character_stats(habits, self.selected_char, user)
        char = cd["character"]
        ch_f=tk.Frame(parent,bg=P["surface2"]); ch_f.pack(fill="x",padx=16,pady=(14,8))
        tk.Label(ch_f,text=char["emoji"],bg=P["surface2"],font=("Arial",40)).pack(side="left",padx=20,pady=14)
        info=tk.Frame(ch_f,bg=P["surface2"]); info.pack(side="left",pady=14)
        tk.Label(info,text=char["name"],bg=P["surface2"],fg=P["gold"],font=("Georgia",18,"bold")).pack(anchor="w")
        tk.Label(info,text=f"Level {cd['level']}  ·  {char['description']}",bg=P["surface2"],fg=P["subtext"],font=FONT_BODY).pack(anchor="w")
        xf=tk.Frame(info,bg=P["surface2"]); xf.pack(anchor="w",pady=6)
        tk.Label(xf,text=f"XP: {cd['xp_in_level']}/{cd['xp_to_next']}",bg=P["surface2"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w")
        ttk.Progressbar(xf,value=cd['xp_in_level'],maximum=max(cd['xp_to_next'],1),length=300,style="Gold.Horizontal.TProgressbar").pack(anchor="w",pady=2)
        hp_r=tk.Frame(ch_f,bg=P["surface2"]); hp_r.pack(side="right",padx=20,pady=14)
        for label,val,mv,col in [("❤️ HP",cd["hp"],cd["max_hp"],P["danger"]),("💙 MP",cd["mp"],cd["max_mp"],P["info"])]:
            r=tk.Frame(hp_r,bg=P["surface2"]); r.pack(anchor="w",pady=3)
            tk.Label(r,text=f"{label} {val}/{mv}",bg=P["surface2"],fg=col,font=FONT_BODY).pack(anchor="w")
            ttk.Progressbar(r,value=val,maximum=max(mv,1),length=180,style="Purple.Horizontal.TProgressbar").pack(anchor="w")
        cp=tk.Frame(parent,bg=P["bg"]); cp.pack(fill="x",padx=16,pady=6)
        tk.Label(cp,text="Character:",bg=P["bg"],fg=P["subtext"],font=FONT_BODY).pack(side="left",padx=8)
        for c in CHARACTERS:
            GlowButton(cp,f"{c['emoji']} {c['name']}",lambda cid=c["id"]: self._pick_char(cid),
                       accent=c["color"] if self.selected_char==c["id"] else P["surface3"]).pack(side="left",padx=4)
        sc=Card(parent); sc.pack(fill="x",padx=16,pady=8)
        tk.Label(sc,text="⚡ Stats",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,6))
        for stat,val in cd["stats"].items():
            StatBar(sc,stat,val).pack(anchor="w",padx=20,pady=3)
        tk.Label(sc,text="",bg=P["card"]).pack(pady=4)
        boss=get_current_boss(habits)
        bc=Card(parent); bc.pack(fill="x",padx=16,pady=8)
        tk.Label(bc,text="👹 Boss Fight",bg=P["card"],fg=P["danger"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
        br=tk.Frame(bc,bg=P["card"]); br.pack(fill="x",padx=16,pady=6)
        tk.Label(br,text=boss["emoji"],bg=P["card"],font=("Arial",36)).pack(side="left",padx=10)
        bi=tk.Frame(br,bg=P["card"]); bi.pack(side="left")
        tk.Label(bi,text=boss["name"],bg=P["card"],fg=P["danger"],font=FONT_SUB).pack(anchor="w")
        tk.Label(bi,text=boss["description"],bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w")
        tk.Label(bi,text=f"Weakness: {boss['weakness'].title()}  |  Reward: {boss['reward']}",
                 bg=P["card"],fg=P["gold"],font=FONT_SMALL).pack(anchor="w")
        bh=tk.Frame(bc,bg=P["card"]); bh.pack(fill="x",padx=16,pady=(0,12))
        tk.Label(bh,text=f"HP: {boss['current_hp']}/{boss['hp']}",bg=P["card"],fg=P["danger"],font=FONT_SMALL).pack(anchor="w")
        ttk.Progressbar(bh,value=boss["current_hp"],maximum=max(boss["hp"],1),length=400,style="Purple.Horizontal.TProgressbar").pack(anchor="w",pady=3)
        tk.Label(bh,text=f"Complete habits to deal damage! ({boss['progress_pct']}% done)",
                 bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w")
        pd=get_pet_status(habits,self.selected_pet)
        petc=Card(parent); petc.pack(fill="x",padx=16,pady=8)
        tk.Label(petc,text="🐾 Companion",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
        pr=tk.Frame(petc,bg=P["card"]); pr.pack(fill="x",padx=16,pady=6)
        tk.Label(pr,text=pd["emoji"],bg=P["card"],font=("Arial",40)).pack(side="left",padx=10)
        pi=tk.Frame(pr,bg=P["card"]); pi.pack(side="left")
        tk.Label(pi,text=f"{pd['pet']['name']} the {pd['pet']['type']}",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w")
        tk.Label(pi,text=f"Level {pd['level']}  ·  {pd['mood']}",bg=P["card"],fg=P["subtext"],font=FONT_BODY).pack(anchor="w")
        StatBar(pi,"Happiness",pd["happiness"],color=P["success"]).pack(anchor="w",pady=4)
        if pd["evolved"]: tk.Label(pi,text="✨ EVOLVED!",bg=P["card"],fg=P["gold"],font=("Georgia",11,"bold")).pack(anchor="w")
        pp=tk.Frame(petc,bg=P["card"]); pp.pack(fill="x",padx=16,pady=(4,12))
        tk.Label(pp,text="Switch:",bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(side="left")
        for p in PETS:
            GlowButton(pp,p["emoji"],lambda pid=p["id"]: self._pick_pet(pid),
                       accent=P["purple"] if self.selected_pet==p["id"] else P["surface3"]).pack(side="left",padx=2)
        gear=get_unlocked_gear(habits)
        gc=Card(parent); gc.pack(fill="x",padx=16,pady=8)
        tk.Label(gc,text="🎒 Gear",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
        if not gear:
            tk.Label(gc,text="Complete more habits to unlock gear!",bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w",padx=20,pady=(0,12))
        else:
            gr=tk.Frame(gc,bg=P["card"]); gr.pack(fill="x",padx=16,pady=(0,12))
            for g in gear:
                gcard=tk.Frame(gr,bg=P["surface2"],highlightbackground=RARITY_COLORS[g["rarity"]],highlightthickness=1)
                gcard.pack(side="left",padx=6,pady=4)
                tk.Label(gcard,text=g["emoji"],bg=P["surface2"],font=("Arial",20)).pack(pady=(8,2))
                tk.Label(gcard,text=g["name"],bg=P["surface2"],fg=RARITY_COLORS[g["rarity"]],font=FONT_SMALL,wraplength=100,justify="center").pack(padx=8)
                tk.Label(gcard,text=g["bonus"],bg=P["surface2"],fg=P["gold"],font=FONT_SMALL).pack(pady=(2,4))
                tk.Label(gcard,text=g["rarity"],bg=P["surface2"],fg=RARITY_COLORS[g["rarity"]],font=FONT_SMALL).pack(pady=(0,8))

    def _pick_char(self,cid): self.selected_char=cid; self._refresh_rpg()
    def _pick_pet(self,pid): self.selected_pet=pid; self._refresh_rpg()

    # MEDICAL
    def _refresh_medical(self):
        for w in self.tab_medical.winfo_children(): w.destroy()
        parent = make_scrollable(self.tab_medical)
        habits = self._habits_cache
        pc=Card(parent); pc.pack(fill="x",padx=16,pady=(14,8))
        tk.Label(pc,text="🏥 Health Insights",bg=P["card"],fg=P["gold"],font=FONT_SUB).pack(anchor="w",padx=16,pady=(12,4))
        tk.Label(pc,text=MEDICAL_DISCLAIMER,bg=P["card"],fg=P["subtext"],font=FONT_SMALL,
                 wraplength=700,justify="left").pack(anchor="w",padx=16,pady=(0,6))
        GlowButton(pc,"⚙️ Update Health Profile",self._health_profile_dialog,accent=P["purple"]).pack(anchor="w",padx=16,pady=(0,12))
        hs=get_health_score(habits)
        sc=Card(parent); sc.pack(fill="x",padx=16,pady=8)
        sr=tk.Frame(sc,bg=P["card"]); sr.pack(fill="x",padx=16,pady=14)
        tk.Label(sr,text=str(hs["score"]),bg=P["card"],fg=hs["color"],font=("Georgia",52,"bold")).pack(side="left")
        si=tk.Frame(sr,bg=P["card"]); si.pack(side="left",padx=20)
        tk.Label(si,text="Health Score",bg=P["card"],fg=P["subtext"],font=FONT_BODY).pack(anchor="w")
        tk.Label(si,text=f"Grade: {hs['grade']}",bg=P["card"],fg=hs["color"],font=("Georgia",22,"bold")).pack(anchor="w")
        tk.Label(si,text="Based on your habits vs. WHO guidelines",bg=P["card"],fg=P["subtext"],font=FONT_SMALL).pack(anchor="w")
        if not habits:
            tk.Label(parent,text="Add habits to see health insights",bg=P["bg"],fg=P["subtext"],font=FONT_BODY).pack(pady=20); return
        for habit in habits:
            insight=get_medical_insight(habit["name"],min(habit["completed_count"],100))
            if not insight: continue
            ic=Card(parent); ic.pack(fill="x",padx=16,pady=6)
            ir=tk.Frame(ic,bg=P["card"]); ir.pack(fill="x",padx=16,pady=(12,4))
            tk.Label(ir,text=habit["name"],bg=P["card"],fg=P["text"],font=FONT_SUB).pack(side="left")
            tk.Label(ir,text=insight["status"],bg=P["card"],fg=insight["status_color"],font=("Trebuchet MS",9,"bold")).pack(side="right")
            tk.Label(ic,text=insight["headline"],bg=P["card"],fg=P["text"],font=FONT_BODY,wraplength=700,justify="left").pack(anchor="w",padx=16,pady=4)
            for b in insight.get("benefits",[]): tk.Label(ic,text=f"  ✅ {b}",bg=P["card"],fg=P["success"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=1)
            for r in insight.get("risks",[]): tk.Label(ic,text=f"  {r}",bg=P["card"],fg=P["warning"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=1)
            for cw in insight.get("condition_warnings",[]): tk.Label(ic,text=f"  {cw}",bg=P["card"],fg=P["danger"],font=FONT_SMALL).pack(anchor="w",padx=16,pady=1)
            tk.Label(ic,text="",bg=P["card"]).pack(pady=3)

    def _health_profile_dialog(self):
        win=tk.Toplevel(self.root); win.title("Health Profile"); win.configure(bg=P["surface"]); win.geometry("440x500"); win.grab_set()
        tk.Label(win,text="🏥 Your Health Conditions",bg=P["surface"],fg=P["gold"],font=FONT_HEAD).pack(pady=(16,4),padx=20,anchor="w")
        tk.Label(win,text="Select all that apply for personalized insights.",bg=P["surface"],fg=P["subtext"],font=FONT_SMALL).pack(padx=20,anchor="w",pady=(0,10))
        vars_map={}; f=tk.Frame(win,bg=P["surface"]); f.pack(fill="both",expand=True,padx=20)
        for cond in HEALTH_CONDITIONS:
            v=tk.BooleanVar(); vars_map[cond]=v
            tk.Checkbutton(f,text=cond,variable=v,bg=P["surface"],fg=P["text"],selectcolor=P["surface2"],activebackground=P["surface"],font=FONT_BODY).pack(anchor="w",pady=2)
        def save():
            selected=[c for c,v in vars_map.items() if v.get()]
            messagebox.showinfo("Saved",f"Profile updated!\nConditions: {', '.join(selected) or 'None'}",parent=win)
            win.destroy(); self._refresh_medical()
        GlowButton(win,"💾 Save",save,accent=P["purple"]).pack(pady=16)

    # CALENDAR
    def _build_calendar_tab(self):
        tab=self.tab_calendar
        ctrl=tk.Frame(tab,bg=P["bg"]); ctrl.pack(fill="x",padx=16,pady=10)
        tk.Label(ctrl,text="Habit:",bg=P["bg"],fg=P["subtext"],font=FONT_BODY).pack(side="left")
        self.cal_var=tk.StringVar()
        self.cal_combo=ttk.Combobox(ctrl,textvariable=self.cal_var,state="readonly",width=24,font=FONT_BODY)
        self.cal_combo.pack(side="left",padx=8)
        self.cal_combo.bind("<<ComboboxSelected>>",lambda e: self._draw_calendar())
        self.cal_month=date.today().replace(day=1)
        GlowButton(ctrl,"◀",self._cal_prev,accent=P["purple_dark"]).pack(side="left",padx=2)
        self.cal_month_lbl=tk.Label(ctrl,text="",bg=P["bg"],fg=P["gold"],font=FONT_SUB,width=16)
        self.cal_month_lbl.pack(side="left")
        GlowButton(ctrl,"▶",self._cal_next,accent=P["purple_dark"]).pack(side="left",padx=2)
        self.cal_grid=tk.Frame(tab,bg=P["bg"]); self.cal_grid.pack(fill="both",expand=True,padx=20,pady=10)

    def _cal_prev(self):
        m=self.cal_month
        self.cal_month=m.replace(month=m.month-1) if m.month>1 else m.replace(year=m.year-1,month=12)
        self._draw_calendar()

    def _cal_next(self):
        m=self.cal_month
        self.cal_month=m.replace(month=m.month+1) if m.month<12 else m.replace(year=m.year+1,month=1)
        self._draw_calendar()

    def _draw_calendar(self):
        for w in self.cal_grid.winfo_children(): w.destroy()
        habits=self._habits_cache; name=self.cal_var.get()
        habit=next((h for h in habits if h["name"]==name),None)
        if not habit: return
        m=self.cal_month; self.cal_month_lbl.config(text=m.strftime("%B %Y"))
        color=habit.get("color",P["purple_light"])
        done=set(self.db.get_history_dates(habit["id"]))
        for col,d in enumerate(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
            tk.Label(self.cal_grid,text=d,bg=P["bg"],fg=P["gold"],font=("Trebuchet MS",9,"bold"),width=6).grid(row=0,column=col,padx=3,pady=3)
        for row,week in enumerate(calendar.monthcalendar(m.year,m.month),1):
            for col,day in enumerate(week):
                if day==0: tk.Label(self.cal_grid,text="",bg=P["bg"],width=6).grid(row=row,column=col,padx=3,pady=3); continue
                d_obj=date(m.year,m.month,day); is_done=str(d_obj) in done; is_today=d_obj==date.today()
                bg=color if is_done else P["surface2"]; fg="white" if is_done else P["subtext"]
                border=P["gold"] if is_today else (color if is_done else P["border"])
                tk.Label(self.cal_grid,text=str(day),bg=bg,fg=fg,
                         font=("Trebuchet MS",11,"bold" if is_today else "normal"),width=5,height=2,
                         highlightbackground=border,highlightthickness=2 if is_today else 1).grid(row=row,column=col,padx=3,pady=3)

    # STATS
    def _build_stats_tab(self):
        tab=self.tab_stats
        bb=tk.Frame(tab,bg=P["bg"]); bb.pack(fill="x",padx=16,pady=10)
        for text,cmd,acc in [
            ("📊 Report",self._show_report,P["purple"]),
            ("⚔️ Compare",self._compare_dialog,P["purple_dark"]),
            ("📤 Export",self._export_csv,P["info"]),
            ("📥 Import",self._import_csv,P["info"]),
            ("💾 Backup",self._backup,P["surface3"]),
            ("🔄 Restore",self._restore,P["surface3"]),
        ]:
            GlowButton(bb,text,cmd,accent=acc).pack(side="left",padx=4)
        self.report_text=tk.Text(tab,font=FONT_MONO,bg=P["surface"],fg=P["text"],relief="flat",padx=16,pady=10,
                                  insertbackground=P["gold"],selectbackground=P["purple_dark"],state="disabled")
        self.report_text.pack(fill="both",expand=True,padx=16,pady=6)

    def _show_report(self):
        report=self.analytics.generate_report(self.user_id)
        self.report_text.config(state="normal"); self.report_text.delete("1.0","end")
        self.report_text.insert("end",report); self.report_text.config(state="disabled")
        self.nb.select(self.tab_stats)

    def _compare_dialog(self):
        habits=self._habits_cache
        if len(habits)<2: messagebox.showinfo("Compare","Need at least 2 habits.",parent=self.root); return
        names=[h["name"] for h in habits]
        win=tk.Toplevel(self.root); win.title("Compare"); win.configure(bg=P["surface"]); win.geometry("380x200"); win.grab_set()
        for i,(label,attr) in enumerate([("Habit 1:","v1"),("Habit 2:","v2")]):
            tk.Label(win,text=label,bg=P["surface"],fg=P["text"],font=FONT_BODY).grid(row=i,column=0,padx=16,pady=10,sticky="w")
            v=ttk.Combobox(win,values=names,state="readonly",width=24); v.grid(row=i,column=1,padx=10); setattr(win,attr,v)
        def do():
            h1=next((h for h in habits if h["name"]==win.v1.get()),None)
            h2=next((h for h in habits if h["name"]==win.v2.get()),None)
            if not h1 or not h2: messagebox.showerror("Error","Select both.",parent=win); return
            win.destroy()
            data=self.analytics.compare_habits(h1["id"],h2["id"])
            if data:
                txt="⚔️  COMPARISON\n"+"═"*44+"\n\n"
                for hname,stats in data.items():
                    txt+=f"✦ {hname}\n"
                    for k,v in stats.items(): txt+=f"   {k:<24}: {v}\n"
                    txt+="\n"
                self.report_text.config(state="normal"); self.report_text.delete("1.0","end")
                self.report_text.insert("end",txt); self.report_text.config(state="disabled")
                self.nb.select(self.tab_stats); self.analytics.plot_comparison(h1["id"],h2["id"])
        GlowButton(win,"⚔️ Compare",do,accent=P["purple"]).grid(row=2,column=0,columnspan=2,pady=16)

    # BADGES
    def _refresh_badges(self):
        for w in self.tab_badges.winfo_children(): w.destroy()
        tab=self.tab_badges
        tk.Label(tab,text="🏅 Badges",bg=P["bg"],fg=P["gold"],font=FONT_HEAD).pack(pady=(14,6),anchor="w",padx=20)
        badges=self.db.get_badges(self.user_id)
        if not badges: tk.Label(tab,text="No badges yet — keep going!",bg=P["bg"],fg=P["subtext"],font=FONT_BODY).pack(pady=30); return
        grid=tk.Frame(tab,bg=P["bg"]); grid.pack(fill="both",expand=True,padx=16,pady=8)
        for i,(badge,earned_at) in enumerate(badges):
            card=tk.Frame(grid,bg=P["surface2"],highlightbackground=P["gold"],highlightthickness=1)
            card.grid(row=i//4,column=i%4,padx=10,pady=10,sticky="nsew"); grid.columnconfigure(i%4,weight=1)
            tk.Label(card,text=badge,font=("Trebuchet MS",13),bg=P["surface2"],fg=P["gold"],wraplength=150,justify="center").pack(padx=16,pady=(14,4))
            tk.Label(card,text=earned_at[:10],font=FONT_SMALL,bg=P["surface2"],fg=P["subtext"]).pack(pady=(0,12))

    # ACTIONS
    def _checkin_dialog(self, habit):
        note=simpledialog.askstring("Note",f"Note for '{habit['name']}' (optional):",parent=self.root)
        try:
            xp,new_badges=self.db.check_habit(habit["id"],note=note,user_id=self.user_id)
            msg=f"✅ +{xp} XP"
            if new_badges: msg+="\n\n🏅 New Badges:\n"+"\n".join(new_badges)
            messagebox.showinfo("Done!",msg,parent=self.root)
            ch=self.db.get_daily_challenge(self.user_id)
            if ch and ch["habit_id"]==habit["id"] and not ch["completed"]:
                self.db.complete_daily_challenge(self.user_id); self.db.add_xp(self.user_id,20)
                messagebox.showinfo("🎯","Daily challenge done! +20 Bonus XP",parent=self.root)
            self._refresh()
        except Exception as e: messagebox.showerror("Error",str(e),parent=self.root)

    def _use_freeze(self,habit):
        h=self.db.get_habit_by_id(habit["id"])
        if h and h["streak_freeze"]<=0:
            if messagebox.askyesno("No Freezes","You have no freezes. Add one?",parent=self.root):
                self.db.add_streak_freeze(habit["id"]); messagebox.showinfo("Done","Freeze added! ✅")
        elif self.db.use_streak_freeze(habit["id"]):
            messagebox.showinfo("🧊","Missed day forgiven — streak protected!")
        else:
            messagebox.showinfo("🧊","Your streak isn't at risk right now.")
        self._refresh()

    def _archive(self,habit):
        self.db.archive_habit(habit["id"]); self.selected_habit=None; self._refresh()

    def _delete(self,habit):
        if messagebox.askyesno("Delete",f"Delete '{habit['name']}'?",parent=self.root):
            self.db.delete_habit(habit["id"]); self.selected_habit=None; self._refresh()

    def _set_challenge(self,habit):
        self.db.set_daily_challenge(habit["id"],self.user_id)
        messagebox.showinfo("🎯",f"Challenge set: {habit['name']}"); self._refresh()

    def _export_csv(self):
        path=filedialog.asksaveasfilename(defaultextension=".csv",filetypes=[("CSV","*.csv")])
        if path:
            try: self.db.export_to_csv(path,self.user_id); messagebox.showinfo("✅",f"Saved to {path}")
            except Exception as e: messagebox.showerror("Error",str(e))

    def _import_csv(self):
        path=filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if path: n=self.db.import_from_csv(path,self.user_id); messagebox.showinfo("✅",f"Imported {n} habits."); self._refresh()

    def _backup(self):
        path=filedialog.asksaveasfilename(defaultextension=".db",filetypes=[("DB","*.db")])
        if path: self.db.backup_database(path); messagebox.showinfo("✅",f"Backup: {path}")

    def _restore(self):
        path=filedialog.askopenfilename(filetypes=[("DB","*.db")])
        if path:
            if messagebox.askyesno("Restore","Overwrite current data?"):
                self.db.restore_database(path); self._refresh()

    def _add_dialog(self): self._habit_form_dialog()
    def _edit_dialog(self,habit): self._habit_form_dialog(habit)

    def _habit_form_dialog(self,habit=None):
        win=tk.Toplevel(self.root); win.title("Add Habit" if not habit else f"Edit — {habit['name']}")
        win.configure(bg=P["surface"]); win.geometry("460x560"); win.grab_set()
        tk.Label(win,text="✦ "+("New Habit" if not habit else "Edit Habit"),bg=P["surface"],fg=P["gold"],font=("Georgia",15,"bold")).pack(pady=(16,4),padx=20,anchor="w")
        form=tk.Frame(win,bg=P["surface"]); form.pack(fill="both",expand=True,padx=20,pady=8); form.columnconfigure(1,weight=1)
        fields={}
        def row_entry(label,default,r):
            tk.Label(form,text=label,bg=P["surface"],fg=P["subtext"],font=FONT_BODY).grid(row=r,column=0,sticky="w",pady=8)
            e=tk.Entry(form,font=FONT_BODY,bg=P["surface2"],fg=P["text"],relief="flat",insertbackground=P["gold"],highlightbackground=P["border"],highlightthickness=1)
            e.insert(0,default); e.grid(row=r,column=1,sticky="ew",padx=(12,0),pady=8); return e
        fields["name"]=row_entry("Habit Name",habit["name"] if habit else "",0)
        fields["freq"]=row_entry("Frequency",habit["frequency"] if habit else "daily",1)
        fields["goal"]=row_entry("Goal Target",str(habit["goal_target"]) if habit else "30",3)
        fields["remind"]=row_entry("Reminder (HH:MM)",habit["reminder_time"] if habit and habit["reminder_time"] else "",4)
        tk.Label(form,text="Category",bg=P["surface"],fg=P["subtext"],font=FONT_BODY).grid(row=2,column=0,sticky="w",pady=8)
        cat_v=tk.StringVar(value=habit["category"] if habit else "General")
        ttk.Combobox(form,textvariable=cat_v,values=CATEGORIES,state="readonly",font=FONT_BODY).grid(row=2,column=1,sticky="ew",padx=(12,0),pady=8)
        tk.Label(form,text="Color",bg=P["surface"],fg=P["subtext"],font=FONT_BODY).grid(row=5,column=0,sticky="w",pady=8)
        color_v=tk.StringVar(value="Purple")
        if habit:
            for cn,cv in COLORS.items():
                if cv==habit.get("color"): color_v.set(cn); break
        ttk.Combobox(form,textvariable=color_v,values=list(COLORS.keys()),state="readonly",font=FONT_BODY).grid(row=5,column=1,sticky="ew",padx=(12,0),pady=8)
        tk.Label(form,text="Difficulty",bg=P["surface"],fg=P["subtext"],font=FONT_BODY).grid(row=6,column=0,sticky="w",pady=8)
        diff_v=tk.IntVar(value=habit["difficulty"] if habit else 1)
        df=tk.Frame(form,bg=P["surface"]); df.grid(row=6,column=1,sticky="w",padx=(12,0))
        for val,lbl in [(1,"⭐ Easy"),(2,"⭐⭐ Medium"),(3,"⭐⭐⭐ Hard")]:
            tk.Radiobutton(df,text=lbl,variable=diff_v,value=val,bg=P["surface"],fg=P["text"],selectcolor=P["purple_dark"],activebackground=P["surface"],font=FONT_SMALL).pack(side="left",padx=4)
        def save():
            name=fields["name"].get().strip(); freq=fields["freq"].get().strip()
            if not name or not freq: messagebox.showerror("Error","Name and frequency required.",parent=win); return
            goal=int(fields["goal"].get()) if fields["goal"].get().isdigit() else 30
            remind=fields["remind"].get().strip() or None
            color=COLORS.get(color_v.get(),P["purple_light"])
            try:
                if habit: self.db.update_habit(habit["id"],name=name,frequency=freq,category=cat_v.get(),color=color,difficulty=diff_v.get(),goal_target=goal,reminder_time=remind)
                else: self.db.add_habit(name,freq,category=cat_v.get(),color=color,difficulty=diff_v.get(),goal_target=goal,reminder_time=remind,user_id=self.user_id)
                win.destroy(); self._refresh()
            except Exception as e: messagebox.showerror("Error",str(e),parent=win)
        GlowButton(win,"💾  Save Habit",save,accent=P["purple"]).pack(pady=14)

    def _switch_profile_dialog(self):
        win=tk.Toplevel(self.root); win.title("Profiles"); win.configure(bg=P["surface"]); win.geometry("380x400"); win.grab_set()
        tk.Label(win,text="👤 Profiles",bg=P["surface"],fg=P["gold"],font=FONT_HEAD).pack(pady=(16,8),anchor="w",padx=20)
        for u in self.db.get_users():
            row=tk.Frame(win,bg=P["surface2"],highlightbackground=P["gold"] if u["id"]==self.user_id else P["border"],highlightthickness=1)
            row.pack(fill="x",padx=16,pady=4)
            tk.Label(row,text=f"👤 {u['username']}",bg=P["surface2"],fg=P["text"],font=FONT_SUB).pack(side="left",padx=12,pady=10)
            tk.Label(row,text=f"Lv.{u['level']} · {u['xp']}XP",bg=P["surface2"],fg=P["subtext"],font=FONT_SMALL).pack(side="left")
            if u["id"]!=self.user_id: GlowButton(row,"Switch",lambda uid=u["id"]: [win.destroy(),self._switch_user(uid)],accent=P["purple"]).pack(side="right",padx=10)
            else: tk.Label(row,text="● Active",bg=P["surface2"],fg=P["success"],font=FONT_SMALL).pack(side="right",padx=10)
        GlowButton(win,"➕ New Profile",lambda: self._new_profile(win),accent=P["purple_dark"]).pack(pady=12)

    def _new_profile(self,parent=None):
        name=simpledialog.askstring("New Profile","Username:",parent=parent or self.root)
        if name:
            try:
                uid=self.db.add_user(name.strip()); self._switch_user(uid)
                if parent: parent.destroy()
            except Exception as e: messagebox.showerror("Error",str(e))

    def _switch_user(self,uid): self.user_id=uid; self.selected_habit=None; self._refresh()

    def _on_habit_select(self,event):
        sel=self.habit_lb.curselection()
        if not sel: return
        idx=sel[0]
        if idx<len(self._habits_cache): self._open_detail(self._habits_cache[idx])

    def _refresh(self):
        self._habits_cache=self.db.get_habits(self.user_id)
        user=self.db.get_user_by_id(self.user_id)
        if user and hasattr(self,"hdr_user_lbl"):
            self.hdr_user_lbl.config(text=f"👤 {user['username']}  ·  ⭐ Lv.{user['level']}  ·  {user['xp']} XP")
            hs=get_health_score(self._habits_cache)
            self.hdr_score_lbl.config(text=f"💚 {hs['score']}/100  {hs['grade']}",fg=hs["color"])
        self.habit_lb.delete(0,"end")
        for h in self._habits_cache:
            self.habit_lb.insert("end",f"  {'🔥' if h['current_streak']>0 else '○'} {h['name']}")
        pd=get_pet_status(self._habits_cache,self.selected_pet)
        if hasattr(self,"pet_emoji_lbl"):
            self.pet_emoji_lbl.config(text=pd["emoji"])
            self.pet_name_lbl.config(text=f"{pd['pet']['name']} Lv.{pd['level']}")
            self.pet_mood_lbl.config(text=pd["mood"])
        ch=self.db.get_daily_challenge(self.user_id)
        if hasattr(self,"dc_label"):
            if ch:
                self.dc_label.config(text=f"{ch['name']} — {'✅ Done!' if ch['completed'] else '⏳ Pending'}",fg=P["text"])
            else: self.dc_label.config(text="No challenge set",fg=P["subtext"])
        names=[h["name"] for h in self._habits_cache]
        if hasattr(self,"cal_combo"):
            self.cal_combo["values"]=names
            if names and not self.cal_var.get(): self.cal_var.set(names[0])
            self._draw_calendar()
        # Data changed: mark every dynamic tab stale, then rebuild just the one
        # currently on screen. The rest rebuild lazily when the user opens them.
        self._dirty = set(self._tab_refreshers)
        self._refresh_current_tab()

    # REMINDERS
    @staticmethod
    def _reminder_due(habit, now_hhmm, today_iso):
        """Pure check: is this habit due for a reminder at now_hhmm today?"""
        rt = (habit.get("reminder_time") or "").strip()
        if not rt or rt != now_hhmm:
            return False
        if habit.get("archived"):
            return False
        # already completed today -> no nag
        return str(habit.get("last_completed") or "")[:10] != today_iso

    def _start_reminder_loop(self):
        self._check_reminders()

    def _check_reminders(self):
        now = datetime.now()
        now_hhmm = now.strftime("%H:%M")
        today_iso = date.today().isoformat()
        for h in self._habits_cache:
            key = (h["id"], f"{today_iso} {now_hhmm}")
            if key in self._reminded:
                continue
            if self._reminder_due(h, now_hhmm, today_iso):
                self._reminded.add(key)
                self._fire_reminder(h)
        # re-check every 30s so we never miss a minute boundary
        try:
            self.root.after(30000, self._check_reminders)
        except Exception:
            pass

    def _fire_reminder(self, habit):
        title = "⏰ Vitalis Reminder"
        msg = f"Time for '{habit['name']}' — keep your streak alive!"
        # Best-effort native OS toast (optional dependency); never fatal.
        try:
            from plyer import notification
            notification.notify(title=title, message=msg, app_name="Vitalis", timeout=10)
        except Exception:
            pass
        # Guaranteed in-app popup.
        try:
            popup = tk.Toplevel(self.root)
            popup.title("Reminder")
            popup.configure(bg=P["surface2"])
            popup.attributes("-topmost", True)
            popup.geometry(f"320x130+{self.root.winfo_x()+480}+{self.root.winfo_y()+40}")
            tk.Label(popup, text=title, bg=P["surface2"], fg=P["gold"],
                     font=("Georgia", 15, "bold")).pack(pady=(16, 4))
            tk.Label(popup, text=msg, bg=P["surface2"], fg=P["text"], font=FONT_BODY,
                     wraplength=280, justify="center").pack(padx=12)
            GlowButton(popup, "Got it", popup.destroy, accent=P["purple"]).pack(pady=12)
            popup.after(15000, popup.destroy)
        except Exception:
            pass

class HabitTrackerGUI(VitalisApp):
    pass

if __name__=="__main__":
    root=tk.Tk()
    app=VitalisApp(root)
    root.mainloop()
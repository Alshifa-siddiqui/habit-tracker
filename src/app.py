import sys, os, tkinter as tk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import HabitDatabase
from analytics import HabitAnalytics
from gui import HabitTrackerGUI

def main():
    db = HabitDatabase()
    analytics = HabitAnalytics(db)
    user_id = 1
    users = db.get_users()
    print("\n✦ VITALIS — Habit Tracker")
    print("─"*40)
    print("Profiles:")
    for u in users:
        print(f"  {u['id']}. {u['username']}  (Lv.{u['level']} | {u['xp']} XP)")
    print("  N. New profile")
    choice = input("Select: ").strip()
    if choice.lower() == "n":
        name = input("Username: ").strip()
        user_id = db.add_user(name)
        print(f"✅ Profile '{name}' created!")
    elif choice.isdigit():
        uid = int(choice)
        if any(u["id"]==uid for u in users): user_id = uid
    user = db.get_user_by_id(user_id)
    print(f"\n✅ Logged in: {user['username']}  Lv.{user['level']}  {user['xp']} XP")
    ch = db.get_daily_challenge(user_id)
    if ch: print(f"🎯 Challenge: {ch['name']} — {'✅ Done' if ch['completed'] else '⏳ Pending'}")

    while True:
        user = db.get_user_by_id(user_id)
        print(f"\n✦ VITALIS  [{user['username']} | Lv.{user['level']}]")
        print("─"*40)
        menu = [
            ("1","➕ Add habit"),("2","📋 Show habits"),("3","✅ Check in"),
            ("4","📊 Analytics"),("5","🏥 Health insights"),("6","🔥 Streak freeze"),
            ("7","🏅 Badges"),("8","🎯 Daily challenge"),("9","📈 Plot progress"),
            ("10","🌡️  Heatmap"),("11","⚔️  Compare habits"),("12","📤 Export CSV"),
            ("13","📥 Import CSV"),("14","💾 Backup"),("15","🔄 Restore"),
            ("16","🗃️  Archive habit"),("17","✏️  Edit habit"),("18","🗑️  Delete habit"),
            ("19","🖥️  Launch GUI"),("20","👤 Switch profile"),("0","👋 Exit"),
        ]
        for k,v in menu: print(f"  {k:>2}. {v}")
        print("─"*40)
        c = input("Choice: ").strip()

        if c == "1":
            name=input("Name: ").strip(); freq=input("Frequency (daily/weekly/monthly): ").strip()
            cat=input("Category [General]: ").strip() or "General"
            diff=input("Difficulty 1-3 [1]: ").strip(); diff=int(diff) if diff in["1","2","3"] else 1
            goal=input("Goal target [30]: ").strip(); goal=int(goal) if goal.isdigit() else 30
            try: db.add_habit(name,freq,category=cat,difficulty=diff,goal_target=goal,user_id=user_id); print(f"✅ '{name}' added!")
            except Exception as e: print(f"❌ {e}")

        elif c == "2":
            habits=db.get_habits(user_id)
            if habits:
                print(f"\n  {'ID':<5}{'Name':<22}{'Freq':<12}{'Cat':<12}{'Streak':<8}{'Done'}")
                print("  "+"-"*65)
                for h in habits: print(f"  {h['id']:<5}{h['name']:<22}{h['frequency']:<12}{h['category']:<12}{h['current_streak']:<8}{h['completed_count']}")
            else: print("❌ No habits.")

        elif c == "3":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']} (streak: {h['current_streak']})")
            hid=input("Habit ID: ").strip()
            if hid.isdigit():
                note=input("Note (optional): ").strip() or None
                try:
                    xp,new_badges=db.check_habit(int(hid),note=note,user_id=user_id)
                    u=db.get_user_by_id(user_id)
                    print(f"✅ +{xp} XP  (Total: {u['xp']} | Lv.{u['level']})")
                    for b in new_badges: print(f"🏅 Badge: {b}")
                except Exception as e: print(f"❌ {e}")

        elif c == "4":
            print(analytics.generate_report(user_id))

        elif c == "5":
            from medical import get_medical_insight, get_health_score, MEDICAL_DISCLAIMER
            habits=db.get_habits(user_id)
            hs=get_health_score(habits)
            print(f"\n{MEDICAL_DISCLAIMER}")
            print(f"\n💚 Health Score: {hs['score']}/100  Grade: {hs['grade']}")
            for h in habits:
                insight=get_medical_insight(h["name"],min(h["completed_count"],100))
                if insight:
                    print(f"\n  {h['name']}  [{insight['status']}]")
                    print(f"  {insight['headline']}")
                    for b in insight.get("benefits",[])[:2]: print(f"    ✅ {b}")
                    for r in insight.get("risks",[])[:2]: print(f"    {r}")

        elif c == "6":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']} (freezes: {h['streak_freeze']})")
            hid=input("Habit ID: ").strip()
            if hid.isdigit():
                print("  A. Use freeze  B. Add freeze")
                sub=input("Choice: ").strip().upper()
                if sub=="A":
                    if db.use_streak_freeze(int(hid)): print("🧊 Streak protected!")
                    else: print("❌ No freezes available.")
                elif sub=="B": db.add_streak_freeze(int(hid)); print("✅ Freeze added!")

        elif c == "7":
            badges=db.get_badges(user_id)
            if badges:
                for b,e in badges: print(f"  {b}  ({e[:10]})")
            else: print("No badges yet!")

        elif c == "8":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']}")
            hid=input("Set challenge ID: ").strip()
            if hid.isdigit():
                db.set_daily_challenge(int(hid),user_id)
                h=db.get_habit_by_id(int(hid)); print(f"🎯 Challenge: {h['name']}")

        elif c in ["9","10"]:
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']}")
            hid=input("Habit ID: ").strip()
            if hid.isdigit():
                if c=="9": analytics.plot_habit_progress(int(hid))
                else: analytics.plot_heatmap(int(hid))

        elif c == "11":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']}")
            h1=input("First ID: ").strip(); h2=input("Second ID: ").strip()
            if h1.isdigit() and h2.isdigit():
                data=analytics.compare_habits(int(h1),int(h2))
                if data:
                    for name,stats in data.items():
                        print(f"\n  {name}:")
                        for k,v in stats.items(): print(f"    {k}: {v}")

        elif c == "12":
            path=input("Export path (.csv): ").strip()
            try: db.export_to_csv(path,user_id); print(f"✅ Exported: {path}")
            except Exception as e: print(f"❌ {e}")

        elif c == "13":
            path=input("CSV path: ").strip()
            if os.path.exists(path): n=db.import_from_csv(path,user_id); print(f"✅ Imported {n}")
            else: print("❌ File not found.")

        elif c == "14":
            path=input("Backup path (.db): ").strip(); db.backup_database(path); print(f"✅ Backup: {path}")

        elif c == "15":
            path=input("Restore from: ").strip()
            if os.path.exists(path): db.restore_database(path); print("✅ Restored.")
            else: print("❌ Not found.")

        elif c == "16":
            habits=db.get_habits(user_id,include_archived=True)
            for h in habits: print(f"  {h['id']}. {h['name']} [{'ARCHIVED' if h['archived'] else 'active'}]")
            hid=input("ID: ").strip()
            if hid.isdigit():
                h=db.get_habit_by_id(int(hid))
                if h:
                    if h["archived"]: db.unarchive_habit(int(hid)); print("✅ Unarchived.")
                    else: db.archive_habit(int(hid)); print("🗃 Archived.")

        elif c == "17":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']}")
            hid=input("ID to edit: ").strip()
            if hid.isdigit():
                h=db.get_habit_by_id(int(hid))
                if h:
                    new_name=input(f"Name [{h['name']}]: ").strip() or h['name']
                    new_freq=input(f"Frequency [{h['frequency']}]: ").strip() or h['frequency']
                    new_cat=input(f"Category [{h['category']}]: ").strip() or h['category']
                    db.update_habit(int(hid),name=new_name,frequency=new_freq,category=new_cat)
                    print("✅ Updated.")

        elif c == "18":
            habits=db.get_habits(user_id)
            for h in habits: print(f"  {h['id']}. {h['name']}")
            hid=input("Habit ID to delete: ").strip()
            if hid.isdigit():
                h=db.get_habit_by_id(int(hid))
                if h and input(f"Delete '{h['name']}'? (yes/no): ").strip().lower()=="yes":
                    db.delete_habit(int(hid)); print("🗑️ Deleted.")

        elif c == "19":
            print("🖥️ Launching Vitalis GUI...")
            root=tk.Tk()
            app=HabitTrackerGUI(root,user_id=user_id)
            root.mainloop()
            user=db.get_user_by_id(user_id)

        elif c == "20":
            users=db.get_users()
            for u in users: print(f"  {u['id']}. {u['username']}")
            uid=input("Switch to ID: ").strip()
            if uid.isdigit() and any(u["id"]==int(uid) for u in users):
                user_id=int(uid); print(f"✅ Switched to {db.get_user_by_id(user_id)['username']}")

        elif c == "0":
            print("👋 Goodbye!"); sys.exit()
        else:
            print("⚠️ Invalid choice.")

if __name__=="__main__":
    main()
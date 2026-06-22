import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta, date
from collections import Counter
from database import HabitDatabase

class HabitAnalytics:
    def __init__(self):
        self.db = HabitDatabase()

    def get_longest_streak(self, habit_id):
        history = self.db.get_habit_history(habit_id)
        if not history: return 0
        try:
            dates = sorted(set([datetime.strptime(str(e[3]),"%Y-%m-%d").date() for e in history]))
        except: return 0
        if not dates: return 0
        streaks=[]; streak=1
        for i in range(len(dates)-1):
            if (dates[i+1]-dates[i]).days in [1,7]: streak+=1
            else: streaks.append(streak); streak=1
        streaks.append(streak)
        return max(streaks)

    def get_completion_rate(self, habit_id, period="monthly"):
        today = date.today()
        start = today-timedelta(days=7) if period=="weekly" else today.replace(day=1)
        total = 7 if period=="weekly" else today.day
        self.db.cursor.execute("SELECT COUNT(*) FROM habit_history WHERE habit_id=? AND completed_date>=? AND completed_date<=?",(habit_id,start,today))
        count = self.db.cursor.fetchone()[0]
        return round((count/total)*100,1) if total>0 else 0.0

    def get_best_day_of_week(self, habit_id):
        dates = self.db.get_history_dates(habit_id)
        if not dates: return "No data"
        days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        counts=Counter()
        for d in dates:
            try: counts[datetime.strptime(str(d),"%Y-%m-%d").weekday()]+=1
            except: pass
        if not counts: return "No data"
        return days[max(counts,key=counts.get)]

    def get_most_consistent_habits(self, top_n=3, user_id=1):
        habits=self.db.get_habits(user_id)
        if not habits: return []
        return sorted([(h['name'],len(self.db.get_habit_history(h['id']))) for h in habits],key=lambda x:x[1],reverse=True)[:top_n]

    def get_habits_needing_improvement(self, bottom_n=3, user_id=1):
        habits=self.db.get_habits(user_id)
        if not habits: return []
        return sorted([(h['name'],len(self.db.get_habit_history(h['id']))) for h in habits],key=lambda x:x[1])[:bottom_n]

    def compare_habits(self, habit_id_1, habit_id_2):
        h1=self.db.get_habit_by_id(habit_id_1); h2=self.db.get_habit_by_id(habit_id_2)
        if not h1 or not h2: return None
        return {
            h1['name']:{"check_ins":len(self.db.get_habit_history(habit_id_1)),"current_streak":h1['current_streak'],"longest_streak":h1['longest_streak'],"weekly_rate":self.get_completion_rate(habit_id_1,"weekly"),"monthly_rate":self.get_completion_rate(habit_id_1,"monthly"),"best_day":self.get_best_day_of_week(habit_id_1)},
            h2['name']:{"check_ins":len(self.db.get_habit_history(habit_id_2)),"current_streak":h2['current_streak'],"longest_streak":h2['longest_streak'],"weekly_rate":self.get_completion_rate(habit_id_2,"weekly"),"monthly_rate":self.get_completion_rate(habit_id_2,"monthly"),"best_day":self.get_best_day_of_week(habit_id_2)},
        }

    def plot_heatmap(self, habit_id, weeks=20):
        dates_raw=self.db.get_history_dates(habit_id); habit=self.db.get_habit_by_id(habit_id)
        if not habit: return
        done=set()
        for d in dates_raw:
            try: done.add(datetime.strptime(str(d),"%Y-%m-%d").date())
            except: pass
        today=date.today(); start=today-timedelta(weeks=weeks); start-=timedelta(days=start.weekday())
        grid=np.zeros((7,weeks)); d=start
        for col in range(weeks):
            for row in range(7):
                if d in done: grid[row][col]=1
                d+=timedelta(days=1)
        fig,ax=plt.subplots(figsize=(weeks*0.5,4)); fig.patch.set_facecolor("#0D0D1A"); ax.set_facecolor("#0D0D1A")
        colors=["#1A1A38", habit.get("color","#9D4EDD")]
        from matplotlib.colors import ListedColormap
        cmap=ListedColormap(colors)
        ax.imshow(grid,cmap=cmap,aspect="auto",vmin=0,vmax=1)
        ax.set_yticks(range(7)); ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],color="#9B8EC4")
        ax.set_xticks([]); ax.set_title(f"Habit Heatmap — {habit['name']}",color="#FFD700")
        ax.tick_params(colors="#9B8EC4"); plt.tight_layout(); plt.show()

    def plot_habit_progress(self, habit_id):
        history=self.db.get_habit_history(habit_id); habit=self.db.get_habit_by_id(habit_id)
        if not history or not habit: print("No data."); return
        dates=[]
        for e in history:
            try: dates.append(datetime.strptime(str(e[3]),"%Y-%m-%d").date())
            except: pass
        counts=Counter(dates)
        fig,ax=plt.subplots(figsize=(12,5)); fig.patch.set_facecolor("#0D0D1A"); ax.set_facecolor("#13132B")
        ax.bar(counts.keys(),counts.values(),color=habit.get("color","#9D4EDD"))
        ax.set_xlabel("Date",color="#9B8EC4"); ax.set_ylabel("Check-ins",color="#9B8EC4")
        ax.set_title(f"Progress — {habit['name']}",color="#FFD700")
        ax.tick_params(colors="#9B8EC4"); plt.xticks(rotation=45); plt.tight_layout(); plt.show()

    def plot_comparison(self, habit_id_1, habit_id_2):
        data=self.compare_habits(habit_id_1,habit_id_2)
        if not data: return
        names=list(data.keys()); metrics=["check_ins","current_streak","longest_streak"]
        labels=["Check-ins","Current Streak","Longest Streak"]; x=np.arange(len(labels)); w=0.35
        fig,ax=plt.subplots(figsize=(10,6)); fig.patch.set_facecolor("#0D0D1A"); ax.set_facecolor("#13132B")
        ax.bar(x-w/2,[data[names[0]][m] for m in metrics],w,label=names[0],color="#9D4EDD")
        ax.bar(x+w/2,[data[names[1]][m] for m in metrics],w,label=names[1],color="#FFD700")
        ax.set_xticks(x); ax.set_xticklabels(labels,color="#9B8EC4"); ax.legend()
        ax.set_title("Habit Comparison",color="#FFD700"); ax.tick_params(colors="#9B8EC4")
        plt.tight_layout(); plt.show()

    def generate_report(self, user_id=1):
        habits=self.db.get_habits(user_id)
        if not habits: return "No habits found."
        report="✦ VITALIS HABIT REPORT\n"+"═"*44+"\n\n"
        for h in habits:
            hid=h['id']
            report+=f"🔹 {h['name']}  [{h['category']}]\n"
            report+=f"   Frequency    : {h['frequency']}\n"
            report+=f"   Difficulty   : {'⭐'*h['difficulty']}\n"
            report+=f"   Check-ins    : {h['completed_count']}/{h['goal_target']}\n"
            report+=f"   Streak       : {h['current_streak']} days (best: {h['longest_streak']})\n"
            report+=f"   Weekly Rate  : {self.get_completion_rate(hid,'weekly')}%\n"
            report+=f"   Monthly Rate : {self.get_completion_rate(hid,'monthly')}%\n"
            report+=f"   Best Day     : {self.get_best_day_of_week(hid)}\n"
            report+=f"   Freezes Left : {h['streak_freeze']}\n\n"
        return report
# lab1.py — Codeforces API version (allowed by robots.txt)
# pip install requests pandas matplotlib wordcloud

import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime, timezone

HANDLE = "tamionv"
SAVE_PATH = "/Users/lauramarin/learningpython/submissions.csv"

def fetch_cf_submissions(handle: str, count: int = 1000) -> pd.DataFrame:
    url = "https://codeforces.com/api/user.status"
    r = requests.get(url, params={"handle": handle, "from": 1, "count": count}, timeout=30)
    r.raise_for_status()
    js = r.json()
    if js.get("status") != "OK":
        raise RuntimeError(js.get("comment", "CF API error"))

    rows = []
    for s in js["result"]:
        sub_id = s.get("id")
        ts = s.get("creationTimeSeconds")
        when = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None
        lang = s.get("programmingLanguage")
        verdict = s.get("verdict") or ""
        time_ms = s.get("timeConsumedMillis")
        mem_b = s.get("memoryConsumedBytes")

        p = s.get("problem", {}) or {}
        contest_id = p.get("contestId")
        idx = p.get("index")
        name = p.get("name") or ""
        tags = p.get("tags", [])

        link_user = f"https://codeforces.com/profile/{handle}"
        if contest_id is not None and idx:
            link_problem = f"https://codeforces.com/contest/{contest_id}/problem/{idx}"
            link_submission = f"https://codeforces.com/contest/{contest_id}/submission/{sub_id}"
            link_contest = f"https://codeforces.com/contest/{contest_id}"
        else:
            link_problem = None
            link_submission = f"https://codeforces.com/submissions/{handle}#submission-{sub_id}"
            link_contest = None

        rows.append({
            "#": sub_id,
            "When": when,
            "Who": handle,
            "Problem": f"{contest_id or ''} {idx or ''} - {name}".strip(),
            "Lang": lang,
            "Verdict": verdict,
            "Time": f"{time_ms} ms" if time_ms is not None else "",
            "Memory": f"{mem_b} B" if mem_b is not None else "",
            "link_submission": link_submission,
            "link_problem": link_problem,
            "link_contest": link_contest,
            "link_user": link_user,
            "problem_tags": tags,
        })

    cols = ["#", "When", "Who", "Problem", "Lang", "Verdict", "Time", "Memory",
            "link_submission", "link_problem", "link_contest", "link_user", "problem_tags"]
    return pd.DataFrame(rows, columns=cols)

def plot_tags_wordcloud(df: pd.DataFrame):
    tags = [t for lst in df["problem_tags"].dropna() for t in (lst if isinstance(lst, list) else [])]
    if not tags:
        print("No tags to plot."); return
    wc = WordCloud(width=1000, height=600, background_color="white").generate(" ".join(tags))
    plt.figure(figsize=(10,6)); plt.imshow(wc); plt.axis("off"); plt.title(f"{HANDLE} — Problem Tags"); plt.show()

def plot_verdicts(df: pd.DataFrame):
    vc = df["Verdict"].fillna("UNKNOWN").astype(str).value_counts()
    plt.figure(figsize=(10,5))
    plt.bar(vc.index, vc.values)
    plt.xticks(rotation=45, ha="right"); plt.ylabel("Count"); plt.title(f"{HANDLE} — Verdicts")
    plt.tight_layout(); plt.show()

if __name__ == "__main__":
    df = fetch_cf_submissions(HANDLE, count=1000)
    print(df.head())
    df.to_csv(SAVE_PATH, index=False)
    print("Saved to:", SAVE_PATH)
    plot_tags_wordcloud(df)
    plot_verdicts(df)
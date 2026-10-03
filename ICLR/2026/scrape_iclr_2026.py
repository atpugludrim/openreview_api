import gzip
import pickle
import getpass
from pathlib import Path

import pandas as pd
import openreview # pip install openreview-py


def main():
    path = Path(".")
    exist_submissions = "iclr_2026_submissions.pkl.gz" in [p.name for p in path.iterdir()]
    if not exist_submissions:
        client = openreview.api.OpenReviewClient(
                baseurl="https://api2.openreview.net",
                username=input("Enter openreview email: "),
                password=getpass.getpass("Enter openreview password:"),
        )
        keyword = input("Enter keyword (currently only handles single word): ")
        keyword = keyword.strip()
        if len(keyword.split()) != 1:
            raise ValueError(f"Cannot handle more than one word keywords at this point (keyword = {keyword})")
        venue_id = "ICLR.cc/2026/Conference"
        submissions = client.get_all_notes(
                invitation=f"{venue_id}/-/Submission",
                details="replies",
        )
        with gzip.open("iclr_2026_submissions.pkl.gz", "wb") as f:
            pickle.dump(submissions, f)
    else:
        keyword = input("Enter keyword (currently only handles single word): ")
        keyword = keyword.strip()
        if len(keyword.split()) != 1:
            raise ValueError(f"Cannot handle more than one word keywords at this point (keyword = {keyword})")
    with gzip.open("iclr_2026_submissions.pkl.gz", "rb") as f:
        submissions = pickle.load(f)
    all_notes = []
    for sub in submissions:
        title = sub.content.get("title", {}).get("value", "")
        abstract = sub.content.get("abstract", {}).get("value", "")
        if keyword.lower() not in title.lower() and keyword.lower() not in abstract.lower():
            continue
        # authors = sub.content.get("authors", {}).get("value", [])
        replies = sub.details["replies"]
        scores = []
        for reply in replies:
            if any(invitation.endswith("Official_Review") for invitation in reply["invitations"]):
                scores.append(reply["content"]["rating"]["value"])
        if len(scores) == 0:
            continue
        avg_scores = sum(scores)/len(scores)
        all_notes.append((title,avg_scores,sub.id))
        print(f"{avg_scores = }")
    titles, scores, ids = list(zip(*sorted(all_notes,key=lambda pair:-pair[1])))
    index = pd.Series(ids, name="ids")
    df = pd.DataFrame(data={"titles":titles,"scores":scores},index=index)
    df.to_csv(f"iclr_{keyword}.csv")
    print(f"Saved in iclr_{keyword}.csv")


if __name__=="__main__":
    main()

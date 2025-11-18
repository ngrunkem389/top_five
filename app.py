from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Simple in-memory storage for submissions
submissions = []

@app.route("/", methods=["GET", "POST"])
def home():
    global submissions
    if request.method == "POST":
        action = request.form.get("action")

        # AI, more specifically, Claude, was used to generate code below for the SUBMIT, LIKE, and COMMENT actions.
        # I prompted it to add functionality for like and comment. It also happened to add functionality for submit, which is good.
        if action == "SUBMIT":
            category = request.form.get("category", "").strip()
            items = [
                request.form.get(f"item{i}", "").strip() for i in range(1, 6)
            ]
            if category and all(items):
                submissions.append({
                    "category": category, 
                    "five": items,
                    "likes": 0,
                    "comments": []
                })
            return redirect("/")
        
        elif action == "LIKE":
            # Add 1 to the like count of a post
            submission_id = int(request.form.get("submission_id", -1))
            if 0 <= submission_id < len(submissions):
                submissions[submission_id]["likes"] = submissions[submission_id].get("likes", 0) + 1
            return redirect("/")
        
        elif action == "COMMENT":
            # Add specified text to the array of comments for a particular post.
            submission_id = int(request.form.get("submission_id", -1))
            comment_text = request.form.get("comment", "").strip()
            if 0 <= submission_id < len(submissions) and comment_text:
                if "comments" not in submissions[submission_id]:
                    submissions[submission_id]["comments"] = []
                submissions[submission_id]["comments"].append(comment_text)
            return redirect("/")
    
    return render_template("index.html", submissions=submissions)

if __name__ == "__main__":
    app.run(debug=True)

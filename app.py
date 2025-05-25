from flask import Flask, render_template, request, url_for
from functools import lru_cache
import requests
app = Flask(__name__)

Github_API = "https://api.github.com/users"
Contribution_API = "https://github-contributions-api.deno.dev"
@lru_cache(maxsize=100)
def get_user_data(username):
    return requests.get(f"{Github_API}/{username}").json()

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form["username"]
        if username:
            user_response = requests.get(f"{Github_API}/{username}")
            repos_response = requests.get(f"{Github_API}/{username}/repos")
            contribution_response = requests.get(f"{Contribution_API}/{username}.json")
            if user_response.status_code == 200:
                user_Data = user_response.json()
                
                #repos = repos_response.json() 
                if repos_response.status_code == 200:
                    repos=[
                        {
                        "name": repo.get("name"),
                        "description": repo.get("description"),
                        "stargazers_count": repo.get("stargazers_count", 0),
                        "html_url": repo.get("html_url")
                        } for repo in repos_response.json()


                    ]
                    total_stars = sum(repo["stargazers_count"] for repo in repos)
                    
                else:
                    repos = []
                    total_stars = 0
                contributions = contribution_response.json() if contribution_response.status_code == 200 else []

                return render_template('index.html',user_data = user_Data, repos=repos, contributions = contributions,  total_stars=total_stars)
            else:
                error = f"user '{username}' not found."
                return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()    

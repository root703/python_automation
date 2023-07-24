import requests

def create_vercel_project(access_token, github_repo):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "name": "My Astro JS Website",  # Set your desired project name here
        "gitRepository": github_repo,
        "framework": "astro"  # Set the framework to "astro" for Astro JS projects
    }
    
    response = requests.post("https://api.vercel.com/v1/projects", headers=headers, json=data)
    return response.json()

def deploy_vercel_project(access_token, project_id):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(f"https://api.vercel.com/v1/projects/{project_id}/deployments", headers=headers)
    return response.json()

if __name__ == "__main__":
    # Replace with your actual Vercel access token and GitHub repository URL
    vercel_access_token = "YOUR_VERCEL_ACCESS_TOKEN"
    github_repo_url = "https://github.com/yourusername/your-astro-js-website.git"

    # Step 1: Create the Vercel project
    project_data = create_vercel_project(vercel_access_token, github_repo_url)
    project_id = project_data["id"]
    print(f"Vercel project created! Project ID: {project_id}")

    # Step 2: Deploy the project
    deploy_data = deploy_vercel_project(vercel_access_token, project_id)
    deployment_url = deploy_data["url"]
    print(f"Vercel project deployed! Deployment URL: {deployment_url}")
